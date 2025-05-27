# Etapa 1: Builder
FROM python:3.12-alpine AS builder

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

# CLAVE: --no-default-groups evita instalar dependencies principales
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-default-groups --group db

COPY src/database/ ./src/database/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-default-groups --group db

# Etapa 2: Runtime
FROM python:3.12-alpine AS runtime

RUN apk add --no-cache \
    libffi \
    openssl \
    && adduser -D -s /bin/sh appuser

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src/database/*.py /app/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
USER appuser

CMD ["python", "test_connection.py"]
