from typing import Optional

from ormar import NoMatch

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
            refer_id: Optional[int] = None,
            bot_id: Optional[int] = None,
    ) -> Customer:
        return await create_new(
            session, chat_id, username, first_name, last_name, refer_id, bot_id
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
    async def find_customer_by_qiwi_comment(cls, qiwi_comment: str) -> Optional[Customer]:
        if not qiwi_comment.isdigit():
            return None
        try:
            return await Customer.objects.get(
                Customer.customer_id == int(qiwi_comment)
            )
        except NoMatch:
            return None

    @classmethod
    async def update_balance_by_qiwi_comment(
            cls, qiwi_comment: str,
            amount: int
    ):
        if not qiwi_comment.isdigit():
            return None
        chat_id = int(qiwi_comment)
        await Customer.objects.filter(
            chat_id=chat_id
        ).update({
            Customer.balance: Customer.balance+amount
        })
