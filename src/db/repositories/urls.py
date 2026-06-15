"""Repository for URL CRUD operations."""

import secrets
import string

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.url import URL

ALPHABET: str = string.ascii_letters + string.digits
SHORT_CODE_LENGTH: int = 7


def _generate_short_code() -> str:
    """Generate a random alphanumeric short code.

    Returns:
        A random string of length ``SHORT_CODE_LENGTH``.
    """
    return "".join(secrets.choice(ALPHABET) for _ in range(SHORT_CODE_LENGTH))


class URLRepository:
    """Handles database operations for the ``URL`` model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the repository with a database session.

        Args:
            session: An active async SQLAlchemy session.
        """
        self.session = session

    async def create(self, original_url: str) -> URL:
        """Create a new shortened URL entry.

        Args:
            original_url: The long URL to shorten.

        Returns:
            The newly created URL record.

        Raises:
            RuntimeError: If a unique short code cannot be generated.
        """
        for _ in range(5):
            short_code = _generate_short_code()
            existing = await self._get_by_short_code(short_code)
            if existing is None:
                url = URL(
                    short_code=short_code,
                    original_url=original_url,
                )
                self.session.add(url)
                await self.session.commit()
                await self.session.refresh(url)
                return url

        raise RuntimeError("Could not generate a unique short code")

    async def _get_by_short_code(self, short_code: str) -> URL | None:
        """Look up a URL by its short code (no click increment).

        Args:
            short_code: The short code to look up.

        Returns:
            The URL record if found, else ``None``.
        """
        result = await self.session.execute(
            select(URL).where(URL.short_code == short_code)
        )
        return result.scalar_one_or_none()

    async def get_by_short_code(self, short_code: str) -> URL | None:
        """Look up a URL by its short code and increment the click counter.

        Args:
            short_code: The short code to look up.

        Returns:
            The URL record if found, else ``None``.
        """
        url = await self._get_by_short_code(short_code)
        if url is not None:
            url.clicks += 1
            await self.session.commit()
        return url

    async def get_stats(self, short_code: str) -> URL | None:
        """Look up a URL by short code without incrementing clicks.

        Args:
            short_code: The short code to look up.

        Returns:
            The URL record if found, else ``None``.
        """
        return await self._get_by_short_code(short_code)

    async def delete(self, url: URL) -> None:
        """Delete a URL record.

        Args:
            url: The URL record to delete.
        """
        await self.session.delete(url)
        await self.session.commit()

    async def list_all(self) -> list[URL]:
        """Return all URL records ordered by creation date descending.

        Returns:
            A list of all URL records.
        """
        result = await self.session.execute(
            select(URL).order_by(URL.created_at.desc())
        )
        return list(result.scalars().all())
