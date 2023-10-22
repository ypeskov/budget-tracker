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
main_test_user_id = 1000
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


@pytest.fixture(scope="session")
def token():
    client.post(f'{auth_path_prefix}/register/', json=main_test_user)
    response = client.post(f'{auth_path_prefix}/login/', json=main_test_user)
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def fake_account():
    return CreateAccountSchema.model_validate({
        'name': 'Fake account',
        'currency_id': 1,
        'account_type_id': 1,
        'balance': 0,
        'opening_date': None,
        'is_hidden': False,
        'comment': None
    })


@pytest.fixture(scope="function")
def create_accounts(token):
    for test_account in test_accounts:
        client.post(f'{accounts_path_prefix}/', json=test_account, headers={'auth-token': token})
    yield
    db.query(Account).delete()
    db.commit()
