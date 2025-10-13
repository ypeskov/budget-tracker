from decimal import Decimal

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from icecream import ic

from app.logger_config import logger
from app.main import app
from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.User import User
from app.schemas.transaction_schema import (
    CreateTransactionSchema,
    UpdateTransactionSchema,
)
from app.schemas.user_schema import UserLoginSchema
from app.services.auth import get_jwt_token as get_jwt_token_service
from app.services.errors import AccessDenied, InvalidAccount, InvalidCategory
from app.services.transaction_management.errors import InvalidTransaction
from app.services.transactions import create_transaction as create_transaction_service
from app.services.transactions import get_transaction_details, get_transactions
from app.services.transactions import update as update_transaction_service
from app.tests.conftest import (
    accounts_path_prefix,
    auth_path_prefix,
    categories_path_prefix,
    db,
    main_test_user_id,
    transactions_path_prefix,
)
from app.tests.data.accounts_data import test_accounts_data

client = TestClient(app)


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    db.query(Account).delete()
    db.query(Transaction).delete()
    db.query(User).delete()
    db.commit()


@pytest.mark.parametrize("amount", [100, 200, 125_000, 500_000_000])
def test_create_transaction_expense_route(token, one_account, amount):
    categories_response = client.get(f'{categories_path_prefix}/', headers={'auth-token': token})
    assert categories_response.status_code == 200
    categories = categories_response.json()

    income_category = None
    expense_category = None
    for category in categories:
        if category['isIncome']:
            income_category = category
        else:
            expense_category = category
        if income_category and expense_category:
            break

    operations = [
        'expense',
        'income',
    ]
    created_transactions_ids = []
    for operation in operations:
        accounts_response = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token})
        account = accounts_response.json()
        initial_balance_acc = account['balance']

        is_income = True if operation == 'income' else False
        transaction_data = {
            'accountId': one_account['id'],
            'amount': amount,
            'currencyId': one_account['currency_id'],
            'date': '2021-01-01',
            'isIncome': is_income,
            'isTransfer': False,
            'notes': 'Test transaction',
        }

        if operation == 'income':
            transaction_data['categoryId'] = income_category['id']
        else:
            transaction_data['categoryId'] = expense_category['id']

        transaction_response = client.post(
            f'{transactions_path_prefix}/',
            json=transaction_data,
            headers={'auth-token': token},
        )
        assert transaction_response.status_code == status.HTTP_200_OK
        transaction = transaction_response.json()
        created_transactions_ids.append(transaction['id'])

        assert transaction['amount'] == amount
        assert transaction['isIncome'] is False if operation == 'expense' else True
        assert transaction['isTransfer'] is False
        assert transaction['notes'] == 'Test transaction'
        assert transaction['account']['id'] == one_account['id']
        if operation == 'income':
            assert transaction['categoryId'] == income_category['id']
        else:
            assert transaction['categoryId'] == expense_category['id']

        accounts_response = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token})
        account = accounts_response.json()

        assert account['balance'] == (initial_balance_acc + amount if is_income else initial_balance_acc - amount)

        # and now test the get transaction details route
        transaction_response = client.get(
            f'{transactions_path_prefix}/{transaction["id"]}',
            headers={'auth-token': token},
        )
        assert transaction_response.status_code == status.HTTP_200_OK
        transaction_details = transaction_response.json()
        assert transaction_details['id'] == transaction['id']
        assert transaction_details['amount'] == transaction_data['amount']
        assert transaction_details['isIncome'] == transaction_data['isIncome']
        assert transaction_details['isTransfer'] == transaction_data['isTransfer']
        assert transaction_details['notes'] == transaction_data['notes']
        assert transaction_details['account']['id'] == transaction_data['accountId']
        assert transaction_details['categoryId'] == transaction_data['categoryId']

        # get all transactions for the user
        transactions_response = client.get(f'{transactions_path_prefix}/', headers={'auth-token': token})
        assert transactions_response.status_code == status.HTTP_200_OK
        transactions = transactions_response.json()
        assert len(transactions) == len(created_transactions_ids)
        for t in transactions:
            assert t['id'] in created_transactions_ids


