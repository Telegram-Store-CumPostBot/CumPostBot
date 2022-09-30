from typing import ForwardRef

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.util import EMPTY_DICT

from settings.settings import settings


url_config = {
    'drivername': 'postgresql+asyncpg',
    'username': settings.pg_user,
    'password': settings.pg_pass,
    'host': settings.pg_host,
    'port': settings.pg_port,
    'database': settings.pg_db_name,
    'query': EMPTY_DICT
}


connection_url = URL(**url_config)


Base = declarative_base()
engine: AsyncEngine = create_async_engine(
    connection_url,
    echo=True
)


AsyncSessionTypingRef = ForwardRef("AsyncSessionTyping")


class AsyncSessionTyping(AsyncSession):
    async def __aenter__(self) -> AsyncSessionTypingRef:
        return self

    async def execute(
            self,
            statement,
            params=None,
            execution_options=EMPTY_DICT,
            bind_arguments=None,
            **kw
    ) -> Result:
        return await super().execute(
            statement,
            params,
            execution_options,
            bind_arguments,
            **kw
        )


class my_sessionmaker(sessionmaker):
    def __call__(self, **local_kw) -> AsyncSessionTyping:
        res = super().__call__(**local_kw)
        return res


async_session = my_sessionmaker(
    engine,
    class_=AsyncSessionTyping,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
