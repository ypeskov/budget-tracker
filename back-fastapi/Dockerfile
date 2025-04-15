FROM python:3.12.3-slim-bookworm AS build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY pyproject.toml uv.lock requirements.txt ./
RUN pip install --no-cache-dir uv && uv pip install --system -r requirements.txt

COPY . /app

EXPOSE 8000
EXPOSE 5678

CMD ["python", "-Xfrozen_modules=off", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

# --------------------------------------

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

COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=build /usr/local/bin /usr/local/bin

COPY --from=build /app /app

# RUN apt-get update && apt-get install -y wget gnupg2 lsb-release

# RUN echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
#     && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
#     && apt-get update \
#     && apt-get install -y gcc libpq-dev postgresql-client-16 \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# RUN pip install --no-cache-dir uv

# COPY pyproject.toml uv.lock requirements.txt /app/
# RUN uv pip install --system -r requirements.txt

# RUN apt-get purge -y --auto-remove gcc libpq-dev \
#  && apt-get clean \
#  && rm -rf /var/lib/apt/lists/*

# COPY . /app

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]