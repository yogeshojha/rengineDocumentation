"""Read-only introspection: print the /help reply and each /help <command> reply as plain text.

Imports the dispatcher and renders lines to text. Opens no database, Redis or network connection.

Run (from the host):
    docker exec -i rengine-channels-1 uv run python - < dump_chat_help.py > chat-help.txt
"""

from channels import commands, render
from channels.dispatch import Dispatcher
from channels.telegram.api import SAFE_LIMIT
from channels.telegram.driver import menu


def text_of(lines):
    return "\n".join("".join(span.text for span in line) for line in lines)


def styled(lines):
    out = []
    for line in lines:
        for span in line:
            if span.style and span.text:
                out.append(f"{span.style}:{span.text!r}")
    return out


# no __init__: _help and _usage read no instance state
dispatcher = Dispatcher.__new__(Dispatcher)
lines = dispatcher._help(None)
messages = render.chunk(lines, SAFE_LIMIT)
print("===== /help =====")
print(text_of(lines))
print(f"----- utf16 length={render.utf16_len(messages[0].text)} messages={len(messages)} "
      f"entities={[len(m.entities) for m in messages]}")
print("----- styled spans:", styled(lines)[:6], "...")

for name in commands.catalog():
    print(f"\n===== /help {name} =====")
    print(text_of(dispatcher._help(name)))

print("\n===== /help nosuch =====")
print(text_of(dispatcher._help("no-such")))

print("\n===== bot command menu (setMyCommands) =====")
for name, title in menu():
    print(f"{name} - {title}")
