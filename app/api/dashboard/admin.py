from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from app.utils.auth import get_current_user

router = APIRouter(prefix="/dashboard/admin")
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def admin_dashboard(request: Request, user=Depends(get_current_user)):
    if not any(role.name == "admin" for role in user.roles):
        raise HTTPException(status_code=403, detail="Acceso restringido a administradores")

    return templates.TemplateResponse("dash_admin.html", {
        "request": request,
        "user": user,
    })
