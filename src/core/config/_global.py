"""Global configuration container for the application.

This module lazily instantiates API and database configuration objects and
exposes them through a single shared ``config`` instance.
"""

from functools import cached_property

from src.api.config import Config as APIConfig
from src.db.config import Config as DBConfig


class Config:
    """Aggregate access to all application configuration groups.

    The properties on this class lazily construct the underlying configuration
    models so the rest of the application can depend on one shared entry point.
    """

    @cached_property
    def api(self) -> APIConfig:
        """Return the configuration used by the HTTP API server.

        Returns:
            API configuration object.
        """
        return APIConfig()  # type: ignore

    @cached_property
    def db(self) -> DBConfig:
        """Return the database connection configuration.

        Returns:
            Database configuration object.
        """
        return DBConfig()  # type: ignore


config = Config()
