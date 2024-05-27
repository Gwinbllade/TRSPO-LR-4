from typing import Optional

from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    name: str
    cost: float
    category_id: int

    class Config:
        from_attributes = True


class ProductFilterSchema(BaseModel):
    category_id: int | None
    min_price: float | None = None
    max_price: float | None = None


class ProductUpdateSchema(BaseModel):
    id: int
    name: str | None = None
    cost: float | None = None
    category_id: int | None = None


class ProductAddSchema(BaseModel):
    name: str
    cost: int
    category_id: int
