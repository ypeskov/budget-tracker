from datetime import date, datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.tests.conftest import db, main_test_user_id

client = TestClient(app)


class TestReportsAPI:
    def test_cash_flow_report_invalid_dates(self, auth_headers):
        report_data = {
            "startDate": "invalid-date",
            "endDate": "2024-01-31",
            "period": "MONTHLY",
        }

        response = client.post(
            "/reports/cashflow/", json=report_data, headers=auth_headers
        )
        assert response.status_code == 422

    def test_balance_report_success(self, token, auth_headers, one_account):
        report_data = {"accountIds": [one_account["id"]], "balanceDate": "2024-01-31"}

        response = client.post(
            "/reports/balance/", json=report_data, headers=auth_headers
        )

        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)

    def test_balance_report_non_hidden_success(self, token, auth_headers, one_account):
        report_data = {"accountIds": [one_account["id"]], "balanceDate": "2024-01-31"}

        response = client.post(
            "/reports/balance/non-hidden/", json=report_data, headers=auth_headers
        )

        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)

    def test_expenses_data_success(self, token, auth_headers):
        report_data = {
            "startDate": "2024-01-01",
            "endDate": "2024-01-31",
            "hideEmptyCategories": True,
        }

        response = client.post(
            "/reports/expenses-data/", json=report_data, headers=auth_headers
        )

        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, (list, dict))
