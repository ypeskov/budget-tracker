from icecream import ic

from app.main import app
from app.database import get_db
from app.data_loaders.work_data.load_all import load_all_data

from app.models.User import User
from app.models.Currency import Currency
from app.models.DefaultCategory import DefaultCategory
from app.models.UserCategory import UserCategory
from app.models.AccountType import AccountType

from app.tests.db_test_cfg import override_get_db

app.dependency_overrides[get_db] = override_get_db

db = next(override_get_db())
load_all_data(db)

def pytest_unconfigure(config):
    db.query(User).delete()
    db.query(Currency).delete()
    db.query(AccountType).delete()
    db.query(UserCategory).delete()
    db.query(DefaultCategory).delete()
    db.commit()

    print("\n\n------- DB is cleared -------\n\n")
