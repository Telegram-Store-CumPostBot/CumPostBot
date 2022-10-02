from database.engine import async_session
from database.models.api.customer import DBAPICustomer
from database.models.api.qiwi_payroll import DBAPIQiWiPayroll
from database.models.api.tg_bot import DBAPITGBot
from services.abstract.payment_service import PaymentService
from services.payment_services.QiWi.QiWiAPI.client.extended.QiWiClient import (
    QiWiClient,
)


class QiWiPaymentService(PaymentService):
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

    async def check_new_payments(self):
        qiwi_txn = await DBAPITGBot.get_qiwi_txn(self._tg_bot_id)
        res = await self._qiwi_api.get_new_payments(
            qiwi_txn
        )
        new_trans, new_qiwi_txn = res.transactions, res.last_processed_payment

        print(new_trans)
        async with async_session() as session:
            for trans in new_trans:
                user_id = await DBAPICustomer.operate_qiwi_payment(
                    session,
                    self._tg_bot_id,
                    trans.comment,
                    trans.sum.amount,
                )
                if not user_id:
                    continue
                await DBAPIQiWiPayroll.create_new(
                    session,
                    trans.id,
                    trans.date,
                    trans.comment,
                    trans.sum.amount,
                    trans.sum.amount // 100 + 1,
                    user_id
                )
            # if qiwi_txn != new_qiwi_txn:
            #     await DBAPITGBot.set_qiwi_txn(self._tg_bot_id, new_qiwi_txn)
            await session.commit()
        return None

    def __repr__(self):
        return 'no implemented repr QiWiPaymentService'
