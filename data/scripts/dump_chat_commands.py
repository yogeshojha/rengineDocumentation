"""Read-only introspection: print every chat command of the remote control catalog as JSON.

Imports the registries and prints. Writes nothing, opens no database or Redis connection.

Run (from the host):
    docker exec -i rengine-channels-1 uv run python - < dump_chat_commands.py > chat-commands.json
"""

import json
import sys

from channels import commands
from shared.definitions.channels import CHAT_GROUP_LABELS

# Builtins carry no schema, so the registry reports no arguments for them. These two read a
# bare argument in the dispatcher itself: channels/dispatch.py:456-458 (/help <command>) and
# channels/dispatch.py:565-567 (/project <name>). Both are optional.
DISPATCHER_ARGS = {"help": "[command]", "project": "[name]"}

rows = []
for group, specs in commands.by_group():
    for spec in specs:
        usage = spec.usage
        from_registry = usage[len(spec.name) + 1 :].strip()
        rows.append(
            {
                "name": spec.name,
                # the argument part of the usage line, "" when the command takes none
                "args": DISPATCHER_ARGS.get(spec.name, from_registry),
                "args_source": "dispatcher" if spec.name in DISPATCHER_ARGS else "registry",
                "capability": spec.capability,
                "description": spec.description,
                # ---- extra detail ----
                "usage": usage,
                "title": spec.title,
                "group": group,
                "group_label": CHAT_GROUP_LABELS[group],
                "source": spec.source,
                "tool": spec.tool,
                "touches_target": spec.touches_target,
                "steps_up": spec.steps_up,
                "value_field": spec.value_field,
                "takes_args": spec.takes_args,
                "presets": spec.presets,
                "arguments": spec.args(),
            }
        )

missing = sorted(set(commands.catalog()) - {r["name"] for r in rows})
if missing:
    print(f"commands outside every group: {missing}", file=sys.stderr)

json.dump(rows, sys.stdout, indent=2, ensure_ascii=False)
sys.stdout.write("\n")
