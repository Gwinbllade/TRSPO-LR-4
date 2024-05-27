from typing import List

from fastapi import Query
from pydantic import BaseModel
from datetime import datetime
from api import enums


class OrderSchema(BaseModel):
    id: int
    user_id: int
    date: datetime
    status: str
    product_id: int

    class Config:
        from_attributes = True


class NewOrderSchema(BaseModel):
    user_id: int
    date: datetime
    status: str
    product_id: int

    class Config:
        from_attributes = True


class OrderAddSchema(BaseModel):
    product_id: int


class OrderUpdateSchema(BaseModel):
    status: enums.OrderStatus
