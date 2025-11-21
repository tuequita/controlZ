from sqlalchemy.orm import Session
from app.config.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    """Trunca a 72 bytes y genera el hash con bcrypt."""
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes)

def init_db():
    print("🧨 Eliminando tablas anteriores...")
    Base.metadata.drop_all(bind=engine)

    print("🛠️ Creando tablas...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    print("➕ Insertando roles...")
    roles = [
        Role(name="admin"),
        Role(name="mesa_directiva"),
        Role(name="propietario"),
        Role(name="inquilino"),
        Role(name="conserje"),
    ]
    db.add_all(roles)

    print("➕ Insertando permisos...")
    permissions = [
        Permission(name="user:create"),
        Permission(name="user:update"),
        Permission(name="user:delete"),
        Permission(name="role:create"),
        Permission(name="role:update"),
        Permission(name="role:delete"),
    ]
    db.add_all(permissions)
    db.commit()

    print("👤 Creando usuarios de prueba...")
    test_users = [
        {"username": "admin", "email": "admin@controlz.com", "roles": ["admin"]},
        {"username": "mesa1", "email": "mesa1@controlz.com", "roles": ["mesa_directiva"]},
        {"username": "prop1", "email": "prop1@controlz.com", "roles": ["propietario"]},
        {"username": "inq1", "email": "inq1@controlz.com", "roles": ["inquilino"]},
        {"username": "cons1", "email": "cons1@controlz.com", "roles": ["conserje"]},
    ]

    for u in test_users:
        user_obj = User(
            username=u["username"],
            email=u["email"],
            password_hash=hash_password("123")  # aquí se trunca y hashea
        )
        for role_name in u["roles"]:
            role_obj = db.query(Role).filter_by(name=role_name).first()
            user_obj.roles.append(role_obj)
        db.add(user_obj)

    db.commit()
    db.close()

    print("✅ Base de datos lista.")


if __name__ == "__main__":
    init_db()
