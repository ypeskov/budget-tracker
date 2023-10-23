from fastapi.testclient import TestClient

from app.tests.conftest import categories_path_prefix
from app.main import app


import icecream
from icecream import ic
icecream.install()

client = TestClient(app)


def test_get_user_categories(token):
    response = client.get(f'{categories_path_prefix}/', headers={'auth-token': token})
    assert response.status_code == 200
    categories = response.json()
    assert type(categories) == list
    assert len(categories) > 0
