from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from app.utils.auth import get_current_user

router = APIRouter(prefix="/dashboard/admin")
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def admin_dashboard(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("dash_admin.html", {
        "request": request,
        "user": user,
    })