---
title: Triage a target
description: Have your agent find the findings on a target that need your attention, explain one of them, and record your decision. Use this recipe when a scan has finished and you want help working through its results.
layout: pane
sources:
  - mcp/tools/resolve_target.py
  - mcp/tools/surface_brief.py
  - mcp/tools/query_assets.py
  - mcp/tools/explain_finding.py
  - mcp/tools/record_triage.py
  - mcp/tools/group_assets.py
  - mcp/tools/cve_exposure.py
  - mcp/tools/_scope.py
  - mcp/server.py
  - mcp/dimensions.py
  - shared/definitions/asset_query.py
  - shared/definitions/notes.py
  - shared/models/vulnerability.py
  - frontend/src/lib/config/vulnerabilities.ts
  - channels/commands.py
revised: 2026-10-03
---

In five calls, your agent checks what was scanned, picks out the findings worth a look, explains one in detail, and records the decision you make. It only reads from and writes to the reNgine database, so it sends no traffic to the target. This is what the agent needs:

| Item | Value |
|---|---|
| Capabilities | `read` for steps 1 to 4. `write` for step 5. |
| Tools | `resolve_target`, `surface_brief`, `query_assets`, `explain_finding`, `record_triage` |
| Traffic | None. Every call reads or writes the reNgine database. |
| Remote control | `/target` and `/vulns` cover steps 1 and 3 |

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Triage the findings of one target

