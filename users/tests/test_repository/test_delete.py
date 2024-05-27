from api.repository import user_repository
from api.models import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.enums import UserRole


async def test_user_deleted_successfully(session: AsyncSession):
    username = "test"

    await user_repository.save(entity=User(role=UserRole.ADMIN, username=username, email="email", hashed_password="hashed_password"))
    await user_repository.delete(username=username)

    assert not (await session.execute(select(User).where(User.username == username))).scalars().all()
