from decimal import Decimal

import pytest
from fastapi import status, HTTPException
from fastapi.testclient import TestClient

from app.models.Account import Account
from app.tests.conftest import categories_path_prefix, transactions_path_prefix, accounts_path_prefix, auth_path_prefix
from app.tests.conftest import db
from app.main import app
from app.models.Transaction import Transaction
from app.services.transactions import process_transfer_type
from app.services.CurrencyProcessor import CurrencyProcessor

import icecream
from icecream import ic

icecream.install()

client = TestClient(app)


@pytest.mark.parametrize("amount", [100, 200, 125_000, 500_000_000])
def test_create_transaction_expense_route(token, one_account, amount):
    categories_response = client.get(f'{categories_path_prefix}/', headers={'auth-token': token})
    assert categories_response.status_code == 200
    categories = categories_response.json()

    operations = ['expense', 'income', ]
    created_transactions_ids = []
    for operation in operations:
        accounts_response = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token})
        account = accounts_response.json()
        initial_balance_acc = account['balance']

        is_income = True if operation == 'income' else False
        transaction_data = {
            'account_id': one_account['id'],
            'category_id': categories[0]['id'],
            'amount': amount,
            'currency_id': one_account['currency_id'],
            'date': '2021-01-01',
            'is_income': is_income,
            'is_transfer': False,
            'notes': 'Test transaction'
        }
        transaction_response = client.post(f'{transactions_path_prefix}/', json=transaction_data,
                                           headers={'auth-token': token})
        assert transaction_response.status_code == status.HTTP_200_OK
        transaction = transaction_response.json()
        created_transactions_ids.append(transaction['id'])

        assert transaction['amount'] == amount
        assert transaction['is_income'] is False if operation == 'expense' else True
        assert transaction['is_transfer'] is False
        assert transaction['notes'] == 'Test transaction'
        assert transaction['account']['id'] == one_account['id']
        assert transaction['category_id'] == categories[0]['id']
        assert transaction['currency_id'] == one_account['currency_id']

        accounts_response = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token})
        account = accounts_response.json()

        assert account['balance'] == (initial_balance_acc + amount if is_income else initial_balance_acc - amount)

        # and now test the get transaction details route
        transaction_response = client.get(f'{transactions_path_prefix}/{transaction["id"]}',
                                          headers={'auth-token': token})
        assert transaction_response.status_code == status.HTTP_200_OK
        transaction_details = transaction_response.json()
        assert transaction_details['id'] == transaction['id']
        assert transaction_details['amount'] == transaction_data['amount']
        assert transaction_details['is_income'] == transaction_data['is_income']
        assert transaction_details['is_transfer'] == transaction_data['is_transfer']
        assert transaction_details['notes'] == transaction_data['notes']
        assert transaction_details['account']['id'] == transaction_data['account_id']
        assert transaction_details['category_id'] == transaction_data['category_id']
        assert transaction_details['currency_id'] == transaction_data['currency_id']

        # get all transactions for the user
        transactions_response = client.get(f'{transactions_path_prefix}/', headers={'auth-token': token})
        assert transactions_response.status_code == status.HTTP_200_OK
        transactions = transactions_response.json()
        assert len(transactions) == len(created_transactions_ids)
        for t in transactions:
            assert t['id'] in created_transactions_ids

    # clean up created transactions
    for i in created_transactions_ids:
        db.query(Transaction).filter(Transaction.id == i).delete()
    db.commit()


