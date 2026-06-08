# config.py — Toda la configuración de la app vive acá
# pydantic-settings lee automáticamente las variables del archivo .env

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Estos nombres tienen que coincidir EXACTAMENTE con los del .env
    SECRET_KEY: str = "dev-secret-key-cambiar-en-produccion"
    ALGORITHM: str = "HS256"  # Algoritmo para firmar los tokens JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 días

    DATABASE_URL: str = "sqlite:///./taskboard.db"

    # Le dice a pydantic que lea el archivo .env
    model_config = {"env_file": ".env"}

# Instancia única que se importa en todo el proyecto
# Uso: from server.config import settings  →  settings.SECRET_KEY
settings = Settings()