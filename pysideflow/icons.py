from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QAbstractButton, QPushButton, QWidget
from qt_material_icons import MaterialIcon

from .models import MaterialScheme
from .utils import blend_colors

_STYLE_MAP: dict[str, MaterialIcon.Style] = {
    "outlined": MaterialIcon.Style.OUTLINED,
    "rounded": MaterialIcon.Style.ROUNDED,
    "sharp": MaterialIcon.Style.SHARP,
}


def get_button_colors(btn_type: str, scheme: MaterialScheme) -> tuple[str, str]:
    """Obtiene los colores para un botón dado un tipo de botón y un esquema de color.

    Args:
        btn_type: "elevated" | "filled" | "filledTonal" | "outlined" | "text"
        scheme: MaterialScheme

    Returns:
        tuple[str, str]: (normal_color, disabled_color)

    """
    disabled_color = blend_colors(scheme.surface, scheme.onSurface, 0.38)

    if btn_type == "filled":
        return scheme.onPrimary, disabled_color
    elif btn_type == "filledTonal":
        return scheme.onSecondaryContainer, disabled_color
    else:
        # elevated, outlined, text all use primary color for their icon/text
        return scheme.primary, disabled_color


def apply_icons(widget: QWidget, scheme: MaterialScheme):
    """Recursively finds all widgets with an `iconName` dynamic property.

    Applies a MaterialIcon with the correct MD3 colors based on their type.
    """
    # include the widget itself just in case it has the property
    widgets = [widget] + widget.findChildren(QWidget)

    for child in widgets:
        icon_name = child.property("iconName")
        if not icon_name:
            continue

        # ── iconStyle ──────────────────────────────────────
        icon_style_prop = child.property("iconStyle")
        style_enum = _STYLE_MAP.get(icon_style_prop, MaterialIcon.Style.ROUNDED)

        # ── iconFill ───────────────────────────────────────
        icon_fill_prop = child.property("iconFill")
        if icon_fill_prop is None:
            is_filled = False
        else:
            is_filled = str(icon_fill_prop).lower() in ("true", "si", "yes", "1")

        # ── Create the icon ────────────────────────────────
        icon = MaterialIcon(icon_name, style=style_enum, fill=is_filled)

        # ── Color by button type ───────────────────────────
        if isinstance(child, QAbstractButton):
            btn_type = child.property("type") or "elevated"
            normal_hex, disabled_hex = get_button_colors(btn_type, scheme)

            icon.set_color(QColor(normal_hex), mode=QIcon.Mode.Normal)
            icon.set_color(QColor(disabled_hex), mode=QIcon.Mode.Disabled)
        else:
            # Fallback for generic widgets
            icon.set_color(QColor(scheme.onSurface), mode=QIcon.Mode.Normal)
            icon.set_color(
                QColor(blend_colors(scheme.surface, scheme.onSurface, 0.38)),
                mode=QIcon.Mode.Disabled,
            )

        # ── Assign icon ─────────────────────────────────────
        if not hasattr(child, "setIcon"):
            continue

        # ── iconScale (dynamic property, default 18) ───────
        icon_size = child.property("iconScale")
        if icon_size is not None:
            if isinstance(icon_size, QSize):
                child.setIconSize(icon_size)
            else:
                child.setIconSize(QSize(int(icon_size), int(icon_size)))
        else:
            child.setIconSize(QSize(18, 18))

        child.setIcon(icon)

        # ── Button-specific MD3 adjustments ────────────────
        if isinstance(child, QPushButton):
            # Qt tiene un gap de ~4px por defecto, MD3 pide 8px.
            # Agregar un espacio en blanco añade los ~4px que faltan.
            text = child.text()
            if text and not text.startswith(" "):
                child.setText(" " + text.lstrip())

            # Para poder cambiar el padding-left a 16px en el CSS
            child.setProperty("hasIcon", True)

    # Single style refresh after all icons are applied
    widget.style().unpolish(widget)
    widget.style().polish(widget)
