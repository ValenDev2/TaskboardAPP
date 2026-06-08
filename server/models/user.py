# models/user.py — Tabla de usuarios
#
# Cada clase que hereda de Base se convierte en una tabla de la DB.
# Cada atributo con mapped_column() se convierte en una columna.

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from server.database import Base

if TYPE_CHECKING:
    from server.models.member import ProjectMember
    from server.models.task import Task

class User(Base):
    __tablename__ = "users"  # nombre de la tabla en la DB

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # único: no puede repetirse
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)          # NUNCA guardar contraseña en texto plano
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relaciones: le dicen a SQLAlchemy cómo conectar tablas
    # "Un usuario puede ser miembro de muchos proyectos"
    memberships: Mapped[list["ProjectMember"]] = relationship("ProjectMember", back_populates="user")
    # "Un usuario puede crear muchas tareas"
    tasks_created: Mapped[list["Task"]] = relationship("Task", back_populates="creator")