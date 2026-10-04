---
title: Agents
description: Connect Claude, Cursor or any other MCP client to reNgine, so your AI agent can look up your targets, read your scan results and plan scans with you. This section also gives your agents these docs in plain text.
sources:
  - mcp/README.md
  - mcp/capabilities.py
  - frontend/src/routes/(app)/agents/+page.svelte
revised: 2026-10-03
---

Your agent connects to reNgine through its MCP server. MCP, the Model Context Protocol, is the standard way AI clients such as Claude Code, Claude Desktop, Cursor and VS Code call outside tools. Once your agent is connected, you can ask it about a target in plain words and it answers from your scan results.

An administrator creates a key for each agent on the **Agents** page. The key decides how far the agent can go, using four capabilities: read results, plan scans, write changes to targets and triage, and launch scans. Read is always granted. Above all keys sits a ceiling for the whole instance, and launch is off in it until an administrator allows it, so by default no agent can send traffic to your targets. The server has {{ counts.mcp_tools }} tools, and your agent sees only the ones its key allows.

The server answers at `<interface origin>/api/v1/mcp` over HTTP, and over stdio on the host that runs reNgine.

If you work on the reNgine code itself, the agent files give your coding agent the repository's layout, commands and rules. The machine-readable pages give any agent these docs as plain Markdown.

{{ section_index }}