def test_update_transaction(token, one_account, create_user):
    initial_balance_acc: float | Decimal = one_account['balance']
    amount_initial: int = 100

    categories_dict: dict = client.get(f'{categories_path_prefix}/', headers={'auth-token': token}).json()
    expense_category = None
    income_category = None
    for category in categories_dict:
        if category['isIncome']:
            income_category = category
        else:
            expense_category = category
        if income_category and expense_category:
            break

    transaction_data = {
        'account_id': one_account['id'],
        'category_id': expense_category['id'],
        'amount': amount_initial,
        'currency_id': one_account['currency_id'],
        'date_time': '2023-10-12T12:00:00Z',
        'is_income': False,
        'is_transfer': False,
        'notes': 'Test transaction',
    }
    transaction_response = client.post(
        f'{transactions_path_prefix}/',
        json=transaction_data,
        headers={'auth-token': token},
    )
    assert transaction_response.status_code == status.HTTP_200_OK
    transaction = transaction_response.json()

    updated_account = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token}).json()
    assert updated_account['balance'] == initial_balance_acc - amount_initial
    updated_balance = updated_account['balance']

    amount_update = 200
    # update transaction
    transaction_data['id'] = transaction['id']
    transaction_data['user_id'] = transaction['userId']
    transaction_data['amount'] = amount_update
    transaction_data['is_income'] = True
    transaction_data['notes'] = 'Updated transaction'
    transaction_data['category_id'] = income_category['id']
    transaction_data['date_time'] = '2023-10-12T12:00:00Z'

    updated_transaction_response = client.put(
        f'{transactions_path_prefix}/',
        json=transaction_data,
        headers={'auth-token': token},
    )

    assert updated_transaction_response.status_code == status.HTTP_200_OK
    updated_transaction = updated_transaction_response.json()

    assert updated_transaction['id'] == transaction['id']
    assert updated_transaction['amount'] == transaction_data['amount']
    assert updated_transaction['isIncome'] == transaction_data['is_income']
    assert updated_transaction['notes'] == transaction_data['notes']
    assert updated_transaction['account']['id'] == transaction_data['account_id']
    assert updated_transaction['categoryId'] == transaction_data['category_id']

    updated_account = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token}).json()
    assert updated_account['balance'] == updated_balance + transaction_data['amount'] + amount_initial

    with pytest.raises(InvalidTransaction) as ex:
        updated_transaction['id'] = 999_999_999
        update_transaction_service(UpdateTransactionSchema(**updated_transaction), main_test_user_id, db)

    with pytest.raises(InvalidAccount):
        updated_transaction['id'] = transaction['id']
        updated_transaction['accountId'] = 999_999_999
        transaction_schema_update = UpdateTransactionSchema(**updated_transaction)
        update_transaction_service(transaction_schema_update, main_test_user_id, db)

    user2 = create_user('email2@email.com', 'qqq_111_')
    with pytest.raises(AccessDenied):
        updated_transaction['id'] = transaction['id']
        updated_transaction['accountId'] = one_account['id']
        updated_transaction['userId'] = user2.id
        transaction_schema_update = UpdateTransactionSchema(**updated_transaction)
        update_transaction_service(transaction_schema_update, user2.id, db)

    with pytest.raises(InvalidTransaction):
        updated_transaction['id'] = transaction['id']
        updated_transaction['isTransfer'] = True
        updated_transaction['targetAccountId'] = 999_999_999
        transaction_schema_update = UpdateTransactionSchema(**updated_transaction)
        update_transaction_service(transaction_schema_update, main_test_user_id, db)

    with pytest.raises(InvalidCategory) as ex:
        updated_transaction['categoryId'] = 999_999_999
        updated_transaction['isTransfer'] = False
        updated_transaction['targetAccountId'] = None
        transaction_schema_update = UpdateTransactionSchema(**updated_transaction)
        update_transaction_service(transaction_schema_update, main_test_user_id, db)


