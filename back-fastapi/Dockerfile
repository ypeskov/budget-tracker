FROM python:3.12.3-slim-bookworm AS prod

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# RUN apt-get update && apt-get install -y libpq5 \
#  && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y wget gnupg2 lsb-release \
 && echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
 && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
 && apt-get update \
 && apt-get install -y postgresql-client-16 \
 && apt-get purge -y --auto-remove wget gnupg2 lsb-release \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y curl ca-certificates && \
curl -LsSf https://astral.sh/uv/install.sh | sh && \
ln -s $(find /root -name uv -type f | grep "/bin/uv$" | head -n1) /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv venv && uv sync

COPY . /app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]