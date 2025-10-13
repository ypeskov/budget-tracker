from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CreateCategorySchema(BaseModel):
    name: str
    parent_id: int | None = None
    is_income: bool


class ResponseCategorySchema(CreateCategorySchema):
    id: int
    user_id: int
    name: str
    parent_id: int | None = None
    is_income: bool
    created_at: datetime
    updated_at: datetime
    children: list["ResponseCategorySchema"] | None = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)


ResponseCategorySchema.model_rebuild()


class GroupedCategorySchema(BaseModel):
    income: list[dict]
    expenses: list[dict]
    model_config = ConfigDict(alias_generator=to_camel)


class CategoryCreateUpdateSchema(BaseModel):
    id: int | None = None
    name: str
    parent_id: int | None = None
    is_income: bool

    model_config = ConfigDict(alias_generator=to_camel)
