# routers/tasks.py — Endpoints de tareas
#
# Reglas de permisos (definidas en la idea original del proyecto):
#   - El owner puede: crear, editar, eliminar tareas, moverlas a cualquier estado
#   - El member puede: ver todas las tareas, marcarlas como "done"
#
# POST   /projects/{project_id}/tasks         → crear tarea (solo owner)
# GET    /projects/{project_id}/tasks         → listar tareas del proyecto (cualquier miembro)
# PATCH  /tasks/{task_id}/status              → cambiar estado (owner: cualquiera | member: solo "done")
# DELETE /tasks/{task_id}                     → eliminar tarea (solo owner)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.user import User
from server.models.task import Task
from server.models.member import ProjectMember
from server.schemas.task import TaskCreate, TaskUpdateStatus, TaskOut
from server.auth import get_current_user

router = APIRouter()


def _get_membership_or_404(db: Session, project_id: int, user_id: int) -> ProjectMember:
    """Verifica que el usuario sea miembro del proyecto."""
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Proyecto no encontrado")
    return membership


@router.post("/projects/{project_id}/tasks", response_model=TaskOut, status_code=201)
def create_task(
    project_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea una tarea nueva en el proyecto. Solo el owner puede crear."""

    membership = _get_membership_or_404(db, project_id, current_user.id)
    if membership.role != "owner":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Solo el creador del proyecto puede agregar tareas"
        )

    task = Task(
        project_id=project_id,
        created_by=current_user.id,
        title=data.title,
        description=data.description,
        status=data.status
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/projects/{project_id}/tasks", response_model=list[TaskOut])
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todas las tareas del proyecto. Cualquier miembro puede ver."""

    _get_membership_or_404(db, project_id, current_user.id)

    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    return tasks


@router.patch("/tasks/{task_id}/status", response_model=TaskOut)
def update_task_status(
    task_id: int,
    data: TaskUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mueve una tarea a otro estado.
    El owner puede moverla a cualquier estado.
    El member solo puede marcarla como 'done'.
    """

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tarea no encontrada")

    membership = _get_membership_or_404(db, task.project_id, current_user.id)

    if membership.role != "owner" and data.status != "done":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Solo podés marcar tareas como completadas"
        )

    task.status = data.status
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina una tarea. Solo el owner puede eliminar."""

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tarea no encontrada")

    membership = _get_membership_or_404(db, task.project_id, current_user.id)
    if membership.role != "owner":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Solo el creador del proyecto puede eliminar tareas"
        )

    db.delete(task)
    db.commit()