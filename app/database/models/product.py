from typing import Optional, ForwardRef

from ormar import Model, Integer, String, ForeignKey, Float, Text
from database.connection import BaseMeta
from database.models.admin import Admin


ProductRef = ForwardRef("Product")
ProductVersionRef = ForwardRef("ProductVersion")


class Product(Model):
    class Meta(BaseMeta):
        tablename = "products"

    id: int = Integer(primary_key=True)
    name: str = String(max_length=30, nullable=False)
    photo_file: str = String(max_length=255, nullable=True)
    count: int = Integer(nullable=False, default=0)

    current_version: Optional[ProductVersionRef] = ForeignKey(ProductVersionRef, related_name="current_versions")
    admin: Optional[Admin] = ForeignKey(Admin)


class ProductVersion(Model):
    class Meta(BaseMeta):
        tablename = "product_versions"

    id: int = Integer(primary_key=True)
    price: float = Float(nullable=False)
    old_price: float = Float(nullable=True)
    description: str = Text(nullable=False)
    extended_description: str = Text(nullable=False)

    product: Optional[Product] = ForeignKey(Product, related_name="products", nullable=False)


Product.update_forward_refs()
ProductVersion.update_forward_refs()
