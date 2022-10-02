from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    BigInteger,
    ForeignKeyConstraint
)
from sqlalchemy.orm import relationship

from database.engine import Base
from database.models.tables.admin import Admin
from database.models.tables.product_version import ProductVersion


class Product(Base):
    __tablename__ = 'products'

    product_id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(30), nullable=False)
    photo_file: Optional[str] = Column(String(255), nullable=True)
    count: int = Column(Integer, nullable=False, default=0)

    current_version_id = Column(Integer)

    admin_id: int = Column(BigInteger, index=True)
    admin = relationship(Admin.__name__, backref='products')

    __table_args__ = (
        ForeignKeyConstraint((admin_id,),
                             [Admin.chat_id]),
        ForeignKeyConstraint((current_version_id,),
                             [ProductVersion.pv_id]),
    )
