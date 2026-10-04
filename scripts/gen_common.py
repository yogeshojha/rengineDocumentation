"""Helpers shared by the reference generators. Standard library only."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
REVISED = "2026-10-03"


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def yaml_str(value: str) -> str:
    if value == "" or re.search(r"[:#\[\]{}&*!|>'\"%@`,]|^\s|\s$|^-", value):
        return json.dumps(value, ensure_ascii=False)
    return value


def front_matter(title: str, description: str, sources: list[str], generated: str, **extra) -> str:
    lines = ["---", f"title: {yaml_str(title)}", f"description: {yaml_str(description)}", "sources:"]
    seen = []
    for s in sources:
        if s and s not in seen:
            seen.append(s)
            lines.append(f"  - {yaml_str(s)}")
    lines.append(f"revised: {REVISED}")
    lines.append(f"generated: {generated}")
    for key, value in extra.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines += [f"  - {yaml_str(str(v))}" for v in value]
        else:
            lines.append(f"{key}: {yaml_str(str(value))}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def join_words(items: list[str], last: str = "and") -> str:
    """'a', 'a and b', 'a, b and c'."""
    items = list(items)
    if len(items) < 2:
        return "".join(items)
    return ", ".join(items[:-1]) + f" {last} " + items[-1]


def gen_line(data_files: list[str], script: str) -> str:
    files = join_words([f"`data/{f}`" for f in data_files])
    return (f"This page is generated from the reNgine 3.0 source. `{script}` writes it from {files}. "
            "To change it, edit the script or refresh the data, not this page.\n{ .rn-gen }\n\n")


def cell(text) -> str:
    """Escape a value for a Markdown table cell."""
    if text is None:
        return ""
    s = str(text).replace("\n", " ").strip()
    return re.sub(r"(?<!\\)\|", r"\\|", s)


def code(text) -> str:
    """Inline code that survives backticks and pipes inside tables."""
    s = str(text)
    if "|" in s:
        return "<code>" + html.escape(s, quote=False).replace("|", "&#124;") + "</code>"
    if "`" in s:
        return f"`` {s} ``"
    return f"`{s}`"


def table(headers: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(cell(c) for c in r) + " |")
    return "\n".join(out) + "\n\n"


def strip_source(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s*source:.*$", "", text).strip()


def upper_first(text: str) -> str:
    """Capitalise the first letter only, so 'services and API health' keeps 'API'."""
    return text[:1].upper() + text[1:]


def sentence(text: str) -> str:
    t = (text or "").strip()
    if t and t[-1] not in ".:!?)`":
        t += "."
    return t


def no_semicolons(text: str) -> str:
    parts = [p.strip() for p in re.split(r";\s+", text or "") if p.strip()]
    out = []
    for p in parts:
        out.append(p[0].upper() + p[1:] if p and p[0].islower() and not re.match(r"^[a-z_.]+[:=]", p) else p)
    return ". ".join(s.rstrip(".") for s in out) + ("." if out else "")


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def write(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def source_files(*refs: str) -> list[str]:
    """Turn 'a.py:10-20; b.py (x)' into repository paths."""
    out = []
    for ref in refs:
        for part in re.split(r"[;,]\s*", ref or ""):
            m = re.match(r"^\s*([\w./\-()\[\]+]+?\.(?:py|ts|svelte|yml|yaml|sh|json|md|toml))", part)
            if m:
                out.append(m.group(1))
    return out