def test_update_transaction_transfer_type(token, one_account, create_transaction):
    categories = client.get(f'{categories_path_prefix}/', headers={'auth-token': token}).json()
    currencies = client.get('/currencies/', headers={'auth-token': token}).json()

    second_acc_details = {
        **one_account,
        'name': 'Second account',
        'id': one_account['id'] + 1,
        'currency_id': currencies[1]['id'],
    }
    second_account_dict: dict = client.post(
        f'{accounts_path_prefix}/',
        json=second_acc_details,
        headers={'auth-token': token},
    ).json()
    src_amount = 100
    target_amount = 200

    transaction_details = {
        'account_id': one_account['id'],
        'category_id': categories[0]['id'],
        'amount': src_amount,
        'currency_id': one_account['currency_id'],
        'date_time': '2023-10-12T12:00:00Z',
        'is_income': False,
        'is_transfer': True,
        'notes': 'Test transaction',
        'target_account_id': second_account_dict['id'],
        'target_amount': target_amount,
    }
    transaction: Transaction = create_transaction_service(
        CreateTransactionSchema(**transaction_details), main_test_user_id, db
    )
    acc1_updated_balance = (client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token}).json())[
        'balance'
    ]
    acc2_updated_balance = (client.get(f'/accounts/{second_account_dict["id"]}', headers={'auth-token': token}).json())[
        'balance'
    ]
    assert acc1_updated_balance == one_account['balance'] - src_amount
    assert acc2_updated_balance == second_account_dict['balance'] + target_amount

    new_src_amount = 50
    new_target_amount = 100
    transaction_details_update = {
        **transaction_details,
        'id': transaction.id,
        'user_id': transaction.user_id,
        'amount': new_src_amount,
        'target_amount': new_target_amount,
    }
    update_transaction_service(UpdateTransactionSchema(**transaction_details_update), main_test_user_id, db)

    updated_first_account = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token}).json()
    updated_second_account = client.get(f'/accounts/{second_account_dict["id"]}', headers={'auth-token': token}).json()

    assert updated_first_account['balance'] == acc1_updated_balance + src_amount - new_src_amount
    assert updated_second_account['balance'] == acc2_updated_balance - target_amount + new_target_amount

    db.query(Transaction).filter(Transaction.id == transaction.id).delete()
    db.query(Account).filter(Account.id == second_account_dict['id']).delete()
    db.commit()


def test_update_transaction_forbidden_category(one_account, create_user, create_transaction, token):
    categories = client.get(f'{categories_path_prefix}/', headers={'auth-token': token}).json()

    email = 'email@email.com'
    password = 'qqq_111_'
    second_user: User = create_user(email, password)
    second_user_token: str = get_jwt_token_service(UserLoginSchema(email=email, password=password), db).access_token
    second_user_categories: dict = client.get(
        f'{categories_path_prefix}/', headers={'auth-token': second_user_token}
    ).json()

    transaction_details: dict = {
        'account_id': one_account['id'],
        # 'user_id': main_test_user_id,
        'category_id': categories[0]['id'],
        'amount': 100,
        'currency_id': one_account['currency_id'],
        'date_time': '2023-10-12T12:00:00Z',
        'is_income': False,
        'is_transfer': False,
    }
    transaction: Transaction = create_transaction_service(
        CreateTransactionSchema(**transaction_details), main_test_user_id, db
    )
    assert transaction.category_id == categories[0]['id']

    transaction_details['id'] = transaction.id
    transaction_details['user_id'] = second_user.id
    transaction_details['category_id'] = second_user_categories[0]['id']
    with pytest.raises(AccessDenied) as ex:
        update_transaction_service(UpdateTransactionSchema(**transaction_details), main_test_user_id, db)

    db.query(Transaction).filter(Transaction.id == transaction.id).delete()
    db.query(User).filter(User.id == second_user.id).delete()
    db.commit()


