### ───────────────────────────────────────────────
### Builder stage
### ───────────────────────────────────────────────
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

RUN rm -f pyproject.toml uv.lock .python-version \
    && rm -rf /root/.cache /app/.cache

### ───────────────────────────────────────────────
### Runtime stage
### ───────────────────────────────────────────────
FROM python:3.13-slim-trixie AS runtime

WORKDIR /app

COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x ./docker/*

RUN rm -rf /app/.venv/share/man \
    /app/.venv/lib/python*/test \
    /app/.venv/lib/python*/ensurepip \
    /app/.venv/lib/python*/distutils/tests \
    /app/.venv/lib/python*/tkinter

CMD ["sh", "./docker/docker-entrypoint.sh"]