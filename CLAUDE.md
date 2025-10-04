# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## IMPORTANT: Context Loading Instructions

**ALWAYS read the following component-specific documentation files when working with the corresponding parts of the project:**

1. **Backend work** (`back-fastapi/`): Read `back-fastapi/CLAUDE.md` for detailed backend architecture, services, and patterns
2. **Frontend work** (`src-front/`): Read `src-front/CLAUDE.md` for detailed frontend architecture, components, and patterns

These files contain essential context about implementation details, patterns, and best practices specific to each component.

## Project Overview

**Budget Tracker** is a self-hosted full-stack budget tracking application that allows users to manage their personal finances privately. The project consists of three main components:

- **Backend**: FastAPI-based REST API (`back-fastapi/`)
- **Frontend**: Vue.js 3 SPA (`src-front/`)
- **Exporter**: Go-based data export utility (`exporter/`)

**Current Version**: 1.6.17

### Tech Stack
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy, Celery, PostgreSQL, Redis
- **Frontend**: Vue 3, Vite, Pinia, Bootstrap 5, Chart.js, Vue Router, i18n
- **Exporter**: Go 1.24.4, pgx/v5
- **Infrastructure**: Docker, Docker Compose, Nginx

## Directory Structure

```
budget-tracker/
├── back-fastapi/          # FastAPI backend application
│   ├── app/               # Application code
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── tasks/         # Celery tasks
│   │   ├── tests/         # Test suite
│   │   └── utils/         # Utility functions
│   ├── alembic/           # Database migrations
│   ├── CLAUDE.md          # Backend-specific docs
│   └── pyproject.toml     # Python dependencies
├── src-front/             # Vue.js frontend application
│   ├── src/
│   │   ├── components/    # Vue components
│   │   ├── views/         # Page components
│   │   ├── stores/        # Pinia stores
│   │   ├── services/      # API client services
│   │   ├── router/        # Vue Router config
│   │   └── locales/       # i18n translations (en, uk)
│   └── package.json       # Node dependencies
├── exporter/              # Go data exporter
│   ├── cmd/               # CLI entry point
│   ├── internal/          # Internal packages
│   └── go.mod             # Go dependencies
├── dbdata/                # PostgreSQL data (local dev)
├── docker-compose.yml     # Development environment
└── README.md              # Main documentation
```

## Development Commands

### Local Development (without Docker)

#### Prerequisites
- PostgreSQL 16.3+
- Redis
- Python 3.12+
- Node.js 18+
- Go 1.24+ (optional, for exporter)

#### Backend Setup
```bash
cd back-fastapi
cp .env.sample .env
# Edit .env with your database credentials

# Install all dependencies including dev extras using uv
uv sync --all-extras
source .venv/bin/activate

# Run database migrations
alembic upgrade head

# Start services (in separate terminals)
./run.sh app      # FastAPI server on :8000
./run.sh celery   # Celery worker
./run.sh beat     # Celery beat scheduler
```

#### Frontend Setup
```bash
cd src-front
npm install
npm run dev       # Vite dev server on :5173
```

### Docker Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api-orgfin

# Stop all services
docker-compose down
```

Services available:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs (dev only)
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- Flower (Celery monitoring): http://localhost:5556

### Testing & Code Quality

#### Backend
```bash
cd back-fastapi

# Run all tests with coverage
./run_tests.sh

# Type checking
./run_mypy.sh

# Linting
pylint app
```

#### Frontend
```bash
cd src-front

# Linting
npm run lint

