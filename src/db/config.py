"""Database connection configuration settings."""

from src.core.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """Database connection settings.

    Attributes:
        DATABASE_URL: Full async PostgreSQL connection string.
        DB_POOL_SIZE: Number of connections to maintain in the pool.
        DB_MAX_OVERFLOW: Maximum overflow connections beyond pool size.
    """

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/url_shortener"
    )
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
