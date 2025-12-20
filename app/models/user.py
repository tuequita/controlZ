from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base
from app.models.user_role import user_role
from passlib.context import CryptContext
from app.core.dashboard import DASHBOARD_PAGES, ROLE_DASHBOARD_PAGES

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    roles = relationship('Role', secondary=user_role, back_populates='users')
    
    property_links = relationship("PropertyUsers", back_populates="user")

    @property
    def properties(self):
        from .property_users import PropertyUsers  # import local
        return [link.property for link in self.property_links]

    def __repr__(self):
        return f"<User(username={self.username})>"
    
    def can(self, permission_name: str) -> bool:
        # Si tiene rol admin, siempre True
        if any(role.name == "admin" for role in self.roles):
            return True
        # Sino, revisa sus permisos asignados
        for role in self.roles:
            if any(perm.name == permission_name for perm in role.permissions):
                return True
        return False
    
    def verify_password(self, password: str) -> bool:
        """Verifica si la contraseña proporcionada coincide con la almacenada"""
        return pwd_context.verify(password, self.password_hash)
    
    def dashboard_pages(self):
        pages = set()

        for role in self.roles:
            role_pages = ROLE_DASHBOARD_PAGES.get(role.name, set())
            pages.update(role_pages)

        # Devuelve objetos DashboardPage
        return [DASHBOARD_PAGES[key] for key in pages]