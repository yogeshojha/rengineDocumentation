"""Write docs/reference/stages/*.md and docs/reference/default-engine.md from data/stages.json."""

from __future__ import annotations

import json
import re

from gen_common import DATA as DATA_DIR
from gen_common import DOCS, code, front_matter, gen_line, join_words, load, sentence, table, write

SCRIPT = "scripts/gen_stages.py"
DATA = "stages.json"
OUT = DOCS / "reference" / "stages"
DIM_PAGES = {
    "web_assets": "web-assets", "endpoints": "endpoints", "services": "services", "ips": "ips",
    "vulnerabilities": "vulnerabilities", "software": "software", "secrets": "secrets",
}
DIM_LABELS = {
    "web_assets": "Web assets", "endpoints": "Endpoints", "services": "Services", "ips": "IP addresses",
    "vulnerabilities": "Vulnerabilities", "software": "Software", "secrets": "Secrets",
}
PASSIVE = {
    "unchanged": "Runs unchanged",
    "degraded": "Runs, but skips what sends traffic to the target",
    "disabled": "Skipped",
}
PASSIVE_SHORT = {
    "unchanged": "Runs unchanged",
    "degraded": "Runs in part",
    "disabled": "Skipped",
}
STATUS = {
    "will_run": "Runs",
    "skipped_disabled": "Off",
    "skipped_not_applicable": "Not applicable",
    "skipped_no_input": "No input",
}
TARGET_TYPES = ["domain", "url", "ip", "ip_range", "asn"]
TYPE_LABELS = {"domain": "Domain", "url": "URL", "ip": "IP address", "ip_range": "CIDR range", "asn": "ASN"}


def reach_tag(stage: dict) -> str:
    if stage["touches_target"]:
        return '<span class="rn-tag active">Active</span>'
    return '<span class="rn-tag passive">Passive</span>'


def stage_link(sid: str, labels: dict, here: str = "") -> str:
    return f"[{labels.get(sid, sid)}]({here}{sid}.md)"


def clean_note(text: str | None) -> str:
    if not text:
        return ""
    text = re.sub(r"\s*\((?:stages|shared|api|worker)/[^)]*\)", "", text)
    return text.strip()


def fmt_default(v) -> str:
    if v is None:
        return "None"
    if isinstance(v, bool):
        return code("true" if v else "false")
    if isinstance(v, list):
        if not v:
            return "Empty"
        return ", ".join(code(x) for x in v[:12]) + (f", and {len(v) - 12} more" if len(v) > 12 else "")
    if isinstance(v, dict):
        return code(json.dumps(v))
    return code(v)


def fmt_choices(f: dict) -> str:
    parts = []
    if f.get("choices"):
        labels = f.get("choice_labels") or {}
        parts.append(", ".join(code(c) + (f" {labels[c]}" if c in labels and labels[c] != c else "") for c in f["choices"]))
    if f.get("minimum") is not None or f.get("maximum") is not None:
        lo = f.get("minimum")
        hi = f.get("maximum")
        parts.append(f"{lo if lo is not None else ''} to {hi if hi is not None else ''}".strip())
    if f.get("max_items"):
        parts.append(f"At most {f['max_items']} items")
    if f.get("max_length"):
        parts.append(f"At most {f['max_length']} characters")
    return ". ".join(parts)


