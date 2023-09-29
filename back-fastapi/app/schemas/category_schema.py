from datetime import datetime

from pydantic import ConfigDict, BaseModel


class CreateCategorySchema(BaseModel):
    name: str
    parent_id: int | None = None
    is_income: bool


class ResponseCategorySchema(CreateCategorySchema):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)
