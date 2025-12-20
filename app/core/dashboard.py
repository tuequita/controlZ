from dataclasses import dataclass

@dataclass(frozen=True)
class DashboardPage:
    key: str
    label: str
    url: str
    icon: str

# app/core/dashboard.py

DASHBOARD_PAGES = {
    "manage_users": DashboardPage(
        key="manage_users",
        label="Gestión de Usuarios",
        url="/users",
        icon="👤"
    ),
    "manage_properties": DashboardPage(
        key="manage_properties",
        label="Gestión de Propiedades",
        url="/properties",
        icon="🏢"
    ),
    "register_payment": DashboardPage(
        key="register_payment",
        label="Registrar Pago",
        url="/payments/new",
        icon="🧾"
    ),
    "payments": DashboardPage(
        key="payments",
        label="Pagos del Edificio",
        url="/payments",
        icon="💰"
    ),
    "reports": DashboardPage(
        key="reports",
        label="Reportes",
        url="/reports",
        icon="📊"
    ),
}


# app/core/dashboard.py

ROLE_DASHBOARD_PAGES = {
    "admin": {
        "manage_users",
        "manage_properties",
        "register_payment",
        "payments",
        "reports",
    },
    "mesa_directiva": {
        "payments",
        "reports",
    },
    "propietario": {
        "payments",
        "reports",
    },
    "inquilino": {
        "register_payment",
    },
    "conserje": {
        "register_payment",
    },
}
