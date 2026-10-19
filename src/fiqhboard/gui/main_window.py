"""The main window.

The first release shows a single welcome page: only working pages are added to
the window (the matrix, the glossary and the diagrams arrive with their data).
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from fiqhboard import APP_NAME, __version__

LAPIS = "#1D4777"
GOLD = "#A47E24"

SCHOOLS = [
    ("Hanafi", "الحنفي"),
    ("Maliki", "المالكي"),
    ("Shafi'i", "الشافعي"),
    ("Hanbali", "الحنبلي"),
]

NEXT = [
    "Side-by-side matrices: one question per row, the four schools in the columns",
    "Every position in each school's own terms, with the book, volume and page it comes from",
    "The evidence drawer: the verse, the hadith (from isnady-data) and the principle behind each ruling",
    "A glossary of fiqh terms in English, Turkish and Arabic",
    "Decision diagrams, one per school, for learning — not as a fatwa",
]


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} {__version__}")
        self.resize(960, 640)

        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(48, 40, 48, 40)
        outer.setSpacing(18)

        title_row = QHBoxLayout()
        title = QLabel(APP_NAME)
        title.setStyleSheet(f"font-size: 34px; font-weight: 600; color: {LAPIS};")
        arabic = QLabel("الفقه المقارن")
        arabic.setStyleSheet(f"font-size: 28px; color: {GOLD};")
        arabic.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignAbsolute | Qt.AlignmentFlag.AlignVCenter)
        title_row.addWidget(title)
        title_row.addStretch(1)
        title_row.addWidget(arabic)
        outer.addLayout(title_row)

        line = QFrame()
        line.setFixedHeight(2)
        line.setStyleSheet(f"background: {GOLD};")
        outer.addWidget(line)

        lead = QLabel("Comparative fiqh of the four Sunni schools — each ruling in its school's own words, "
                      "with its source and its evidence.")
        lead.setWordWrap(True)
        lead.setStyleSheet("font-size: 17px;")
        outer.addWidget(lead)

        chips = QHBoxLayout()
        chips.setSpacing(10)
        for name, ar in SCHOOLS:
            chip = QLabel(f"{name}  ·  {ar}")
            chip.setStyleSheet(
                f"border: 1px solid {LAPIS}; border-radius: 12px; padding: 4px 12px; font-size: 14px;")
            chips.addWidget(chip)
        chips.addStretch(1)
        outer.addLayout(chips)

        heading = QLabel("Coming next")
        heading.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {GOLD}; margin-top: 12px;")
        outer.addWidget(heading)
        for item in NEXT:
            row = QLabel(f"•  {item}")
            row.setWordWrap(True)
            row.setStyleSheet("font-size: 14px;")
            outer.addWidget(row)

        outer.addStretch(1)
        footer = QLabel(
            f'Version {__version__} · first release, reserving the name · '
            f'<a href="https://github.com/bayramkotan/fiqhboard">github.com/bayramkotan/fiqhboard</a>')
        footer.setOpenExternalLinks(True)
        footer.setStyleSheet("font-size: 12px;")
        outer.addWidget(footer)

        self.setCentralWidget(page)
