from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from fastapi import APIRouter, HTTPException, Depends, Body
from app.config.database import SessionLocal
from app.schemas.user_schema import UserCreate, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.utils.auth import create_access_token
from app.config.database import get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")

    user = db.query(User).filter(User.email == email).first()
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    
    role = user.roles[0].name if user.roles else "usuario"
    token = create_access_token({
        "sub": user.email,
        "role": role
    })

    # Devolver token en cookie HttpOnly (protegida) y JSON con meta (role, username)
    response = JSONResponse({
        "message": "Login exitoso",
        "role": role,
        "username": user.username
    })
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,      # preferible True por seguridad
        secure=False,       # en localhost False; en producción pon True
        samesite="lax",     # permite navegacion normal y proteccion CSRF basica
        max_age=60*60*24,   # 1 día
        path="/"
    )
    return response

@router.get("/me")
def me(user = Depends(get_current_user)):
    return {"username": user.username, "email": user.email, "roles": [r.name for r in user.roles]}


@router.post("/create", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
