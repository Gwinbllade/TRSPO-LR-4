from pytest_mock import MockerFixture
import pytest
from httpx import AsyncClient

from api.repository import category_repository
from api.domain import CategoryScheme


@pytest.fixture(autouse=True)
def necessary_mocks(mocker: MockerFixture):
    mocker.patch.object(category_repository, "get", return_value=CategoryScheme(id=1, name="name"))
    mocker.patch.object(category_repository, "save")


async def test_get_called_with_correct_arguments_if_admin(mocker: MockerFixture, client: AsyncClient, admin_auth):
    category_id = 123
    spy = mocker.spy(category_repository, "get")

    res = await client.put(f"/categories/{category_id}", cookies={"access_token": "access_token"})

    assert res.status_code == 200
    assert spy.call_count == 1
    assert spy.call_args.kwargs == {
        "id": category_id
    }


async def test_update_called_if_category_exists_and_admin(mocker: MockerFixture, client: AsyncClient, admin_auth):
    new_name = "test"
    spy = mocker.spy(category_repository, "save")

    res = await client.put(f"/categories/123", params={"name": new_name}, cookies={"access_token": "access_token"})

    assert res.status_code == 200
    assert spy.call_count == 1
    assert spy.call_args.kwargs == {
        "entity": mocker.ANY
    }
    assert spy.call_args.kwargs["entity"].name == new_name


async def test_update_not_called_if_category_not_exists_and_admin(mocker: MockerFixture, client: AsyncClient, admin_auth):
    mocker.patch.object(category_repository, "get", return_value=None)
    spy = mocker.spy(category_repository, "save")

    res = await client.put(f"/categories/123", cookies={"access_token": "access_token"})

    assert res.status_code == 404
    assert spy.call_count == 0


async def test_400_if_not_updated(mocker: MockerFixture, client: AsyncClient, admin_auth):
    mocker.patch.object(category_repository, "save", side_effect=Exception)

    res = await client.put(f"/categories/123", cookies={"access_token": "access_token"})

    assert res.status_code == 400


async def test_403_if_not_admin(mocker: MockerFixture, client: AsyncClient, buyer_auth):
    res = await client.put(f"/categories/123", cookies={"access_token": "access_token"})

    assert res.status_code == 403


async def test_401_if_not_authorized(mocker: MockerFixture, client: AsyncClient):
    res = await client.put(f"/categories/123")

    assert res.status_code == 401
