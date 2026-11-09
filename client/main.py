# client/main.py — Inicio de la app de escritorio

import os
import sys
import webview
from PyQt5.QtWidgets import QApplication

class API:
    def copiar_al_portapapeles(self, texto: str):
        """Copia texto directamente al portapapeles del sistema operativo."""
        clipboard = QApplication.clipboard()
        clipboard.setText(texto)
        return True

def get_resource_path(relative_path):
    """Obtiene la ruta absoluta a los recursos, compatible con PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

# Ruta absoluta al archivo HTML de login (compatible con dev y binario empaquetado)
START_PAGE = get_resource_path(os.path.join("ui", "index.html"))

if __name__ == "__main__":
    api = API()
    window = webview.create_window(
        title="TaskHUD",
        url=START_PAGE,
        width=1280,
        height=800,
        min_size=(900, 600),
        resizable=True,
        js_api=api,
    )

    webview.start(debug=False)