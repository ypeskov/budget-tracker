from collections import namedtuple

from sqlalchemy import text
from icecream import ic

from app.database import get_db
from app.models.User import User
from app.models.UserCategory import UserCategory
from app.services.auth import create_users


db = next(get_db())


UserModel = namedtuple('UserModel', 'id email first_name last_name password')
default_values = [
    UserModel(id=1, email='user1@example.com', first_name='Yura1', last_name='Peskov1', password='qqq'),
    UserModel(id=2, email='user2@example.com', first_name='Yura2', last_name='Peskov2', password='qqq'),
]


def generate_test_users():
    # set autoincrement for categories to 1
    sql_query = text(f"ALTER SEQUENCE user_categories_id_seq RESTART WITH 1;")
    db.execute(sql_query)

    try:
        for user in default_values:
            create_users(user, db)
            print(f'{user.first_name} is created')

        print('All test users were generated')
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
