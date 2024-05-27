from datetime import datetime, timedelta

from jose import jwt

from passlib.context import CryptContext
from pydantic import EmailStr

from api.config import config
from api.repository import user_repository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except:
        return False


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.secret_key, config.hash_algorithm
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await user_repository.get(email=email)
    if not (user and verify_password(password, user.hashed_password)):
        return None
    return user
