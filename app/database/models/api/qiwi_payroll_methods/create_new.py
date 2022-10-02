from datetime import datetime

from database.engine import AsyncSessionTyping
from database.models.tables.qiwi_payroll import QiWiPayroll
from logger import get_logger


async def create_new_qiwi_payroll(
        session: AsyncSessionTyping,
        txn_id: int,
        qiwi_date: datetime,
        comment: str,
        amount: float,
        commission: float,
        customer_chat_id: int,
        customer_tg_bot_id: int,
) -> QiWiPayroll:
    log = get_logger(__name__)
    log.info('txn_id=%d, comment=%s, amount=%f - start',
             txn_id, comment, amount)
    payroll = QiWiPayroll(
        txn_id=txn_id,
        qiwi_date=qiwi_date,
        comment=comment,
        amount=amount,
        commission=commission,
        customer_chat_id=customer_chat_id,
        customer_tg_bot_id=customer_tg_bot_id,
    )
    session.add(payroll)
    log.info('txn_id=%d, comment=%s, amount=%f - success add to session',
             txn_id, comment, amount)
    return payroll
