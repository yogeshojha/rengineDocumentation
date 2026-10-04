"""Write reference/mcp-tools.md, agents/mcp/tools.md and agents/mcp/server-instructions.md from data/mcp-tools.json."""

from __future__ import annotations

import json

from gen_common import DOCS, code, front_matter, gen_line, load, sentence, table, write

SCRIPT = "scripts/gen_mcp.py"
DATA = "mcp-tools.json"
GROUP_ORDER = ["Orient", "Interrogate", "Explain", "Act"]
CAP_ORDER = ["read", "plan", "write", "launch"]
GROUP_INTRO = {
    "Orient": "Tools that help an agent find its way: projects, targets, scan engines, scan contexts, "
              "the query language, the status of a scan, and what was scanned for a target.",
    "Interrogate": "Tools that answer questions about your results: search, count and group assets, compare runs, "
                   "see what changed, and check one CVE or the mail and DNS posture of a domain.",
    "Explain": "Tools that explain one finding in full, or what the scanner did in a run.",
    "Act": "Tools that act: plan a scan, add, update or delete targets, record triage decisions, "
           "and start, pause, resume or cancel scans and focused rescans.",
}


def reach(tool: dict) -> str:
    return '<span class="rn-tag active">Active</span>' if tool["touches_target"] else '<span class="rn-tag passive">Passive</span>'


def fmt_default(p: dict) -> str:
    if p["required"]:
        return "Required"
    d = p["default"]
    if d is None:
        return "None"
    if isinstance(d, bool):
        return code("true" if d else "false")
    if isinstance(d, (list, dict)):
        return code(json.dumps(d))
    return code(d)


def constraints(p: dict) -> str:
    c = p.get("constraints") or {}
    parts = []
    if "minimum" in c or "maximum" in c:
        parts.append(f"{c.get('minimum', '')} to {c.get('maximum', '')}".strip())
    if "maxItems" in c:
        parts.append(f"At most {c['maxItems']} items")
    if "maxLength" in c:
        parts.append(f"At most {c['maxLength']} characters")
    if "enum" in c:
        parts.append(", ".join(code(v) for v in c["enum"]))
    for k, v in c.items():
        if k not in ("minimum", "maximum", "maxItems", "maxLength", "enum"):
            parts.append(f"{k} {v}")
    return ". ".join(parts)


def tools_sorted(data: dict) -> list[dict]:
    return sorted(data["tools"], key=lambda t: (GROUP_ORDER.index(t["group"]) if t["group"] in GROUP_ORDER else 9, CAP_ORDER.index(t["capability"]), t["name"]))


