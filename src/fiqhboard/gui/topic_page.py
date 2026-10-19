"""A topic: one row per question, the four schools in the columns, and the evidence drawer on the right.

A row asks something every school can answer; the cell's colour is its answer, so the eye sees who stands
with whom. Under the answer: the school's own term (never mapped onto another school's), the basis it rests on
(the school's own name for its relied-upon view), and a mark when the school holds other views as well.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from fiqhboard.core import compare
from fiqhboard.core.data import SCHOOL_IDS, Data, Position, Question, Topic, cite, pick
from fiqhboard.gui import theme
from fiqhboard.gui.widgets import RIGHT, Segments, arabic, clear, content_css, direction, label, small

FILTERS = [("all", "All"), ("agree", "Four agree"), ("differ", "Differ")]
LANGS = [("en", "EN"), ("tr", "TR"), ("ar", "عربي")]

WORDS = {   # the few words of the page that belong to the content language
    "agree": {"en": "the four agree", "tr": "dördü aynı", "ar": "اتفق الأربعة"},
    "differ": {"en": "they differ", "tr": "ayrılıyorlar", "ar": "اختلفوا"},
    "other": {"en": "+{n} other view", "tr": "+{n} diğer görüş", "ar": "+{n} قول آخر"},
    "draft": {"en": "DRAFT", "tr": "TASLAK", "ar": "مسوَّدة"},
}


def word(key: str, lang: str, **kw) -> str:
    return pick(WORDS[key], lang).format(**kw)


def badge(text: str, index: int, lang: str, size: float = 9.5) -> QLabel:
    strong, soft = theme.answer_color(index)
    lab = label(text)
    lab.setStyleSheet(f"QLabel {{ background: {soft}; color: {strong}; border-radius: 8px; padding: 3px 10px; "
                      f"{content_css(lang, size, bold=True)} }}")
    return lab


def term_text(data: Data, term_id: str | None, lang: str) -> str:
    if not term_id:
        return ""
    g = data.glossary[term_id]
    return g["ar"] if lang == "ar" else f"{g['latin']} · {g['ar']}"


def basis_text(data: Data, basis_id: str, lang: str) -> str:
    b = data.bases.get(basis_id)
    if not b:
        return ""
    return b["ar"] if lang == "ar" else b["latin"]


class Row(QFrame):
    clicked = Signal(str)

    def __init__(self, data: Data, question: Question, lang: str) -> None:
        super().__init__()
        self.setObjectName("Row")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.question = question
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 12, 16, 14)
        outer.setSpacing(10)

        head = QHBoxLayout()
        text = label(pick(question.text, lang), "Question", wrap=True)
        text.setStyleSheet(f"QLabel#Question {{ {content_css(lang, 10.5, bold=True)} }}")
        head.addWidget(text, 1)
        state = compare.agreement(question)
        tag = small(word(state, lang), "Agree" if state == compare.AGREE else "Differ", lang, 8.5, bold=True)
        head.addWidget(tag, 0, Qt.AlignmentFlag.AlignTop)
        outer.addLayout(head)

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(0)
        index = {a.id: i for i, a in enumerate(question.answers)}
        for col, school in enumerate(SCHOOL_IDS):
            grid.setColumnStretch(col, 1)
            grid.addWidget(self._cell(data, question, question.positions[school], index, lang), 0, col,
                           Qt.AlignmentFlag.AlignTop)
        outer.addLayout(grid)

    @staticmethod
    def _cell(data: Data, question: Question, p: Position, index: dict, lang: str) -> QWidget:
        cell = QWidget()
        box = QVBoxLayout(cell)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(4)
        answer = question.answer(p.answer)
        line = QHBoxLayout()
        line.addWidget(badge(pick(answer.label, lang), index[p.answer], lang))
        line.addStretch(1)
        box.addLayout(line)
        if p.term:
            box.addWidget(small(term_text(data, p.term, lang), "Term", lang, 9, wrap=True))
        basis = basis_text(data, p.basis, lang)
        if basis:
            box.addWidget(small(basis, "Basis", lang, 8))
        marks = QHBoxLayout()
        marks.setSpacing(8)
        if p.other:
            marks.addWidget(small(word("other", lang, n=len(p.other)), "OtherTag", lang, 8, bold=True))
        if p.status == "draft":
            marks.addWidget(small(word("draft", lang), "DraftTag", lang, 7.5, bold=True))
        marks.addStretch(1)
        box.addLayout(marks)
        return cell

    def set_selected(self, on: bool) -> None:
        self.setProperty("selected", "true" if on else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event) -> None:   # noqa: N802 — Qt's name
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.question.id)
        super().mousePressEvent(event)


class Drawer(QScrollArea):
    """The evidence drawer: each school's position with its note, basis, source and other views; then the
    evidence and the terms the row uses."""

    def __init__(self) -> None:
        super().__init__()
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMinimumWidth(320)
        self.body = QFrame()
        self.body.setObjectName("Drawer")
        self.box = QVBoxLayout(self.body)
        self.box.setContentsMargins(22, 20, 22, 22)
        self.box.setSpacing(8)
        self.setWidget(self.body)

    def empty(self) -> None:
        clear(self.box)
        self.box.addWidget(label("Choose a row to see each school's position in its own words, the book it comes "
                                 "from, other views within the school, and the evidence.", "DrawerMuted", wrap=True))
        self.box.addStretch(1)

    def show_question(self, data: Data, q: Question, lang: str) -> None:
        clear(self.box)
        self.body.setLayoutDirection(direction(lang))
        title = label(pick(q.text, lang), "DrawerTitle", wrap=True)
        title.setStyleSheet(f"QLabel#DrawerTitle {{ {content_css(lang, 12, bold=True)} }}")
        self.box.addWidget(title)
        index = {a.id: i for i, a in enumerate(q.answers)}

        groups = compare.groups(q)
        if len(groups) == 1:
            summary = word("agree", lang)
        else:
            parts = []
            for answer_id, schools in groups:
                names = ", ".join(pick(data.school(s)["name"], lang) for s in schools)
                parts.append(f"{pick(q.answer(answer_id).label, lang)}: {names}")
            summary = "  ·  ".join(parts)
        self.box.addWidget(small(summary, "DrawerMuted", lang, 9, wrap=True))

        self.box.addWidget(label("THE FOUR SCHOOLS", "DrawerHeading"))
        for school in SCHOOL_IDS:
            self.box.addWidget(self._school_card(data, q, school, index, lang))

        if q.evidence:
            self.box.addWidget(label("EVIDENCE", "DrawerHeading"))
            for ev_id in q.evidence:
                self.box.addWidget(self._evidence(data.evidence[ev_id], lang))

        terms = [t for t in q.terms if t in data.glossary]
        if terms:
            self.box.addWidget(label("TERMS", "DrawerHeading"))
            for t in terms:
                g = data.glossary[t]
                head = label(term_text(data, t, lang), "DrawerText")
                head.setStyleSheet(f"QLabel#DrawerText {{ {content_css(lang, 10, bold=True)} }}")
                self.box.addWidget(head)
                definition = label(pick(g["def"], lang), "DrawerMuted", wrap=True)
                definition.setStyleSheet(f"QLabel#DrawerMuted {{ {content_css(lang, 9)} }}")
                self.box.addWidget(definition)

        self.box.addSpacing(10)
        self.box.addWidget(label("For learning, not fatwa: for your own situation, ask a qualified scholar.",
                                 "DrawerMuted", wrap=True))
        self.box.addStretch(1)
        self.verticalScrollBar().setValue(0)

    def _school_card(self, data: Data, q: Question, school: str, index: dict, lang: str) -> QFrame:
        p = q.positions[school]
        card = QFrame()
        card.setObjectName("SchoolCard")
        box = QVBoxLayout(card)
        box.setContentsMargins(12, 10, 12, 10)
        box.setSpacing(5)
        head = QHBoxLayout()
        s = data.school(school)
        name = label(pick(s["name"], lang), "DrawerText")
        name.setStyleSheet(f"QLabel#DrawerText {{ {content_css(lang, 10, bold=True)} }}")
        head.addWidget(name)
        head.addStretch(1)
        head.addWidget(badge(pick(q.answer(p.answer).label, lang), index[p.answer], lang, 9))
        box.addLayout(head)
        for view_i, view in enumerate((p, *p.other)):
            if view_i:
                other = small(f"{basis_text(data, view.basis, lang)} → {pick(q.answer(view.answer).label, lang)}",
                              "OtherTag", lang, 8.5, bold=True, wrap=True)
                box.addWidget(other)
            bits = [x for x in (term_text(data, view.term, lang), basis_text(data, view.basis, lang) if not view_i
                                else "") if x]
            if bits:
                box.addWidget(small("  ·  ".join(bits), "DrawerMuted", lang, 9, wrap=True))
            if view.note:
                note = label(pick(view.note, lang), "DrawerText", wrap=True)
                note.setStyleSheet(f"QLabel#DrawerText {{ {content_css(lang, 9.5)} }}")
                box.addWidget(note)
        source = cite(data, p.source)
        if source:
            if p.status == "draft" and not p.source.get("page"):
                source += "  —  volume and page to be checked"
            src = label(source, "DrawerMuted", wrap=True)
            src.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            box.addWidget(src)
        return card

    @staticmethod
    def _evidence(ev: dict, lang: str) -> QFrame:
        frame = QFrame()
        frame.setObjectName("Quote")
        box = QVBoxLayout(frame)
        box.setContentsMargins(12, 8, 12, 8)
        box.setSpacing(4)
        text = arabic(ev["ar"], 13.5, color=theme.current().ink)
        text.setWordWrap(True)
        text.setAlignment(RIGHT)
        box.addWidget(text)
        if lang != "ar" and ev.get("text"):
            box.addWidget(label(pick(ev["text"], lang), "DrawerText", wrap=True))
        ref = label(pick(ev["ref"], lang), "DrawerMuted")
        ref.setStyleSheet(f"QLabel#DrawerMuted {{ {content_css(lang, 8.5)} }}")
        box.addWidget(ref)
        return frame


class TopicPage(QWidget):
    language_requested = Signal(str)

    def __init__(self, data: Data, lang: str) -> None:
        super().__init__()
        self.setObjectName("Page")
        self.data, self.lang = data, lang
        self.topic: Topic | None = data.topics[0] if data.topics else None
        self.filter = "all"
        self.selected: str | None = None
        self.rows: dict[str, Row] = {}

        split = QSplitter(Qt.Orientation.Horizontal)
        split.setChildrenCollapsible(False)
        split.setHandleWidth(1)
        self.scroll = QScrollArea()
        self.scroll.setObjectName("Scroll")
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.body = QWidget()
        self.body.setObjectName("ScrollBody")
        self.box = QVBoxLayout(self.body)
        self.box.setContentsMargins(32, 26, 32, 28)
        self.box.setSpacing(10)
        self.scroll.setWidget(self.body)
        self.drawer = Drawer()
        split.addWidget(self.scroll)
        split.addWidget(self.drawer)
        split.setStretchFactor(0, 1)
        split.setSizes([860, 400])
        self.split = split

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(split)
        self.render()

    # ---------------------------------------------------------------- state
    def set_topic(self, topic_id: str) -> None:
        topic = self.data.topic(topic_id)
        if topic and topic is not self.topic:
            self.topic, self.selected, self.filter = topic, None, "all"
            self.render()

    def set_language(self, lang: str) -> None:
        self.lang = lang
        self.render()

    def select(self, question_id: str | None) -> None:
        self.selected = question_id
        for qid, row in self.rows.items():
            row.set_selected(qid == question_id)
        q = next((q for q in self.topic.questions if q.id == question_id), None) if self.topic else None
        if q:
            self.drawer.show_question(self.data, q, self.lang)
        else:
            self.drawer.empty()

    def _set_filter(self, key: str) -> None:
        self.filter = key
        self.render()

    # ---------------------------------------------------------------- drawing
    def render(self) -> None:
        clear(self.box)
        self.rows = {}
        lang = self.lang
        self.body.setLayoutDirection(direction(lang))
        if not self.topic:
            self.box.addWidget(label("No topics yet.", "Lead"))
            return
        t = self.topic

        top = QHBoxLayout()
        crumbs = label("  ›  ".join(pick(t.path, lang)).upper() if lang != "ar" else "  ›  ".join(pick(t.path, lang)),
                       "Crumbs")
        top.addWidget(crumbs)
        top.addStretch(1)
        top.addWidget(label("CONTENT", "FilterTitle"))
        langs = Segments(LANGS, lang)
        langs.changed.connect(self.language_requested.emit)
        top.addWidget(langs)
        self.box.addLayout(top)
        title_row = QHBoxLayout()
        title = label(pick(t.title, lang), "PageTitle")
        title.setStyleSheet(f"QLabel#PageTitle {{ {content_css(lang, 19, bold=True)} }}")
        title_row.addWidget(title)
        title_row.addStretch(1)
        if lang != "ar":
            title_row.addWidget(arabic(pick(t.title, "ar"), 19, color=theme.current().gold))
        self.box.addLayout(title_row)
        if t.lead:
            lead = label(pick(t.lead, lang), "Lead", wrap=True)
            lead.setStyleSheet(f"QLabel#Lead {{ {content_css(lang, 10.5)} }}")
            self.box.addWidget(lead)

        if self.data.status == "draft":
            draft = QFrame()
            draft.setObjectName("Draft")
            d = QHBoxLayout(draft)
            d.setContentsMargins(12, 7, 12, 7)
            note = label(pick(self.data.note, lang), wrap=True)
            note.setStyleSheet(f"QLabel {{ {content_css(lang, 9)} }}")
            d.addWidget(note)
            self.box.addWidget(draft)

        controls = QHBoxLayout()
        controls.setSpacing(10)
        controls.addWidget(label("SHOW", "FilterTitle"))
        filters = Segments(FILTERS, self.filter)
        filters.changed.connect(self._set_filter)
        controls.addWidget(filters)
        controls.addSpacing(8)
        questions = t.questions
        agree = sum(1 for q in questions if compare.agreement(q) == compare.AGREE)
        controls.addWidget(label(f"{len(questions)} questions · {agree} the four agree · "
                                 f"{len(questions) - agree} differ", "Summary"))
        controls.addStretch(1)
        self.box.addSpacing(6)
        self.box.addLayout(controls)
        self.box.addSpacing(6)

        heads = QGridLayout()
        heads.setContentsMargins(17, 0, 17, 0)
        heads.setHorizontalSpacing(12)
        for col, school in enumerate(SCHOOL_IDS):
            s = self.data.school(school)
            heads.setColumnStretch(col, 1)
            cell = QVBoxLayout()
            cell.setSpacing(0)
            name = label(pick(s["name"], lang), "SchoolHead")
            name.setStyleSheet(f"QLabel#SchoolHead {{ {content_css(lang, 10.5, bold=True)} }}")
            name.setToolTip(pick(s["eponym"], lang))
            cell.addWidget(name)
            if lang != "ar":
                sub = arabic(s["name"]["ar"], 11, color=theme.current().gold)
                sub.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignAbsolute)
                cell.addWidget(sub)
            heads.addLayout(cell, 0, col)
        self.box.addLayout(heads)

        shown = [q for q in questions if self.filter == "all" or compare.agreement(q) == self.filter]
        for q in shown:
            row = Row(self.data, q, lang)
            row.clicked.connect(self.select)
            self.rows[q.id] = row
            self.box.addWidget(row)
        if not shown:
            self.box.addWidget(label("No question in this topic matches the filter.", "Lead"))
        self.box.addStretch(1)
        self.select(self.selected if self.selected in self.rows else None)
