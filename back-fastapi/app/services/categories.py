from sqlalchemy.orm import Session

from icecream import ic

from app.logger_config import logger
from app.models.UserCategory import UserCategory
from app.schemas.category_schema import GroupedCategorySchema, CategoryCreateUpdateSchema

ic.configureOutput(includeContext=True)


def get_user_categories(user_id: int, db: Session, include_deleted: bool = False) -> list[UserCategory]:
    query = db.query(UserCategory).filter_by(user_id=user_id)

    if not include_deleted:
        query = query.filter(UserCategory.is_deleted == False)

    categories = query.order_by(UserCategory.is_income, UserCategory.name).all()

    def add_children(category: UserCategory, result_list: list, parent_name: str = None):
        if parent_name:
            category_display_name = f"{parent_name} >> {category.name}"
        else:
            category_display_name = category.name

        prefix = "+" if category.is_income else "-"
        category.name = f"({prefix}) {category_display_name}"

        result_list.append(category)

        children = [cat for cat in categories if cat.parent_id == category.id]
        for child in sorted(children, key=lambda x: x.name):
            add_children(child, result_list, category_display_name)

    result = []
    for category in categories:
        if category.parent_id is None:
            add_children(category, result)

    return result


def grouped_user_categories(user_id: int, db: Session, include_deleted: bool = False) -> GroupedCategorySchema:
    query = db.query(UserCategory).filter(UserCategory.user_id == user_id)

    if not include_deleted:
        query = query.filter(UserCategory.is_deleted == False).order_by(UserCategory.name)

    raw_categories: list[UserCategory] = query.all()

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


def create_or_update_category(user_id: int, db: Session, category_data: CategoryCreateUpdateSchema) -> UserCategory:
    if category_data.id:
        try:
            category: UserCategory = db.query(UserCategory).filter(UserCategory.id == category_data.id,
                                                                   UserCategory.user_id == user_id).one()
            for key, value in category_data.dict().items():
                setattr(category, key, value)

            db.commit()
            db.refresh(category)
        except Exception as e:
            logger.error(f"Error updating category: {e}")
            raise e
    else:
        category = UserCategory(**category_data.dict(), user_id=user_id)
        db.add(category)
        db.commit()
        db.refresh(category)

    return category


def delete_category(user_id: int,  category_id: int, db: Session) -> UserCategory:
    try:
        category: UserCategory = db.query(UserCategory).filter(UserCategory.id == category_id,
                                                               UserCategory.user_id == user_id).one()
        category.is_deleted = True
        db.commit()
    except Exception as e:
        logger.error(f"Error deleting category: {e}")
        raise e

    return category
