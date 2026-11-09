# client/main.py — Inicio de la app de escritorio

import os
import webview
from PyQt5.QtWidgets import QApplication

class API:
    def copiar_al_portapapeles(self, texto: str):
        """Copia texto directamente al portapapeles del sistema operativo."""
        clipboard = QApplication.clipboard()
        clipboard.setText(texto)
        return True

# Ruta absoluta al archivo HTML de login
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
START_PAGE = os.path.join(BASE_DIR, "ui", "index.html")

if __name__ == "__main__":
    api = API()
    window = webview.create_window(
        title="TaskBoard",
        url=START_PAGE,
        width=1280,
        height=800,
        min_size=(900, 600),
        resizable=True,
        js_api=api,
    )

    webview.start(debug=False)