# src/app/models/user_role.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base

user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)
