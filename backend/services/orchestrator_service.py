"""
Orchestrator Service
====================
Business logic for lead agent orchestrator (multi-agent coordination)
"""

from typing import Optional, Dict, Any
import time
from datetime import datetime
import os

from langchain_openai import ChatOpenAI
from utils.orchestrator import LeadAgentOrchestrator

from agents.medgemma_agent import create_medgemma_agent
from agents.txgemma_agent import create_txgemma_agent
from agents.derm_agent import create_derm_agent
from agents.cxr_agent import create_cxr_agent
from agents.pathology_agent import create_pathology_agent

from backend.models.orchestrator import (
    OrchestratorQueryResponse,
    RoutingInfo,
    AgentContribution
)
from backend.config import settings


class OrchestratorService:
    """Service for orchestrator operations"""

    def __init__(self):
        self._orchestrator: Optional[LeadAgentOrchestrator] = None
        self._initialize_orchestrator()

    def _initialize_orchestrator(self):
        """Initialize the orchestrator with all agents"""
        try:
            # Create orchestrator LLM
            orchestrator_llm = ChatOpenAI(
                temperature=settings.openai_temperature,
                model_name=settings.openai_model,
                openai_api_key=settings.openai_api_key or os.getenv("OPENAI_API_KEY")
            )

            # Create all specialist agents
            agents = {
                "MedGemma": create_medgemma_agent(),
                "TxGemma": create_txgemma_agent(),
                "Derm Foundation": create_derm_agent(),
                "CXR Foundation": create_cxr_agent(),
                "Pathology": create_pathology_agent()
            }

            # Create orchestrator
            self._orchestrator = LeadAgentOrchestrator(
                agents=agents,
                llm=orchestrator_llm
            )

        except Exception as e:
            print(f"Error initializing orchestrator: {e}")
            self._orchestrator = None

    async def process_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        image_data: Optional[str] = None,
        show_routing: bool = False
    ) -> OrchestratorQueryResponse:
        """Process query through orchestrator"""
        start_time = time.time()

        try:
            if not self._orchestrator:
                raise Exception("Orchestrator not initialized")

            # Prepare context
            full_context = context or {}
            if image_data:
                full_context["image_data"] = image_data

            # Process through orchestrator
            result = self._orchestrator.process_query(query, full_context)

            processing_time = time.time() - start_time

            # Build response
            response = OrchestratorQueryResponse(
                query=query,
                response=result.synthesized_output,
                confidence=result.confidence,
                processing_time=processing_time,
                agents_consulted=result.agents_consulted,
                timestamp=datetime.now(),
                metadata=result.metadata
            )

            # Add routing info if requested
            if show_routing and result.routing_decision:
                response.routing_info = RoutingInfo(
                    primary_agent=result.routing_decision.primary_agent,
                    additional_agents=result.routing_decision.additional_agents,
                    execution_mode=result.routing_decision.execution_mode,
                    requires_image=result.routing_decision.requires_image,
                    urgency_level=result.routing_decision.urgency_level,
                    medical_domain=result.routing_decision.medical_domain,
                    reasoning=result.routing_decision.reasoning,
                    confidence=result.routing_decision.confidence,
                    safety_flags=result.routing_decision.safety_flags
                )

                # Add agent contributions
                response.agent_contributions = [
                    AgentContribution(
                        agent_name=agent_resp.agent_name,
                        response=agent_resp.output,
                        confidence=agent_resp.confidence,
                        processing_time=agent_resp.processing_time
                    )
                    for agent_resp in result.agent_responses
                ]

            return response

        except Exception as e:
            return OrchestratorQueryResponse(
                query=query,
                response="",
                confidence=0.0,
                processing_time=time.time() - start_time,
                agents_consulted=[],
                timestamp=datetime.now(),
                error=str(e)
            )

    def get_memory_summary(self) -> Dict[str, Any]:
        """Get memory system summary"""
        if not self._orchestrator:
            return {"error": "Orchestrator not initialized"}

        memory = self._orchestrator.memory
        return {
            "working_memory_size": len(memory.working_memory),
            "short_term_memory_size": len(memory.short_term_memory),
            "long_term_memory_size": len(memory.long_term_memory)
        }

    def clear_memory(self):
        """Clear orchestrator memory"""
        if self._orchestrator:
            self._orchestrator.memory.working_memory.clear()
            self._orchestrator.memory.short_term_memory.clear()
