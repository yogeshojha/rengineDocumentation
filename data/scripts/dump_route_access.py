"""Read-only: print the authentication dependency of every API route as JSON. Imports the app, opens no connection."""
import json
import sys

from fastapi.routing import APIRoute

from app.main import app

NAMES = {
    "get_current_superuser": "administrator",
    "get_current_active_user": "user",
    "get_current_user": "user",
    "get_stream_user": "user",
}


def walk(dep, seen):
    for sub in dep.dependencies:
        name = getattr(sub.call, "__name__", str(sub.call))
        seen.append(name)
        walk(sub, seen)


out = []
for route in app.routes:
    if not isinstance(route, APIRoute):
        continue
    names = []
    walk(route.dependant, names)
    level = "none"
    for n in names:
        if n in NAMES:
            if NAMES[n] == "administrator" or level == "none":
                level = NAMES[n]
    other = sorted({n for n in names if ("token" in n.lower() or "connector" in n.lower() or "mcp" in n.lower()) and n not in NAMES})
    for method in sorted(route.methods):
        out.append({"method": method, "path": route.path, "access": level, "other_auth": other})
sys.stdout.write(json.dumps(sorted(out, key=lambda r: (r["path"], r["method"])), indent=1) + "\n")
