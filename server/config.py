# server/config.py — Configuración global de TaskHUD

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret-key-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    DATABASE_URL: str = "sqlite:///./taskboard.db"
    ALLOWED_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000,file://"

    # Configuración para leer el .env e ignorar variables extra que no estén definidas aquí
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()