from sqlalchemy import Index, Integer, Column, Float, text

from database.engine import Base


class Admin(Base):
    __tablename__ = 'admins'

    admin_id: int = Column(Integer, primary_key=True, autoincrement=True)
    chat_id: int = Column(Integer, nullable=False)
    debt: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False,
        server_default=text("0")
    )

    __table_args__ = (
        Index('idx_chat_id', chat_id, porstgresql_using='btree'),
    )
