# models/invitation.py - Tabla de invitaciones

import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from server.database import Base

class Invitation(Base):
    __tablename__ = "invitations"

    id         = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    code       = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4())[:8])
    status     = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("Project", back_populates="invitations")