from ormar import ModelMeta
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.url import URL as DB_URL

from settings.settings import settings


connection_url: DB_URL = DB_URL(drivername='postgresql',
                                username=settings.pg_user,
                                password=settings.pg_pass,
                                host=settings.pg_host,
                                port=settings.pg_port,
                                database=settings.pg_db_name,
                                )


Base = declarative_base()
engine = create_engine(connection_url)

# ормар берет либо str либо свой класс ссылки
database = Database(connection_url.__str__())

metadata = MetaData()


class BaseMeta(ModelMeta):
    metadata = metadata
    database = database


async def connect_to_database():
    while True:
        try:
            metadata.create_all(engine)
            break
        except OperationalError:
            continue

    if not database.is_connected:
        await database.connect()
