"""Visual identity of fiqhboard, shared with isnady.

Lapis blue for structure, gold for the accent, as in illuminated manuscripts. Arabic is set in Amiri
(bundled, SIL OFL), a naskh in the Bulaq press tradition; interface chrome keeps the system font.

Seven named themes; "system" follows the light or dark scheme of the desktop.
Answer colours: each answer of a row gets its own colour, so the eye sees who stands with whom. The words are
always written as well; the colour only helps.
"""

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QFontDatabase, QGuiApplication, QPalette
from PySide6.QtWidgets import QApplication, QStyleFactory

from fiqhboard import config

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONT_DIR = ASSETS / "fonts"
ICON_DIR = ASSETS / "icons"
ARABIC_FAMILY = "Amiri"


@dataclass(frozen=True)
class Tokens:
    dark: bool
    window: str        # app background
    surface: str       # cards, inputs
    border: str
    ink: str           # main text
    muted: str         # secondary text
    lapis: str         # primary
    lapis_soft: str    # hover / selected backgrounds
    gold: str          # accent
    gilt: str          # soft gold background
    sidebar: str
    sidebar_ink: str
    sidebar_muted: str
    sidebar_selected: str
    pill: str


LIGHT = Tokens(
    dark=False, window="#EEF1F5", surface="#FFFFFF", border="#D9DFE7", ink="#18212C", muted="#5B6878",
    lapis="#1D4777", lapis_soft="#E3EBF5", gold="#A47E24", gilt="#F2E2B3",
    sidebar="#14304F", sidebar_ink="#F1F4F8", sidebar_muted="#9DB0C6", sidebar_selected="#22466F",
    pill="#EDF1F6",
)
DARK = Tokens(
    dark=True, window="#10151C", surface="#18202A", border="#2A3542", ink="#E4E9EF", muted="#8E9BAA",
    lapis="#7FAEE0", lapis_soft="#1F2C3B", gold="#D6B25E", gilt="#4B3C17",
    sidebar="#0B1522", sidebar_ink="#E4E9EF", sidebar_muted="#7D8FA5", sidebar_selected="#1A2D45",
    pill="#222C38",
)
PAPER = Tokens(
    dark=False, window="#F3EEE4", surface="#FFFCF6", border="#E2D8C8", ink="#2B241C", muted="#776A59",
    lapis="#8A3B1F", lapis_soft="#F1E2D4", gold="#A8792A", gilt="#F3DFAE",
    sidebar="#3A2A1E", sidebar_ink="#F6EEE3", sidebar_muted="#BCAA93", sidebar_selected="#55402E",
    pill="#EFE6D8",
)
SLATE = Tokens(
    dark=False, window="#F5F6F8", surface="#FFFFFF", border="#E2E5EA", ink="#111827", muted="#646B78",
    lapis="#4338CA", lapis_soft="#ECEDFE", gold="#C2700A", gilt="#FCE7C2",
    sidebar="#FFFFFF", sidebar_ink="#111827", sidebar_muted="#646B78", sidebar_selected="#ECEDFE",
    pill="#F0F2F5",
)
EMERALD = Tokens(
    dark=False, window="#EFF5F2", surface="#FFFFFF", border="#D3E2DB", ink="#13241D", muted="#58706A",
    lapis="#0F6E66", lapis_soft="#DCF0EA", gold="#B0741C", gilt="#F6E1B2",
    sidebar="#0B3B33", sidebar_ink="#EAF6F2", sidebar_muted="#93BCB1", sidebar_selected="#14544A",
    pill="#E7F1ED",
)
MIDNIGHT = Tokens(
    dark=True, window="#0D1117", surface="#161B22", border="#2A313C", ink="#E6EDF3", muted="#8B949E",
    lapis="#5CC8BC", lapis_soft="#16302E", gold="#E3B341", gilt="#4A3A12",
    sidebar="#090C10", sidebar_ink="#E6EDF3", sidebar_muted="#7D8590", sidebar_selected="#18242C",
    pill="#21262D",
)
CONTRAST = Tokens(
    dark=True, window="#000000", surface="#0B0B0B", border="#BDBDBD", ink="#FFFFFF", muted="#D4D4D4",
    lapis="#FFD400", lapis_soft="#2E2A00", gold="#FFD400", gilt="#5C4D00",
    sidebar="#000000", sidebar_ink="#FFFFFF", sidebar_muted="#D4D4D4", sidebar_selected="#262626",
    pill="#1A1A1A",
)
THEMES = {   # key: (name, description, tokens)
    "light": ("Lapis", "Lapis and gold of illuminated manuscripts", LIGHT),
    "dark": ("Lapis Night", "The same, by night", DARK),
    "paper": ("Paper", "Warm cream and ink, for long reading", PAPER),
    "slate": ("Slate", "Quiet and modern, a light sidebar", SLATE),
    "emerald": ("Emerald", "Green and gold", EMERALD),
    "midnight": ("Midnight", "Deep dark with teal", MIDNIGHT),
    "contrast": ("High Contrast", "Black, white and yellow, for low vision", CONTRAST),
}

