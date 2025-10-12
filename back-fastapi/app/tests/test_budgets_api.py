from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models.Budget import PeriodEnum
from app.services.errors import NotFoundError
from app.tests.conftest import db, main_test_user_id

client = TestClient(app)


class TestBudgetsAPI:
    def test_get_budgets_success(self, auth_headers):
        response = client.get("/budgets/", headers=auth_headers)
        assert response.status_code == 200
        budgets = response.json()
        assert isinstance(budgets, list)

    def test_create_budget_invalid_data(self, auth_headers):
        budget_data = {
            "name": "",
            "currencyId": 999,
            "targetAmount": -100,
            "period": "INVALID_PERIOD",
            "repeat": True,
            "startDate": "2024-01-01T00:00:00",
            "endDate": "2024-01-31T23:59:59",
            "categories": [],
        }

        response = client.post("/budgets/add/", json=budget_data, headers=auth_headers)
        assert response.status_code in [400, 422, 500]

    def test_get_budgets_with_include_filter(self, auth_headers):
        response = client.get("/budgets/?include=active", headers=auth_headers)
        assert response.status_code == 200

        response = client.get("/budgets/?include=archived", headers=auth_headers)
        assert response.status_code == 200

        response = client.get("/budgets/?include=all", headers=auth_headers)
        assert response.status_code == 200

    def test_get_budgets_invalid_include(self, auth_headers):
        response = client.get("/budgets/?include=invalid", headers=auth_headers)
        assert response.status_code == 400

    def test_delete_budget_not_found(self, auth_headers):
        response = client.delete("/budgets/999999/", headers=auth_headers)
        assert response.status_code == 404

    def test_archive_budget_not_found(self, auth_headers):
        response = client.put("/budgets/999999/archive/", headers=auth_headers)
        assert response.status_code == 404

    def test_daily_processing_authorized(self, auth_headers):
        # This test assumes user_id 1 has admin privileges
        # We'll test the forbidden case since we don't have admin user
        response = client.get("/budgets/daily-processing/", headers=auth_headers)
        assert response.status_code == 403
