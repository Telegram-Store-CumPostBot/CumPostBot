from cashews import cache
from sqlalchemy import update

from database.engine import async_session
from database.models.api.tg_bot_methods.get_qiwi_txn import get_qiwi_txn
from database.models.tables.tg_bot import TGBot
from logger import get_logger


@cache.invalidate(get_qiwi_txn, {'tg_bot_id': 'tg_bot_id'})
async def set_qiwi_txn(tg_bot_id: int, qiwi_txn: int) -> bool:
    """Устанавливает qiwi_txn
    Пока всегда возвращает True"""
    log = get_logger(__name__)
    log.info('set_qiwi_txn bot_id: %d qiwi_txn: %d', tg_bot_id, qiwi_txn)
    async with async_session() as session:
        query = query_set_qiwi_txn(tg_bot_id, qiwi_txn)
        await session.execute(query)
        await session.commit()
    return True


def query_set_qiwi_txn(tg_bot_id: int, qiwi_txn: int):
    query = update(TGBot).where(
        TGBot.tg_bot_id == tg_bot_id
    ).values(
        qiwi_txn=qiwi_txn
    )
    return query