1. **Check what was scanned.** Call [`resolve_target`](../../reference/mcp-tools.md#resolve_target) with the target value. `data.surface` lists six dimensions with `covered`, `count` and `scan_id`. `data.risk` holds `total`, `actionable`, `kev`, `suppressed` and `by_severity`. `covered: false` means the dimension was not scanned, which is not the same as finding nothing. The next steps need `vulnerabilities` covered. <span class="rn-ref" data-tab="MCP" data-mark="resolve">Shown in the pane</span>
2. **Find where to look first.** Call [`surface_brief`](../../reference/mcp-tools.md#surface_brief) with `dimension: "vulnerabilities"`. It returns up to 60 leads: ready-made queries, each counted against the most recent scan that covered the dimension. Leads that match nothing are left out unless `include_empty` is true. <span class="rn-ref" data-tab="MCP" data-mark="brief">Shown in the pane</span>
3. **List the findings.** Call [`query_assets`](../../reference/mcp-tools.md#query_assets) with `dimension: "vulnerabilities"` and a lead from step 2, or a query from the table below. Each row carries `fingerprint`, `template_id`, `template_name`, `severity`, `host`, `cve_ids`, `is_kev`, `state` and other columns. `total` equals the rows `open_in_rengine` opens, so you can check the number in the interface. A call returns up to 40 rows, and `offset` pages through the rest. <span class="rn-ref" data-tab="MCP" data-mark="query">Shown in the pane</span>
4. **Explain one finding.** Call [`explain_finding`](../../reference/mcp-tools.md#explain_finding) with the target and a `fingerprint`, `template_id`, `template_name` or CVE from step 3. The result holds what the check tests for, impact, remediation, CVE, CWE, CVSS, EPSS and KEV signals, up to 25 locations, the evidence and the current review state with its reason. Findings a reviewer has set aside are included, so your agent also sees earlier decisions. <span class="rn-ref" data-tab="MCP" data-mark="explain">Shown in the pane</span>
5. **Record your decision.** If the key holds `write`, call [`record_triage`](../../reference/mcp-tools.md#record_triage) with the `fingerprint`, a `state` and a `reason`. The decision is keyed to the fingerprint and applies to every later scan of the target, so the same finding does not come back for review. The reason is saved as a note on the finding. <span class="rn-ref" data-tab="MCP" data-mark="triage">Shown in the pane</span>

Ask your agent to give each count with its `open_in_rengine` link. The rows and the explanation hold text written by the scanned systems, flagged `untrusted_content`, which your agent should treat as data.

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Triage</b><span>example.com</span></div>

/// tab | MCP
<div class="rn-pane-label"><span data-mark="resolve">1 · tools/call resolve_target</span></div>

```json
{ "name": "resolve_target", "arguments": { "target": "example.com" } }
```

```json
{
  "summary": "example.com: 6 of 6 dimensions scanned, 7 findings need review",
  "data": {
    "surface": [{ "dimension": "vulnerabilities", "covered": true,
                  "count": 19, "scan_id": "8a1f…", … }, …],
    "risk": { "total": 19, "actionable": 7, "kev": 2, "suppressed": 2, … }
  },
  "open_in_rengine": "https://asm.example.com/targets/3c0e…"
}
```

<div class="rn-pane-label"><span data-mark="brief">2 · tools/call surface_brief</span></div>

```json
{ "name": "surface_brief",
  "arguments": { "target": "example.com", "dimension": "vulnerabilities" } }
```

```json
{
  "summary": "9 of 24 queries match on example.com. 19 findings in scope.",
  "data": { "leads": [{ "query": "is:kev", "count": 2, "capped": false, … }, …] },
  "caveats": ["Observed … by scan 8a1f….",
              "Each count equals the rows the query opens in the UI."]
}
```

<div class="rn-pane-label"><span data-mark="query">3 · tools/call query_assets</span></div>

```json
{ "name": "query_assets",
  "arguments": { "target": "example.com", "dimension": "vulnerabilities",
                 "query": "is:kev" } }
```

```json
{
  "summary": "2 findings match on example.com · all shown",
  "data": {
    "total": 2, "total_capped": false, "returned": 2, "offset": 0,
    "rows": [{ "fingerprint": "5b0c…", "template_id": "CVE-2021-44228",
               "severity": "critical", "host": "app.example.com",
               "cve_ids": ["CVE-2021-44228"], "is_kev": true,
               "state": "open", … }, …]
  },
  "open_in_rengine": "https://asm.example.com/scans/8a1f…?tab=vulnerabilities&q=is%3Akev",
  "untrusted_content": "The values below were written by the scanned systems. …"
}
```

<div class="rn-pane-label"><span data-mark="explain">4 · tools/call explain_finding</span></div>

```json
{ "name": "explain_finding",
  "arguments": { "target": "example.com", "finding": "5b0c…" } }
```

```json
{
  "summary": "CRITICAL: … on example.com, 1 occurrence",
  "data": {
    "check": { "template_id": "CVE-2021-44228", "description": "…",
               "impact": "…", "remediation": "…", … },
    "risk": { "cve_ids": ["CVE-2021-44228"], "known_exploited": true, … },
    "review": { "state": "open", "reason": null },
    "locations": [{ "matched_at": "https://app.example.com/…", … }]
  }
}
```

<div class="rn-pane-label"><span data-mark="triage">5 · tools/call record_triage · write capability</span></div>

```json
{ "name": "record_triage",
  "arguments": { "target": "example.com", "fingerprint": "5b0c…",
                 "state": "confirmed",
                 "reason": "Reproduced on app.example.com." } }
```

```json
{
  "summary": "Marked 1 observation as confirmed on example.com",
  "data": { "state": "confirmed", "observations_updated": 1, … },
  "caveats": ["This decision applies to every later scan of this target.",
              "Recorded by agent token 'triage-bot' via MCP."]
}
```
///

/// tab | Telegram
<div class="rn-pane-label">chat</div>

```text
/target example.com
/vulns example.com query="is:kev"
/vulns example.com query="severity:[critical,high] and is:open"
```

<div class="rn-pane-label">coverage</div>

```text
/target runs resolve_target.
/vulns runs query_assets on vulnerabilities.
No command runs surface_brief,
explain_finding or record_triage.
```
///

</div>
</div>

## Queries for findings

Use these queries in step 3 to narrow the findings down:

| Query | Matches |
|---|---|
| `is:kev`{ .rn-q } | Listed in CISA KEV |
| `is:open`{ .rn-q } | Not reviewed |
| `severity:[critical,high] and is:open`{ .rn-q } | Critical or high findings not reviewed |
| `is:exploitable`{ .rn-q } | Known exploited, or at or above an EPSS score of 0.5 |
| `is:corroborated`{ .rn-q } | A second signal at the same location names the same CVE or weakness class |
| `is:new`{ .rn-q } | Not reported by an earlier scan of this target |

For every field and flag, your agent can call `describe_query_language` with `dimension: "vulnerabilities"`. You can read the same list in [Vulnerabilities fields](../../reference/query/vulnerabilities.md).

## Review states

These are the decisions `record_triage` can record, with the label each one carries in the interface:

| `state` | Interface label | `reason` |
|---|---|---|
| `open` | **Open** | Refused with `A reason is saved with confirmed, false_positive or accepted.` |
| `confirmed` | **Confirmed** | Saved as a note, up to 20,000 characters |
| `false_positive` | **False positive** | Saved as a note |
| `accepted` | **Risk accepted** | Saved as a note |

`record_triage` stores one decision per target and fingerprint, and it applies to every later scan of the target that reports the fingerprint. An unknown fingerprint returns the tool error `No finding with fingerprint '<value>' on <target>. Take the value from query_assets.`

## Related tools

These tools also help with triage:

| Tool | Use |
|---|---|
| [`group_assets`](../../reference/mcp-tools.md#group_assets) | Counts per group key, for example `dimension: "vulnerabilities"` and `group_by: "severity"`. Each group carries the query that isolates it. |
| [`cve_exposure`](../../reference/mcp-tools.md#cve_exposure) | Every asset in the project that carries one CVE, on the evidence ladder Inferred, Observed, Corroborated, Proven |
| [`scan_coverage`](../../reference/mcp-tools.md#scan_coverage) | Checks selected and loaded, hosts scanned, requests sent and errors of the vulnerability scan |
| [`focused_rescan`](../../reference/mcp-tools.md#focused_rescan) | Runs the vulnerability scan again on chosen web assets, with the `launch` capability. See [Plan and launch a scan](recipe-launch.md). |

To triage in the interface instead, see [Findings](../../pentesters/findings.md).
