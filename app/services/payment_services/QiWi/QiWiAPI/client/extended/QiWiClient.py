from typing import Optional

from services.payment_services.QiWi.QiWiAPI.client.base.BaseQiWiClient import (
    BaseQiWiClient,
)
from services.payment_services.QiWi.QiWiAPI.methods.implementation.\
    GetNewPayments import GetNewPayments, NewTransactions


class QiWiClient(BaseQiWiClient):
    def __init__(
            self,
            api_access_token: str,
            phone_number: Optional[str] = None,
    ):
        super().__init__(api_access_token, phone_number)

    async def get_new_payments(
            self,
            last_processed_payment: int
    ) -> NewTransactions:
        method = GetNewPayments(
            self._request_service,
            last_processed_payment,
            self._phone_number_without_plus_sign
        )
        return await self.execute_method(method)

    @property
    def _phone_number_without_plus_sign(self) -> str:
        if self._phone_number is None:
            raise RuntimeError('Phone number is empty')
        return self._phone_number[1:]
