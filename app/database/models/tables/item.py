from sqlalchemy import Column, Integer, Text, Float, text, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from database.engine import Base
from database.models.tables.product import Product


class Item(Base):
    __tablename__ = 'items'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    product_line: str = Column(Text, nullable=False)
    cost_price: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False,
        server_default=text('0')
    )

    product_id: int = Column(Integer, index=True)
    product = relationship(Product.__name__, backref='items')

    __table_args__ = (
        ForeignKeyConstraint((product_id,),
                             [Product.product_id]),
    )
