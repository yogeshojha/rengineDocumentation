---
title: Control what an agent can do
description: Decide what each agent can read and change in reNgine, which projects it reaches, and when its key expires. Administrators create, edit and cut off keys on the **Agents** page.
sources:
  - mcp/capabilities.py
  - mcp/service.py
  - mcp/models.py
  - mcp/settings.py
  - mcp/limits.py
  - mcp/telemetry.py
  - mcp/context.py
  - mcp/tools/_scope.py
  - shared/utils/bearer.py
  - api/app/api/v1/mcp.py
  - frontend/src/routes/(app)/agents/+page.svelte
  - frontend/src/lib/components/agents/
  - frontend/src/lib/components/access/ladder-pick.svelte
  - frontend/src/lib/types/mcp.ts
  - frontend/src/lib/utilities/mcp.ts
  - frontend/src/lib/stores/mcp.svelte.ts
revised: 2026-10-03
---

Every agent works through a key, and the key sets its limits. You choose what the agent may do, which projects it sees and how long the key lasts, and you can change access or cut an agent off at any time without touching your other agents.

The interface calls a token a key, and the client that holds it an agent. The protocol messages and the HTTP API call it a token.

## Capabilities

A key holds some of four capabilities. Each one gives access to a group of tools, from reading results up to launching scans. Use this table to decide how far an agent needs to go.

| Capability | Label | Grants | Reach line | Tools | Ceiling default |
|---|---|---|---|---|---|
| `read` | **Read** | Query assets, services, endpoints, findings and coverage. | **Reads** | 16 tools: `resolve_target`, `surface_brief`, `describe_query_language`, `list_targets`, `list_projects`, `list_engines`, `list_contexts`, `scan_status`, `query_assets`, `group_assets`, `what_changed`, `compare_runs`, `cve_exposure`, `domain_posture`, `explain_finding`, `scan_coverage` | On. Always granted. |
| `plan` | **Plan** | Resolve a scan plan without running it. | **Reads and plans scans** | `plan_scan` | On |
| `write` | **Write** | Add, change and delete targets. Record triage decisions. | **Reads and changes targets and triage** | `add_target`, `update_target`, `delete_target`, `record_triage` | On |
| `launch` | **Launch** | Start, pause, resume and cancel scans and focused rescans. | **Launches scans** | `start_scan`, `focused_rescan`, `pause_scan`, `resume_scan`, `cancel_scan` | Off |

`launch` is the one capability marked as reaching targets: only an agent with `launch` can send traffic to your targets. `start_scan`, `resume_scan` and `focused_rescan` send traffic to targets, and `start_scan` at passive intensity sends none. `start_scan` adds a target that is not yet in the project only when the key also holds `write`. `delete_target` belongs to `write` and is the one tool marked `destructiveHint`. Every tool is listed in [Tools](tools.md) and the [MCP tools reference](../../reference/mcp-tools.md).

Your agent sees only the tools its capabilities allow, because `tools/list` returns no others. If it calls a tool outside them anyway, it gets JSON-RPC error `-32002` with `This token lacks the <capability> capability.`, and the call history records the call as refused.

## Choose the access

You pick the access when you create the key, and you can change it later. In the connect sheet, **Access** is a ladder: **Read**, **Plan**, **Write**, **Launch**. The rung you select grants its own capability and every capability below it that the ceiling allows. The default is **Plan**, which grants `read` and `plan`. A rung that is off in the ceiling is disabled and shows **Off in the ceiling**. The line under the ladder sums up what the key can do and in which project, followed by **Sends no traffic** or **Sends traffic to targets**.

If you create keys through the HTTP API, `capabilities` is a list. reNgine stores any subset you send, adds `read`, and drops unknown names.

To change an agent's access later, select **Edit access** on its row. The sheet opens as **Edit access · {name}**, where you can change **Project** and **Access**. **Save** applies the change, and the toast reads **Access saved**. A key's name and expiry stay as they were set at creation. A revoked key cannot be edited.

