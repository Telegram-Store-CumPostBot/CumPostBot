from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database.engine import Base


class Product(Base):
    __tablename__ = 'products'

    product_id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(30), nullable=False)
    photo_file: Optional[str] = Column(String(255), nullable=True)
    count: int = Column(Integer, nullable=False, default=0)

    current_version_id = Column(
        Integer,
        ForeignKey('product_versions.pv_id')
    )
    admin_id: int = Column(
        BigInteger,
        ForeignKey('admins.chat_id'),
        index=True
    )
    admin = relationship('Admin', backref='products')
