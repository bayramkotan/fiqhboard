"""The main window: the sidebar (pages and the topic tree), the pages, and the menus."""

from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtGui import QAction, QActionGroup, QDesktopServices, QGuiApplication, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from fiqhboard import APP_NAME, __version__, config
from fiqhboard.core import data as core_data
from fiqhboard.core.data import pick
from fiqhboard.gui import theme
from fiqhboard.gui.reference_pages import GlossaryPage, SourcesPage
from fiqhboard.gui.topic_page import TopicPage
from fiqhboard.gui.widgets import arabic, label

HOME = "https://github.com/bayramkotan/fiqhboard"
PAGES = [("topics", "Topics"), ("glossary", "Glossary"), ("sources", "Sources")]
LANG_NAMES = {"en": "English", "tr": "Türkçe", "ar": "العربية"}


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1360, 860)
        self.data = core_data.load()
        self.lang = config.get("content.language")
        self.page_key = "topics"
        self._build_menus()
        self._build()
        hints = QGuiApplication.styleHints()
        if hasattr(hints, "colorSchemeChanged"):
            hints.colorSchemeChanged.connect(lambda _s: theme.theme_mode() == "system" and self.retheme())

    # ---------------------------------------------------------------- layout
    def _build(self, topic_id: str | None = None, selected: str | None = None, flt: str = "all") -> None:
        root = QWidget()
        row = QHBoxLayout(root)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.addWidget(self._sidebar())

        self.stack = QStackedWidget()
        self.topics = TopicPage(self.data, self.lang)
        if topic_id:
            self.topics.topic = self.data.topic(topic_id) or self.topics.topic
            self.topics.filter, self.topics.selected = flt, selected
            self.topics.render()
        self.glossary = GlossaryPage(self.data, self.lang)
        self.sources = SourcesPage(self.data, self.lang)
        for page in (self.topics, self.glossary, self.sources):
            page.language_requested.connect(self.set_language)
            self.stack.addWidget(page)
        row.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.show_page(self.page_key)

    def _sidebar(self) -> QFrame:
        side = QFrame()
        side.setObjectName("Sidebar")
        side.setFixedWidth(250)
        box = QVBoxLayout(side)
        box.setContentsMargins(0, 22, 0, 16)
        box.setSpacing(6)

        mark = QHBoxLayout()
        mark.setContentsMargins(26, 0, 22, 8)
        word = label(APP_NAME, "Wordmark")
        word.setStyleSheet(f"QLabel#Wordmark {{ font-size: 17pt; font-weight: 700; color: {theme.current().sidebar_ink}; }}")
        mark.addWidget(word)
        mark.addStretch(1)
        mark.addWidget(arabic("فقه", 20, bold=True, color=theme.current().gold))
        box.addLayout(mark)

        self.nav = QListWidget()
        self.nav.setObjectName("Nav")
        self.nav.setFixedHeight(3 * 42 + 8)
        self.nav.setCursor(Qt.CursorShape.PointingHandCursor)
        for key, text in PAGES:
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, key)
            item.setSizeHint(QSize(200, 40))
            self.nav.addItem(item)
        self.nav.currentItemChanged.connect(
            lambda item, _old: item and self.show_page(item.data(Qt.ItemDataRole.UserRole)))
        box.addWidget(self.nav)

        box.addSpacing(10)
        box.addWidget(label("TOPICS", "SidebarHeading"))
        self.tree = QTreeWidget()
        self.tree.setObjectName("Topics")
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(14)
        self.tree.setRootIsDecorated(False)
        self.tree.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tree.setContentsMargins(0, 0, 0, 0)
        self.tree.setStyleSheet("QTreeWidget#Topics { margin-left: 18px; margin-right: 12px; }")
        parents: dict[tuple, QTreeWidgetItem] = {}
        for topic in self.data.topics:
            path = tuple(pick(topic.path, self.lang))
            parent = parents.get(path)
            if parent is None:
                parent = QTreeWidgetItem([" › ".join(path)])
                parent.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.tree.addTopLevelItem(parent)
                parents[path] = parent
            child = QTreeWidgetItem([pick(topic.title, self.lang)])
            child.setData(0, Qt.ItemDataRole.UserRole, topic.id)
            parent.addChild(child)
        self.tree.expandAll()
        self.tree.itemClicked.connect(self._topic_clicked)
        box.addWidget(self.tree, 1)

        foot = label(f"Version {__version__}\nPilot data · every cell a draft", "SidebarFooter")
        foot.setContentsMargins(26, 0, 16, 0)
        box.addWidget(foot)
        return side

    def _topic_clicked(self, item: QTreeWidgetItem, _col: int) -> None:
        topic_id = item.data(0, Qt.ItemDataRole.UserRole)
        if topic_id:
            self.topics.set_topic(topic_id)
            self.show_page("topics")

    def _sync_tree(self) -> None:
        current = self.topics.topic.id if self.topics.topic else None
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            for j in range(parent.childCount()):
                child = parent.child(j)
                child.setSelected(self.page_key == "topics" and child.data(0, Qt.ItemDataRole.UserRole) == current)

    def show_page(self, key: str) -> None:
        self.page_key = key
        index = [k for k, _ in PAGES].index(key)
        self.stack.setCurrentIndex(index)
        if self.nav.currentRow() != index:
            self.nav.blockSignals(True)
            self.nav.setCurrentRow(index)
            self.nav.blockSignals(False)
        self._sync_tree()

    # ---------------------------------------------------------------- menus
    def _build_menus(self) -> None:
        bar = self.menuBar()
        file_menu = bar.addMenu("&File")
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        view = bar.addMenu("&View")
        go = view.addMenu("&Go to")
        for i, (key, text) in enumerate(PAGES, start=1):
            action = QAction(text, self)
            action.setShortcut(QKeySequence(f"Ctrl+{i}"))
            action.triggered.connect(lambda _=False, k=key: self.show_page(k))
            go.addAction(action)
        view.addSeparator()

        themes = view.addMenu("&Theme")
        group = QActionGroup(self)
        modes = [("system", "Follow the system")] + [(k, v[0]) for k, v in theme.THEMES.items()]
        for key, text in modes:
            action = QAction(text, self, checkable=True)
            action.setChecked(theme.theme_mode() == key)
            if key in theme.THEMES:
                action.setToolTip(theme.THEMES[key][1])
            action.triggered.connect(lambda _=False, k=key: self.set_theme(k))
            group.addAction(action)
            themes.addAction(action)
            if key == "system":
                themes.addSeparator()

        size = view.addMenu("Text &size")
        for text, keys, step in (("Larger", QKeySequence.StandardKey.ZoomIn, 1),
                                 ("Smaller", QKeySequence.StandardKey.ZoomOut, -1),
                                 ("Reset", QKeySequence("Ctrl+0"), 0)):
            action = QAction(text, self)
            action.setShortcut(keys)
            action.triggered.connect(lambda _=False, s=step: self.change_text_size(s))
            size.addAction(action)

        langs = view.addMenu("&Content language")
        self.lang_group = QActionGroup(self)
        for code in config.CONTENT_LANGUAGES:
            action = QAction(LANG_NAMES[code], self, checkable=True)
            action.setData(code)
            action.setChecked(code == config.get("content.language"))
            action.triggered.connect(lambda _=False, c=code: self.set_language(c))
            self.lang_group.addAction(action)
            langs.addAction(action)

        help_menu = bar.addMenu("&Help")
        page = QAction("Project page", self)
        page.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(HOME)))
        help_menu.addAction(page)
        about = QAction(f"About {APP_NAME}", self)
        about.triggered.connect(self.about)
        help_menu.addAction(about)

    # ---------------------------------------------------------------- actions
    def rebuild(self) -> None:
        t = self.topics
        self._build(t.topic.id if t.topic else None, t.selected, t.filter)

    def retheme(self) -> None:
        theme.apply(QApplication.instance())
        self.rebuild()

    def set_theme(self, mode: str) -> None:
        theme.set_theme_mode(mode)
        self.retheme()

    def change_text_size(self, step: int) -> None:
        value = 1.0 if step == 0 else theme.text_scale() + step * theme.TEXT_SCALE_STEP
        theme.set_text_scale(value)
        self.retheme()

    def set_language(self, lang: str) -> None:
        if lang not in config.CONTENT_LANGUAGES:
            return
        config.set("content.language", lang)
        self.lang = lang
        for action in self.lang_group.actions():
            action.setChecked(action.data() == lang)
        self.rebuild()

    def about(self) -> None:
        QMessageBox.about(
            self, f"About {APP_NAME}",
            f"<h3>{APP_NAME} {__version__}</h3>"
            "<p>Comparative fiqh of the four Sunni schools: one question per row, each school in its own terms, "
            "every position with its source and its evidence.</p>"
            "<p>The data in this version is a pilot: every cell is a draft whose volume and page are still to be "
            "checked. For learning, not fatwa.</p>"
            f'<p><a href="{HOME}">{HOME}</a><br>MIT License · Amiri font: SIL Open Font License</p>')
