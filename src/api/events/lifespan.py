"""Application lifespan hook for startup and shutdown orchestration."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from src.db.engine import close_db, init_db

if TYPE_CHECKING:
    from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: "FastAPI") -> AsyncGenerator[None]:
    """Wrap application startup and shutdown phases.

    Startup initialises the database connection pool. Shutdown disposes of it.

    Args:
        app: FastAPI application instance.

    Yields:
        Nothing. The context manager exists so startup and shutdown hooks can
        be added in a single place when needed.
    """

    await init_db()
    yield
    await close_db()
