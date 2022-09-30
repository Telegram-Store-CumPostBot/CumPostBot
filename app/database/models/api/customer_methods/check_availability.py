from cashews import cache
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from database.engine import async_session
from database.models.tables.customer import Customer
from logger import get_logger


@cache(ttl=1_800_000, key='customer:availability:{chat_id}{bot_id}')
async def check_availability(chat_id: int, bot_id: int) -> bool:
    log = get_logger(__name__)
    log.info('check user availability chat_id: %d bot_id: %d', chat_id, bot_id)
    async with async_session() as session:
        session: AsyncSession
        query = query_check_availability(chat_id, bot_id)
        res: Result = await session.execute(query)

    user = res.first()
    print(user)
    if user:
        return True
    return False


def query_check_availability(chat_id: int, bot_id: int) -> Select:
    query: Select = select(
        Customer.customer_id
    ).where(
        Customer.chat_id == chat_id,
        Customer.tg_bot_id == bot_id
    )
    return query
