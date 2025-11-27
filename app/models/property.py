from sqlalchemy import Column, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=True)
    code = Column(String(50), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    #payments = relationship('Payment', back_populates='property')
    property_links = relationship("PropertyUsers", back_populates="property")
    @property
    def users(self):
        from .property_users import PropertyUsers  # import local aquí
        return [link.user for link in self.property_links]

    def __repr__(self):
        return f"<Property(name={self.name}, code={self.code})>"
