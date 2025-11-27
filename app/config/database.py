from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.core.config import settings

# Conexión a MySQL usando DATABASE_URL de tu config
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,       # muestra queries para debug
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
