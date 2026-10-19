<p align="center">
  <img src="https://raw.githubusercontent.com/bayramkotan/fiqhboard/main/assets/screenshots/icon.png" width="96" alt="fiqhboard">
</p>

<h1 align="center">fiqhboard &nbsp;<sub>الفقه المقارن</sub></h1>

<p align="center">
  <strong>Comparative fiqh of the four Sunni schools</strong><br>
  <sub>Hanafi, Maliki, Shafi'i and Hanbali side by side — every position in its school's own words, with its source and its evidence</sub>
</p>

<p align="center">
  <a href="https://pypi.org/project/fiqhboard/">
    <img src="https://img.shields.io/badge/PyPI-v0.0.1-1D4777?style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI">
  </a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-A47E24?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-5B6878?style=for-the-badge" alt="Platform">
  <a href="https://www.npmjs.com/package/fiqhboard">
    <img src="https://img.shields.io/badge/npm-v0.0.1-14304F?style=for-the-badge&logo=npm" alt="npm">
  </a>
  <img src="https://img.shields.io/badge/License-MIT-D6B25E?style=for-the-badge" alt="License">
</p>

<p align="center">
  <a href="#-why-fiqhboard">Why</a> •
  <a href="#%EF%B8%8F-the-window">The window</a> •
  <a href="#-how-a-row-is-built">How a row is built</a> •
  <a href="#-install">Install</a> •
  <a href="#%EF%B8%8F-command-line">Command line</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-license">License</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/bayramkotan/fiqhboard/main/assets/screenshots/matrix-light.png" alt="The obligatory acts of wudu: one question per row, the four schools in the columns, the evidence drawer on the right">
</p>

> **Pre-alpha.** The window works end to end — the matrix, the evidence drawer, the glossary, the sources, seven themes, English, Turkish and Arabic content — on **pilot data**: two topics on wudu, every cell marked *draft*. The works are named; the volume and page of each position are still to be checked. Do not cite it yet.

---

## 💡 Why fiqhboard

Comparing the four schools usually means reading four books, each in its own vocabulary. fiqhboard puts them in one table — without flattening them into one vocabulary:

- **One question per row.** A row does not ask "is it fard?"; it asks something every school can answer, such as *"Is wudu valid without an intention?"* The colours and the agree / differ filter come from that answer.
- **Each school in its own terms.** The Hanafi *wājib* is not the Shafi'i *wājib*; a Hanbali *sharṭ* is not a *farḍ*. Every cell shows the school's own term, in Arabic and in transliteration, and no term is mapped onto another school's.
- **The relied-upon view, and the others.** A cell shows the school's relied-upon position, named the way the school names it — *al-muftā bihi*, *al-mashhūr*, *al-aṣaḥḥ*, *al-madhhab* — and marks the other views held within the school.
- **Nothing without a source.** Every position names the book, volume and page it comes from; every piece of evidence — verse, hadith, principle — is cited.
- **Agreement of the four is not ijmāʿ.** When the four schools agree, fiqhboard says *the four agree*. Ijmāʿ is shown only where a source claims it, attributed to that source.
- **For learning, not fatwa.** For your own situation, ask a qualified scholar.

## 🖥️ The window

