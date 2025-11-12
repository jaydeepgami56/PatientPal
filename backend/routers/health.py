"""
Health Check Router
===================
Simple health check endpoints
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    # TODO: Check if models are loaded, DB is connected, etc.
    return {
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }
