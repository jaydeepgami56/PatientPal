"""
Agent Service
=============
Business logic for agent management and queries
"""

from typing import List, Optional, Dict, Any
import time
from datetime import datetime
import os

from agents.medgemma_agent import create_medgemma_agent
from agents.txgemma_agent import create_txgemma_agent
from agents.derm_agent import create_derm_agent
from agents.cxr_agent import create_cxr_agent
from agents.pathology_agent import create_pathology_agent

from backend.models.agent import AgentInfo, AgentQueryResponse, AgentConfigUpdate
from utils.agent_base import BaseHealthcareAgent


class AgentService:
    """Service for managing healthcare AI agents"""

    def __init__(self):
        self._agents: Dict[str, BaseHealthcareAgent] = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all available agents"""
        try:
            self._agents = {
                "MedGemma": create_medgemma_agent(),
                "TxGemma": create_txgemma_agent(),
                "Derm Foundation": create_derm_agent(),
                "CXR Foundation": create_cxr_agent(),
                "Pathology": create_pathology_agent()
            }
        except Exception as e:
            print(f"Warning: Error initializing agents: {e}")
            self._agents = {}

    async def list_agents(self) -> List[AgentInfo]:
        """List all available agents"""
        agents_info = []

        for name, agent in self._agents.items():
            agents_info.append(AgentInfo(
                name=agent.name,
                model_id=agent.model_id,
                model_type=agent.config.model_type,
                description=agent.config.description,
                capabilities=agent.config.capabilities,
                priority=agent.config.priority,
                is_available=agent._is_initialized
            ))

        return agents_info

    async def get_agent(self, agent_name: str) -> Optional[AgentInfo]:
        """Get specific agent information"""
        agent = self._agents.get(agent_name)
        if not agent:
            return None

        return AgentInfo(
            name=agent.name,
            model_id=agent.model_id,
            model_type=agent.config.model_type,
            description=agent.config.description,
            capabilities=agent.config.capabilities,
            priority=agent.config.priority,
            is_available=agent._is_initialized
        )

    async def query_agent(
        self,
        agent_name: str,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        image_data: Optional[str] = None
    ) -> AgentQueryResponse:
        """Query a specific agent"""
        start_time = time.time()

        try:
            agent = self._agents.get(agent_name)
            if not agent:
                return AgentQueryResponse(
                    agent_name=agent_name,
                    query=query,
                    response="",
                    confidence=0.0,
                    processing_time=0.0,
                    timestamp=datetime.now(),
                    error=f"Agent '{agent_name}' not found"
                )

            # Ensure agent is initialized
            if not agent._is_initialized:
                agent.initialize()

            # Process query
            agent_response = agent.process(query, context)

            processing_time = time.time() - start_time

            return AgentQueryResponse(
                agent_name=agent_name,
                query=query,
                response=agent_response.output,
                confidence=agent_response.confidence,
                processing_time=processing_time,
                timestamp=datetime.now(),
                metadata=agent_response.metadata
            )

        except Exception as e:
            return AgentQueryResponse(
                agent_name=agent_name,
                query=query,
                response="",
                confidence=0.0,
                processing_time=time.time() - start_time,
                timestamp=datetime.now(),
                error=str(e)
            )

    async def update_agent_config(
        self,
        agent_name: str,
        config: AgentConfigUpdate
    ) -> bool:
        """Update agent configuration"""
        agent = self._agents.get(agent_name)
        if not agent:
            return False

        # Update configuration
        if config.temperature is not None:
            agent.config.temperature = config.temperature
        if config.max_tokens is not None:
            agent.config.max_tokens = config.max_tokens
        if config.priority is not None:
            agent.config.priority = config.priority

        return True
