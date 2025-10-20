"""
Basic tests for Planned Transactions API.

Note: These are minimal tests to verify the API structure.
Full test coverage should include:
- Recurring transaction generation
- Future balance calculations
- Balance projections
- Edge cases for recurrence rules
"""

from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models.Account import Account
from app.models.PlannedTransaction import PlannedTransaction
from app.models.Transaction import Transaction
from app.models.User import User
from app.tests.conftest import db, main_test_user_id

client = TestClient(app)

planned_transactions_path_prefix = '/planned-transactions'
financial_planning_path_prefix = '/financial-planning'


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    db.query(PlannedTransaction).delete()
    db.query(Transaction).delete()
    db.query(Account).delete()
    db.query(User).delete()
    db.commit()


def test_create_one_time_planned_transaction(token, one_account):
    """Test creating a one-time planned transaction"""
    planned_date = (datetime.now() + timedelta(days=7)).isoformat()

    planned_transaction_data = {
        'amount': 100.50,
        'label': 'Future expense',
        'notes': 'Planned payment',
        'isIncome': False,
        'plannedDate': planned_date,
        'isRecurring': False,
        'recurrenceRule': None,
    }

    response = client.post(
        f'{planned_transactions_path_prefix}/',
        json=planned_transaction_data,
        headers={'auth-token': token},
    )

    print(f"URL: {planned_transactions_path_prefix}/")
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data['amount'] == 100.50
    assert data['label'] == 'Future expense'
    assert data['isIncome'] is False
    assert data['isRecurring'] is False
    assert data['isExecuted'] is False
    assert data['isActive'] is True


def test_create_recurring_planned_transaction(token, one_account):
    """Test creating a recurring planned transaction"""
    planned_date = (datetime.now() + timedelta(days=1)).isoformat()
    end_date = (datetime.now() + timedelta(days=30)).isoformat()

    planned_transaction_data = {
        'amount': 50.00,
        'label': 'Monthly subscription',
        'notes': 'Recurring payment',
        'isIncome': False,
        'plannedDate': planned_date,
        'isRecurring': True,
        'recurrenceRule': {'frequency': 'monthly', 'interval': 1, 'endDate': end_date},
    }

    response = client.post(
        f'{planned_transactions_path_prefix}/',
        json=planned_transaction_data,
        headers={'auth-token': token},
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data['isRecurring'] is True
    assert data['recurrenceRule'] is not None
    assert data['recurrenceRule']['frequency'] == 'monthly'


def test_get_planned_transactions(token, one_account):
    """Test getting list of planned transactions"""
    # Create a few planned transactions first
    for i in range(3):
        planned_date = (datetime.now() + timedelta(days=i + 1)).isoformat()
        planned_transaction_data = {
            'amount': 100.0 * (i + 1),
            'label': f'Planned transaction {i + 1}',
            'notes': '',
            'isIncome': False,
            'plannedDate': planned_date,
            'isRecurring': False,
        }

        client.post(
            f'{planned_transactions_path_prefix}/',
            json=planned_transaction_data,
            headers={'auth-token': token},
        )

    # Get all planned transactions
    response = client.get(f'{planned_transactions_path_prefix}/', headers={'auth-token': token})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3


def test_update_planned_transaction(token, one_account):
    """Test updating a planned transaction"""
    # Create planned transaction
    planned_date = (datetime.now() + timedelta(days=5)).isoformat()
    planned_transaction_data = {
        'amount': 75.0,
        'label': 'Original label',
        'notes': '',
        'isIncome': False,
        'plannedDate': planned_date,
        'isRecurring': False,
    }

    create_response = client.post(
        f'{planned_transactions_path_prefix}/',
        json=planned_transaction_data,
        headers={'auth-token': token},
    )

    created_id = create_response.json()['id']

    # Update it
    update_data = {
        'id': created_id,
        'accountId': one_account['id'],
        'amount': 100.0,
        'categoryId': None,
        'label': 'Updated label',
        'notes': 'Updated notes',
        'isIncome': False,
        'plannedDate': planned_date,
        'isRecurring': False,
    }

    response = client.put(
        f'{planned_transactions_path_prefix}/{created_id}',
        json=update_data,
        headers={'auth-token': token},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['amount'] == 100.0
    assert data['label'] == 'Updated label'
    assert data['notes'] == 'Updated notes'


def test_delete_planned_transaction(token, one_account):
    """Test soft deleting a planned transaction"""
    # Create planned transaction
    planned_date = (datetime.now() + timedelta(days=5)).isoformat()
    planned_transaction_data = {
        'amount': 50.0,
        'label': 'To be deleted',
        'notes': '',
        'isIncome': False,
        'plannedDate': planned_date,
        'isRecurring': False,
    }

    create_response = client.post(
        f'{planned_transactions_path_prefix}/',
        json=planned_transaction_data,
        headers={'auth-token': token},
    )

    created_id = create_response.json()['id']

    # Delete it
    response = client.delete(
        f'{planned_transactions_path_prefix}/{created_id}',
        headers={'auth-token': token},
    )

    assert response.status_code == status.HTTP_200_OK

    # Verify it's not returned in list
    list_response = client.get(f'{planned_transactions_path_prefix}/', headers={'auth-token': token})

    data = list_response.json()
    assert created_id not in [pt['id'] for pt in data]


def test_calculate_future_balance(token, one_account):
    """Test future balance calculation"""
    # Create a planned transaction
    planned_date = (datetime.now() + timedelta(days=10)).isoformat()
    planned_transaction_data = {
        'amount': 500.0,
        'label': 'Future income',
        'notes': '',
        'isIncome': True,
        'plannedDate': planned_date,
        'isRecurring': False,
    }

    client.post(
        f'{planned_transactions_path_prefix}/',
        json=planned_transaction_data,
        headers={'auth-token': token},
    )

    # Calculate future balance
    target_date = (datetime.now() + timedelta(days=15)).isoformat()
    request_data = {
        'targetDate': target_date,
        'accountIds': None,
        'includeInactive': False,
    }

    response = client.post(
        f'{financial_planning_path_prefix}/future-balance',
        json=request_data,
        headers={'auth-token': token},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert 'totalCurrentBalance' in data
    assert 'totalProjectedBalance' in data
    assert 'totalPlannedIncome' in data
    assert 'totalPlannedExpenses' in data
    assert 'accounts' in data


# TODO: Add more comprehensive tests:
# - Test recurrence rule validation
# - Test occurrence generation for different frequencies
# - Test balance projection over time periods
# - Test filters (by account, date range, status)
# - Test error cases (invalid account, invalid dates, etc.)