def test_process_transfer_type(create_transaction, token, one_account, create_user):
    second_account_details = {
        **one_account,
        'name': 'Second account',
        'id': one_account['id'] + 1,
    }

    second_account_response = client.post(
        f'{accounts_path_prefix}/',
        json=second_account_details,
        headers={'auth-token': token},
    )
    assert second_account_response.status_code == status.HTTP_200_OK
    json_response = second_account_response.json()
    second_account = Account(
        user_id=json_response['userId'],
        account_type_id=json_response['accountTypeId'],
        balance=json_response['balance'],
        currency_id=json_response['currencyId'],
        id=json_response['id'],
        initial_balance=json_response['initialBalance'],
        is_hidden=json_response['isHidden'],
        name=json_response['name'],
        opening_date=json_response['openingDate'],
        comment=json_response['comment'],
    )
    transaction_details = {
        'accountId': one_account['id'],
        'amount': 100,
        'date': '2021-01-01',
        'isIncome': False,
        'isTransfer': True,
        'notes': 'Test transaction',
        'targetAccountId': second_account.id,
    }
    transaction: Transaction = create_transaction(transaction_details)
    assert transaction.is_transfer is True

    updated_account = client.get(f'/accounts/{one_account["id"]}', headers={'auth-token': token}).json()
    assert updated_account['balance'] == one_account['balance'] - 100
    updated_account2 = client.get(f'/accounts/{second_account.id}', headers={'auth-token': token}).json()
    assert updated_account2['balance'] == second_account.balance + 100

    new_user = create_user('ex@ex.com', 'qqq_111_')
    new_user_profile = client.post(
        f'{auth_path_prefix}/login/',
        json={
            'email': 'ex@ex.com',
            'password': 'qqq_111_',
        },
    )
    new_user_token = new_user_profile.json()['accessToken']
    third_account_details = {
        **one_account,
        'name': 'Third account',
        'id': one_account['id'] + 2,
        'user_id': new_user.id,
    }
    third_account_response = client.post(
        f'{accounts_path_prefix}/',
        json=third_account_details,
        headers={'auth-token': new_user_token},
    )
    assert third_account_response.status_code == status.HTTP_200_OK
    json_response = third_account_response.json()
    third_account = Account(
        user_id=json_response['userId'],
        account_type_id=json_response['accountTypeId'],
        balance=json_response['balance'],
        currency_id=json_response['currencyId'],
        id=json_response['id'],
        initial_balance=json_response['initialBalance'],
        is_hidden=json_response['isHidden'],
        name=json_response['name'],
        opening_date=json_response['openingDate'],
        comment=json_response['comment'],
    )

    db.query(Account).filter(Account.id == second_account.id).delete()
    db.query(Account).filter(Account.id == third_account.id).delete()
    db.query(Transaction).filter(Transaction.id == transaction.id).delete()
    db.query(Account).filter(Account.id == one_account['id']).delete()
    db.query(User).filter(User.id == new_user.id).delete()
    db.commit()


def test_process_transfer_type_diff_currencies(create_transaction, token, one_account, create_user):
    first_account = Account(**one_account)
    first_account.balance = Decimal(first_account.balance)

    user2 = create_user('email@email.com', 'qqq_111_')

    currencies = client.get('/currencies/', headers={'auth-token': token}).json()

    second_account_details = {
        **test_accounts_data[0],
        'name': 'Second account',
        'id': first_account.id + 1,
        'currency_id': currencies[1]['id'],
    }
    json_response = client.post(
        f'{accounts_path_prefix}/',
        json=second_account_details,
        headers={'auth-token': token},
    ).json()
    second_account = Account(
        user_id=json_response['userId'],
        account_type_id=json_response['accountTypeId'],
        balance=json_response['balance'],
        currency_id=json_response['currencyId'],
        id=json_response['id'],
        initial_balance=json_response['initialBalance'],
        is_hidden=json_response['isHidden'],
        name=json_response['name'],
        opening_date=json_response['openingDate'],
        comment=json_response['comment'],
    )
    second_account.balance = Decimal(second_account.balance)

    transaction_details = {
        'accountId': first_account.id,
        'amount': 100,
        'date': '2021-01-01',
        'isIncome': False,
        'isTransfer': True,
        'notes': 'Test transaction',
        'targetAccountId': second_account.id,
        'targetAmount': 200,
    }
    transaction: Transaction = create_transaction(transaction_details)

    account1_updated = client.get(f'/accounts/{first_account.id}', headers={'auth-token': token}).json()
    account2_updated = client.get(f'/accounts/{second_account.id}', headers={'auth-token': token}).json()
    assert account1_updated['balance'] == first_account.balance - 100
    assert account2_updated['balance'] == second_account.balance + 200

    db.query(Account).filter(Account.id == first_account.id).delete()
    db.query(Account).filter(Account.id == second_account.id).delete()
    db.query(Transaction).filter(Transaction.id == transaction.id).delete()
    db.query(User).filter(User.id == user2.id).delete()
    db.commit()


