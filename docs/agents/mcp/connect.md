---
title: Connect your agent
description: Create a key on the **Agents** page and add reNgine to Claude Code, Claude Desktop, Cursor, VS Code or any other MCP client. Your agent can then ask reNgine about your targets and scan results.
layout: pane
sources:
  - frontend/src/lib/components/agents/connect-sheet.svelte
  - frontend/src/routes/(app)/agents/+page.svelte
  - frontend/src/lib/components/agents/settings-sheet.svelte
  - frontend/src/lib/components/agents/agents-table.svelte
  - frontend/src/lib/types/mcp.ts
  - frontend/src/lib/utilities/mcp.ts
  - mcp/clients.py
  - mcp/settings.py
  - mcp/server.py
  - mcp/protocol.py
  - mcp/transport.py
  - mcp/stdio.py
  - mcp/service.py
  - mcp/telemetry.py
  - shared/utils/bearer.py
  - shared/config.py
  - api/app/api/v1/mcp.py
  - install.sh
revised: 2026-10-03
---

To connect, you create a key for your agent, paste a configuration into your client, and check that the first call arrives. The table below holds everything a client needs, for when you set one up by hand.

| Item | Value |
|---|---|
| Endpoint | `<interface origin>/api/v1/mcp`, for example `https://asm.example.com/api/v1/mcp`. `POST` only. |
| Transports | HTTP and stdio. Both apply the same key checks, capabilities and rate limit. |
| Protocol | MCP `2025-06-18` over JSON-RPC 2.0. `initialize` also accepts `2026-07-28` and `2025-03-26`. |
| Authentication | `Authorization: Bearer <key>` on HTTP. The `RENGINE_MCP_TOKEN` environment variable on stdio. |
| Key | `rngmcp_` followed by 48 hexadecimal characters. Shown once. Only its SHA-256 hash is stored. |
| Tools | {{ counts.mcp_tools }}. `tools/list` returns the tools of the capabilities the key holds. |
| Server | Stopped on a new instance. Every call is refused until the server starts. |
| Managed by | Administrators. Other users see **Agents are managed by administrators** on the **Agents** page. |

The interface calls the token a **key**, and the client that holds it an **agent**.

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Add an agent

Give each agent its own key. You then see each agent's calls on its own, and you can cut one agent's access without touching the others. Only administrators can open the **Agents** page.

1. **Open the Agents page.** Select **Integrations**, then **Agents**, in the sidebar. You can also find **Agents** in the command palette, <kbd>Ctrl</kbd> <kbd>K</kbd>. The header shows whether the server is running, **Server running** or **Server stopped**, and the endpoint with a copy button.
2. **Open the connect sheet.** Select **Connect an agent**. <span class="rn-ref" data-tab="Interface" data-mark="sheet">Shown in the pane</span>
3. **Pick your client.** Under **Client**, select **Claude Code**, **Claude Desktop**, **Cursor**, **VS Code** or **Other**. reNgine fills in **Name** for you, for example `claude-code`. You can type your own name instead, up to 80 characters. <span class="rn-ref" data-tab="Interface" data-mark="client">Shown in the pane</span>
4. **Decide what the agent can reach and do.** Under **Project**, choose **Every project** or one project. **Access** is a ladder of **Read**, **Plan**, **Write** and **Launch**. The rung you select grants its own capability and every capability below it that the instance ceiling allows. The default, **Plan**, lets the agent read results and plan scans without sending any traffic. A rung that is off in the ceiling is disabled and shows **Off in the ceiling**. The line under the ladder sums up your choice, for example **Reads and plans scans** in **every project** · **Sends no traffic**. <span class="rn-ref" data-tab="Interface" data-mark="access">Shown in the pane</span>
5. **Decide when the key expires.** Under **Key expires**, choose **In 7 days**, **In 30 days**, **In 90 days**, **In a year** or **Never**. The default is **In 30 days**. <span class="rn-ref" data-tab="Interface" data-mark="expiry">Shown in the pane</span>
6. **Create the key.** Select **Create key**. The sheet now carries the agent's name as its title and the line **Shown once. Only a hash is stored.** Below it, you get a ready-made configuration for each client, with the endpoint and the key filled in. <span class="rn-ref" data-tab="Key created" data-mark="snippet">Shown in the pane</span>
7. **Copy the configuration into your client.** Copy the configuration for your client, or the HTTP configuration under **Other**. Do it before you select **Done**: reNgine does not show the key again. <span class="rn-ref" data-tab="HTTP" data-mark="config">Shown in the pane</span>
8. **Start the server if it is stopped.** On a new instance the server is stopped, and it refuses every call. If the sheet shows **Server stopped. Calls are refused.**, select **Start server**. While the server runs and your client has not called yet, the sheet shows **Waiting for the first call** and the key prefix. <span class="rn-ref" data-tab="Key created" data-mark="state">Shown in the pane</span>

