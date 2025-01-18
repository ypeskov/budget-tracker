from pydantic import ConfigDict, BaseModel, PlainSerializer
from pydantic.alias_generators import to_camel


class OAuthToken(BaseModel):
    credential: str

    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True,
                              alias_generator=to_camel)