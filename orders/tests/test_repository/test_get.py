from api.repository import category_repository
from api.models import Category


async def test_category_returned():
    name = "test"

    await category_repository.save(entity=Category(name=name))

    assert await category_repository.get(name=name)

async def test_none_returned():
    name = "test"

    assert not (await category_repository.get(name=name))
