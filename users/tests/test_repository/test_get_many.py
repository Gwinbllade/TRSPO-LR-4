from api.repository import user_repository
from api.models import User
from api.enums import UserRole


async def test_categories_returned():
    username = "test"

    await user_repository.save(entity=User(role=UserRole.ADMIN, username=username, email="email", hashed_password="hashed_password"))

    assert await user_repository.get_many()


async def test_none_returned():
    assert not (await user_repository.get_many())
