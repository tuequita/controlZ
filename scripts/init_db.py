from sqlalchemy.orm import Session
from app.config.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    print("🛠️ Creando tablas en MySQL...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    # Verificar si ya hay roles
    if db.query(Role).count() == 0:

        # 1️⃣ Crear roles base
        roles = [
            Role(name="admin", description="Administrador del sistema"),
            Role(name="mesa_directiva", description="Miembro de la mesa directiva"),
            Role(name="propietario", description="Propietario de un departamento"),
            Role(name="inquilino", description="Inquilino"),
            Role(name="conserje", description="Encargado del edificio"),
        ]
        db.add_all(roles)

        # 2️⃣ Crear permisos base
        permissions = [
            Permission(name="user:create", description="Crear usuario"),
            Permission(name="user:update", description="Actualizar usuario"),
            Permission(name="user:delete", description="Eliminar usuario"),
            Permission(name="role:create", description="Crear rol"),
            Permission(name="role:update", description="Actualizar rol"),
            Permission(name="role:delete", description="Eliminar rol"),
        ]
        db.add_all(permissions)
        db.commit()

        # 3️⃣ Asignar permisos al rol admin
        # admin_role = db.query(Role).filter_by(name="admin").first()
        # admin_role.permissions = db.query(Permission).all()
        # db.commit()

        # 4️⃣ Crear usuarios de prueba para cada rol
        test_users = [
            {"username": "admin", "email": "admin@controlz.com", "roles": ["admin"]},
            {"username": "mesa1", "email": "mesa1@controlz.com", "roles": ["mesa_directiva"]},
            {"username": "propietario1", "email": "propietario1@controlz.com", "roles": ["propietario"]},
            {"username": "inquilino1", "email": "inquilino1@controlz.com", "roles": ["inquilino"]},
            {"username": "conserje1", "email": "conserje1@torrez.com", "roles": ["conserje"]},
        ]

        for u in test_users:
            user_obj = User(
                username=u["username"],
                email=u["email"],
                password_hash=pwd_context.hash("123")
            )
            # Asignar roles al usuario
            for role_name in u["roles"]:
                role_obj = db.query(Role).filter_by(name=role_name).first()
                if role_obj:
                    user_obj.roles.append(role_obj)
            db.add(user_obj)

        db.commit()

        print("✅ Base de datos inicializada con roles, permisos y usuarios de prueba.")

    else:
        print("⚠️ La base de datos ya contiene datos. No se reinicia.")

    db.close()

if __name__ == "__main__":
    init_db()
