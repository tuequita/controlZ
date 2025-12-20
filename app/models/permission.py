from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.role_permission import role_permission
from .base import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    roles = relationship("Role", secondary="role_permission", back_populates="permissions")

    def __repr__(self):
        return f"<Permission(name={self.name})>"