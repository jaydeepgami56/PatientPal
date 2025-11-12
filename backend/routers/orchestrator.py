"""
Orchestrator Router
===================
Endpoints for lead agent orchestrator (multi-agent coordination)
"""

from fastapi import APIRouter, HTTPException

from backend.models.orchestrator import (
    OrchestratorQueryRequest,
    OrchestratorQueryResponse
)
from backend.services.orchestrator_service import OrchestratorService

router = APIRouter(prefix="/orchestrator")

# Initialize orchestrator service
orchestrator_service = OrchestratorService()


@router.post("/query", response_model=OrchestratorQueryResponse)
async def query_orchestrator(request: OrchestratorQueryRequest):
    """
    Query the lead agent orchestrator.
    It will intelligently route to appropriate specialist agents.
    """
    try:
        response = await orchestrator_service.process_query(
            query=request.query,
            context=request.context,
            image_data=request.image_data,
            show_routing=request.show_routing
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memory/summary")
async def get_memory_summary():
    """Get memory system summary"""
    try:
        summary = orchestrator_service.get_memory_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/memory/clear")
async def clear_memory():
    """Clear orchestrator memory"""
    try:
        orchestrator_service.clear_memory()
        return {"status": "success", "message": "Memory cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
