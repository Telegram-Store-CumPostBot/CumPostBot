from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.engine import Base

utcnow = datetime.utcnow


class QiwiPayroll(Base):
    __tablename__ = 'qiwi_payrolls'

    txn_id: int = Column(Integer, primary_key=True, autoincrement=False)
    check_date: datetime = Column(DateTime, nullable=False, default=utcnow)
    qiwi_date: datetime = Column(DateTime, nullable=False)
    comment: str = Column(String(255), nullable=False)
    amount: float = Column(Float, nullable=False)
    commission: float = Column(Float, nullable=False)

    customer_id: int = Column(Integer, ForeignKey('customers.customer_id'))
    customer = relationship('Customer', backref='qiwi_payrolls')

    def __repr__(self):
        return f'user={self.customer_id}, amount={self.amount}'
