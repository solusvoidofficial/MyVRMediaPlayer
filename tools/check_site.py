#!/usr/bin/env python3
"""Static checks for the My VR Media Player website.

Checks:
  1. Every local href/src resolves to a file (directory URLs -> index.html).
  2. Fragment links, including same-page ones, point at an id in the target page.
  3. Forbidden private-repo references are absent from every HTML page.
  4. Required public copy/sections are present.

No dependencies; run from anywhere: python tools/check_site.py
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}

# Applied to every *.html page. A bare LICENSE reference is the private repo file;
# the public Apache URL /licenses/LICENSE-2.0 is allowed because it is preceded by /.
FORBIDDEN_PATTERNS = [
    r"THIRD_PARTY_NOTICES\.md",
    r"(?<![\w./-])LICENSE(?![\w./-])",
    r"(?<![\w.])ui/",
]

REQUIRED = {
    "licenses/index.html": [
        "Playback engines",
        "Consolidated third-party notices",
        "Google SDK components",
        "Android Software Development Kit License",
        "Play Billing Library",
        "Google Mobile Ads SDK",
        "User Messaging Platform",
        "Play Integrity",
        "Build/test-only tools",
        "Apache License",
        "Version 2.0, January 2004",
        "Benchmark",
        "Espresso",
        "JUnit",
        "build/test-only",
        "Last updated",
    ],
    "privacy/index.html": [
        "canRequestAds()",
        "limited",
        "non-personalized",
        "US state privacy rights",
        "authorized agent",
        "non-discrimination",
        "Legal bases",
        "withdraw",
        "complaint",
        "international transfers",
        "GitHub",
        "Cloudflare",
        "Last updated",
    ],
    "index.html": [
        "User Messaging Platform",
        "limited",
        "Remove Ads",
    ],
    "README.md": [
        "limited-ads",
        "US-state",
    ],
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        for attr in ("href", "src"):
            value = data.get(attr)
            if value:
                self.links.append(value.strip())
        if data.get("id"):
            self.ids.add(data["id"])


def parse(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def resolve(page: Path, raw: str) -> tuple[Path, str] | None:
    """Return (target file, fragment) for a local URL, or None for external URLs."""
    if not raw or raw.startswith("#"):
        return None
    if raw.startswith("//"):
        return None
    parts = urlsplit(raw)
    if parts.scheme in SKIP_SCHEMES or parts.scheme:
        return None
    if not parts.path:
        return None
    path = unquote(parts.path)
    if path.startswith("/"):
        target = ROOT / path.lstrip("/")
    else:
        target = page.parent / path
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target.resolve(), unquote(parts.fragment)


def main() -> int:
    failures: list[str] = []
    pages = sorted(ROOT.rglob("*.html"))
    cache: dict[Path, PageParser] = {}

    for page in pages:
        rel = page.relative_to(ROOT).as_posix()
        text = page.read_text(encoding="utf-8")
        parser = parse(page)
        cache[page.resolve()] = parser
        for raw in parser.links:
            if raw.startswith("#"):
                fragment = unquote(raw[1:])
                if fragment and fragment not in parser.ids:
                    failures.append(f"{rel}: missing fragment #{fragment} in {rel}")
                continue
            resolved = resolve(page, raw)
            if resolved is None:
                continue
            target, fragment = resolved
            if not target.is_file():
                failures.append(f"{rel}: broken local link {raw!r} -> {target}")
                continue
            if fragment:
                target_parser = cache.get(target)
                if target_parser is None:
                    target_parser = parse(target)
                    cache[target] = target_parser
                if fragment not in target_parser.ids:
                    failures.append(
                        f"{rel}: missing fragment #{fragment} in "
                        f"{target.relative_to(ROOT).as_posix()}"
                    )

        for pattern in FORBIDDEN_PATTERNS:
            match = re.search(pattern, text)
            if match:
                failures.append(f"{rel}: forbidden reference {match.group(0)!r}")

    for rel, needles in REQUIRED.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                failures.append(f"{rel}: missing required text {needle!r}")

    if failures:
        print(f"FAIL ({len(failures)} issue(s))")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"PASS: {len(pages)} HTML pages, local links/fragments, forbidden refs and copy checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
