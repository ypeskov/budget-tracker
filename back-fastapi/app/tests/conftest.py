from icecream import ic

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from app.schemas.account_schema import CreateAccountSchema
from app.tests.db_test_cfg import override_get_db
from app.data_loaders.work_data.load_all import load_all_data
from app.models.User import User
from app.models.Currency import Currency
from app.models.DefaultCategory import DefaultCategory
from app.models.UserCategory import UserCategory
from app.models.AccountType import AccountType
from app.models.Account import Account

from app.tests.data.auth_data import test_users, main_test_user
from app.tests.data.accounts_data import test_accounts

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
    db.commit()

    print("\n\n------- DB is cleared -------\n\n")


@pytest.fixture(scope="function")
def token():
    """ Create a user for test purposes and return his access token """
    client.post(f'{auth_path_prefix}/register/', json=main_test_user)
    response = client.post(f'{auth_path_prefix}/login/', json=main_test_user)
    assert response.status_code == 200
    user = response.json()

    yield user["access_token"]
    db.query(User).filter(User.id == main_test_user_id).delete()
    db.commit()


@pytest.fixture(scope="function")
def one_account(token, acc_id=1):
    account_details = test_accounts[0]
    account_details['id'] = acc_id

    acc_response = client.post(f'{accounts_path_prefix}/', json=account_details, headers={'auth-token': token})
    acc = acc_response.json()
    yield acc
    db.query(Account).filter(Account.id == acc['id']).delete()
    db.commit()


@pytest.fixture(scope="function")
def fake_account():
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
def create_accounts(token):
    accounts = []
    for test_account in test_accounts:
        accounts.append(client.post(f'{accounts_path_prefix}/', json=test_account, headers={'auth-token': token}).json())
    yield accounts
    db.query(Account).filter_by(user_id=main_test_user_id).delete()
    db.commit()
