from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Nombre interno del departamento (ej: "6H", "4A")
    name = Column(String(50), nullable=False)

    # Metros cuadrados, habitaciones, nota, etc.
    area_m2 = Column(Integer, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)

    code = Column(String(50), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con edificio
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    building = relationship("Building", back_populates="units")

    # Si mantienes la tabla PropertyUsers para múltiples dueños
    property_links = relationship("PropertyUsers", back_populates="property")

    @property
    def users(self):
        return [link.user for link in self.property_links]

    def __repr__(self):
        return f"<Property(name={self.name}, building_id={self.building_id})>"