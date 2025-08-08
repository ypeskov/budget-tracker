from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    FRONTEND_URL: str = "https://orgfin.run"

    DB_USER: str = "username"
    DB_PASSWORD: str = "userpassword"
    DB_HOST: str = "db-budgeter"
    DB_NAME: str = "dbname"
    DB_PORT: int = 5432

    CELERY_BROKER_URL: str = "redis://redis-budgeter:6379"
    CELERY_RESULT_BACKEND: str = "redis://redis-budgeter:6379"

    CURRENCYBEACON_API_URL: str = ""
    CURRENCYBEACON_API_KEY: str = "currencybeaconapikey"
    CURRENCYBEACON_API_VERSION: str = "v1"

    TEST_LOG_FILE: str = "test.log"

    DAILY_UPDATE_EXCHANGE_RATES_HOUR: str = "13"
    DAILY_UPDATE_EXCHANGE_RATES_MINUTE: str = "00"

    DAILY_DB_BACKUP_HOUR: str = "14"
    DAILY_DB_BACKUP_MINUTE: str = "00"

    DAILY_BUDGETS_PROCESSING_HOUR: str = "00"
    DAILY_BUDGETS_PROCESSING_MINUTE: str = "01"

    DB_BACKUP_DIR: str = "backup"

    ADMINS_NOTIFICATION_EMAILS: list[str] = []

    MAIL_USERNAME: str = "example@example.com"
    MAIL_PASSWORD: str = "*************"
    MAIL_FROM: str = "example@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "OrgFin.run Team"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True

    # JWT expiration time in minutes
    LOGIN_SESSION_EXPIRATION_MINUTES: int = 30

    GOOGLE_CLIENT_ID: str = "123"
    SECRET_KEY: str = "111111111"

    # OpenAI configuration for expense analysis
    OPENAI_API_KEY: str = "your-openai-api-key"
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_TEMPERATURE: float = 0.3

    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"))


settings = Settings()
