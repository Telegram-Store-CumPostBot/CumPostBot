from typing import Optional

from database.engine import AsyncSessionTyping
from database.models.api.customer_methods.check_availability import \
    check_availability
from database.models.api.customer_methods.update_user_balance import \
    update_user_balance
from logger import get_logger


async def operate_qiwi_payment(
        session: AsyncSessionTyping,
        bot_id: int,
        comment: str,
        amount: float
) -> Optional[int]:
    log = get_logger(__name__)
    log.info('bot_id: %d, comment: %s, amount: %f - start',
             bot_id, comment, amount)
    if not comment.isdecimal():
        log.info('bot_id: %d, comment: %s, amount: %f - incorrect comment',
                 bot_id, comment, amount)
        return None

    if await check_availability(session, int(comment), bot_id):
        await update_user_balance(session, bot_id, int(comment), amount)
        return int(comment)
    log.info('bot_id: %d, comment: %s, amount: %f - not fount user_id=%s',
             bot_id, comment, amount, comment)
    return None
