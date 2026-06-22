# routers/projects.py — Endpoints de proyectos
#
# POST   /projects              → crear un proyecto (el creador queda como owner)
# GET    /projects               → listar mis proyectos (donde soy owner o member)
# GET    /projects/{id}          → ver un proyecto específico
# POST   /projects/{id}/invite   → generar código de invitación (solo owner)
# POST   /projects/join          → unirse a un proyecto con un código

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.user import User
from server.models.project import Project
from server.models.member import ProjectMember
from server.models.invitation import Invitation
from server.schemas.project import (
    ProjectCreate, ProjectOut, InvitationOut, JoinProjectRequest
)
from server.auth import get_current_user

router = APIRouter()


def _get_membership_or_404(db: Session, project_id: int, user_id: int) -> ProjectMember:
    """
    Helper interno: busca la membresía del usuario en el proyecto.
    Si no existe, el usuario no tiene acceso → error 404.
    Usamos 404 en vez de 403 para no revelar si el proyecto existe.
    """
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Proyecto no encontrado")
    return membership


@router.post("", response_model=ProjectOut, status_code=201)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea un proyecto nuevo. El creador queda automáticamente como owner."""

    project = Project(
        name=data.name,
        description=data.description,
        owner_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    membership = ProjectMember(
        project_id=project.id,
        user_id=current_user.id,
        role="owner"
    )
    db.add(membership)
    db.commit()

    result = ProjectOut.model_validate(project)
    result.my_role = "owner"
    return result


@router.get("", response_model=list[ProjectOut])
def list_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todos los proyectos donde el usuario es owner o member."""

    memberships = db.query(ProjectMember).filter(
        ProjectMember.user_id == current_user.id
    ).all()

    results = []
    for m in memberships:
        out = ProjectOut.model_validate(m.project)
        out.my_role = m.role
        results.append(out)
    return results


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Devuelve los datos de un proyecto si el usuario tiene acceso."""

    membership = _get_membership_or_404(db, project_id, current_user.id)
    out = ProjectOut.model_validate(membership.project)
    out.my_role = membership.role
    return out


@router.post("/{project_id}/invite", response_model=InvitationOut, status_code=201)
def create_invitation(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Genera un código de invitación. Solo el owner puede invitar."""

    membership = _get_membership_or_404(db, project_id, current_user.id)
    if membership.role != "owner":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Solo el creador del proyecto puede invitar usuarios"
        )

    invitation = Invitation(project_id=project_id)
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return invitation


@router.post("/join", response_model=ProjectOut)
def join_project(
    data: JoinProjectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Une al usuario actual a un proyecto usando un código de invitación."""

    invitation = db.query(Invitation).filter(
        Invitation.code == data.code,
        Invitation.status == "pending"
    ).first()

    if not invitation:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Código de invitación inválido o ya usado"
        )

    # Verificar que no sea ya miembro
    existing = db.query(ProjectMember).filter(
        ProjectMember.project_id == invitation.project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Ya sos miembro de este proyecto"
        )

    # Crear la membresía como "member" (no owner)
    membership = ProjectMember(
        project_id=invitation.project_id,
        user_id=current_user.id,
        role="member"
    )
    db.add(membership)

    # Marcar la invitación como usada
    invitation.status = "accepted"
    db.commit()

    out = ProjectOut.model_validate(membership.project)
    out.my_role = "member"
    return out