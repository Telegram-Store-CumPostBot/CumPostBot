from sqlalchemy import Column, Integer, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from database.engine import Base
from database.models.tables.product import Product
from database.models.tables.tg_bot import TGBot


class ProductVisible(Base):
    __tablename__ = 'product_visible'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    visible: bool = Column(Boolean, nullable=False)

    tg_bot_id: int = Column(Integer)
    tg_bot = relationship('TGBot', backref='products_visible')

    product_id: int = Column(Integer)
    product = relationship('Product', backref='visible')

    __table_args__ = (
        ForeignKeyConstraint((tg_bot_id,),
                             [TGBot.tg_bot_id]),
        ForeignKeyConstraint((product_id,),
                             [Product.product_id])
    )
