"""Entry points.

The same program answers to several names:
  fiqhboard, fqb    no arguments: open the window; with arguments: the command line
  fiqhboard-gui     always the window, without a console on Windows

The command line never imports Qt, so it works on a server, over SSH and in
scripts, and starts quickly.
"""

import os
import sys

from fiqhboard import APP_NAME, __version__


def gui_main() -> int:
    try:
        from PySide6.QtCore import QLoggingCategory
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("The fiqhboard window needs PySide6:  pip install PySide6\n"
              "The command line works without it; see:  fqb -h", file=sys.stderr)
        return 1

    from fiqhboard.gui.main_window import MainWindow

    if not os.environ.get("QT_LOGGING_RULES"):
        # Qt reports, for every installed font, that it cannot shape a script none of them covers:
        # hundreds of harmless lines. Only that category is silenced; a user's own QT_LOGGING_RULES wins.
        QLoggingCategory.setFilterRules("qt.text.font.db=false")
    if sys.platform == "win32":
        # without its own id, Windows groups the window under python(w).exe and shows Python's icon
        try:
            import ctypes

            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("bayramkotan.fiqhboard")
        except (AttributeError, OSError):
            pass

    app = QApplication(sys.argv[:1])
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(__version__)
    app.setDesktopFileName("fiqhboard")
    window = MainWindow()
    window.show()
    return app.exec()


def main() -> int:
    if len(sys.argv) > 1:
        from fiqhboard.cli import main as cli_main

        return cli_main(sys.argv[1:])
    return gui_main()


if __name__ == "__main__":
    raise SystemExit(main())
