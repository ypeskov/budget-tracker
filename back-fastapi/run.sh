#!/usr/bin/env bash

source venv/bin/activate

if [ $# -eq 0 ]; then
    echo "Start main app"
    uvicorn app.main:app --reload
else
    case "$1" in
        app)
            echo "Start main app"
            uvicorn app.main:app --reload
            ;;
        celery)
            echo "Start celery worker"
            celery -A app.celery worker -l info
            ;;
        beat)
            echo "Start celery beat"
            celery -A app.celery beat --loglevel=info
            ;;
        *)
            echo "Unknown command $1"
            echo "Available commands: app, celery, beat"
            ;;
    esac
fi
