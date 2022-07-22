from typing import Optional

from ormar import Model, Integer, Text, ForeignKey, Float
from database.connection import BaseMeta
from database.models.product import Product


class Item(Model):
    class Meta(BaseMeta):
        tablename = "items"

    id: int = Integer(primary_key=True)
    product_line: str = Text()
    cost_price: float = Float(nullable=False, default=0)

    product: Optional[Product] = ForeignKey(Product)
