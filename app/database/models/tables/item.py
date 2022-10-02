from sqlalchemy import Column, Integer, Text, Float, text, ForeignKey
from sqlalchemy.orm import relationship

from database.engine import Base


class Item(Base):
    __tablename__ = 'items'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    product_line: str = Column(Text, nullable=False)
    cost_price: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False,
        server_default=text('0')
    )

    product_id: int = Column(
        Integer,
        ForeignKey('products.product_id'), index=True
    )
    product = relationship('Product', backref='items')
