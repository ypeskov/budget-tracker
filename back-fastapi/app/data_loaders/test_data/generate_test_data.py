from .generate_users import generate_test_users
from .generate_accounts import generate_test_accounts


def generate_all_data():
    generate_test_users()
    generate_test_accounts()


if __name__ == "__main__":
    generate_all_data()
