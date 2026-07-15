from enum import StrEnum

from pydantic import BaseModel, ConfigDict
from PySide6.QtGui import QColor


class ThemeMode(StrEnum):
    """Modo del tema."""

    AUTO = "auto"
    LIGHT = "light"
    DARK = "dark"


class ThemeConfig(BaseModel):
    """Modelo que centraliza toda la configuración del tema."""

    model_config = ConfigDict(frozen=True, use_enum_values=True)

    seed_color: str = "#6750a4"
    theme_mode: ThemeMode = ThemeMode.AUTO
    invert_secondary: bool = False

    def get_seed_color_qt(self) -> QColor:
        """Convierte el string a QColor cuando lo necesites."""
        return QColor(self.seed_color)


class MaterialScheme(BaseModel):
    """Paleta de colores Material Design."""

    model_config = ConfigDict(frozen=True)

    # ── Primary ───────────────────────────────────────────
    primary: str
    onPrimary: str  # Color
    primaryContainer: str
    onPrimaryContainer: str  # Color
    inversePrimary: str
    # ── Secondary ─────────────────────────────────────────
    secondary: str
    onSecondary: str  # Color
    secondaryContainer: str
    onSecondaryContainer: str  # Color
    # ── Tertiary ─────────────────────────────────────────
    tertiary: str
    onTertiary: str  # Color
    tertiaryContainer: str
    onTertiaryContainer: str  # Color
    # ── Error ────────────────────────────────────────────
    error: str
    onError: str  # Color
    errorContainer: str
    onErrorContainer: str  # Color
    # ── Surface ──────────────────────────────────────────
    surface: str
    onSurface: str  # Color
    surfaceVariant: str
    onSurfaceVariant: str  # Color
    inverseSurface: str
    inverseOnSurface: str
    # ── Surface Container ────────────────────────────────
    surfaceContainerLowest: str
    surfaceContainerLow: str
    surfaceContainer: str
    surfaceContainerHigh: str
    surfaceContainerHighest: str
    surfaceDim: str
    surfaceBright: str
    # ── Background ───────────────────────────────────────
    background: str
    onBackground: str  # Color
    # ── Outline ──────────────────────────────────────────
    outline: str
    outlineVariant: str
    # ── Scrim ────────────────────────────────────────────
    scrim: str
    # ── Shadow ───────────────────────────────────────────
    shadow: str
