from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.utils.auth import get_current_user

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/hi")
def root():
    return {"message": "Hello from FastAPI!"}

# Página de login
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/")
def dashboard(request: Request, user=Depends(get_current_user)):
    # el usuario viene desde el token
    roles = [r.name for r in user.roles]

    if "admin" in roles:
        return RedirectResponse("/dashboard/admin")

    if "conserje" in roles:
        return RedirectResponse("/dashboard/conserje")

    if "propietario" in roles:
        return RedirectResponse("/dashboard/propietario")

    if "inquilino" in roles:
        return RedirectResponse("/dashboard/inquilino")

    if "mesa_directiva" in roles:
        return RedirectResponse("/dashboard/mesa")

    # fallback
    return {"error": "Rol no reconocido"}