def test_process_non_transfer_type(create_transaction, token, one_account, create_user):
    first_account = Account(**one_account)
    first_account.balance = Decimal(first_account.balance)

    amount = 100
    transaction_details = {
        'accountId': first_account.id,
        'amount': amount,
        'date': '2021-01-01',
        'isIncome': False,
        'isTransfer': False,
        'notes': 'Test transaction',
        'targetAccountId': None,
    }
    transaction1: Transaction = create_transaction(transaction_details)
    updated_account = client.get(f'/accounts/{first_account.id}', headers={'auth-token': token}).json()
    assert first_account.balance - amount == updated_account['balance']
    updated_balance = updated_account['balance']

    transaction_details['isIncome'] = True
    transaction2 = create_transaction(transaction_details)
    updated_account = client.get(f'/accounts/{first_account.id}', headers={'auth-token': token}).json()
    assert updated_account['balance'] == updated_balance + amount

    db.query(Account).filter(Account.id == first_account.id).delete()
    db.query(Transaction).filter(Transaction.id == transaction1.id).delete()
    db.query(Transaction).filter(Transaction.id == transaction2.id).delete()
    db.commit()


def test_create_transaction_expense_route_invalid_account(token, one_account):
    categories_response = client.get(f'{categories_path_prefix}/', headers={'auth-token': token})
    assert categories_response.status_code == 200
    categories = categories_response.json()

    operations = [
        'expense',
        'income',
    ]
    for operation in operations:
        transaction_data = {
            'account_id': 999999999,
            'category_id': categories[0]['id'],
            'amount': 100,
            'currency_id': one_account['currency_id'],
            'date': '2021-01-01',
            'is_income': True if operation == 'income' else False,
            'is_transfer': False,
            'notes': 'Test transaction',
        }
        transaction_response = client.post(
            f'{transactions_path_prefix}/',
            json=transaction_data,
            headers={'auth-token': token},
        )
        assert transaction_response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    # clean up created transactions
    db.query(Transaction).filter(Transaction.account_id == 999999999).delete()
    db.commit()


def test_create_transaction_expense_route_invalid_category(token, one_account):
    operations = [
        'expense',
        'income',
    ]
    for operation in operations:
        transaction_data = {
            'account_id': one_account['id'],
            'category_id': 999999999,
            'amount': 100,
            'currency_id': one_account['currency_id'],
            'date': '2021-01-01',
            'is_income': True if operation == 'income' else False,
            'is_transfer': False,
            'notes': 'Test transaction',
        }
        transaction_response = client.post(
            f'{transactions_path_prefix}/',
            json=transaction_data,
            headers={'auth-token': token},
        )
        logger.info(transaction_response.json())
        assert transaction_response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    # clean up created transactions
    db.query(Transaction).filter(Transaction.category_id == 999999999).delete()
    db.commit()


