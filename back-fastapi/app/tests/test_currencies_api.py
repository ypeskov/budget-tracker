from fastapi.testclient import TestClient

from app.main import app
from app.tests.conftest import currencies_path_prefix

import icecream
from icecream import ic
icecream.install()

client = TestClient(app)


def test_all_currencies_api(token):
    response = client.get(f'{currencies_path_prefix}/', headers={'auth-token': token})
    assert response.status_code == 200
    currencies = response.json()
    assert type(currencies) == list
    assert len(currencies) > 0
    assert 'id' in currencies[0]
    assert 'name' in currencies[0]
    assert 'code' in currencies[0]
