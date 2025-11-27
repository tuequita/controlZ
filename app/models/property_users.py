from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class PropertyUsers(Base):
    __tablename__ = "property_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(Enum("owner", "tenant", name="property_user_roles"), default="owner")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='property_links')
    property = relationship('Property', back_populates='property_links')
