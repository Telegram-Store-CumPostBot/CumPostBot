from typing import Optional

from cashews import cache

from database.engine import AsyncSessionTyping
from database.models.api.customer_methods.check_availability import (
    check_availability,
)
from database.models.tables.customer import Customer
from logger import get_logger


@cache.invalidate(
    check_availability, {
        'bot_id': 'tg_bot_id'
    }
)
async def create_new(
        session: AsyncSessionTyping,
        chat_id: int,
        username: str,
        first_name: str,
        last_name: str,
        tg_bot_id: int,
        ref_chat_id: Optional[int] = None,
        ref_tg_bot_id: Optional[int] = None,
) -> Customer:
    log = get_logger(__name__)
    log.info('create new user chat_id: %d bot_id: %d', chat_id, tg_bot_id)
    user = Customer(
        chat_id=chat_id,
        tg_bot_id=tg_bot_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        ref_chat_id=ref_chat_id,
        ref_tg_bot_id=ref_tg_bot_id,
    )
    session.add(user)
    log.info('success add new user chat_id: %d bot_id: %d in session',
             chat_id, tg_bot_id)
    return user
