# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
- `./run.sh` - Start the FastAPI app with auto-reload
- `./run.sh app` - Same as above
- `./run.sh celery` - Start Celery worker
- `./run.sh beat` - Start Celery beat scheduler

### Testing
- `./run_tests.sh` - Run all tests with coverage report
- `cd app/tests && make test` - Run tests in verbose mode
- `cd app/tests && make test-auth` - Run specific auth tests
- `cd app/tests && make test-accounts` - Run specific account tests
- `cd app/tests && make cov` - Run tests with coverage report

### Code Quality
- `./run_mypy.sh` - Run MyPy type checking
- `pylint app` - Run PyLint linting (configured in pylintrc)

### Database
- Alembic migrations are in `alembic/versions/`
- Use `alembic upgrade head` to apply migrations
- Use `alembic revision --autogenerate -m "message"` to create new migrations

## Architecture Overview

This is a FastAPI-based budget tracking application with the following key architectural patterns:

### Core Structure
- **Models** (`app/models/`): SQLAlchemy ORM models for database entities
- **Schemas** (`app/schemas/`): Pydantic models for request/response validation
- **Services** (`app/services/`): Business logic layer with specialized service classes
- **Routes** (`app/routes/`): FastAPI route handlers organized by domain
- **Tasks** (`app/tasks/`): Celery background tasks

### Key Services
- **TransactionManager** (`app/services/transaction_management/`): Handles complex transaction operations including transfers
- **CurrencyProcessor** (`app/services/CurrencyProcessor.py`): Manages currency conversions
- **Report Generators** (`app/services/reports_generators/`): Generate various financial reports

### Transaction System
The transaction system uses a manager pattern with separate handlers for:
- **NonTransferTypeTransaction**: Regular income/expense transactions
- **TransferTypeTransaction**: Money transfers between accounts
- Both inherit from common transaction management logic

### Database
- PostgreSQL with SQLAlchemy ORM
- Uses Alembic for migrations
- Models follow a user-centric design with proper foreign key relationships

### Background Processing
- Celery for asynchronous tasks (exchange rate updates, backups, budget processing)
- Redis as message broker and result backend
- Scheduled tasks for daily operations

### Configuration
- Settings managed via `app/config.py` using Pydantic settings
- Environment-based configuration with sensible defaults
- Separate test configuration support

### Development Setup
- Uses `uv` for dependency management (see `pyproject.toml`)
- Docker support with multi-stage builds
- Comprehensive test suite with pytest and coverage