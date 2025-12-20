from fastapi import Request
from fastapi.templating import Jinja2Templates
from app.models.user import User

templates = Jinja2Templates(directory="app/templates")

def render(
    request: Request,
    template_name: str,
    *,
    user: User | None = None,
    context: dict | None = None
):
    ctx = {
        "request": request
    }

    if context:
        ctx.update(context)

    if user:
        ctx["user"] = user
        ctx["pages"] = user.dashboard_pages()

    return templates.TemplateResponse(template_name, ctx)
