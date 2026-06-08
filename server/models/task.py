# models/task.py — Tabla de tareas

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from server.database import Base

# Los estados posibles de una tarea — igual a las columnas del tablero
TASK_STATUSES = ["backlog", "ready", "in_progress", "in_review", "done"]

class Task(Base):
    __tablename__ = "tasks"

    id          = Column(Integer, primary_key=True, index=True)
    project_id  = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_by  = Column(Integer, ForeignKey("users.id"),    nullable=False)
    title       = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # Estado actual de la tarea en el tablero Kanban
    status      = Column(String, nullable=False, default="backlog")
    created_at  = Column(DateTime, server_default=func.now())
    updated_at  = Column(DateTime, server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")
    creator = relationship("User",    back_populates="tasks_created")