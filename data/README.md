# Data snapshots

The reference pages of the docs are generated from the files in this folder, so they match the reNgine code the files were taken from. This page tells you what each file holds and how to refresh it after the reNgine code changes.

## What reads these files

- `scripts/gen_*.py`, run with `make gen`, write the generated pages: the pages under `docs/reference/` that carry `generated:` in their front matter, `docs/developers/api/search-*.md`, and `docs/agents/mcp/tools.md` and `docs/agents/mcp/server-instructions.md`.
- `hooks/rengine.py` reads them when the site is built, to compute the counts shown on the home page and in the text of the pages.

## Where the snapshots come from

Each snapshot was taken from the `release/3.0.0` working tree of `yogeshojha/rengine`. The dump scripts in `data/scripts/` only import modules and print. They open no database, Redis or network connection.

Two files are not snapshots: `env-notes.json` and `shortcuts-extra.json` are written by hand.

## Refresh a snapshot

You need a reNgine dev stack running (`docker compose up -d` in the reNgine checkout), with the checkout at `../rengine`. Run each command from the root of this repository.

| File | What it holds | How to refresh it |
|---|---|---|
| `query-schema.json` | The query grammar, the seven dimensions, every field, flag, group key, sort key and example, and the vocabularies | `docker exec -i rengine-api-1 /app/.venv/bin/python - < data/scripts/build_query_schema.py > data/query-schema.json` |
| `stages.json` | The stage catalog: stages, options, steps, intensity profiles, the Default engine resolution, presets, rescan limits, port profiles and wordlists | `docker exec -i rengine-api-1 /app/.venv/bin/python - < data/scripts/dump_stage_catalog.py > data/stages.json 2> /dev/null` |
| `default-engine.yaml` | The YAML the engine editor exports for the Default engine | `docker exec -i rengine-api-1 /app/.venv/bin/python - < data/scripts/dump_default_engine_yaml.py > data/default-engine.yaml 2> /dev/null` |
| `mcp-tools.json` | The MCP server, its capabilities, the client snippets and the 26 tools | `docker exec -i rengine-api-1 /app/.venv/bin/python - < data/scripts/dump_mcp_tools.py > data/mcp-tools.json` |
| `mcp-dimensions.json` | The dimensions, row limits and windows the MCP tools accept, and the rescan schema | `docker exec -i rengine-api-1 /app/.venv/bin/python - < data/scripts/dump_mcp_dimensions.py`, then merge the two JSON documents it prints into one object, with the second under the key `rescan` |
| `chat-commands.json` | The remote control commands | `docker exec -i rengine-channels-1 uv run python - < data/scripts/dump_chat_commands.py > data/chat-commands.json` |
| `chat-help.txt` | The `/help` reply and each `/help <command>` reply | `docker exec -i rengine-channels-1 uv run python - < data/scripts/dump_chat_help.py > data/chat-help.txt` |
| `openapi.json` | The OpenAPI 3.1 document of the API | `curl -s http://127.0.0.1:8000/openapi.json > data/openapi.json`. The API serves this document only when `DEBUG` is on. |
| `route-access.json` | The authentication each API route checks: user, administrator or none | `docker exec -i rengine-api-1 /app/.venv/bin/python - < data/scripts/dump_route_access.py > data/route-access.json 2> /dev/null` |
| `repo.json` | The `rengine` CLI usage, the installer flags, the `.env.example` variables, the pinned tool versions, the base images and the shortcut tables of the interface, read from files in the checkout | `python3 scripts/snapshot_repo.py --repo ../rengine`, or `make snapshot` |
| `env-notes.json` | Notes on each configuration variable: the value the installer writes and what the variable changes, checked in `shared/config.py`, `api/app/config.py` and `install.sh` | Edit it by hand. `scripts/gen_ops.py` stops with an error when a variable in `repo.json` has no note. |
| `shortcuts-extra.json` | Keyboard shortcuts that have no shortcut dialog in the interface, with their source files | Edit it by hand. |

After a refresh, run `make gen` and review the diff of `docs/` before you commit.
