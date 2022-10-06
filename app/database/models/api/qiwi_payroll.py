from datetime import datetime

from database.engine import AsyncSessionTyping
from database.models.api.qiwi_payroll_methods.create_new import \
    create_new_qiwi_payroll
from database.models.tables.qiwi_payroll import QiWiPayroll


class DBAPIQiWiPayroll:
    @classmethod
    async def create_new(
            cls,
            session: AsyncSessionTyping,
            txn_id: int,
            qiwi_date: datetime,
            comment: str,
            amount: float,
            commission: float,
            customer_chat_id: int,
            customer_tg_bot_id: int,
    ) -> QiWiPayroll:
        qiwi_date = qiwi_date.replace(tzinfo=None)
        return await create_new_qiwi_payroll(
            session, txn_id, qiwi_date, comment, amount, commission,
            customer_chat_id, customer_tg_bot_id
        )