You can also start and stop the server from **Settings** on the **Agents** page. To change a key's access later, or to cut it off, see [Control what an agent can do](capabilities.md).

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Connect an agent</b><span>asm.example.com</span></div>

/// tab | HTTP
<div class="rn-pane-label"><span data-mark="config">MCP configuration · Other</span></div>

```json
{
  "mcpServers": {
    "rengine": {
      "type": "http",
      "url": "https://asm.example.com/api/v1/mcp",
      "headers": {
        "Authorization": "Bearer rngmcp_000000000000000000000000000000000000000000000000"
      }
    }
  }
}
```

<div class="rn-pane-label">check from a shell</div>

```bash
curl -s -X POST https://asm.example.com/api/v1/mcp \
  -H "Authorization: Bearer $RENGINE_MCP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "ping"}'
```

<div class="rn-pane-label">response · 200</div>

```json
{"jsonrpc":"2.0","id":1,"result":{}}
```
///

/// tab | stdio
<div class="rn-pane-label">shell, in the install directory</div>

```bash
cd /opt/rengine
export RENGINE_MCP_TOKEN=rngmcp_eb50a761…
docker compose exec -T -e RENGINE_MCP_TOKEN api \
  /app/.venv/bin/python -m mcp.stdio
```

<div class="rn-pane-label">MCP configuration</div>

```json
{
  "mcpServers": {
    "rengine": {
      "command": "docker",
      "args": ["compose", "exec", "-T", "-e", "RENGINE_MCP_TOKEN",
               "api", "/app/.venv/bin/python", "-m", "mcp.stdio"],
      "env": { "RENGINE_MCP_TOKEN": "rngmcp_eb50a761…" }
    }
  }
}
```

<div class="rn-pane-label">one message per line</div>

```text
→ {"jsonrpc": "2.0", "id": 1, "method": "ping"}
← {"jsonrpc": "2.0", "id": 1, "result": {}}
```
///

/// tab | Interface
<div class="rn-ui" aria-label="Connect an agent sheet: Client Claude Code, Name claude-code, Project Every project, Access at Plan with Launch off in the ceiling, the reach line Reads and plans scans in every project, Sends no traffic, Key expires In 30 days, and the Create key button">
<span class="rn-ui-sheet">
<span class="rn-ui-dlg__head" data-mark="sheet"><b>Connect an agent</b></span>
<span class="rn-ui-fld" data-mark="client"><span class="rn-ui-label">Client</span><span class="rn-ui-seg" style="--rn-n:3"><span class="on">Claude Code</span><span>Claude Desktop</span><span>Cursor</span><span>VS Code</span><span>Other</span></span></span>
<span class="rn-ui-fld" data-mark="client"><span class="rn-ui-label">Name</span><span class="rn-ui-in">claude-code</span></span>
<span class="rn-ui-fld" data-mark="access"><span class="rn-ui-label">Project</span><span class="rn-ui-in">Every project</span></span>
<span class="rn-ui-fld" data-mark="access"><span class="rn-ui-label">Access</span><span class="rn-ui-seg" style="--rn-n:4"><span class="on">Read</span><span class="on">Plan</span><span>Write</span><span style="opacity:.4">Launch</span></span><span class="rn-ui-help">Reads and plans scans in <b>every project</b> · Sends no traffic</span></span>
<span class="rn-ui-fld" data-mark="expiry"><span class="rn-ui-label">Key expires</span><span class="rn-ui-in">In 30 days</span></span>
<span class="rn-ui-foot"><span class="rn-ui-btn">Cancel</span><span class="rn-ui-btn pri">Create key</span></span>
</span>
</div>
///

