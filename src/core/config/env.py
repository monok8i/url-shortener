"""Shared Pydantic settings base for environment-variable driven config."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ABS_PATH = Path(__file__).parent.parent.parent.parent


class BaseEnvConfig(BaseSettings):
    """Base class for settings that load values from the repository ``.env`` file.

    Subclasses inherit Pydantic settings behavior and automatically read
    environment variables from the project-level ``.env`` file.
    """

    model_config = SettingsConfigDict(
        env_file=ABS_PATH / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
