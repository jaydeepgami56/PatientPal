"""
Orchestrator API Models
=======================
Pydantic models for lead agent orchestrator endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime


class OrchestratorQueryRequest(BaseModel):
    """Request to orchestrator"""
    query: str = Field(..., description="User query")
    context: Optional[Dict[str, Any]] = Field(None, description="Conversation context")
    image_data: Optional[str] = Field(None, description="Base64 encoded image if needed")
    show_routing: bool = Field(default=False, description="Include routing details in response")


class RoutingInfo(BaseModel):
    """Routing decision information"""
    primary_agent: str
    additional_agents: List[str]
    execution_mode: Literal["single", "parallel", "sequential"]
    requires_image: bool
    urgency_level: Literal["emergency", "urgent", "routine"]
    medical_domain: Optional[str]
    reasoning: str
    confidence: float
    safety_flags: List[str]


class AgentContribution(BaseModel):
    """Individual agent's contribution"""
    agent_name: str
    response: str
    confidence: float
    processing_time: float


class OrchestratorQueryResponse(BaseModel):
    """Response from orchestrator"""
    query: str
    response: str = Field(..., description="Synthesized response")
    confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time: float
    agents_consulted: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)

    # Optional detailed routing info
    routing_info: Optional[RoutingInfo] = None
    agent_contributions: Optional[List[AgentContribution]] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class ConversationHistoryItem(BaseModel):
    """Item in conversation history"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
