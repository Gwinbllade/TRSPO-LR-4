from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from api.models import *
from api.config import config


engine = create_async_engine(url=config.db_url)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Repository:
    cls = Base

    async def get(self, **kwargs) -> type[cls] | None:
        stmt = select(self.cls).filter_by(**kwargs)
        async with Session() as session:
            return (await session.execute(stmt)).scalar_one_or_none()

    async def get_many(self, **kwargs) -> list[type[cls]]:
        stmt = select(self.cls).filter_by(**kwargs)
        async with Session() as session:
            return (await session.execute(stmt)).scalars().all()

    async def save(self, entity: type[cls]) -> None:
        stmt = insert(self.cls)
        async with Session() as session:
            await session.execute(
                stmt.on_conflict_do_update(index_elements=["id"], set_=stmt.excluded),
                [entity.to_dict()]
            )
            await session.commit()
    
    async def delete(self, **kwargs) -> None:
        stmt = delete(self.cls).filter_by(**kwargs)
        async with Session() as session:
            await session.execute(stmt)
            await session.commit()
 

class OrderRepository(Repository):
    cls = Order


class ProductRepository(Repository):
    cls = Product


class CategoryRepository(Repository):
    cls = Category


order_repository = OrderRepository()
product_repository = ProductRepository()
category_repository = CategoryRepository()
