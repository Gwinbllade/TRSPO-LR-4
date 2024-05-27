import requests

from fastapi import Request, HTTPException, Depends, status

from api.config import config
from api.domain import UserSchema


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token)):
    response = requests.get(
        url=config.user_api,
        cookies={
            "access_token": token,
        }
    )
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = UserSchema.model_validate_json(json_data=response.content)

    return user
