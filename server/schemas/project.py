# schemas/project.py — Validación de datos de proyectos

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProjectCreate(BaseModel):
    """Lo que el cliente manda para crear un proyecto."""
    name: str
    description: Optional[str] = None


class ProjectOut(BaseModel):
    """Lo que el servidor devuelve al consultar un proyecto."""
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: datetime
    # rol del usuario actual en este proyecto — útil para el frontend
    # (para saber si mostrar botones de owner o no)
    my_role: Optional[str] = None

    model_config = {"from_attributes": True}


class InvitationOut(BaseModel):
    """Lo que el servidor devuelve al crear una invitación."""
    id: int
    code: str
    status: str

    model_config = {"from_attributes": True}


class JoinProjectRequest(BaseModel):
    """Lo que el cliente manda para unirse a un proyecto con un código."""
    code: str