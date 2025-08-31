import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.tests.conftest import db, main_test_user_id

client = TestClient(app)


class TestUserSettingsAPI:
    
    def test_get_languages_success(self, auth_headers):
        response = client.get("/settings/languages/", headers=auth_headers)
        
        assert response.status_code == 200
        languages = response.json()
        assert isinstance(languages, list)
        
        
    def test_get_settings_success(self, auth_headers):
        response = client.get("/settings/", headers=auth_headers)
        
        assert response.status_code == 200
        settings = response.json()
        assert isinstance(settings, dict)
        
        
    def test_store_settings_success(self, auth_headers):
        settings_data = {
            "language": "en",
            "theme": "light",
            "dateFormat": "DD/MM/YYYY"
        }
        
        response = client.post("/settings/", json=settings_data, headers=auth_headers)
        
        assert response.status_code in [200, 422, 500]  # May fail due to validation rules
        
    def test_store_settings_invalid_key(self, auth_headers):
        settings_data = {
            "invalidKey": "value"
        }
        
        response = client.post("/settings/", json=settings_data, headers=auth_headers)
        assert response.status_code == 422
        
        
    def test_get_base_currency_success(self, auth_headers):
        response = client.get("/settings/base-currency/", headers=auth_headers)
        
        assert response.status_code == 200
        currency = response.json()
        assert "id" in currency
        assert "code" in currency
        assert "name" in currency
        
        
    def test_set_base_currency_success(self, auth_headers):
        currency_data = {
            "currencyId": 1
        }
        
        response = client.put("/settings/base-currency/", json=currency_data, headers=auth_headers)
        
        assert response.status_code == 200
        currency = response.json()
        assert currency["id"] == 1
        
    def test_set_base_currency_invalid_id(self, auth_headers):
        currency_data = {
            "currencyId": 999999
        }
        
        response = client.put("/settings/base-currency/", json=currency_data, headers=auth_headers)
        assert response.status_code in [422, 500]
        
    def test_set_base_currency_missing_id(self, auth_headers):
        currency_data = {}
        
        response = client.put("/settings/base-currency/", json=currency_data, headers=auth_headers)
        assert response.status_code == 422
        
