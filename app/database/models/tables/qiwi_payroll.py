from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    String,
    Float,
    BigInteger,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship

from database.engine import Base
from database.models.tables.customer import Customer

utcnow = datetime.utcnow


class QiWiPayroll(Base):
    __tablename__ = 'qiwi_payrolls'

    txn_id: int = Column(BigInteger, primary_key=True, autoincrement=False)
    check_date: datetime = Column(DateTime, nullable=False, default=utcnow)
    qiwi_date: datetime = Column(DateTime, nullable=False)
    comment: str = Column(String(255), nullable=False)
    amount: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False
    )
    commission: float = Column(
        Float(precision=7, decimal_return_scale=2),
        nullable=False
    )
    customer_chat_id: int = Column(BigInteger)
    customer_tg_bot_id: int = Column(BigInteger)
    customer = relationship(Customer.__name__, backref='qiwi_payrolls')

    __table_args__ = (
        ForeignKeyConstraint((customer_chat_id, customer_tg_bot_id),
                             [Customer.chat_id, Customer.tg_bot_id]),
    )

    def __repr__(self):
        return f'user={self.customer_id}, amount={self.amount}'
