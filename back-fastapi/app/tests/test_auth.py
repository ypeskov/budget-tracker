from fastapi.testclient import TestClient

from app.main import app
from app.tests.db_test_cfg import override_get_db
from app.data_loaders.work_data.load_all import load_all_data

import icecream
icecream.install()

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
    data = response.json()
    assert 'id' in data
    assert data['id'] == json['id']
    assert response.status_code == 200
    assert data['email'] == json['email']
    assert data['first_name'] == json['first_name']
    assert data['last_name'] == json['last_name']


def test_login_user():
    response = client.post(
        "/auth/login/",
        json={"email": "user1@example.com", "password": "q"},
    )
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    response = client.get("/auth/profile", headers={'auth-token': data["access_token"]})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user1@example.com"

