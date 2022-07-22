from typing import Optional

from ormar import Model, Integer, String, ForeignKey
from database.connection import BaseMeta
from database.models.admin import Admin
from database.models.product_version import ProductVersion


class Product(Model):
    class Meta(BaseMeta):
        tablename = "products"

    id: int = Integer(primary_key=True)
    name: str = String(max_length=30, nullable=False)
    photo_file: str = String(max_length=255, nullable=True)
    count: int = Integer(nullable=False, default=0)

    current_version: Optional[ProductVersion] = ForeignKey(ProductVersion)
    admin: Optional[Admin] = ForeignKey(Admin)
