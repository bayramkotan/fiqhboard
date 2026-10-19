"""The glossary (every term with its definition, and where the schools use it differently) and the sources
(the works each position is taken from, by school, with the author's death year)."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QScrollArea, QVBoxLayout, QWidget

from fiqhboard.core.data import SCHOOL_IDS, Data, pick
from fiqhboard.gui import theme
from fiqhboard.gui.topic_page import LANGS
from fiqhboard.gui.widgets import Segments, arabic, clear, content_css, direction, label


class _Page(QWidget):
    language_requested = Signal(str)
    TITLE = ("", "")
    LEAD = ""

    def __init__(self, data: Data, lang: str) -> None:
        super().__init__()
        self.setObjectName("Page")
        self.data, self.lang = data, lang
        scroll = QScrollArea()
        scroll.setObjectName("Scroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.body = QWidget()
        self.body.setObjectName("ScrollBody")
        outer = QVBoxLayout(self.body)
        outer.setContentsMargins(32, 26, 32, 28)
        outer.setSpacing(10)

        title_row = QHBoxLayout()
        title = label(self.TITLE[0], "PageTitle")
        title.setStyleSheet(f"QLabel#PageTitle {{ font-size: {theme.pt(19):.1f}pt; font-weight: 700; }}")
        title_row.addWidget(title)
        title_row.addStretch(1)
        title_row.addWidget(arabic(self.TITLE[1], 19, color=theme.current().gold))
        outer.addLayout(title_row)
        outer.addWidget(label(self.LEAD, "Lead", wrap=True))

        controls = QHBoxLayout()
        self.add_controls(controls)
        controls.addStretch(1)
        controls.addWidget(label("CONTENT", "FilterTitle"))
        self.langs = Segments(LANGS, lang)
        self.langs.changed.connect(self.language_requested.emit)
        controls.addWidget(self.langs)
        outer.addLayout(controls)

        self.list = QVBoxLayout()
        self.list.setSpacing(10)
        outer.addLayout(self.list)
        outer.addStretch(1)
        scroll.setWidget(self.body)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(scroll)
        self.render()

    def add_controls(self, row: QHBoxLayout) -> None:
        pass

    def set_language(self, lang: str) -> None:
        self.lang = lang
        self.langs.set_current(lang)
        self.render()

    def render(self) -> None:
        raise NotImplementedError

    @staticmethod
    def card() -> tuple[QFrame, QVBoxLayout]:
        frame = QFrame()
        frame.setObjectName("Card")
        box = QVBoxLayout(frame)
        box.setContentsMargins(18, 14, 18, 14)
        box.setSpacing(6)
        return frame, box


class GlossaryPage(_Page):
    TITLE = ("Glossary", "المصطلحات")
    LEAD = ("Each term as the schools use it. A word that means one thing in one school and another in the next "
            "— wājib above all — is defined for each, and never mapped from one school onto another.")

    def add_controls(self, row: QHBoxLayout) -> None:
        self.search = QLineEdit()
        self.search.setPlaceholderText("Filter terms…")
        self.search.setClearButtonEnabled(True)
        self.search.setMaximumWidth(320)
        self.search.textChanged.connect(lambda _t: self.render())
        row.addWidget(self.search)

    def render(self) -> None:
        clear(self.list)
        lang = self.lang
        needle = self.search.text().strip().casefold() if hasattr(self, "search") else ""
        shown = 0
        for g in self.data.glossary.values():
            haystack = " ".join([g["latin"], g["ar"], *g["def"].values()]).casefold()
            if needle and needle not in haystack:
                continue
            frame, box = self.card()
            frame.setLayoutDirection(direction(lang))
            head = QHBoxLayout()
            head.addWidget(label(g["latin"], "CardTitle"))
            head.addStretch(1)
            head.addWidget(arabic(g["ar"], 15, bold=True, color=theme.current().gold))
            box.addLayout(head)
            text = label(pick(g["def"], lang), "CardText", wrap=True)
            text.setStyleSheet(f"QLabel#CardText {{ {content_css(lang, 10)} }}")
            box.addWidget(text)
            self.list.addWidget(frame)
            shown += 1
        if not shown:
            self.list.addWidget(label("No term matches.", "Lead"))


class SourcesPage(_Page):
    TITLE = ("Sources", "المصادر")
    LEAD = ("The works the positions are taken from: for each school its relied-upon texts and their commentaries, "
            "and two works of comparative fiqh. Death years are hijri. A position names the work, the volume and "
            "the page; in this pilot data the pages are still to be checked.")

    def render(self) -> None:
        clear(self.list)
        lang = self.lang
        groups = [(s, [w for w in self.data.works.values() if w["school"] == s]) for s in SCHOOL_IDS]
        groups.append((None, [w for w in self.data.works.values() if not w["school"]]))
        for school, works in groups:
            if not works:
                continue
            frame, box = self.card()
            head = QHBoxLayout()
            if school:
                s = self.data.school(school)
                name, name_ar = pick(s["name"], lang), s["name"]["ar"]
                relied = next((b for b in self.data.bases.values() if b.get("school") == school), None)
            else:
                name, name_ar, relied = {"en": "Comparative", "tr": "Mukayeseli", "ar": "الفقه المقارن"}[lang], \
                    "الخلاف العالي", None
            title = label(name, "CardTitle")
            title.setStyleSheet(f"QLabel#CardTitle {{ {content_css(lang, 11, bold=True)} }}")
            head.addWidget(title)
            if relied:
                head.addWidget(label(f"relied-upon view: {relied['latin']} · {relied['ar']}", "Pill"))
            head.addStretch(1)
            head.addWidget(arabic(name_ar, 14, bold=True, color=theme.current().gold))
            box.addLayout(head)
            for w in sorted(works, key=lambda w: w["died"]):
                row = QHBoxLayout()
                row.addWidget(label(f"{w['title']}  —  {w['author']}  (d. {w['died']})", "CardText"))
                row.addStretch(1)
                row.addWidget(arabic(f"{w['title_ar']} — {w['author_ar']}", 12.5, color=theme.current().ink))
                box.addLayout(row)
            self.list.addWidget(frame)
