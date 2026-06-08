# schemas/user.py — Define qué datos se esperan y qué datos se devuelven
#
# Pydantic valida automáticamente los datos que llegan en los requests.
# Si el cliente manda un email sin "@", Pydantic lo rechaza antes
# de que llegue a tu código. Sin schemas, tendrías que validar todo a mano.
#
# Hay 3 schemas distintos para el usuario:
#   UserCreate  → datos que manda el cliente para registrarse
#   UserLogin   → datos que manda el cliente para hacer login
#   UserOut     → datos que el servidor devuelve (sin la contraseña)

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Lo que el cliente manda al registrarse."""
    username: str
    email: EmailStr   # EmailStr valida automáticamente que sea un email válido
    password: str


class UserLogin(BaseModel):
    """Lo que el cliente manda al hacer login."""
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Lo que el servidor devuelve — NUNCA incluir password_hash."""
    id: int
    username: str
    email: str

    # Esto le dice a Pydantic que puede leer atributos de objetos SQLAlchemy
    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    """Respuesta del login: el token y su tipo."""
    access_token: str
    token_type: str = "bearer"
    user: UserOut