from sqlalchemy import Column, Integer, ForeignKey, Index, BigInteger
from sqlalchemy.orm import relationship

from database.engine import Base


class SubAdmin(Base):
    __tablename__ = 'sub_admins'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    chat_id: int = Column(BigInteger, nullable=False)

    tg_bot_id: int = Column(Integer, ForeignKey('tg_bots.tg_bot_id'))
    tg_bot = relationship('TGBot', backref='sub_admins')

    __table_args__ = (
        Index('idx_ch_tg_id', chat_id, tg_bot_id, porstgresql_using='btree'),
    )
