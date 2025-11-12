"""
Triage Router
=============
Endpoints for triage functionality
"""

from fastapi import APIRouter, HTTPException
from typing import Dict
import uuid
from datetime import datetime

from backend.models.triage import (
    TriageStartRequest,
    InterviewRequest,
    InterviewResponse,
    TriageAnalysisRequest,
    TriageAnalysisResponse,
    TriageSessionResponse,
    InterviewMessage
)
from backend.services.triage_service import TriageService

router = APIRouter(prefix="/triage")

# In-memory session storage (replace with Redis/DB in production)
sessions: Dict[str, Dict] = {}

# Initialize triage service
triage_service = TriageService()


@router.post("/start", response_model=TriageSessionResponse)
async def start_triage(request: TriageStartRequest):
    """Start a new triage session"""
    try:
        session_id = request.session_id or str(uuid.uuid4())

        # Initialize session
        sessions[session_id] = {
            "session_id": session_id,
            "phase": "welcome",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "interview_data": {},
            "messages": []
        }

        return TriageSessionResponse(
            session_id=session_id,
            phase="welcome",
            created_at=sessions[session_id]["created_at"],
            updated_at=sessions[session_id]["updated_at"],
            interview_data={}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/interview", response_model=InterviewResponse)
async def interview(request: InterviewRequest):
    """Continue interview conversation"""
    try:
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        session = sessions[request.session_id]

        # Add user message to history
        user_msg = InterviewMessage(
            role="user",
            content=request.user_message,
            timestamp=datetime.now()
        )
        session["messages"].append(user_msg)

        # Get agent response using service
        agent_response, is_complete = await triage_service.process_interview(
            session_id=request.session_id,
            user_message=request.user_message,
            messages=session["messages"]
        )

        # Add agent message to history
        agent_msg = InterviewMessage(
            role="assistant",
            content=agent_response,
            timestamp=datetime.now()
        )
        session["messages"].append(agent_msg)
        session["updated_at"] = datetime.now()

        if is_complete:
            session["phase"] = "analysis"

        return InterviewResponse(
            session_id=request.session_id,
            agent_message=agent_response,
            is_complete=is_complete,
            messages=session["messages"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", response_model=TriageAnalysisResponse)
async def analyze_triage(request: TriageAnalysisRequest):
    """Perform triage analysis on interview data"""
    try:
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        # Perform analysis using service
        analysis = await triage_service.perform_analysis(
            session_id=request.session_id,
            messages=request.messages
        )

        sessions[request.session_id]["phase"] = "complete"
        sessions[request.session_id]["updated_at"] = datetime.now()

        return analysis

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}", response_model=TriageSessionResponse)
async def get_session(session_id: str):
    """Get triage session information"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    return TriageSessionResponse(
        session_id=session_id,
        phase=session["phase"],
        created_at=session["created_at"],
        updated_at=session["updated_at"],
        interview_data=session.get("interview_data", {})
    )
