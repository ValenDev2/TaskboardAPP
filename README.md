# TaskBoard

Sistema de gestión de tareas colaborativo — app de escritorio con Python.

## Requisitos

- Python 3.11 o superior
- pip (viene con Python)

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd taskboard

# 2. Crear entorno virtual (aísla las dependencias del proyecto)
python -m venv venv

# 3. Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
cp .env.example .env
# Editá el archivo .env con tus valores
```

## Correr el servidor (desarrollo)

```bash
uvicorn server.main:app --reload --port 8000
```

Luego abrí http://localhost:8000/docs para ver los endpoints.

## Correr el cliente desktop

```bash
python client/main.py
```

## Estructura del proyecto

```
taskboard/
├── server/
│   ├── models/     # Tablas de la base de datos
│   ├── schemas/    # Validación de datos (entrada/salida)
│   ├── routers/    # Endpoints agrupados por feature
│   ├── config.py   # Configuración general
│   ├── database.py # Conexión con SQLite
│   └── main.py     # Entry point del servidor
├── client/
│   ├── main.py     # Entry point desktop (PyWebView)
│   └── ui/         # Frontend HTML/CSS/JS
├── .env            # Variables de entorno (no subir a Git)
├── .env.example    # Template del .env
└── requirements.txt
```