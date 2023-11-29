from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base

DB_NAME = 'budgeter_test'
DB_USER = 'postgres'
DB_PASSWORD = 'budgeter'
DB_HOST = 'db-budgeter'

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
