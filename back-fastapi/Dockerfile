FROM python:3.12.3-bookworm AS dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install debugpy
RUN pip install pydevd-pycharm~=241.14494.241

COPY . /app

EXPOSE 8000
EXPOSE 5678

CMD ["python", "-Xfrozen_modules=off", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --------------------------------------

FROM python:3.12.3-slim-bookworm AS prod

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/

RUN apt-get update && apt-get install -y wget gnupg2 lsb-release

RUN echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y gcc libpq-dev postgresql-client-16 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

