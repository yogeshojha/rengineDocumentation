"""Write data/repo.json from files in a reNgine checkout: CLI, installer, configuration and tool versions."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def heredoc(text: str, func: str) -> list[str]:
    m = re.search(func + r"\(\)\s*\{\s*cat <<'EOF'\n(.*?)\nEOF", text, re.S)
    if not m:
        raise SystemExit(f"usage heredoc not found in {func}")
    return m.group(1).splitlines()


def parse_cli(repo: Path) -> dict:
    path = repo / "deploy" / "rengine"
    lines = heredoc(path.read_text(), "usage")
    commands: list[dict] = []
    for line in lines[2:]:
        if not line.strip():
            continue
        m = re.match(r"^  (\S+(?: \S+)?)\s{2,}(.*)$", line)
        if m and not line.startswith("    "):
            usage, desc = m.group(1), m.group(2)
            name, _, args = usage.partition(" ")
            commands.append({"name": name, "args": args, "description": desc, "options": []})
            continue
        m = re.match(r"^\s{4,}(--\S+)\s+(.*)$", line)
        if m and commands:
            commands[-1]["options"].append({"flag": m.group(1), "description": m.group(2)})
        elif commands:
            commands[-1]["description"] += " " + line.strip()
    return {"source": "deploy/rengine", "usage": lines[0], "help": "\n".join(lines), "commands": commands}


def parse_installer(repo: Path) -> dict:
    path = repo / "install.sh"
    text = path.read_text()
    lines = heredoc(text, "usage")
    groups: list[dict] = []
    current: dict | None = None
    for line in lines[1:]:
        if not line.strip():
            continue
        if not line.startswith(" "):
            current = {"title": line.strip().rstrip(","), "items": []}
            groups.append(current)
            continue
        m = re.match(r"^  ((?:--|[A-Z])\S*)(?: (\[?<?[\w.]+>?\]?))?(?:\s{2,}(.*))?$", line)
        if m and current is not None:
            current["items"].append({"flag": m.group(1), "arg": m.group(2) or "", "description": m.group(3) or ""})
        elif current is not None and current["items"]:
            item = current["items"][-1]
            item["description"] = (item["description"] + "\n" + line.strip()).strip()
    intro = [g for g in groups if g["title"].startswith("Run without")]
    for g in intro:
        groups.remove(g)
    minimum = re.search(r'(\d+) GB is the minimum, (\d+) GB is recommended\. --force overrides\."\n\s+fi\n\s+local parent', text)
    disk = re.search(r"GB disk free on \$parent\. (\d+) GB is the minimum, (\d+) GB is recommended", text)
    return {
        "source": "install.sh",
        "usage": lines[0],
        "help": "\n".join(lines),
        "groups": groups,
        "memory_gb": {"minimum": int(minimum.group(1)), "recommended": int(minimum.group(2))} if minimum else None,
        "disk_gb": {"minimum": int(disk.group(1)), "recommended": int(disk.group(2))} if disk else None,
    }


def parse_env(repo: Path) -> dict:
    path = repo / ".env.example"
    sections: list[dict] = []
    current = {"title": "", "variables": []}
    pending: list[str] = []
    banner = False
    for raw in path.read_text().splitlines():
        line = raw.rstrip()
        if re.match(r"^# #{10,}$", line):
            banner = not banner
            if banner:
                pending = []
            continue
        if banner and line.startswith("# "):
            if current["variables"] or current["title"]:
                sections.append(current)
            current = {"title": line[2:].strip(), "variables": []}
            continue
        if not line:
            pending = []
            continue
        if line.startswith("#"):
            pending.append(line.lstrip("# ").strip())
            continue
        m = re.match(r"^([A-Z][A-Z0-9_]*)=(.*)$", line)
        if m:
            current["variables"].append({"name": m.group(1), "default": m.group(2), "comment": " ".join(pending)})
            pending = []
    sections.append(current)
    sections = [s for s in sections if s["variables"]]
    return {"source": ".env.example", "sections": sections, "count": sum(len(s["variables"]) for s in sections)}


def parse_tools(repo: Path) -> dict:
    tools: list[dict] = []
    worker = (repo / "worker" / "Dockerfile").read_text()
    m = re.search(r"go\.dev/dl/go([\d.]+)\.linux", worker)
    if m:
        tools.append({"name": "Go toolchain", "version": m.group(1), "module": "go.dev/dl", "kind": "build", "source": "worker/Dockerfile"})
    for mod, ver in re.findall(r"go install -v (\S+)@(v[\w.\-]+)", worker):
        name = mod.rstrip("/.").split("/")[-1]
        if name in ("...", "cmd") or mod.endswith("/..."):
            name = mod.split("/")[2]
        if re.fullmatch(r"v\d+", name):
            name = mod.split("/")[2]
        tools.append({"name": name, "version": ver, "module": mod, "kind": "go", "source": "worker/Dockerfile"})
    for name, ver in re.findall(r"ARG ([A-Z]+)_VERSION=(v[\w.\-]+)", worker):
        tools.append({"name": name.lower(), "version": ver, "module": "release binary", "kind": "binary", "source": "worker/Dockerfile"})
    for name, ver in re.findall(r"pip install [^\n]*?([a-z0-9_\-]+)==([\w.]+)", worker):
        tools.append({"name": name, "version": ver, "module": "PyPI", "kind": "python", "source": "worker/Dockerfile"})
    apt = re.search(r"FROM base AS development\n\n#[^\n]*\nRUN apt-get update && apt-get install -y --no-install-recommends \\\n(.*?)&& rm -rf", worker, re.S)
    packages = []
    if apt:
        packages = [p for p in re.split(r"[\s\\]+", apt.group(1)) if p]
    images: list[dict] = []
    for df in sorted(repo.glob("*/Dockerfile*")):
        for base, stage in re.findall(r"^FROM (\S+)(?: AS (\S+))?", df.read_text(), re.M):
            if ":" in base:
                images.append({"image": base, "file": str(df.relative_to(repo)), "stage": stage})
    compose = (repo / "docker-compose.prod.yml").read_text()
    for img in sorted(set(re.findall(r"image: ([a-z][\w./-]*:[\w.\-]+)\s*$", compose, re.M))):
        images.append({"image": img, "file": "docker-compose.prod.yml", "stage": ""})
    return {"tools": tools, "apt_packages": packages, "images": images}


SHORTCUT_TABLES = [
    ("frontend/src/routes/(app)/targets/+page.svelte", "SHORTCUTS", "Targets list"),
    ("frontend/src/lib/components/scans/scan-history-table.svelte", "SHORTCUTS", "Scans list"),
    ("frontend/src/lib/components/scans/results/vulnerabilities-table.svelte", "SHORTCUTS", "Vulnerabilities table"),
    ("frontend/src/lib/config/whats-new.ts", "NEW_KEYS", "What's new, events"),
    ("frontend/src/lib/config/whats-new.ts", "VISUAL_KEYS", "What's new, visual changes"),
    ("frontend/src/routes/(app)/bounty-hub/[platform]/+page.svelte", "SHORTCUTS", "Bounty reports"),
]


def ts_record(text: str, name: str) -> dict:
    m = re.search(name + r": Record<string, string> = \{(.*?)\};", text, re.S)
    return dict(re.findall(r"\[VulnState\.(\w+)\]: '([^']*)'", m.group(1))) if m else {}


def parse_shortcuts(repo: Path) -> list[dict]:
    vuln = (repo / "frontend/src/lib/config/vulnerabilities.ts").read_text()
    keys, labels = ts_record(vuln, "VULN_STATE_KEYS"), ts_record(vuln, "VULN_STATE_LABELS")
    send = re.search(r"SEND_SHORTCUT = '([^']+)'", (repo / "frontend/src/lib/config/connectors.ts").read_text()).group(1)
    consts = {
        "SEND_SHORTCUT": send,
        "Object.values(VULN_STATE_KEYS).join(' / ')": " / ".join(keys.values()),
        "Object.values(VULN_STATE_LABELS).join(', ')": ", ".join(labels.values()),
    }
    tables = []
    for rel, const, title in SHORTCUT_TABLES:
        text = (repo / rel).read_text()
        m = re.search(r"\b" + const + r": \[string, string\]\[\] = \[(.*?)\n\s*\];", text, re.S)
        if not m:
            raise SystemExit(f"shortcut table {const} not found in {rel}")
        rows = []
        for a, b in re.findall(r"\[\s*('[^']*'|[^,\]]+),\s*('[^']*'|[^\]]+?)\s*\]", m.group(1)):
            a, b = a.strip(), b.strip()
            a = a[1:-1] if a.startswith("'") else consts.get(a, a)
            b = b[1:-1] if b.startswith("'") else consts.get(b, b)
            rows.append([a, b])
        line = text[: m.start()].count("\n") + 1
        tables.append({"title": title, "source": f"{rel}:{line}", "rows": rows})
    return tables


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=str(ROOT.parent / "rengine"), help="path to a reNgine checkout")
    ap.add_argument("--out", default=str(ROOT / "data" / "repo.json"))
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    data = {
        "generated_by": "scripts/snapshot_repo.py",
        "version": (repo / "VERSION").read_text().strip(),
        "cli": parse_cli(repo),
        "installer": parse_installer(repo),
        "env": parse_env(repo),
        "tools": parse_tools(repo),
        "shortcuts": parse_shortcuts(repo),
    }
    Path(args.out).write_text(json.dumps(data, indent=1) + "\n")
    print(f"wrote {args.out}: {len(data['cli']['commands'])} commands, "
          f"{sum(len(g['items']) for g in data['installer']['groups'])} installer entries, "
          f"{data['env']['count']} variables, {len(data['tools']['tools'])} tools")


if __name__ == "__main__":
    main()
