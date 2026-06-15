"""URL model for storing shortened URL mappings."""

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class URL(Base):
    """Represents a shortened URL mapping.

    Attributes:
        id: Auto-increment primary key.
        short_code: Unique alphanumeric code used in the short URL path.
        original_url: The original long URL to redirect to.
        clicks: Number of times the short URL has been accessed.
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
    """

    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_code: Mapped[str] = mapped_column(
        String(10), unique=True, index=True, nullable=False
    )
    original_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    clicks: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