## Set the ceiling for the instance { #instance-ceiling }

The ceiling is the highest access any key may hold. It lets an administrator switch a capability off for every agent at once, for example to keep all agents from launching scans. You set it in **Agent settings** under **Ceiling**, which reads **Highest access any key may hold.** Open it with **Settings** on the **Agents** page. Only administrators can change it.

Each capability has its own switch:

| Capability | Switch | Default |
|---|---|---|
| Read | Disabled, marked **required** | On |
| Plan | **Allow Plan** | On |
| Write | **Allow Write** | On |
| Launch | **Allow Launch**, marked with a warning icon labelled **Reaches targets** | Off |

The ceiling applies to every request, so changing it takes effect on existing keys too:

| Event | Effect |
|---|---|
| A request | The key runs with its stored capabilities limited by the ceiling at that moment, `read` included. |
| Create or edit a key above the ceiling | Refused: `<Label> is switched off for this instance. Raise the ceiling first.` |
| Lower the ceiling | Every key that exceeded it loses the capabilities now off. The toast reads **Ceiling saved**. |
| Raise the ceiling | Keys keep their stored capabilities. A capability removed by an earlier lowering is granted again with **Edit access**. |

The **Tools** sheet dims the capability groups that are off at the ceiling and marks their tools **Off**.

## Limit an agent to one project

Give an agent one project when it only needs one, so it cannot see the targets of your other projects. **Project** in the connect sheet is **Every project** or one project. A key reaches every target of its project. A key for **Every project** reaches every active project.

This is how the project scope works when your agent calls a tool:

| Case | Result |
|---|---|
| A tool names a target | The target is looked up inside the key's scope, by value, by id, or by a unique part of its value. |
| A tool takes `project_id` and the call omits it | The key's project. For **Every project**, the only active project. |
| Several projects in scope and no `project_id` | Tool error `Pass project_id. This token can see several projects: <name (id)>, …`, listing up to 8 |
| `project_id` outside the scope | Tool error `The project is outside this token's scope.` |
| The key's project is deleted | Every request is refused with `The token's project was deleted.` |

The **Scope** column of the **Agents** table shows the project name or **Every project** and the number of targets reached.

## Who a key acts for

Only administrators can open the **Agents** page. Other users see **Agents are managed by administrators**. Each key acts for the administrator who issued it, and works only while that account is active and still an administrator. Deactivating or demoting that account refuses the key with `The token's issuer is not an active administrator.` A password change does not affect it. The **Issued by** column then greys the name, with the hint **Not an active administrator. The key is refused.**, and reads **Deleted user** for a deleted account.

Scans, rescans, targets and triage decisions made through a key are attributed to its issuer, so each change an agent makes traces back to a person. The result caveats name the key, for example `Started by agent token 'claude-code' via MCP.`

## Key format

You need these details when you store a key in a secret manager or check one in a script.

| Property | Value |
|---|---|
| Format | `rngmcp_` followed by 48 lowercase hexadecimal characters, 55 characters in total |
| Source | 24 random bytes |
| Stored | The SHA-256 hash, and a display prefix of `rngmcp_` and the first 8 hexadecimal characters |
| Shown | Once, in the connect sheet and in the `secret` field of the create response |
| Sent as | `Authorization: Bearer <key>`. A bare key without `Bearer` is also accepted. |

reNgine refuses a value with another prefix or length before it looks anything up.

## Expiry

A key that expires limits the damage if it leaks. Choose the shortest expiry that fits the work.

| Choice | Days |
|---|---|
| **In 7 days** | 7 |
| **In 30 days** | 30, the default |
| **In 90 days** | 90 |
| **In a year** | 365 |
| **Never** | No expiry |

Through the HTTP API, `expires_in_days` takes 1 to 365, or `null` for no expiry, with a default of 30. The **Expires** column shows the date, **In {n} days** in the last seven days, **Expired** or **Never**. An expired key is refused with `The token expired.`

