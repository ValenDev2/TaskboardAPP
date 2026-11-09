#!/usr/bin/env fish

# 1. Limpiar cualquier servidor previo que haya quedado colgado en el puerto 8000
pkill -f "uvicorn server.main:app" >/dev/null 2>&1

# 2. Activar entorno virtual
source venv/bin/activate.fish

# 3. Arrancar el backend en segundo plano
echo "🚀 Iniciando Backend (FastAPI)..."
uvicorn server.main:app --reload --port 8000 &

# Esperar 2 segundos a que Uvicorn inicialice
sleep 2

# 4. Arrancar el cliente de escritorio
echo "💻 Iniciando Cliente de escritorio..."
cd client
python main.py

# 5. Al cerrar el cliente o presionar Ctrl + C, matar todo proceso de Uvicorn del backend
echo "🛑 Cerrando Backend..."
pkill -f "uvicorn server.main:app" >/dev/null 2>&1