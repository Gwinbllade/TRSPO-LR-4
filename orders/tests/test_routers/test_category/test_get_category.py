from httpx import AsyncClient
from pytest_mock import MockerFixture
import pytest

from api.domain import CategoryScheme
from api.repository import category_repository

@pytest.fixture(autouse=True)
def necessary_mocks(mocker: MockerFixture):
    mocker.patch.object(category_repository, "get", return_value=CategoryScheme(id=1, name="name"))


async def test_category_repository_called_to_get_category_with_correct_arguments(
    mocker: MockerFixture, client: AsyncClient
):
    category_id = 123
    spy = mocker.spy(category_repository, "get")

    res = await client.get(f"/categories/{category_id}")

    assert res.status_code == 200
    assert spy.call_count == 1
    assert spy.call_args.kwargs == {
        "id": category_id
    }


async def test_404_returned_if_category_not_found(mocker: MockerFixture, client: AsyncClient):
    mocker.patch.object(category_repository, "get", return_value=None)

    res = await client.get(f"/categories/{123}")

    assert res.status_code == 404
