from sqlalchemy import Index, Integer, Column, Float, text, BigInteger

from database.engine import Base


class Admin(Base):
    __tablename__ = 'admins'

    chat_id: int = Column(BigInteger, primary_key=True, nullable=False)
    debt: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False,
        server_default=text("0")
    )

    __table_args__ = (
        # Index('idx_chat_id', chat_id, porstgresql_using='btree'),
    )
