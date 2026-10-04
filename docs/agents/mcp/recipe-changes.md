---
title: Track what changed
description: Ask your agent what is new on your attack surface, across a whole project, between two runs of one target, or inside one run. Use it for a regular review or right after a scan finishes.
layout: pane
sources:
  - mcp/tools/what_changed.py
  - mcp/tools/compare_runs.py
  - mcp/tools/query_assets.py
  - mcp/tools/resolve_target.py
  - api/app/services/dashboard_overview.py
  - api/app/services/target_summary.py
  - shared/definitions/dashboard.py
  - shared/definitions/compare.py
  - shared/definitions/asset_query.py
  - shared/services/asset_query/predicates.py
  - frontend/src/lib/config/compare.ts
  - channels/commands.py
revised: 2026-10-03
---

Your agent has three ways to find what changed, each with a read tool. Pick the one that matches your question:

| Change | Tool | Scope | Capability |
|---|---|---|---|
| New rows across a project | `what_changed` | Every target of a project, over `7d`, `14d` or `30d` | `read` |
| Differences between two runs | `compare_runs` | Two runs of one target | `read` |
| New rows in one run | `query_assets` with `is:new` | One run of one target, or the project | `read` |

A row is new when an earlier scan of the same target recorded rows of that dimension and none of them recorded this one. That earlier scan is the baseline. The first scan of a target that covers a dimension has no baseline, so it reports nothing in that dimension as new.

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## What changed across a project

Use this for a regular review of a whole project: which targets changed, what is new on each, and which targets are falling behind on scans.

