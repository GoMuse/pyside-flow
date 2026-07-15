"""Tests for pysideflow.models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError
from PySide6.QtGui import QColor
from pysideflow.models import MaterialScheme, ThemeConfig, ThemeMode


class TestThemeConfig:
    """Tests for ThemeConfig model — defaults, validation, Qt interop."""

    def test_default_seed_color(self):
        """Default seed is the MD3 baseline purple."""
        config = ThemeConfig()
        assert config.seed_color == "#6750a4"

    def test_default_theme_mode_is_auto(self):
        """Default theme_mode is AUTO."""
        config = ThemeConfig()
        assert config.theme_mode == ThemeMode.AUTO

    def test_get_seed_color_qt_returns_qcolor(self):
        """get_seed_color_qt returns a QColor instance."""
        config = ThemeConfig(seed_color="#ff0000")
        color = config.get_seed_color_qt()
        assert isinstance(color, QColor)
        assert color.name() == "#ff0000"

    def test_get_seed_color_qt_requires_hash_prefix(self):
        """QColor without # prefix falls back to black — Qt behavior."""
        config = ThemeConfig(seed_color="ff0000")
        color = config.get_seed_color_qt()
        # QColor('ff0000') is not a valid hex name → falls back to black
        assert color.name() == "#000000"

    def test_theme_mode_light(self):
        """Explicit ThemeMode.LIGHT is preserved."""
        config = ThemeConfig(theme_mode=ThemeMode.LIGHT)
        assert config.theme_mode == ThemeMode.LIGHT

    def test_theme_mode_dark(self):
        """Explicit ThemeMode.DARK is preserved."""
        config = ThemeConfig(theme_mode=ThemeMode.DARK)
        assert config.theme_mode == ThemeMode.DARK

    def test_config_is_frozen(self):
        """ThemeConfig is immutable (frozen Pydantic model)."""
        config = ThemeConfig()
        with pytest.raises((TypeError, ValidationError)):
            config.seed_color = "#000000"  # type: ignore[misc]

    def test_invalid_seed_color_still_accepted_as_string(self):
        """ThemeConfig accepts any string as seed (delegates validation to QColor)."""
        config = ThemeConfig(seed_color="not-a-color")
        assert config.seed_color == "not-a-color"

    def test_serialize_uses_enum_values(self):
        """model_dump returns 'auto'/'light'/'dark' strings, not enum objects."""
        config = ThemeConfig(theme_mode=ThemeMode.DARK)
        data = config.model_dump()
        assert data["theme_mode"] == "dark"


class TestMaterialScheme:
    """Tests for MaterialScheme — immutability, validation."""

    def test_scheme_is_frozen(self):
        """MaterialScheme is immutable."""
        scheme = MaterialScheme(
            primary="#6750a4",
            onPrimary="#ffffff",
            primaryContainer="#eaddff",
            onPrimaryContainer="#21005d",
            inversePrimary="#d0bcff",
            secondary="#625b71",
            onSecondary="#ffffff",
            secondaryContainer="#e8def8",
            onSecondaryContainer="#1d192b",
            tertiary="#7d5260",
            onTertiary="#ffffff",
            tertiaryContainer="#ffd8e4",
            onTertiaryContainer="#31111d",
            error="#b3261e",
            onError="#ffffff",
            errorContainer="#f9dedc",
            onErrorContainer="#410e0b",
            surface="#fef7ff",
            onSurface="#1c1b1f",
            surfaceVariant="#e7e0ec",
            onSurfaceVariant="#49454f",
            inverseSurface="#313033",
            inverseOnSurface="#f4eff4",
            surfaceContainerLowest="#fafafa",
            surfaceContainerLow="#f5f5f5",
            surfaceContainer="#eeeeee",
            surfaceContainerHigh="#e8e8e8",
            surfaceContainerHighest="#e0e0e0",
            surfaceDim="#ded8e1",
            surfaceBright="#fef7ff",
            background="#fef7ff",
            onBackground="#1c1b1f",
            outline="#79747e",
            outlineVariant="#cac4d0",
            scrim="#000000",
            shadow="#000000",
        )
        with pytest.raises((TypeError, ValidationError)):
            scheme.primary = "#000000"  # type: ignore[misc]

    def test_missing_field_raises_validation_error(self):
        """All 35 fields are required."""
        with pytest.raises(ValidationError):
            MaterialScheme(primary="#6750a4")
