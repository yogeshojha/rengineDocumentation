---
title: Plan and launch a scan
description: Let your agent show you what a scan would do before anything runs, then start it, follow it and rescan chosen assets. Planning sends no traffic. Launching does, so an administrator has to allow it first.
layout: pane
sources:
  - mcp/tools/list_plans.py
  - mcp/tools/plan_scan.py
  - mcp/tools/start_scan.py
  - mcp/tools/scan_runs.py
  - mcp/tools/focused_rescan.py
  - mcp/capabilities.py
  - shared/models/scan_preview.py
  - shared/services/scan_resolve.py
  - shared/enums/scan.py
  - shared/definitions/rescan.py
  - frontend/src/lib/components/agents/settings-sheet.svelte
  - channels/commands.py
revised: 2026-10-03
---

Planning and launching are separate capabilities. With **Plan**, your agent can show you which stages would run, at what rate and for about how long, without contacting the target. Only an agent with **Launch** can start the scan, and **Launch** is off for the instance until an administrator allows it. This is what each part needs:

| Item | Value |
|---|---|
| Capabilities | `read` for the lists and the status. `plan` for `plan_scan`. `launch` for `start_scan`, `focused_rescan`, `pause_scan`, `resume_scan` and `cancel_scan`. |
| Ceiling | `launch` is off at the instance ceiling by default |
| Traffic | `start_scan` sends traffic to the target unless the intensity is passive. `focused_rescan` sends traffic to the named assets. `plan_scan` contacts nothing. |
| Attribution | Scans and rescans are created as the administrator who issued the key. The caveats name the key. |
| Remote control | `/scan`, `/progress`, `/scans`, `/pause`, `/resume`, `/cancel` |

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Plan the scan

Plan first when you want to see what a scan would do before anything reaches the target.

