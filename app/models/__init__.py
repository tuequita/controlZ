from .user import User
from .property import Property
from .property_users import PropertyUsers
from sqlalchemy.orm import relationship


# Ahora que todas las clases existen, podemos definir las relaciones
User.property_links = relationship("PropertyUsers", back_populates="user")
Property.property_links = relationship("PropertyUsers", back_populates="property")
PropertyUsers.user = relationship("User", back_populates="property_links")
PropertyUsers.property = relationship("Property", back_populates="property_links")
