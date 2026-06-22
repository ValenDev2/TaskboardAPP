# routers/tasks.py - Endpoints de tareas
#
# Permisos:
#   Owner  - mover a cualquier estado, crear y eliminar tareas
#   Member - mover solo a "in_progress" o "in_review"

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.user import User
from server.models.task import Task
from server.models.member import ProjectMember
from server.schemas.task import TaskCreate, TaskUpdateStatus, TaskOut
from server.auth import get_current_user

router = APIRouter()

MEMBER_ALLOWED_STATUSES = {"in_progress", "in_review"}


def _get_membership_or_404(db: Session, project_id: int, user_id: int) -> ProjectMember:
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
    membership = _get_membership_or_404(db, project_id, current_user.id)
    if membership.role != "owner":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el creador puede agregar tareas")

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
    _get_membership_or_404(db, project_id, current_user.id)
    return db.query(Task).filter(Task.project_id == project_id).all()


@router.patch("/tasks/{task_id}/status", response_model=TaskOut)
def update_task_status(
    task_id: int,
    data: TaskUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tarea no encontrada")

    membership = _get_membership_or_404(db, task.project_id, current_user.id)

    if membership.role != "owner" and data.status not in MEMBER_ALLOWED_STATUSES:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Solo podés mover tareas a 'En curso' o 'En revision'"
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
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tarea no encontrada")

    membership = _get_membership_or_404(db, task.project_id, current_user.id)
    if membership.role != "owner":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el creador puede eliminar tareas")

    db.delete(task)
    db.commit()