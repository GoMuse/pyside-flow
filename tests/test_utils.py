"""Tests for pysideflow.utils."""

from __future__ import annotations

import pytest
from pysideflow.utils import blend_colors


class TestBlendColors:
    """Tests for blend_colors — alpha compositing over solid backgrounds."""

    def test_full_opacity_returns_overlay(self):
        """At 100% opacity, result equals the overlay color."""
        result = blend_colors("#000000", "#ff0000", 1.0)
        assert result == "#ff0000"

    def test_zero_opacity_returns_base(self):
        """At 0% opacity, result equals the base color."""
        result = blend_colors("#ff0000", "#000000", 0.0)
        assert result == "#ff0000"

    def test_half_opacity_blend(self):
        """50% blend of white over black yields middle gray."""
        result = blend_colors("#000000", "#ffffff", 0.5)
        assert result == "#7f7f7f"

    def test_md3_disabled_opacity(self):
        """MD3 disabled content uses 38% opacity."""
        result = blend_colors("#fef7ff", "#1c1b1f", 0.38)
        # Should be 7-char hex
        assert len(result) == 7
        assert result.startswith("#")
        # Should not equal either input
        assert result != "#fef7ff"
        assert result != "#1c1b1f"

    def test_strips_hash_prefix(self):
        """Handles hex strings with leading #."""
        result = blend_colors("#ff0000", "#00ff00", 1.0)
        assert result == "#00ff00"

    def test_handles_8_char_hex_argb(self):
        """Strips alpha channel from 8-char hex (ARGB → RGB)."""
        result = blend_colors("#ff000000", "#ffffffff", 0.5)
        assert result == "#7f7f7f"

    def test_empty_base_returns_base(self):
        """Empty base string returns the base unchanged."""
        result = blend_colors("", "#ff0000", 0.5)
        assert result == ""

    def test_empty_overlay_returns_base(self):
        """Empty overlay returns the base unchanged."""
        result = blend_colors("#000000", "", 0.5)
        assert result == "#000000"

    def test_invalid_hex_returns_base(self):
        """Invalid hex (< 6 chars) returns the base color unchanged."""
        result = blend_colors("#abc", "#ffffff", 0.5)
        assert result == "#abc"

    def test_opacity_clamped_to_valid_range(self):
        """Alpha compositing naturally clamps to 0–255, no overflow."""
        result = blend_colors("#ffffff", "#000000", 0.95)
        assert result == "#0c0c0c"

    @pytest.mark.parametrize(
        ("base", "overlay", "opacity", "expected"),
        [
            ("#ff0000", "#00ff00", 0.25, "#bf3f00"),
            ("#ff0000", "#00ff00", 0.50, "#7f7f00"),
            ("#ff0000", "#00ff00", 0.75, "#3fbf00"),
        ],
    )
    def test_red_over_green_gradient(self, base, overlay, opacity, expected):
        """Blend red over green at various opacities."""
        result = blend_colors(base, overlay, opacity)
        assert result == expected
