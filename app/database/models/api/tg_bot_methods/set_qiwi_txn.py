from sqlalchemy import update

from database.engine import async_session
from database.models.tables.tg_bot import TGBot


async def set_qiwi_txn(tg_bot_id: int, qiwi_txn: int) -> bool:
    """Устанавливает qiwi_txn
    Пока всегда возвращает True"""
    async with async_session() as session:
        query = query_set_qiwi_txn(tg_bot_id, qiwi_txn)
        await session.execute(query)
    return True


def query_set_qiwi_txn(tg_bot_id: int, qiwi_txn: int):
    query = update(TGBot).where(
        TGBot.tg_bot_id == tg_bot_id
    ).values(
        qiwi_txn=qiwi_txn
    )
    return query
