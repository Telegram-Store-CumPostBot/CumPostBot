from sqlalchemy import update
from sqlalchemy.sql import Update

from database.engine import AsyncSessionTyping
from database.models.tables.customer import Customer
from logger import get_logger


async def update_user_balance(
        session: AsyncSessionTyping,
        bot_id: int,
        user_id: int,
        amount: float,
):
    log = get_logger(__name__)
    log.info(f'start {bot_id=}, {user_id=}, {amount=}')
    query = query_update_balance(bot_id, user_id, amount)
    await session.execute(query)
    log.info(f'success add update {bot_id=}, {user_id=}, {amount=} in session')


def query_update_balance(bot_id: int, user_id: int, amount: float) -> Update:
    query = update(Customer).where(
        Customer.tg_bot_id == bot_id,
        Customer.customer_id == user_id,
    ).values(
        balance=Customer.balance + amount
    )
    return query
