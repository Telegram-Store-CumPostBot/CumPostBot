from typing import Optional

from sqlalchemy import Column, Integer, String, Text, ForeignKey

from database.connection import Base


class TGBot(Base):
    __tablename__ = 'tg_bots'

    tg_bot_id: int = Column(Integer, primary_key=True, autoincrement=False)
    tg_token: int = Column(String(46), nullable=False)
    start_message: Optional[str] = Column(Text, nullable=True)
    qiwi_txn: Optional[int] = Column(Integer, nullable=True)

    admin_id: int = Column(Integer, ForeignKey('admins.admin_id'))
