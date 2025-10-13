from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel

PASSWORD_MIN_LENGTH = 3
PASSWORD_MAX_LENGTH = 50
password_field: str = Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)


class UserBase(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)


class UserRegistration(UserBase):
    id: int | None = None
    first_name: str = ''
    last_name: str = ''
    password: str = password_field

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)


class UserLoginSchema(UserBase):
    password: str = password_field


class UserResponse(UserBase):
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)
