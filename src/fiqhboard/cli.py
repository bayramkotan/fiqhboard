"""The command line. It never imports Qt.

The window and the command line give the same answer, both from fiqhboard.core:

    fqb topics                              the topics and their questions
    fqb topic wudu.obligatory               a topic as a table: one question per row, the four schools
    fqb topic wudu.obligatory niyya         one question in full: notes, other views, sources, evidence
    fqb term wajib                          glossary terms (all of them without a word)
    fqb sources                             the works the positions come from
    fqb config [KEY [VALUE]]                the settings the window uses
"""

import argparse
import json
import os
import sys

from fiqhboard import APP_NAME, __version__, config

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
            "examples:\n"
            f"  {prog} topics\n"
            f"  {prog} topic wudu.obligatory --differ\n"
            f"  {prog} topic wudu.obligatory niyya --lang tr\n"
            f"  {prog} term wajib\n"
            f"  {prog} config view.theme dark\n"
            "\n"
            "The data in this version is a pilot: every position is a draft whose volume and page\n"
            "are still to be checked. For learning, not fatwa."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.add_parser("version", help="the version (also -v, -V, --version)")

    def lang_and_json(p: argparse.ArgumentParser) -> None:
        p.add_argument("--lang", choices=config.CONTENT_LANGUAGES,
                       help="content language (default: the window's, now %(default)s)",
                       default=config.get("content.language"))
        p.add_argument("--json", action="store_true", help="machine-readable output")

    p = sub.add_parser("topics", help="the topics and their questions")
    lang_and_json(p)
    p = sub.add_parser("topic", help="a topic as a table, or one of its questions in full")
    p.add_argument("topic", help="topic id, e.g. wudu.obligatory (see: topics)")
    p.add_argument("question", nargs="?", help="question id, e.g. niyya")
    show = p.add_mutually_exclusive_group()
    show.add_argument("--agree", action="store_true", help="only the rows where the four schools agree")
    show.add_argument("--differ", action="store_true", help="only the rows where they differ")
    lang_and_json(p)
    p = sub.add_parser("term", help="glossary terms")
    p.add_argument("word", nargs="?", help="a term id or any word in it (all terms without one)")
    lang_and_json(p)
    p = sub.add_parser("sources", help="the works the positions come from")
    lang_and_json(p)
    p = sub.add_parser("config", help="show or change a setting")
    p.add_argument("key", nargs="?", help=", ".join(config.DEFAULTS))
    p.add_argument("value", nargs="?")
    return parser


