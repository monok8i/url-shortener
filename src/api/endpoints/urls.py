"""URL shortening and redirect endpoints with HTML rendering."""

from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.templates import templates
from src.db.engine import get_db
from src.db.repositories import URLRepository

router = APIRouter(tags=["urls"])


def _normalise_url(url: str) -> str:
    """Prepend ``https://`` if the URL does not have a scheme.

    Args:
        url: The raw URL string.

    Returns:
        A URL with an explicit scheme.
    """

    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Render the homepage with the URL creation form and URL list.

    Args:
        request: The incoming HTTP request.
        db: Async database session.

    Returns:
        Rendered HTML page.
    """

    repo = URLRepository(db)
    urls = await repo.list_all()

    return templates.TemplateResponse(
        request,
        "index.html",
        {"urls": urls},
    )


@router.get("/{short_code}/stats", response_class=HTMLResponse)
async def url_stats(
    request: Request,
    short_code: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Render the statistics page for a single short URL.

    Args:
        request: The incoming HTTP request.
        short_code: The short code to look up.
        db: Async database session.

    Returns:
        Rendered HTML page or 404 if not found.
    """

    repo = URLRepository(db)
    url = await repo.get_stats(short_code)
    if url is None:
        return templates.TemplateResponse(
            request,
            "not_found.html",
            status_code=404,
        )

    host = request.base_url
    short_url = str(host).rstrip("/") + "/" + url.short_code

    return templates.TemplateResponse(
        request,
        "stats.html",
        {"url": url, "short_url": short_url},
    )


@router.post("/")
async def create_url(
    original_url: str = Form(...),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    """Create a new shortened URL from a form submission.

    Args:
        original_url: The original URL submitted via the form.
        db: Async database session.

    Returns:
        Redirect back to the homepage.
    """

    repo = URLRepository(db)
    await repo.create(_normalise_url(original_url))
    return RedirectResponse(url="/", status_code=303)


@router.delete("/{short_code}")
async def delete_url_api(
    short_code: str,
    db: AsyncSession = Depends(get_db),
) -> Response:
    """Delete a shortened URL entry (REST API).

    Args:
        short_code: The short code to delete.
        db: Async database session.

    Returns:
        204 No Content on success, 404 if not found.
    """

    repo = URLRepository(db)
    url = await repo.get_stats(short_code)
    if url is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    await repo.delete(url)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{short_code}/delete")
async def delete_url_form(
    short_code: str,
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    """Delete a shortened URL entry via HTML form.

    Args:
        short_code: The short code to delete.
        db: Async database session.

    Returns:
        Redirect back to the homepage.
    """

    repo = URLRepository(db)
    url = await repo.get_stats(short_code)
    if url is not None:
        await repo.delete(url)

    return RedirectResponse(url="/", status_code=303)


@router.get("/{short_code}", response_model=None)
async def redirect_to_url(
    request: Request,
    short_code: str,
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    """Redirect a short code to its original URL.

    Args:
        request: The incoming HTTP request.
        short_code: The short code to resolve.
        db: Async database session.

    Returns:
        HTTP redirect to the original URL, or 404 if not found.
    """

    repo = URLRepository(db)
    url = await repo.get_by_short_code(short_code)
    if url is None:
        return templates.TemplateResponse(
            request,
            "not_found.html",
            status_code=404,
        )

    return RedirectResponse(url=url.original_url, status_code=307)
