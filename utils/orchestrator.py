"""
Lead Agent Orchestrator
======================
Implements hybrid Anthropic + AWS Agent Squad pattern for multi-agent coordination.
Uses LLM-based routing, parallel execution, and result synthesis.
All data models use Pydantic for validation.
"""

import re
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.agent_base import BaseHealthcareAgent, AgentResponse
from utils.memory import ThreeTierMemory
from utils.prompts import ROUTER_PROMPT, SYNTHESIS_PROMPT, SAFETY_CHECK_PROMPT
from langchain_openai import ChatOpenAI


class RoutingDecision(BaseModel):
    """Routing decision from orchestrator with Pydantic validation"""
    query: str = Field(..., description="Original user query")
    primary_agent: str = Field(..., description="Primary agent name")
    additional_agents: List[str] = Field(default_factory=list, description="Additional agents for multi-agent consultation")
    execution_mode: Literal["single", "parallel", "sequential"] = Field(default="single", description="How to execute agents")
    requires_image: bool = Field(default=False, description="Whether image is required")
    urgency_level: Literal["emergency", "urgent", "routine"] = Field(default="routine", description="Urgency classification")
    medical_domain: Optional[str] = Field(None, description="Medical specialty/domain")
    reasoning: str = Field(..., description="Why this routing was chosen")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Routing confidence score")
    safety_flags: List[str] = Field(default_factory=list, description="Detected safety red flags")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True


class OrchestratedResponse(BaseModel):
    """Final response from orchestration with Pydantic validation"""
    query: str = Field(..., description="Original user query")
    routing_decision: RoutingDecision = Field(..., description="How query was routed")
    agent_responses: List[AgentResponse] = Field(default_factory=list, description="Responses from consulted agents")
    synthesized_output: str = Field(..., description="Final synthesized response")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence")
    processing_time: float = Field(..., ge=0.0, description="Total processing time in seconds")
    agents_consulted: List[str] = Field(default_factory=list, description="Names of agents consulted")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    error: Optional[str] = Field(None, description="Error message if orchestration failed")

    class Config:
        arbitrary_types_allowed = True


