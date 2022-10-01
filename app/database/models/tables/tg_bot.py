from typing import Optional

from sqlalchemy import Column, Integer, String, Text, ForeignKey, BigInteger

from database.engine import Base


class TGBot(Base):
    __tablename__ = 'tg_bots'

    tg_bot_id: int = Column(BigInteger, primary_key=True, autoincrement=False)
    tg_token: int = Column(String(46), nullable=False)
    start_message: Optional[str] = Column(Text, nullable=True)
    qiwi_txn: Optional[int] = Column(Integer, nullable=True)

    admin_id: int = Column(Integer, ForeignKey('admins.admin_id'))
