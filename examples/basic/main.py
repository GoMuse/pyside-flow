import os
import sys

# Agregamos el path del proyecto para asegurar que encuentre 'pysideflow'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from pysideflow import apply_theme
from pysideflow.models import ThemeConfig, ThemeMode


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación."""

    def __init__(self):
        """Inicializa la ventana principal."""
        super().__init__()
        self.setWindowTitle("PySideFlow Basic Example")
        self.resize(400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.label = QLabel("Prueba de PySideFlow")
        # Usamos la tipografía Material Design 3 que acabamos de agregar
        self.label.setProperty("class", "displayLarge")
        layout.addWidget(self.label)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Escribí algo acá...")
        layout.addWidget(self.line_edit)

        self.checkbox = QCheckBox("Material Design mola")
        layout.addWidget(self.checkbox)

        self.button = QPushButton("Botón Primario")
        layout.addWidget(self.button)

        # Botones para cambiar temas
        hbox = QHBoxLayout()
        self.btn_light = QPushButton("Tema Claro")
        self.btn_light.clicked.connect(lambda: self.change_theme(ThemeMode.LIGHT))
        hbox.addWidget(self.btn_light)

        self.btn_dark = QPushButton("Tema Oscuro")
        self.btn_dark.clicked.connect(lambda: self.change_theme(ThemeMode.DARK))
        hbox.addWidget(self.btn_dark)

        layout.addLayout(hbox)

    def change_theme(self, mode: ThemeMode):
        """Cambia el tema de la aplicación."""
        # Configuramos el tema usando nuestro modelo
        config = ThemeConfig(
            theme_mode=mode,
            seed_color="#6750a4",  # El color de Material 3 por defecto
        )
        # Lo aplicamos
        apply_theme(QApplication.instance(), config)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("BugCodeX")
    app.setApplicationName("PysideFlow")
    # Cargamos el tema guardado o uno por defecto si es la primera vez
    config = ThemeConfig(theme_mode=ThemeMode.AUTO, seed_color="#6750a4")
    apply_theme(app, config)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
