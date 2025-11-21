from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from fastapi import APIRouter, HTTPException, Depends

from app.config.database import SessionLocal
from app.schemas.user_schema import UserCreate, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth import create_access_token
from fastapi import Body
from app.config.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")

    user = db.query(User).filter(User.email == email).first()
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/create", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
