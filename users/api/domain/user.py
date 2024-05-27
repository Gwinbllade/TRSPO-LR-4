from pydantic import BaseModel, EmailStr

from api import enums


class UserSchema(BaseModel):
    id: int
    role: enums.UserRole
    username: str
    email: str

    class Config:
        from_attributes = True


class UserAuthSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    username: str | None = None
    password: str | None = None