def stage_page(st: dict, data: dict, labels: dict, total_steps: int, default_engine: dict) -> str:
    src = st["source"].split(":")[0]
    folder = src.rsplit("/", 1)[0] + "/"
    reach = "It sends traffic to your target." if st["touches_target"] else "It sends no traffic to your target."
    desc = f"{sentence(st['description'])} {reach}"
    out = front_matter(st["label"], desc, [st["source"], folder, "stages/registry.py"], SCRIPT,
                       layout="reference", nav_order=st["step"] * 100 + data["stages"].index(st))
    out += gen_line([DATA], SCRIPT)
    tags = [reach_tag(st), f'<span class="rn-tag neutral">{st["role"]}</span>']
    if st["always_on"]:
        tags.append('<span class="rn-tag neutral">always on</span>')
    out += " ".join(tags) + "\n\n"
    out += ("Use this page to check when the stage runs, what it needs from earlier stages, "
            "what it adds to your results and which options you can set. "
            "To see how it fits with the other stages, go to [Stages](index.md).\n\n")

    in_default = default_engine["stages"].get(st["id"], {}).get("enabled", st["default_enabled"])
    rows = [
        ["Key in the engine YAML", code(st["id"])],
        ["Group", st["group_label"]],
        ["Role", "Capability: you select it in a scan engine or a custom scan" if st["role"] == "capability" else "Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available"],
        ["Step", f"{st['step'] + 1} of {total_steps}"],
        ["Depends on", ", ".join(stage_link(d, labels) for d in st["depends_on"]) or "None"],
        ["Input", ", ".join(code(c) for c in st["consumes"]) or "None"],
        ["Output", ", ".join(code(c) for c in st["produces"]) or "None"],
        ["Adds results to", ", ".join(f"[{DIM_LABELS[w]}](../query/{DIM_PAGES[w]}.md)" for w in st["writes"] if w in DIM_LABELS) or "None"],
        ["Tools", ", ".join(code(t) for t in st["tools"]) or "None"],
        ["API keys", ", ".join(code(k) for k in st["api_keys"]) + (" (required)" if st["requires_api_keys"] else " (optional)") if st["api_keys"] else "None"],
        ["Target types", ", ".join(TYPE_LABELS.get(t, t) for t in st["target_types"])],
        ["On by default", "Yes" if st["default_enabled"] else "No"],
        ["In the Default engine", "Yes" if in_default else "No"],
        ["Sends traffic to the target", "Yes" if st["touches_target"] else "No"],
        ["At passive intensity", PASSIVE.get(st["passive_behaviour"], st["passive_behaviour"])],
    ]
    if st.get("check_of"):
        rows.append(["Findings", f"Reported as findings of {stage_link(st['check_of'], labels)}, severities " + ", ".join(f'<span class="rn-sev {s}">{s}</span>' for s in st["finding_severities"])])
    out += table(["Property", "Value"], rows)
    if st.get("writes_note"):
        out += f"What it stores in the database: {sentence(st['writes_note'])}\n\n"
    note = clean_note(st.get("passive_note") or data["intensity"].get("passive_notes", {}).get(st["id"]))
    if note and st["passive_behaviour"] == "degraded":
        out += f"What changes at passive intensity: {sentence(note)}\n\n"

    tr = st.get("transport")
    if tr:
        out += "## Request rate\n\n"
        rows = []
        for level in data["intensity"]["levels"]:
            rate = tr["rate"].get(level) if tr.get("rate") else None
            threads = tr["threads"].get(level) if tr.get("threads") else None
            rows.append([level.capitalize(), f"{rate:,}" if rate else "Not limited", threads or ""])
        out += f"The stage runs `{tr['tool']}` with a timeout of {tr['timeout_seconds']} s"
        out += f" and {tr['retries']} retry" if tr.get("retries") == 1 else (f" and {tr['retries']} retries" if tr.get("retries") else "")
        out += ". Its rate and threads depend on the intensity you choose.\n\n"
        out += table(["Intensity", "Rate per second", "Threads"], rows)

    if st["fields"]:
        out += "## Options\n\n"
        out += ("You set these options per stage: in the engine editor, in the engine YAML, "
                "or in the stage settings of a custom scan.\n\n")
        rows = []
        for f in st["fields"]:
            name = code(f["name"]) + (" (advanced)" if f.get("advanced") else "")
            rows.append([name, f.get("title") or "", f["type"], fmt_default(f.get("default")), fmt_choices(f), sentence(f.get("description") or "")])
        out += table(["Option", "Label", "Type", "Default", "Values", "Description"], rows)
    return out


