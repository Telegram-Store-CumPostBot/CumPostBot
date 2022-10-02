from typing import NamedTuple, Optional

from glQiwiApi.core.request_service import RequestServiceProto
from glQiwiApi.qiwi.clients.wallet.methods.history import GetHistory
from glQiwiApi.qiwi.clients.wallet.types import (
    TransactionType,
    Transaction,
    History,
)

from services.payment_services.QiWi.QiWiAPI.\
    methods.abstract.BaseQiWiMethod import BaseQiWiMethod


class NewTransactions(NamedTuple):
    transactions: list[Transaction]
    last_processed_payment: Optional[int]


class GetNewPayments(BaseQiWiMethod):
    def __init__(
            self,
            request_service: RequestServiceProto,
            last_operate_payment: Optional[int],
            phone_number_without_plus_sign: str,
    ):
        self._request_service = request_service
        self._last_operate_payment = last_operate_payment
        self._phone_number_without_plus_sign = phone_number_without_plus_sign
        self._next_id = None
        self._next_date = None

    async def _work(self) -> NewTransactions:
        transactions = await self._get_transactions()
        if not transactions.transactions:
            return NewTransactions([], None)
        if not self._last_operate_payment:
            return NewTransactions([], transactions[0].id)
        new_transactions = []
        top_transaction_id = transactions[0].id
        while True:
            self._next_id = transactions.next_transaction_id
            self._next_date = transactions.next_transaction_date
            tmp_new_trans = filter(self.filter_comp, transactions)
            new_transactions.extend(tmp_new_trans)

            if self.stop_iterations:
                break
            transactions = await self._get_transactions()
            transactions = transactions.transactions

        return NewTransactions(new_transactions, top_transaction_id)

    async def _get_transactions(self) -> History:
        return await self._request_service.execute_api_method(
                GetHistory(
                    rows=50,
                    transaction_type=TransactionType.IN,
                    next_txn_id=self._next_id,
                    next_txn_date=self._next_date,
                ),
                phone_number=self._phone_number_without_plus_sign,
            )

    @property
    def stop_iterations(self) -> bool:
        return not self._next_id or self._next_id <= self._last_operate_payment

    def filter_comp(self, operation: Transaction) -> bool:
        return operation.id > self._last_operate_payment
