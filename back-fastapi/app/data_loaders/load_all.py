from .category_data_loader import load_default_categories
from .currency_data_loader import load_default_currencies
from .account_type_data_loader import load_default_account_types


def load_all_data():
    load_default_categories()
    load_default_currencies()
    load_default_account_types()


if __name__ == "__main__":
    load_all_data()
