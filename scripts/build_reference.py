"""Build the Glossary and the Tags page from two small data files, and check tags.

Why: with hundreds of pages, a hand-kept glossary and free-typed tags drift
apart ("api", "API testing", "APIs"). One list each keeps them tidy.

Reads
-----
data/glossary.yml   every term: term, meaning, page, and stands_for for short forms
data/tags.yml       the only tags a page may use, each with one plain sentence

Writes
------
1. docs/glossary.md        the A to Z list between the BEGIN/END glossary markers
2. includes/abbreviations.md
                           hover explanations for short forms (API, BDD, CI/CD...),
                           added to every page by pymdownx.snippets auto_append
3. docs/tags.md            the "jump to a tag" list between the BEGIN/END tag markers

Checks
------
- Every topic and lesson in the menu has 1 to 3 tags, all from data/tags.yml.
- Every glossary term is unique and links to a page that exists.

Usage (from the repository root):
    .venv/bin/python scripts/build_reference.py           # update files
    .venv/bin/python scripts/build_reference.py --check   # fail if out of date or invalid
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml  # PyYAML, already installed with Zensical (requirements-docs.txt)

sys.path.insert(0, str(Path(__file__).parent))
import build_nav  # noqa: E402  (same folder; reuses the menu's page loader)

DOCS = Path("docs")
GLOSSARY_DATA = Path("data/glossary.yml")
TAGS_DATA = Path("data/tags.yml")
GLOSSARY_PAGE = DOCS / "glossary.md"
TAGS_PAGE = DOCS / "tags.md"
ABBREVIATIONS = Path("includes/abbreviations.md")

GLOSSARY_BEGIN = "<!-- BEGIN glossary (generated from data/glossary.yml, do not edit by hand) -->"
GLOSSARY_END = "<!-- END glossary -->"
TAGS_BEGIN = "<!-- BEGIN tag list (generated from data/tags.yml, do not edit by hand) -->"
TAGS_END = "<!-- END tag list -->"
MAX_TAGS = 3


class DataError(Exception):
    """Something in the data files or a page's tags needs fixing."""


def slug(text: str) -> str:
    """The same anchor the site makes for a heading or tag: 'CI/CD' -> 'cicd'."""
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_]+", "-", text)


def load_list(path: Path, required: tuple[str, ...]) -> list[dict]:
    items = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    for number, item in enumerate(items, 1):
        missing = [key for key in required if not item.get(key)]
        if missing:
            raise DataError(f"{path}: entry {number} is missing {', '.join(missing)}")
    return items


# ------------------------------------------------------------------ tags


def all_pages() -> list[build_nav.Page]:
    """Every topic and lesson that appears in the menu."""
    pages: list[build_nav.Page] = []
    stack = [topic for _, topics in build_nav.load_sections() for topic in topics]
    while stack:
        page = stack.pop()
        pages.append(page)
        stack.extend(page.children)
    return sorted(pages, key=lambda p: p.path)


def check_tags(allowed: set[str]) -> dict[str, int]:
    """Return how many pages use each tag. Raise if a page breaks the rules."""
    counts = dict.fromkeys(allowed, 0)
    problems = []
    menu_pages = {p.path for p in all_pages()}
    for path in sorted(DOCS.rglob("*.md")):
        tags = build_nav.read_meta(path).get("tags") or []
        unknown = [t for t in tags if t not in allowed]
        if unknown:
            problems.append(f"{path}: unknown tag(s) {unknown}. Use one from {TAGS_DATA}")
        if path in menu_pages and not 1 <= len(tags) <= MAX_TAGS:
            problems.append(f"{path}: give it 1 to {MAX_TAGS} tags (it has {len(tags)})")
        for tag in tags:
            if tag in counts:
                counts[tag] += 1
    if problems:
        raise DataError("\n  ".join(["page tags need fixing:", *problems]))
    return counts


def build_tag_list(tags: list[dict], counts: dict[str, int]) -> str:
    chips = []
    for tag in sorted(tags, key=lambda t: t["name"].lower()):
        name, count = tag["name"], counts[tag["name"]]
        if count == 0:
            continue  # the listing below only has tags in use
        about = tag["about"].replace('"', "&quot;")
        chips.append(
            f'<a class="zts-tag" href="#tag:{slug(name)}" title="{about}">'
            f'{name} <span class="zts-tag__count">{count}</span></a>'
        )
    return "\n".join(
        [
            TAGS_BEGIN,
            '<nav class="zts-tags" aria-label="Jump to a tag">',
            *chips,
            "</nav>",
            TAGS_END,
        ]
    )


