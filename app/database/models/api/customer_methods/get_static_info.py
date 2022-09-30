from cashews import cache
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from data_models.user_models import ProfileInfo
from database.engine import async_session
from database.models.tables.customer import Customer
from logger import get_logger
from settings.settings import config


ttl_cache = float(config['CacheTimings']['user_static_info'])
key_cache = 'customer:static_info:{chat_id}{bot_id}'


@cache(ttl=ttl_cache, key=key_cache)
async def get_static_info(chat_id: int, bot_id: int) -> ProfileInfo:
    log = get_logger(__name__)
    log.info('get user static info chat_id: %d bot_id: %d', chat_id, bot_id)
    async with async_session() as session:
        query = query_static_info(chat_id, bot_id)
        res = await session.execute(query)

    user = res.mappings().first()
    return ProfileInfo(chat_id=chat_id, tg_bot_id=bot_id, **user)


def query_static_info(chat_id: int, bot_id: int) -> Select:
    query: Select = select(
        Customer.username,
        Customer.first_name,
        Customer.last_name,
        Customer.ref_count
    ).where(
        Customer.chat_id == chat_id,
        Customer.tg_bot_id == bot_id
    )
    return query