def test_create_transaction_forbidden(create_user):
    email1 = 'email1@email.com'
    password = 'qqq_111_'
    user1 = create_user(email1, password)
    user1_token = client.post(f'{auth_path_prefix}/login/', json={'email': email1, 'password': password}).json()[
        'accessToken'
    ]

    email2 = 'email2@email.com'
    user2 = create_user(email2, password)
    user2_token = client.post(f'{auth_path_prefix}/login/', json={'email': email2, 'password': password}).json()[
        'accessToken'
    ]
    user2_categories = client.get(f'{categories_path_prefix}/', headers={'auth-token': user2_token}).json()

    account_details = {
        'name': 'Test account',
        'account_type_id': 2,
        'initial_balance': 100,
        'balance': 100,
        'currency_id': 1,
        'user_id': user1.id,
    }
    account_response = client.post(
        f'{accounts_path_prefix}/',
        json=account_details,
        headers={'auth-token': user1_token},
    )
    assert account_response.status_code == status.HTTP_200_OK
    json_response = account_response.json()
    account = Account(
        user_id=json_response['userId'],
        account_type_id=json_response['accountTypeId'],
        balance=json_response['balance'],
        currency_id=json_response['currencyId'],
        id=json_response['id'],
        initial_balance=json_response['initialBalance'],
        is_hidden=json_response['isHidden'],
        name=json_response['name'],
        opening_date=json_response['openingDate'],
        comment=json_response['comment'],
    )

    transaction_data = {
        'account_id': account.id,
        'category_id': user2_categories[0]['id'],
        'amount': 100,
        'currency_id': account.currency_id,
        'date': '2021-01-01',
        'is_income': False,
        'is_transfer': False,
        'notes': 'Test transaction',
    }
    transaction_response = client.post(
        f'{transactions_path_prefix}/',
        json=transaction_data,
        headers={'auth-token': user1_token},
    )
    assert transaction_response.status_code == status.HTTP_403_FORBIDDEN

    db.query(Account).filter(Account.id == account.id).delete()
    db.query(User).filter(User.id == user1.id).delete()
    db.query(User).filter(User.id == user2.id).delete()
    db.commit()


def test_create_transaction_forbidden_account(create_user):
    email1 = 'email1@email.com'
    password = 'qqq_111_'
    user1 = create_user(email1, password)

    email2 = 'email2@email.com'
    user2 = create_user(email2, 'qqq_111_')
    user2_token = client.post(f'{auth_path_prefix}/login/', json={'email': email2, 'password': password}).json()[
        'accessToken'
    ]

    account2_details = {
        'name': 'Test account',
        'account_type_id': 2,
        'initial_balance': 100,
        'balance': 100,
        'currency_id': 1,
        'user_id': user2.id,
    }
    account2 = client.post(
        f'{accounts_path_prefix}/',
        json=account2_details,
        headers={'auth-token': user2_token},
    ).json()
    categories = client.get(f'{categories_path_prefix}/', headers={'auth-token': user2_token}).json()
    transaction_details = {
        'account_id': account2['id'],
        'category_id': categories[0]['id'],
        'amount': 100,
        'currency_id': account2['currencyId'],
        'date': '2021-01-01',
        'is_income': False,
        'is_transfer': False,
        'notes': 'Test transaction',
        'target_account_id': account2['id'],
    }
    transaction_schema = CreateTransactionSchema(**transaction_details)

    with pytest.raises(AccessDenied) as ex:
        create_transaction_service(transaction_schema, user1.id, db)

    db.query(Account).filter(Account.id == account2['id']).delete()
    db.query(User).filter(User.id == user1.id).delete()
    db.query(User).filter(User.id == user2.id).delete()
    db.commit()


