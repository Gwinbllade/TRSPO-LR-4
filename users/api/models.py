from typing import Any

from sqlalchemy import Enum
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

from api import enums


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def to_dict() -> dict[str, Any]:
        pass


class User(Base):
    __tablename__ = "user"

    role: Mapped[enums.UserRole] = mapped_column(Enum(enums.UserRole))
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    def to_dict(self) -> dict[str, Any]:
        user_dict = dict(
            role=self.role,
            username=self.username,
            email=self.email,
            hashed_password=self.hashed_password,
        )

        if self.id:
            user_dict["id"] = self.id

        return user_dict
