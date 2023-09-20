from .generate_users import clear_test_users


def clear_all_data():
    clear_test_users()
    print('All test data was deleted')


if __name__ == "__main__":
    clear_all_data()
