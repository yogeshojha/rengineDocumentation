@AGENTS.md

## Claude Code

These notes add to AGENTS.md for Claude Code sessions in this repository.

- Your Bash tool runs commands without a terminal. Pass `-T` to `docker compose exec`.
- `make db-reset` reads a confirmation from the terminal and stops without one, so it does not run from your Bash tool. It runs from a terminal only: ask the user to run it.
- To query a running instance from your session, add its MCP server with the key from **Connect an agent** on the **Agents** page:

  ```bash
  claude mcp add --transport http rengine <interface origin>/api/v1/mcp --header "Authorization: Bearer <key>"
  ```

- To operate an instance over MCP, use the `rengine` skill. It holds the rules for counts, coverage and launches: https://rengine.wiki/agents/files/skill/
