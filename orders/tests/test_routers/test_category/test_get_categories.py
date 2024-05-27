from httpx import AsyncClient
from pytest_mock import MockerFixture

from api.repository import category_repository


async def test_category_repository_called_to_get_categories(mocker: MockerFixture, client: AsyncClient):
    spy = mocker.patch.object(category_repository, "get_many")

    res = await client.get("/categories")

    assert res.status_code == 200
    assert spy.call_count == 1
    assert spy.call_args.kwargs == {}
