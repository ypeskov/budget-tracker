# ---- builder: compile wheels here
FROM python:3.13-slim-bookworm AS builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# install uv and build venv with deps
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
 && ln -s $(find /root -name uv -type f | grep "/bin/uv$" | head -n1) /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv venv && uv sync --frozen --no-dev
COPY . /app

# ---- runtime: lean image + pg_dump
FROM python:3.13-slim-bookworm AS prod
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"
WORKDIR /app

# PGDG repo + client binaries (pg_dump) + rclone for Google Drive backups
RUN apt-get update && apt-get install -y --no-install-recommends wget gnupg lsb-release \
 && echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
    > /etc/apt/sources.list.d/pgdg.list \
 && wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc \
    | gpg --dearmor -o /etc/apt/trusted.gpg.d/pgdg.gpg \
 && apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client-17 \
    rclone \
 && apt-get purge -y --auto-remove wget gnupg lsb-release \
 && rm -rf /var/lib/apt/lists/*

# copy app + prebuilt venv (no compilers here)
COPY --from=builder /app /app

EXPOSE 8000
CMD ["gunicorn","app.main:app","-w","2","-k","uvicorn.workers.UvicornWorker","--bind","0.0.0.0:8000"]