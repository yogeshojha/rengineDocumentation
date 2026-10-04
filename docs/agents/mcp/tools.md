---
title: Tools
description: "The 26 tools an AI agent can call on the reNgine MCP server, grouped by the capability a token needs to use them. Use this page to decide which capabilities to give an agent."
sources:
  - mcp/registry.py
  - mcp/tools/
  - mcp/capabilities.py
revised: 2026-10-03
generated: scripts/gen_mcp.py
layout: pane
---

This page is generated from the reNgine 3.0 source. `scripts/gen_mcp.py` writes it from `data/mcp-tools.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

Each tool needs one capability, and a token sees only the tools of the capabilities it holds. Every token holds Read. Grant another capability when the agent needs to do more. <span class="rn-tag passive">Passive</span> marks a tool that sends no traffic to your target, <span class="rn-tag active">Active</span> a tool that does.

## Read

Query assets, services, endpoints, findings and coverage. Every token has this capability.

| Tool | Reach | What it does |
|---|---|---|
| [`describe_query_language`](../../reference/mcp-tools.md#describe_query_language) | <span class="rn-tag passive">Passive</span> | The query grammar for one dimension: fields with types and operators, is:/has: flags, group keys and examples. |
| [`list_contexts`](../../reference/mcp-tools.md#list_contexts) | <span class="rn-tag passive">Passive</span> | The saved scan contexts in a project, with the id start_scan takes. |
| [`list_engines`](../../reference/mcp-tools.md#list_engines) | <span class="rn-tag passive">Passive</span> | The saved scan engines in a project, with the id start_scan and plan_scan take. |
| [`list_projects`](../../reference/mcp-tools.md#list_projects) | <span class="rn-tag passive">Passive</span> | The projects this token can reach. |
| [`list_targets`](../../reference/mcp-tools.md#list_targets) | <span class="rn-tag passive">Passive</span> | The targets this token can reach, with project and type. |
| [`resolve_target`](../../reference/mcp-tools.md#resolve_target) | <span class="rn-tag passive">Passive</span> | For each of a target's result dimensions: whether it was scanned, what the most recent covering scan found, when, and the scan id other tools take. |
| [`scan_status`](../../reference/mcp-tools.md#scan_status) | <span class="rn-tag passive">Passive</span> | Status of a scan: stages finished, running and failed, and counts found so far. |
| [`surface_brief`](../../reference/mcp-tools.md#surface_brief) | <span class="rn-tag passive">Passive</span> | The curated query library, each query counted against the target's most recent covering scan and ranked by how well it discriminates. |
| [`compare_runs`](../../reference/mcp-tools.md#compare_runs) | <span class="rn-tag passive">Passive</span> | Rows that appeared, changed and disappeared between two runs of one target, per result dimension. |
| [`cve_exposure`](../../reference/mcp-tools.md#cve_exposure) | <span class="rn-tag passive">Passive</span> | Every asset in the estate that carries one CVE, across both findings dimensions, counted on one evidence ladder. |
| [`domain_posture`](../../reference/mcp-tools.md#domain_posture) | <span class="rn-tag passive">Passive</span> | Sender, mail-transport and zone checks per registrable domain of a target, from its newest settled run: SPF policy and lookup count, DMARC policy and subdomain policy, DKIM selectors found, MTA-STS mode, TLS-RPT, DNSSEC and CAA. |
| [`group_assets`](../../reference/mcp-tools.md#group_assets) | <span class="rn-tag passive">Passive</span> | Count a target's surface by a group key: technology, status, ASN, country, severity, service class. |
| [`query_assets`](../../reference/mcp-tools.md#query_assets) | <span class="rn-tag passive">Passive</span> | Search one dimension of the attack surface with the query language, on one target or across every target in the project. |
| [`what_changed`](../../reference/mcp-tools.md#what_changed) | <span class="rn-tag passive">Passive</span> | New web assets, services, endpoints, addresses and findings per target over a window, plus targets not scanned or stale. |
| [`explain_finding`](../../reference/mcp-tools.md#explain_finding) | <span class="rn-tag passive">Passive</span> | One finding in full: what the check tests for, impact, remediation, CVE, CWE, CVSS, EPSS and KEV signals, every location on the target, and the triage decision with its reason. |
| [`scan_coverage`](../../reference/mcp-tools.md#scan_coverage) | <span class="rn-tag passive">Passive</span> | The scanner's account of a run: checks selected and loaded, hosts scanned, requests sent, errors and hosts abandoned. |

## Plan

Resolve a scan plan without running it. The instance ceiling allows it by default, so you can grant it to a token.

| Tool | Reach | What it does |
|---|---|---|
| [`plan_scan`](../../reference/mcp-tools.md#plan_scan) | <span class="rn-tag passive">Passive</span> | Resolve what a scan would do: stages and their order, skipped stages and the reason, footprint and estimated duration. |

## Write

Add, change and delete targets. Record triage decisions. The instance ceiling allows it by default, so you can grant it to a token.

| Tool | Reach | What it does |
|---|---|---|
| [`add_target`](../../reference/mcp-tools.md#add_target) | <span class="rn-tag passive">Passive</span> | Add targets to a project. |
| [`delete_target`](../../reference/mcp-tools.md#delete_target) | <span class="rn-tag passive">Passive</span> | Delete a target and everything recorded against it: scans, web assets, services, endpoints, findings and triage decisions. |
| [`record_triage`](../../reference/mcp-tools.md#record_triage) | <span class="rn-tag passive">Passive</span> | Record a review decision against a finding: confirmed, false positive or accepted risk. |
| [`update_target`](../../reference/mcp-tools.md#update_target) | <span class="rn-tag passive">Passive</span> | Change a target's display name, tags or organizations. |

## Launch

Start, pause, resume and cancel scans and focused rescans. The instance ceiling does not allow it by default. An administrator must allow it before any token can use it.

| Tool | Reach | What it does |
|---|---|---|
| [`cancel_scan`](../../reference/mcp-tools.md#cancel_scan) | <span class="rn-tag active">Active</span> | Stop a running scan. |
| [`focused_rescan`](../../reference/mcp-tools.md#focused_rescan) | <span class="rn-tag active">Active</span> | Re-run a set of stages against named assets as a separate scan. |
| [`pause_scan`](../../reference/mcp-tools.md#pause_scan) | <span class="rn-tag active">Active</span> | Pause a running scan. |
| [`resume_scan`](../../reference/mcp-tools.md#resume_scan) | <span class="rn-tag active">Active</span> | Resume a paused scan. |
| [`start_scan`](../../reference/mcp-tools.md#start_scan) | <span class="rn-tag active">Active</span> | Start a scan against a target in this token's project. |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Tool discovery</b><span>JSON-RPC 2.0</span></div>

/// tab | MCP
<div class="rn-pane-label">request</div>

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

<div class="rn-pane-label">tools a read-only token sees</div>

```text
describe_query_language
list_contexts
list_engines
list_projects
list_targets
resolve_target
scan_status
surface_brief
compare_runs
cve_exposure
domain_posture
group_assets
query_assets
what_changed
explain_finding
scan_coverage
```
///

/// tab | Call
<div class="rn-pane-label">tools/call</div>

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "resolve_target",
    "arguments": {
      "target": "example.com"
    }
  }
}
```
///

</div>
</div>

For the parameters and the return shape of each tool, see the [MCP tools reference](../../reference/mcp-tools.md).
