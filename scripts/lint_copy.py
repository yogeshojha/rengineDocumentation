"""Check docs/**/*.md and agent-files/**/*.md against the copy rules. Exit 1 on an error."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "docs", ROOT / "agent-files"]

BANNED = re.compile(
    r"\b(powerful|seamless(?:ly)?|robust|effortless(?:ly)?|easily|simply|just|best-in-class|cutting-edge|"
    r"blazing(?:ly)?|world-class|comprehensive|unlock(?:s|ed)?|leverag(?:e|es|ed|ing)|supercharg(?:e|es|ed)|"
    r"streamline[sd]?|empower(?:s|ed)?|holistic|elevate[sd]?|dive in|at a glance|please|game-chang\w*|"
    r"state-of-the-art|next-generation|revolutionary|delightful|magic(?:al)?|amazing|awesome)\b",
    re.I,
)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⭕✅❌]")
EMDASH = re.compile("—")
NOTE_THAT = re.compile(r"\b(e\.g\.|i\.e\.|etc\.)", re.I)
RETIRED = re.compile(r"\b(web hosts?|(?<!Find )live hosts?)\b", re.I)
SOFT = re.compile(r"\b(obviously|of course|don't worry)\b", re.I)

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def prose_lines(text: str):
    """Yield (number, line) for lines outside fences and front matter, with code spans, HTML attributes and URLs removed."""
    lines = text.split("\n")
    i = 0
    if lines and lines[0] == "---":
        i = 1
        while i < len(lines) and lines[i] != "---":
            yield i + 1, lines[i], True
            i += 1
        i += 1
    fence = None
    while i < len(lines):
        line = lines[i]
        m = FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
        elif m:
            fence = m.group(1)
        else:
            clean = re.sub(r"`+[^`]*`+", " ", line)
            clean = re.sub(r"<[^>]+>", " ", clean)
            clean = re.sub(r"\]\([^)]*\)", "]", clean)
            clean = re.sub(r"https?://\S+", " ", clean)
            clean = re.sub(r"\{[:.#][^}]*\}", " ", clean)
            yield i + 1, clean, False
        i += 1


def check(path: Path) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    allow_retired = "<!-- lint: retired nouns listed -->" in text
    for n, line, in_front in prose_lines(text):
        where = f"{rel}:{n}"
        if in_front and not line.startswith(("description:", "title:", "  - title:", "    text:", "    title:", "  text:", "install_note:")) and "text:" not in line:
            continue
        checks = [(BANNED, "banned word"), (EMOJI, "emoji"), (EMDASH, "em dash"), (NOTE_THAT, "aside")]
        if not allow_retired:
            checks.append((RETIRED, "retired noun"))
        for rx, label in checks:
            for m in rx.finditer(line):
                errors.append(f"{where}: {label} '{m.group(0)}'")
        stripped = line.strip()
        if not in_front and re.search(r"(?<![!=<>~])!(?![=~\[])", stripped) and not stripped.startswith("!!!"):
            errors.append(f"{where}: exclamation mark")
        for m in SOFT.finditer(line):
            warnings.append(f"{where}: review '{m.group(0)}'")
    return errors, warnings


def main() -> int:
    files = sorted(p for t in TARGETS if t.exists() for p in t.rglob("*.md"))
    if len(sys.argv) > 1:
        wanted = {Path(a).resolve() for a in sys.argv[1:]}
        files = [f for f in files if f.resolve() in wanted]
    all_errors, all_warnings = [], []
    for f in files:
        e, w = check(f)
        all_errors += e
        all_warnings += w
    for w in all_warnings:
        print("warning:", w)
    for e in all_errors:
        print("error:", e)
    print(f"{len(files)} files, {len(all_errors)} errors, {len(all_warnings)} warnings")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
