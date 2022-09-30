from sqlalchemy import Column, Integer, ForeignKey, Index

from database.engine import Base


class SubAdmin(Base):
    __tablename__ = 'sub_admins'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    chat_id: int = Column(Integer, nullable=False)

    tg_bot_id: int = Column(Integer, ForeignKey('tg_bots.tg_bot_id'))

    __table_args__ = (
        Index('idx_ch_tg_id', chat_id, tg_bot_id, porstgresql_using='btree'),
    )