def test_get_all_transactions(token, create_transaction, one_account):
    categories = client.get(f'{categories_path_prefix}/', headers={'auth-token': token}).json()

    transaction_details = {
        'account_id': one_account['id'],
        'amount': 100,
        'category_id': categories[0]['id'],
        'currency_id': one_account['currency_id'],
        'is_income': False,
        'is_transfer': False,
        'notes': 'Test transaction',
        'target_account_id': None,
    }

    number_of_transactions = 10
    transactions: list[Transaction] = []
    for transaction in range(number_of_transactions):
        transactions.append(
            create_transaction_service(CreateTransactionSchema(**transaction_details), main_test_user_id, db)
        )

    transactions_from_service = get_transactions(main_test_user_id, db)
    assert len(transactions_from_service) == number_of_transactions

    transactions_from_service = get_transactions(
        main_test_user_id,
        db,
        {
            'types': [
                'expense',
            ]
        },
    )
    assert len(transactions_from_service) == number_of_transactions

    transactions_from_service = get_transactions(
        main_test_user_id,
        db,
        {
            'types': [
                'income',
            ]
        },
    )
    assert len(transactions_from_service) == 0

    transactions_from_service = get_transactions(main_test_user_id, db, {'types': ['expense', 'income']})
    assert len(transactions_from_service) == number_of_transactions

    transactions_from_service = get_transactions(main_test_user_id, db, {'types': ['transfer', 'income']})
    assert len(transactions_from_service) == 0

    transactions_from_service = get_transactions(
        main_test_user_id, db, {'types': ['transfer', 'income'], 'categories': []}
    )
    assert len(transactions_from_service) == 0

    transactions_from_service = get_transactions(main_test_user_id, db, {'currencies': [1, 2, 3, 4]})
    assert len(transactions_from_service) == number_of_transactions

    transactions_from_service = get_transactions(
        main_test_user_id,
        db,
        {
            'accounts': [
                one_account['id'],
            ]
        },
    )
    assert len(transactions_from_service) == number_of_transactions

    transactions_from_service = get_transactions(main_test_user_id, db, {'page': 1, 'per_page': 5})
    assert len(transactions_from_service) == 5

    for transaction in transactions_from_service:
        db.query(Transaction).filter(Transaction.id == transaction.id).delete()
    db.commit()


def test_get_transaction_details(token, create_transaction, one_account):
    categories = client.get(f'{categories_path_prefix}/', headers={'auth-token': token}).json()

    transaction_details = {
        'account_id': one_account['id'],
        'amount': 100,
        'category_id': categories[0]['id'],
        'currency_id': one_account['currency_id'],
        'is_income': False,
        'is_transfer': False,
        'notes': 'Test transaction',
        'target_account_id': None,
    }

    transaction = create_transaction_service(CreateTransactionSchema(**transaction_details), main_test_user_id, db)

    transaction_from_service = get_transaction_details(transaction_id=transaction.id, user_id=main_test_user_id, db=db)
    assert transaction_from_service.id == transaction.id
    assert transaction_from_service.amount == transaction.amount
    assert transaction_from_service.is_income == transaction.is_income
    assert transaction_from_service.is_transfer == transaction.is_transfer
    assert transaction_from_service.notes == transaction.notes
    assert transaction_from_service.account_id == transaction.account_id
    assert transaction_from_service.category_id == transaction.category_id

    with pytest.raises(HTTPException) as ex:
        get_transaction_details(999_999_999, main_test_user_id, db)
    assert ex.value.status_code == status.HTTP_404_NOT_FOUND
    assert ex.value.detail == 'Transaction not found'

    db.query(Transaction).filter(Transaction.id == transaction.id).delete()
    db.commit()


def test_get_transaction_details_forbidden(token, create_transaction, one_account, create_user):
    email = 'email@email.com'
    password = 'qqq_111_'
    user2 = create_user(email, password)
    categories = client.get(f'{categories_path_prefix}/', headers={'auth-token': token}).json()

    transaction_details = {
        'account_id': one_account['id'],
        'amount': 100,
        'category_id': categories[0]['id'],
        'currency_id': one_account['currency_id'],
        'is_income': False,
        'is_transfer': False,
        'notes': 'Test transaction',
        'target_account_id': None,
    }

    transaction = create_transaction_service(CreateTransactionSchema(**transaction_details), main_test_user_id, db)
    with pytest.raises(HTTPException) as ex:
        get_transaction_details(transaction_id=transaction.id, user_id=user2.id, db=db)
    assert ex.value.status_code == status.HTTP_403_FORBIDDEN
    assert ex.value.detail == 'Forbidden'
