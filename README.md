<h1 align="center">⚖️ fiqhboard &nbsp;<sub>الفقه المقارن</sub></h1>

<p align="center">
  <strong>Comparative fiqh of the four Sunni schools</strong><br>
  <sub>Hanafi, Maliki, Shafi'i and Hanbali side by side — every ruling in its school's own words, with its source and its evidence</sub>
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
  <a href="#-how-a-comparison-is-built">How</a> •
  <a href="#-install">Install</a> •
  <a href="#%EF%B8%8F-command-line">Command line</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-license">License</a>
</p>

> **Planning (0.0.1).** This first release reserves the name and opens a welcome window. The comparison matrices, the evidence drawer, the glossary and the diagrams follow, release by release.

---

## 💡 Why fiqhboard

Comparing the four schools usually means reading four books, each in its own vocabulary. fiqhboard puts them in one table — without flattening them into one vocabulary:

- **One question per row.** A row does not ask "is it fard?"; it asks something every school can answer, such as *"Is wudu valid without an intention?"* The colours and the agree/disagree filter come from that answer.
- **Each school in its own terms.** The Hanafi *wajib* is not the Shafi'i *wajib*; a Hanbali *shart* is not a *fard*. Every cell shows the school's own term, in Arabic and in transliteration, and no term is mapped onto another school's.
- **The relied-upon view, and the others.** A cell shows the school's relied-upon position (*mu'tamad*, *mufta bihi*, *mashhur*, *asahh*) and says so; other views within the school stay one click away.
- **Nothing without a source.** Every position names the book, volume and page it comes from; every piece of evidence — verse, hadith, principle — is cited.
- **Agreement of the four is not ijma'.** When the four schools agree, fiqhboard says *the four schools agree*. Ijma' is shown only where a source claims it, attributed to that source.
- **For learning, not fatwa.** The decision diagrams teach how each school reasons; for your own situation, ask a qualified scholar.

## 🧩 How a comparison is built

```text
topic        wudu › its obligatory acts
question     Is wudu valid without an intention?
answers      valid · invalid
             ┌──────────────┬──────────────┬──────────────┬──────────────┐
             │ Hanafi       │ Maliki       │ Shafi'i      │ Hanbali      │
             ├──────────────┼──────────────┼──────────────┼──────────────┤
answer       │ valid        │ invalid      │ invalid      │ invalid      │
own term     │ sunna  سنة   │ fard  فرض    │ fard  فرض    │ shart  شرط   │
source       │ book, vol, p │ book, vol, p │ book, vol, p │ book, vol, p │
             └──────────────┴──────────────┴──────────────┴──────────────┘
evidence     hadith  bukhari:1  ·  Qur'an 5:6
```

The data lives as JSON in a separate repository, is checked by a validator (no source, no publication), and is read into SQLite so the application works offline. Hadith evidence uses the same references as [isnady](https://github.com/bayramkotan/isnady) and its data.

## 📦 Install

```bash
pip install fiqhboard
```

On Linux distributions that protect the system Python (Arch, CachyOS, Debian, Ubuntu), use `pipx install fiqhboard`, a virtual environment, or add `--break-system-packages`.

Portable applications (Windows exe, Linux AppImage, macOS) join the GitHub Releases in a coming version.

## ⌨️ Command line

| Short | Full | What it does |
|---|---|---|
| `fqb` | `fiqhboard` | Opens the window |
| `fqb -V` | `fiqhboard --version` | Prints the version (`-v`, `-V`, `--version`, `version`) |
| `fqb -h` | `fiqhboard -h` | Help |
| | `fiqhboard-gui` | The window, without a console on Windows |

The command line never loads Qt, so it runs over SSH and in scripts. Every feature of the window will also be on the command line.

## 🗺️ Roadmap

- [x] **0.0.1** — the name, the package, a welcome window
- [ ] The application skeleton: settings, themes, interface languages (English, Turkish, Arabic first), portable applications
- [ ] The data format and its validator; the data repository
- [ ] The first topic end to end: the obligatory acts of wudu, every cell sourced
- [ ] The comparison matrix and the evidence drawer
- [ ] The glossary, with a definition under every term
- [ ] Decision diagrams, one per school (the prostration of forgetfulness first)
- [ ] Export to PDF, PNG and Markdown
- [ ] Purity (*taharah*) and prayer (*salat*) in full

## 📄 License

The application is released under the [MIT License](LICENSE). Quoted works keep their own licences; modern works under copyright are cited, never reproduced.
