"""js/README.md (shown on npmjs.com) made from README.md (shown on GitHub and PyPI), so the three never differ.

    python tools/sync_readme.py           write js/README.md
    python tools/sync_readme.py --check   exit 1 if js/README.md is not what README.md gives (the release checks it)

Pictures in README.md use absolute raw.githubusercontent.com addresses, so they show on all three sites.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NPM_NOTE = """> **About this npm package.** `npm install fiqhboard` installs a small JavaScript library that will grow
> into the client of fiqhboard's web API; it does **not** install the fiqhboard application. The application is
> installed with Python (`pip install fiqhboard`, see [Install](https://github.com/bayramkotan/fiqhboard#-install)), and the portable desktop apps will be
> on the [GitHub Releases](https://github.com/bayramkotan/fiqhboard/releases/latest) page. The npm package always
> carries the same version number as the application.
>
> ```js
> import { info, version } from "fiqhboard";
> console.log(version);      // the fiqhboard version, the same as on PyPI and GitHub
> console.log(info());       // { name, version, dataLoaded, homepage }
> ```

"""
MARK = "<!-- generated from README.md by tools/sync_readme.py — edit README.md, not this file -->\n"


def generate() -> str:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    # the note goes after the opening block (title, badges, picture, status): before the first "## " heading
    at = readme.find("\n## ")
    head, rest = (readme[:at + 1], readme[at + 1:]) if at > 0 else ("", readme)
    return MARK + head + "\n" + NPM_NOTE + rest


if __name__ == "__main__":
    target = ROOT / "js" / "README.md"
    text = generate()
    if "--check" in sys.argv:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != text:
            sys.exit("js/README.md is not in step with README.md: run  python tools/sync_readme.py")
        print("js/README.md is in step with README.md")
    else:
        target.write_text(text, encoding="utf-8", newline="\n")      # LF everywhere: the same file, the same MD5
        print(f"wrote {target.relative_to(ROOT)} ({len(text):,} characters)")