def index_page(data: dict, labels: dict) -> str:
    steps = data["execution_steps"]
    out = front_matter(
        "Stages",
        "Stages are the steps of a scan. Use this page to see what each one does, which tools it runs, "
        "and whether it sends traffic to your target.",
        ["stages/registry.py", "stages/base.py", "stages/config.py", "stages/presets.py", "shared/definitions/launch.py"],
        SCRIPT, layout="reference")
    out += gen_line([DATA], SCRIPT)
    out += (f"reNgine has {data['stage_count']} stages. When you start a scan, reNgine runs the enabled stages in {len(steps)} steps. "
            "The stages of one step run in parallel, and the next step starts when every stage of the step has settled. "
            "A stage always runs after the stages it depends on. A deferrable stage that no other stage depends on runs in a later step.\n\n")
    out += ("<span class=\"rn-tag passive\">Passive</span> marks a stage that sends no traffic to your target, "
            "and <span class=\"rn-tag active\">Active</span> a stage that does. "
            "Check these tags before you scan a target that you must not touch.\n\n")
    out += ("Further down you find the intensity profiles, the presets for new scan engines, "
            "the port profiles, the built-in wordlists and the limits of focused rescans.\n\n")
    out += "## Execution steps\n\n"
    out += "The order in which reNgine runs the stages. The stages in one row run at the same time.\n\n"
    rows = []
    for i, step in enumerate(steps):
        rows.append([f"{i + 1}", ", ".join(f"{stage_link(s, labels)} {reach_tag(next(x for x in data['stages'] if x['id'] == s))}" for s in step)])
    out += table(["Step", "Stages"], rows)

    out += "## All stages\n\n"
    out += ("Every stage, with the key you use in the engine YAML, whether it sends traffic, "
            "and what it does at passive intensity.\n\n")
    rows = []
    for st in sorted(data["stages"], key=lambda x: (x["step"], x["id"])):
        rows.append([stage_link(st["id"], labels), code(st["id"]), st["group_label"], st["role"], reach_tag(st),
                     PASSIVE_SHORT[st["passive_behaviour"]], "Yes" if st["default_enabled"] else "No"])
    out += table(["Stage", "Key", "Group", "Role", "Reach", "Passive intensity", "Default"], rows)
    out += ("**Role** tells you how a stage gets into a run. You select a capability stage in a scan engine or a custom scan. "
            "A support stage runs when a stage you selected needs what it produces, or when its own input is available. "
            "An always-on stage is added as soon as any stage is selected. "
            "**Runs in part** means the stage runs but skips what sends traffic to the target. "
            "**Default** shows whether the stage is on in the catalog defaults.\n\n")

    inten = data["intensity"]
    out += "## Intensity\n\n"
    out += ("Intensity decides how hard reNgine hits your target. Use Passive when you must not send any traffic, "
            "Normal for most scans, and Aggressive when you own the target and want results faster. "
            "This is the text the interface shows for each choice.\n\n")
    out += table(["Intensity", "Interface text"], [[v["label"], v["help"]] for k, v in inten["ui_copy"].items()])
    tools = inten["rate_tools_defined"] + [t for t in inten["profiles"]["normal"] if t not in inten["rate_tools_defined"]]
    rows = []
    for t in tools:
        row = [code(t)]
        for level in inten["levels"]:
            p = inten["profiles"][level].get(t, {})
            row.append(f"{p.get('rate') or 'not limited'} / {p.get('threads')}")
        row.append(f"{inten['tool_timeout_seconds'].get(t, '')} s")
        rows.append(row)
    out += ("### Profiles\n\nEach cell shows the rate per second and the number of threads a tool uses at that intensity. "
            "Passive and Normal share one transport profile. At Passive intensity, the stages that send traffic do not run.\n\n")
    out += table(["Tool"] + [lv.capitalize() for lv in inten["levels"]] + ["Timeout"], rows)
    lim = inten["limits"]
    out += (f"With a custom transport you can set a rate of up to {lim['MAX_RATE']:,} a second, up to {lim['MAX_THREADS']:,} threads "
            f"and a timeout of up to {lim['MAX_TIMEOUT']:,} seconds.\n\n")
    out += "### Stages at passive intensity\n\n"
    out += "What still runs when you choose Passive.\n\n"
    out += table(["Behaviour", "Stages"], [
        ["Skipped", ", ".join(stage_link(s, labels) for s in inten["disabled_under_passive"])],
        ["Run in part, skipping what sends traffic to the target", ", ".join(stage_link(s, labels) for s in inten["degraded_under_passive"])],
        ["Run unchanged", ", ".join(stage_link(s, labels) for s in inten["unchanged_under_passive"])],
    ])

    out += "## Presets\n\n"
    out += ("When you create a scan engine, you start from a preset: a ready-made stage selection that you can then adjust. "
            "You pick it in the new engine dialog. "
            "The Passive Recon preset is a stage selection with passive intensity. "
            "Passive intensity itself is a separate, run-level switch.\n\n")
    rows = []
    for p in data["presets"]:
        changes = []
        for sid, cfg in p["stages"].items():
            if "enabled" in cfg:
                changes.append(("+" if cfg["enabled"] else "-") + sid)
        rows.append([p["title"], code(p["name"]), p["description"], p["intensity"].capitalize(),
                     ", ".join(code(c) for c in changes) if changes else "Catalog defaults"])
    out += table(["Preset", "Key", "Description", "Intensity", "Changes from the catalog defaults"], rows)

    pp = data.get("port_profiles") or {}
    if pp.get("profiles"):
        out += "## Port profiles\n\n"
        users = [st for st in data["stages"] if any(f["name"] == "profile" and "top-100" in (f.get("choices") or []) for f in st["fields"])]
        out += ("A port profile is the set of ports that "
                + join_words([stage_link(st["id"], labels) for st in users])
                + " checks. Choose it with the `profile` option of the stage.\n\n")
        out += table(["Profile", "Key", "Ports", "Description"],
                     [[p["label"], code(p["key"]), f"{p['approx']:,}" if p["approx"] else "", p["description"]] for p in pp["profiles"]])

    wl = data.get("wordlists") or {}
    if wl.get("builtin"):
        out += "## Wordlists\n\n"
        users = [st for st in data["stages"] if any(f["name"] == "wordlist" for f in st["fields"])]
        out += ("reNgine ships with these wordlists. "
                + join_words([stage_link(st["id"], labels) for st in users])
                + " use the wordlist of their kind by default. Upload your own in Arsenal when you need other words.\n\n")
        out += table(["Wordlist", "Key", "Kind", "Words", "Description"],
                     [[w["name"], code(w["slug"]), w["kind"], f"{w['words']:,}", w["description"]] for w in wl["builtin"]])
        out += (f"A custom wordlist can be up to {wl['max_bytes'] // 1048576} MB, "
                f"with words of up to {wl['max_word_length']} characters.\n\n")

    rs = data.get("rescan") or {}
    if rs:
        out += "## Focused rescans\n\n"
        out += ("A focused rescan runs chosen stages again on assets you pick from completed scans, "
                "without discovering the target again. These are its limits.\n\n")
        out += table(["Property", "Value"], [
            ["Stages a rescan can run", ", ".join(stage_link(s, labels) for s in rs["rescannable_stages"])],
            ["Assets per rescan", f"{rs['max_assets']:,}"],
            ["Runs per rescan", str(rs["max_scans"])],
            ["Checks per rescan", str(rs["max_templates"])],
        ])
        out += ("When you start a rescan from a dimension, reNgine seeds it with the host or the address of each row "
                "and selects these stages by default.\n\n")
        out += table(["Dimension", "Seed", "Default stages"], [
            [DIM_LABELS[d], rs["dimension_seed"].get(d, ""), ", ".join(stage_link(s, labels) for s in st)]
            for d, st in rs["dimension_stages"].items()])
    return out


