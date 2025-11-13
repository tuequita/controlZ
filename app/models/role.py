from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.user_role import user_role
from app.models.role_permission import role_permission
from .base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    users = relationship("User", secondary="user_role", back_populates="roles")
    permissions = relationship("Permission", secondary="role_permission", back_populates="roles")

    def __repr__(self):
        return f"<Role(name={self.name})>"