def test_update_transaction(token, one_account):
    account_response = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token})
    account = account_response.json()
    initial_balance_acc = account['balance']
    amount = 100

    categories_response = client.get(f'{categories_path_prefix}/', headers={'auth-token': token})
    assert categories_response.status_code == 200
    categories = categories_response.json()

    transaction_data = {
        'account_id': one_account['id'],
        'category_id': categories[0]['id'],
        'amount': amount,
        'currency_id': one_account['currency_id'],
        'date': '2021-01-01',
        'is_income': False,
        'is_transfer': False,
        'notes': 'Test transaction'
    }
    transaction_response = client.post(f'{transactions_path_prefix}/', json=transaction_data,
                                       headers={'auth-token': token})
    assert transaction_response.status_code == status.HTTP_200_OK
    transaction = transaction_response.json()

    # update transaction
    transaction_data['id'] = transaction['id']
    transaction_data['user_id'] = transaction['user_id']
    transaction_data['amount'] = 200
    transaction_data['is_income'] = True
    transaction_data['notes'] = 'Updated transaction'
    transaction_data['category_id'] = categories[1]['id']
    transaction_data['date'] = '2021-01-02'
    updated_transaction_response = client.put(f'{transactions_path_prefix}/{transaction["id"]}',
                                              json=transaction_data,
                                              headers={'auth-token': token})
    assert updated_transaction_response.status_code == status.HTTP_200_OK
    updated_transaction = updated_transaction_response.json()

    assert updated_transaction['id'] == transaction['id']
    assert updated_transaction['amount'] == transaction_data['amount']
    assert updated_transaction['is_income'] == transaction_data['is_income']
    assert updated_transaction['is_transfer'] == transaction_data['is_transfer']
    assert updated_transaction['notes'] == transaction_data['notes']
    assert updated_transaction['account']['id'] == transaction_data['account_id']
    assert updated_transaction['category_id'] == transaction_data['category_id']
    assert updated_transaction['currency_id'] == transaction_data['currency_id']


def test_currency_processor(create_transaction, token, one_account):
    transaction: Transaction = create_transaction(one_account, 100)

    with pytest.raises(HTTPException) as ex:
        CurrencyProcessor(None, db).calculate_exchange_rate()
    assert ex.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert ex.value.detail == 'Transaction is required'

    with pytest.raises(HTTPException) as ex:
        CurrencyProcessor(transaction, db).calculate_exchange_rate()
    assert ex.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert ex.value.detail == 'Exchange rate or target amount are required'

    transaction.exchange_rate = Decimal(1.5)
    transaction.target_amount = Decimal(100)
    with pytest.raises(HTTPException) as ex:
        CurrencyProcessor(transaction, db).calculate_exchange_rate()
    assert ex.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert ex.value.detail == 'Only one parameter must be provided: Exchange rate or target amount'

    transaction.exchange_rate = Decimal(1.5)
    transaction.target_amount = None
    transaction = CurrencyProcessor(transaction, db).calculate_exchange_rate()
    assert transaction.target_amount == 150

    transaction.exchange_rate = None
    transaction.target_amount = Decimal(150)
    transaction = CurrencyProcessor(transaction, db).calculate_exchange_rate()
    assert transaction.exchange_rate == 1.5

    db.query(Transaction).filter(Transaction.id == transaction.id).delete()
    db.commit()


def test_process_transfer_type(create_transaction, token, one_account, create_user):
    second_account_details = {**one_account, 'name': 'Second account', 'id': one_account['id'] + 1}
    second_account_response = client.post(f'{accounts_path_prefix}/', json=second_account_details,
                                          headers={'auth-token': token})
    assert second_account_response.status_code == status.HTTP_200_OK
    second_account = Account(**second_account_response.json())
    transaction: Transaction = create_transaction(one_account, 100)
    transaction.target_account_id = second_account.id
    transaction.target_account = second_account
    transaction.account = Account(**one_account)
    transaction.account.balance = Decimal(transaction.account.balance)

    transaction = process_transfer_type(transaction, transaction.user_id, db)
    assert transaction.is_transfer is False

    transaction.target_account_id = None
    transaction.target_account = None
    with pytest.raises(HTTPException) as ex:
        process_transfer_type(transaction, transaction.user_id, db)
    assert ex.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert ex.value.detail == 'Invalid target account'

    new_user = create_user('ex@ex.com', 'qqq')
    new_user_profile = client.post(f'{auth_path_prefix}/login/', json={
        'email': 'ex@ex.com',
        'password': 'qqq',
    })
    new_user_token = new_user_profile.json()['access_token']
    third_account_details = {**one_account, 'name': 'Third account', 'id': one_account['id'] + 2,
                             'user_id': new_user.id}
    third_account_response = client.post(f'{accounts_path_prefix}/', json=third_account_details,
                                         headers={'auth-token': new_user_token})
    assert third_account_response.status_code == status.HTTP_200_OK
    third_account = Account(**third_account_response.json())

    transaction.target_account_id = third_account.id
    transaction.target_account = third_account
    transaction.target_account_id = third_account.id
    with pytest.raises(HTTPException) as ex:
        process_transfer_type(transaction, transaction.user_id, db)
    assert ex.value.status_code == status.HTTP_403_FORBIDDEN
    assert ex.value.detail == 'Forbidden'
