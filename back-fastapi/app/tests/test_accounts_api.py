import pytest
from fastapi import status
from fastapi.testclient import TestClient
from icecream import ic

from app.main import app
from app.models.Account import Account
from app.models.User import User
from app.schemas.account_schema import CreateAccountSchema
from app.services.accounts import create_account, get_account_details
from app.services.errors import (
    AccessDenied,
    InvalidAccount,
    InvalidAccountType,
    InvalidCurrency,
    InvalidUser,
    NotFoundError,
)
from app.tests.conftest import (
    accounts_path_prefix,
    auth_path_prefix,
    db,
    main_test_user_id,
    truly_invalid_account_id,
    truly_invalid_account_type_id,
    truly_invalid_currency_id,
)
from app.tests.data.accounts_data import test_account_types, test_accounts_data
from app.tests.data.auth_data import test_users

client = TestClient(app)


def test_invalid_token_add_account():
    response = client.post(
        f'{accounts_path_prefix}/', json={}, headers={'auth-token': 'Invalid token'}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_wrong_account_details(token):
    response = client.post(
        f'{accounts_path_prefix}/', json={}, headers={'auth-token': token}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_wrong_user_request(fake_account):
    with pytest.raises(InvalidUser):
        create_account(fake_account, truly_invalid_account_id, db)


def test_create_acc_with_invalid_currency(fake_account, token):
    fake_account.currency_id = truly_invalid_currency_id
    with pytest.raises(InvalidCurrency):
        create_account(fake_account, main_test_user_id, db)


def test_create_acc_with_invalid_type(fake_account, token):
    fake_account.account_type_id = truly_invalid_account_type_id
    with pytest.raises(InvalidAccountType):
        create_account(fake_account, main_test_user_id, db)


def test_access_denied_to_other_user_account(token):
    other_user = client.post(f'{auth_path_prefix}/register/', json=test_users[0])
    assert other_user.status_code == status.HTTP_200_OK
    other_account_details = {**test_accounts_data[0]}
    del other_account_details['id']

    other_user_account = create_account(
        CreateAccountSchema.model_validate(other_account_details),
        other_user.json()['id'],
        db,
    )
    assert other_user_account is not None

    with pytest.raises(AccessDenied):
        get_account_details(other_user_account.id, main_test_user_id, db)

    db.query(Account).filter_by(id=other_user_account.id).delete()
    db.query(User).filter_by(id=other_user.json()['id']).delete()
    db.commit()


def test_get_invalid_account_details():
    with pytest.raises(NotFoundError):
        get_account_details(truly_invalid_account_id, main_test_user_id, db)


@pytest.mark.parametrize("test_account", test_accounts_data)
def test_add_get_account(test_account, token):
    response_account = client.post(
        f'{accounts_path_prefix}/', json=test_account, headers={'auth-token': token}
    )
    assert response_account.status_code == status.HTTP_200_OK

    account_details = response_account.json()
    assert 'id' in account_details
    assert account_details['name'] == test_account['name']
    assert account_details['currencyId'] == test_account['currencyId']
    assert account_details['accountTypeId'] == test_account['accountTypeId']
    assert account_details['balance'] == test_account['balance']
    assert 'openingDate' in account_details
    assert account_details['openingDate'] is not None

    response = client.get(
        f'{accounts_path_prefix}/{account_details["id"]}', headers={'auth-token': token}
    )
    assert response.status_code == status.HTTP_200_OK
    account_details = response.json()
    assert 'id' in account_details
    assert account_details['name'] == test_account['name']
    assert account_details['currencyId'] == test_account['currencyId']
    assert account_details['accountTypeId'] == test_account['accountTypeId']
    assert account_details['balance'] == test_account['balance']
    assert 'openingDate' in account_details
    assert account_details['openingDate'] is not None

    # delete account after test
    db.query(Account).filter_by(id=account_details['id']).delete()
    db.commit()


def test_get_accounts_list(token, create_accounts):
    response = client.get(
        f'{accounts_path_prefix}/?includeHidden=false', headers={'auth-token': token}
    )
    assert response.status_code == status.HTTP_200_OK
    accounts_list = response.json()

    # check if all accounts are in response
    number_of_accounts = len(test_accounts_data)
    assert len(accounts_list) == number_of_accounts

    # check first account details in response
    assert accounts_list[0]['name'] == test_accounts_data[0]['name']
    assert accounts_list[0]['currencyId'] == test_accounts_data[0]['currencyId']
    assert accounts_list[0]['accountTypeId'] == test_accounts_data[0]['accountTypeId']
    assert accounts_list[0]['balance'] == test_accounts_data[0]['balance']
    assert 'openingDate' in accounts_list[0]
    assert accounts_list[0]['openingDate'] is not None

    # check last account details in response
    assert (
        accounts_list[number_of_accounts - 1]['name']
        == test_accounts_data[number_of_accounts - 1]['name']
    )
    assert (
        accounts_list[number_of_accounts - 1]['currencyId']
        == test_accounts_data[number_of_accounts - 1]['currencyId']
    )
    assert (
        accounts_list[number_of_accounts - 1]['accountTypeId']
        == test_accounts_data[number_of_accounts - 1]['accountTypeId']
    )
    assert (
        accounts_list[number_of_accounts - 1]['balance']
        == test_accounts_data[number_of_accounts - 1]['balance']
    )
    assert 'openingDate' in accounts_list[number_of_accounts - 1]
    assert accounts_list[number_of_accounts - 1]['openingDate'] is not None


def test_all_account_types_exist(token):
    response = client.get(
        f'{accounts_path_prefix}/types/', headers={'auth-token': token}
    )
    assert response.status_code == status.HTTP_200_OK
    account_types = response.json()

    assert len(account_types) == len(test_account_types)

    i = 0
    for test_account_type in test_account_types:
        assert test_account_type['name'] == test_account_types[i]['name']
        assert test_account_type['id'] == test_account_types[i]['id']
        assert test_account_type['is_credit'] == test_account_types[i]['is_credit']
        i += 1


def test_update_account(token, one_account):
    account = one_account
    account['name'] = 'Updated account'
    account['initialBalance'] = 100_999
    account['balance'] = 100_999
    account['comment'] = 'Updated comment'
    account['openingDate'] = '2023-12-28T23:00:00Z'

    response = client.put(
        f'{accounts_path_prefix}/{account["id"]}',
        json=account,
        headers={'auth-token': token},
    )
    assert response.status_code == status.HTTP_200_OK

    updated_account = response.json()
    assert updated_account['accountTypeId'] == account['account_type_id']
    assert updated_account['name'] == account['name']
    assert updated_account['balance'] == account['balance']
    assert updated_account['initialBalance'] == account['initialBalance']
    assert updated_account['comment'] == account['comment']
    assert updated_account['openingDate'] == account['openingDate']

    # delete account after test
    db.delete(db.query(Account).filter_by(id=account['id']).first())
    db.commit()


def test_update_invalid_account(token, one_account):
    account = one_account
    account['name'] = 'Updated account'
    account['initialBalance'] = 100_999
    account['balance'] = 100_999
    account['comment'] = 'Updated comment'
    account['openingDate'] = '2023-12-28T23:00:00Z'

    response = client.put(
        f'{accounts_path_prefix}/{truly_invalid_account_id}',
        json=account,
        headers={'auth-token': token},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