## Rotate a key

Rotate a key when it is about to expire or may have leaked. A key cannot be rotated in place, so you create a new one and then cut off the old one. Your agent keeps working throughout.

1. **Create the new key.** Select **Connect an agent** and choose the same project and access.
2. **Replace the key in the client.** Copy the new configuration into the client and confirm its first call.
3. **Cut access on the old key.** Select **Cut access** on the old agent's row.

## Cut access and delete

Cut access when an agent should stop working right away. Delete the agent afterwards to remove it from the list.

| Action | Where | Confirmation | Effect |
|---|---|---|---|
| **Cut access** | Row menu of a usable key | **Cut access**: `Agent {name} is disconnected and key {prefix}… stops working.` | The key is revoked and its live sessions are dropped. The toast reads **Access cut**. The row shows **Key revoked**. |
| **Delete** | Row menu of a revoked or expired key | **Delete agent**: `Agent {name} and its key are removed.` | The row is removed. The toast reads **Agent deleted**. |

A revoked key is refused with `The token was revoked.`

## Keys per instance

An instance holds at most 50 keys that are not revoked. Expired keys count until you cut their access or delete them, so clean up old agents when you get close to the limit. At the limit **Connect an agent** is disabled with **Limit of 50 agents reached.**, and the HTTP API answers `The instance has 50 tokens. Revoke one first.`

## Rate limit

The rate limit caps how many calls each agent makes per minute, so one busy agent cannot flood the instance.

| Setting | Value |
|---|---|
| Where | **Agent settings**, **Rate limit**, **calls per minute, per agent** |
| Default | 120 |
| Range | 1 to 10,000 |
| Counted | Every JSON-RPC request of the key, `initialize`, `tools/list` and `ping` included |
| Window | 60 seconds from the first request of the window |
| Over the limit | JSON-RPC error `-32002`, `Rate limit exceeded. Retry in a minute.` |

When you save it, the toast reads **Rate limit saved**. The limit is not applied while Redis is unreachable. For the other limits on the HTTP endpoint, see [Limits and errors](limits.md).

## The Agents table

The **Agents** table shows every agent at once: what it can do, what it reaches, when it last called and when its key expires.

| Column | Content |
|---|---|
| **Agent** | The name, a presence dot, and the client and version of the last request, the key prefix before the first request, or the key state |
| **Access** | The highest capability held, on a four-step meter |
| **Scope** | The project or **Every project**, and the number of targets |
| **Last call** | Time of the last request and **{n} calls**, or **Unused** |
| **Expires** | Date, **In {n} days**, **Expired**, **Never** or **Revoked** |
| **Issued by** | The administrator who created the key |

The presence dot tells you whether the agent is in use right now:

| Presence | Meaning |
|---|---|
| **Connected** | A request in the last minute |
| **Idle** | The last request between one and five minutes ago |
| **Offline** | No request in the last five minutes |
| **Key expired** | The key has expired |
| **Key revoked** | Access was cut |

The row menu holds **History**, **Edit access** and **Cut access**, or **History** and **Delete** for a revoked or expired key. The page refreshes every 10 seconds while it is visible.

## See what an agent did

The call history shows each tool your agent called, with its arguments and result, so you can check its work and see why a call was refused. Select an agent's name, or **History** in its row menu, to open it. The sheet takes the agent's name as its title and reads **Recent calls**.

| Element | Content |
|---|---|
| Filters | **All**, **Changes**, **Refused or failed**, each with a count. **Changes** are successful calls of `write` and `launch` tools. |
| Session | Calls of one agent and client at most five minutes apart, with the day, time, client, **{n} calls** and duration, and the number of changes and failures |
| Call | Time to the second, tool title, arguments, the result summary or **Refused.** with the error, the tool name, and **· changed data** or **· sent traffic** for a change |
| **Open** | Opens the `open_in_rengine` link of the result in the interface |

