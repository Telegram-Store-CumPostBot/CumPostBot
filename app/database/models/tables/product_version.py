from typing import Optional

from ormar import Integer
from sqlalchemy import Column, Text, Float, ForeignKey

from database.engine import Base


class ProductVersion(Base):
    __tablename__ = 'product_versions'

    pv_id: int = Column(Integer, primary_key=True, autoincrement=True)
    price: float = Column(Float, nullable=False)
    old_price: Optional[float] = Column(Float, nullable=True)
    description: str = Column(Text, nullable=False)
    extended_description: str = Column(Text, nullable=False)

    product_id: int = Column(Integer, ForeignKey('products.product_id'))
