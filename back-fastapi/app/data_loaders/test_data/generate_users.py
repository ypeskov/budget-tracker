from collections import namedtuple

from icecream import ic

from app.database import get_db
from app.models.User import User
from app.services.auth import create_users


db = next(get_db())


UserModel = namedtuple('UserModel', 'email first_name last_name password')
default_values = [
    UserModel(email='user1@example.com', first_name='Yura1', last_name='Peskov1', password='qqq'),
    UserModel(email='user2@example.com', first_name='Yura2', last_name='Peskov2', password='qqq'),
    UserModel(email='user3@example.com', first_name='Yura3', last_name='Peskov3', password='qqq'),
    UserModel(email='user4@example.com', first_name='Yura4', last_name='Peskov4', password='qqq'),
]


def generate_test_users():
    try:
        for user in default_values:
            create_users(user, db)
            print(f'{user.first_name} is created')

        print('All test users are uploaded into DB')
    except Exception as e:
        ic(e)


def clear_test_users():
    try:
        users = db.query(User).all()
        for u in users:
            db.delete(u)
        db.commit()
    except Exception as e:
        ic(e)


if __name__ == '__main__':
    generate_test_users()
