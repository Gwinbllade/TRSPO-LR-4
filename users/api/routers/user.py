from fastapi import APIRouter, HTTPException, Depends, Response, status, Request

from api.auth import get_password_hash, authenticate_user, create_access_token
from api.repository import user_repository
from api.dependencies import get_current_user
from api.models import User
from api.domain import UserSchema, UserAuthSchema, UserUpdateSchema, UserLoginSchema

from api import enums

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("")
async def get_users(current_user: User = Depends(get_current_user)) -> list[UserSchema]:
    if current_user.role == enums.UserRole.ADMIN:
        users = await user_repository.get_many()
        return users
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.get("/me")
async def get_info_user(current_user: User = Depends(get_current_user)) -> UserSchema:
    return current_user


@router.get("/{user_id}")
async def get_user(user_id: int, current_user: User = Depends(get_current_user)) -> UserSchema:
    if current_user.role == enums.UserRole.ADMIN:
        user = await user_repository.get(id=user_id)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.post("/auth/register")
async def register(user_data: UserAuthSchema = Depends()) -> str:
    print("\t\t->", user_data.email)
    existing_user = await user_repository.get(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    else:
        print(user_data.password, user_data.email)
        hashed_password = get_password_hash(user_data.password)
        await user_repository.save(User(
            email=user_data.email,
            hashed_password=hashed_password,
            username=user_data.username,
            role=enums.UserRole.BUYER,
        ))

        return "User created successfully"


@router.patch("")
async def update(user_data: UserUpdateSchema = Depends(), current_user: User = Depends(get_current_user)) -> str:
    print(current_user.id)
    user = await user_repository.get(id=current_user.id)

    update_data = user_data.model_dump(exclude_none=True)
    if password := update_data.get("password"):
        user.hashed_password = password
    if username := update_data.get("username"):
        user.username = username
    try:
        await user_repository.save(entity=user)
    except:
        raise HTTPException(status_code=500, detail="Failed to update user")
    else:
        return "User updated successfully"


@router.post("/auth/login")
async def login_user(response: Response, user_date: UserLoginSchema = Depends()):
    user = await authenticate_user(user_date.email, user_date.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return "Successfully login"


@router.post("/auth/logout")
async def logout(request: Request, response: Response):
    if "access_token" in request.cookies:
        response.delete_cookie("access_token")
        return {"message": "User logout"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