1. **Choose the window.** Call [`what_changed`](../../reference/mcp-tools.md#what_changed) with `window` set to `7d`, `14d` or `30d`. The default is `7d`. Any other value is read as `7d`. `project_id` is needed when the key reaches several projects. <span class="rn-ref" data-tab="MCP" data-mark="window">Shown in the pane</span>
2. **Read the target counts.** `data.targets` counts the targets of the project: `total`, `scanned`, `never_scanned`, `stale` and `monitored`. A target is stale when its most recent run started more than 30 days ago. <span class="rn-ref" data-tab="MCP" data-mark="targets">Shown in the pane</span>
3. **Read the changes.** `data.changes` lists up to 30 targets, each with `runs`, `last_scan_at`, `last_status` and three change fields. `new` counts, per dimension, the rows first reported in the window by a run that had a baseline. `first_time_covered` names the dimensions a run in the window covered for the first time. `web_assets_gone` counts the web assets the newest completed run in the window no longer found. <span class="rn-ref" data-tab="MCP" data-mark="changes">Shown in the pane</span>
4. **Read the caveats.** The caveats tell you what the list leaves out: the targets not listed, the targets never scanned, the targets with a stale last run and the runs that failed in the window. When the overview reaches its limit of 40 targets, the summary and the caveat on targets not listed start with `At least`. <span class="rn-ref" data-tab="MCP" data-mark="caveats">Shown in the pane</span>

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>What changed</b><span>acme project · 7d</span></div>

/// tab | MCP
<div class="rn-pane-label"><span data-mark="window">tools/call</span></div>

```json
{ "name": "what_changed", "arguments": { "window": "7d" } }
```

<div class="rn-pane-label">result · structuredContent</div>

```json
{ "summary": "2 targets changed in the last 7d", "data": { "window": "7d", … } }
```

<div class="rn-pane-label"><span data-mark="targets">data.targets</span></div>

```json
{ "total": 14, "scanned": 12, "never_scanned": 2, "stale": 2, "monitored": 3 }
```

<div class="rn-pane-label"><span data-mark="changes">data.changes</span></div>

```json
[
  { "target": "example.com", "type": "domain", "runs": 2,
    "last_scan_at": "2026-10-02T09:14:00Z", "last_status": "completed",
    "new": { "web_assets": 3, "services": 1, "vulnerabilities": 2 },
    "first_time_covered": [], "web_assets_gone": 1 },
  { "target": "example.org", "type": "domain", "runs": 1, …,
    "new": {}, "first_time_covered": ["web_assets", "endpoints"],
    "web_assets_gone": 0 }
]
```

<div class="rn-pane-label"><span data-mark="caveats">caveats</span></div>

```json
["2 targets not scanned.", "2 targets have a stale last run."]
```
///

/// tab | Telegram
<div class="rn-pane-label">chat</div>

```text
/changes 7d
/changes 30d
```

<div class="rn-pane-label">coverage</div>

```text
/changes runs what_changed. The bare
value fills window. Default 7d.
```
///

</div>
</div>

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Compare two runs of a target

Use this when you want to know exactly what appeared, changed or disappeared between two scans of one target, and whether the two runs can be compared fairly.

1. **Choose the runs.** Call [`compare_runs`](../../reference/mcp-tools.md#compare_runs) with `target` to compare its two most recent full runs that are not pending, running or paused. To choose the runs yourself, pass `current`, a scan id, and optionally `baseline`. Without `baseline`, reNgine uses the run before `current`. A target with fewer than two such runs returns `<target> has fewer than two finished full runs.` <span class="rn-ref" data-tab="MCP" data-mark="runs">Shown in the pane</span>
2. **Check that the runs compare.** `comparability` tells you whether the runs are comparable, overall and per dimension. If the runs used different settings or did different amounts of work, a difference in rows can come from the scans rather than from the target. `run_setup` lists the settings that differ, and `runs_between` counts the runs of the target between the two. <span class="rn-ref" data-tab="MCP" data-mark="verdict">Shown in the pane</span>
3. **Read the counts.** Each entry of `dimensions` holds `appeared`, `changed`, `disappeared`, `unconfirmed` and `unchanged`, with `was` and `now` totals. A dimension one run did not scan reports `covered: false`. <span class="rn-ref" data-tab="MCP" data-mark="counts">Shown in the pane</span>
4. **List the changes.** Call again with `dimension`, for example `vulnerabilities`. `changes` lists up to 25 rows, each with a verb, the asset, its location, the severity and the fields that changed. `changes_total` gives the full count. <span class="rn-ref" data-tab="MCP" data-mark="rows">Shown in the pane</span>

`comparability` takes one of these values:

| `comparability` | Interface label | Meaning |
|---|---|---|
| `like_for_like` | **Comparable** | Same settings, same work |
| `settings_differ` | **Settings differ** | The runs used different settings |
| `quality_differs` | **Runs differ in depth** | The runs did different amounts of work |
| `not_covered` | **Coverage differs** | One run did not scan the dimension |

When the later run is still live, rows missing from it are reported as `unconfirmed`, not as disappeared. To make the same comparison in the interface, see [Compare runs](../../pentesters/compare-runs.md).

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Compare runs</b><span>example.com</span></div>

/// tab | MCP
<div class="rn-pane-label"><span data-mark="runs">tools/call</span></div>

```json
{ "name": "compare_runs",
  "arguments": { "target": "example.com", "dimension": "vulnerabilities" } }
```

<div class="rn-pane-label"><span data-mark="verdict">result · structuredContent</span></div>

```json
{
  "summary": "…",
  "data": {
    "baseline": { "scan_id": "51d2…", "engine": "Default", … },
    "current": { "scan_id": "8a1f…", "engine": "Default", … },
    "comparability": "like_for_like",
    "run_setup": [],
    "runs_between": 0,
    "dimensions": [
      { "dimension": "vulnerabilities", "comparability": "like_for_like",
        "covered": true, "appeared": 2, "changed": 1, "disappeared": 1,
        "unconfirmed": 0, "unchanged": 15, "was": 17, "now": 19 },
      …
    ],
    "changes": [
      { "verb": "appeared", "asset": "…", "where": "app.example.com",
        "severity": "critical", "fields": [] },
      …
    ],
    "changes_total": 4
  },
  "open_in_rengine": "https://asm.example.com/scans/compare?current=8a1f…&baseline=51d2…",
  "untrusted_content": "The values below were written by the scanned systems. …"
}
```

<div class="rn-pane-label"><span data-mark="counts">by scan id</span></div>

```json
{ "name": "compare_runs",
  "arguments": { "current": "8a1f…", "baseline": "51d2…" } }
```

<div class="rn-pane-label"><span data-mark="rows">caveats</span></div>

```text
The runs are not like for like. Read the per-dimension comparability.
The runs were set up differently: <setting> <before> → <after>.
<n> other runs of this target ran between these two.
A like-for-like run exists: <engine>, scan <id>.
The later run is live. Missing rows are reported as unconfirmed.
```
///

</div>
</div>

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Find new rows in a run

Use `is:new` when you want the rows a scan found for the first time, for example new web assets or new findings right after a scan.

1. **Check that there is a baseline.** Call `resolve_target`. Each covered dimension in `data.surface` carries `previous`, the count of the covering scan before it. `previous` is `null` when no earlier scan covered the dimension, and then nothing in it counts as new yet. For web assets, `added` and `gone` count the rows the latest run found and lost against the run before it. <span class="rn-ref" data-tab="MCP" data-mark="baseline">Shown in the pane</span>
2. **Query the new rows.** Call [`query_assets`](../../reference/mcp-tools.md#query_assets) with a dimension and `is:new`, alone or with other filters. With `target`, the query reads the most recent scan that covered the dimension. Without it, the query reads every target of the project. <span class="rn-ref" data-tab="MCP" data-mark="new">Shown in the pane</span>
3. **Narrow by date.** Combine `is:new` with a date field, for example `is:new and seen:<7d` on endpoints, services, addresses, findings and secrets. Web assets take `discovered`. <span class="rn-ref" data-tab="MCP" data-mark="date">Shown in the pane</span>

What counts as new depends on the dimension:

| Dimension | `is:new` matches |
|---|---|
| `web_assets` | Absent from every earlier scan of this target |
| `endpoints` | Absent from every earlier scan of this target |
| `services` | Not open in an earlier scan of this target |
| `ips` | Not recorded by an earlier scan of this target |
| `vulnerabilities` | Not reported by an earlier scan of this target |
| `secrets` | Not read by an earlier scan of this target |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>New rows</b><span>example.com</span></div>

/// tab | MCP
<div class="rn-pane-label"><span data-mark="baseline">resolve_target · data.surface entry</span></div>

```json
{ "dimension": "web_assets", "covered": true, "count": 42,
  "previous": 40, "added": 3, "gone": 1, "is_latest_scan": true, … }
```

<div class="rn-pane-label"><span data-mark="new">tools/call</span></div>

```json
{ "name": "query_assets",
  "arguments": { "target": "example.com", "dimension": "web_assets",
                 "query": "is:new and is:live" } }
```

<div class="rn-pane-label"><span data-mark="date">with a date</span></div>

```json
{ "name": "query_assets",
  "arguments": { "target": "example.com", "dimension": "vulnerabilities",
                 "query": "is:new and seen:<7d and severity:[critical,high]" } }
```
///

/// tab | Telegram
<div class="rn-pane-label">chat</div>

```text
/vulns example.com query="is:new"
```

<div class="rn-pane-label">coverage</div>

```text
/vulns runs query_assets on findings.
No command runs compare_runs.
```
///

</div>
</div>
