from typing import NamedTuple

from glQiwiApi.qiwi.clients.wallet.types import Transaction


class NewTransactions(NamedTuple):
    transactions: list[Transaction]
    last_processed_payment: int


def one_run(func):
    async def wrapper(self, *args, **kwargs):
        if self.__runs:
            return None
        self.__runs = True
        res = await func(self, *args, **kwargs)
        self.__runs = False
        return res
    return wrapper
