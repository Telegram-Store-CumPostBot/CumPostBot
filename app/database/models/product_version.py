from typing import Optional, ForwardRef

from ormar import Model, Integer, Float, Text, ForeignKey
from database.connection import BaseMeta


ProductRef = ForwardRef("Product")


class ProductVersion(Model):
    class Meta(BaseMeta):
        tablename = "product_versions"

    id: int = Integer(primary_key=True)
    price: float = Float(nullable=False)
    old_price: float = Float(nullable=True)
    description: str = Text(nullable=False)
    extended_description: str = Text(nullable=False)

    product: Optional[ProductRef] = ForeignKey(ProductRef)