| | |
|---|---|
| ![Nullifiers of wudu, Lapis Night theme](https://raw.githubusercontent.com/bayramkotan/fiqhboard/main/assets/screenshots/matrix-dark.png) | ![The same matrix in Arabic, right to left](https://raw.githubusercontent.com/bayramkotan/fiqhboard/main/assets/screenshots/matrix-arabic.png) |
| **Lapis Night.** Each answer has its own colour, so the eye sees who stands with whom; the words are always written too. | **Arabic, right to left.** The content switches between English, Turkish and Arabic with one click; Arabic is set in Amiri. |
| ![Turkish content, Paper theme](https://raw.githubusercontent.com/bayramkotan/fiqhboard/main/assets/screenshots/matrix-turkish.png) | ![The glossary](https://raw.githubusercontent.com/bayramkotan/fiqhboard/main/assets/screenshots/glossary.png) |
| **Turkish, Paper theme.** Seven themes: Lapis, Lapis Night, Paper, Slate, Emerald, Midnight and High Contrast — or follow the system. | **The glossary.** Every term with its definition; where the schools use a word differently, each use is defined. |

- **The matrix** — one row per question, the four schools in the columns. *Show: All · Four agree · Differ* filters the rows.
- **The evidence drawer** — click a row: each school's answer, its own term, its basis, its note, its other views and its source; then the verses and hadith, in Arabic with a translation; then the terms the row uses.
- **The glossary** and **the sources** — the works each school's positions are taken from, with the author's death year (hijri), and the name each school gives its relied-upon view.
- **View menu** — theme, text size (<kbd>Ctrl</kbd> <kbd>+</kbd> / <kbd>Ctrl</kbd> <kbd>−</kbd> / <kbd>Ctrl</kbd> <kbd>0</kbd>), content language; <kbd>Ctrl</kbd> <kbd>1</kbd>–<kbd>3</kbd> go to Topics, Glossary, Sources.

## 🧩 How a row is built

```text
topic        Purity › Wudu › The obligatory acts of wudu
question     Is wudu valid without an intention?
answers      valid · invalid
             ┌───────────────┬───────────────┬───────────────┬───────────────┐
             │ Hanafi        │ Maliki        │ Shafi'i       │ Hanbali       │
             ├───────────────┼───────────────┼───────────────┼───────────────┤
answer       │ valid         │ invalid       │ invalid       │ invalid       │
own term     │ sunna  سنة    │ farḍ  فرض     │ farḍ  فرض     │ sharṭ  شرط    │
basis        │ al-muftā bihi │ al-mashhūr    │ al-aṣaḥḥ      │ al-madhhab    │
source       │ al-Qudūrī     │ Khalīl        │ al-Nawawī     │ al-Buhūtī     │
             └───────────────┴───────────────┴───────────────┴───────────────┘
evidence     al-Bukhari 1  ·  Qur'an 5:6
```

A position that is not a draft must give a page; a term, a basis, a work or a piece of evidence that does not exist stops the data from loading. The data will move to its own repository with a validator, and be read into SQLite so the application works offline. Hadith evidence uses the same references as [isnady](https://github.com/bayramkotan/isnady).

## 📦 Install

```bash
pip install fiqhboard
fqb
```

On Linux distributions that protect the system Python (Arch, CachyOS, Debian, Ubuntu), use `pipx install fiqhboard`, a virtual environment, or add `--break-system-packages`. Portable applications (Windows exe, Linux AppImage, macOS) join the GitHub Releases in a coming version.

## ⌨️ Command line

Everything the window shows, the command line shows too — from the same core, without loading Qt, so it runs over SSH and in scripts.

| Command | What it does |
|---|---|
| `fqb` | Opens the window (`fiqhboard-gui`: the window without a console on Windows) |
| `fqb topics` | The topics and their questions; `=` the four agree, `≠` they differ |
| `fqb topic wudu.obligatory` | A topic as a table: the answer, the own term and the basis of each school |
| `fqb topic wudu.obligatory --differ` | Only the rows where the schools differ (`--agree`: only where they agree) |
| `fqb topic wudu.obligatory niyya` | One question in full: notes, other views, sources, evidence |
| `fqb term wajib` | Glossary terms (all of them without a word) |
| `fqb sources` | The works the positions come from |
| `fqb config view.theme dark` | Show or change a setting (`view.theme`, `view.text_scale`, `content.language`) |
| `fqb -V` | The version (`-v`, `-V`, `--version`, `version`) |

`--lang en|tr|ar` chooses the content language and `--json` gives machine-readable output, for every data command. `fiqhboard` is the long name of `fqb`.

```text
$ fqb topic wudu.obligatory niyya
niyya: Is wudu valid without an intention?   (they differ)
  Hanafi   valid                   sunna سنة         al-muftā bihi
  Maliki   invalid                 farḍ فرض          al-mashhūr
  Shafi'i  invalid                 farḍ فرض          al-aṣaḥḥ
  Hanbali  invalid                 sharṭ شرط         al-madhhab
```

## 🗺️ Roadmap

- [x] **0.0.1** — the name, the package, a welcome window
- [x] The interface on pilot data: the matrix, the evidence drawer, the glossary, the sources, themes, English / Turkish / Arabic content, the command line
- [ ] The data format and its validator; the data repository; every cell of wudu sourced to volume and page
- [ ] Interface languages (English, Turkish, Arabic first); portable applications
- [ ] Decision diagrams, one per school (the prostration of forgetfulness first)
- [ ] Export to PDF, PNG and Markdown
- [ ] Purity (*ṭahāra*) and prayer (*ṣalāt*) in full

## 📄 License

The application is released under the [MIT License](https://github.com/bayramkotan/fiqhboard/blob/main/LICENSE). The bundled Amiri typeface is under the SIL Open Font License. Quoted works keep their own licences; modern works under copyright are cited, never reproduced.
