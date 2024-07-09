import os

from app.models.UserSettings import UserSettings

os.environ['TEST_MODE'] = 'True'

from decimal import Decimal
from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient
from icecream import ic

from app.main import app
from app.database import get_db
from app.config import Settings
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

from app.tests.data.auth_data import main_test_user
from app.tests.data.accounts_data import test_accounts_data

ic.configureOutput(includeContext=True)

settings = Settings()

test_log_file = f"logs/{settings.TEST_LOG_FILE}"
with open(test_log_file, 'w') as f:
    pass

app.dependency_overrides[get_db] = override_get_db

db = next(override_get_db())

auth_path_prefix = '/auth'
accounts_path_prefix = '/accounts'
currencies_path_prefix = '/currencies'
categories_path_prefix = '/categories'
transactions_path_prefix = '/transactions'

main_test_user_id = 1000
main_user_account1_id = 1
main_user_account2_id = 2

truly_invalid_account_id = 999_999_999
truly_invalid_account_type_id = 9_999_999
truly_invalid_currency_id = 9_999_999

client = TestClient(app)


@pytest.fixture(scope='module', autouse=True)
def setup_db():
    db.query(User).delete()
    db.query(Currency).delete()
    db.query(AccountType).delete()
    db.query(UserCategory).delete()
    db.query(DefaultCategory).delete()
    db.query(Account).delete()
    db.query(Transaction).delete()
    db.query(UserSettings).delete()
    db.commit()
    print("\n------- DB is cleared -------")

    load_all_data(db)

    yield

    db.query(User).delete()
    db.query(Currency).delete()
    db.query(AccountType).delete()
    db.query(UserCategory).delete()
    db.query(DefaultCategory).delete()
    db.query(Account).delete()
    db.query(Transaction).delete()
    db.query(UserSettings).delete()
    db.commit()


@pytest.fixture(scope="function")
def token():
    """ Create a user for test purposes and return his access token """
    user: User = create_users_service(UserRegistration.model_validate(main_test_user), db)
    user.is_active = True
    db.commit()
    token = get_jwt_token_service(UserLoginSchema.model_validate(main_test_user), db)

    yield token['access_token']

    db.query(UserSettings).filter(UserSettings.user_id == user.id).delete()
    db.delete(user)
    db.commit()


@pytest.fixture(scope="function")
def one_account(token):
    account_details = {
        **test_accounts_data[0],
        'id': main_user_account1_id,
        'user_id': main_test_user_id,
        'initial_balance': test_accounts_data[0]['balance'],
    }

    account_schema = CreateAccountSchema.model_validate(account_details)
    account: Account = create_account_service(account_schema, main_test_user_id, db)
    account_dict = {**account.__dict__}

    if '_sa_instance_state' in account_dict:
        del account_dict['_sa_instance_state']

    account_dict['initial_balance'] = float(account_dict['initial_balance'])
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
        'initial_balance': 0,
        'balance': 0,
        'opening_date': None,
        'is_hidden': False,
        'comment': ""
    })


@pytest.fixture(scope="function")
def create_accounts(token):
    accounts = [
        create_account_service(CreateAccountSchema.model_validate(test_acc), main_test_user_id, db)
        for test_acc in test_accounts_data
    ]
    yield accounts

    for account in accounts:
        db.delete(db.query(Account).filter(Account.id == account.id).first())


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
                                  user_id=transaction_props['userId'],
                                  account_id=transaction_props['accountId'],
                                  category_id=transaction_props['categoryId'],
                                  target_account_id=transaction_props['targetAccountId'],
                                  amount=Decimal(transaction_props['amount']),
                                  currency_id=transaction_props['currencyId'],
                                  date_time=transaction_props['dateTime'],
                                  is_income=transaction_props['isIncome'],
                                  is_transfer=transaction_props['isTransfer'],
                                  notes=transaction_props['notes'])
        if transaction_props['targetAmount'] is not None:
            transaction.target_amount = Decimal(transaction_props['targetAmount'])
        return transaction

    return _create_transaction


@pytest.fixture(scope="function")
def create_user():
    def _create_user(email, password='qqq_111_', first_name=None, last_name=None):
        user = {
            'email': email,
            'password': password,
        }
        if first_name:
            user['first_name'] = first_name
        if last_name:
            user['last_name'] = last_name

        user_schema = UserRegistration.model_validate(user)
        u = create_users_service(user_schema, db)
        u.is_active = True
        db.commit()

        return u

    return _create_user
