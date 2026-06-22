# models/member.py - Tabla de miembros de proyectos

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from server.database import Base

class ProjectMember(Base):
    __tablename__ = "project_members"

    id         = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    role       = Column(String, nullable=False, default="member")
    joined_at  = Column(DateTime, server_default=func.now())

    user    = relationship("User",    back_populates="memberships")
    project = relationship("Project", back_populates="members")