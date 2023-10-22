import pytest
from fastapi.testclient import TestClient

from app.tests.conftest import accounts_path_prefix
from app.tests.data.accounts_data import test_accounts, test_account_types
from app.main import app
from app.models.Account import Account
from app.tests.conftest import db

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

    # delete account after test
    db.query(Account).filter_by(id=account_details['id']).delete()
    db.commit()


def test_get_accounts_list(token, create_accounts):
    response = client.get(f'{accounts_path_prefix}/', headers={'auth-token': token})
    assert response.status_code == 200
    accounts_list = response.json()

    # check if all accounts are in response
    assert len(accounts_list) == len(test_accounts)

    # check first account details in response
    assert accounts_list[0]['name'] == test_accounts[0]['name']
    assert accounts_list[0]['currency_id'] == test_accounts[0]['currency_id']
    assert accounts_list[0]['account_type_id'] == test_accounts[0]['account_type_id']
    assert accounts_list[0]['balance'] == test_accounts[0]['balance']
    assert 'opening_date' in accounts_list[0]
    assert accounts_list[0]['opening_date'] is not None

    # check last account details in response
    assert accounts_list[7]['name'] == test_accounts[7]['name']
    assert accounts_list[7]['currency_id'] == test_accounts[7]['currency_id']
    assert accounts_list[7]['account_type_id'] == test_accounts[7]['account_type_id']
    assert accounts_list[7]['balance'] == test_accounts[7]['balance']
    assert 'opening_date' in accounts_list[7]
    assert accounts_list[7]['opening_date'] is not None


def test_all_account_types_exist(token):
    response = client.get(f'{accounts_path_prefix}/types/', headers={'auth-token': token})
    assert response.status_code == 200
    account_types = response.json()

    assert len(account_types) == len(test_account_types)

    i = 0
    for test_account_type in test_account_types:
        assert test_account_type['name'] == test_account_types[i]['name']
        assert test_account_type['id'] == test_account_types[i]['id']
        assert test_account_type['is_credit'] == test_account_types[i]['is_credit']

        i += 1
