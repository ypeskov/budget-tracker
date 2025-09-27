from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "prod"
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
    # Secret key is required (no insecure default)
    SECRET_KEY: str = ""

    # OpenAI configuration for expense analysis
    OPENAI_API_KEY: str = "your-openai-api-key"
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_TEMPERATURE: float = 0.3

    # Google Drive backup configuration
    GDRIVE_OAUTH_TOKEN: str = ""  # OAuth2 token from rclone authorize drive
    GDRIVE_FOLDER_PATH: str = "services/orgfin.run/backups"

    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"))

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value: str, info: ValidationInfo) -> str:
        """Ensure SECRET_KEY is present and sufficiently strong.

        In production (ENVIRONMENT in {"prod", "production"}) require length >= 32,
        otherwise allow shorter keys but at least 8 characters.
        """
        if not value or not isinstance(value, str) or value.strip() == "":
            raise ValueError("SECRET_KEY must be provided via environment")
        environment = str((info.data or {}).get("ENVIRONMENT", "")).lower()
        min_len = 16 if environment in {"prod", "production"} else 8
        if len(value) < min_len:
            raise ValueError(
                f"SECRET_KEY is too short (got {len(value)}), minimum is {min_len} characters for {environment or 'non-production'}"
            )
        return value


settings = Settings()
