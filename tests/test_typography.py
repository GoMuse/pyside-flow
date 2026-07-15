"""Tests for pysideflow.tokens.typography."""

from __future__ import annotations

from PySide6.QtGui import QFont
from pysideflow.tokens.typography import MD3Typography, TypeScale


class TestTypeScale:
    """Tests for TypeScale token — to_qfont conversion, weight mapping."""

    def test_to_qfont_returns_qfont(self):
        """to_qfont returns a valid QFont instance."""
        scale = TypeScale(family="Roboto", size=16, weight=400, tracking=0.5)
        font = scale.to_qfont()
        assert isinstance(font, QFont)

    def test_to_qfont_family(self):
        """Font family is preserved."""
        scale = TypeScale(family="Inter", size=14, weight=500, tracking=0.1)
        font = scale.to_qfont()
        assert font.family() == "Inter"

    def test_to_qfont_pixel_size(self):
        """Pixel size matches the token size."""
        scale = TypeScale(family="Roboto", size=22, weight=400, tracking=0.0)
        font = scale.to_qfont()
        assert font.pixelSize() == 22

    def test_weight_400_maps_to_normal(self):
        """Weight 400 → QFont.Weight.Normal."""
        font = TypeScale(family="Roboto", size=14, weight=400, tracking=0.0).to_qfont()
        assert font.weight() == QFont.Weight.Normal

    def test_weight_500_maps_to_medium(self):
        """Weight 500 → QFont.Weight.Medium."""
        font = TypeScale(family="Roboto", size=14, weight=500, tracking=0.0).to_qfont()
        assert font.weight() == QFont.Weight.Medium

    def test_weight_600_maps_to_demi_bold(self):
        """Weight 600 → QFont.Weight.DemiBold."""
        font = TypeScale(family="Roboto", size=14, weight=600, tracking=0.0).to_qfont()
        assert font.weight() == QFont.Weight.DemiBold

    def test_weight_700_maps_to_bold(self):
        """Weight 700 → QFont.Weight.Bold."""
        font = TypeScale(family="Roboto", size=14, weight=700, tracking=0.0).to_qfont()
        assert font.weight() == QFont.Weight.Bold

    def test_unknown_weight_falls_back_to_normal(self):
        """Weights not in the map default to Normal."""
        font = TypeScale(family="Roboto", size=14, weight=300, tracking=0.0).to_qfont()
        assert font.weight() == QFont.Weight.Normal

    def test_letter_spacing_is_set(self):
        """Tracking value becomes absolute letter spacing."""
        scale = TypeScale(family="Roboto", size=14, weight=400, tracking=0.25)
        font = scale.to_qfont()
        assert font.letterSpacing() == 0.25
        assert font.letterSpacingType() == QFont.SpacingType.AbsoluteSpacing

    def test_model_is_frozen(self):
        """TypeScale is immutable (frozen Pydantic model)."""
        scale = TypeScale(family="Roboto", size=14, weight=400, tracking=0.0)
        with __import__("pytest").raises(Exception):
            scale.size = 999  # type: ignore[misc]


class TestMD3Typography:
    """Verify all MD3 token attributes exist and are TypeScale instances."""

    _EXPECTED_TOKENS = [
        "displayLarge",
        "displayMedium",
        "displaySmall",
        "headlineLarge",
        "headlineMedium",
        "headlineSmall",
        "titleLarge",
        "titleMedium",
        "titleSmall",
        "labelLarge",
        "labelMedium",
        "labelSmall",
        "bodyLarge",
        "bodyMedium",
        "bodySmall",
    ]

    def test_all_tokens_are_typescale_instances(self):
        """Every MD3Typography token is a TypeScale instance."""
        for name in self._EXPECTED_TOKENS:
            token = getattr(MD3Typography, name)
            assert isinstance(token, TypeScale), f"MD3Typography.{name} is not TypeScale"

    def test_all_tokens_have_positive_size(self):
        """All typography tokens have size > 0."""
        for name in self._EXPECTED_TOKENS:
            token = getattr(MD3Typography, name)
            assert token.size > 0, f"MD3Typography.{name}.size = {token.size}"

    def test_all_tokens_have_valid_weight(self):
        """All typography tokens use weight 400 or 500 (MD3 spec)."""
        for name in self._EXPECTED_TOKENS:
            token = getattr(MD3Typography, name)
            assert token.weight in (400, 500), f"MD3Typography.{name}.weight = {token.weight}"

    def test_token_to_qfont_does_not_raise(self):
        """to_qfont() succeeds for every MD3 typography token."""
        for name in self._EXPECTED_TOKENS:
            token = getattr(MD3Typography, name)
            font = token.to_qfont()
            assert isinstance(font, QFont)
