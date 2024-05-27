from typing import List

from fastapi import APIRouter, HTTPException, Depends, status

from api.repository import category_repository
from api.dependencies import get_current_user
from api.models import Category
from api.domain import CategoryUpdateScheme, CategoryScheme, CategoryAddScheme, UserSchema
from api import enums

router = APIRouter(
    prefix="/categories",
    tags=['Categories']
)


@router.get("")
async def get_categories() -> list[CategoryScheme]:
    return await category_repository.get_many()


@router.get("/{category_id}")
async def get_category(category_id: int) -> CategoryScheme:
    category = await category_repository.get(id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("")
async def add(args: CategoryAddScheme = Depends(), current_user: UserSchema = Depends(get_current_user)) -> CategoryAddScheme:
    if current_user.role == enums.UserRole.ADMIN:
        try:
            new_category = Category(name=args.name)
            await category_repository.save(entity=Category(name=args.name))
            return new_category
        except:
            raise HTTPException(400, detail="Category not added. Check the parameters ")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.delete("/{category_id}")
async def delete(category_id: int, current_user: UserSchema = Depends(get_current_user)) -> str:
    if current_user.role == enums.UserRole.ADMIN:
        result = await category_repository.get(id=category_id)
        if result is None:
            raise HTTPException(404, detail="Category not found. Check the category id")

        try:
            await category_repository.delete(id=category_id)
            return "Category deleted successfully"
        except:
            raise HTTPException(400, detail="Category not deleted. Check the category id")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.put("/{category_id}")
async def update(category_id: int, category_data: CategoryUpdateScheme = Depends(),
                 current_user: UserSchema = Depends(get_current_user)) -> CategoryScheme:
    if current_user.role == enums.UserRole.ADMIN:
        category = await category_repository.get(id=category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        if category_data.name:
            category.name = category_data.name
    
        try:
            await category_repository.save(entity=category)
            return category
        except:
            raise HTTPException(status_code=400, detail="Failed to update category")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
