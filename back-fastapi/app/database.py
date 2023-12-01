from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import Settings

s = Settings()

SQLALCHEMY_DATABASE_URL = f'postgresql://{s.db_user}:{s.db_password}@{s.db_host}:{s.db_port}/{s.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():  # pragma: no cover
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
