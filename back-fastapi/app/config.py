from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str = 'username'
    db_password: str = 'userpassword'
    db_host: str = 'db'
    db_name: str = 'dbname'

    class Config:
        # `.env.prod` takes priority over `.env`
        env_file = '.env', '.env.local', '.env.prod'
