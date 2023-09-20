from icecream import ic

from app.database import get_db
from app.models.User import User


db = next(get_db())


def generate_test_users():
    default_values = [
        User(email='user1@example.com', first_name='Yura1', last_name='Peskov1', password='qqq'),
        User(email='user2@example.com', first_name='Yura2', last_name='Peskov2', password='qqq'),
        User(email='user3@example.com', first_name='Yura3', last_name='Peskov3', password='qqq'),
        User(email='user4@example.com', first_name='Yura4', last_name='Peskov4', password='qqq'),
    ]

    try:
        db.bulk_save_objects(default_values)
        db.commit()
        print('test users are uploaded into DB')
    except Exception as e:
        ic(e)
        ic(e.args)


if __name__ == '__main__':
    load_default_account_types()
