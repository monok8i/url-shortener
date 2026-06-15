"""Top-level router composition for the backend."""

from fastapi import APIRouter

from .endpoints.healthcheck import router as healthcheck_router
from .endpoints.urls import router as urls_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(healthcheck_router)

page_router = APIRouter()
page_router.include_router(urls_router)

__all__ = ("api_router", "page_router")
