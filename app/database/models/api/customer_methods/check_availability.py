from cashews import cache
from sqlalchemy.engine.result import Result
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from database.engine import AsyncSessionTyping
from database.models.tables.customer import Customer
from logger import get_logger


@cache(ttl=1_800_000, key='customer:availability:{chat_id}{bot_id}')
async def check_availability(
        session: AsyncSessionTyping,
        chat_id: int,
        bot_id: int,
) -> bool:
    log = get_logger(__name__)
    log.info('check user availability chat_id: %d bot_id: %d', chat_id, bot_id)
    query = query_check_availability(chat_id, bot_id)
    res: Result = await session.execute(query)

    user = res.first()
    log.info('res check user availability chat_id: %d bot_id: %d',
             chat_id, bot_id)
    return bool(user)


def query_check_availability(chat_id: int, bot_id: int) -> Select:
    query: Select = select(
        Customer.chat_id
    ).where(
        Customer.chat_id == chat_id,
        Customer.tg_bot_id == bot_id
    )
    return query
