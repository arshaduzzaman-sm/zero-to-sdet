"""List finished pages whose text reads harder than school grade 8.

The brief asks for a reading level around grade 6 to 8 (the 10-year-old test).
This uses the Flesch-Kincaid grade level:

    grade = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59

Only the prose is measured: front matter, code, tables, HTML and headings are
left out. Syllables are counted with pyphen (a hyphenation dictionary).
Draft pages are skipped.

Usage (from the repository root):
    .venv/bin/python scripts/check_readability.py            # report only
    .venv/bin/python scripts/check_readability.py --strict   # exit 1 if a page is too hard

A score is a hint, not a verdict: short technical words like "pytest" or
"PostgreSQL" can push it up. Read flagged pages aloud and simplify where it helps.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pyphen

DOCS = Path("docs")
MAX_GRADE = 8.0
MIN_WORDS = 80  # shorter pages give unreliable scores
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
SENTENCE_END = re.compile(r"[.!?]+(?:\s|$)")
DICTIONARY = pyphen.Pyphen(lang="en_US")


def prose(markdown: str) -> str:
    """Keep only the sentences a reader reads."""
    text = FRONT_MATTER.sub("", markdown)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"^(\s*)(```|~~~).*?^\1\2", " ", text, flags=re.DOTALL | re.MULTILINE)
    blocks: list[str] = []  # one entry per paragraph, list item or box title
    current: list[str] = []

    def flush() -> None:
        if current:
            block = " ".join(current)
            if not SENTENCE_END.search(block):
                block += "."  # a list item without a full stop is still one sentence
            blocks.append(block)
            current.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "|", "<", "---", "--8<--")):
            flush()  # blank lines, headings, tables and HTML end a paragraph
            continue
        starts_new = re.match(r"^(!!!|\?\?\?|\d+\.\s|[-*+]\s)", stripped)
        if starts_new:
            flush()
        stripped = re.sub(r'^(!!!|\?\?\?\+?)\s+\w+(\s+"([^"]*)")?', r"\3", stripped)
        stripped = re.sub(r"^(\d+\.|[-*+])\s+", "", stripped)  # list markers
        stripped = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", stripped)  # links -> text
        stripped = re.sub(r"\{[^}]*\}", "", stripped)  # attribute lists
        stripped = re.sub(r":[a-z0-9-]+:", "", stripped)  # icons like :lucide-bug:
        stripped = re.sub(r"<[^>]+>|`[^`]*`|[*_]", "", stripped).strip()
        if stripped:
            current.append(stripped)
        if starts_new and starts_new.group(1) in ("!!!", "???"):
            flush()  # a box title is its own sentence
    flush()
    return " ".join(blocks)


def syllables(word: str) -> int:
    return max(1, len(DICTIONARY.positions(word.lower())) + 1)


def grade(text: str) -> tuple[float, int]:
    words = WORD.findall(text)
    sentences = max(1, len(SENTENCE_END.findall(text)))
    if not words:
        return 0.0, 0
    syllable_count = sum(syllables(w) for w in words)
    score = 0.39 * (len(words) / sentences) + 11.8 * (syllable_count / len(words)) - 15.59
    return round(score, 1), len(words)


def main() -> int:
    strict = "--strict" in sys.argv[1:]
    results = []
    for page in sorted(DOCS.rglob("*.md")):
        markdown = page.read_text(encoding="utf-8")
        if re.search(r"^status:\s*draft\s*$", markdown, re.MULTILINE):
            continue
        score, words = grade(prose(markdown))
        if words >= MIN_WORDS:
            results.append((score, words, page))
    too_hard = [r for r in results if r[0] > MAX_GRADE]
    target = f"target: grade {MAX_GRADE:g} or lower"
    print(f"check_readability: {len(results)} finished pages measured ({target})")
    for score, words, page in sorted(results, reverse=True):
        mark = "TOO HARD" if score > MAX_GRADE else "ok      "
        print(f"  {mark}  grade {score:>4}  {words:>5} words  {page}")
    if too_hard:
        print(
            f"check_readability: {len(too_hard)} page(s) above grade {MAX_GRADE:g}. "
            "Read them aloud and simplify long sentences and long words."
        )
        return 1 if strict else 0
    print("check_readability: every page is easy to read")
    return 0


if __name__ == "__main__":
    sys.exit(main())
