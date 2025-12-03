from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)  # Nombre del edificio
    address = Column(String(255), nullable=False)  # Dirección completa
    code = Column(String(50), unique=True, nullable=True)  # Código interno (ej: LV-001)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con unidades (departamentos)
    units = relationship("Property", back_populates="building")

    def __repr__(self):
        return f"<Building(name={self.name}, address={self.address})>"
