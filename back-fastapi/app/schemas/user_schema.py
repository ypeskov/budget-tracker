from pydantic import ConfigDict, BaseModel, EmailStr, Field
from pydantic.alias_generators import to_camel


PASSWORD_MIN_LENGTH = 3
PASSWORD_MAX_LENGTH = 15
password_field: str = Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)


class UserBase(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel)


class UserRegistration(UserBase):
    first_name: str = ''
    last_name: str = ''
    password: str = password_field


class UserLoginSchema(UserBase):
    password: str = password_field


class UserResponse(UserBase):
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
