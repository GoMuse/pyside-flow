"""Tests for pysideflow.app."""

from __future__ import annotations

import json
from pathlib import Path
from unittest import mock

import pytest
from PySide6.QtGui import QColor
from pysideflow import app as app_module
from pysideflow.generator import generate_material_scheme
from pysideflow.models import MaterialScheme, ThemeConfig


# ── Fixtures ────────────────────────────────────────────────
@pytest.fixture
def light_scheme() -> MaterialScheme:
    """Return a real MD3 light scheme for testing."""
    return generate_material_scheme(QColor("#6750a4"), is_dark=False)


@pytest.fixture
def tmp_appdata(monkeypatch, tmp_path: Path) -> Path:
    """Redirect QStandardPaths to a temp dir so tests don't touch real AppData."""
    monkeypatch.setattr(
        "PySide6.QtCore.QStandardPaths.writableLocation",
        lambda _: str(tmp_path),
    )
    return tmp_path


# ═══════════════════════════════════════════════════════════════
# _save_theme / _load_theme_cache
# ═══════════════════════════════════════════════════════════════


class TestThemeCache:
    """Tests for _save_theme and _load_theme_cache."""

    def test_save_and_load_roundtrip(self, tmp_appdata: Path):
        """Saved config+palette is recovered identically."""
        config = ThemeConfig(seed_color="#ff0000", theme_mode="dark")  # type: ignore[arg-type]
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

        app_module._save_theme(config, scheme, True)

        loaded_config, loaded_scheme, loaded_is_dark = app_module._load_theme_cache()

        assert loaded_config is not None
        assert loaded_config.seed_color == "#ff0000"
        assert loaded_config.theme_mode == "dark"
        assert loaded_scheme is not None
        assert loaded_scheme.primary == "#6750a4"
        assert loaded_is_dark is True

    def test_load_from_empty_cache(self, tmp_appdata: Path):
        """Empty/missing cache returns (None, None, None)."""
        config, scheme, is_dark = app_module._load_theme_cache()
        assert config is None
        assert scheme is None
        assert is_dark is None

    def test_load_corrupted_json_returns_none(self, tmp_appdata: Path):
        """Corrupted cache file returns None tuple without crashing."""
        (tmp_appdata / "theme.json").write_text("not valid json{{{", encoding="utf-8")
        config, scheme, is_dark = app_module._load_theme_cache()
        assert config is None

    def test_save_creates_theme_json(self, tmp_appdata: Path):
        """_save_theme creates a theme.json file."""
        config = ThemeConfig()
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

        app_module._save_theme(config, scheme, False)

        theme_file = tmp_appdata / "theme.json"
        assert theme_file.exists()
        data = json.loads(theme_file.read_text(encoding="utf-8"))
        assert "config" in data
        assert "palette" in data
        assert data["is_dark"] is False


# ═══════════════════════════════════════════════════════════════
# _build_theme
# ═══════════════════════════════════════════════════════════════


class TestBuildTheme:
    """Tests for _build_theme — stylesheet generation."""

    def test_returns_non_empty_string(self, qtbot, light_scheme):
        """_build_theme produces a non-empty CSS string."""
        # _add_fonts tries to access font files on disk — skip it in tests
        with mock.patch.object(app_module, "_add_fonts", return_value=None):
            stylesheet = app_module._build_theme(light_scheme)
        assert isinstance(stylesheet, str)
        assert len(stylesheet) > 0

    def test_contains_scheme_colors(self, qtbot, light_scheme):
        """Rendered stylesheet contains theme color values."""
        with mock.patch.object(app_module, "_add_fonts", return_value=None):
            stylesheet = app_module._build_theme(light_scheme)
        assert light_scheme.primary in stylesheet
        assert light_scheme.surface in stylesheet

    def test_inline_template_string(self, qtbot, light_scheme):
        """Passing a raw Jinja2 string as template works."""
        with mock.patch.object(app_module, "_add_fonts", return_value=None):
            result = app_module._build_theme(light_scheme, template="COLOR={{ scheme.primary }}")
        assert light_scheme.primary in result


# ═══════════════════════════════════════════════════════════════
# get_theme
# ═══════════════════════════════════════════════════════════════


class TestGetTheme:
    """Tests for get_theme."""

    def test_returns_none_when_no_cache(self, tmp_appdata: Path):
        """get_theme returns None if nothing has been saved."""
        result = app_module.get_theme()
        assert result is None

    def test_returns_scheme_after_save(self, tmp_appdata: Path, light_scheme):
        """get_theme returns the last saved scheme."""
        config = ThemeConfig()
        app_module._save_theme(config, light_scheme, False)
        result = app_module.get_theme()
        assert isinstance(result, MaterialScheme)
        assert result.primary == light_scheme.primary
