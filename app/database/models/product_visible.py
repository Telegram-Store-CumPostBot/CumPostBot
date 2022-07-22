from typing import Optional

from ormar import Model, Integer, Boolean, ForeignKey
from database.connection import BaseMeta
from database.models.product import Product
from database.models.tg_bot import TGBot


class ProductVisible(Model):
    class Meta(BaseMeta):
        tablename = "product_visible"

    id: int = Integer(primary_key=True)
    visible: bool = Boolean(nullable=False)

    tg_bot: Optional[TGBot] = ForeignKey(TGBot)
    product: Optional[Product] = ForeignKey(Product)
