from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    db_user: str = 'username'
    db_password: str = 'userpassword'
    db_host: str = 'db-budgeter'
    db_name: str = 'dbname'

    TEST_LOG_FILE: str = 'test.log'

    model_config = SettingsConfigDict(env_file=('.env', '.env.local', '.env.prod'))
