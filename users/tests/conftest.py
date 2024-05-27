import pytest
from pytest_mock import MockerFixture
from asyncio import get_event_loop
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import insert

from pathlib import Path

from .dbutils import drop_database, database_exists, create_database

from api.config import config
from api.repository import Session, engine
from api.models import Base, User
from api.app import app

import json

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
