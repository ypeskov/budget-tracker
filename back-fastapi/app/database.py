from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import Settings

s = Settings()

SQLALCHEMY_DATABASE_URL = f'postgresql://{s.db_user}:{s.db_password}@{s.db_host}/{s.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
