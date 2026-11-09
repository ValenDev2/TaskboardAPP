#!/usr/bin/env fish

# 1. Activar entorno virtual
source venv/bin/activate.fish

# 2. Arrancar el backend en segundo plano
echo "🚀 Iniciando Backend (FastAPI)..."
uvicorn server.main:app --reload --port 8000 &
set BACKEND_PID $last_pid

# Esperar 2 segundos a que Uvicorn termine de inicializarse
sleep 2

# 3. Arrancar el cliente de escritorio
echo "💻 Iniciando Cliente de escritorio..."
cd client
python main.py

# 4. Al cerrar la ventana del cliente, matar el proceso del backend
echo "🛑 Cerrando Backend..."
kill $BACKEND_PID