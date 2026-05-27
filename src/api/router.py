"""Top-level API router composition for the backend."""

from fastapi import APIRouter

from .endpoints.healthcheck import router as healthcheck_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(healthcheck_router)

__all__ = ("api_router",)
