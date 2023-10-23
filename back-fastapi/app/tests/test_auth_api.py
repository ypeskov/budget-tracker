import pytest
from fastapi import status, HTTPException
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


def test_create_existing_user(token):
    user_response = client.get("/auth/profile", headers={'auth-token': token})
    assert user_response.status_code == status.HTTP_200_OK
    existing_user = user_response.json()
    existing_user['password'] = 'new_password'

    response = client.post(f'{auth_path_prefix}/register/', json=existing_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': 'User with this email already exists'}


def test_incorrect_password(token):
    user_response = client.get("/auth/profile", headers={'auth-token': token})
    assert user_response.status_code == status.HTTP_200_OK
    existing_user = user_response.json()
    existing_user['password'] = 'wrong_password'

    response = client.post(f'{auth_path_prefix}/login/', json=existing_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_incorrect_email(token):
    user_response = client.get("/auth/profile", headers={'auth-token': token})
    assert user_response.status_code == status.HTTP_200_OK
    existing_user = user_response.json()
    existing_user['email'] = 'wrong@wrong.com'
    existing_user['password'] = 'new_password'

    response = client.post(f'{auth_path_prefix}/login/', json=existing_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
