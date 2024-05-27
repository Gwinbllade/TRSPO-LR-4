from datetime import datetime

from fastapi import Request, HTTPException, Depends, status
from jose import JWTError, jwt

from api.config import config
from api.repository import user_repository


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token)):
    global payload

    try:
        payload = jwt.decode(token, config.secret_key, config.hash_algorithm)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    expire: str = payload.get("exp")  # This line raises the 'NameError' because 'payload' is not defined
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await user_repository.get(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
