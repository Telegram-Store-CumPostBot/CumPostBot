from typing import Optional

from cashews import cache
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from database.engine import async_session
from database.models.tables.tg_bot import TGBot
from logger import get_logger


@cache(ttl=15, key='tgbot:get_qiwi_txn:{tg_bot_id}')
async def get_qiwi_txn(tg_bot_id: int) -> Optional[int]:
    log = get_logger(__name__)
    log.info('get_qiwi_txn bot_id: %d', tg_bot_id)
    async with async_session() as session:
        query = query_get_qiwi_txn(tg_bot_id)
        res = await session.execute(query)
    return res.first()[0]


def query_get_qiwi_txn(tg_bot_id: int) -> Select:
    query = select(TGBot.qiwi_txn).where(TGBot.tg_bot_id == tg_bot_id)
    return query
