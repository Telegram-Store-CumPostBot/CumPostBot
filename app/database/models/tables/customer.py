from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    text,
    BigInteger, PrimaryKeyConstraint, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship

from database.engine import Base
from database.models.helpers.transform_tg_id import transform_tg_id
from database.models.tables.tg_bot import TGBot


def default_tg_id(column_name: str):
    def tg_id(context):
        return transform_tg_id(context.get_current_parameters()[column_name])
    return tg_id


class Customer(Base):
    __tablename__ = 'customers'

    chat_id: int = Column(BigInteger, nullable=False)
    balance: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False,
        server_default=text('0')
    )
    fake_bal: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False,
        server_default=text('0')
    )
    sum_orders: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False,
        server_default=text('0')
    )
    ref_count: int = Column(Integer, nullable=False, server_default=text('0'))
    ref_fees: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False,
        server_default=text('0')
    )
    username: str = Column(String(32))
    first_name: str = Column(String(64))
    last_name: str = Column(String(64))

    qiwi_chat_id: int = Column(
        BigInteger, nullable=False, default=default_tg_id('chat_id')
    )
    qiwi_tg_bot_id: int = Column(
        BigInteger, nullable=False, default=default_tg_id('tg_bot_id')
    )

    ref_chat_id: Optional[int] = Column(BigInteger, nullable=True)
    ref_tg_bot_id: Optional[int] = Column(BigInteger, nullable=True)
    referrals = relationship('Customer')

    tg_bot_id: int = Column(BigInteger)
    tg_bot = relationship(TGBot.__name__, backref='customers')

    __table_args__ = (
        PrimaryKeyConstraint(chat_id, tg_bot_id),
        ForeignKeyConstraint((tg_bot_id,),
                             [TGBot.tg_bot_id]),
        ForeignKeyConstraint((ref_chat_id, ref_tg_bot_id),
                             [chat_id, tg_bot_id]),
    )

    def __repr__(self):
        return f'chat_id = {self.chat_id}, username = {self.username},\
                 tg_bot_id = {self.tg_bot_id}: balance={self.balance} '
