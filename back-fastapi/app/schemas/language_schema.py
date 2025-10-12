from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class LanguageSchema(BaseModel):
    id: int
    name: str
    code: str
    is_deleted: bool

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )
