from typing import Optional

from cashews import cache
from sqlalchemy.engine.result import Result
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from data_models.user_models import BaseUser
from database.engine import AsyncSessionTyping
from database.models.tables.customer import Customer
from logger import get_logger


cache_key = 'customer:qiwi_availability:{qiwi_chat_id}{qiwi_bot_id}'


@cache(ttl=1_800_000, key=cache_key)
async def qiwi_check_availability(
        session: AsyncSessionTyping,
        qiwi_chat_id: int,
        qiwi_bot_id: int,
) -> Optional[BaseUser]:
    log = get_logger(__name__)
    log.info('check QIWI user availability chat_id: %d bot_id: %d',
             qiwi_chat_id, qiwi_bot_id)

    query = query_check_availability(qiwi_chat_id, qiwi_bot_id)
    res: Result = await session.execute(query)

    user = res.first()
    log.info('res WIWI check user availability chat_id: %d bot_id: %d is %s',
             qiwi_chat_id, qiwi_bot_id, bool(user))

    if not user:
        return user
    print(user)
    return BaseUser(**user)


def query_check_availability(chat_id: int, bot_id: int) -> Select:
    query: Select = select(
        Customer.chat_id,
        Customer.tg_bot_id
    ).where(
        Customer.qiwi_chat_id == chat_id,
        Customer.qiwi_tg_bot_id == bot_id
    )
    return query
