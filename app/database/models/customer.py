from typing import Optional

from ormar import Model, Integer, ForeignKey, Float
from database.connection import BaseMeta
from database.models.tg_bot import TGBot


# TODO найти способ без повторного объявления класса
class Customer:
    pass


class Customer(Model):
    class Meta(BaseMeta):
        tablename = "customers"

    id: int = Integer(primary_key=True)
    balance: float = Float(nullable=False, default=0)
    fake_balance: float = Float(nullable=False, default=0)
    chat_id = Integer(nullable=False)
    sum_orders: float = Float(nullable=False, default=0)

    refer: Optional[Customer] = ForeignKey(Customer)
    tg_bot: Optional[TGBot] = ForeignKey(TGBot)
