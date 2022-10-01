from sqlalchemy.future import select

from database.engine import async_session
from database.models.tables.tg_bot import TGBot
from logger import get_logger


async def check_availability(tg_bot_id: int) -> bool:
    log = get_logger(__name__)
    log.info('check bot availability tg_bot_id: %d', tg_bot_id)
    async with async_session() as session:
        query = select(TGBot.tg_bot_id).where(TGBot.tg_bot_id == tg_bot_id)
        res = await session.execute(query)
    res = res.all()
    return bool(res)
