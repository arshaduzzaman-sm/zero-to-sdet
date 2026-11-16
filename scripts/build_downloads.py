"""Make one ZIP download per topic, with every template and example file it uses.

The pages show the main files. The ZIP has all of them, so a reader can start
from the download alone. Run it after `zensical build`; it writes into site/
only, so nothing is committed:

    .venv/bin/zensical build
    .venv/bin/python scripts/build_downloads.py

A topic in modules/<section>/<topic>/ becomes site/downloads/<topic>.zip, with
its templates/ and examples/ folders inside a folder of the same name.

Only files tracked by git go in: exactly what the public repository shows.
A local .env, a test database or a report on this computer never ends up in a
download. The files are written in a fixed order with a fixed date, so the same
files always make the same ZIP.

Each topic page links to its ZIP (`../../downloads/<topic>.zip`);
scripts/check_links.py then checks the file exists, and --check here checks
every topic page has the link.
"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

MODULES = Path("modules")
DOCS = Path("docs")
OUT = Path("site") / "downloads"
FOLDERS = ("templates", "examples")
FIXED_DATE = (2026, 1, 1, 0, 0, 0)
SITE_URL = "https://arshaduzzaman-sm.github.io/zero-to-sdet/"


def tracked_files() -> set[Path]:
    """Every file git tracks under modules/, plus files staged to be added."""
    out = subprocess.run(
        ["git", "ls-files", "-z", "--cached", str(MODULES)],
        capture_output=True,
        check=True,
    ).stdout
    return {Path(name) for name in out.decode().split("\0") if name}


def topics() -> list[tuple[str, Path, Path]]:
    """(slug, module folder, topic page) for every topic with a templates/ folder."""
    found = []
    for folder in sorted(MODULES.glob("*/*/templates")):
        module = folder.parent
        slug = module.name.replace("_", "-")
        page = DOCS / module.parent.name.replace("_", "-") / slug / "index.md"
        found.append((slug, module, page))
    return found


def link_for(slug: str) -> str:
    return f"../../downloads/{slug}.zip"


def build(slug: str, module: Path, page: Path, tracked: set[Path]) -> int:
    files = sorted(
        path
        for path in tracked
        if any(path.is_relative_to(module / name) for name in FOLDERS) and path.is_file()
    )
    url = SITE_URL + str(page.parent.relative_to(DOCS)) + "/"
    readme = (
        f"Files from Zero to SDET: {url}\n\n"
        "Open that page for what each file is for and how to use it.\n"
        "templates/ holds the files to copy into your own work.\n"
        "examples/ holds the demo code the lessons run.\n"
    )
    OUT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT / f"{slug}.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        entries = [("README.txt", readme.encode())]
        entries += [(str(p.relative_to(module)), p.read_bytes()) for p in files]
        for name, data in entries:
            info = zipfile.ZipInfo(f"{slug}/{name}", date_time=FIXED_DATE)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    return len(files)


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    problems = []
    for slug, module, page in topics():
        if not page.exists():
            problems.append(f"{module}: no topic page at {page}")
            continue
        if link_for(slug) not in page.read_text(encoding="utf-8"):
            problems.append(f"{page}: add a link to {link_for(slug)} under ## Templates")
    if problems:
        print("\n".join(problems))
        return 1
    if check_only:
        print(f"build_downloads: {len(topics())} topic pages link to their download")
        return 0
    if not Path("site/index.html").exists():
        print("Build the site first: .venv/bin/zensical build")
        return 1
    tracked = tracked_files()
    for slug, module, page in topics():
        count = build(slug, module, page, tracked)
        print(f"  {slug}.zip  {count} files")
    print(f"build_downloads: {len(topics())} downloads in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
