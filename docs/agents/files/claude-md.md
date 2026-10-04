---
title: CLAUDE.md
description: If you work on reNgine with Claude Code, add this CLAUDE.md beside AGENTS.md. Claude Code then loads the repository instructions, plus a few notes for its own sessions, every time you start one.
sources:
  - .gitignore
  - Makefile
  - mcp/clients.py
revised: 2026-10-03
---

This file is small. Its first line imports [AGENTS.md](agents-md.md), so Claude Code reads the repository instructions through it. The rest holds notes for Claude Code alone: how to run commands without a terminal, how to reach a running instance over MCP, and where to find the `rengine` skill.

## Where to put it

| Item | Value |
|---|---|
| File name | `CLAUDE.md` |
| Location | The root of a reNgine checkout, beside [AGENTS.md](agents-md.md) |
| Version control | Untracked. The repository's `.gitignore` lists `CLAUDE.md`. |
| First line | `@AGENTS.md`, the Claude Code import of the file beside it |

Claude Code expands an `@path` import when a session starts. A relative path resolves against the file that holds the import. Imports nest up to four levels. A path inside a code span or a code block is not imported.

## Which file Claude Code reads

That depends on what sits at the root of your checkout:

| Files at the checkout root | Claude Code reads |
|---|---|
| `AGENTS.md` only | `AGENTS.md`, from Claude Code 2.1.277 |
| `AGENTS.md` and this `CLAUDE.md` | `CLAUDE.md`, with `AGENTS.md` expanded once through the import |
| `AGENTS.md` and a `CLAUDE.md` without the import | `CLAUDE.md` only |

If your checkout already has a `CLAUDE.md`, keep it and add the line `@AGENTS.md` at its top instead of using this file. To see which files a session loaded, run `/context`: it lists them under **Memory files**.

## Install it

1. Download <https://rengine.wiki/agent-files/CLAUDE.md>, or copy the file with the copy button on the block below.
2. Save it as `CLAUDE.md` at the root of your checkout, beside `AGENTS.md`.
3. Start a Claude Code session in the checkout and run `/context` to check what the session loaded.

## The file

This is the full file, as Claude Code reads it.

````markdown
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
````
