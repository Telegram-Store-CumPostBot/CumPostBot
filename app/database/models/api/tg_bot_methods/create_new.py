from typing import Optional

from database.engine import async_session
from database.models.tables.tg_bot import TGBot
from logger import get_logger


async def create_new(
        bot_id: int,
        bot_token: str,
        start_message: Optional[str] = None,
        qiwi_txn: Optional[int] = None,
        admin_id: Optional[int] = None,
) -> TGBot:
    log = get_logger(__name__)
    log.info('call method "create bot" bot_id: %d bot_token: %s admin_id: %s',
             bot_id, bot_token, str(admin_id))

    async with async_session() as session:
        bot = TGBot(
            tg_bot_id=bot_id,
            tg_token=bot_token,
            start_message=start_message,
            qiwi_txn=qiwi_txn,
            admin_id=admin_id,
        )
        session.add(bot)
        await session.commit()
    log = get_logger(__name__)
    log.info('success create bot bot_id: %d bot_token: %s admin_id: %s',
             bot_id, bot_token, str(admin_id))
    return bot
