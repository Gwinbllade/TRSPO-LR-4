from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status

from api.domain import ProductAddSchema, ProductSchema, ProductUpdateSchema, UserSchema
from api.repository import product_repository
from api.dependencies import get_current_user
from api.models import Product
from api import enums


router = APIRouter(
    prefix="/products",
    tags=['Products']
)


@router.get("")
async def get_products(category_id: int | None = None) -> list[ProductSchema]:
    if category_id is not None:
        products = await product_repository.get_many(category_id=category_id)
    else:
        products = await product_repository.get_many()
    return products


@router.post("")
async def add_product(args: ProductAddSchema = Depends(), current_user: UserSchema = Depends(get_current_user)) -> ProductAddSchema:
    if current_user.role == enums.UserRole.ADMIN:
        try:
            new_product = Product(name=args.name,
                cost=args.cost,
                category_id=args.category_id)
            
            await product_repository.save(entity=new_product)
            return new_product
        except:
            raise HTTPException(501, detail="product not added. Check the parameters ")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.delete("/{product_id}")
async def delete_product(product_id: int, current_user: UserSchema = Depends(get_current_user)) -> str:
    if current_user.role == enums.UserRole.ADMIN:
        result = await product_repository.get(id=product_id)
        if result is None:
            raise HTTPException(501, detail="product not delete. Check the product id ")
        try:
            await product_repository.delete(id=product_id)
            return "Product deleted successfully"
        except:
            raise HTTPException(501, detail="product not delete. Check the product id ")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.patch("")
async def update(product_data: ProductUpdateSchema = Depends(), current_user: UserSchema = Depends(get_current_user)) -> ProductSchema:
    if current_user.role == enums.UserRole.ADMIN:
        product = await product_repository.get(id=product_data.id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product_data.name:
            product.name = product_data.name
        if product_data.cost:
            product.cost = product_data.cost
        if product_data.category_id:
            product.category_id = product_data.category_id

        try:
            await product_repository.save(entity=product)
            return product
        except:
            raise HTTPException(status_code=400, detail="Failed to update product")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
