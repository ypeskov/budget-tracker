#!/usr/bin/env bash

echo "Now pulling the latest changes from the repository."
git pull

echo "Pull the Docker images from Docker Hub and restart the containers in docker-compose.prod.yaml."
docker-compose -f docker-compose.prod.yml down &&\
docker-compose -f docker-compose.prod.yml up -d

echo "Building the front-end and restart front-end"
cd src-front && bash build.sh

echo "Done."
