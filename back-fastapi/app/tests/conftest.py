from icecream import ic

from app.main import app
from app.database import get_db

from app.models.User import User
from app.models.Currency import Currency
from app.models.DefaultCategory import DefaultCategory
from app.models.UserCategory import UserCategory
from app.models.AccountType import AccountType

from app.tests.db_test_cfg import override_get_db

app.dependency_overrides[get_db] = override_get_db

db = next(override_get_db())


def pytest_unconfigure(config):
    db.query(User).delete()
    db.query(Currency).delete()
    db.query(AccountType).delete()
    db.query(UserCategory).delete()
    db.query(DefaultCategory).delete()
    db.commit()

    print("\n\n------- DB is cleared -------\n\n")
