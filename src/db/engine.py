"""Async SQLAlchemy engine and session management."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config._global import config as app_config

_engine = None
_async_session_factory = None


async def init_db() -> None:
    """Create the async engine and session factory.

    Should be called once during application startup.
    """
    global _engine, _async_session_factory

    db_config = app_config.db
    _engine = create_async_engine(
        db_config.DATABASE_URL,
        pool_size=db_config.DB_POOL_SIZE,
        max_overflow=db_config.DB_MAX_OVERFLOW,
    )
    _async_session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def close_db() -> None:
    """Dispose of the engine and release all connections.

    Should be called once during application shutdown.
    """
    global _engine, _async_session_factory

    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_factory = None


async def get_db() -> AsyncGenerator[AsyncSession]:
    """Yield an async database session for dependency injection.

    Yields:
        An async SQLAlchemy session.

    Raises:
        RuntimeError: If the database has not been initialised.
    """
    if _async_session_factory is None:
        raise RuntimeError("Database not initialised. Call init_db() first.")

    async with _async_session_factory() as session:
        yield session
