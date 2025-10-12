from .generate_accounts import generate_test_accounts
from .generate_transactions import generate_test_transactions
from .generate_users import generate_test_users


def generate_all_data():
    generate_test_users()
    generate_test_accounts()
    generate_test_transactions()


if __name__ == "__main__":
    generate_all_data()