def reference_page(data: dict) -> str:
    srv = data["server"]
    out = front_matter(
        "MCP tools",
        f"All {len(data['tools'])} tools of the reNgine MCP server: what each one does, the capability it needs, "
        "whether it sends traffic to your target, its parameters and what it returns. "
        "Use it when you build an agent on reNgine or want to know exactly what your agent can do.",
        ["mcp/registry.py", "mcp/tools/", "mcp/capabilities.py"], SCRIPT, layout="reference")
    out += gen_line([DATA], SCRIPT)
    out += (f"Your MCP client sees and calls only the tools that the capabilities of its token allow. "
            f"The server is called `{srv['name']}`, its endpoint is `{srv['endpoint_url_shape']}`, "
            f"and it uses protocol version `{srv['protocol']}`. "
            "To decide what a token may do, see [Capabilities and tokens](../agents/mcp/capabilities.md). "
            "Some tools also have a Telegram command that runs the same tool, listed under **Telegram command**.\n\n")
    out += "## All tools\n\n"
    out += ("The tools are grouped by what they help an agent do. "
            "**Reach** tells you whether a tool sends traffic to your target. Select a tool to see its parameters and what it returns.\n\n")
    rows = []
    for t in tools_sorted(data):
        rows.append([f"[{code(t['name'])}](#{t['name']})", t["group"], t["capability"], reach(t), t["title"]])
    out += table(["Tool", "Group", "Capability", "Reach", "Title"], rows)

    for group in GROUP_ORDER:
        tools = [t for t in tools_sorted(data) if t["group"] == group]
        if not tools:
            continue
        out += f"## {group}\n\n"
        if group in GROUP_INTRO:
            out += GROUP_INTRO[group] + "\n\n"
        for t in tools:
            out += f"### {t['name']} {{ #{t['name']} }}\n\n"
            out += f"{sentence(t['description'])}\n\n"
            out += f"Title\n:   {t['title']}\n\n"
            out += f"Capability\n:   `{t['capability']}`\n\n"
            out += f"Sends traffic to the target\n:   {reach(t)} {sentence(t['traffic_note'])}\n\n"
            hints = []
            if t.get("read_only_hint"):
                hints.append("`readOnlyHint`")
            if t.get("destructive_hint"):
                hints.append("`destructiveHint`")
            if hints:
                out += f"Annotations\n:   {', '.join(hints)}\n\n"
            if t.get("chat_command"):
                out += f"Telegram command\n:   [`/{t['chat_command']}`](remote-control-commands.md#{t['chat_command']})\n\n"
            if t.get("context_tokens"):
                out += f"Context cost\n:   About {t['context_tokens']:,} tokens for its entry in `tools/list`\n\n"
            if t["params"]:
                out += "You can pass these parameters.\n\n"
                rows = [[code(p["name"]), code(p["type"]), fmt_default(p), constraints(p), sentence(p["description"])] for p in t["params"]]
                out += table(["Parameter", "Type", "Default", "Constraints", "Description"], rows)
            else:
                out += "It takes no parameters.\n\n"
            out += f"Returns\n:   {sentence(t['returns'])}\n\n"
            if t.get("examples"):
                out += "Examples, written as the tool name followed by its arguments:\n\n"
                out += "```text\n" + "\n".join(t["examples"]) + "\n```\n\n"
    return out


def overview_page(data: dict) -> str:
    out = front_matter(
        "Tools",
        f"The {len(data['tools'])} tools an AI agent can call on the reNgine MCP server, grouped by the capability a token needs to use them. "
        "Use this page to decide which capabilities to give an agent.",
        ["mcp/registry.py", "mcp/tools/", "mcp/capabilities.py"], SCRIPT, layout="pane")
    out += gen_line([DATA], SCRIPT)
    caps = {c["id"]: c for c in data["capabilities"]}
    out += '<div class="rn-split" markdown>\n<div class="rn-prose" markdown>\n\n'
    out += ("Each tool needs one capability, and a token sees only the tools of the capabilities it holds. "
            "Every token holds Read. Grant another capability when the agent needs to do more. "
            "<span class=\"rn-tag passive\">Passive</span> marks a tool that sends no traffic to your target, "
            "<span class=\"rn-tag active\">Active</span> a tool that does.\n\n")
    for cap in CAP_ORDER:
        c = caps[cap]
        tools = [t for t in tools_sorted(data) if t["capability"] == cap]
        if c["always_granted"]:
            ceiling = "Every token has this capability."
        elif c["default_ceiling"]:
            ceiling = "The instance ceiling allows it by default, so you can grant it to a token."
        else:
            ceiling = "The instance ceiling does not allow it by default. An administrator must allow it before any token can use it."
        out += f"## {c['label']}\n\n{sentence(c['description'])} {ceiling}\n\n"
        rows = [[f"[{code(t['name'])}](../../reference/mcp-tools.md#{t['name']})", reach(t), sentence(t["description"].split(". ")[0])] for t in tools]
        out += table(["Tool", "Reach", "What it does"], rows)
    out += "</div>\n<div class=\"rn-pane\" markdown>\n"
    out += '<div class="rn-pane-head"><b>Tool discovery</b><span>JSON-RPC 2.0</span></div>\n\n'
    out += "/// tab | MCP\n"
    out += '<div class="rn-pane-label">request</div>\n\n'
    out += "```json\n" + json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, indent=2) + "\n```\n\n"
    read_tools = [t["name"] for t in tools_sorted(data) if t["capability"] == "read"]
    out += '<div class="rn-pane-label">tools a read-only token sees</div>\n\n'
    out += "```text\n" + "\n".join(read_tools) + "\n```\n"
    out += "///\n\n"
    out += "/// tab | Call\n"
    out += '<div class="rn-pane-label">tools/call</div>\n\n'
    call = {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "resolve_target", "arguments": {"target": "example.com"}}}
    out += "```json\n" + json.dumps(call, indent=2) + "\n```\n"
    out += "///\n\n"
    out += "</div>\n</div>\n\n"
    out += "For the parameters and the return shape of each tool, see the [MCP tools reference](../../reference/mcp-tools.md).\n"
    return out


