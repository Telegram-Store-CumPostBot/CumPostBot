from typing import Optional

from data_models.user_models import MoneyUserInfo, ProfileInfo
from database.engine import AsyncSessionTyping
from database.models.api.customer_methods.check_availability import (
    check_availability,
)
from database.models.api.customer_methods.create_user import create_new
from database.models.api.customer_methods.get_balance import get_balance
from database.models.api.customer_methods.get_static_info import (
    get_static_info,
)
from database.models.api.customer_methods.operate_qiwi_payment import \
    operate_qiwi_payment
from database.models.api.customer_methods.update_user_balance import \
    update_user_balance
from database.models.tables.customer import Customer


class DBAPICustomer:
    @classmethod
    async def create_user(
            cls,
            session: AsyncSessionTyping,
            chat_id: int,
            username: str,
            first_name: str,
            last_name: str,
            tg_bot_id: int,
            ref_chat_id: Optional[int] = None,
            ref_tg_bot_id: Optional[int] = None,
    ) -> Customer:
        return await create_new(
            session, chat_id, username, first_name,
            last_name, tg_bot_id, ref_chat_id, ref_tg_bot_id
        )

    @classmethod
    async def check_availability(
            cls,
            session: AsyncSessionTyping,
            chat_id: int,
            bot_id: int,
    ) -> bool:
        return await check_availability(session, chat_id, bot_id)

    @classmethod
    async def get_balance(
            cls,
            session: AsyncSessionTyping,
            chat_id: int,
            bot_id: int
    ) -> MoneyUserInfo:
        return await get_balance(session, chat_id, bot_id)

    @classmethod
    async def get_static_info(
            cls,
            session: AsyncSessionTyping,
            chat_id: int,
            bot_id: int
    ) -> ProfileInfo:
        return await get_static_info(session, chat_id, bot_id)

    @classmethod
    async def update_user_balance(
            cls,
            session: AsyncSessionTyping,
            bot_id: int,
            chat_id: int,
            amount: float,
    ):
        await update_user_balance(
            session,
            bot_id,
            chat_id,
            amount
        )

    @classmethod
    async def operate_qiwi_payment(
            cls,
            session: AsyncSessionTyping,
            bot_id: int,
            comment: str,
            amount: float
    ) -> Optional[int]:
        """Возвращает id пользователя, к которому присвоили платеж"""
        return await operate_qiwi_payment(session, bot_id, comment, amount)
