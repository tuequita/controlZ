from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.utils.auth import get_user_from_request, get_current_user
from app.config.database import get_db
from sqlalchemy.orm import Session

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
def default_page(request: Request, db: Session = Depends(get_db)):
    user = get_user_from_request(request, db)

    if not user:
        return RedirectResponse("/login", status_code=302)

    return RedirectResponse("/dashboard", status_code=302)

@router.get("/dashboard")
def dashboard(request: Request, user=Depends(get_current_user)):
    if not any(role.name == "admin" for role in user.roles):
        raise HTTPException(status_code=403, detail="Acceso restringido a administradores")

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
    })

@router.get("/payments/new")
def payment_new(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("new_payment.html", {
        "request": request,
        "user": user,
        "properties": [
            {"id": 1, "name": "Dpto 101"},
            {"id": 2, "name": "Dpto 102"},
        ]
    })
