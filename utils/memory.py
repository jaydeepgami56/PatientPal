"""
Three-Tier Memory System for Multi-Agent Orchestration
======================================================
Based on AWS Agent Squad pattern for managing context across user, orchestrator, and specialist agents.
All data models use Pydantic for validation.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Single message in conversation with Pydantic validation"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="When message was created")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Optional metadata")

    class Config:
        arbitrary_types_allowed = True


class AgentConsultation(BaseModel):
    """Record of a consultation with a specialist agent"""
    agent_name: str = Field(..., description="Name of consulted agent")
    query: str = Field(..., description="Query sent to agent")
    response: str = Field(..., description="Agent's response")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence")
    processing_time: float = Field(..., ge=0.0, description="Processing time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


class OrchestrationEvent(BaseModel):
    """Record of an orchestration decision"""
    query: str = Field(..., description="User query")
    routing_decision: Dict[str, Any] = Field(..., description="Routing decision details")
    agents_consulted: List[str] = Field(default_factory=list)
    execution_mode: str = Field(..., description="single, parallel, or sequential")
    total_processing_time: float = Field(..., ge=0.0)
    timestamp: datetime = Field(default_factory=datetime.now)
    success: bool = Field(default=True)
    error: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class ThreeTierMemory:
    """
    Three-tier memory system for orchestrator

    Tier 1: User ↔ Lead Agent conversation history
    Tier 2: Lead Agent ↔ Specialist Agent consultations
    Tier 3: Orchestration audit trail
    """

    def __init__(self):
        # Tier 1: Conversation between user and lead agent
        self.conversation_history: List[Message] = []

        # Tier 2: Consultations with specialist agents
        self.agent_consultations: Dict[str, List[AgentConsultation]] = {}

        # Tier 3: Orchestration events (audit trail)
        self.orchestration_log: List[OrchestrationEvent] = []

    # ========================================================================
    # TIER 1: User ↔ Lead Agent Conversation
    # ========================================================================

    def add_user_message(self, content: str, metadata: Optional[Dict] = None) -> Message:
        """
        Add user message to conversation history

        Args:
            content: Message content
            metadata: Optional metadata

        Returns:
            Message: Pydantic-validated message object
        """
        message = Message(
            role="user",
            content=content,
            metadata=metadata or {}
        )
        self.conversation_history.append(message)
        return message

    def add_assistant_message(self, content: str, metadata: Optional[Dict] = None) -> Message:
        """
        Add assistant message to conversation history

        Args:
            content: Response content
            metadata: Optional metadata

        Returns:
            Message: Pydantic-validated message object
        """
        message = Message(
            role="assistant",
            content=content,
            metadata=metadata or {}
        )
        self.conversation_history.append(message)
        return message

    def get_conversation_history(self, max_messages: Optional[int] = None) -> List[Message]:
        """
        Get conversation history, optionally limited to recent messages

        Args:
            max_messages: Maximum number of recent messages to return

        Returns:
            List[Message]: Recent conversation messages
        """
        if max_messages is None:
            return self.conversation_history
        return self.conversation_history[-max_messages:]

    def get_context_summary(self, max_messages: int = 5) -> str:
        """
        Get formatted summary of recent conversation for context

        Args:
            max_messages: Number of recent messages to include

        Returns:
            str: Formatted conversation context
        """
        recent = self.get_conversation_history(max_messages)
        if not recent:
            return "No previous conversation."

        summary_lines = []
        for msg in recent:
            summary_lines.append(f"{msg.role.capitalize()}: {msg.content}")

        return "\n".join(summary_lines)

    # ========================================================================
    # TIER 2: Lead Agent ↔ Specialist Agents
    # ========================================================================

    def log_agent_consultation(
        self,
        agent_name: str,
        query: str,
        response: str,
        confidence: float,
        processing_time: float,
        metadata: Optional[Dict] = None
    ) -> AgentConsultation:
        """
        Log consultation with a specialist agent

        Args:
            agent_name: Name of consulted agent
            query: Query sent to agent
            response: Agent's response
            confidence: Response confidence score
            processing_time: Time taken to process
            metadata: Optional metadata

        Returns:
            AgentConsultation: Pydantic-validated consultation record
        """
        consultation = AgentConsultation(
            agent_name=agent_name,
            query=query,
            response=response,
            confidence=confidence,
            processing_time=processing_time,
            metadata=metadata or {}
        )

        if agent_name not in self.agent_consultations:
            self.agent_consultations[agent_name] = []

        self.agent_consultations[agent_name].append(consultation)
        return consultation

    def get_agent_consultations(self, agent_name: str) -> List[AgentConsultation]:
        """
        Get all consultations for a specific agent

        Args:
            agent_name: Name of agent

        Returns:
            List[AgentConsultation]: All consultations with this agent
        """
        return self.agent_consultations.get(agent_name, [])

    def get_recent_consultation(self, agent_name: str) -> Optional[AgentConsultation]:
        """
        Get most recent consultation with a specific agent

        Args:
            agent_name: Name of agent

        Returns:
            Optional[AgentConsultation]: Most recent consultation or None
        """
        consultations = self.get_agent_consultations(agent_name)
        return consultations[-1] if consultations else None

    def get_all_consultations_summary(self) -> str:
        """
        Get summary of all agent consultations

        Returns:
            str: Formatted summary of consultations
        """
        if not self.agent_consultations:
            return "No agent consultations yet."

        summary_lines = []
        for agent_name, consultations in self.agent_consultations.items():
            summary_lines.append(f"{agent_name}: {len(consultations)} consultation(s)")

        return "\n".join(summary_lines)

    # ========================================================================
    # TIER 3: Orchestration Audit Trail
    # ========================================================================

    def log_orchestration_event(
        self,
        query: str,
        routing_decision: Dict[str, Any],
        agents_consulted: List[str],
        execution_mode: str,
        total_processing_time: float,
        success: bool = True,
        error: Optional[str] = None
    ) -> OrchestrationEvent:
        """
        Log an orchestration event to audit trail

        Args:
            query: User query
            routing_decision: Routing decision details
            agents_consulted: List of agent names consulted
            execution_mode: How agents were executed (single/parallel/sequential)
            total_processing_time: Total time for orchestration
            success: Whether orchestration succeeded
            error: Error message if failed

        Returns:
            OrchestrationEvent: Pydantic-validated event record
        """
        event = OrchestrationEvent(
            query=query,
            routing_decision=routing_decision,
            agents_consulted=agents_consulted,
            execution_mode=execution_mode,
            total_processing_time=total_processing_time,
            success=success,
            error=error
        )

        self.orchestration_log.append(event)
        return event

    def get_orchestration_log(self, max_events: Optional[int] = None) -> List[OrchestrationEvent]:
        """
        Get orchestration event log

        Args:
            max_events: Maximum number of recent events to return

        Returns:
            List[OrchestrationEvent]: Recent orchestration events
        """
        if max_events is None:
            return self.orchestration_log
        return self.orchestration_log[-max_events:]

    def get_orchestration_stats(self) -> Dict[str, Any]:
        """
        Get statistics about orchestration performance

        Returns:
            Dict: Statistics summary
        """
        if not self.orchestration_log:
            return {
                "total_queries": 0,
                "success_rate": 0.0,
                "avg_processing_time": 0.0,
                "agents_used": []
            }

        total = len(self.orchestration_log)
        successful = sum(1 for e in self.orchestration_log if e.success)
        avg_time = sum(e.total_processing_time for e in self.orchestration_log) / total

        # Collect all unique agents used
        all_agents = set()
        for event in self.orchestration_log:
            all_agents.update(event.agents_consulted)

        return {
            "total_queries": total,
            "successful_queries": successful,
            "failed_queries": total - successful,
            "success_rate": successful / total if total > 0 else 0.0,
            "avg_processing_time": avg_time,
            "agents_used": sorted(list(all_agents))
        }

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def clear_all(self):
        """Clear all memory tiers (use with caution)"""
        self.conversation_history = []
        self.agent_consultations = {}
        self.orchestration_log = []

    def clear_conversation(self):
        """Clear only conversation history (Tier 1)"""
        self.conversation_history = []

    def get_full_context(self, max_messages: int = 10) -> Dict[str, Any]:
        """
        Get comprehensive context across all tiers

        Args:
            max_messages: Number of recent conversation messages

        Returns:
            Dict: Complete context summary
        """
        return {
            "conversation": self.get_context_summary(max_messages),
            "consultations": self.get_all_consultations_summary(),
            "stats": self.get_orchestration_stats()
        }

    def export_to_dict(self) -> Dict[str, Any]:
        """
        Export all memory to dictionary format for serialization

        Returns:
            Dict: Complete memory state
        """
        return {
            "conversation_history": [msg.dict() for msg in self.conversation_history],
            "agent_consultations": {
                agent: [consult.dict() for consult in consultations]
                for agent, consultations in self.agent_consultations.items()
            },
            "orchestration_log": [event.dict() for event in self.orchestration_log]
        }

    def get_memory_size(self) -> Dict[str, int]:
        """
        Get size of each memory tier

        Returns:
            Dict: Count of items in each tier
        """
        total_consultations = sum(len(consults) for consults in self.agent_consultations.values())

        return {
            "conversation_messages": len(self.conversation_history),
            "agent_consultations": total_consultations,
            "orchestration_events": len(self.orchestration_log),
            "unique_agents_consulted": len(self.agent_consultations)
        }
