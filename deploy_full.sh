#!/usr/bin/env bash

git pull

cd back-fastapi && docker-compose down && docker-compose up -f docker-compose.prod.yaml -d

cd src-front/ && bash build.sh