# Format code
npm run format
```

## Backend API (FastAPI)

For detailed backend documentation, see `back-fastapi/CLAUDE.md`

### Key API Endpoints

- **Auth**: `/api/v1/auth/*` - Registration, login, Google OAuth
- **Accounts**: `/api/v1/accounts/*` - Account management
- **Transactions**: `/api/v1/transactions/*` - Income, expense, transfer operations
- **Planned Transactions**: `/api/v1/planned-transactions/*` - Future transaction planning
- **Financial Planning**: `/api/v1/financial-planning/*` - Future balance calculations and projections
- **Categories**: `/api/v1/categories/*` - Category management
- **Budgets**: `/api/v1/budgets/*` - Budget tracking
- **Reports**: `/api/v1/reports/*` - Financial reports
- **Analytics**: `/api/v1/analytics/*` - Expense analysis with OpenAI
- **Currencies**: `/api/v1/currencies/*` - Currency management
- **Exchange Rates**: `/api/v1/exchange-rates/*` - Exchange rate data
- **Settings**: `/api/v1/settings/*` - User settings

### Core Features

1. **Multi-currency Support**
   - Automatic exchange rate updates via CurrencyBeacon API
   - Currency conversion for transactions
   - Base currency per user

2. **Account Types**
   - Regular accounts (checking, savings, cash)
   - Credit accounts with limits and billing cycles

3. **Transaction System**
   - Income, expense, and transfer transactions
   - Transaction templates for recurring operations
   - Complex transfer handling with currency conversion

4. **Budget Management**
   - Monthly budgets by category
   - Automatic rollover of unused amounts
   - Budget status tracking

5. **Financial Planning**
   - Planned transactions (one-time and recurring)
   - Future balance calculations
   - Balance projections over time
   - Automatic transaction execution
   - Recurrence rules (daily, weekly, monthly, yearly)

6. **Reports & Analytics**
   - Balance reports
   - Cash flow analysis
   - Expense categorization
   - Spending trends
   - OpenAI-powered expense insights

7. **Background Tasks** (Celery)
   - Daily exchange rate updates (13:00)
   - Daily database backups with Google Drive upload (14:00)
   - Monthly budget processing (00:01)
   - Planned transactions processing (00:05)
   - Token cleanup (02:00)

## Frontend (Vue.js 3)

### Architecture

- **State Management**: Pinia stores for auth, accounts, transactions, categories, currencies, planned transactions
- **Routing**: Vue Router with navigation guards for authentication
- **API Communication**: Axios-based service layer (`src/services/`)
- **Internationalization**: Vue i18n (English, Ukrainian)
- **UI Framework**: Bootstrap 5 with custom SCSS
- **Charts**: Chart.js via vue-chartjs

### Main Views

- `HomeView.vue` - Dashboard with account summaries
- `AccountsListView.vue` - Account management
- `AccountDetailsView.vue` - Account transactions and details
- `TransactionsListView.vue` - Transaction list with filters
- `TransactionNewView.vue` - Create/edit transactions
- `BudgetsView.vue` - Budget management
- `FinancialPlanningView.vue` - Planned transactions and future balance projections
- `ReportsView.vue` - Reports hub
- `BalanceReportView.vue` - Balance over time
- `CashFlowReportView.vue` - Income vs expenses
- `ExpenseCategorizationReportView.vue` - Expense breakdown
- `SpendingTrendsReportView.vue` - Spending patterns
- `ExpensesReportView.vue` - Detailed expense analysis
- `Settings.vue` - User settings and preferences
- `LoginView.vue` / `RegisterView.vue` - Authentication

### Key Stores (Pinia)

- `authStore` - Authentication state, JWT token management
- `accountsStore` - Account data and operations
- `transactionsStore` - Transaction CRUD operations
- `plannedTransactionsStore` - Planned transactions and financial planning
- `categoriesStore` - Category management
- `currenciesStore` - Currency data and exchange rates
- `budgetsStore` - Budget tracking

### Environment Variables

Create `.env` in `src-front/`:
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

## Exporter (Go)

Go-based utility for exporting data from PostgreSQL database.

### Structure
- `cmd/cli.go` - CLI entry point
- `internal/config/` - Configuration management
- `internal/database/` - Database connection
- `internal/models/` - Data models
- `internal/repositories/` - Data access layer
- `internal/services/` - Business logic

### Usage
```bash
cd exporter
go run cmd/cli.go [options]
```

## Infrastructure

### Docker Services (docker-compose.yml)

1. **api-orgfin** - FastAPI backend container
2. **front-orgfin** - Vite dev server (dev mode) or Nginx (prod)
3. **db-orgfin** - PostgreSQL 16.3
4. **redis-orgfin** - Redis for Celery
5. **celery-orgfin** - Celery worker
6. **celery-beat-orgfin** - Celery beat scheduler
7. **dashboard-redis-celery** - Flower monitoring

### Database

- **Engine**: PostgreSQL 16.3
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic
- **Connection Pool**: Managed by SQLAlchemy

#### Main Tables
- `users` - User accounts
- `accounts` - Financial accounts
- `transactions` - All financial transactions
- `planned_transactions` - Planned/future transactions
- `categories` (default_categories, user_categories) - Transaction categories
- `currencies` - Supported currencies
- `exchange_rate_history` - Historical exchange rates
- `budgets` - Budget definitions and tracking
- `user_settings` - User preferences
- `activation_tokens` - Email verification tokens

### Celery Tasks

Configured in `back-fastapi/app/tasks/tasks.py`:

1. **daily_update_exchange_rates** - Fetch latest rates from CurrencyBeacon
   - Schedule: Daily at 13:00
   - Retries: 24 times, 10 min intervals

2. **make_db_backup** - PostgreSQL backup + Google Drive upload
   - Schedule: Daily at 14:00
   - Creates compressed SQL dump
   - Uploads to Google Drive via rclone

3. **daily_budgets_processing** - Process monthly budgets
   - Schedule: Daily at 00:01
   - Archives outdated budgets
   - Updates budget amounts

4. **process_due_planned_transactions** - Check and log due planned transactions
   - Schedule: Daily at 00:05
   - Finds transactions due today
   - Logs them (manual execution required)

5. **delete_old_activation_tokens** - Cleanup expired tokens
   - Schedule: Daily at 02:00

## Deployment

### Build & Push Docker Images

#### Backend
```bash
cd back-fastapi
./build-and-push.sh push [version]
```

This script:
1. Builds Docker image
2. Tags with version
3. Pushes to Docker Hub
4. Updates version in `docker-compose.prod.yml`

#### Frontend
```bash
cd src-front
./build-frontend-docker.sh
```

### Deploy to Server

```bash
# On server
cd budget-tracker
./deploy_full.sh
```

This pulls latest images and restarts services.

### Production Configuration

Backend `.env` should include:
- `ENVIRONMENT=prod` - Disables API docs
- Strong `SECRET_KEY` (min 16 chars)
- Production database credentials
- Email SMTP settings
- CurrencyBeacon API key
- Google OAuth credentials
- OpenAI API key (for analytics)
- Google Drive OAuth token (for backups)

## API Authentication

The application uses JWT tokens for authentication:

1. **Login**: POST `/api/v1/auth/login` returns access token
2. **Token included** in `Authorization: Bearer <token>` header
3. **Token refresh**: Automatic via middleware when near expiration
4. **Google OAuth**: Alternative login via `/api/v1/auth/google`

Frontend stores token in Pinia store and includes in all API requests.

## Key Design Patterns

### Backend
- **Service Layer Pattern**: Business logic separated from routes
- **Repository Pattern**: Data access abstraction
- **Manager Pattern**: TransactionManager for complex operations
- **Dependency Injection**: FastAPI dependencies for DB sessions, auth
- **Schema Validation**: Pydantic models for request/response

### Frontend
- **Composition API**: Vue 3 script setup syntax
- **Store Pattern**: Centralized state management with Pinia
- **Service Layer**: API calls abstracted in service modules
- **Component-based**: Reusable components for forms, cards, charts

## Security Considerations

1. **Password Hashing**: bcrypt with salt
2. **JWT Tokens**: Signed with SECRET_KEY, short expiration
3. **CORS**: Configured for specific origins
4. **SQL Injection**: Protected by SQLAlchemy ORM
5. **XSS**: Vue's automatic escaping
6. **CSRF**: Not needed for JWT-based API
7. **Rate Limiting**: Consider adding for production
8. **HTTPS**: Required in production

## Common Development Tasks

### Add New API Endpoint

1. Define Pydantic schema in `back-fastapi/app/schemas/`
2. Add route handler in `back-fastapi/app/routes/`
3. Implement business logic in `back-fastapi/app/services/`
4. Add tests in `back-fastapi/app/tests/`
5. Update frontend service in `src-front/src/services/`
6. Use in Vue component

### Add New Database Model

1. Create model in `back-fastapi/app/models/`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review and edit migration in `alembic/versions/`
4. Apply: `alembic upgrade head`
5. Create corresponding Pydantic schemas

### Add New Frontend Page

1. Create view component in `src-front/src/views/`
2. Add route in `src-front/src/router/index.js`
3. Add navigation link in components
4. Create API service methods if needed
5. Update Pinia store if needed

### Add New Celery Task

1. Define task in `back-fastapi/app/tasks/tasks.py`
2. Configure schedule in `back-fastapi/app/celery.py`
3. Test with `./run.sh celery` and `./run.sh beat`

## Troubleshooting

### Backend issues
- Check logs: `docker-compose logs -f api-orgfin`
- Verify database connection in `.env`
- Run migrations: `alembic upgrade head`
- Check Redis: `redis-cli ping`

### Frontend issues
- Clear browser cache and localStorage
- Check API_URL in `.env`
- Verify backend is running: `curl http://localhost:8000/docs`
- Check browser console for errors

### Celery issues
- Check Redis connection
- View Flower dashboard: http://localhost:5556
- Check Celery logs: `docker-compose logs -f celery-orgfin`
- Verify beat schedule: `docker-compose logs -f celery-beat-orgfin`

## Additional Resources

- FastAPI docs: https://fastapi.tiangolo.com
- Vue 3 docs: https://vuejs.org
- SQLAlchemy docs: https://docs.sqlalchemy.org
- Celery docs: https://docs.celeryq.dev
- Alembic docs: https://alembic.sqlalchemy.org

## Version History

- **1.6.17** (Current) - Latest stable release
- Backend API: v1.8.4
- See git log for detailed changelog