# One colour per answer of a row, in the row's answer order: (strong, soft background).
ANSWER_COLORS = {
    False: [("#1D6B4F", "#E1F1EA"), ("#9A3B2E", "#F6E3DF"), ("#8A6512", "#F5EBCF"), ("#4A3F8C", "#E8E5F6")],
    True: [("#7FD0A8", "#173328"), ("#EE9A8B", "#3A1F1B"), ("#E5C46A", "#3A2F12"), ("#AFA4F0", "#26223F")],
}

_current: Tokens = LIGHT
TEXT_SCALE_MIN, TEXT_SCALE_MAX, TEXT_SCALE_STEP = 0.8, 1.6, 0.1


def current() -> Tokens:
    return _current


def answer_color(index: int) -> tuple[str, str]:
    palette = ANSWER_COLORS[_current.dark]
    return palette[index % len(palette)]


def theme_mode() -> str:
    return config.get("view.theme")


def set_theme_mode(mode: str) -> None:
    config.set("view.theme", mode if mode in config.THEMES else "system")


def text_scale() -> float:
    return float(config.get("view.text_scale"))


def set_text_scale(value: float) -> float:
    value = round(min(max(value, TEXT_SCALE_MIN), TEXT_SCALE_MAX), 2)
    config.set("view.text_scale", value)
    return value


def load_fonts() -> bool:
    ok = False
    for name in ("Amiri-Regular.ttf", "Amiri-Bold.ttf"):
        path = FONT_DIR / name
        if path.exists() and QFontDatabase.addApplicationFont(str(path)) != -1:
            ok = True
    return ok


def pt(size: float) -> float:
    """A point size times the reader's text size (View → Text size)."""
    return round(size * text_scale(), 1)


def arabic_font(point_size: float, bold: bool = False) -> QFont:
    font = QFont(ARABIC_FAMILY)
    font.setPointSizeF(pt(point_size))
    font.setBold(bold)
    return font


def font_css(font: QFont) -> str:
    """The font as style-sheet text. A widget with its own style sheet ignores setFont()."""
    weight = "700" if font.bold() else "400"
    return f"font-family: '{font.family()}'; font-size: {font.pointSizeF():.1f}pt; font-weight: {weight};"


def _is_dark_scheme() -> bool:
    hints = QGuiApplication.styleHints()
    if getattr(hints, "colorScheme", None) is not None:
        return hints.colorScheme() == Qt.ColorScheme.Dark
    return QGuiApplication.palette().color(QPalette.ColorRole.Window).lightness() < 128


def _palette(t: Tokens) -> QPalette:
    p = QPalette()
    role = QPalette.ColorRole
    p.setColor(role.Window, QColor(t.window))
    p.setColor(role.WindowText, QColor(t.ink))
    p.setColor(role.Base, QColor(t.surface))
    p.setColor(role.AlternateBase, QColor(t.window))
    p.setColor(role.Text, QColor(t.ink))
    p.setColor(role.Button, QColor(t.surface))
    p.setColor(role.ButtonText, QColor(t.ink))
    p.setColor(role.Highlight, QColor(t.lapis))
    p.setColor(role.HighlightedText, QColor(t.surface if not t.dark else t.window))
    p.setColor(role.ToolTipBase, QColor(t.surface))
    p.setColor(role.ToolTipText, QColor(t.ink))
    p.setColor(role.PlaceholderText, QColor(t.muted))
    p.setColor(role.Link, QColor(t.lapis))
    for r in (role.Text, role.WindowText, role.ButtonText):
        p.setColor(QPalette.ColorGroup.Disabled, r, QColor(t.muted))
    return p


def _icon(name: str, t: Tokens) -> str:
    return (ICON_DIR / f"{name}-{'dark' if t.dark else 'light'}.svg").as_posix()


