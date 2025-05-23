# Yet Another Budget Tracker

## Description
This is a budget tracker application that allows users to track their incomes and expenses.
The main idea is to make self-hosted budget tracker that and keep info for yourself only.

Something like paranoid mode in the budget tracking world.

## Table of Contents
  - [Local Development](#local-development)
  - [Prerequisites](#prerequisites)
  - [Application setup](#application-setup)


# Local Development
Package manager: poetry


## Prerequisites
- PostgreSQL
Db can be run in Docker container or right on your OS.
- Redis
Redis can be run in Docker container or right on your OS.


## Application setup
You can run it locally in Docker container or right on your OS.
OS steps:
### Clone the repository
```bash
git clone git@github.com:ypeskov/budget-tracker.git budget-tracker
``` 
### Run PostgreSQL and Redis
Go to back-end app directory
```bash
cd budget-tracker/back-fastapi
```
### Create `.env` file in the root of the back-end app directory
```bash
cp .env.sample .env
```
### setup python virtual environment
```bash
poetry shell
```
### Install dependencies
```bash
poetry install
```
### Run the application Celery worker
```bash
./run.sh celery
```
### Run the application Beat
```bash
./run.sh beat
```
### Run the application FastAPI
```bash
./run.sh app
```
### Now run frontend part of the application
```bash
cd ../src-front
npm install
npm run dev
```

## Build Docker Images and Push to Docker Hub
### Build and push the back-end image
```bash
./build-and-push.sh push [tag version]
```
### Add commit and push master branch
The script above will push the image to Docker Hub and will add a new version in docekr-compose file.

### Login to server and pull the image
```bash
cd budget-tracker/
./deploy_full.sh
```

## License
This project is licensed under the MIT license.

