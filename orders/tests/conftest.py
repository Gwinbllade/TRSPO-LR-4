import pytest
from pytest_mock import MockerFixture
from asyncio import get_event_loop
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncConnection

from .dbutils import drop_database, database_exists, create_database

from api.config import config
from api.repository import Session, engine
from api.models import Base
from api.app import app
from api.domain import UserSchema
from api import enums

import requests
from httpx import AsyncClient


@pytest.fixture(scope="session")
def event_loop(request):
    loop = get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def db_conn() -> AsyncGenerator[AsyncConnection, None]:
    if await database_exists(database_url=config.db_url):
        await drop_database(database_url=config.db_url)
    await create_database(database_url=config.db_url)

    engine.echo = False
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        yield conn
    await engine.dispose()

    if await database_exists(database_url=config.db_url):
        await drop_database(database_url=config.db_url)


@pytest.fixture()
async def session(mocker: MockerFixture):
    async with Session() as session:
        mocker.patch.object(session, "commit")
        yield session


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


class AuthResponse:
    def __init__(self, role: enums.UserRole) -> None:
        self.role = role

    @property
    def status_code(self):
        return 200
    
    @property
    def content(self):
        return UserSchema(id=1, role=self.role, username="username", email="email").model_dump_json()


@pytest.fixture
def admin_auth(mocker: MockerFixture):
    mocker.patch.object(requests, "get", return_value=AuthResponse(role=enums.UserRole.ADMIN))


@pytest.fixture
def buyer_auth(mocker: MockerFixture):
    mocker.patch.object(requests, "get", return_value=AuthResponse(role=enums.UserRole.BUYER))