The history records every tool call: unknown tools, refused capabilities, invalid arguments, tool errors and successes. `initialize`, `tools/list` and `ping` are not recorded. The arguments line has at most 200 characters. To keep secrets out of the history, it leaves out arguments whose names contain `token`, `secret`, `password`, `header`, `cookie`, `auth` or `key`, removes URL query strings and masks detected secrets.

The instance keeps the newest 200 tool calls in Redis, across MCP keys, remote control chats and Ask conversations. The list expires seven days after the last call. The history sheet shows the MCP calls among them.

## Browse the tools

Use the **Tools** sheet to see exactly what an agent with a given access can call, and how much of its context the tool descriptions take. **Tools** on the **Agents** page lists every tool, grouped by capability, with the number of tools and their estimated context tokens per group. A group off at the ceiling is dimmed and marked **off**. Selecting a tool shows its name, capability, **Destructive** for `delete_target`, **Off** when its capability is off at the ceiling, the title and context tokens, the description, **Arguments** with type, **required** or default and allowed values, and **Examples**. <kbd>j</kbd> and <kbd>k</kbd>, or the arrow keys, move between tools.

## Agent settings

**Agent settings** holds the controls that apply to every agent: the server itself, the ceiling and the rate limit. Open it with **Settings** on the **Agents** page.

| Section | Content |
|---|---|
| **Server** | **Running** with the uptime, or **Stopped**. **Stopping disconnects every agent.** **Stop server** or **Start server**. **Endpoint**, **Protocol** and **stdio**, each with its value. |
| **Ceiling** | One switch per capability. See [Instance ceiling](#instance-ceiling). |
| **Rate limit** | Calls per minute, per agent |

**Stop server** with connected agents asks for confirmation: **Stop server**, `{n} connected agents are disconnected.` The toasts read **Server started** and **Server stopped**.

## Manage agents through the HTTP API

Use these endpoints to create and manage keys from a script instead of the **Agents** page. They take an administrator session, not an MCP key. `GET /api/v1/mcp/status` and `GET /api/v1/mcp/tools` take any signed-in user. The live sessions in the status are returned to administrators only.

| Method and path | Purpose |
|---|---|
| `GET /api/v1/mcp/status` | Server state, endpoint, stdio command, protocol version, rate limit, ceiling, live sessions, capability and client catalogues |
| `PATCH /api/v1/mcp/settings` | `enabled`, `rate_limit_per_minute`, `ceiling` |
| `GET /api/v1/mcp/tools` | Every tool with its schema, examples and `context_tokens` |
| `GET /api/v1/mcp/calls` | The call history, `limit` from 1 to 200, default 100 |
| `GET /api/v1/mcp/tokens` | Every key |
| `POST /api/v1/mcp/tokens` | Create a key. `201` with the key row, `secret` and the client configurations. |
| `PATCH /api/v1/mcp/tokens/{token_id}` | `name`, `project_id`, `capabilities` |
| `POST /api/v1/mcp/tokens/{token_id}/revoke` | Cut access. `204`. |
| `DELETE /api/v1/mcp/tokens/{token_id}` | Delete. `204`. |

```bash
# RENGINE=https://asm.example.com; jar holds the session from POST /api/v1/auth/login
curl -b jar -X POST "$RENGINE/api/v1/mcp/tokens" \
  -H "Content-Type: application/json" \
  -d '{"name": "triage-bot", "project_id": "'"$PROJECT"'",
       "capabilities": ["read", "write"], "expires_in_days": 90}'
```

```bash
curl -b jar -X PATCH "$RENGINE/api/v1/mcp/settings" \
  -H "Content-Type: application/json" \
  -d '{"ceiling": {"read": true, "plan": true, "write": true, "launch": true}}'
```

A `ceiling` object sets every capability: a capability left out takes its default. A refused change returns `400` with the message as `detail`.
