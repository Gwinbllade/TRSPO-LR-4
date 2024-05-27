from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status

from api.repository import order_repository, product_repository
from api.domain import OrderAddSchema, OrderSchema, OrderUpdateSchema, NewOrderSchema, UserSchema
from api.models import Order
from api.dependencies import get_current_user
from api import enums


router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)


@router.get("")
async def get_orders(current_user: UserSchema = Depends(get_current_user)) -> List[OrderSchema]:
    if current_user.role == enums.UserRole.ADMIN:
        return await order_repository.get_many()
    else:
        return await order_repository.get_many(user_id=current_user.id)


@router.get("/{status}")
async def get_orders_by_status(status: enums.OrderStatus, current_user: UserSchema = Depends(get_current_user)) -> List[OrderSchema]:
    if current_user.role == enums.UserRole.ADMIN:
        return await order_repository.get_many(status=status)
    else:
        raise HTTPException(403)


@router.post("")
async def create_order(data: OrderAddSchema = Depends(), current_user: UserSchema = Depends(get_current_user)) -> NewOrderSchema:
    result = await product_repository.get(id=data.product_id)
    if result is None:
        raise HTTPException(404, detail="Product not found.")

    try:
        new_order = Order(
            status=enums.OrderStatus.PROCESSING,
            date=datetime.now(),
            user_id=current_user.id,
            product_id=data.product_id,
        )
        await order_repository.save(entity=new_order)
        return new_order
    except:
        raise HTTPException(500, detail="Order not created.")


@router.delete("/{order_id}")
async def delete(order_id: int, current_user: UserSchema = Depends(get_current_user)) -> str:
    if current_user.role == enums.UserRole.ADMIN:
        result = await order_repository.get(id=order_id)
        if result is None:
            raise HTTPException(501, detail="Order not delete. Check the product id ")

        try:
            await order_repository.delete(id=order_id)
            return "Order delete successfully"
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.patch("/status/{order_id}")
async def update_status(order_id:int, order_data: OrderUpdateSchema = Depends(), current_user: UserSchema = Depends(get_current_user)) -> OrderSchema:
    if current_user.role == enums.UserRole.ADMIN:
        order = await order_repository.get(id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        order.status = order_data.status
        try:
            await order_repository.save(entity=order)
            return order
        except:
            raise HTTPException(status_code=500, detail="Failed to update order status ")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