def instructions_page(data: dict) -> str:
    srv = data["server"]
    out = front_matter(
        "Server instructions",
        "When an MCP client connects, reNgine sends it a short set of instructions on how to use its tools. "
        "Read them here to know what your agent is told, along with the protocol details of the server.",
        ["mcp/server.py", "mcp/protocol.py", "mcp/transport.py", "mcp/stdio.py"], SCRIPT, layout="pane")
    out += gen_line([DATA], SCRIPT)
    out += '<div class="rn-split" markdown>\n<div class="rn-prose" markdown>\n\n'
    out += ("Your client receives this text in the `instructions` field of the `initialize` result. "
            "It tells the agent which tool to call first, how to read coverage, and how to treat the data it gets back.\n\n")
    out += "## Instructions\n\n"
    for para in srv["instructions"].split("\n\n"):
        out += "> " + para.strip().replace("\n", " ") + "\n>\n"
    out = out.rstrip(">\n") + "\n\n"
    out += "## Server\n\n"
    out += "Use these details when you set up a client by hand or debug a connection.\n\n"
    out += table(["Property", "Value"], [
        ["Name", code(srv["name"])],
        ["Endpoint", code(srv["endpoint_url_shape"])],
        ["Protocol version", code(srv["protocol"])],
        ["Accepted versions", ", ".join(code(v) for v in srv["supported_protocols"])],
        ["Methods", ", ".join(code(m) for m in srv["methods"])],
        ["Rate limit", f"{srv['default_rate_limit_per_minute']} calls a minute per token by default, set from 1 to 10,000"],
        ["stdio command", code(srv["stdio_command"])],
    ])
    out += ("If your client asks for one of the accepted versions, the server answers with that version. "
            f"Otherwise it answers with `{srv['protocol']}`.\n\n")
    out += "</div>\n<div class=\"rn-pane\" markdown>\n"
    out += '<div class="rn-pane-head"><b>initialize</b><span>JSON-RPC 2.0</span></div>\n\n'
    out += "/// tab | MCP\n"
    out += '<div class="rn-pane-label">result</div>\n\n'
    result = {"protocolVersion": srv["protocol"], "capabilities": {"tools": {"listChanged": False}},
              "serverInfo": {"name": srv["name"], "version": "3.0.0"}, "instructions": "This is the MCP server for reNgine, …"}
    out += "```json\n" + json.dumps(result, indent=2) + "\n```\n"
    out += "///\n\n"
    out += "</div>\n</div>\n"
    return out


def main() -> None:
    data = load(DATA)
    changed = 0
    changed += write(DOCS / "reference" / "mcp-tools.md", reference_page(data))
    changed += write(DOCS / "agents" / "mcp" / "tools.md", overview_page(data))
    changed += write(DOCS / "agents" / "mcp" / "server-instructions.md", instructions_page(data))
    print(f"gen_mcp: 3 pages, {changed} changed")


if __name__ == "__main__":
    main()
