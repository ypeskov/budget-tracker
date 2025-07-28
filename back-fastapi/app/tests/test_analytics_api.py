import pytest
from datetime import date, timedelta
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.services.analytics.expense_analyzer import ExpenseAnalyzer


client = TestClient(app)


class TestAnalyticsAPI:
    
    @pytest.fixture
    def mock_analyzer(self):
        with patch('app.routes.analytics.ExpenseAnalyzer') as mock:
            analyzer_instance = AsyncMock()
            mock.return_value = analyzer_instance
            yield analyzer_instance
    
    def test_spending_trends_success(self, mock_analyzer, auth_headers):
        mock_analyzer.analyze_spending_trends.return_value = "Анализ трендов расходов: ваши основные расходы..."
        
        response = client.post(
            "/analytics/spending-trends/",
            json={
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
                "limit": 50
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "анализ трендов расходов" in data["analysis"].lower()
        
    def test_spending_trends_no_data(self, mock_analyzer, auth_headers):
        mock_analyzer.analyze_spending_trends.return_value = None
        
        response = client.post(
            "/analytics/spending-trends/",
            json={
                "startDate": "2024-01-01",
                "endDate": "2024-01-31"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 503
        assert "временно недоступен" in response.json()["detail"]
        
    def test_budget_recommendations_success(self, mock_analyzer, auth_headers):
        mock_analyzer.get_budget_recommendations.return_value = "Рекомендации по бюджету: рекомендуем сократить расходы..."
        
        response = client.post(
            "/analytics/budget-recommendations/",
            json={
                "startDate": "2024-01-01",
                "endDate": "2024-01-31"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "рекомендации" in data["analysis"].lower()
        
    def test_expense_categorization_success(self, mock_analyzer, auth_headers):
        mock_analyzer.analyze_expense_categorization.return_value = "Анализ категоризации: категории настроены корректно..."
        
        response = client.post(
            "/analytics/expense-categorization/",
            json={
                "startDate": "2024-01-01",
                "endDate": "2024-01-31"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "категори" in data["analysis"].lower()
        
    def test_financial_insights_success(self, mock_analyzer, auth_headers):
        mock_analyzer.get_financial_insights.return_value = "Финансовые инсайты: ваши основные финансовые привычки..."
        
        response = client.post(
            "/analytics/financial-insights/",
            json={
                "startDate": "2024-01-01",
                "endDate": "2024-01-31"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "финансов" in data["analysis"].lower()
        
    def test_monthly_summary_success(self, mock_analyzer, auth_headers):
        mock_analyzer.get_monthly_summary.return_value = "Месячное резюме: в январе вы потратили 50000 рублей..."
        
        response = client.post(
            "/analytics/monthly-summary/",
            json={
                "monthDate": "2024-01-15"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "январе" in data["analysis"].lower()
        
    def test_invalid_date_range(self, auth_headers):
        response = client.post(
            "/analytics/spending-trends/",
            json={
                "startDate": "2024-01-31",
                "endDate": "2024-01-01"  # End date before start date
            },
            headers=auth_headers
        )
        
        # Should still pass validation, but might return empty analysis
        assert response.status_code in [200, 503, 500]
        
    def test_invalid_limit_values(self, auth_headers):
        # Test limit too low
        response = client.post(
            "/analytics/spending-trends/",
            json={
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
                "limit": 5  # Below minimum of 10
            },
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error
        
        # Test limit too high
        response = client.post(
            "/analytics/spending-trends/",
            json={
                "startDate": "2024-01-01",
                "endDate": "2024-01-31", 
                "limit": 300  # Above maximum of 200
            },
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error
        
    def test_unauthorized_access(self):
        response = client.post(
            "/analytics/spending-trends/",
            json={
                "startDate": "2024-01-01",
                "endDate": "2024-01-31"
            }
            # No auth headers
        )
        
        assert response.status_code == 401
        
    def test_exception_handling(self, mock_analyzer, auth_headers):
        mock_analyzer.analyze_spending_trends.side_effect = Exception("OpenAI API Error")
        
        response = client.post(
            "/analytics/spending-trends/",
            json={
                "startDate": "2024-01-01",
                "endDate": "2024-01-31"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 500
        assert "ошибка" in response.json()["detail"].lower()