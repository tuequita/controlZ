from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, DateTime, Text
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class PaymentPart(Base):
    __tablename__ = 'payment_parts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(Integer, ForeignKey('payments.id'), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    paid_at = Column(DateTime, default=datetime.utcnow)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    payment = relationship('Payment', back_populates='parts')
