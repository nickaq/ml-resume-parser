"""
Health check route — used by Docker and load balancers.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Return service health status."""
    return {"status": "ok"}
