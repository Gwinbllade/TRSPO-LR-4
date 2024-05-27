from asyncpg.exceptions import InvalidCatalogNameError
from sqlalchemy import make_url, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


async def database_exists(database_url: str) -> bool:
    url = make_url(database_url)
    database = url.database

    async_engine: AsyncEngine | None = None
    try:
        stmt = text(f"SELECT 1 FROM pg_database WHERE datname='{database}'")
        dbs = [database, "postgres", "template0", "template1", None]
        for db in dbs:
            url = url.set(database=db)
            async_engine = create_async_engine(url)
            try:
                async with async_engine.connect() as async_connection:
                    return bool(await async_connection.scalar(stmt))
            except (OperationalError, ProgrammingError, InvalidCatalogNameError):
                pass
        return False
    finally:
        if async_engine:
            await async_engine.dispose()


async def drop_database(database_url: str) -> None:
    url = make_url(database_url)
    database = url.database

    async_engine: AsyncEngine | None = None
    try:
        prep = text(
            f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{database}'
            AND pid <> pg_backend_pid();
            """,
        )
        stmt = text(f"DROP DATABASE {database}")

        url = url.set(database="postgres")
        async_engine = create_async_engine(url, isolation_level="AUTOCOMMIT")
        try:
            async with async_engine.begin() as async_connection:
                await async_connection.execute(prep)
                await async_connection.execute(stmt)
        except (OperationalError, ProgrammingError, InvalidCatalogNameError):
            pass
    finally:
        if async_engine:
            await async_engine.dispose()


async def create_database(database_url: str, encoding: str = "utf8") -> None:
    url = make_url(database_url)
    database = url.database

    async_engine: AsyncEngine | None = None
    try:
        stmt = text(
            f"CREATE DATABASE {database} ENCODING {encoding} TEMPLATE 'template1'",
        )

        url = url.set(database="postgres")
        async_engine = create_async_engine(url, isolation_level="AUTOCOMMIT")
        try:
            async with async_engine.begin() as async_connection:
                await async_connection.execute(stmt)
        except (OperationalError, ProgrammingError, InvalidCatalogNameError):
            pass
    finally:
        if async_engine:
            await async_engine.dispose()
