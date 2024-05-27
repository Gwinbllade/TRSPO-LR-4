from api.repository import category_repository
from api.models import Category

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def test_category_deleted_successfully(session: AsyncSession):
    name = "test"

    await category_repository.save(entity=Category(name=name))
    await category_repository.delete(name=name)

    assert not (await session.execute(select(Category).where(Category.name == name))).scalars().all()
