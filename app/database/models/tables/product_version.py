from typing import Optional

from ormar import Integer
from sqlalchemy import Column, Text, Float, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from database.engine import Base
from database.models.tables.product import Product


class ProductVersion(Base):
    __tablename__ = 'product_versions'

    pv_id: int = Column(Integer, primary_key=True, autoincrement=True)
    price: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False
    )
    old_price: Optional[float] = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=True
    )
    description: str = Column(Text, nullable=False)
    extended_description: str = Column(Text, nullable=False)

    product_id: int = Column(Integer)
    product = relationship(Product.__name__, backref='versions')

    __table_args__ = (
        ForeignKeyConstraint((product_id,),
                             [Product.product_id]),
    )
