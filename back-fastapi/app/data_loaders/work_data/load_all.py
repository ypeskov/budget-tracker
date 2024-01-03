from icecream import ic
from sqlalchemy.orm import Session

from .category_data_loader import load_default_categories
from .currency_data_loader import load_default_currencies
from .account_type_data_loader import load_default_account_types


def load_all_data(db: Session | None = None):
    print('---- Loading default data ----')
    load_default_categories(db)
    load_default_currencies(db)
    load_default_account_types(db)
    print('---- Default data is loaded ----')


if __name__ == "__main__":  # pragma: no cover
    load_all_data()
