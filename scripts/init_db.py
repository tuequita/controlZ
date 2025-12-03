from sqlalchemy.orm import Session
from app.config.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.building import Building
from app.models.property import Property
from app.models.property_users import PropertyUsers

from passlib.context import CryptContext
import random
import string
from datetime import datetime

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes)

# ---------------------------------------------------------
# GENERADORES AUXILIARES
# ---------------------------------------------------------

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@demo.com"

def random_username():
    return ''.join(random.choices(string.ascii_lowercase, k=8))

def create_property_name(floor, letter):
    return f"{floor}{letter}"

# ---------------------------------------------------------
# SEED PRINCIPAL
# ---------------------------------------------------------

def init_db():
    print("🧨 Eliminando tablas anteriores...")
    Base.metadata.drop_all(bind=engine)

    print("🛠️ Creando tablas...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    # ---------------------------------------------------------
    # ROLES
    # ---------------------------------------------------------
    print("➕ Insertando roles...")
    roles = [
        Role(name="admin"),
        Role(name="mesa_directiva"),
        Role(name="propietario"),
        Role(name="inquilino"),
        Role(name="conserje"),
    ]
    db.add_all(roles)

    # ---------------------------------------------------------
    # PERMISOS
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # EDIFICIO
    # ---------------------------------------------------------
    print("🏢 Creando edificio Torre Z...")

    building = Building(
        name="Torre Z",
        address="Carrer Lope de Vega 25, Poblenou, Barcelona",
        code="TZ-001",
        created_at=datetime.utcnow()
    )
    db.add(building)
    db.commit()

    # ---------------------------------------------------------
    # DEPARTAMENTOS
    # ---------------------------------------------------------
    print("🏠 Generando departamentos...")

    letters = list("ABCDEFGHIJ")
    properties = []

    property_count = 0

    for floor in range(1, 15):  # pisos 1 → 14
        for letter in letters:
            # Piso 14 solo tiene 8 departamentos → A a H
            if floor == 14 and letter in ["I", "J"]:
                continue

            unit = Property(
                name=create_property_name(floor, letter),
                area_m2=random.choice([60, 70, 80, 85, 90]),
                bedrooms=random.choice([1, 2, 3]),
                description="Unidad generada para demo",
                code=f"DPT-{floor}{letter}",
                building_id=building.id
            )
            db.add(unit)
            properties.append(unit)
            property_count += 1

    db.commit()
    print(f"🏠 Total departamentos creados: {property_count}")

    # ---------------------------------------------------------
    # USUARIOS ESPECIALES
    # ---------------------------------------------------------

    print("👤 Creando usuarios administradores...")
    admins = []
    for i in range(3):
        u = User(
            username=f"admin{i}",
            email=f"admin{i}@controlz.com",
            password_hash=hash_password("123")
        )
        u.roles.append(db.query(Role).filter_by(name="admin").first())
        admins.append(u)
        db.add(u)

    print("👤 Creando mesa directiva...")
    mesa = []
    for i in range(5):
        u = User(
            username=f"mesa{i}",
            email=f"mesa{i}@controlz.com",
            password_hash=hash_password("123")
        )
        u.roles.append(db.query(Role).filter_by(name="mesa_directiva").first())
        mesa.append(u)
        db.add(u)

    print("👤 Creando conserjes...")
    cons = []
    for i in range(3):
        u = User(
            username=f"cons{i}",
            email=f"cons{i}@controlz.com",
            password_hash=hash_password("123")
        )
        u.roles.append(db.query(Role).filter_by(name="conserje").first())
        cons.append(u)
        db.add(u)

    db.commit()

    # ---------------------------------------------------------
    # USUARIOS GENERALES (~400)
    # ---------------------------------------------------------
    print("👥 Creando 400 usuarios...")

    all_users = []
    propietario_role = db.query(Role).filter_by(name="propietario").first()
    inquilino_role = db.query(Role).filter_by(name="inquilino").first()

    for i in range(400):
        username = random_username()
        user = User(
            username=username,
            email=random_email(),
            password_hash=hash_password("123")
        )
        # Asignación aleatoria de rol general
        user.roles.append(random.choice([propietario_role, inquilino_role]))
        db.add(user)
        all_users.append(user)

    db.commit()

    # ---------------------------------------------------------
    # ASIGNAR USUARIOS A PROPIEDADES
    # ---------------------------------------------------------
    print("🔗 Asignando usuarios a propiedades...")

    all_users_db = db.query(User).all()
    all_properties_db = db.query(Property).all()

    # Tomamos solo usuarios propietarios e inquilinos
    propietarios_list = [u for u in all_users_db if any(r.name == "propietario" for r in u.roles)]
    inquilinos_list = [u for u in all_users_db if any(r.name == "inquilino" for r in u.roles)]

    random.shuffle(propietarios_list)
    random.shuffle(inquilinos_list)

    # 100 departamentos tendrán propietario
    for i, prop in enumerate(all_properties_db[:100]):
        owner = propietarios_list[i]
        link = PropertyUsers(
            user_id=owner.id,
            property_id=prop.id,
            role="owner"
        )
        db.add(link)

        # La mitad tendrá además inquilino
        if i % 2 == 0 and len(inquilinos_list) > i:
            tenant = inquilinos_list[i]
            link2 = PropertyUsers(
                user_id=tenant.id,
                property_id=prop.id,
                role="tenant"
            )
            db.add(link2)

    db.commit()

    print("✅ DEMO COMPLETA: edificio, departamentos, usuarios y relaciones cargadas.")
    db.close()

# ---------------------------------------------------------
# EJECUTAR SEED
# ---------------------------------------------------------

if __name__ == "__main__":
    init_db()
