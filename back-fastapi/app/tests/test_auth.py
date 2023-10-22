import pytest
from fastapi.testclient import TestClient

from app.tests.conftest import auth_path_prefix
from app.main import app
from app.tests.data.auth_data import test_users

import icecream
icecream.install()

client = TestClient(app)


@pytest.mark.parametrize("test_user", test_users)
def test_create_user(test_user):
    response = client.post(f'{auth_path_prefix}/register/', json=test_user)
    data = response.json()
    assert 'id' in data
    assert data['id'] == test_user['id']
    assert response.status_code == 200
    assert data['email'] == test_user['email']
    assert data['first_name'] == test_user['first_name']
    assert data['last_name'] == test_user['last_name']


@pytest.mark.parametrize("test_user", test_users)
def test_login_user(test_user):
    response = client.post(f'{auth_path_prefix}/login/', json=test_user)
    assert response.status_code == 200
    login_info = response.json()
    assert "access_token" in login_info
    assert login_info["token_type"] == "bearer"

    response = client.get("/auth/profile", headers={'auth-token': login_info["access_token"]})
    assert response.status_code == 200
    profile = response.json()
    assert "id" in profile
    assert profile["id"] == test_user["id"]
    assert profile["email"] == test_user["email"]
    assert profile["first_name"] == test_user["first_name"]
    assert profile["last_name"] == test_user["last_name"]



