from fastapi import FastAPI
from app.api import routes_users, routes_pages
from fastapi.staticfiles import StaticFiles
from app.models.base import Base
from app.config.database import engine
from app.models.permission import Permission
from app.models.user import User
from app.models.role import Role

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TorreZ")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(routes_users.router, prefix="/api")  # JSON API
app.include_router(routes_pages.router)                 # Páginas HTML

