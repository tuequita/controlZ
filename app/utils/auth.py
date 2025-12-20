from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, Cookie, Header
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from fastapi import Request


auth_scheme = HTTPBearer()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def get_current_user(
    authorization: str | None = Header(None),
    access_token: str | None = Cookie(None),
    db: Session = Depends(get_db)
):
    token = None

    # 1) Si viene header Authorization: Bearer <token>
    if authorization:
        if authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
        else:
            # si Authorization existe pero no empieza con Bearer -> invalid
            raise HTTPException(status_code=401, detail="Not authenticated")

    # 2) Si no hay header, usar cookie (access_token)
    if not token and access_token:
        if access_token.startswith("Bearer "):
            token = access_token.replace("Bearer ", "")
        else:
            token = access_token

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
    except JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def get_user_from_request(request: Request, db: Session):
    """
    Devuelve el usuario autenticado o None.
    NO lanza excepción.
    """
    token = None

    # 1) Intentar leer header Authorization
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")

    # 2) Si no hay, intentar con cookie
    if not token:
        cookie_token = request.cookies.get("access_token")
        if cookie_token:
            if cookie_token.startswith("Bearer "):
                token = cookie_token.replace("Bearer ", "")
            else:
                token = cookie_token

    if not token:
        return None

    # 3) Intentar decodificar JWT
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if not email:
            return None
    except JWTError:
        return None

    # 4) Buscar user en DB
    user = db.query(User).filter(User.email == email).first()
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def require_permission(permission: str):
    def checker(user: User = Depends(get_current_user)):
        if not user.has_permission(permission):
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos suficientes"
            )
        return user
    return checker