from sqlalchemy import Column, Integer, ForeignKey, Enum, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    paid_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recorded_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(Enum('pending', 'partial', 'paid', name='payment_status'), default='pending')

    total_amount = Column(DECIMAL(10, 2), nullable=False, default=0)
    due_amount = Column(DECIMAL(10, 2), nullable=False, default=0)
    remaining_amount = Column(DECIMAL(10, 2), nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    property = relationship('Property', back_populates='payments')
    paid_by = relationship('User', foreign_keys=[paid_by_user_id])
    recorded_by = relationship('User', foreign_keys=[recorded_by_user_id])
    parts = relationship('PaymentPart', back_populates='payment')
    files = relationship('PaymentFile', back_populates='payment')

    def __repr__(self):
        return f"<Payment(property={self.property_id}, month={self.month}, year={self.year})>"
