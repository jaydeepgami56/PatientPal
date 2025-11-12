"""
Base Agent Classes and Interfaces
===================================
Provides abstract base classes for healthcare AI agents with LangChain integration.
Each specialist agent inherits from BaseHealthcareAgent.
Uses Pydantic for data validation and structure.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
import logging

logger = logging.getLogger(__name__)


class AgentConfig(BaseModel):
    """Configuration for healthcare agent"""
    name: str = Field(..., description="Unique agent name")
    model_id: str = Field(..., description="Hugging Face model ID or OpenAI model name")
    model_type: str = Field(..., description="Model provider: 'huggingface', 'openai', etc.")
    description: str = Field(..., description="Agent purpose and capabilities")
    capabilities: List[str] = Field(default_factory=list, description="List of agent capabilities")
    priority: int = Field(default=1, ge=1, le=10, description="Agent priority (1-10)")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="LLM temperature")
    max_tokens: int = Field(default=512, ge=1, description="Maximum tokens to generate")
    api_key: Optional[str] = Field(default=None, description="API key if required")

    class Config:
        arbitrary_types_allowed = True


class AgentResponse(BaseModel):
    """Standardized response from healthcare agents"""
    agent_name: str = Field(..., description="Name of agent that generated response")
    timestamp: datetime = Field(default_factory=datetime.now)
    input_query: str = Field(..., description="Original user query")
    output: str = Field(..., description="Agent's response")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = Field(default=None, description="Error message if any")
    processing_time: float = Field(default=0.0, description="Processing time in seconds")

    class Config:
        arbitrary_types_allowed = True


class BaseHealthcareAgent(ABC):
    """
    Abstract base class for all healthcare AI agents.
    Enforces consistent interface across MedGemma, TxGemma, Path Foundation, etc.
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.name = config.name
        self.model_id = config.model_id
        self.logger = logging.getLogger(f"Agent.{self.name}")
        self._llm = None
        self._is_initialized = False

    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the agent's LLM and resources.
        Returns True if successful, False otherwise.
        """
        pass

    @abstractmethod
    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """
        Process a query and return standardized response.

        Args:
            query: User's question or task
            context: Additional context (patient data, images, etc.)

        Returns:
            AgentResponse with results
        """
        pass

    @abstractmethod
    def validate_input(self, query: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate that input is appropriate for this agent.

        Returns:
            True if valid, False otherwise
        """
        pass

    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        return self.config.capabilities

    def get_status(self) -> Dict[str, Any]:
        """Return current agent status"""
        return {
            "name": self.name,
            "model_id": self.model_id,
            "initialized": self._is_initialized,
            "capabilities": self.config.capabilities,
            "priority": self.config.priority
        }

    def shutdown(self):
        """Clean up resources"""
        self.logger.info(f"Shutting down {self.name}")
        self._is_initialized = False


class RoutingDecision(BaseModel):
    """Model for routing decisions"""
    query: str
    selected_agent: str
    reasoning: str
    timestamp: datetime = Field(default_factory=datetime.now)
    processing_time: float = 0.0


class SupervisorAgent:
    """
    Supervisor/Router Agent that coordinates specialist agents.
    Uses LangChain to determine which agent(s) to invoke based on user query.
    """

    def __init__(self, agents: List[BaseHealthcareAgent]):
        self.agents = {agent.name: agent for agent in agents}
        self.logger = logging.getLogger("SupervisorAgent")
        self.routing_history: List[RoutingDecision] = []

    def route_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> RoutingDecision:
        """
        Determine which agent should handle the query.

        Args:
            query: User's question
            context: Additional context

        Returns:
            RoutingDecision with selected agent and reasoning
        """
        start_time = datetime.now()
        query_lower = query.lower()

        # Simple keyword-based routing (can be enhanced with LLM-based routing)
        if any(word in query_lower for word in ['xray', 'x-ray', 'chest', 'cxr', 'lung']):
            selected = 'CXR Foundation'
            reasoning = "Query contains chest X-ray related keywords"
        elif any(word in query_lower for word in ['skin', 'rash', 'dermatology', 'lesion', 'mole']):
            selected = 'Derm Foundation'
            reasoning = "Query contains dermatology related keywords"
        elif any(word in query_lower for word in ['treatment', 'therapy', 'medication', 'prescribe']):
            selected = 'TxGemma'
            reasoning = "Query contains treatment related keywords"
        elif any(word in query_lower for word in ['pathology', 'biopsy', 'tissue', 'histology']):
            selected = 'Path Foundation'
            reasoning = "Query contains pathology related keywords"
        else:
            selected = 'MedGemma'
            reasoning = "Default general medical agent for general queries"

        processing_time = (datetime.now() - start_time).total_seconds()

        return RoutingDecision(
            query=query,
            selected_agent=selected,
            reasoning=reasoning,
            processing_time=processing_time
        )

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """
        Execute query by routing to appropriate agent.

        Args:
            query: User's question
            context: Additional context

        Returns:
            AgentResponse from selected agent
        """
        start_time = datetime.now()

        # Route to appropriate agent
        routing_decision = self.route_query(query, context)
        self.logger.info(f"Routing query to: {routing_decision.selected_agent} - {routing_decision.reasoning}")

        if routing_decision.selected_agent not in self.agents:
            return AgentResponse(
                agent_name="Supervisor",
                timestamp=datetime.now(),
                input_query=query,
                output="",
                confidence=0.0,
                metadata={"routing_decision": routing_decision.dict()},
                error=f"Agent {routing_decision.selected_agent} not found"
            )

        selected_agent = self.agents[routing_decision.selected_agent]

        # Ensure agent is initialized
        if not selected_agent._is_initialized:
            if not selected_agent.initialize():
                return AgentResponse(
                    agent_name=routing_decision.selected_agent,
                    timestamp=datetime.now(),
                    input_query=query,
                    output="",
                    confidence=0.0,
                    metadata={"routing_decision": routing_decision.dict()},
                    error="Agent initialization failed"
                )

        # Validate input
        if not selected_agent.validate_input(query, context):
            return AgentResponse(
                agent_name=routing_decision.selected_agent,
                timestamp=datetime.now(),
                input_query=query,
                output="",
                confidence=0.0,
                metadata={"routing_decision": routing_decision.dict()},
                error="Input validation failed"
            )

        # Process query
        response = selected_agent.process(query, context)

        # Add routing info to metadata
        response.metadata["routing_decision"] = routing_decision.dict()

        # Record routing
        self.routing_history.append(routing_decision)

        return response

    def get_routing_history(self) -> List[Dict[str, Any]]:
        """Return history of routing decisions"""
        return [decision.dict() for decision in self.routing_history]

    def get_available_agents(self) -> List[str]:
        """Return list of available agent names"""
        return list(self.agents.keys())
