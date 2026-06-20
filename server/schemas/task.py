# schemas/task.py — Validación de datos de tareas

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

# Los únicos estados válidos — coinciden con las columnas del tablero
VALID_STATUSES = {"backlog", "ready", "in_progress", "in_review", "done"}


class TaskCreate(BaseModel):
    """Lo que el cliente manda para crear una tarea."""
    title: str
    description: Optional[str] = None
    status: str = "backlog"

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str) -> str:
        if v not in VALID_STATUSES:
            raise ValueError(f"status debe ser uno de: {VALID_STATUSES}")
        return v


class TaskUpdateStatus(BaseModel):
    """Lo que el cliente manda para mover una tarea entre columnas."""
    status: str

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str) -> str:
        if v not in VALID_STATUSES:
            raise ValueError(f"status debe ser uno de: {VALID_STATUSES}")
        return v


class TaskOut(BaseModel):
    """Lo que el servidor devuelve al consultar tareas."""
    id: int
    project_id: int
    created_by: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}