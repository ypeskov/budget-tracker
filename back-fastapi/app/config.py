from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    ENVIRONMENT: str = 'prod'

    DB_USER: str = 'username'
    DB_PASSWORD: str = 'userpassword'
    DB_HOST: str = 'db-budgeter'
    DB_NAME: str = 'dbname'
    DB_PORT: int = 5432

    CELERY_BROKER_URL: str = 'redis://redis-budgeter:6379'
    CELERY_RESULT_BACKEND: str = 'redis://redis-budgeter:6379'

    CURRENCYBEACON_API_URL: str = ''
    CURRENCYBEACON_API_KEY: str = 'currencybeaconapikey'
    CURRENCYBEACON_API_VERSION: str = 'v1'

    TEST_LOG_FILE: str = 'test.log'

    DAILY_UPDATE_EXCHANGE_RATES_HOUR: str = '13'
    DAILY_UPDATE_EXCHANGE_RATES_MINUTE: str = '00'

    DAILY_DB_BACKUP_HOUR: str = '14'
    DAILY_DB_BACKUP_MINUTE: str = '00'

    DB_BACKUP_DIR: str = 'backup'
    DB_BACKUP_NOTIFICATION_EMAILS: list[str] = Field(..., alias='DB_BACKUP_NOTIFICATION_EMAILS')

    MAIL_USERNAME: str = "example@example.com"
    MAIL_PASSWORD: str = "*************"
    MAIL_FROM: str = "example@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "OrgFin.run Team"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True

    model_config = SettingsConfigDict(env_file=('.env', '.env.local', '.env.prod'))
