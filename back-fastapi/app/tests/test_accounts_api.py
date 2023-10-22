import pytest
from fastapi.testclient import TestClient

from app.tests.conftest import accounts_path_prefix
from app.main import app

import icecream
from icecream import ic
icecream.install()

client = TestClient(app)


def test_add_account(token):
    response = client.post(f'{accounts_path_prefix}/',
                           json={
                               "name": "test_account",
                               "currency_id": 1,
                               "account_type_id": 1,
                               "balance": 0
                           },
                           headers={'auth-token': token})
    assert response.status_code == 200
    account_details = response.json()
    assert account_details["name"] == "test_account"
    assert account_details["currency_id"] == 1
    assert account_details["account_type_id"] == 1
    assert account_details["balance"] == 0
    assert "id" in account_details
