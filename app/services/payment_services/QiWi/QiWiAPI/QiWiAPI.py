from typing import NamedTuple

from glQiwiApi.qiwi.clients.wallet.types import Transaction


class NewTransactions(NamedTuple):
    transactions: list[Transaction]
    last_processed_payment: int
