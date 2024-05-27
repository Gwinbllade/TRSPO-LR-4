from pytest_mock import MockerFixture
import pytest
from httpx import AsyncClient

from api.repository import category_repository


@pytest.fixture(autouse=True)
def necessary_mocks(mocker: MockerFixture):
    mocker.patch.object(category_repository, "save")


async def test_save_called_with_correct_arguments_if_admin(mocker: MockerFixture, client: AsyncClient, admin_auth):
    name = "name"
    spy = mocker.spy(category_repository, "save")

    res = await client.post(f"/categories", params={"name": name}, cookies={"access_token": "access_token"})

    assert res.status_code == 200
    assert spy.call_count == 1
    assert spy.call_args.kwargs == {
        "entity": mocker.ANY
    }
    assert spy.call_args.kwargs["entity"].name == name


async def test_400_if_not_created(mocker: MockerFixture, client: AsyncClient, admin_auth):
    mocker.patch.object(category_repository, "save", side_effect=Exception)

    res = await client.post(f"/categories", params={"name": "name"}, cookies={"access_token": "access_token"})

    assert res.status_code == 400


async def test_403_if_not_admin(mocker: MockerFixture, client: AsyncClient, buyer_auth):
    res = await client.post(f"/categories", params={"name": "name"}, cookies={"access_token": "access_token"})

    assert res.status_code == 403


async def test_401_if_not_authorized(mocker: MockerFixture, client: AsyncClient):
    res = await client.post(f"/categories", params={"name": "name"})

    assert res.status_code == 401