def default_engine_page(data: dict, labels: dict) -> str:
    eng = data["default_engine"]
    out = front_matter(
        "Default scan engine",
        "The Default engine is the scan engine built into reNgine. "
        "Use this page to see what it runs on each type of target, and the YAML behind it.",
        ["shared/definitions/default_engine.py", "api/app/services/scan_engine/service.py", "stages/presets.py"],
        SCRIPT, layout="reference")
    out += gen_line([DATA, "default-engine.yaml"], SCRIPT)
    out += "Its name, description and intensity, and how it differs from the catalog defaults.\n\n"
    out += table(["Property", "Value"], [
        ["Name", eng["name"]],
        ["Description", eng["description"]],
        ["Intensity", eng["intensity"].capitalize()],
        ["Built in", "Yes" if eng["builtin"] else "No"],
        ["Changes from the catalog defaults", ", ".join(f"{code(k)} {'enabled' if v.get('enabled') else 'disabled'}" for k, v in eng["stages"].items())],
    ])
    out += "The engine runs every stage that is on by default, plus the vulnerability scan. The port scan is off.\n\n"
    out += ("## Stages per target type\n\nWhat a run of the Default engine does on each type of target, at Normal intensity. "
            "Use it to find out why a stage did not run on your target.\n\n")
    res = eng["resolution"]
    order = [s for step in data["execution_steps"] for s in step]
    rows = []
    for sid in order:
        row = [stage_link(sid, labels, "stages/")]
        for tt in TARGET_TYPES:
            info = res.get(tt, {}).get("normal", {}).get("stages", {}).get(sid)
            row.append(STATUS.get(info["status"], info["status"]) if info else "")
        rows.append(row)
    out += table(["Stage"] + [TYPE_LABELS[t] for t in TARGET_TYPES], rows)
    out += ("**Off** means the engine does not enable the stage. **Not applicable** means the stage does not work on this type of target. "
            "**No input** means no earlier stage produces what this stage needs.\n\n")
    yaml_text = (DATA_DIR / "default-engine.yaml").read_text(encoding="utf-8").rstrip()
    out += ("## Engine YAML\n\nThe YAML the engine editor exports for the Default engine. "
            "Use it as a starting point when you write your own engine.\n\n")
    out += "```yaml\n" + yaml_text + "\n```\n"
    return out


def main() -> None:
    data = load(DATA)
    labels = {s["id"]: s["label"] for s in data["stages"]}
    steps = len(data["execution_steps"])
    changed = 0
    wanted = {"index.md"}
    changed += write(OUT / "index.md", index_page(data, labels))
    for st in data["stages"]:
        wanted.add(f"{st['id']}.md")
        changed += write(OUT / f"{st['id']}.md", stage_page(st, data, labels, steps, data["default_engine"]))
    for stale in OUT.glob("*.md"):
        if stale.name not in wanted:
            stale.unlink()
    changed += write(DOCS / "reference" / "default-engine.md", default_engine_page(data, labels))
    print(f"gen_stages: {len(data['stages']) + 2} pages, {changed} changed")


if __name__ == "__main__":
    main()
