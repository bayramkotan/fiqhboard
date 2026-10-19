"""The comparison data, without Qt (the window and the command line read the same thing).

For now the data is the bundled pilot file assets/data/sample.json, every position marked draft. The data
repository, its validator and the SQLite cache replace it in a later release; the shape stays the same:

    topic → questions → one answer per school (an id from the question's own answers),
            in the school's own term, with its basis (mu'tamad, by the school's own name for it) and its source.
"""

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "assets" / "data" / "sample.json"
SCHOOL_IDS = ("hanafi", "maliki", "shafii", "hanbali")
LANGUAGES = ("en", "tr", "ar")


def pick(value, lang: str) -> str:
    """One language from a {en, tr, ar} dict, falling back to English (evidence has no Arabic 'text')."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return value.get(lang) or value.get("en") or next(iter(value.values()), "")


@dataclass(frozen=True)
class Answer:
    id: str
    label: dict


@dataclass(frozen=True)
class Position:
    school: str
    answer: str
    term: str | None          # a glossary id: the school's own word for it
    basis: str                # a bases id
    source: dict
    status: str
    note: dict | None = None
    other: tuple = ()         # other views inside the school: (Position, ...)


@dataclass(frozen=True)
class Question:
    id: str
    text: dict
    answers: tuple
    positions: dict           # school id → Position
    terms: tuple = ()
    evidence: tuple = ()

    def answer(self, answer_id: str) -> Answer | None:
        return next((a for a in self.answers if a.id == answer_id), None)


@dataclass(frozen=True)
class Topic:
    id: str
    path: dict
    title: dict
    lead: dict
    questions: tuple = field(default_factory=tuple)


@dataclass(frozen=True)
class Data:
    status: str
    note: dict
    schools: tuple            # raw dicts, in SCHOOL_IDS order
    bases: dict
    works: dict               # id → dict
    evidence: dict            # id → dict
    glossary: dict            # id → dict (in file order)
    topics: tuple

    def topic(self, topic_id: str) -> Topic | None:
        return next((t for t in self.topics if t.id == topic_id), None)

    def school(self, school_id: str) -> dict:
        return next(s for s in self.schools if s["id"] == school_id)


class DataError(ValueError):
    pass


def _position(school: str, raw: dict, question_id: str, answers: set) -> Position:
    if raw.get("answer") not in answers:
        raise DataError(f"{question_id}/{school}: answer {raw.get('answer')!r} is not one of the question's answers")
    if raw.get("status") != "draft" and not (raw.get("source") or {}).get("page"):
        raise DataError(f"{question_id}/{school}: a position that is not a draft needs a page in its source")
    other = tuple(_position(school, {**o, "source": o.get("source") or raw.get("source"), "status": raw.get("status")},
                            question_id, answers) for o in raw.get("other", ()))
    return Position(school=school, answer=raw["answer"], term=raw.get("term"), basis=raw.get("basis", ""),
                    source=raw.get("source") or {}, status=raw.get("status", "draft"), note=raw.get("note"),
                    other=other)


def parse(raw: dict) -> Data:
    topics = []
    for t in raw.get("topics", ()):
        questions = []
        for q in t.get("questions", ()):
            answers = tuple(Answer(a["id"], a["label"]) for a in q["answers"])
            ids = {a.id for a in answers}
            missing = [s for s in SCHOOL_IDS if s not in q.get("positions", {})]
            if missing:
                raise DataError(f"{t['id']}/{q['id']}: no position for {', '.join(missing)}")
            positions = {s: _position(s, q["positions"][s], q["id"], ids) for s in SCHOOL_IDS}
            questions.append(Question(q["id"], q["text"], answers, positions,
                                      tuple(q.get("terms", ())), tuple(q.get("evidence", ()))))
        topics.append(Topic(t["id"], t["path"], t["title"], t.get("lead", {}), tuple(questions)))
    data = Data(status=raw.get("status", "draft"), note=raw.get("note", {}),
                schools=tuple(sorted(raw["schools"], key=lambda s: SCHOOL_IDS.index(s["id"]))),
                bases=raw.get("bases", {}), works={w["id"]: w for w in raw.get("works", ())},
                evidence={e["id"]: e for e in raw.get("evidence", ())},
                glossary={g["id"]: g for g in raw.get("glossary", ())}, topics=tuple(topics))
    for topic in data.topics:          # every reference must resolve
        for q in topic.questions:
            for ev in q.evidence:
                if ev not in data.evidence:
                    raise DataError(f"{q.id}: unknown evidence {ev}")
            for p in q.positions.values():
                for view in (p, *p.other):
                    if view.term and view.term not in data.glossary:
                        raise DataError(f"{q.id}/{p.school}: unknown term {view.term}")
                    if view.basis and view.basis not in data.bases:
                        raise DataError(f"{q.id}/{p.school}: unknown basis {view.basis}")
                    work = view.source.get("work")
                    if work and work not in data.works:
                        raise DataError(f"{q.id}/{p.school}: unknown work {work}")
    return data


@lru_cache(maxsize=1)
def load(path: str | None = None) -> Data:
    file = Path(path) if path else DATA_FILE
    return parse(json.loads(file.read_text(encoding="utf-8")))


def cite(data: Data, source: dict) -> str:
    """'al-Qudūrī, al-Mukhtaṣar' plus volume and page when known; '(page to be checked)' when not."""
    work = data.works.get(source.get("work", ""))
    if not work:
        return ""
    text = f"{work['author']}, {work['title']}"
    vol, page = source.get("vol"), source.get("page")
    if page:
        text += f", {vol}/{page}" if vol else f", p. {page}"
    return text
