import asyncio

from glQiwiApi.qiwi.clients.wallet.types import Transaction
from sqlalchemy.exc import IntegrityError

from database.engine import async_session
from database.models.api.customer import DBAPICustomer
from database.models.api.qiwi_payroll import DBAPIQiWiPayroll
from database.models.api.tg_bot import DBAPITGBot
from decorators.util_decorators.one_run_func import one_run
from errors.NoFoundUser import NoFoundUser
from logger import get_logger
from services.abstract.payment_service import PaymentService
from services.payment_services.QiWi.QiWiAPI.client.extended.QiWiClient import (
    QiWiClient,
)


class QiWiPaymentService(PaymentService):
    _implementations = {}

    def __init__(
            self,
            access_token: str,
            phone: str,
            tg_bot_id: int,
    ):
        self._access_token = access_token
        self._phone = phone
        self._tg_bot_id = tg_bot_id
        self._qiwi_api = QiWiClient(access_token, phone)

    def __new__(
            cls,
            access_token: str,
            phone: str,
            tg_bot_id: int,
    ):
        key = (access_token, phone, tg_bot_id)
        if not QiWiPaymentService._implementations.get(key):
            QiWiPaymentService._implementations[key] = super(
                QiWiPaymentService, cls
            ).__new__(cls, access_token, phone, tg_bot_id)
        return QiWiPaymentService._implementations[key]

    async def last_operate_payment(self) -> int:
        return await DBAPITGBot.get_qiwi_txn(self._tg_bot_id)

    @one_run
    async def check_new_payments(self):
        qiwi_txn = await self.last_operate_payment()
        res = await self._qiwi_api.get_new_payments(
            qiwi_txn
        )
        new_trans, new_qiwi_txn = res.transactions, res.last_processed_payment

        print(new_trans)
        tasks = [self._operate_one_payment(trans) for trans in new_trans]
        await asyncio.gather(*tasks)

        async with async_session() as session:
            async with session.begin():
                if qiwi_txn != new_qiwi_txn:
                    await DBAPITGBot.set_qiwi_txn(self._tg_bot_id,
                                                  new_qiwi_txn)
        return None

    async def _operate_one_payment(
            self,
            trans: Transaction
    ):
        log = get_logger(__name__)
        try:
            async with async_session() as session:
                async with session.begin():
                    chat_id = await DBAPICustomer.operate_qiwi_payment(
                        session,
                        self._tg_bot_id,
                        trans.comment,
                        trans.sum.amount,
                    )
                    if not chat_id:
                        raise NoFoundUser
                    await DBAPIQiWiPayroll.create_new(
                        session,
                        trans.id,
                        trans.date,
                        trans.comment,
                        trans.sum.amount,
                        trans.sum.amount // 100 + 1,
                        chat_id,
                        self._tg_bot_id,
                    )

        except IntegrityError:
            log.info('txn_id: %d, comment: %s, amount: %f - '
                     'try add duplicate trans',
                     trans.id, trans.comment, trans.sum.amount)
        except NoFoundUser:
            log.info('txn_id: %d, comment: %s, amount: %f - '
                     'incorrect comment (no found user with this comment)',
                     trans.id, trans.comment, trans.sum.amount)

    def __repr__(self):
        return 'no implemented repr QiWiPaymentService'
