# routers/auth.py — Endpoints de autenticación
#
# POST /auth/register → crea un usuario nuevo
# POST /auth/login    → devuelve un token JWT
# GET  /auth/me       → devuelve el usuario actual (requiere token)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.user import User
from server.models.member import ProjectMember
from server.schemas.user import UserCreate, UserLogin, UserOut, TokenOut
from server.auth import hash_password, verify_password, create_access_token, get_current_user

# APIRouter agrupa endpoints relacionados — como un mini-app dentro de la app
router = APIRouter()


@router.post("/register", response_model=TokenOut, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registra un usuario nuevo y devuelve su token."""

    # Verificar que el email no esté en uso
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Verificar que el username no esté en uso
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )

    # Crear el usuario — hashear la contraseña antes de guardarla
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # actualiza el objeto con el id asignado por la DB

    token = create_access_token(new_user.id)
    return {"access_token": token, "token_type": "bearer", "user": new_user}


@router.post("/login", response_model=TokenOut)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Verifica credenciales y devuelve un token JWT."""

    user = db.query(User).filter(User.email == credentials.email).first()

    # Mismo mensaje para email y contraseña incorrectos — no dar pistas
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Devuelve el perfil del usuario autenticado."""
    return current_user