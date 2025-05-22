# Etapa base: imagen oficial de Python, versión slim para menor tamaño
FROM python:3.12-slim-bookworm AS base

# Etapa builder: instala uv y dependencias
FROM base AS builder

# Instala uv desde la imagen oficial de Astral (más rápido y seguro que usar pip)
COPY --from=ghcr.io/astral-sh/uv:0.7.6 /uv /bin/uv

# Opciones de optimización para uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copia solo archivos de dependencias para aprovechar el cache de Docker
COPY pyproject.toml uv.lock /app/

# Instala dependencias en modo congelado (reproducible), sin dev ni editable
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copia el resto del código fuente
COPY . /app

# Sincroniza el proyecto (instala en .venv, no editable, no dev)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# Etapa final: imagen limpia y ligera
FROM base

WORKDIR /app

# Copia solo el entorno virtual y el código fuente desde el builder
COPY --from=builder /app /app

# Usa el entorno virtual creado por uv
ENV PATH="/app/.venv/bin:$PATH"

# Comando por defecto para ejecutar la app
CMD ["python", "main.py"]
