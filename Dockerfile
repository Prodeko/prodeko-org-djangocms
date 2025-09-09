# Stage 1 - build tiedotteet frontend
FROM node:12 as tiedotteet-build
WORKDIR /app

COPY tiedotteet/frontend/package.json tiedotteet/frontend/package-lock.json ./
RUN npm ci

ADD tiedotteet/frontend /app
RUN npm run build:prod

# Stage 2 - main container definition
FROM ghcr.io/astral-sh/uv:python3.12-trixie

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_TOOL_BIN_DIR=/usr/local/bin
ENV UV_LINK_MODE=copy

# SSL/TLS with certs shipped with the docker image
ENV SSL_CERT_DIR=/etc/ssl/certs

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client gettext dos2unix \
  && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY . /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=tiedotteet-build /app/public/tiedotteet /app/tiedotteet/frontend/public/tiedotteet
