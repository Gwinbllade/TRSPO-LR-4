from pydantic import BaseModel, EmailStr

from api import enums


class UserSchema(BaseModel):
    id: int
    role: enums.UserRole
    username: str
    email: str

    class Config:
        from_attributes = True
