"""Check every link on the built website (the site/ folder).

Internal links (always): the target page or file must exist, and so must the
#anchor if there is one. External links (with --external): each address must
answer. Run `zensical build` first.

Usage (from the repository root):
    .venv/bin/python scripts/check_links.py              # internal links only (fast)
    .venv/bin/python scripts/check_links.py --external   # also visit external sites

Exit code 1 if a link is broken. External sites that block robots (for example
LinkedIn) are listed as "could not verify", not as broken.
"""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlsplit

SITE = Path("site")
SITE_PREFIX = "/zero-to-sdet/"  # the path part of site_url in zensical.toml
# Links to the site's own public address are checked against site/ (works before launch too).
SITE_URL = "https://arshaduzzaman-sm.github.io/zero-to-sdet/"
SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:")
# Our own repository is private until Phase 9, so GitHub answers 404 to visitors.
# Remove this entry when the repository is public.
SKIP_EXTERNAL_PREFIXES = ("https://github.com/arshaduzzaman-sm/zero-to-sdet",)
# Sites that refuse automated visitors; a failure here is "could not verify".
BLOCKS_ROBOTS = ("linkedin.com",)
USER_AGENT = "Mozilla/5.0 (compatible; zero-to-sdet-link-check)"
TIMEOUT = 15


class LinkParser(HTMLParser):
    """Collect href/src values and element ids from one HTML page."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value is None:
                continue
            if name in ("href", "src"):
                self.links.append(value)
            elif name in ("id", "name"):
                self.ids.add(value)


def parse(page: Path) -> LinkParser:
    parser = LinkParser()
    parser.feed(page.read_text(encoding="utf-8", errors="replace"))
    return parser


def resolve(page: Path, target: str) -> Path:
    """Turn a link into the file it points to inside site/."""
    path = unquote(target)
    if path.startswith(SITE_PREFIX):
        file = SITE / path[len(SITE_PREFIX) :]
    elif path.startswith("/"):
        file = SITE / path.lstrip("/")
    else:
        file = page.parent / path
    if path.endswith("/") or file.is_dir():
        file = file / "index.html"
    return file.resolve()


def check_internal(pages: list[Path]) -> tuple[list[str], set[str]]:
    parsed = {p.resolve(): parse(p) for p in pages}
    problems: list[str] = []
    external: set[str] = set()
    for page, info in parsed.items():
        where = page.relative_to(SITE.resolve())
        for link in info.links:
            if link.startswith(SKIP_SCHEMES) or link.startswith("//"):
                continue
            if link.startswith(SITE_URL):
                link = SITE_PREFIX + link[len(SITE_URL) :]
            elif urlsplit(link).scheme in ("http", "https"):
                external.add(urldefrag(link)[0])
                continue
            target, anchor = urldefrag(link)
            file = resolve(page, target) if target else page
            if not file.exists():
                problems.append(f"{where}: missing page or file -> {link}")
                continue
            if anchor and file.suffix == ".html":
                ids = parsed[file].ids if file in parsed else parse(file).ids
                if unquote(anchor) not in ids:
                    problems.append(f"{where}: missing #{anchor} in {file.name} -> {link}")
    return problems, external


def visit(url: str) -> tuple[str, str | None]:
    """Return (url, None) if it answers, else (url, reason)."""
    if not url.startswith(("https://", "http://")):
        return url, "not an http(s) address"
    for method in ("HEAD", "GET"):  # some servers refuse HEAD, so try GET too
        request = urllib.request.Request(  # noqa: S310 (scheme checked above)
            url, method=method, headers={"User-Agent": USER_AGENT}
        )
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT):  # noqa: S310
                return url, None
        except urllib.error.HTTPError as err:
            if method == "GET" or err.code not in (403, 405, 501):
                return url, f"HTTP {err.code}"
        except (urllib.error.URLError, TimeoutError, OSError) as err:
            return url, str(getattr(err, "reason", err))
    return url, "no answer"


def check_external(urls: set[str]) -> tuple[list[str], list[str]]:
    to_visit = sorted(u for u in urls if not u.startswith(SKIP_EXTERNAL_PREFIXES))
    broken, unverified = [], []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for url, reason in pool.map(visit, to_visit):
            if reason is None:
                continue
            host = urlsplit(url).hostname or ""
            if any(host == d or host.endswith("." + d) for d in BLOCKS_ROBOTS):
                unverified.append(f"{url} ({reason})")
            else:
                broken.append(f"{url} ({reason})")
    return broken, unverified


def main() -> int:
    if not (SITE / "index.html").exists():
        print("check_links: site/ not found. Run: .venv/bin/zensical build", file=sys.stderr)
        return 1
    pages = sorted(SITE.rglob("*.html"))
    problems, external = check_internal(pages)
    print(f"check_links: {len(pages)} pages, {len(external)} external addresses")
    for problem in problems:
        print(f"  BROKEN  {problem}")
    if "--external" in sys.argv[1:]:
        broken, unverified = check_external(external)
        for item in broken:
            print(f"  BROKEN  {item}")
        for item in unverified:
            print(f"  could not verify (site blocks robots)  {item}")
        problems += broken
    else:
        print("  (external links not checked; add --external)")
    if problems:
        print(f"check_links: {len(problems)} broken link(s)")
        return 1
    print("check_links: no broken links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
