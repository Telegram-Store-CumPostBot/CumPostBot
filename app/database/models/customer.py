from typing import Optional, ForwardRef

from ormar import Model, Integer, ForeignKey, Float, String, IndexColumns
from database.connection import BaseMeta
from database.models.tg_bot import TGBot
from settings.settings import config

CustomerRef = ForwardRef("Customer")


class Customer(Model):
    class Meta(BaseMeta):
        tablename = "customers"
        constraints = [IndexColumns('chat_id', postgresql_using='btree')]

    id: int = Integer(primary_key=True)
    balance: float = Float(nullable=False, default=0)
    fake_balance: float = Float(nullable=False, default=0)
    chat_id = Integer(nullable=False)
    sum_orders: float = Float(nullable=False, default=0)
    username: str = String(max_length=32)
    first_name: str = String(max_length=64)
    last_name: str = String(max_length=64)

    refer: Optional[CustomerRef] = ForeignKey(CustomerRef, related_name="referes")
    tg_bot: Optional[TGBot] = ForeignKey(TGBot, related_name="tg_bots")


Customer.update_forward_refs()
