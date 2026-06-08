# client/main.py — Punto de entrada de la app de escritorio
#
# PyWebView crea una ventana nativa del sistema operativo
# y adentro renderiza una página web (el frontend HTML/CSS/JS)
# que se comunica con el servidor FastAPI remoto.
#
# Es exactamente como un browser, pero sin la barra de direcciones.

import webview

# URL del servidor: en desarrollo es localhost, en producción es tu servidor real
# Más adelante esto va a venir de un archivo de configuración
SERVER_URL = "http://localhost:8000"

if __name__ == "__main__":
    window = webview.create_window(
        title="TaskBoard",
        url=SERVER_URL,
        width=1280,
        height=800,
        min_size=(900, 600),
        # resizable=True permite redimensionar la ventana
        resizable=True,
    )

    # debug=True muestra las DevTools del browser (F12)
    # Poné debug=False cuando distribuyas la app
    webview.start(debug=True)