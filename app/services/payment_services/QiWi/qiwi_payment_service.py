from database.models.api.tg_bot import DBAPITGBot
from services.abstract.payment_service import PaymentService
from services.payment_services.QiWi.QiWiAPI.client.extended.QiWiClient import (
    QiWiClient,
)


# TODO:  check_new_payments
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
        new_trans, new_qiwi_txn = await self._qiwi_api.get_new_payments(
            qiwi_txn
        )
        if qiwi_txn != new_qiwi_txn:
            await DBAPITGBot.set_qiwi_txn(self._tg_bot_id, new_qiwi_txn)

    def __repr__(self):
        return 'no implemented repr QiWiPaymentService'
