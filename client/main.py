# client/main.py — Inicio de la app de escritorios

import os
import webview

# Ruta absoluta al archivo HTML de login
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
START_PAGE = os.path.join(BASE_DIR, "ui", "index.html")

if __name__ == "__main__":
    window = webview.create_window(
        title="TaskBoard",
        url=START_PAGE,
        width=1280,
        height=800,
        min_size=(900, 600),
        resizable=True,
    )

    webview.start(debug=False)