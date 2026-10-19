# Changelog

Every release of fiqhboard, newest first. The same version number is published on PyPI, npm and GitHub.

## [Unreleased]

The interface, on pilot data.

- **The matrix**: one row per question that every school can answer, the four schools in the columns. Each cell shows the school's answer (each answer in its own colour), its own term in transliteration and Arabic, the basis it rests on — named as the school names its relied-upon view (*al-muftā bihi*, *al-mashhūr*, *al-aṣaḥḥ*, *al-madhhab*) — a mark when the school holds other views, and a *draft* mark. *Show: All · Four agree · Differ*.
- **The evidence drawer**: click a row for each school's note, other views and source, the verses and hadith in Arabic with a translation, and the terms the row uses.
- **The glossary** and **the sources** pages; a topic tree in the sidebar.
- **Content in English, Turkish and Arabic** (right to left, in the bundled Amiri typeface), switched with one click or from View → Content language.
- **Seven themes** (Lapis, Lapis Night, Paper, Slate, Emerald, Midnight, High Contrast) or follow the system; text size with Ctrl + / Ctrl − / Ctrl 0. Settings are kept in `settings.json` in the data folder (`FIQHBOARD_DATA_DIR` to move it).
- **Pilot data**: two topics — the obligatory acts of wudu and what nullifies it, 14 questions — every position a draft whose volume and page are still to be checked. The loader refuses a position that is not a draft without a page, and any term, basis, work or evidence that does not exist.
- **The command line**, from the same core and without Qt: `fqb topics`, `fqb topic TOPIC [QUESTION] [--agree|--differ]`, `fqb term [WORD]`, `fqb sources`, `fqb config [KEY [VALUE]]`; `--lang en|tr|ar` and `--json` on every data command.
- A drawn application icon (a lapis tile, فقه in gold).
- The README rewritten with screenshots for GitHub, PyPI and npm; `js/README.md` is made from it by `tools/sync_readme.py`, and the release checks that the two agree. `tools/make_screenshots.py` makes the pictures from the real window; `tools/bump_version.py` sets the version everywhere at once.

## [0.0.1] — 2026-10-19

The first release: it reserves the name.

- The `fiqhboard` package with the commands `fiqhboard` and `fqb` (no arguments: the window; with arguments: the command line) and `fiqhboard-gui` (the window, without a console on Windows).
- A welcome window that says what fiqhboard is and what comes next.
- `fqb -V` / `--version` / `version`, and `fqb -h`.
- The README: why fiqhboard, how a comparison is built (one question per row, each school in its own terms, nothing without a source), and the roadmap.
- The npm package `fiqhboard` 0.0.1, a placeholder that reserves the name.
