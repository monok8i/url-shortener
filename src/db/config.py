"""Database connection configuration settings."""

from pydantic import field_validator

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

    @field_validator("DATABASE_URL")
    @classmethod
    def normalise_scheme(cls, v: str) -> str:
        """Convert ``postgres://`` to ``postgresql+asyncpg://``.

        Many cloud providers (Fly.io, Heroku, etc.) expose
        ``postgres://`` URLs.  SQLAlchemy's async driver requires the
        ``postgresql+asyncpg://`` scheme, so we rewrite it here.

        Args:
            v: The raw connection string.

        Returns:
            A connection string with the async-compatible scheme.
        """
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        if v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v
