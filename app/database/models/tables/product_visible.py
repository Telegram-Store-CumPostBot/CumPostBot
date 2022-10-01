from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.engine import Base


class ProductVisible(Base):
    __tablename__ = 'product_visible'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    visible: bool = Column(Boolean, nullable=False)

    tg_bot_id: int = Column(Integer, ForeignKey('tg_bots.tg_bot_id'))
    tg_bot = relationship('TGBot', backref='products_visible')

    product_id: int = Column(Integer, ForeignKey('products.product_id'))
    product = relationship('Product', backref='visible')
