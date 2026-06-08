# models/project.py — Tabla de proyectos

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from server.database import Base

class Project(Base):
    __tablename__ = "projects"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    description = Column(String, nullable=True)  # opcional
    owner_id    = Column(Integer, ForeignKey("users.id"), nullable=False)  # quién lo creó
    created_at  = Column(DateTime, server_default=func.now())

    # "Un proyecto tiene muchos miembros"
    members = relationship("ProjectMember", back_populates="project")
    # "Un proyecto tiene muchas tareas"
    tasks   = relationship("Task", back_populates="project")
    # "Un proyecto tiene muchas invitaciones"
    invitations = relationship("Invitation", back_populates="project")