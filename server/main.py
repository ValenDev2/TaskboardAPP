from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.database import engine, Base
import server.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskBoard API",
    description="Sistema de gestión de tareas colaborativo",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "message": "TaskBoard API funcionando",
        "docs": "Visitá /docs para ver todos los endpoints"
    }

# Routers
from server.routers import auth, projects, tasks
app.include_router(auth.router,     prefix="/auth",     tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(tasks.router,    tags=["tasks"])  # sin prefix, las rutas ya incluyen /projects y /tasks