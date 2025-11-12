"""
Agent API Models
================
Pydantic models for agent endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class AgentInfo(BaseModel):
    """Agent information"""
    name: str
    model_id: str
    model_type: str
    description: str
    capabilities: List[str]
    priority: int
    is_available: bool = True


class AgentQueryRequest(BaseModel):
    """Request to query a specific agent"""
    agent_name: str = Field(..., description="Name of the agent to query")
    query: str = Field(..., description="User query")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    image_data: Optional[str] = Field(None, description="Base64 encoded image if needed")


class AgentQueryResponse(BaseModel):
    """Response from agent query"""
    agent_name: str
    query: str
    response: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time: float
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class AgentConfigUpdate(BaseModel):
    """Update agent configuration"""
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1)
    priority: Optional[int] = Field(None, ge=1, le=10)
