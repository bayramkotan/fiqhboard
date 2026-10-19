"""Small building blocks shared by the pages."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QLabel, QLayout, QPushButton, QWidget

from fiqhboard.gui import theme

RIGHT = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignAbsolute | Qt.AlignmentFlag.AlignVCenter


def label(text: str = "", name: str = "", wrap: bool = False, rich: bool = False) -> QLabel:
    lab = QLabel(text)
    if name:
        lab.setObjectName(name)
    lab.setWordWrap(wrap)
    lab.setTextFormat(Qt.TextFormat.RichText if rich else Qt.TextFormat.PlainText)
    return lab


def arabic(text: str, size: float = 12, bold: bool = False, color: str = "", name: str = "") -> QLabel:
    """Arabic in Amiri, right to left. Its font goes in the style sheet: a styled label ignores setFont()."""
    lab = label(text, name)
    lab.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    css = theme.font_css(theme.arabic_font(size, bold))
    lab.setStyleSheet(f"QLabel {{ {css} {'color: ' + color + ';' if color else ''} background: transparent; }}")
    return lab


def content_css(lang: str, size: float, bold: bool = False) -> str:
    """Text in the content language: Arabic in Amiri, a little larger; other languages in the UI font."""
    if lang == "ar":
        return theme.font_css(theme.arabic_font(size * 1.22, bold))
    return f"font-size: {theme.pt(size):.1f}pt; font-weight: {700 if bold else 400};"


def small(text: str, name: str, lang: str, size: float, bold: bool = False, wrap: bool = False) -> QLabel:
    """A small styled label in the content language: in Arabic it takes Amiri, its colour stays the theme's."""
    lab = label(text, name, wrap=wrap)
    if lang == "ar":
        lab.setStyleSheet(f"QLabel#{name} {{ {content_css(lang, size, bold)} }}")
    return lab


def direction(lang: str) -> Qt.LayoutDirection:
    return Qt.LayoutDirection.RightToLeft if lang == "ar" else Qt.LayoutDirection.LeftToRight


def clear(layout: QLayout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            widget = item.widget()
            widget.hide()               # gone from the screen now, not at the next event loop turn
            widget.setParent(None)
            widget.deleteLater()
        elif item.layout():
            clear(item.layout())


class Segments(QWidget):
    """A row of exclusive buttons: [All] [Four agree] [Differ]."""

    changed = Signal(str)

    def __init__(self, options: list[tuple[str, str]], current: str, parent=None) -> None:
        super().__init__(parent)
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._buttons: dict[str, QPushButton] = {}
        for key, text in options:
            button = QPushButton(text)
            button.setObjectName("Segment")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setChecked(key == current)
            button.clicked.connect(lambda _=False, k=key: self.changed.emit(k))
            self._group.addButton(button)
            self._buttons[key] = button
            row.addWidget(button)

    def set_current(self, key: str) -> None:
        if key in self._buttons:
            self._buttons[key].setChecked(True)
