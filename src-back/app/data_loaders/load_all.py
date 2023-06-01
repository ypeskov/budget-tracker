from .category_data_loader import load_default_categories
from .currency_data_loader import load_default_currencies


def load_all_data():
    load_default_categories()
    load_default_currencies()


if __name__ == "__main__":
    load_all_data()