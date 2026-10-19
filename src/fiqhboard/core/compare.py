"""What a row says once the four answers are in: do the four schools agree, and who stands with whom.

"The four schools agree" is never called ijma' here: ijma' is shown only where a source claims it.
"""

from collections import Counter

from fiqhboard.core.data import SCHOOL_IDS, Question

AGREE, DIFFER = "agree", "differ"


def groups(question: Question) -> list[tuple[str, list[str]]]:
    """The answers given, in the question's own answer order, each with the schools that give it."""
    out = []
    for answer in question.answers:
        schools = [s for s in SCHOOL_IDS if question.positions[s].answer == answer.id]
        if schools:
            out.append((answer.id, schools))
    return out


def agreement(question: Question) -> str:
    return AGREE if len(groups(question)) == 1 else DIFFER


def majority(question: Question) -> tuple[str, int] | None:
    """The answer most schools give and how many, when one answer has more schools than any other."""
    counts = Counter(p.answer for p in question.positions.values()).most_common()
    if len(counts) > 1 and counts[0][1] == counts[1][1]:
        return None
    return counts[0]


def lone(question: Question) -> str | None:
    """The one school that stands alone against the other three, if there is one."""
    g = groups(question)
    if len(g) == 2:
        for _, schools in g:
            if len(schools) == 1:
                return schools[0]
    return None


def summary(question: Question) -> dict:
    return {"agreement": agreement(question), "groups": groups(question), "lone": lone(question)}
