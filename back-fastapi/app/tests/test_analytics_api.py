from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAnalyticsAPI:
    @pytest.fixture
    def mock_analyzer(self):
        with patch('app.routes.analytics.ExpenseAnalyzer') as mock:
            analyzer_instance = AsyncMock()
            mock.return_value = analyzer_instance
            yield analyzer_instance

    def test_spending_trends_success(self, mock_analyzer, auth_headers):
        mock_analyzer.analyze_spending_trends.return_value = (
            "Анализ трендов расходов: ваши основные расходы..."
        )

        response = client.post(
            "/analytics/spending-trends/",
            json={"startDate": "2024-01-01", "endDate": "2024-01-31", "limit": 50},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "анализ трендов расходов" in data["analysis"].lower()

    def test_spending_trends_no_data(self, mock_analyzer, auth_headers):
        mock_analyzer.analyze_spending_trends.return_value = None

        response = client.post(
            "/analytics/spending-trends/",
            json={"startDate": "2024-01-01", "endDate": "2024-01-31"},
            headers=auth_headers,
        )

        assert response.status_code == 500

    def test_expense_categorization_success(self, mock_analyzer, auth_headers):
        mock_analyzer.analyze_expense_categorization.return_value = (
            "Анализ категоризации: категории настроены корректно..."
        )

        response = client.post(
            "/analytics/expense-categorization/",
            json={"startDate": "2024-01-01", "endDate": "2024-01-31"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "категори" in data["analysis"].lower()

    def test_invalid_date_range(self, auth_headers):
        response = client.post(
            "/analytics/spending-trends/",
            json={
                "startDate": "2024-01-31",
                "endDate": "2024-01-01",  # End date before start date
            },
            headers=auth_headers,
        )

        # Should still pass validation, but might return empty analysis
        assert response.status_code in [200, 503, 500]

    def test_unauthorized_access(self):
        response = client.post(
            "/analytics/spending-trends/",
            json={"startDate": "2024-01-01", "endDate": "2024-01-31"},
            # No auth headers
        )

        assert response.status_code == 401

    def test_exception_handling(self, mock_analyzer, auth_headers):
        mock_analyzer.analyze_spending_trends.side_effect = Exception(
            "OpenAI API Error"
        )

        response = client.post(
            "/analytics/spending-trends/",
            json={"startDate": "2024-01-01", "endDate": "2024-01-31"},
            headers=auth_headers,
        )

        assert response.status_code == 500
