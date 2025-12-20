from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.utils.auth import get_user_from_request, get_current_user, require_permission
from app.config.database import get_db
from app.models.user import User
from sqlalchemy.orm import Session
from app.core.render import render
from datetime import datetime

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
def dashboard(
    request: Request,
    user=Depends(get_current_user)
):
    return render(
        request,
        "dashboard.html",
        user=user
    )

@router.get("/payments/new")
def payment_new(
    request: Request,
    user=Depends(get_current_user)
):
    now = datetime.now()
    return render(
        request,
        "new_payment.html",
        user=user,
        context={
            "current_year": now.year,
            "current_month": now.month,
            "properties": [
                {"id": 1, "name": "Dpto 101"},
                {"id": 2, "name": "Dpto 102"},
            ]
        }
    )