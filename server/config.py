# config.py — Toda la configuración de la app
# pydantic-settings lee automáticamente las variables del archivo .env

from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    SECRET_KEY: str = "dev-secret-key-cambiar-en-produccion"
    ALGORITHM: str = "HS256"  # Algoritmo para firmar los tokens JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 días

    DATABASE_URL: str = "sqlite:///./taskboard.db"

    model_config = {"env_file": ".env"}

settings = Settings()