def stylesheet(t: Tokens) -> str:
    chevron = _icon("chevron", t)
    on_lapis = t.surface if not t.dark else t.window
    s = text_scale()
    return f"""
    QMainWindow, QWidget#Page {{ background: {t.window}; }}
    QMenuBar {{ background: {t.window}; color: {t.ink}; border-bottom: 1px solid {t.border}; padding: 2px 6px; }}
    QMenuBar::item {{ background: transparent; padding: 5px 10px; border-radius: 5px; }}
    QMenuBar::item:selected {{ background: {t.lapis_soft}; }}
    QMenu {{ background: {t.surface}; color: {t.ink}; border: 1px solid {t.border}; padding: 6px 0; }}
    QMenu::item {{ padding: 6px 28px 6px 26px; }}
    QMenu::item:selected {{ background: {t.lapis_soft}; color: {t.ink}; }}
    QMenu::item:disabled {{ color: {t.muted}; }}
    QMenu::separator {{ height: 1px; background: {t.border}; margin: 5px 12px; }}
    QMenu::indicator {{ width: 14px; height: 14px; left: 7px; }}
    QToolTip {{ background: {t.surface}; color: {t.ink}; border: 1px solid {t.border}; padding: 4px 6px; }}
    QDialog {{ background: {t.window}; }}

    /* sidebar */
    QFrame#Sidebar {{ background: {t.sidebar}; border: none;
                      border-right: 1px solid {t.border if t.sidebar.upper() == t.surface.upper() else t.sidebar}; }}
    QLabel#Wordmark {{ color: {t.sidebar_ink}; }}
    QLabel#WordmarkArabic {{ color: {t.gold}; }}
    QLabel#SidebarFooter {{ color: {t.sidebar_muted}; font-size: 8.5pt; }}
    QLabel#SidebarHeading {{ color: {t.sidebar_muted}; font-size: 8pt; font-weight: 700; letter-spacing: 0.6px;
                             padding: 0 28px; }}
    QListWidget#Nav {{ background: transparent; border: none; outline: none; color: {t.sidebar_ink}; }}
    QListWidget#Nav::item {{ padding-left: 16px; margin: 2px 12px; border-radius: 8px; color: {t.sidebar_muted}; }}
    QListWidget#Nav::item:hover {{ background: {t.sidebar_selected}; color: {t.sidebar_ink}; }}
    QListWidget#Nav::item:selected {{ background: {t.sidebar_selected}; color: {t.sidebar_ink};
                                      border-left: 3px solid {t.gold}; }}
    QTreeWidget#Topics {{ background: transparent; border: none; outline: none; color: {t.sidebar_muted}; }}
    QTreeWidget#Topics::item {{ padding: 5px 4px; border-radius: 6px; }}
    QTreeWidget#Topics::item:hover {{ background: {t.sidebar_selected}; color: {t.sidebar_ink}; }}
    QTreeWidget#Topics::item:selected {{ background: {t.sidebar_selected}; color: {t.sidebar_ink}; }}
    QTreeWidget#Topics::branch, QTreeWidget#Topics::branch:selected {{ background: transparent; border: none; }}

    /* page head */
    QLabel#Crumbs {{ color: {t.muted}; font-size: {8.5 * s:.1f}pt; font-weight: 600; letter-spacing: 0.4px; }}
    QLabel#PageTitle {{ color: {t.ink}; }}
    QLabel#PageTitleArabic {{ color: {t.gold}; }}
    QLabel#Lead {{ color: {t.muted}; font-size: {10.5 * s:.1f}pt; }}
    QFrame#Draft {{ background: {t.gilt}; border: 1px solid {t.gold}; border-radius: 9px; }}
    QFrame#Draft QLabel {{ color: {t.ink}; background: transparent; font-size: {9 * s:.1f}pt; }}

    /* controls */
    QPushButton#Segment {{ background: {t.surface}; color: {t.muted}; border: 1.5px solid {t.border};
                          border-radius: 8px; padding: 5px 14px; font-weight: 600; }}
    QPushButton#Segment:hover {{ border-color: {t.lapis}; color: {t.ink}; }}
    QPushButton#Segment:checked {{ background: {t.lapis}; color: {on_lapis}; border-color: {t.lapis}; }}
    QLabel#FilterTitle {{ color: {t.muted}; font-size: 8.5pt; font-weight: 600; letter-spacing: 0.3px; }}
    QLabel#Summary {{ color: {t.muted}; }}
    QLineEdit {{ background: {t.surface}; color: {t.ink}; border: 1px solid {t.border}; border-radius: 9px;
                 padding: 7px 12px; }}
    QLineEdit:focus {{ border: 1.5px solid {t.lapis}; }}
    QComboBox {{ background: {t.surface}; color: {t.ink}; border: 1px solid {t.border}; border-radius: 7px;
                 padding: 5px 10px; min-height: 18px; combobox-popup: 0; }}
    QComboBox::drop-down {{ border: none; width: 24px; }}
    QComboBox::down-arrow {{ image: url("{chevron}"); width: 12px; height: 12px; }}
    QPushButton#Link {{ background: transparent; color: {t.lapis}; border: none; padding: 2px 4px; font-weight: 600;
                        text-align: left; }}
    QPushButton#Link:hover {{ color: {t.gold}; }}

    /* the matrix */
    QScrollArea#Scroll, QWidget#ScrollBody {{ background: {t.window}; border: none; }}
    QLabel#SchoolHead {{ color: {t.ink}; font-weight: 700; font-size: {10.5 * s:.1f}pt; }}
    QLabel#SchoolHeadArabic {{ color: {t.gold}; }}
    QFrame#Row {{ background: {t.surface}; border: 1px solid {t.border}; border-radius: 12px; }}
    QFrame#Row:hover {{ border-color: {t.lapis}; }}
    QFrame#Row[selected="true"] {{ border: 2px solid {t.gold}; }}
    QFrame#Row QLabel {{ background: transparent; }}
    QLabel#Question {{ color: {t.ink}; font-weight: 600; font-size: {10.5 * s:.1f}pt; }}
    QLabel#Agree {{ color: {t.lapis}; background: {t.lapis_soft}; border-radius: 8px; padding: 1px 9px;
                   font-size: {8.5 * s:.1f}pt; font-weight: 700; }}
    QLabel#Differ {{ color: {t.gold}; border: 1px solid {t.gold}; border-radius: 8px; padding: 1px 9px;
                    font-size: {8.5 * s:.1f}pt; font-weight: 700; }}
    QLabel#Term {{ color: {t.muted}; font-size: {9 * s:.1f}pt; }}
    QLabel#Basis {{ color: {t.muted}; font-size: {8 * s:.1f}pt; }}
    QLabel#DraftTag {{ color: {t.gold}; font-size: {7.5 * s:.1f}pt; font-weight: 700; letter-spacing: 0.4px; }}
    QLabel#OtherTag {{ color: {t.lapis}; font-size: {8 * s:.1f}pt; font-weight: 700; }}

    /* the drawer */
    QFrame#Drawer {{ background: {t.surface}; border: none; border-left: 1px solid {t.border}; }}
    QFrame#Drawer QLabel {{ background: transparent; }}
    QLabel#DrawerTitle {{ color: {t.ink}; font-weight: 700; font-size: {12 * s:.1f}pt; }}
    QLabel#DrawerHeading {{ color: {t.gold}; font-weight: 700; font-size: {8.5 * s:.1f}pt; letter-spacing: 0.6px;
                           margin-top: 8px; }}
    QLabel#DrawerText {{ color: {t.ink}; font-size: {10 * s:.1f}pt; }}
    QLabel#DrawerMuted {{ color: {t.muted}; font-size: {9 * s:.1f}pt; }}
    QFrame#Quote {{ border: none; border-left: 3px solid {t.gold}; background: {t.window}; border-radius: 4px; }}
    QFrame#SchoolCard {{ background: {t.window}; border: 1px solid {t.border}; border-radius: 9px; }}

    /* glossary and sources */
    QFrame#Card {{ background: {t.surface}; border: 1px solid {t.border}; border-radius: 12px; }}
    QFrame#Card QLabel {{ background: transparent; }}
    QLabel#CardTitle {{ color: {t.lapis}; font-weight: 700; font-size: {11 * s:.1f}pt; }}
    QLabel#CardText {{ color: {t.ink}; font-size: {10 * s:.1f}pt; }}
    QLabel#Pill {{ background: {t.pill}; color: {t.ink}; border-radius: 7px; padding: 2px 10px; font-size: 8.5pt; }}

    QSplitter::handle {{ background: {t.border}; }}
    QScrollBar:vertical {{ background: transparent; width: 11px; margin: 2px; }}
    QScrollBar::handle:vertical {{ background: {t.border}; border-radius: 4px; min-height: 36px; }}
    QScrollBar::handle:vertical:hover {{ background: {t.muted}; }}
    QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
    QStatusBar {{ background: {t.window}; color: {t.muted}; }}
    """


def apply(app: QApplication, mode: str | None = None) -> Tokens:
    """Apply the chosen theme (default: the saved choice; "system" follows the desktop)."""
    global _current
    if "Fusion" in QStyleFactory.keys() and app.style().name().lower() != "fusion":
        app.setStyle("Fusion")
    mode = mode or theme_mode()
    _current = THEMES[mode][2] if mode in THEMES else (DARK if _is_dark_scheme() else LIGHT)
    app.setPalette(_palette(_current))
    app.setStyleSheet(stylesheet(_current))
    return _current
