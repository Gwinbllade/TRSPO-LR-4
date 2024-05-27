from api.repository import user_repository
from api.models import User
from api.enums import UserRole

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def test_user_created_successfully(session: AsyncSession):
    username = "test"

    await user_repository.save(entity=User(role=UserRole.ADMIN, username=username, email="email", hashed_password="hashed_password"))

    assert (await session.execute(select(User).where(User.username == username))).scalar_one_or_none()


async def test_user_update_successfully(session: AsyncSession):
    username = "test"
    new_username = "new_test"

    await user_repository.save(entity=User(role=UserRole.ADMIN, username=username, email="email", hashed_password="hashed_password"))
    user = await user_repository.get(username=username)

    user.username = new_username
    await user_repository.save(entity=user)

    assert len((await session.execute(select(User))).scalars().all()) == 1
    assert (await session.execute(select(User).where(User.username == new_username))).scalar_one_or_none()
