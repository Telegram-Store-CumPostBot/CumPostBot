from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    BigInteger,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship

from database.engine import Base
from database.models.tables.admin import Admin


class TGBot(Base):
    __tablename__ = 'tg_bots'

    tg_bot_id: int = Column(BigInteger, primary_key=True, autoincrement=False)
    tg_token: int = Column(String(46), nullable=False)
    start_message: Optional[str] = Column(Text, nullable=True)
    qiwi_txn: Optional[int] = Column(BigInteger, nullable=True)

    admin_id: int = Column(Integer, nullable=True)
    admin = relationship('Admin', backref='tg_bots')

    __table_args__ = (
        ForeignKeyConstraint((admin_id,),
                             [Admin.chat_id]),
    )
