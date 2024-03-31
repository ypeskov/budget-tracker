from icecream import ic
from sqlalchemy.orm import Session

from app.models.UserCategory import UserCategory
from app.schemas.category_schema import GroupedCategorySchema


def get_user_categories(user_id: int, db: Session) -> list[UserCategory]:
    return db.query(UserCategory).filter_by(user_id=user_id).all()


def grouped_user_categories(user_id: int, db: Session) -> GroupedCategorySchema:
    raw_categories: list[UserCategory] = db.query(UserCategory).filter_by(user_id=user_id).all()

    categories_dict: dict[int, UserCategory] = {}

    income_categories: list[dict] = []
    expense_categories: list[dict] = []

    for category in raw_categories:
        categories_dict[category.id] = category
        category.children = []

    for category in raw_categories:
        if category.parent_id:
            categories_dict[category.parent_id].children.append(category)
        else:
            if category.is_income:
                income_categories.append(category)
            else:
                expense_categories.append(category)

    def category_to_dict(category):
        return {
            "id": category.id,
            "name": category.name,
            "parentId": category.parent_id,
            "isIncome": category.is_income,
            "children": [category_to_dict(child) for child in category.children]
        }

    grouped_categories = {
        "income": [category_to_dict(category) for category in income_categories],
        "expenses": [category_to_dict(category) for category in expense_categories]
    }

    return GroupedCategorySchema(**grouped_categories)
