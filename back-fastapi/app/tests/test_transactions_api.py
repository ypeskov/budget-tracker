import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.tests.conftest import categories_path_prefix, accounts_path_prefix, transactions_path_prefix
from app.tests.data.accounts_data import test_accounts
from app.main import app

import icecream
from icecream import ic

icecream.install()

client = TestClient(app)


@pytest.mark.parametrize("amount", [100, 200, 125_000, 500_000_000])
def test_create_transaction_expense_route(token, one_account, amount):
    categories_response = client.get(f'{categories_path_prefix}/', headers={'auth-token': token})
    assert categories_response.status_code == 200
    categories = categories_response.json()

    operations = ['expense', 'income',]
    for operation in operations:
        accounts_response = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token})
        account = accounts_response.json()
        initial_balance_acc = account['balance']

        is_income = True if operation == 'income' else False
        transaction_response = client.post(
            f'{transactions_path_prefix}/',
            json={
                'account_id': one_account['id'],
                'category_id': categories[0]['id'],
                'amount': amount,
                'currency_id': one_account['currency_id'],
                'date': '2021-01-01',
                'is_income': is_income,
                'is_transfer': False,
                'notes': 'Test transaction'
            },
            headers={'auth-token': token}
        )
        assert transaction_response.status_code == status.HTTP_200_OK
        transaction = transaction_response.json()

        assert transaction['amount'] == amount
        assert transaction['is_income'] is False if operation == 'expense' else True
        assert transaction['is_transfer'] is False
        assert transaction['notes'] == 'Test transaction'
        assert transaction['account']['id'] == one_account['id']
        assert transaction['category_id'] == categories[0]['id']
        assert transaction['currency_id'] == one_account['currency_id']

        accounts_response = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token})
        account = accounts_response.json()

        if is_income:
            assert account['balance'] == (initial_balance_acc + amount)
        else:
            assert account['balance'] == (initial_balance_acc - amount)
