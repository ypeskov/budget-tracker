from decimal import Decimal
from collections.abc import Callable

from icecream import ic

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from app.tests.db_test_cfg import override_get_db
from app.data_loaders.work_data.load_all import load_all_data

from app.schemas.account_schema import CreateAccountSchema
from app.schemas.user_schema import UserRegistration, UserLoginSchema

from app.models.User import User
from app.models.Currency import Currency
from app.models.DefaultCategory import DefaultCategory
from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.models.AccountType import AccountType
from app.models.Account import Account

from app.services.accounts import create_account as create_account_service
from app.services.auth import create_users as create_users_service, get_jwt_token as get_jwt_token_service

from app.tests.data.auth_data import test_users, main_test_user
from app.tests.data.accounts_data import test_accounts

ic.configureOutput(includeContext=True)
app.dependency_overrides[get_db] = override_get_db

db = next(override_get_db())
load_all_data(db)

auth_path_prefix = '/auth'
accounts_path_prefix = '/accounts'
currencies_path_prefix = '/currencies'
categories_path_prefix = '/categories'
transactions_path_prefix = '/transactions'

main_test_user_id = 1000
main_user_account1_id = 1
main_user_account2_id = 2

truly_invalid_account_id = 9999999
truly_invalid_account_type_id = 9999999
truly_invalid_currency_id = 9999999

client = TestClient(app)


def pytest_unconfigure(config):
    db.query(User).delete()
    db.query(Currency).delete()
    db.query(AccountType).delete()
    db.query(UserCategory).delete()
    db.query(DefaultCategory).delete()
    db.query(Account).delete()
    db.query(Transaction).delete()
    db.commit()

    print("\n\n------- DB is cleared -------\n\n")


@pytest.fixture(scope="function")
def token():
    """ Create a user for test purposes and return his access token """
    user: User = create_users_service(UserRegistration(**main_test_user), db)
    user_dict = {**user.__dict__}

    if '_sa_instance_state' in user_dict:
        del user_dict['_sa_instance_state']

    token = get_jwt_token_service(UserLoginSchema(**main_test_user), db)

    yield token['access_token']
    db.query(User).filter(User.id == user.id).delete()
    db.commit()


@pytest.fixture(scope="function")
def one_account(token) -> dict:
    account_details = {**test_accounts[0], 'id': main_user_account1_id, 'user_id': main_test_user_id}

    account_schema = CreateAccountSchema(**account_details)
    account: Account = create_account_service(account_schema, main_test_user_id, db)
    account_dict = {**account.__dict__}

    if '_sa_instance_state' in account_dict:
        del account_dict['_sa_instance_state']

    account_dict['balance'] = float(account_dict['balance'])
    account_dict['opening_date'] = str(account_dict['opening_date'])
    account_dict['updated_at'] = str(account_dict['updated_at'])
    account_dict['created_at'] = str(account_dict['created_at'])

    yield account_dict

    db.query(Account).filter_by(id=account.id).delete()
    db.commit()


@pytest.fixture(scope="function")
def fake_account() -> CreateAccountSchema:
    return CreateAccountSchema.model_validate({
        'name': 'Fake account',
        'user_id': main_test_user_id,
        'currency_id': 1,
        'account_type_id': 1,
        'balance': 0,
        'opening_date': None,
        'is_hidden': False,
        'comment': None
    })


@pytest.fixture(scope="function")
def create_accounts(token) -> list[Account]:
    accounts = []
    for test_account in test_accounts:
        accounts.append(
            client.post(f'{accounts_path_prefix}/', json=test_account, headers={'auth-token': token}).json())
    yield accounts
    db.query(Account).filter_by(user_id=main_test_user_id).delete()
    db.commit()


@pytest.fixture(scope="function")
def create_transaction(token) -> Callable[[dict], Transaction]:
    categories_response = client.get(f'{categories_path_prefix}/', headers={'auth-token': token})
    categories = categories_response.json()

    def _create_transaction(transaction_details: dict):
        transaction_data = {
            'account_id': transaction_details['account_id'],
            'category_id': categories[0]['id'],
            'amount': 100,
            'target_amount': 100,
            'currency_id': transaction_details['currency_id'],
            'target_account_id': transaction_details['target_account_id'],
            'is_income': False,
            'is_transfer': False,
            'notes': 'Test transaction'
        }
        transaction_data = {**transaction_data, **transaction_details}

        transaction_response = client.post(f'{transactions_path_prefix}/', json=transaction_data,
                                           headers={'auth-token': token})
        assert transaction_response.status_code == 200
        transaction_props = transaction_response.json()
        transaction = Transaction(id=transaction_props['id'],
                                  user_id=transaction_props['user_id'],
                                  account_id=transaction_props['account_id'],
                                  category_id=transaction_props['category_id'],
                                  target_account_id=transaction_props['target_account_id'],
                                  target_amount=Decimal(transaction_props['target_amount']),
                                  amount=Decimal(transaction_props['amount']),
                                  currency_id=transaction_props['currency_id'],
                                  date_time=transaction_props['date_time'],
                                  is_income=transaction_props['is_income'],
                                  is_transfer=transaction_props['is_transfer'],
                                  notes=transaction_props['notes'])
        return transaction

    return _create_transaction


@pytest.fixture(scope="function")
def create_user():
    def _create_user(email, password):
        user = {
            'email': email,
            'password': password,
        }
        user_response = client.post(f'{auth_path_prefix}/register/', json=user)
        assert user_response.status_code == 200
        user_props = user_response.json()
        return User(**user_props)

    return _create_user
