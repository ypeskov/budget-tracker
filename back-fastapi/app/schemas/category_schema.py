from datetime import datetime

from pydantic import BaseModel


class CreateCategorySchema(BaseModel):
    name: str
    parent_id: int | None
    is_income: bool


class ResponseCategorySchema(CreateCategorySchema):
    id: int
    user_id: int

    class Config:
        orm_mode = True
