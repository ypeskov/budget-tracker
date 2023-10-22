import pytest
from fastapi.testclient import TestClient

from app.tests.conftest import accounts_path_prefix
from app.tests.data.accounts_data import test_accounts
from app.main import app

import icecream
from icecream import ic
icecream.install()

client = TestClient(app)


@pytest.mark.parametrize("test_account", test_accounts)
def test_add_get_account(test_account, token):
    response = client.post(f'{accounts_path_prefix}/', json=test_account, headers={'auth-token': token})
    assert response.status_code == 200
    account_details = response.json()
    assert 'id' in account_details
    assert account_details['name'] == test_account['name']
    assert account_details['currency_id'] == test_account['currency_id']
    assert account_details['account_type_id'] == test_account['account_type_id']
    assert account_details['balance'] == test_account['balance']
    assert 'opening_date' in account_details
    assert account_details['opening_date'] is not None

    response = client.get(f'{accounts_path_prefix}/{account_details["id"]}', headers={'auth-token': token})
    assert response.status_code == 200
    account_details = response.json()
    assert 'id' in account_details
    assert account_details['name'] == test_account['name']
    assert account_details['currency_id'] == test_account['currency_id']
    assert account_details['account_type_id'] == test_account['account_type_id']
    assert account_details['balance'] == test_account['balance']
    assert 'opening_date' in account_details
    assert account_details['opening_date'] is not None
    
