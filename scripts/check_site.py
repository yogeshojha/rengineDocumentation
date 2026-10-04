"""Check the built site in site/: internal links and anchors resolve, every page has its Markdown copy, llms.txt resolves."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
import os
SITE = Path(os.environ.get("SITE_DIR", ROOT / "site"))
BASE = "https://rengine.wiki/"


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])


def parse(path: Path) -> Links:
    p = Links()
    p.feed(path.read_text(encoding="utf-8", errors="replace"))
    return p


def target_file(url_path: str) -> Path | None:
    rel = unquote(url_path).lstrip("/")
    cand = SITE / rel
    if rel == "" or rel.endswith("/"):
        cand = cand / "index.html"
    if cand.is_dir():
        cand = cand / "index.html"
    return cand if cand.exists() else None


def main() -> int:
    if not SITE.exists():
        print("site/ not found. Run make build first.")
        return 1
    pages = sorted(p for p in SITE.rglob("index.html") if "assets" not in p.parts)
    cache: dict[Path, Links] = {}
    errors: list[str] = []
    for page in pages:
        if page.parent.name == "404" or page.parent == SITE / "search":
            continue
        if 'http-equiv="refresh"' in page.read_text(encoding="utf-8", errors="replace")[:600]:
            continue
        links = cache.setdefault(page, parse(page))
        page_url = "/" + str(page.parent.relative_to(SITE)).replace(".", "") + "/"
        page_url = page_url.replace("//", "/")
        for href in links.hrefs:
            if href.startswith(("mailto:", "javascript:")):
                continue
            absolute = urljoin("https://rengine.wiki" + page_url, href)
            parsed = urlparse(absolute)
            if parsed.netloc != "rengine.wiki":
                continue
            path, frag = urldefrag(parsed.path + ("#" + parsed.fragment if parsed.fragment else ""))
            tf = target_file(path)
            if tf is None:
                errors.append(f"{page.relative_to(SITE)}: broken link {href}")
                continue
            if frag and tf.suffix == ".html":
                ids = cache.setdefault(tf, parse(tf)).ids
                if unquote(frag) not in ids:
                    errors.append(f"{page.relative_to(SITE)}: missing anchor {href}")
        rel = page.parent.relative_to(SITE)
        md = SITE / ("index.md" if str(rel) == "." else f"{rel}.md")
        if not md.exists():
            errors.append(f"{page.relative_to(SITE)}: no Markdown copy at {md.relative_to(SITE)}")
    for name in ("llms.txt", "llms-full.txt"):
        if not (SITE / name).exists():
            errors.append(f"{name} missing")
    llms = (SITE / "llms.txt").read_text(encoding="utf-8") if (SITE / "llms.txt").exists() else ""
    for url in re.findall(r"\]\((https://rengine\.wiki/[^)]+)\)", llms):
        if not (SITE / url[len(BASE):]).exists():
            errors.append(f"llms.txt: {url} does not exist")
    for e in errors:
        print("error:", e)
    print(f"{len(pages)} pages checked, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
