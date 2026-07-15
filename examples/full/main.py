import os
import sys

# Agregamos el path del proyecto para asegurar que encuentre 'pysideflow'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from pysideflow import apply_icons, apply_theme
from pysideflow.models import ThemeConfig, ThemeMode

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Configurar el theme en modo oscuro para que se parezca a la imagen
    config = ThemeConfig(theme_mode=ThemeMode.DARK, seed_color="#6750a4")
    scheme = apply_theme(app, config)

    # Cargar UI generada
    from pathlib import Path

    ui_file_path = str(Path(__file__).resolve().parent / "gallery.ui")
    ui_file = QFile(ui_file_path)
    if not ui_file.open(QFile.ReadOnly):
        print(f"Error opening {ui_file_path}")
        sys.exit(-1)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()

    apply_icons(window, scheme)

    window.show()
    sys.exit(app.exec())
