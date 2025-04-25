# Usa una imagen base oficial de Python
FROM python:3.12-slim as base

# Etapa builder para instalar dependencias con Poetry
FROM base AS builder

# instalar poetry
RUN pip install poetry==2.0.0

# Instalar Poetry
ENV POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR="/tmp/poetry_cache"

RUN curl -sSL https://install.python-poetry.org | python3 -

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos necesarios para instalar dependencias
COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR

# Copiar el resto del proyecto
COPY ./app ./app

EXPOSE 3002

CMD ["poetry", "run", "uvicorn", "app.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "3002"]