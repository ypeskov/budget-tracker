from pydantic_settings import SettingsConfigDict, BaseSettings


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

    DB_BACKUP_DIR: str = 'backup'

    model_config = SettingsConfigDict(env_file=('.env', '.env.local', '.env.prod'))
