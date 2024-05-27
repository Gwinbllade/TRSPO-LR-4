from api.repository import category_repository
from api.models import Category

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def test_category_created_successfully(session: AsyncSession):
    name = "test"

    await category_repository.save(entity=Category(name=name))

    assert (await session.execute(select(Category).where(Category.name == name))).scalar_one_or_none()


async def test_category_update_successfully(session: AsyncSession):
    name = "test"
    new_name = "new_test"

    await category_repository.save(entity=Category(name=name))
    category = await category_repository.get(name=name)

    category.name = new_name
    await category_repository.save(entity=category)

    assert len((await session.execute(select(Category))).scalars().all()) == 1
    assert (await session.execute(select(Category).where(Category.name == new_name))).scalar_one_or_none()
