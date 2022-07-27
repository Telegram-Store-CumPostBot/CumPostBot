from typing import Optional, ForwardRef

from ormar import Model, Integer, ForeignKey, Float, String, IndexColumns
from database.connection import BaseMeta
from database.models.tg_bot import TGBot


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

    refer: Optional[CustomerRef] = ForeignKey(CustomerRef, related_name="referes")
    tg_bot: Optional[TGBot] = ForeignKey(TGBot, related_name="tg_bots")