def _utf8_output() -> None:
    """Windows writes redirected output in an old code page; Arabic would fail."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def _dump(value) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


# ------------------------------------------------------------------ commands
def cmd_topics(args) -> int:
    from fiqhboard.core.data import load, pick
    from fiqhboard.core import compare

    data = load()
    if args.json:
        _dump([{"id": t.id, "title": pick(t.title, args.lang), "path": pick(t.path, args.lang),
                "questions": [{"id": q.id, "text": pick(q.text, args.lang), "agreement": compare.agreement(q)}
                              for q in t.questions]} for t in data.topics])
        return 0
    for t in data.topics:
        print(f"{t.id}   {' › '.join(pick(t.path, args.lang))} › {pick(t.title, args.lang)}")
        for q in t.questions:
            mark = "=" if compare.agreement(q) == compare.AGREE else "≠"
            print(f"   {mark} {q.id:<15} {pick(q.text, args.lang)}")
        print()
    print("= the four schools agree   ≠ they differ        details:  fqb topic TOPIC [QUESTION]")
    return 0


def _position_json(data, q, p, lang) -> dict:
    from fiqhboard.core.data import cite, pick

    term = data.glossary.get(p.term) if p.term else None
    basis = data.bases.get(p.basis, {})
    return {"answer": p.answer, "label": pick(q.answer(p.answer).label, lang),
            "term": {"id": p.term, "latin": term["latin"], "ar": term["ar"]} if term else None,
            "basis": {"id": p.basis, "latin": basis.get("latin"), "ar": basis.get("ar")},
            "note": pick(p.note, lang) or None, "source": {**p.source, "cite": cite(data, p.source)},
            "status": p.status, "other": [_position_json(data, q, o, lang) for o in p.other]}


def cmd_topic(args) -> int:
    from fiqhboard.core.data import SCHOOL_IDS, cite, load, pick
    from fiqhboard.core import compare

    data = load()
    topic = data.topic(args.topic)
    if not topic:
        print(f"no topic {args.topic!r}; the topics: {', '.join(t.id for t in data.topics)}", file=sys.stderr)
        return 2
    lang = args.lang
    questions = list(topic.questions)
    if args.question:
        questions = [q for q in questions if q.id == args.question]
        if not questions:
            print(f"no question {args.question!r} in {topic.id}; its questions: "
                  f"{', '.join(q.id for q in topic.questions)}", file=sys.stderr)
            return 2
    elif args.agree or args.differ:
        want = compare.AGREE if args.agree else compare.DIFFER
        questions = [q for q in questions if compare.agreement(q) == want]

    if args.json:
        _dump({"topic": topic.id, "title": pick(topic.title, lang), "status": data.status,
               "questions": [{"id": q.id, "text": pick(q.text, lang), "agreement": compare.agreement(q),
                              "positions": {s: _position_json(data, q, q.positions[s], lang) for s in SCHOOL_IDS},
                              "evidence": [{"id": e, "ref": pick(data.evidence[e]["ref"], lang),
                                            "ar": data.evidence[e]["ar"],
                                            "text": pick(data.evidence[e].get("text"), lang) or None}
                                           for e in q.evidence]}
                             for q in questions]})
        return 0

    names = {s: pick(data.school(s)["name"], lang) for s in SCHOOL_IDS}
    width = max(len(n) for n in names.values()) + 2
    print(pick(topic.title, lang))
    print("=" * len(pick(topic.title, lang)))
    if data.status == "draft":
        print(f"[{pick(data.note, lang)}]")
    for q in questions:
        print()
        state = "the four agree" if compare.agreement(q) == compare.AGREE else "they differ"
        print(f"{q.id}: {pick(q.text, lang)}   ({state})")
        for s in SCHOOL_IDS:
            p = q.positions[s]
            term = data.glossary.get(p.term) if p.term else None
            term_text = f"{term['latin']} {term['ar']}" if term else ""
            basis = data.bases.get(p.basis, {}).get("latin", "")
            other = f"  +{len(p.other)} other view" if p.other else ""
            print(f"  {names[s]:<{width}}{pick(q.answer(p.answer).label, lang):<24}{term_text:<18}{basis}{other}")
        if not args.question:
            continue
        for s in SCHOOL_IDS:
            p = q.positions[s]
            lines = []
            if p.note:
                lines.append(pick(p.note, lang))
            for o in p.other:
                b = data.bases.get(o.basis, {}).get("latin", "")
                lines.append(f"other view ({b}): {pick(q.answer(o.answer).label, lang)}"
                             + (f" — {pick(o.note, lang)}" if o.note else ""))
            source = cite(data, p.source)
            if source:
                lines.append(source + ("  (volume and page to be checked)" if not p.source.get("page") else ""))
            print(f"\n  {names[s]}")
            for line in lines:
                print(f"    {line}")
        if q.evidence:
            print("\n  Evidence")
            for e in q.evidence:
                ev = data.evidence[e]
                print(f"    {pick(ev['ref'], lang)}")
                print(f"      {ev['ar']}")
                if lang != "ar" and ev.get("text"):
                    print(f"      {pick(ev['text'], lang)}")
    if not args.question:
        print(f"\none question in full:  fqb topic {topic.id} QUESTION")
    return 0


def cmd_term(args) -> int:
    from fiqhboard.core.data import load, pick

    data = load()
    terms = list(data.glossary.values())
    if args.word:
        w = args.word.casefold()
        exact = [g for g in terms if g["id"] == w]
        terms = exact or [g for g in terms
                          if w in " ".join([g["id"], g["latin"], g["ar"], *g["def"].values()]).casefold()]
    if args.json:
        _dump([{"id": g["id"], "latin": g["latin"], "ar": g["ar"], "definition": pick(g["def"], args.lang)}
               for g in terms])
        return 0 if terms else 1
    if not terms:
        print(f"no term matches {args.word!r}", file=sys.stderr)
        return 1
    for g in terms:
        print(f"{g['latin']}  {g['ar']}   [{g['id']}]")
        print(f"    {pick(g['def'], args.lang)}\n")
    return 0


def cmd_sources(args) -> int:
    from fiqhboard.core.data import SCHOOL_IDS, load, pick

    data = load()
    if args.json:
        _dump(list(data.works.values()))
        return 0
    for school in (*SCHOOL_IDS, None):
        works = sorted((w for w in data.works.values() if w["school"] == school), key=lambda w: w["died"])
        if not works:
            continue
        print(pick(data.school(school)["name"], args.lang) if school else "Comparative")
        for w in works:
            print(f"    {w['title']} — {w['author']} (d. {w['died']})    {w['title_ar']} — {w['author_ar']}")
        print()
    print("Death years are hijri.")
    return 0


def cmd_config(args) -> int:
    try:
        if args.key is None:
            for key in config.DEFAULTS:
                print(f"{key} = {config.get(key)}")
            print(f"\n(kept in {config.settings_path()})")
        elif args.value is None:
            print(config.get(args.key))
        else:
            value = float(args.value) if args.key == "view.text_scale" else args.value
            config.set(args.key, value)
            print(f"{args.key} = {config.get(args.key)}")
    except (config.ConfigError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
    return 0


COMMANDS = {"topics": cmd_topics, "topic": cmd_topic, "term": cmd_term, "sources": cmd_sources,
            "config": cmd_config}


def main(argv=None) -> int:
    _utf8_output()
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in VERSION_WORDS:
        print(f"{APP_NAME} {__version__}")
        return 0
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command in COMMANDS:
        try:
            return COMMANDS[args.command](args)
        except BrokenPipeError:          # `fqb topics | head`: the reader left early, which is fine
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
            return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
