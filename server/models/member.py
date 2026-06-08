# models/member.py — Tabla que conecta usuarios con proyectos
#
# Esta tabla es el puente entre User y Project.
# Guarda qué usuario pertenece a qué proyecto y con qué rol.

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from server.database import Base

class ProjectMember(Base):
    __tablename__ = "project_members"

    id         = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    # rol puede ser "owner" o "member"
    # owner: crea, edita, elimina tareas e invita usuarios
    # member: ve tareas y las marca como done
    role       = Column(String, nullable=False, default="member")
    joined_at  = Column(DateTime, server_default=func.now())

    # Relaciones inversas para navegar fácilmente
    user    = relationship("User",    back_populates="memberships")
    project = relationship("Project", back_populates="members")