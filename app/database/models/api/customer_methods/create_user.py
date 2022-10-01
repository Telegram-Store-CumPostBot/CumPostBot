from typing import Optional

from cashews import cache
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.api.customer_methods.check_availability import (
    check_availability,
)
from database.engine import async_session
from database.models.tables.customer import Customer
from logger import get_logger


@cache.invalidate(
    check_availability, {
        'bot_id': 'tg_bot_id'
    }
)
async def create_new(
        chat_id: int,
        username: str,
        first_name: str,
        last_name: str,
        refer_id: Optional[int] = None,
        tg_bot_id: Optional[int] = None,
) -> Customer:
    log = get_logger(__name__)
    log.info('create new user chat_id: %d bot_id: %d', chat_id, tg_bot_id)
    async with async_session() as session:
        session: AsyncSession
        kwargs = {
            'chat_id': chat_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        }
        if refer_id:
            kwargs['refer_id'] = refer_id
        if tg_bot_id:
            kwargs['tg_bot_id'] = tg_bot_id

        user = Customer(**kwargs)
        session.add(user)
        await session.commit()
    log.info('success create new user chat_id: %d bot_id: %d',
             chat_id, tg_bot_id)
    return user
