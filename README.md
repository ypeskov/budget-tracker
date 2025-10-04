# Budget Tracker

**Version 1.6.17** - A self-hosted, privacy-first personal finance management application

## Description

Budget Tracker is a comprehensive full-stack application for managing personal finances with complete privacy. Built with modern technologies, it provides multi-currency support, advanced budgeting, financial planning, and AI-powered analytics - all while keeping your financial data under your control.

Think of it as paranoid mode in the budget tracking world - your data stays with you.

## Features

### Core Functionality
- **Multi-currency Support** - Track accounts in different currencies with automatic exchange rate updates
- **Account Management** - Regular accounts (checking, savings, cash) and credit accounts with billing cycles
- **Transaction Management** - Income, expenses, and transfers with currency conversion
- **Transaction Templates** - Save and reuse common transactions
- **Financial Planning** - Plan future transactions (one-time and recurring) with automatic execution
- **Budget Tracking** - Monthly budgets by category with automatic rollover

### Reports & Analytics
- **Balance Reports** - Track account balances over time
- **Cash Flow Analysis** - Visualize income vs expenses
- **Expense Categorization** - Breakdown spending by category
- **Spending Trends** - Identify spending patterns
- **AI-Powered Insights** - OpenAI integration for expense analysis

### Additional Features
- **Authentication** - Email/password and Google OAuth support
- **Multi-language** - English and Ukrainian interfaces
- **Automatic Backups** - Daily database backups to Google Drive
- **Data Export** - Export your data using the Go-based exporter utility
- **Self-hosted** - Complete control over your financial data

## Tech Stack

- **Backend**: Python 3.12+, FastAPI, SQLAlchemy, Celery, PostgreSQL 16.3, Redis
- **Frontend**: Vue.js 3, Vite, Pinia, Bootstrap 5, Chart.js, Vue i18n
- **Exporter**: Go 1.24.4
- **Infrastructure**: Docker, Docker Compose, Nginx

## Table of Contents