/// tab | Key created
<div class="rn-ui" aria-label="The sheet after Create key: title claude-code, the description Shown once. Only a hash is stored., the client choices with Claude Code selected, the claude mcp add command in a Terminal block, the status Waiting for the first call with the key prefix, and the Done button">
<span class="rn-ui-sheet">
<span class="rn-ui-dlg__head"><b>claude-code</b><span>Shown once. Only a hash is stored.</span></span>
<span class="rn-ui-fld" data-mark="snippet"><span class="rn-ui-seg" style="--rn-n:3"><span class="on">Claude Code</span><span>Claude Desktop</span><span>Cursor</span><span>VS Code</span><span>Other</span></span><span class="rn-ui-label" style="margin-top:.5rem">Terminal</span><span class="rn-ui-code">claude mcp add --transport http rengine https://asm.example.com/api/v1/mcp --header "Authorization: Bearer rngmcp_000000000000000000000000000000000000000000000000"</span></span>
<span class="rn-ui-fld" data-mark="state"><span class="rn-ui-toggle"><span>Waiting for the first call<small>rngmcp_eb50a761…</small></span></span></span>
<span class="rn-ui-foot"><span class="rn-ui-btn pri">Done</span></span>
</span>
</div>
///

</div>
</div>

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Client configurations

The connect sheet writes these for you. Look here when you want to see where each one goes, or when you set up a client by hand. Every configuration names the server `rengine` and holds the endpoint and your key.

| Client | Where it goes | What it is |
|---|---|---|
| **Claude Code** | Terminal | A `claude mcp add` command with the HTTP transport and the `Authorization` header |
| **Claude Desktop** | `claude_desktop_config.json` | `mcp-remote` started with `npx`. The key is in the `RENGINE_AUTH` environment variable. |
| **Cursor** | `~/.cursor/mcp.json` | An `mcpServers` entry with `url` and `headers` |
| **VS Code** | `.vscode/mcp.json` | A `servers` entry with `type: http`, `url` and `headers` |
| **Other** | MCP configuration | An `mcpServers` entry with `type: http`, `url` and `headers`. Shown on the **HTTP** tab above. |

Over HTTP, your client sends one JSON-RPC message per `POST` and gets one JSON body back. There is no event stream and no session header. A `GET` on the endpoint returns `405`, and batched requests are refused with `Batched requests are not supported.`

Use stdio when your agent runs on the host that runs reNgine. Your client starts a command that reads one JSON-RPC message per line on standard input and writes one response per line on standard output. You can copy the command from **stdio** in **Agent settings**. Run it in the install directory: `/opt/rengine` if you installed as root, `$HOME/rengine` otherwise. The account that runs it needs to use Docker and to read `.env`. `-e RENGINE_MCP_TOKEN` passes the key from your client's environment into the `api` container.

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Client configuration</b><span>asm.example.com</span></div>

/// tab | Claude Code
<div class="rn-pane-label">Terminal</div>

```bash
claude mcp add --transport http rengine \
  https://asm.example.com/api/v1/mcp \
  --header "Authorization: Bearer rngmcp_eb50a761…"
```
///

/// tab | Claude Desktop
<div class="rn-pane-label">claude_desktop_config.json</div>

```json
{
  "mcpServers": {
    "rengine": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://asm.example.com/api/v1/mcp",
        "--header",
        "Authorization:${RENGINE_AUTH}"
      ],
      "env": {
        "RENGINE_AUTH": "Bearer rngmcp_eb50a761…"
      }
    }
  }
}
```
///

/// tab | Cursor
<div class="rn-pane-label">~/.cursor/mcp.json</div>

```json
{
  "mcpServers": {
    "rengine": {
      "url": "https://asm.example.com/api/v1/mcp",
      "headers": {
        "Authorization": "Bearer rngmcp_eb50a761…"
      }
    }
  }
}
```
///