1. **Give the agent access.** An administrator switches on **Allow Launch** under **Ceiling** in **Agent settings**, then selects **Edit access** on the agent's row, sets **Access** to **Launch** and selects **Save**. Planning alone needs **Plan**. See [Control what an agent can do](capabilities.md).
2. **List the scan engines.** A scan engine is a saved selection of stages with its settings and an intensity. Call [`list_engines`](../../reference/mcp-tools.md#list_engines), optionally with `contains`. Each engine has an `id`, `name`, `description`, `intensity` and the `stages` its document enables. Up to 25 are returned by default, 50 at most. <span class="rn-ref" data-tab="MCP" data-mark="engines">Shown in the pane</span>
3. **List the scan contexts.** A scan context holds the scope, authentication, rate limits and proxy for a run, so you set them once and every scan that uses the context follows them. Call [`list_contexts`](../../reference/mcp-tools.md#list_contexts). Each context has an `id`, `name`, the authentication kind, the rate limit, exclusions, `only_these_hosts` and `through_proxy`. Credentials are not returned to the agent. <span class="rn-ref" data-tab="MCP" data-mark="contexts">Shown in the pane</span>
4. **Plan the scan.** Call [`plan_scan`](../../reference/mcp-tools.md#plan_scan) with the target and either `engine_id` or a list of `stages`, and optionally `intensity`. The target does not need to exist yet. The result lists each phase with its stages, each with a status and the reason for a skip, a summary with the rate settings and the estimated duration, and warnings. The caveat reads `Nothing ran.` <span class="rn-ref" data-tab="MCP" data-mark="plan">Shown in the pane</span>

Each stage in the plan has a status, and a skipped stage carries its reason:

| Stage status | `reason` |
|---|---|
| `will_run` | None |
| `skipped_disabled` | `Disabled in engine.` or `Skipped at passive intensity.` |
| `skipped_not_applicable` | `Not applicable to <type> targets.` |
| `skipped_no_input` | `No earlier stage produces <kinds>.` |
| `skipped_needs_key` | `<stage> skipped. API key not configured.` |

`plan_scan` takes no scan context.

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Plan</b><span>example.com</span></div>

/// tab | MCP
<div class="rn-pane-label"><span data-mark="engines">tools/call list_engines</span></div>

```json
{ "name": "list_engines", "arguments": {} }
```

```json
{
  "summary": "…",
  "data": [
    { "id": "0b7e…", "name": "Default", "intensity": "normal",
      "stages": ["subdomain_discovery", "http_probe", "vulnerability_scan", …], … }
  ],
  "open_in_rengine": "https://asm.example.com/automation/engines"
}
```

<div class="rn-pane-label"><span data-mark="contexts">tools/call list_contexts</span></div>

```json
{ "name": "list_contexts", "arguments": {} }
```

```json
{
  "data": [{ "id": "c41a…", "name": "staging login", "auth": "…",
             "rate_limit_per_minute": 300, "through_proxy": false, … }],
  "open_in_rengine": "https://asm.example.com/automation/contexts",
  "caveats": ["Credentials are not returned."]
}
```

<div class="rn-pane-label"><span data-mark="plan">tools/call plan_scan · plan capability</span></div>

```json
{
  "name": "plan_scan",
  "arguments": {
    "target": "example.com",
    "stages": ["subdomain_discovery", "vulnerability_scan"],
    "intensity": "passive"
  }
}
```

```json
{
  "summary": "… stages would run against example.com using …",
  "data": {
    "phases": [{ "phase": "…", "stages": [
      { "stage": "subdomain_discovery", "label": "…",
        "status": "will_run", "reason": null }, …] }, …],
    "summary": { "rate_summary": "…", "estimated_duration_human": "…", … },
    "warnings": []
  },
  "caveats": ["Nothing ran."]
}
```
///

</div>
</div>

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Start and follow the scan

Once the plan looks right, your agent can start the scan and check on it until it finishes. This needs **Launch**.

1. **Start the scan.** Call [`start_scan`](../../reference/mcp-tools.md#start_scan) with the target and either `engine_id` or `stages`, and optionally `intensity` and `context_id`. `intensity` overrides the engine's intensity. If the value is not yet a target of the project, reNgine adds it, but only when the key also holds `write`. The result holds `scan_id`, `status`, `engine`, `target_id` and `started_at`, and a link to the run. <span class="rn-ref" data-tab="MCP" data-mark="start">Shown in the pane</span>
2. **Read the traffic caveat.** The first caveat tells you whether traffic is going out. It reads `Traffic is being sent to the target.`, or `Passive intensity. No traffic reaches the target.` <span class="rn-ref" data-tab="MCP" data-mark="start">Shown in the pane</span>
3. **Check the status.** Call [`scan_status`](../../reference/mcp-tools.md#scan_status) with `scan`. The result holds the status, the stages done, running, failed and skipped, and `found_so_far` per dimension. The server sends no progress notifications, so your agent has to ask. Without arguments, `scan_status` lists the pending and running scans, or the most recent runs when none is live. <span class="rn-ref" data-tab="MCP" data-mark="status">Shown in the pane</span>
4. **Pause, resume or cancel.** [`pause_scan`](../../reference/mcp-tools.md#pause_scan) pauses a running scan. [`resume_scan`](../../reference/mcp-tools.md#resume_scan) restarts a paused scan at its first unfinished stage. [`cancel_scan`](../../reference/mcp-tools.md#cancel_scan) stops a pending, running or paused scan. Each takes `scan` or `target`. Results written so far are kept. <span class="rn-ref" data-tab="MCP" data-mark="control">Shown in the pane</span>
5. **Read the results.** When the status is `completed`, call `resolve_target` and `query_assets`. See [Triage a target](recipe-triage.md).

`scan_status` reports one of these statuses:

| Status | Meaning |
|---|---|
| `pending` | Queued |
| `running` | Stages are running |
| `paused` | Stopped by `pause_scan`. Stages that were running run again from the start on resume. |
| `completed` | Finished |
| `failed` | Finished with an error. `data.error` holds it. |
| `cancelled` | Stopped by `cancel_scan` |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Launch</b><span>example.com</span></div>

/// tab | MCP
<div class="rn-pane-label"><span data-mark="start">tools/call start_scan · launch capability</span></div>

```json
{
  "name": "start_scan",
  "arguments": {
    "target": "example.com",
    "engine_id": "0b7e…",
    "intensity": "normal"
  }
}
```

```json
{
  "summary": "Scan started on example.com with Default",
  "data": { "scan_id": "8a1f…", "status": "pending", "engine": "Default",
            "target": "example.com", "target_id": "3c0e…", … },
  "open_in_rengine": "https://asm.example.com/scans/8a1f…",
  "caveats": ["Traffic is being sent to the target.",
              "scan_status follows the run. cancel_scan stops it.",
              "Started by agent token 'claude-code' via MCP."]
}
```

<div class="rn-pane-label"><span data-mark="status">tools/call scan_status</span></div>

```json
{ "name": "scan_status", "arguments": { "scan": "8a1f…" } }
```

```json
{
  "summary": "running: 4 of 11 stages done, running …",
  "data": {
    "status": "running", "elapsed_seconds": 412,
    "stages": { "done": […], "running": […] },
    "found_so_far": { "Web assets": 42, "IP addresses": 12, "Services": 0,
                      "Endpoints": 0, "Vulnerabilities": 0 },
    "error": null, …
  },
  "caveats": ["The run has not finished. Counts are partial."]
}
```

<div class="rn-pane-label"><span data-mark="control">pause, resume, cancel</span></div>

```json
{ "name": "pause_scan",  "arguments": { "scan": "8a1f…" } }
{ "name": "resume_scan", "arguments": { "target": "example.com" } }
{ "name": "cancel_scan", "arguments": { "target": "example.com" } }
```
///

/// tab | Telegram
<div class="rn-pane-label">chat</div>

```text
/scan example.com intensity=passive
/scan example.com engine_id=0b7e…
/progress 8a1f…
/scans
/pause 8a1f…
/resume 8a1f…
/cancel 8a1f…
```

<div class="rn-pane-label">confirmation</div>

```text
/scan, /pause, /resume and /cancel are
confirmed with the account's
authenticator code.
```
///

</div>
</div>

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Rescan chosen assets

A focused rescan runs a few stages again on assets picked from completed scans, without enumerating the whole target again. Use it to take a fresh look at a handful of assets, for example new web assets or the web assets behind a finding.

1. **Pick the assets.** Call `query_assets` on the target and take the values from the rows: host names for web assets, endpoints, findings and secrets, IP addresses for services and addresses. An IP address is read as an address in every dimension. <span class="rn-ref" data-tab="MCP" data-mark="pick">Shown in the pane</span>
2. **Start the rescan.** Call [`focused_rescan`](../../reference/mcp-tools.md#focused_rescan) with the target, the `dimension` and up to 200 `assets`. `stages` is optional, up to 20. Without it, the dimension's default stages run. The parent is the most recent scan of the target that covered the dimension. <span class="rn-ref" data-tab="MCP" data-mark="rescan">Shown in the pane</span>
3. **Follow the new run.** The rescan is a separate run with its own `scan_id`. Its results are recorded on the new run, not on the parent. Poll it with `scan_status`. <span class="rn-ref" data-tab="MCP" data-mark="rescan">Shown in the pane</span>

Without `stages`, these stages run for each dimension:

| Dimension | Default stages |
|---|---|
| `web_assets` | `http_probe` |
| `endpoints` | `http_probe`, `url_discovery` |
| `services` | `port_scan` |
| `ips` | `port_scan` |
| `vulnerabilities` | `http_probe`, `vulnerability_scan` |
| `secrets` | `http_probe`, `secret_mining` |

The rescannable stages are `http_probe`, `port_scan`, `screenshot`, `secret_mining`, `url_discovery`, `vhost` and `vulnerability_scan`. Telegram has no command for `focused_rescan`. To run a focused rescan in the interface, see [Focused rescans](../../pentesters/focused-rescans.md).

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Focused rescan</b><span>example.com</span></div>

/// tab | MCP
<div class="rn-pane-label"><span data-mark="pick">tools/call query_assets</span></div>

```json
{ "name": "query_assets",
  "arguments": { "target": "example.com", "dimension": "web_assets",
                 "query": "is:new and is:live" } }
```

<div class="rn-pane-label"><span data-mark="rescan">tools/call focused_rescan · launch capability</span></div>

```json
{
  "name": "focused_rescan",
  "arguments": {
    "target": "example.com",
    "dimension": "vulnerabilities",
    "assets": ["app.example.com", "api.example.com"]
  }
}
```

```json
{
  "summary": "Rescanning 2 findings on example.com with …",
  "data": { "scan_id": "e93d…", "parent_scan_id": "8a1f…",
            "dimension": "vulnerabilities", "assets": 2,
            "stages": ["http_probe", "vulnerability_scan"],
            "status": "pending" },
  "open_in_rengine": "https://asm.example.com/scans/e93d…",
  "caveats": ["Traffic is being sent to these assets.",
              "Results are recorded on this run, not on the parent scan."]
}
```
///

</div>
</div>

## Intensity

Intensity decides how hard a scan hits your target. Your agent sets it with `intensity`, and the interface describes each value like this:

| `intensity` | Interface text |
|---|---|
| `passive` | Findings come from public sources only. No request reaches the target. |
| `normal` | 150 requests a second per tool. 1,000 packets a second for the port scan. |
| `aggressive` | 400 requests a second per tool. 3,000 packets a second for the port scan, and higher concurrency. |

!!! note ""
    Passive intensity is a run-level switch. The Passive preset is a stage selection saved in a scan engine. Stage names such as `passive_ports` describe one stage. The three are separate. See [Scan engines and intensity](../../pentesters/scan-engines.md).

## Launch errors

If a launch is refused, the message tells you why:

| Message | Cause |
|---|---|
| `This token lacks the launch capability.` | JSON-RPC error `-32002`. The key does not hold `launch`, or the ceiling has it off. |
| `<value> is not a target in this project. Adding a target needs the write capability.` | `start_scan` on a new value without `write` |
| `Scan not started: <reason>` | The scan service refused the launch |
| `Plan not valid: <reason>`, `Plan not resolved: <reason>` | `plan_scan` could not build or resolve the plan |
| `The scan is <status>. Nothing to pause.` | `pause_scan` on a scan that is not running |
| `The scan is <status>. Nothing to resume.` | `resume_scan` on a scan that is not paused |
| `The scan is <status>. Nothing to stop.` | `cancel_scan` on a finished scan |
| `No scan with id '<id>'. Take the id from start_scan or scan_status.` | Unknown scan id |
| `Not rescannable: <stages>. Choose from: <stages>.` | `focused_rescan` with a stage outside the rescannable list |
| `Rescan not started: no asset matched the parent scan.` | None of the assets is in the parent scan |
