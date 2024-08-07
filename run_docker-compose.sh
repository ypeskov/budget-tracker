#!/usr/bin/env bash

if [ $# -eq 0 ]; then
  echo "Starting services without back app..."
  docker compose up db-orgfin \
                    redis-orgfin \
#                    celery-orgfin \
#                    celery-beat-orgfin \
#                    dashboard-redis-celery
#                    api-orgfin \
#                    adminer-orgfin \


elif [ "$1" == "full" ]; then
  echo "Starting all services..."
  docker compose up
elif [ "$1" == "prod" ]; then
  docker compose -f docker-compose.prod.yml up
else
  echo "Unknown argument: $1"
  echo "Variants:"
  echo "  0 - default - Start all services without back app"
  echo "  full - Start all services"
  exit 1
fi
