"""Healthcheck endpoint."""

from fastapi import APIRouter

router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])


@router.get("/")
async def healthcheck():
    return {"success": True}
