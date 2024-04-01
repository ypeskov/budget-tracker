from fastapi import APIRouter, Depends, Request, HTTPException, Body
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.models.UserCategory import UserCategory
from app.schemas.category_schema import ResponseCategorySchema, GroupedCategorySchema, CategoryCreateUpdateSchema
from app.services.categories import get_user_categories, grouped_user_categories, create_or_update_category, \
    delete_category

router = APIRouter(
    tags=['Categories'],
    prefix='/categories',
    dependencies=[Depends(check_token)]
)


@router.get('/', response_model=list[ResponseCategorySchema])
def get_categories(request: Request, db: Session = Depends(get_db)) -> list[UserCategory]:
    return get_user_categories(request.state.user['id'], db)


@router.get('/grouped/', response_model=GroupedCategorySchema)
def get_grouped_categories(request: Request, db: Session = Depends(get_db)) -> GroupedCategorySchema:
    user_id = request.state.user['id']
    return grouped_user_categories(user_id, db)


@router.put('/{category_id}/', response_model=ResponseCategorySchema)
def update_category(category_id: int,
                    request: Request,
                    category_data: CategoryCreateUpdateSchema = Body(...),
                    db: Session = Depends(get_db)) -> UserCategory:
    try:
        user_id = request.state.user['id']
        updated_category = create_or_update_category(user_id, db, category_data, )
        return updated_category
    except Exception as e:
        logger.error(f"Error updating category: {e}")
        raise HTTPException(status_code=400, detail="Error updating category")


@router.post('/', response_model=ResponseCategorySchema, status_code=201)
def create_category(request: Request,
                    category_data: CategoryCreateUpdateSchema = Body(...),
                    db: Session = Depends(get_db)) -> ResponseCategorySchema:
    user_id = request.state.user['id']
    try:
        new_category = create_or_update_category(user_id=user_id, db=db, category_data=category_data)
        return new_category
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(status_code=400, detail=f"Error creating category: {e}")


@router.delete('/{category_id}/', status_code=200, response_model=ResponseCategorySchema)
def delete_category_endpoint(category_id: int, request: Request, db: Session = Depends(get_db)) -> UserCategory:
    user_id = request.state.user['id']
    try:
        return delete_category(user_id, category_id, db)
    except Exception as e:
        logger.error(f"Error deleting category: {e}")
        raise HTTPException(status_code=400, detail="Error deleting category")

