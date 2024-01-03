from pydantic import ConfigDict, BaseModel


class AccountTypeResponseSchema(BaseModel):
    id: int
    type_name: str
    is_credit: bool
    model_config = ConfigDict(from_attributes=True)
