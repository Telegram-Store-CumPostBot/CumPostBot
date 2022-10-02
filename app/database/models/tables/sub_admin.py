from sqlalchemy import Column, ForeignKey, BigInteger, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from database.engine import Base


class SubAdmin(Base):
    __tablename__ = 'sub_admins'

    chat_id: int = Column(BigInteger, nullable=False)

    tg_bot_id: int = Column(BigInteger, ForeignKey('tg_bots.tg_bot_id'))
    tg_bot = relationship('TGBot', backref='sub_admins')

    __table_args__ = (
        PrimaryKeyConstraint(chat_id, tg_bot_id),
    )
