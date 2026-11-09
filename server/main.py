import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from server.database import engine, Base
import server.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskHUD API",
    description="Sistema de gestión de tareas colaborativo",
    version="1.0.0",
)

# Permitir orígenes locales con cualquier puerto dinámico asignado por pywebview
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r"http://(127\.0\.0\.1|localhost)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "message": "TaskHUD API funcionando",
        "docs": "Visitá /docs para ver todos los endpoints"
    }

# Routers
from server.routers import auth, projects, tasks
app.include_router(auth.router,     prefix="/auth",     tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(tasks.router,    tags=["tasks"])