/// tab | VS Code
<div class="rn-pane-label">.vscode/mcp.json</div>

```json
{
  "servers": {
    "rengine": {
      "type": "http",
      "url": "https://asm.example.com/api/v1/mcp",
      "headers": {
        "Authorization": "Bearer rngmcp_eb50a761…"
      }
    }
  }
}
```
///

</div>
</div>

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Check the connection

Before you hand your agent real work, make sure it reaches reNgine and sees the tools you expect. The pane shows each of these calls with its answer.

1. **Initialize.** Your client sends `initialize` when it connects. The answer names the server `rengine`, its version and the protocol version, and carries the [server instructions](server-instructions.md): a short guide that tells your agent which tool to call first and how to read the answers. If your client asks for a protocol version reNgine supports, reNgine answers with that version. For any other value it answers with `2025-06-18`. <span class="rn-ref" data-tab="initialize" data-mark="init">Shown in the pane</span>
2. **List the tools.** `tools/list` returns the tools your key's capabilities allow, each with `name`, `title`, `description`, `inputSchema` and `annotations`. The list has no cursor, so every tool comes back in one answer. <span class="rn-ref" data-tab="tools/list" data-mark="list">Shown in the pane</span>
3. **Call resolve_target.** The server instructions tell your agent to call [`resolve_target`](../../reference/mcp-tools.md#resolve_target) first. For each of six dimensions, it tells you whether a scan covered it, how many rows it holds, and the scan id the other tools take. <span class="rn-ref" data-tab="tools/call" data-mark="call">Shown in the pane</span>
4. **Check the interface.** If the connect sheet is still open, **Waiting for the first call** changes to **Connected · {client} {version}** and **First call {tool title} · {summary}**. On the **Agents** page, the agent's row shows the client and **Last call**.

How many tools your agent sees depends on the access you gave its key:

| Access | Capabilities | Tools in `tools/list` |
|---|---|---|
| **Read** | read | 16 |
| **Plan** | read, plan | 17 |
| **Write** | read, plan, write | 21 |
| **Launch** | read, plan, write, launch | 26 |

Each tool also carries hints about what it does: `readOnlyHint` is true for the read tools, and `destructiveHint` is true for `delete_target` alone.

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>First calls</b><span>example.com</span></div>

/// tab | initialize
<div class="rn-pane-label"><span data-mark="init">request</span></div>

```json
{
  "jsonrpc": "2.0", "id": 1, "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": { "name": "example-agent", "version": "1.0.0" }
  }
}
```

<div class="rn-pane-label">result</div>

```json
{
  "protocolVersion": "2025-06-18",
  "capabilities": { "tools": { "listChanged": false } },
  "serverInfo": { "name": "rengine", "version": "3.0.0" },
  "instructions": "This is the MCP server for reNgine, …"
}
```
///

/// tab | tools/list
<div class="rn-pane-label"><span data-mark="list">request</span></div>

```json
{ "jsonrpc": "2.0", "id": 2, "method": "tools/list" }
```

<div class="rn-pane-label">result, first entry</div>

```json
{
  "tools": [
    {
      "name": "resolve_target",
      "title": "Resolve target",
      "description": "For each of a target's result dimensions: …",
      "inputSchema": {
        "type": "object",
        "properties": {
          "target": { "type": "string", "title": "Target",
                      "description": "A domain, IP address, CIDR range, URL or ASN added as a target." }
        },
        "required": ["target"],
        "additionalProperties": false
      },
      "annotations": { "readOnlyHint": true, "destructiveHint": false }
    },
    …
  ]
}
```
///

/// tab | tools/call
<div class="rn-pane-label"><span data-mark="call">request</span></div>

```json
{
  "jsonrpc": "2.0", "id": 3, "method": "tools/call",
  "params": {
    "name": "resolve_target",
    "arguments": { "target": "example.com" }
  }
}
```

<div class="rn-pane-label">result · structuredContent</div>

```json
{
  "summary": "example.com: 5 of 6 dimensions scanned, 7 findings need review",
  "data": {
    "target": { "id": "3c0e…", "value": "example.com", "type": "domain", … },
    "surface": [
      { "dimension": "web_assets", "covered": true, "count": 42,
        "scan_id": "8a1f…", "is_latest_scan": true, … },
      { "dimension": "secrets", "covered": false, "count": null, … },
      …
    ],
    "risk": { "total": 19, "actionable": 7, "kev": 1, … }
  },
  "open_in_rengine": "https://asm.example.com/targets/3c0e…",
  "caveats": ["Not scanned: Secrets."]
}
```
///

</div>
</div>

## Find your endpoint

Your endpoint is the address of the reNgine interface followed by `/api/v1/mcp`. You can copy it from the **Agents** page or from **Agent settings**. reNgine takes the origin from the first entry of `CORS_ORIGINS`, which the installer sets to your public origin.

The endpoint depends on how reNgine was installed:

| Install mode | Endpoint | TLS |
|---|---|---|
| Public domain | `https://<domain>/api/v1/mcp` | Let's Encrypt certificate |
| Server address | `https://<address>/api/v1/mcp`, or `https://<address>:<UI port>/api/v1/mcp` when the UI port is not `443` | Certificate from Caddy's internal authority |
| Local | `http://localhost:<UI port>/api/v1/mcp`, UI port `8080` by default | None |
| Published API port | `http://127.0.0.1:<API port>/api/v1/mcp`, on the host only | None |

[Install reNgine](../../pentesters/install.md) explains the install modes.

## Protocol methods

If you write your own client, or want to know exactly what the server answers, this table lists every method it handles.

| Method | Answer |
|---|---|
| `initialize` | `protocolVersion`, `capabilities` with `tools.listChanged` false, `serverInfo` and `instructions` |
| `notifications/initialized` | No response. HTTP returns `200` with `{}`. |
| `ping` | `{}` |
| `tools/list` | The tools the key may call |
| `tools/call` | A tool result, or a tool error with `isError: true` |
| Any other method | Error `-32601`, `Unknown method '<name>'.` An unknown notification is ignored. |

The server offers tools only. It has no prompts, resources or sampling, and it sends no notifications. To name the client of a request, reNgine uses `clientInfo.name` from `initialize` and, for other HTTP requests, the `User-Agent` header. Every answered request, including `initialize`, `tools/list` and `ping`, updates the key's **Last call** and call count.

## Connection states

These states tell you whether your agent is reaching reNgine. You see them in the connect sheet and in the **Agents** table.

| Where | State | Meaning |
|---|---|---|
| Connect sheet | **Server stopped. Calls are refused.** | The server is off. **Start server** starts it. |
| Connect sheet | **Waiting for the first call** | The key has not been used |
| Connect sheet | **Connected · {client} {version}** | The key has answered a request. **First call** names the first tool and its summary. |
| **Agents** table | **Connected** | A request in the last minute |
| **Agents** table | **Idle** | The last request between one and five minutes ago |
| **Agents** table | **Offline** | No request in the last five minutes |
| **Agents** table | **Key expired**, **Key revoked** | The key is refused |

## If your agent cannot connect

The error message tells you what went wrong. Find it below and apply the fix. Each message arrives as a JSON-RPC error with code `-32001` inside an HTTP `200` response, on both transports.

| Message | What to do |
|---|---|
| `The MCP server is stopped. Start it on the Agents page.` | Select **Start server** in the connect sheet or in **Agent settings**. |
| ``Send an MCP token as `Authorization: Bearer <token>`.`` | Send the header. The key starts with `rngmcp_` and has 55 characters. On stdio, set `RENGINE_MCP_TOKEN`. |
| `The token is not valid.` | Copy the key from the configuration again, or create a key. |
| `The token was revoked.` | Create a key. |
| `The token expired.` | Create a key. |
| `The token's issuer is not an active administrator.` | Create a key as an active administrator. |
| `The token's project was deleted.` | Select **Edit access** on the agent's row and choose another project or **Every project**. |

If one client address sends 20 rejected keys within 15 minutes, the HTTP endpoint answers `429` with `Too many attempts. Try again in <n> seconds.` Calls refused because the server is stopped do not count toward this limit. For the rate limit, capability errors and tool errors, see [Limits and errors](limits.md).
