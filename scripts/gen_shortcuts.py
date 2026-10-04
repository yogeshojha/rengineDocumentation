"""Write reference/keyboard-shortcuts.md from data/repo.json (dialog tables) and data/shortcuts-extra.json."""

from __future__ import annotations

import re

from gen_common import DOCS, front_matter, gen_line, load, table, write

SCRIPT = "scripts/gen_shortcuts.py"


def keys(text: str) -> str:
    """Render 'j / k', 'Ctrl+K', '1 to 4' as kbd elements."""
    def one(k: str) -> str:
        k = k.strip()
        if "+" in k and len(k) > 1:
            return "<kbd>" + "</kbd>+<kbd>".join(p for p in k.split("+")) + "</kbd>"
        return f"<kbd>{k}</kbd>"
    parts = re.split(r"(\s+(?:/|or|to)\s+|,\s*held)", text)
    out = []
    for p in parts:
        if re.fullmatch(r"\s+(?:/|or|to)\s+", p):
            out.append(" " + p.strip().replace("/", "or") + " ")
        elif p.startswith(","):
            out.append(", held")
        elif p.strip():
            if re.fullmatch(r"\d( \d)+", p.strip()):
                out.append(" ".join(one(x) for x in p.split()))
            else:
                out.append(one(p))
    return "".join(out)


def page() -> str:
    repo = load("repo.json")
    extra = load("shortcuts-extra.json")
    srcs = [t["source"].split(":")[0] for t in repo["shortcuts"]] + [s for g in extra["groups"] for s in g.get("sources", [])]
    out = front_matter("Keyboard shortcuts",
                       "Work through targets, scans and findings without reaching for the mouse. "
                       "This page lists the keyboard shortcuts of the reNgine interface, page by page.",
                       srcs, SCRIPT, layout="reference")
    out += gen_line(["repo.json", "shortcuts-extra.json"], SCRIPT)
    out += ("On macOS, press <kbd>Cmd</kbd> wherever this page says <kbd>Ctrl</kbd>. "
            "Single-key shortcuts do not work while you are typing in a text field. "
            "Some pages also list their keys in a dialog, which you open with their **Keyboard shortcuts** button or with <kbd>?</kbd>.\n\n")
    out += "## Pages with a shortcut dialog\n\n"
    out += "These pages show the same keys in their own dialog.\n\n"
    for t in repo["shortcuts"]:
        out += f"### {t['title']}\n\n"
        out += table(["Keys", "Action"], [[keys(a), b] for a, b in t["rows"]])
    out += "## Other shortcuts\n\n"
    out += "These shortcuts have no dialog in the interface, so this page is where you find them.\n\n"
    for g in extra["groups"]:
        out += f"### {g['title']}\n\n"
        out += table(["Keys", "Action"], [[keys(a), b] for a, b in g["rows"]])
    return out


def main() -> None:
    changed = write(DOCS / "reference" / "keyboard-shortcuts.md", page())
    print(f"gen_shortcuts: 1 page, {int(changed)} changed")


if __name__ == "__main__":
    main()
