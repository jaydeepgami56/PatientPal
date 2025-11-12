"""
Triage API Models
=================
Pydantic models for triage endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class TriageStartRequest(BaseModel):
    """Request to start a new triage session"""
    patient_name: Optional[str] = Field(None, description="Patient name")
    session_id: Optional[str] = Field(None, description="Session ID for resuming")


class InterviewMessage(BaseModel):
    """Chat message in interview"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now)


class InterviewRequest(BaseModel):
    """Request to continue interview"""
    session_id: str = Field(..., description="Triage session ID")
    user_message: str = Field(..., description="User's response")


class InterviewResponse(BaseModel):
    """Response from interview endpoint"""
    session_id: str
    agent_message: str
    is_complete: bool = Field(default=False, description="Whether interview is complete")
    messages: List[InterviewMessage] = Field(default_factory=list)


class TriageAnalysisRequest(BaseModel):
    """Request for triage analysis"""
    session_id: str = Field(..., description="Triage session ID")
    messages: List[InterviewMessage] = Field(..., description="Interview messages")


class TriageAnalysisResponse(BaseModel):
    """Triage analysis result"""
    session_id: str
    ats_category: str = Field(..., description="ATS category (1-5)")
    urgency: str = Field(..., description="Urgency level")
    chief_complaint: str
    symptoms: List[str]
    recommended_action: str
    report: str = Field(..., description="RACGP-compliant report")
    confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TriageSessionResponse(BaseModel):
    """Response with session info"""
    session_id: str
    phase: str = Field(..., description="Current phase: welcome, interview, report, triage")
    created_at: datetime
    updated_at: datetime
    interview_data: Dict[str, Any] = Field(default_factory=dict)
