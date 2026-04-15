"""
Router registry — mounts all route modules under the API prefix.
"""

from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.resumes import router as resumes_router
from app.api.routes.vacancies import router as vacancies_router

api_router = APIRouter()

# Mount each router with its sub-prefix
api_router.include_router(health_router, prefix="")
api_router.include_router(auth_router, prefix="")
api_router.include_router(resumes_router, prefix="")
api_router.include_router(vacancies_router, prefix="")
api_router.include_router(recommendations_router, prefix="")
