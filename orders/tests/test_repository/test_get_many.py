from api.repository import category_repository
from api.models import Category


async def test_categories_returned():
    name = "test"

    await category_repository.save(entity=Category(name=name))

    assert await category_repository.get_many()

async def test_empty_list_returned():
    assert not (await category_repository.get_many())
