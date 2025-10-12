import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from icecream import ic

from app.main import app
from app.models.User import User
from app.tests.conftest import auth_path_prefix, db
from app.tests.data.auth_data import test_users

ic.configureOutput(includeContext=True)

client = TestClient(app)


@pytest.mark.parametrize("test_user", test_users)
def test_create_user(test_user):
    response = client.post(f'{auth_path_prefix}/register/', json=test_user)
    data = response.json()

    assert 'id' in data
    assert data['id'] == test_user['id']
    assert response.status_code == 200
    assert data['email'] == test_user['email']
    assert data['firstName'] == test_user['firstName']
    assert data['lastName'] == test_user['lastName']

    db.query(User).delete()


@pytest.mark.parametrize("test_user", test_users)
def test_login_user(test_user, create_user):
    create_user(
        test_user['email'],
        test_user['password'],
        test_user['firstName'],
        test_user['lastName'],
    )
    response = client.post(f'{auth_path_prefix}/login/', json=test_user)
    assert response.status_code == 200
    login_info = response.json()
    assert "accessToken" in login_info
    assert login_info["tokenType"] == "bearer"

    response = client.get(
        "/auth/profile", headers={'auth-token': login_info["accessToken"]}
    )
    assert response.status_code == 200

    profile = response.json()
    assert "id" in profile
    assert profile["email"] == test_user["email"]
    assert profile["first_name"] == test_user["firstName"]
    assert profile["last_name"] == test_user["lastName"]


def test_create_existing_user(token):
    user_response = client.get("/auth/profile", headers={'auth-token': token})
    assert user_response.status_code == status.HTTP_200_OK
    existing_user = user_response.json()
    existing_user['password'] = 'new_password'

    response = client.post(f'{auth_path_prefix}/register/', json=existing_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == {'detail': 'User with this email already exists'}


def test_incorrect_password(token):
    user_response = client.get("/auth/profile", headers={'auth-token': token})
    assert user_response.status_code == status.HTTP_200_OK
    existing_user = user_response.json()
    existing_user['password'] = 'wrong_password'

    response = client.post(f'{auth_path_prefix}/login/', json=existing_user)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_incorrect_email(token):
    user_response = client.get("/auth/profile", headers={'auth-token': token})
    assert user_response.status_code == status.HTTP_200_OK
    existing_user = user_response.json()
    existing_user['email'] = 'wrong@wrong.com'
    existing_user['password'] = 'new_password'

    response = client.post(f'{auth_path_prefix}/login/', json=existing_user)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
