"""The command line. It never imports Qt.

Every feature of the window will also be here (fiqhboard's rule: the window
and the command line give the same answer, both from fiqhboard.core).
"""

import argparse
import os
import sys

from fiqhboard import APP_NAME, __version__

VERSION_WORDS = {"-v", "-V", "--version", "--v", "--V", "version"}


def _prog() -> str:
    name = os.path.basename(sys.argv[0] or "") if sys.argv else ""
    name = os.path.splitext(name)[0]
    return name if name in ("fiqhboard", "fqb") else "fiqhboard"


def build_parser() -> argparse.ArgumentParser:
    prog = _prog()
    parser = argparse.ArgumentParser(
        prog=prog,
        description="fiqhboard: comparative fiqh of the four Sunni schools (Hanafi, Maliki, Shafi'i, Hanbali).",
        epilog=(
            "Without arguments the window opens.\n"
            "\n"
            "commands:\n"
            f"  {prog} version       the version (also -v, -V, --version)\n"
            "\n"
            "This is the first release: it reserves the name. The comparison matrices,\n"
            "the evidence drawer, the glossary and the diagrams follow."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("command", nargs="?", choices=["version"], help=argparse.SUPPRESS)
    return parser


def _utf8_output() -> None:
    """Windows writes redirected output in an old code page; Arabic would fail."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main(argv=None) -> int:
    _utf8_output()
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in VERSION_WORDS:
        print(f"{APP_NAME} {__version__}")
        return 0
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "version":
        print(f"{APP_NAME} {__version__}")
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
