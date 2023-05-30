from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str

    class Config:
        orm_mode = True


class UserRegistration(UserBase):
    first_name: str
    last_name: str
    password: str


class UserLoginSchema(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(UserBase):
    first_name: str | None
    last_name: str | None
