"""Set the "Last updated" date on every finished page, from git history.

Each page in docs/ gets `updated: "15 November 2026"` in its front matter:
- the date of the last commit that changed the file, or
- today, if the file has changes that are not committed yet.

Draft pages (`status: draft`) are skipped: they have no real content yet.
The date is shown at the end of the page by overrides/partials/source-file.html.

Usage (from the repository root):
    .venv/bin/python scripts/update_page_dates.py
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

DOCS = Path("docs")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def last_changed(path: Path) -> dt.date:
    """Date of the last commit for this file, or today if it has local changes."""
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if dirty:
        return dt.date.today()
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return dt.date.fromisoformat(out) if out else dt.date.today()


def human(day: dt.date) -> str:
    # "15 November 2026": no leading zero, month in words, readable everywhere.
    return f"{day.day} {day:%B %Y}"


def main() -> None:
    changed = 0
    for page in sorted(DOCS.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        match = FRONT_MATTER.match(text)
        if not match:
            continue
        meta = match.group(1)
        if re.search(r"^status:\s*draft\s*$", meta, re.MULTILINE):
            continue
        line = f'updated: "{human(last_changed(page))}"'
        if re.search(r"^updated:.*$", meta, re.MULTILINE):
            new_meta = re.sub(r"^updated:.*$", line, meta, flags=re.MULTILINE)
        else:
            new_meta = f"{meta}\n{line}"
        if new_meta != meta:
            page.write_text(text.replace(meta, new_meta, 1), encoding="utf-8")
            changed += 1
            print(f"updated {page}")
    print(f"{changed} page(s) changed")


if __name__ == "__main__":
    main()
