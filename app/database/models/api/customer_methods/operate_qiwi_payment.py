from typing import Optional

from data_models.user_models import BaseUser
from database.engine import AsyncSessionTyping
from database.models.api.customer_methods.qiwi_check_availability import (
    qiwi_check_availability,
)
from database.models.api.customer_methods.update_user_balance import (
    update_user_balance,
)
from logger import get_logger
from settings.digit_constants import BASE_LEN_ID
from settings.settings import calculate_qiwi_amount


async def operate_qiwi_payment(
        session: AsyncSessionTyping,
        bot_id: int,
        comment: Optional[str],
        amount: float
) -> Optional[int]:
    log = get_logger(__name__)
    log.info('bot_id: %d, comment: %s, amount: %f - start',
             bot_id, comment, amount)

    if not comment or len(comment) != 2*BASE_LEN_ID or not comment.isdecimal():
        log.info('bot_id: %d, comment: %s, amount: %f - incorrect comment',
                 bot_id, comment, amount)
        return None

    trans_bot_id = int(comment[BASE_LEN_ID:])
    trans_chat_id = int(comment[:BASE_LEN_ID])
    user: BaseUser = await qiwi_check_availability(
        session, trans_chat_id, trans_bot_id)
    if not user:
        log.info('bot_id: %d, comment: %s, amount: %f - not fount user_id=%s',
                 bot_id, comment, amount, trans_chat_id)
        return None
    if user.tg_bot_id == bot_id:
        amount = calculate_qiwi_amount(amount)
        await update_user_balance(session, bot_id, user.chat_id, amount)
        return user.chat_id
