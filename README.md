# budget-tracker

## Description
This is a budget tracker application that allows users to track their incomes and expenses.
The main idea is to make self-hosted budget tracker that and keep info for yourself only.

Something like paranoid mode in the budget tracking world.

## Table of Contents
- [Local Development] (#local-development)
- [Usage](#usage)
- [License](#license)

## Local Development

### Prerequisites
- PostgreSQL
Db can be run in Docker container or right on your OS.
- Redis
Redis can be run in Docker container or right on your OS.


## Application setup
You can run it locally in Docker container or right on your OS.
OS steps:
1. Clone the repository
```bash
git clone git@github.com:ypeskov/budget-tracker.git budget-tracker
``` 
2. Run PostgreSQL and Redis
3. cd back-fastapi and create `.env` file in the root of the project and add the following variables:
```bash
cp .env.sample .env
```
4. setup python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
5. Install dependencies
```bash
pip install -r requirements.txt
```
6. Run the application Celery worker
```bash
./run celery
```
7. Run the application Beat
```bash
./run beat
```
8. Run the application FastAPI
```bash
./run app
```
9. Now run frontend part of the application
```bash
cd ../src-front
npm install
npm run dev
```

## License
This project is licensed under the MIT license.

