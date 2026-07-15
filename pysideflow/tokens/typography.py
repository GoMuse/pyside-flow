from pydantic import BaseModel, ConfigDict
from PySide6.QtGui import QFont


class TypeScale(BaseModel):
    """Material Design 3 Type Scale Tokens."""

    family: str = "Roboto"
    size: int
    weight: int
    tracking: float

    model_config = ConfigDict(frozen=True)

    def to_qfont(self) -> QFont:
        """Convierte este token en un objeto QFont listo para usar en PySide6."""
        font = QFont(self.family)
        font.setPixelSize(self.size)

        # Mapeamos los pesos CSS a los de Qt
        weight_map = {
            400: QFont.Weight.Normal,
            500: QFont.Weight.Medium,
            600: QFont.Weight.DemiBold,
            700: QFont.Weight.Bold,
        }
        font.setWeight(weight_map.get(self.weight, QFont.Weight.Normal))
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, self.tracking)
        return font


class MD3Typography:
    """Todos los tokens de tipografía de Material Design 3."""

    # Display
    displayLarge = TypeScale(size=57, weight=400, tracking=-0.25)
    displayMedium = TypeScale(size=45, weight=400, tracking=0.0)
    displaySmall = TypeScale(size=36, weight=400, tracking=0.0)

    # Headline
    headlineLarge = TypeScale(size=32, weight=400, tracking=0.0)
    headlineMedium = TypeScale(size=28, weight=400, tracking=0.0)
    headlineSmall = TypeScale(size=24, weight=400, tracking=0.0)

    # Title
    titleLarge = TypeScale(size=22, weight=400, tracking=0.0)
    titleMedium = TypeScale(size=16, weight=500, tracking=0.15)
    titleSmall = TypeScale(size=14, weight=500, tracking=0.1)

    # Label
    labelLarge = TypeScale(size=14, weight=500, tracking=0.1)
    labelMedium = TypeScale(size=12, weight=500, tracking=0.5)
    labelSmall = TypeScale(size=11, weight=500, tracking=0.5)

    # Body
    bodyLarge = TypeScale(size=16, weight=400, tracking=0.5)
    bodyMedium = TypeScale(size=14, weight=400, tracking=0.25)
    bodySmall = TypeScale(size=12, weight=400, tracking=0.4)
