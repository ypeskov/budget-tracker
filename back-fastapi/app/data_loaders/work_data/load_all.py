from icecream import ic
from sqlalchemy.orm import Session

from .category_data_loader import load_default_categories
from .currency_data_loader import load_default_currencies
from .account_type_data_loader import load_default_account_types


def load_all_data(db: Session = None):
    load_default_categories(db)
    load_default_currencies(db)
    load_default_account_types(db)
    pass


if __name__ == "__main__":
    load_all_data()
