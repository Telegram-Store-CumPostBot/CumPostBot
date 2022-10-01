from cashews import cache
from sqlalchemy.engine import Result
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from data_models.user_models import MoneyUserInfo
from database.engine import async_session
from database.models.tables.customer import Customer
from logger import get_logger
from settings.settings import config


cache_key = 'customer:balance:{chat_id}{bot_id}'
ttl_cache = float(config['CacheTimings']['user_balance'])


@cache(ttl=ttl_cache, key=cache_key)
async def get_balance(chat_id: int, bot_id: int) -> MoneyUserInfo:
    log = get_logger(__name__)
    log.info('get user balance chat_id: %d bot_id: %d', chat_id, bot_id)
    async with async_session() as session:
        query = get_query_get_balance_info(chat_id, bot_id)
        res: Result = await session.execute(query)
        user = res.first()

    user = MoneyUserInfo(chat_id=chat_id, tg_bot_id=bot_id, **user)
    log.info('user (chat_id: %d bot_id: %d) - balance: %d',
             chat_id, bot_id, user.total_balance)
    return user


def get_query_get_balance_info(chat_id: int, bot_id: int) -> Select:
    query: Select = select(
        Customer.balance,
        Customer.fake_bal,
        Customer.sum_orders,
        Customer.ref_fees
    ).where(
        Customer.chat_id == chat_id,
        Customer.tg_bot_id == bot_id
    )
    return query
