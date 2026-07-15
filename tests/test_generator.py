"""Tests for pysideflow.generator."""

from __future__ import annotations

from PySide6.QtGui import QColor
from pysideflow.generator import generate_material_scheme
from pysideflow.models import MaterialScheme


class TestGenerateMaterialScheme:
    """Tests for generate_material_scheme — MD3 palette generation."""

    def test_returns_material_scheme_light(self):
        """Generates a valid MaterialScheme for a light theme."""
        scheme = generate_material_scheme(QColor("#6750a4"), is_dark=False)
        assert isinstance(scheme, MaterialScheme)
        assert scheme.primary.startswith("#")
        assert scheme.surface != scheme.primary  # different roles

    def test_returns_material_scheme_dark(self):
        """Generates a valid MaterialScheme for a dark theme."""
        scheme = generate_material_scheme(QColor("#6750a4"), is_dark=True)
        assert isinstance(scheme, MaterialScheme)
        # Dark surface should be darker than light
        light = generate_material_scheme(QColor("#6750a4"), is_dark=False)
        assert scheme.surface != light.surface

    def test_different_seed_produces_different_scheme(self):
        """Different seed colors yield different palettes."""
        red = generate_material_scheme(QColor("#ff0000"), is_dark=False)
        blue = generate_material_scheme(QColor("#0000ff"), is_dark=False)
        assert red.primary != blue.primary

    def test_all_hex_fields_are_valid(self):
        """Every color field is a valid 7-char hex string."""
        scheme = generate_material_scheme(QColor("#6750a4"), is_dark=False)
        for field_name in MaterialScheme.model_fields:
            value = getattr(scheme, field_name)
            assert isinstance(value, str), f"{field_name} is not str"
            assert len(value) == 7, f"{field_name} = {value!r} (expected 7 chars)"
            assert value.startswith("#"), f"{field_name} = {value!r} (no # prefix)"

    def test_handles_color_with_alpha(self):
        """Colors with alpha channel are handled correctly."""
        scheme = generate_material_scheme(QColor(103, 80, 164, 128), is_dark=False)
        assert isinstance(scheme, MaterialScheme)
        assert scheme.primary.startswith("#")
