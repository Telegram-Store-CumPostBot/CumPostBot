from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    text,
    UniqueConstraint,
    BigInteger
)
from sqlalchemy.orm import relationship

from database.engine import Base


class Customer(Base):
    __tablename__ = 'customers'

    customer_id: int = Column(Integer, primary_key=True, autoincrement=True)
    balance: float = Column(Float, nullable=False, server_default=text('0'))
    fake_bal: float = Column(Float, nullable=False, server_default=text('0'))
    chat_id: int = Column(Integer, nullable=False)
    sum_orders: float = Column(Float, nullable=False, server_default=text('0'))
    ref_count: int = Column(Integer, nullable=False, server_default=text('0'))
    ref_fees: float = Column(Float, nullable=False, server_default=text('0'))
    username: str = Column(String(32))
    first_name: str = Column(String(64))
    last_name: str = Column(String(64))

    ref_key = 'customers.customer_id'
    ref_customer_id: Optional[int] = Column(Integer, ForeignKey(ref_key))
    referrals: Optional[int] = relationship('Customer')

    tg_bot_id: int = Column(BigInteger, ForeignKey('tg_bots.tg_bot_id'))

    __table_args__ = (
        UniqueConstraint(chat_id, tg_bot_id, name='idx_chat_id_tg_bot_id'),
    )

    def __repr__(self):
        return f'chat_id = {self.chat_id}, username = {self.username},\
                 tg_bot_id = {self.tg_bot_id}: balance={self.balance} '
