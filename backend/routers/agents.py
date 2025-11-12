"""
Agents Router
=============
Endpoints for agent management and queries
"""

from fastapi import APIRouter, HTTPException
from typing import List

from backend.models.agent import (
    AgentInfo,
    AgentQueryRequest,
    AgentQueryResponse,
    AgentConfigUpdate
)
from backend.services.agent_service import AgentService

router = APIRouter(prefix="/agents")

# Initialize agent service
agent_service = AgentService()


@router.get("/list", response_model=List[AgentInfo])
async def list_agents():
    """List all available agents"""
    try:
        return await agent_service.list_agents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_name}", response_model=AgentInfo)
async def get_agent(agent_name: str):
    """Get specific agent information"""
    try:
        agent = await agent_service.get_agent(agent_name)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
        return agent
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=AgentQueryResponse)
async def query_agent(request: AgentQueryRequest):
    """Query a specific agent"""
    try:
        response = await agent_service.query_agent(
            agent_name=request.agent_name,
            query=request.query,
            context=request.context,
            image_data=request.image_data
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{agent_name}/config")
async def update_agent_config(agent_name: str, config: AgentConfigUpdate):
    """Update agent configuration"""
    try:
        success = await agent_service.update_agent_config(agent_name, config)
        if not success:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
        return {"status": "success", "message": f"Agent '{agent_name}' configuration updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
