"""Set the last-updated date on every finished page, from git history.

Each page in docs/ gets `updated: "2026-11-15"` in its front matter:
- the date of the last commit that changed the file, or
- today, if the file has changes that are not committed yet.

Draft pages (`status: draft`) are skipped: they have no real content yet.
The date is not shown to readers. overrides/main.html puts it in a meta tag
for search engines.

Usage (from the repository root):
    .venv/bin/python scripts/update_page_dates.py           # update the dates
    .venv/bin/python scripts/update_page_dates.py --check   # only report, change nothing
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

DOCS = Path("docs")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def last_changed(path: Path) -> dt.date:
    """Date of the last commit for this file, or today if it has local changes."""
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--", str(path)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if dirty:
        return dt.date.today()
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", str(path)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return dt.date.fromisoformat(out) if out else dt.date.today()


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale = []
    for page in sorted(DOCS.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        match = FRONT_MATTER.match(text)
        if not match:
            continue
        meta = match.group(1)
        if re.search(r"^status:\s*draft\s*$", meta, re.MULTILINE):
            continue
        line = f'updated: "{last_changed(page).isoformat()}"'
        if re.search(r"^updated:.*$", meta, re.MULTILINE):
            new_meta = re.sub(r"^updated:.*$", line, meta, flags=re.MULTILINE)
        else:
            new_meta = f"{meta}\n{line}"
        if new_meta != meta:
            stale.append(page)
            if not check:
                page.write_text(text.replace(meta, new_meta, 1), encoding="utf-8")
                print(f"updated {page}")
    if check:
        for page in stale:
            print(f"  out of date: {page}")
        print(
            f"update_page_dates: {len(stale)} page(s) need a new date"
            + (", run: .venv/bin/python scripts/update_page_dates.py" if stale else "")
        )
        return 1 if stale else 0
    print(f"{len(stale)} page(s) changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
