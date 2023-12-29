from pydantic import ConfigDict, BaseModel, EmailStr, Field


PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 15
password_field: str = Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)


class UserBase(BaseModel):
    id: int | None = None
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserRegistration(UserBase):
    first_name: str = ''
    last_name: str = ''
    password: str = password_field


class UserLoginSchema(UserBase):
    password: str = password_field


class UserResponse(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    model_config = ConfigDict(from_attributes=True)
