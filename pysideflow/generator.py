import logging

from PySide6.QtGui import QColor

from .models import MaterialScheme

logger = logging.getLogger(__name__)


def _qcolor_to_argb(color: QColor) -> int:
    """Convert a QColor to an ARGB integer."""
    return int(color.rgba()) & 0xFFFFFFFF


def _argb_to_hex(argb: int) -> str:
    """Convert an ARGB integer to a hex string."""
    return QColor.fromRgba(int(argb) & 0xFFFFFFFF).name(QColor.NameFormat.HexRgb).lower()


def _hex_to_qml_hex_rgb(hex_str: str) -> str:
    """Convert a hex string to a QML hex rgb."""
    hex = hex_str.strip().lower()
    if not hex.startswith("#"):
        return hex
    if len(hex) == 9:
        return hex[:7]
    return hex


def generate_material_scheme(seed_color: QColor, is_dark: bool) -> MaterialScheme:
    """Genera y devuelve una instancia de MaterialScheme, no un dict."""
    argb = int(seed_color.rgba()) & 0xFFFFFFFF

    try:
        from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        from materialyoucolor.hct import Hct
        from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot

        source = Hct.from_int(argb)
        scheme = SchemeTonalSpot(source, bool(is_dark), 0.0)
        dynamic_colors = MaterialDynamicColors()

        scheme_dict = {}
        for field_name in MaterialScheme.model_fields:
            dynamic_color = getattr(dynamic_colors, field_name)
            hex_string = str(dynamic_color.get_hex(scheme))
            scheme_dict[field_name] = _hex_to_qml_hex_rgb(hex_string)

        # LA MAGIA: Desempaquetamos el dict directamente en el modelo de Pydantic
        return MaterialScheme(**scheme_dict)

    except Exception as e:
        logger.error("Error generando Material Scheme: %s", e)
        raise RuntimeError(f"Error generando Material Scheme: {e}") from e
