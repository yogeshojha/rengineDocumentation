"""Write reference/remote-control-commands.md from data/chat-commands.json and data/chat-help.txt."""

from __future__ import annotations

import re

from gen_common import DATA, DOCS, code, front_matter, gen_line, load, sentence, table, write

SCRIPT = "scripts/gen_chat.py"
GROUPS = ["Targets", "Scans", "Results", "Lookups", "Chat"]


def help_blocks() -> dict[str, str]:
    text = (DATA / "chat-help.txt").read_text(encoding="utf-8")
    blocks = {}
    for m in re.finditer(r"^===== /help ?(\S*) =====\n(.*?)(?=^=====|\Z)", text, re.S | re.M):
        body = re.split(r"^-----", m.group(2), flags=re.M)[0].strip()
        blocks[m.group(1) or "_index"] = body
    return blocks


def reach(c: dict) -> str:
    return '<span class="rn-tag active">Active</span>' if c["touches_target"] else '<span class="rn-tag passive">Passive</span>'


def page() -> str:
    cmds = load("chat-commands.json")
    helps = help_blocks()
    out = front_matter(
        "Remote control commands",
        f"All {len(cmds)} commands you can send to reNgine from Telegram, with their arguments, the capability each one needs, "
        "and which ones ask for your authenticator code. Use it when you run scans or check results from a chat.",
        ["channels/commands.py", "channels/dispatch.py", "channels/stepup.py", "mcp/tools/", "toolbox/"], SCRIPT, layout="reference")
    out += gen_line(["chat-commands.json", "chat-help.txt"], SCRIPT)
    out += ("Once an administrator has paired your Telegram chat with your reNgine account, you send these commands to the bot. "
            "Most of them run an [MCP tool](mcp-tools.md) or a toolbox lookup, within the capabilities granted to the chat. "
            "A command that needs more than the read capability is marked **Second factor**: "
            "the bot asks for the authenticator code of your account before it runs it. "
            "If your account has no authenticator enrolled, the chat can run read commands only. "
            "To set up the chat, see [Remote control over Telegram](../pentesters/telegram.md).\n\n")
    out += ("Write the first argument as it is, and any further arguments as `key=value`, "
            "for example `/scan example.com intensity=passive`.\n\n")
    if "_index" in helps:
        out += "## The help reply\n\nSend `/help` and the bot replies with this list.\n\n```text\n" + helps["_index"] + "\n```\n\n"
    out += "## All commands\n\n"
    out += ("**Runs** shows the MCP tool or toolbox lookup behind each command. "
            "<span class=\"rn-tag active\">Active</span> marks a command that sends traffic to your target.\n\n")
    rows = []
    for g in GROUPS:
        for c in [c for c in cmds if c["group_label"] == g]:
            runs = f"[`{c['tool']}`](mcp-tools.md#{c['tool']})" if c["source"] == "mcp" else (f"toolbox `{c['tool']}`" if c["source"] == "toolbox" else "Chat command")
            rows.append([f"[{code('/' + c['name'])}](#{c['name']})", g, c["capability"], reach(c), "Second factor" if c["steps_up"] else "", runs])
    out += table(["Command", "Group", "Capability", "Reach", "Confirmation", "Runs"], rows)
    for g in GROUPS:
        out += f"## {g} {{ #group-{g.lower()} }}\n\n"
        for c in [c for c in cmds if c["group_label"] == g]:
            out += f"### /{c['name']} {{ #{c['name']} }}\n\n"
            out += f"{sentence(c['description'])}\n\n"
            out += f"How to write it\n:   {code(c['usage'] if c['name'] != 'help' else '/help [command]')}\n\n"
            out += f"Capability\n:   `{c['capability']}`\n\n"
            out += f"Sends traffic to the target\n:   {reach(c)} {'Yes' if c['touches_target'] else 'No'}\n\n"
            if c["steps_up"]:
                out += "Confirmation\n:   Asks for the authenticator code of your account before it runs\n\n"
            if c.get("presets"):
                out += "Fixed arguments\n:   " + ", ".join(f"{code(k)} = {code(v)}" for k, v in c["presets"].items()) + "\n\n"
            if c["arguments"]:
                out += "It takes these arguments.\n\n"
                rows = [[code(a["name"]), code(a["type"]), "Yes" if a["required"] else "No", code(a["default"]) if a.get("default") not in (None, "") else "",
                         sentence(a["description"]) if a["description"] else ""] for a in c["arguments"]]
                out += table(["Argument", "Type", "Required", "Default", "Description"], rows)
            if c["name"] in helps:
                out += f"The bot's reply to `/help {c['name']}`:\n\n"
                out += "```text\n" + helps[c["name"]] + "\n```\n\n"
    return out


def main() -> None:
    changed = write(DOCS / "reference" / "remote-control-commands.md", page())
    print(f"gen_chat: 1 page, {int(changed)} changed")


if __name__ == "__main__":
    main()
