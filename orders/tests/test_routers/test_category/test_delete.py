from pytest_mock import MockerFixture
import pytest
from httpx import AsyncClient

from api.repository import category_repository
from api.domain import CategoryScheme


@pytest.fixture(autouse=True)
def necessary_mocks(mocker: MockerFixture):
    mocker.patch.object(category_repository, "get", return_value=CategoryScheme(id=1, name="name"))
    mocker.patch.object(category_repository, "delete")


async def test_get_called_with_correct_arguments_if_admin(mocker: MockerFixture, client: AsyncClient, admin_auth):
    category_id = 123
    spy = mocker.spy(category_repository, "get")

    res = await client.delete(f"/categories/{category_id}", cookies={"access_token": "access_token"})

    assert res.status_code == 200
    assert spy.call_count == 1
    assert spy.call_args.kwargs == {
        "id": category_id
    }


async def test_delete_called_if_category_exists_and_admin(mocker: MockerFixture, client: AsyncClient, admin_auth):
    category_id = 123
    spy = mocker.spy(category_repository, "delete")

    res = await client.delete(f"/categories/{category_id}", cookies={"access_token": "access_token"})

    assert res.status_code == 200
    assert spy.call_count == 1
    assert spy.call_args.kwargs == {
        "id": category_id
    }


async def test_delete_not_called_if_category_not_exists_and_admin(mocker: MockerFixture, client: AsyncClient, admin_auth):
    mocker.patch.object(category_repository, "get", return_value=None)
    spy = mocker.spy(category_repository, "delete")

    res = await client.delete(f"/categories/123", cookies={"access_token": "access_token"})

    assert res.status_code == 404
    assert spy.call_count == 0


async def test_400_if_not_deleted(mocker: MockerFixture, client: AsyncClient, admin_auth):
    mocker.patch.object(category_repository, "delete", side_effect=Exception)

    res = await client.delete(f"/categories/123", cookies={"access_token": "access_token"})

    assert res.status_code == 400


async def test_403_if_not_admin(mocker: MockerFixture, client: AsyncClient, buyer_auth):
    res = await client.delete(f"/categories/123", cookies={"access_token": "access_token"})

    assert res.status_code == 403


async def test_401_if_not_authorized(mocker: MockerFixture, client: AsyncClient):
    res = await client.delete(f"/categories/123")

    assert res.status_code == 401
