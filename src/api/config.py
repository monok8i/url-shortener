"""API server configuration settings."""

from pydantic import Field

from src.core.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """Host and port used by the API server.

    Attributes:
        API_HOST: Host interface the API server listens on.
        API_PORT: TCP port the API server listens on.
        ALLOW_ORIGINS: List of allowed origins for CORS middleware. If
            empty, CORS is disabled.
        ALLOW_METHODS: List of allowed HTTP methods for CORS. Defaults to
            all standard methods.
        ALLOW_CREDENTIALS: Whether to allow credentials in CORS requests.
            Defaults to True.
        ALLOW_HEADERS: List of allowed HTTP headers for CORS. Defaults to
            allowing all headers.
    """

    API_HOST: str = "0.0.0.0"
    API_PORT: int = Field(default=8000, validation_alias="PORT")
    ALLOW_ORIGINS: list[str] = ["http://localhost:3000"]
    ALLOW_METHODS: list[str] = ["GET", "POST"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_HEADERS: list[str] = ["*"]
