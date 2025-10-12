from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )
