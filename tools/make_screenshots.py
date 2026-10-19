"""The README pictures, made from the real window (offscreen, so it runs anywhere):

    python tools/make_screenshots.py            write assets/screenshots/*.png
    python tools/make_screenshots.py OUTDIR     write them somewhere else

Each picture is the window as a user sees it: a theme, a content language, a page, a selected row. Settings are
kept in a temporary folder, so the user's own settings are not touched.
"""

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ["FIQHBOARD_DATA_DIR"] = tempfile.mkdtemp(prefix="fiqhboard-shots-")

from PySide6.QtWidgets import QApplication  # noqa: E402

from fiqhboard import config  # noqa: E402
from fiqhboard.gui import icon, theme  # noqa: E402
from fiqhboard.gui.main_window import MainWindow  # noqa: E402

SHOTS = [   # file, theme, language, page, topic, selected row
    ("matrix-light.png", "light", "en", "topics", "wudu.obligatory", "niyya"),
    ("matrix-dark.png", "dark", "en", "topics", "wudu.nullifiers", "touch_private"),
    ("matrix-arabic.png", "light", "ar", "topics", "wudu.obligatory", "muwalat"),
    ("matrix-turkish.png", "paper", "tr", "topics", "wudu.nullifiers", "camel"),
    ("glossary.png", "light", "en", "glossary", None, None),
    ("sources.png", "emerald", "en", "sources", None, None),
]


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "assets" / "screenshots"
    out.mkdir(parents=True, exist_ok=True)
    app = QApplication(sys.argv[:1])
    theme.load_fonts()
    for name, mode, lang, page, topic, row in SHOTS:
        config.set("view.theme", mode)
        config.set("content.language", lang)
        theme.apply(app)
        window = MainWindow()
        window.resize(1400, 880)
        if topic:
            window.topics.set_topic(topic)
        window.show_page(page)
        window.show()
        if row:
            window.topics.select(row)
        for _ in range(5):
            app.processEvents()
        window.grab().save(str(out / name))
        print(f"wrote {out / name}")
        window.close()
        window.deleteLater()
        app.processEvents()
    icon.pixmap(256).save(str(out / "icon.png"))
    print(f"wrote {out / 'icon.png'}")


if __name__ == "__main__":
    main()
