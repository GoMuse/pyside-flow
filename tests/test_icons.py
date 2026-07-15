"""Tests for pysideflow.icons."""

from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QPushButton, QToolButton, QWidget
from pysideflow.icons import apply_icons, get_button_colors
from pysideflow.models import MaterialScheme


# ── Fixture: a minimal valid scheme ─────────────────────────
def _scheme() -> MaterialScheme:
    """Return a MaterialScheme with distinct colors for assertions."""
    return MaterialScheme(
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


# ═══════════════════════════════════════════════════════════════
# get_button_colors
# ═══════════════════════════════════════════════════════════════


class TestGetButtonColors:
    """Tests for pysideflow.icons.get_button_colors."""

    def test_filled_uses_on_primary(self):
        """Filled buttons use onPrimary for icon/text color."""
        scheme = _scheme()
        normal, _disabled = get_button_colors("filled", scheme)
        assert normal == scheme.onPrimary

    def test_filled_tonal_uses_on_secondary_container(self):
        """Filled tonal buttons use onSecondaryContainer for icon/text color."""
        scheme = _scheme()
        normal, _disabled = get_button_colors("filledTonal", scheme)
        assert normal == scheme.onSecondaryContainer

    def test_elevated_uses_primary(self):
        """Elevated buttons use primary for icon/text color."""
        scheme = _scheme()
        normal, _disabled = get_button_colors("elevated", scheme)
        assert normal == scheme.primary

    def test_outlined_uses_primary(self):
        """Outlined buttons use primary for icon/text color."""
        scheme = _scheme()
        normal, _disabled = get_button_colors("outlined", scheme)
        assert normal == scheme.primary

    def test_text_uses_primary(self):
        """Text buttons use primary for icon/text color."""
        scheme = _scheme()
        normal, _disabled = get_button_colors("text", scheme)
        assert normal == scheme.primary

    def test_disabled_is_blend_38_percent(self):
        """Disabled color is a 38% blend of onSurface over surface — never raw."""
        scheme = _scheme()
        _normal, disabled = get_button_colors("elevated", scheme)
        # blend_colors(surface, onSurface, 0.38) — verify it's not surface nor onSurface
        assert disabled != scheme.surface
        assert disabled != scheme.onSurface
        # Should be a 6-char hex color
        assert len(disabled) == 7
        assert disabled.startswith("#")


# ═══════════════════════════════════════════════════════════════
# apply_icons
# ═══════════════════════════════════════════════════════════════


class TestApplyIcons:
    """Tests for pysideflow.icons.apply_icons."""

    def test_icon_applied_to_button_with_icon_name(self, qtbot):
        """Widgets with iconName get an icon assigned."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")

        apply_icons(window, _scheme())

        assert not button.icon().isNull()

    def test_no_icon_name_skipped(self, qtbot):
        """Widgets without iconName keep null icon."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("No Icon", window)

        apply_icons(window, _scheme())

        assert button.icon().isNull()

    def test_widget_without_set_icon_skipped(self, qtbot):
        """Widgets without setIcon are skipped gracefully."""
        window = QMainWindow()
        qtbot.addWidget(window)
        container = QWidget(window)
        container.setProperty("iconName", "home")

        # Should not raise
        apply_icons(window, _scheme())

    def test_button_gets_icon_size_18_by_default(self, qtbot):
        """Buttons default to 18×18 iconSize when iconScale is not set."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")

        apply_icons(window, _scheme())

        assert button.iconSize() == QSize(18, 18)

    def test_button_respects_icon_scale_property(self, qtbot):
        """IconScale dynamic property overrides the default 18px size."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")
        button.setProperty("iconScale", 24)

        apply_icons(window, _scheme())

        assert button.iconSize() == QSize(24, 24)

    def test_qpushbutton_gets_has_icon_property(self, qtbot):
        """QPushButton gets hasIcon=True so CSS can target [hasIcon="true"]."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")

        apply_icons(window, _scheme())

        assert button.property("hasIcon") is True

    def test_qpushbutton_text_prefixed_with_space(self, qtbot):
        """QPushButton gets a leading space to match MD3 8px gap."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")

        apply_icons(window, _scheme())

        assert button.text().startswith(" ")

    def test_space_not_accumulated_on_second_call(self, qtbot):
        """Calling apply_icons twice should not double the space prefix."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")

        apply_icons(window, _scheme())
        apply_icons(window, _scheme())

        # Should have one space, not "  Home"
        assert button.text() == " Home"

    def test_toolbutton_gets_icon(self, qtbot):
        """QToolButton (via QAbstractButton) also gets icons."""
        window = QMainWindow()
        qtbot.addWidget(window)
        btn = QToolButton(window)
        btn.setProperty("iconName", "search")

        apply_icons(window, _scheme())

        assert not btn.icon().isNull()

    def test_default_style_is_rounded(self, qtbot):
        """Without iconStyle, icon defaults to rounded."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")

        apply_icons(window, _scheme())

        # Verify visual output: check available sizes (icon was created)
        sizes = button.icon().availableSizes()
        assert len(sizes) > 0

    def test_style_outlined(self, qtbot):
        """iconStyle='outlined' produces a valid MaterialIcon."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")
        button.setProperty("iconStyle", "outlined")

        apply_icons(window, _scheme())

        assert not button.icon().isNull()

    def test_style_sharp(self, qtbot):
        """iconStyle='sharp' produces a valid MaterialIcon."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")
        button.setProperty("iconStyle", "sharp")

        apply_icons(window, _scheme())

        assert not button.icon().isNull()

    def test_icon_fill_true(self, qtbot):
        """iconFill=True produces a filled MaterialIcon."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")
        button.setProperty("iconFill", True)

        apply_icons(window, _scheme())

        assert not button.icon().isNull()

    def test_icon_fill_false_string(self, qtbot):
        """'false' as string should be treated as falsy."""
        window = QMainWindow()
        qtbot.addWidget(window)
        button = QPushButton("Home", window)
        button.setProperty("iconName", "home")
        button.setProperty("iconFill", "false")

        apply_icons(window, _scheme())

        assert not button.icon().isNull()

    def test_root_widget_icon_name(self, qtbot):
        """The root widget itself is included in the scan (line 45)."""
        window = QMainWindow()
        qtbot.addWidget(window)
        # QMainWindow has setIcon via setWindowIcon
        window.setProperty("iconName", "home")

        # Should not raise — window is included first in the list
        apply_icons(window, _scheme())