# -------------------------------------------------------------- glossary


def check_glossary(terms: list[dict]) -> None:
    seen: dict[str, str] = {}
    for item in terms:
        key = slug(item["term"])
        if key in seen:
            raise DataError(f"{GLOSSARY_DATA}: '{item['term']}' is listed twice")
        seen[key] = item["term"]
        if not (DOCS / item["page"]).exists():
            raise DataError(
                f"{GLOSSARY_DATA}: '{item['term']}' links to docs/{item['page']}, "
                "which does not exist"
            )
        if item.get("stands_for") and not re.fullmatch(r"[A-Z0-9/&-]+", item["term"]):
            raise DataError(
                f"{GLOSSARY_DATA}: '{item['term']}': stands_for is only for short forms like API"
            )


def build_glossary(terms: list[dict]) -> str:
    ordered = sorted(terms, key=lambda t: t["term"].lower())
    letters = sorted({t["term"][0].upper() for t in ordered})
    jump = " ".join(f"[{letter}](#{letter.lower()})" for letter in letters)
    parts = [
        GLOSSARY_BEGIN,
        "",
        f'<nav class="zts-az" aria-label="Jump to a letter" markdown>{jump}</nav>',
        "",
    ]
    current = ""
    for item in ordered:
        letter = item["term"][0].upper()
        if letter != current:
            current = letter
            parts += [f"## {letter}", ""]
        title = item["term"]
        if item.get("stands_for"):
            title += f" ({item['stands_for']})"
        topic = build_nav.Page(DOCS / item["page"], build_nav.read_meta(DOCS / item["page"]))
        parts += [
            f"[](){{ #{slug(item['term'])} }}**{title}**",
            f":   {item['meaning'].strip()}",
            "",
            f"    Learn more: [{topic.title}]({item['page']})",
            "",
        ]
    parts.append(GLOSSARY_END)
    return "\n".join(parts)


def build_abbreviations(terms: list[dict]) -> str:
    lines = [
        "<!-- Generated by scripts/build_reference.py from data/glossary.yml. Do not edit by hand.",
        "     Added to every page (pymdownx.snippets auto_append) for hover explanations. -->",
        "",
    ]
    for item in sorted(terms, key=lambda t: t["term"].lower()):
        if item.get("stands_for"):
            first_sentence = re.split(r"(?<=\.)\s", item["meaning"].strip())[0]
            lines.append(f"*[{item['term']}]: {item['stands_for']}. {first_sentence}")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ main


def main() -> int:
    check = "--check" in sys.argv[1:]
    try:
        tags = load_list(TAGS_DATA, ("name", "about"))
        names = [t["name"] for t in tags]
        if len(set(names)) != len(names):
            raise DataError(f"{TAGS_DATA}: a tag is listed twice")
        counts = check_tags(set(names))
        terms = load_list(GLOSSARY_DATA, ("term", "meaning", "page"))
        check_glossary(terms)
        updates = {
            GLOSSARY_PAGE: build_nav.replace_block(
                GLOSSARY_PAGE.read_text(encoding="utf-8"),
                GLOSSARY_BEGIN,
                GLOSSARY_END,
                build_glossary(terms),
                GLOSSARY_PAGE,
            ),
            TAGS_PAGE: build_nav.replace_block(
                TAGS_PAGE.read_text(encoding="utf-8"),
                TAGS_BEGIN,
                TAGS_END,
                build_tag_list(tags, counts),
                TAGS_PAGE,
            ),
            ABBREVIATIONS: build_abbreviations(terms),
        }
    except (DataError, build_nav.NavError) as err:
        print(f"build_reference: {err}", file=sys.stderr)
        return 1

    stale = [
        p for p, new in updates.items() if not p.exists() or p.read_text(encoding="utf-8") != new
    ]
    if check:
        if stale:
            print(
                "build_reference: out of date, run: .venv/bin/python scripts/build_reference.py",
                file=sys.stderr,
            )
            for p in stale:
                print(f"  {p}", file=sys.stderr)
            return 1
        print("build_reference: glossary, tags and hover explanations are up to date")
        return 0
    for p in stale:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(updates[p], encoding="utf-8")
        print(f"updated {p}")
    unused = sorted(name for name, count in counts.items() if count == 0)
    print(f"{len(terms)} glossary terms, {len(names)} tags ({len(unused)} not used yet)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
