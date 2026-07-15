import json
import logging
from pathlib import Path

import darkdetect
import jinja2
from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from .generator import generate_material_scheme
from .models import MaterialScheme, ThemeConfig
from .tokens import MD3Elevation, MD3Shape, MD3State, MD3Typography
from .utils import blend_colors

logger = logging.getLogger(__name__)

TEMPLATE_FILE = str(Path(__file__).resolve().parent / "styles" / "material.jinja")


def apply_theme(app: QApplication, config: ThemeConfig | None = None) -> MaterialScheme:
    """Aplica el tema y retorna el MaterialScheme generado. Si config es None, intenta cargar el último usado."""

    # 1. Intentamos leer el caché del disco
    saved_config, saved_palette, saved_is_dark = _load_theme_cache()

    # 2. Si no pasaron config, usamos el guardado o uno por defecto
    if config is None:
        config = saved_config if saved_config else ThemeConfig()

    # 3. Resolver is_dark actual (clave si el OS cambió de claro a oscuro en modo AUTO)
    is_dark = (
        bool(darkdetect.isDark()) if config.theme_mode == "auto" else config.theme_mode == "dark"
    )

    # 4. Validar Caché: ¿Todo sigue igual que la última vez?
    if (
        saved_config
        and saved_palette
        and config.seed_color == saved_config.seed_color
        and config.theme_mode == saved_config.theme_mode
        and is_dark == saved_is_dark
    ):
        # Caché HIT: Usamos la paleta guardada (¡Ahorramos CPU!)
        material_scheme = saved_palette
    else:
        # Caché MISS: Regeneramos y guardamos
        material_scheme = generate_material_scheme(
            seed_color=config.get_seed_color_qt(), is_dark=is_dark
        )
        _save_theme(config, material_scheme, is_dark)

    # 5. Construir stylesheet y aplicarlo
    stylesheet = _build_theme(material_scheme)
    app.setStyleSheet(stylesheet)

    return material_scheme


def get_theme() -> MaterialScheme | None:
    """Retorna el esquema de colores actualmente guardado en caché."""
    _, saved_palette, _ = _load_theme_cache()
    return saved_palette


def _build_theme(scheme: MaterialScheme, template: str = TEMPLATE_FILE) -> str:
    """Build a theme."""

    try:
        _add_fonts()
    except Exception as e:
        logger.warning("Error intentando cargar las fuentes: %s", e)

    # Render custom template
    template_path = Path(template)
    if template_path.exists():
        parent = str(template_path.parent)
        template_name = template_path.name
        loader = jinja2.FileSystemLoader(parent)
        env = jinja2.Environment(autoescape=False, loader=loader)
        stylesheet = env.get_template(template_name)
    else:
        env = jinja2.Environment(autoescape=False, loader=jinja2.BaseLoader)
        stylesheet = env.from_string(template)

    # Inyectar funciones helper
    env.globals["blend_colors"] = blend_colors

    return stylesheet.render(
        scheme=scheme,
        typography=MD3Typography,
        shape=MD3Shape,
        elevation=MD3Elevation,
        state=MD3State,
    )


def _save_theme(config: ThemeConfig, scheme: MaterialScheme, is_dark: bool) -> None:
    """Guarda la configuración, la paleta y el estado is_dark en un único archivo theme.json."""
    try:
        app_data_path = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        dir_path = Path(app_data_path)
        dir_path.mkdir(parents=True, exist_ok=True)

        file_path = dir_path / "theme.json"

        data = {"config": config.model_dump(), "palette": scheme.model_dump(), "is_dark": is_dark}

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        logger.error("No se pudo guardar el theme en AppData: %s", e)


def _load_theme_cache() -> tuple[ThemeConfig | None, MaterialScheme | None, bool | None]:
    """Carga el caché del tema desde el disco."""
    try:
        app_data_path = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        file_path = Path(app_data_path) / "theme.json"

        if not file_path.exists():
            return None, None, None

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        saved_config = ThemeConfig(**data.get("config", {}))
        saved_is_dark = data.get("is_dark")

        saved_palette = None
        if "palette" in data:
            saved_palette = MaterialScheme(**data["palette"])

        return saved_config, saved_palette, saved_is_dark
    except Exception as e:
        logger.error("Error leyendo theme.json del caché: %s", e)
        return None, None, None


def _add_fonts() -> None:
    """Busca en la carpeta 'fonts' y registra las fuentes en la base de datos de Qt."""
    fonts_path = Path(__file__).parent / "fonts"

    if not fonts_path.exists() or not fonts_path.is_dir():
        return

    # Iterar sobre las carpetas de fuentes (por ejemplo, "roboto")
    for font_dir in fonts_path.iterdir():
        if not font_dir.is_dir():
            continue

        # Buscar archivos de fuentes comunes (.ttf, .otf)
        for font_file in font_dir.glob("*.[to]tf"):
            font_id = QFontDatabase.addApplicationFont(str(font_file))
            if font_id == -1:
                logger.warning("No se pudo cargar la fuente: %s", font_file.name)