- [Quick Start with Docker](#quick-start-with-docker)
- [Local Development](#local-development)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Quick Start with Docker

The fastest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone git@github.com:ypeskov/budget-tracker.git budget-tracker
cd budget-tracker

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

Services include:
- FastAPI backend
- Vue.js frontend (Vite dev server)
- PostgreSQL database
- Redis
- Celery worker and beat scheduler
- Flower (Celery monitoring at http://localhost:5556)

## Local Development

### Prerequisites

- **PostgreSQL** 16.3+
- **Redis** 6.0+
- **Python** 3.12+
- **Node.js** 18+
- **uv** (Python package manager)
- **Go** 1.24+ (optional, for exporter)

### Backend Setup

```bash
# Navigate to backend directory
cd back-fastapi

# Create and configure environment file
cp .env.sample .env
# Edit .env with your database credentials and API keys

# Install dependencies using uv (includes all dev extras)
uv sync --all-extras
source .venv/bin/activate

# Run database migrations
alembic upgrade head

# Start backend services (in separate terminals)
./run.sh app      # FastAPI server on port 8000
./run.sh celery   # Celery worker
./run.sh beat     # Celery beat scheduler
```

#### Required Environment Variables

Edit `back-fastapi/.env`:
```env
ENVIRONMENT='dev'
FRONTEND_URL='http://localhost:5173'

# Database Configuration
DB_USER='postgres'
DB_PASSWORD='your-password'
DB_HOST='localhost'
DB_NAME='budget_db'
DB_PORT='5432'

# Redis/Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379

# CurrencyBeacon API
CURRENCYBEACON_API_URL='https://api.currencybeacon.com'
CURRENCYBEACON_API_KEY='your-api-key'
CURRENCYBEACON_API_VERSION='v1'

# Scheduled Tasks (24-hour format)
DAILY_UPDATE_EXCHANGE_RATES_HOUR=13
DAILY_UPDATE_EXCHANGE_RATES_MINUTE=00
DAILY_DB_BACKUP_HOUR=14
DAILY_DB_BACKUP_MINUTE=00
DAILY_BUDGETS_PROCESSING_HOUR=00
DAILY_BUDGETS_PROCESSING_MINUTE=01

# Backup Configuration
DB_BACKUP_DIR='backup'
ADMINS_NOTIFICATION_EMAILS=["admin@example.com"]

# Email Configuration
MAIL_USERNAME="your-email@gmail.com"
MAIL_PASSWORD="your-app-password"
MAIL_FROM="your-email@gmail.com"
MAIL_PORT=587
MAIL_SERVER="smtp.gmail.com"
MAIL_FROM_NAME="Budget Tracker"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
USE_CREDENTIALS=True

# Authentication
GOOGLE_CLIENT_ID=your-google-client-id
SECRET_KEY=your-secret-key-min-16-chars

# Optional: OpenAI for expense analytics
OPENAI_API_KEY=sk-proj-your-key

# Optional: Google Drive backups
GDRIVE_OAUTH_TOKEN=""
GDRIVE_FOLDER_PATH="backups/budget-tracker"
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd src-front

# Install dependencies
npm install

# Create environment file
cp .env.sample .env
# Edit .env with your configuration

# Start development server
npm run dev  # Runs on http://localhost:5173
```

#### Frontend Environment Variables

Edit `src-front/.env`:
```env
VITE_BACKEND_HOST="http://localhost:8000"
VITE_GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
```

### Running Tests

#### Backend Tests
```bash
cd back-fastapi

# Run all tests with coverage
./run_tests.sh

# Type checking
./run_mypy.sh

# Linting
pylint app
```

#### Frontend Linting
```bash
cd src-front
npm run lint
npm run format
```

## Architecture

### Background Tasks (Celery)

Automated daily tasks:
- Update exchange rates from CurrencyBeacon API
- Database backup and upload to Google Drive
- Process monthly budgets and rollover
- Execute due planned transactions
- Clean up expired activation tokens

API documentation available at `http://localhost:8000/docs` (development only)

## Key Features

### Multi-currency Support

- Track accounts in different currencies
- Automatic daily exchange rate updates via CurrencyBeacon API
- Seamless currency conversion for transfers
- Set your base currency per user

### Account Types

**Regular Accounts**: Checking, savings, cash
- Track balance
- Unlimited transactions
- Multi-currency support

**Credit Accounts**: Credit cards and lines of credit
- Set credit limit
- Define billing cycle dates
- Track available credit
- Calculate interest and fees

### Transaction System

- **Income**: Record money coming in
- **Expenses**: Track spending by category
- **Transfers**: Move money between accounts with automatic currency conversion
- **Templates**: Save frequently used transactions for quick entry
- **Bulk Import**: Import transactions from CSV files

### Financial Planning

Plan your financial future with:
- **One-time planned transactions**: Future expenses or income
- **Recurring transactions**: Daily, weekly, monthly, or yearly schedules
- **Automatic execution**: Transactions are automatically created when due
- **Balance projections**: Visualize future account balances
- **What-if scenarios**: Toggle planned transactions on/off to see impact

### Budget Management

- Create monthly budgets by category
- Track spending against budget limits
- Automatic rollover of unused amounts
- Visual progress indicators
- Budget vs actual reports

### Reports & Analytics

**Built-in Reports**:
- Balance over time
- Cash flow (income vs expenses)
- Expense categorization
- Spending trends and patterns
- Category-wise expense breakdown

**AI-Powered Analytics** (requires OpenAI API key):
- Intelligent expense insights
- Spending pattern analysis
- Personalized recommendations

### Data Export

Use the Go-based exporter to extract your data:
```bash
cd exporter
go run cmd/cli.go --help
```

## Deployment

### Build and Push Docker Images

#### Backend
```bash
cd back-fastapi
./build-and-push.sh push [version]
```

This script:
1. Builds the Docker image
2. Tags with version number
3. Pushes to Docker Hub

#### Frontend
```bash
cd src-front
./build-frontend-docker.sh
```

### Deploy to Production (Kubernetes)

Production deployment uses Kubernetes. Manifest files and configuration are maintained in a separate repository:

**Repository**: https://github.com/ypeskov/k8s-orgfin

After building and pushing Docker images, update the Kubernetes manifests with the new image versions and apply the changes to your cluster.

## Troubleshooting

### Backend Issues

```bash
# Check backend logs
docker-compose logs -f api-orgfin

# Verify database connection
docker-compose exec api-orgfin python -c "from app.database import engine; print(engine.url)"

# Run migrations
docker-compose exec api-orgfin alembic upgrade head

# Check Celery tasks
docker-compose logs -f celery-orgfin
docker-compose logs -f celery-beat-orgfin
```

### Frontend Issues

```bash
# Check frontend logs
docker-compose logs -f front-orgfin

# Rebuild frontend
cd src-front
npm install
npm run build

# Clear browser cache and localStorage
# Verify API connection in browser console
```

### Database Issues

```bash
# Check PostgreSQL logs
docker-compose logs -f db-orgfin

# Access database shell
docker-compose exec db-orgfin psql -U budget_user -d budget_db

# Backup database manually
docker-compose exec db-orgfin pg_dump -U budget_user budget_db > backup.sql
```

### Redis/Celery Issues

```bash
# Check Redis connection
docker-compose exec redis-orgfin redis-cli ping

# View Celery monitoring dashboard
# Open http://localhost:5556 (Flower)

# Restart Celery services
docker-compose restart celery-orgfin celery-beat-orgfin
```

### Common Issues

**Issue**: Frontend can't connect to backend
- Verify `VITE_BACKEND_HOST` in `src-front/.env`
- Check backend is running: `curl http://localhost:8000/docs`
- Check browser console for CORS errors

**Issue**: Exchange rates not updating
- Verify `CURRENCYBEACON_API_KEY` in backend `.env`
- Check Celery beat logs: `docker-compose logs celery-beat-orgfin`
- Manually trigger: Check Flower dashboard

**Issue**: Planned transactions not executing
- Verify Celery beat is running
- Check logs for `process_due_planned_transactions` task
- Confirm transactions are marked as "active"

## Documentation

- **Project Overview**: [CLAUDE.md](CLAUDE.md)
- **Backend Details**: [back-fastapi/CLAUDE.md](back-fastapi/CLAUDE.md)
- **Frontend Details**: [src-front/CLAUDE.md](src-front/CLAUDE.md)
- **API Documentation**: http://localhost:8000/docs (dev only)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow existing code style and conventions
- Write tests for new features
- Update documentation as needed
- Run linting before committing:
  - Backend: `./run_mypy.sh` and `pylint app`
  - Frontend: `npm run lint`

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation in CLAUDE.md files
- Review API documentation at `/docs` endpoint

---

**Note**: This is a self-hosted application. You are responsible for securing your installation, keeping dependencies updated, and maintaining backups of your data.