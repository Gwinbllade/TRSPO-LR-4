from typing import Any
from datetime import datetime

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

from api import enums


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def to_dict() -> dict[str, Any]:
        pass


class Order(Base):
    __tablename__ = "order"

    status: Mapped[enums.OrderStatus] = mapped_column(Enum(enums.OrderStatus))
    date: Mapped[datetime]
    user_id: Mapped[int]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", onupdate="CASCADE", ondelete="CASCADE"))

    def to_dict(self) -> dict[str, Any]:
        return dict(
            id=self.id,
            status=self.status,
            date=self.date,
            user_id=self.user_id,
            product_id=self.product_id,
        )


class Product(Base):
    __tablename__ = "product"

    name: Mapped[str]
    cost: Mapped[float]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", onupdate="CASCADE", ondelete="CASCADE"))

    def to_dict(self) -> dict[str, Any]:
        return dict(
            id=self.id,
            name=self.name,
            cost=self.cost,
            category_id=self.category_id,
        )


class Category(Base):
    __tablename__ = "category"

    name: Mapped[str]

    def to_dict(self) -> dict[str, Any]:
        return dict(
            id=self.id,
            name=self.name,
        )
