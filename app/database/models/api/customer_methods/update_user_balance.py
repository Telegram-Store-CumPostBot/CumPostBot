from sqlalchemy import update
from sqlalchemy.sql import Update

from database.engine import AsyncSessionTyping
from database.models.tables.customer import Customer
from logger import get_logger


async def update_user_balance(
        session: AsyncSessionTyping,
        bot_id: int,
        chat_id: int,
        amount: float,
):
    log = get_logger(__name__)
    log.info('bot_id: %d, chat_id: %d, amount: %d - start ',
             bot_id, chat_id, amount)
    query = query_update_balance(bot_id, chat_id, amount)
    await session.execute(query)
    log.info('bot_id: %d, chat_id: %d, amount: %d - '
             'success add update is session',
             bot_id, chat_id, amount)


def query_update_balance(bot_id: int, chat_id: int, amount: float) -> Update:
    query = update(Customer).where(
        Customer.tg_bot_id == bot_id,
        Customer.chat_id == chat_id,
    ).values(
        balance=Customer.balance + amount
    )
    return query
