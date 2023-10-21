from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from icecream import install
install()

from app.data_loaders.work_data.load_all import load_all_data
from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:budgeter@db/budgeter_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

db = next(override_get_db())
load_all_data(db)


client = TestClient(app)


def test_create_user():
    json = {
        "id": 1,
        "email": "user1@example.com",
        "first_name": "Yura",
        "last_name": "Peskov",
        "password": "q"
    }
    response = client .post(
        '/auth/register/',
        json=json)
    ic(response.json())


# def test_login_user():
#     response = client.post(
#         "/auth/login/",
#         json={"email": "user1@example.com", "password": "qqq"},
#     )
#     assert response.status_code == 200, response.text
#     data = response.json()
#
#     # assert data["email"] == "user1@example.com"
#     assert "access_token" in data
#     assert data["token_type"] == "bearer"
#     response = client.get("/auth/profile", headers={'auth-token': data["access_token"]})
#     assert response.status_code == 200
#     data = response.json()
#     assert data["email"] == "user1@example.com"
#     # assert data["id"] == user_id
