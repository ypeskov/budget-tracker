import pytest
from datetime import date, timedelta
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.tests.conftest import db

client = TestClient(app)


class TestExchangeRatesAPI:
    
    def test_get_rates_success(self, auth_headers):
        response = client.get("/exchange-rates/", headers=auth_headers)
        
        assert response.status_code == 200
        rates = response.json()
        assert isinstance(rates, (dict, list))
        
        
    @patch('app.services.exchange_rates.update_exchange_rates')
    def test_update_rates_success(self, mock_update, auth_headers):
        # Mock successful update
        mock_update.return_value = {
            "id": 1,
            "rates": {"USD": 1.0, "EUR": 0.85},
            "date": "2024-01-01"
        }
        
        response = client.get("/exchange-rates/update/", headers=auth_headers)
        
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)
        
        