class LeadAgentOrchestrator:
    """
    Lead Agent Orchestrator implementing hybrid Anthropic + AWS pattern

    Features:
    - LLM-based intelligent routing
    - Parallel and sequential agent execution
    - Multi-agent response synthesis
    - Three-tier memory management
    - Safety/emergency detection
    """

    def __init__(self, agents: Dict[str, BaseHealthcareAgent], llm: ChatOpenAI):
        """
        Initialize orchestrator

        Args:
            agents: Dictionary of {agent_name: agent_instance}
            llm: ChatOpenAI instance for routing and synthesis
        """
        self.agents = agents
        self.llm = llm
        self.memory = ThreeTierMemory()

        # Emergency keywords for safety checks
        self.emergency_keywords = [
            "chest pain", "can't breathe", "difficulty breathing",
            "unconscious", "seizure", "stroke", "severe bleeding",
            "choking", "heart attack", "anaphylaxis", "can't move",
            "severe headache", "crushing chest", "shortness of breath"
        ]

    # ========================================================================
    # SAFETY & EMERGENCY DETECTION
    # ========================================================================

    def check_safety(self, query: str) -> Dict[str, Any]:
        """
        Quick keyword-based safety check for emergency red flags

        Args:
            query: User query to check

        Returns:
            Dict with emergency status and detected flags
        """
        query_lower = query.lower()

        detected_flags = [
            keyword for keyword in self.emergency_keywords
            if keyword in query_lower
        ]

        is_emergency = len(detected_flags) > 0

        return {
            "is_emergency": is_emergency,
            "flags": detected_flags,
            "urgency": "emergency" if is_emergency else "routine"
        }

    # ========================================================================
    # QUERY ANALYSIS & ROUTING
    # ========================================================================

    def analyze_query(self, query: str, context: Optional[Dict] = None) -> RoutingDecision:
        """
        LLM-based query analysis and routing decision

        Args:
            query: User query to analyze
            context: Optional context (e.g., has_image, patient_data)

        Returns:
            RoutingDecision: Pydantic-validated routing decision
        """
        # Quick safety check first
        safety_result = self.check_safety(query)

        # If emergency detected, short-circuit to emergency response
        if safety_result["is_emergency"]:
            return RoutingDecision(
                query=query,
                primary_agent="emergency",
                urgency_level="emergency",
                reasoning=f"Emergency keywords detected: {', '.join(safety_result['flags'])}",
                confidence=1.0,
                safety_flags=safety_result["flags"]
            )

        # Prepare context information
        context_str = "No additional context provided."
        if context:
            context_parts = []
            if context.get("has_image"):
                context_parts.append("User has uploaded an image")
            if context.get("image_type"):
                context_parts.append(f"Image type: {context['image_type']}")
            if context.get("patient_data"):
                context_parts.append("Patient context data available")
            if context_parts:
                context_str = ", ".join(context_parts)

        # LLM-based routing for non-emergency queries
        prompt = ROUTER_PROMPT.format(
            query=query,
            context=context_str,
            available_agents=", ".join(self.agents.keys())
        )

        try:
            response = self.llm.invoke(prompt)
            routing = self._parse_routing_response(response.content, query)
            return routing

        except Exception as e:
            # Fallback to default routing if LLM fails
            return RoutingDecision(
                query=query,
                primary_agent="MedGemma",
                reasoning=f"Default routing due to error: {str(e)}",
                confidence=0.5
            )

    def _parse_routing_response(self, llm_response: str, query: str) -> RoutingDecision:
        """
        Parse LLM routing response into structured RoutingDecision

        Args:
            llm_response: Raw LLM response text
            query: Original query

        Returns:
            RoutingDecision: Parsed and validated decision
        """
        # Extract fields using regex
        agent_match = re.search(r'SELECTED_AGENT:\s*(.+)', llm_response)
        additional_match = re.search(r'ADDITIONAL_AGENTS:\s*(.+)', llm_response)
        execution_match = re.search(r'EXECUTION_MODE:\s*(single|parallel|sequential)', llm_response, re.IGNORECASE)
        image_match = re.search(r'REQUIRES_IMAGE:\s*(Yes|No)', llm_response, re.IGNORECASE)
        urgency_match = re.search(r'URGENCY:\s*(emergency|urgent|routine)', llm_response, re.IGNORECASE)
        confidence_match = re.search(r'CONFIDENCE:\s*(High|Medium|Low)', llm_response, re.IGNORECASE)
        reasoning_match = re.search(r'REASONING:\s*(.+)', llm_response)

        # Parse values
        primary_agent = agent_match.group(1).strip() if agent_match else "MedGemma"

        # Parse additional agents
        additional_agents = []
        if additional_match:
            agents_str = additional_match.group(1).strip()
            if agents_str.lower() not in ["none", "n/a", ""]:
                additional_agents = [a.strip() for a in agents_str.split(",")]

        execution_mode = execution_match.group(1).lower() if execution_match else "single"
        requires_image = image_match.group(1).lower() == "yes" if image_match else False
        urgency = urgency_match.group(1).lower() if urgency_match else "routine"

        # Map confidence to numeric
        confidence_map = {"high": 0.9, "medium": 0.7, "low": 0.5}
        confidence_str = confidence_match.group(1).lower() if confidence_match else "medium"
        confidence = confidence_map.get(confidence_str, 0.7)

        reasoning = reasoning_match.group(1).strip() if reasoning_match else "Default routing"

        return RoutingDecision(
            query=query,
            primary_agent=primary_agent,
            additional_agents=additional_agents,
            execution_mode=execution_mode,
            requires_image=requires_image,
            urgency_level=urgency,
            reasoning=reasoning,
            confidence=confidence
        )

    # ========================================================================
    # AGENT EXECUTION
    # ========================================================================

    def execute_single_agent(
        self,
        agent_name: str,
        query: str,
        context: Optional[Dict] = None
    ) -> AgentResponse:
        """
        Execute single specialist agent

        Args:
            agent_name: Name of agent to execute
            query: User query
            context: Optional context data

        Returns:
            AgentResponse: Pydantic-validated response from agent
        """
        agent = self.agents.get(agent_name)

        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found. Available: {list(self.agents.keys())}")

        # Initialize if needed
        if not agent._is_initialized:
            success = agent.initialize()
            if not success:
                raise RuntimeError(f"Failed to initialize agent '{agent_name}'")

        # Validate input
        if not agent.validate_input(query, context):
            raise ValueError(f"Invalid input for agent '{agent_name}'")

        # Process query
        response = agent.process(query, context)

        # Log consultation in memory
        self.memory.log_agent_consultation(
            agent_name=agent_name,
            query=query,
            response=response.output,
            confidence=response.confidence,
            processing_time=response.processing_time,
            metadata=response.metadata
        )

        return response

    def execute_parallel(
        self,
        agent_names: List[str],
        query: str,
        context: Optional[Dict] = None
    ) -> List[AgentResponse]:
        """
        Execute multiple agents in parallel for faster processing

        Args:
            agent_names: List of agent names to execute
            query: User query
            context: Optional context data

        Returns:
            List[AgentResponse]: Responses from all agents
        """
        responses = []
        errors = []

        with ThreadPoolExecutor(max_workers=len(agent_names)) as executor:
            # Submit all agent executions
            futures = {
                executor.submit(self.execute_single_agent, name, query, context): name
                for name in agent_names
            }

            # Collect results as they complete
            for future in as_completed(futures):
                agent_name = futures[future]
                try:
                    response = future.result()
                    responses.append(response)
                except Exception as e:
                    error_msg = f"Error executing {agent_name}: {str(e)}"
                    errors.append(error_msg)
                    print(f"⚠️ {error_msg}")

        # If all agents failed, raise error
        if not responses and errors:
            raise RuntimeError(f"All parallel agents failed: {'; '.join(errors)}")

        return responses

    def execute_sequential(
        self,
        agent_pipeline: List[str],
        query: str,
        context: Optional[Dict] = None
    ) -> List[AgentResponse]:
        """
        Execute agents sequentially, passing output as context to next agent

        Args:
            agent_pipeline: Ordered list of agent names
            query: User query
            context: Initial context

        Returns:
            List[AgentResponse]: Responses from pipeline agents
        """
        responses = []
        current_context = context or {}

        for agent_name in agent_pipeline:
            # Execute agent with accumulated context
            response = self.execute_single_agent(agent_name, query, current_context)
            responses.append(response)

            # Add this agent's output to context for next agent
            current_context[f"{agent_name}_output"] = response.output
            current_context[f"{agent_name}_confidence"] = response.confidence

        return responses

    # ========================================================================
    # RESULT SYNTHESIS
    # ========================================================================

    def synthesize_results(self, responses: List[AgentResponse], query: str) -> str:
        """
        Synthesize multiple agent responses into coherent unified output

        Args:
            responses: List of agent responses to synthesize
            query: Original user query

        Returns:
            str: Synthesized response text
        """
        # If only one response, return it directly
        if len(responses) == 1:
            return responses[0].output

        # Build agent responses dict for synthesis
        agent_outputs = {}
        for response in responses:
            agent_outputs[response.agent_name] = {
                "output": response.output,
                "confidence": f"{response.confidence:.0%}"
            }

        # Format for prompt
        agent_responses_str = "\n\n".join([
            f"**{name}:**\n{data['output']}\n(Confidence: {data['confidence']})"
            for name, data in agent_outputs.items()
        ])

        # Use LLM to synthesize
        prompt = SYNTHESIS_PROMPT.format(
            query=query,
            agent_responses=agent_responses_str
        )

        try:
            synthesized = self.llm.invoke(prompt)
            return synthesized.content
        except Exception as e:
            # Fallback: simple concatenation if synthesis fails
            fallback = f"## Multi-Agent Consultation Results\n\n"
            for response in responses:
                fallback += f"### {response.agent_name}\n{response.output}\n\n"
            fallback += f"\n⚠️ Note: Automatic synthesis failed. Results shown separately."
            return fallback

    # ========================================================================
    # MAIN ORCHESTRATION
    # ========================================================================

    def orchestrate(self, query: str, context: Optional[Dict] = None) -> OrchestratedResponse:
        """
        Main orchestration method - analyzes, routes, executes, and synthesizes

        Args:
            query: User query
            context: Optional context (image, patient data, etc.)

        Returns:
            OrchestratedResponse: Complete orchestrated response with all details
        """
        start_time = datetime.now()

        # Add to conversation memory
        self.memory.add_user_message(query)

        try:
            # Step 1: Analyze query and determine routing
            routing_decision = self.analyze_query(query, context)

            # Step 2: Handle emergency separately
            if routing_decision.urgency_level == "emergency":
                emergency_output = self._generate_emergency_response(routing_decision.safety_flags)

                # Log orchestration event
                processing_time = (datetime.now() - start_time).total_seconds()
                self.memory.log_orchestration_event(
                    query=query,
                    routing_decision=routing_decision.dict(),
                    agents_consulted=[],
                    execution_mode="emergency",
                    total_processing_time=processing_time,
                    success=True
                )

                # Add to conversation memory
                self.memory.add_assistant_message(emergency_output)

                return OrchestratedResponse(
                    query=query,
                    routing_decision=routing_decision,
                    agent_responses=[],
                    synthesized_output=emergency_output,
                    confidence=1.0,
                    processing_time=processing_time,
                    agents_consulted=[],
                    metadata={"emergency": True, "safety_flags": routing_decision.safety_flags}
                )

            # Step 3: Execute agents based on routing decision
            agent_responses = []

            if routing_decision.execution_mode == "single":
                # Single agent execution
                response = self.execute_single_agent(
                    routing_decision.primary_agent, query, context
                )
                agent_responses = [response]

            elif routing_decision.execution_mode == "parallel":
                # Parallel execution of multiple agents
                all_agents = [routing_decision.primary_agent] + routing_decision.additional_agents
                agent_responses = self.execute_parallel(all_agents, query, context)

            elif routing_decision.execution_mode == "sequential":
                # Sequential pipeline execution
                all_agents = [routing_decision.primary_agent] + routing_decision.additional_agents
                agent_responses = self.execute_sequential(all_agents, query, context)

            # Step 4: Synthesize results
            synthesized_output = self.synthesize_results(agent_responses, query)

            # Step 5: Calculate metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            avg_confidence = sum(r.confidence for r in agent_responses) / len(agent_responses) if agent_responses else 0.0
            agents_consulted = [r.agent_name for r in agent_responses]

            # Step 6: Log orchestration event
            self.memory.log_orchestration_event(
                query=query,
                routing_decision=routing_decision.dict(),
                agents_consulted=agents_consulted,
                execution_mode=routing_decision.execution_mode,
                total_processing_time=processing_time,
                success=True
            )

            # Add to conversation memory
            self.memory.add_assistant_message(synthesized_output)

            # Step 7: Build orchestrated response
            return OrchestratedResponse(
                query=query,
                routing_decision=routing_decision,
                agent_responses=agent_responses,
                synthesized_output=synthesized_output,
                confidence=avg_confidence,
                processing_time=processing_time,
                agents_consulted=agents_consulted,
                metadata={
                    "routing_confidence": routing_decision.confidence,
                    "execution_mode": routing_decision.execution_mode,
                    "num_agents": len(agent_responses)
                }
            )

        except Exception as e:
            # Handle errors gracefully
            processing_time = (datetime.now() - start_time).total_seconds()
            error_msg = str(e)

            # Log failed orchestration
            if 'routing_decision' in locals():
                self.memory.log_orchestration_event(
                    query=query,
                    routing_decision=routing_decision.dict() if routing_decision else {},
                    agents_consulted=[],
                    execution_mode="error",
                    total_processing_time=processing_time,
                    success=False,
                    error=error_msg
                )

            return OrchestratedResponse(
                query=query,
                routing_decision=routing_decision if 'routing_decision' in locals() else None,
                agent_responses=[],
                synthesized_output="",
                confidence=0.0,
                processing_time=processing_time,
                agents_consulted=[],
                error=error_msg,
                metadata={"error_type": type(e).__name__}
            )

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _generate_emergency_response(self, flags: List[str]) -> str:
        """
        Generate emergency guidance response

        Args:
            flags: Detected red flags

        Returns:
            str: Emergency response text
        """
        return f"""
🚨 **EMERGENCY DETECTED**

**Red flags identified:** {', '.join(flags)}

## IMMEDIATE ACTION REQUIRED:

### 1. Call 000 (Emergency Services) NOW
Do not delay. Call immediately and provide:
- Your exact location
- The symptoms/condition
- Patient's age and consciousness level

### 2. While Waiting for Ambulance:
- Stay calm and stay with the patient
- Do NOT drive yourself to hospital
- If unconscious: Place in recovery position (on side)
- If chest pain: Sit down, rest, take aspirin if available (unless allergic)
- If choking: Perform Heimlich maneuver or back blows
- If severe bleeding: Apply direct pressure with clean cloth

### 3. Do NOT Wait:
⚠️ **This is a potentially life-threatening situation**
⚠️ **Do NOT wait for a GP appointment**
⚠️ **Do NOT attempt to drive to hospital yourself**

---

**This is an automated emergency detection system. For medical emergencies in Australia, always call 000.**
"""

    def get_memory(self) -> ThreeTierMemory:
        """Get the memory system for access to conversation history"""
        return self.memory

    def get_available_agents(self) -> List[str]:
        """Get list of available agent names"""
        return list(self.agents.keys())

    def get_agent_status(self) -> Dict[str, bool]:
        """Get initialization status of all agents"""
        return {name: agent._is_initialized for name, agent in self.agents.items()}
