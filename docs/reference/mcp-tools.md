---
title: MCP tools
description: "All 26 tools of the reNgine MCP server: what each one does, the capability it needs, whether it sends traffic to your target, its parameters and what it returns. Use it when you build an agent on reNgine or want to know exactly what your agent can do."
sources:
  - mcp/registry.py
  - mcp/tools/
  - mcp/capabilities.py
revised: 2026-10-03
generated: scripts/gen_mcp.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_mcp.py` writes it from `data/mcp-tools.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Your MCP client sees and calls only the tools that the capabilities of its token allow. The server is called `rengine`, its endpoint is `<UI origin>/api/v1/mcp`, and it uses protocol version `2025-06-18`. To decide what a token may do, see [Capabilities and tokens](../agents/mcp/capabilities.md). Some tools also have a Telegram command that runs the same tool, listed under **Telegram command**.

## All tools

The tools are grouped by what they help an agent do. **Reach** tells you whether a tool sends traffic to your target. Select a tool to see its parameters and what it returns.

| Tool | Group | Capability | Reach | Title |
|---|---|---|---|---|
| [`describe_query_language`](#describe_query_language) | Orient | read | <span class="rn-tag passive">Passive</span> | Describe query language |
| [`list_contexts`](#list_contexts) | Orient | read | <span class="rn-tag passive">Passive</span> | List scan contexts |
| [`list_engines`](#list_engines) | Orient | read | <span class="rn-tag passive">Passive</span> | List scan engines |
| [`list_projects`](#list_projects) | Orient | read | <span class="rn-tag passive">Passive</span> | List projects |
| [`list_targets`](#list_targets) | Orient | read | <span class="rn-tag passive">Passive</span> | List targets |
| [`resolve_target`](#resolve_target) | Orient | read | <span class="rn-tag passive">Passive</span> | Resolve target |
| [`scan_status`](#scan_status) | Orient | read | <span class="rn-tag passive">Passive</span> | Scan status |
| [`surface_brief`](#surface_brief) | Orient | read | <span class="rn-tag passive">Passive</span> | Surface brief |
| [`compare_runs`](#compare_runs) | Interrogate | read | <span class="rn-tag passive">Passive</span> | Compare runs |
| [`cve_exposure`](#cve_exposure) | Interrogate | read | <span class="rn-tag passive">Passive</span> | CVE exposure |
| [`domain_posture`](#domain_posture) | Interrogate | read | <span class="rn-tag passive">Passive</span> | Domain posture |
| [`group_assets`](#group_assets) | Interrogate | read | <span class="rn-tag passive">Passive</span> | Group assets |
| [`query_assets`](#query_assets) | Interrogate | read | <span class="rn-tag passive">Passive</span> | Query assets |
| [`what_changed`](#what_changed) | Interrogate | read | <span class="rn-tag passive">Passive</span> | What changed |
| [`explain_finding`](#explain_finding) | Explain | read | <span class="rn-tag passive">Passive</span> | Explain finding |
| [`scan_coverage`](#scan_coverage) | Explain | read | <span class="rn-tag passive">Passive</span> | Scan coverage |
| [`plan_scan`](#plan_scan) | Act | plan | <span class="rn-tag passive">Passive</span> | Plan a scan |
| [`add_target`](#add_target) | Act | write | <span class="rn-tag passive">Passive</span> | Add targets |
| [`delete_target`](#delete_target) | Act | write | <span class="rn-tag passive">Passive</span> | Delete a target |
| [`record_triage`](#record_triage) | Act | write | <span class="rn-tag passive">Passive</span> | Record triage |
| [`update_target`](#update_target) | Act | write | <span class="rn-tag passive">Passive</span> | Update a target |
| [`cancel_scan`](#cancel_scan) | Act | launch | <span class="rn-tag active">Active</span> | Cancel a scan |
| [`focused_rescan`](#focused_rescan) | Act | launch | <span class="rn-tag active">Active</span> | Focused rescan |
| [`pause_scan`](#pause_scan) | Act | launch | <span class="rn-tag active">Active</span> | Pause a scan |
| [`resume_scan`](#resume_scan) | Act | launch | <span class="rn-tag active">Active</span> | Resume a scan |
| [`start_scan`](#start_scan) | Act | launch | <span class="rn-tag active">Active</span> | Start a scan |

## Orient

Tools that help an agent find its way: projects, targets, scan engines, scan contexts, the query language, the status of a scan, and what was scanned for a target.

### describe_query_language { #describe_query_language }

The query grammar for one dimension: fields with types and operators, is:/has: flags, group keys and examples. Fields differ per dimension.

Title
:   Describe query language

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 165 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `dimension` | `string` | `web_assets` |  | Which grammar to describe. One of: web_assets, endpoints, services, ips, vulnerabilities, secrets. |
| `fields_only` | `boolean` | `false` |  | Return field names only. |

Returns
:   data{dimension,noun,max_query_length,connectors[{symbol,means}],operators[{symbol,means}],flags[{flag,means}],fields[{name,type,operators,means,example,values?,aliases?}],group_keys[{key,label,means}],examples[{query,means}] (first 20)}; with fields_only: data{dimension,fields[names]}. No open_in_rengine link.

Examples, written as the tool name followed by its arguments:

```text
describe_query_language dimension=services
```

### list_contexts { #list_contexts }

The saved scan contexts in a project, with the id start_scan takes. A context carries authentication, scope, rate limits and proxy. Credentials are not returned.

Title
:   List scan contexts

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 156 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `project_id` | <code>string &#124; null</code> | None |  | Which project's contexts. Omit when the token is scoped to one. |
| `limit` | `integer` | `25` | 1 to 50 |  |

Returns
:   data[] of {id,name,description,auth,rate_limit_per_minute,excluded{hosts,paths,addresses},only_these_hosts,through_proxy,last_used_at}. Credentials are not returned. open_in_rengine: /automation/contexts.

Examples, written as the tool name followed by its arguments:

```text
list_contexts
```

### list_engines { #list_engines }

The saved scan engines in a project, with the id start_scan and plan_scan take. An engine is a named configuration of stages.

Title
:   List scan engines

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 188 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `contains` | <code>string &#124; null</code> | None |  | Only engines whose name or description contains this text. |
| `project_id` | <code>string &#124; null</code> | None |  | Which project's engines. Omit when the token is scoped to one. |
| `limit` | `integer` | `25` | 1 to 50 |  |

Returns
:   data[] of {id,name,description,intensity,stages[enabled stage names],last_used_at}. open_in_rengine: /automation/engines.

Examples, written as the tool name followed by its arguments:

```text
list_engines
list_engines contains=passive
```

### list_projects { #list_projects }

The projects this token can reach.

Title
:   List projects

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 59 tokens for its entry in `tools/list`

It takes no parameters.

Returns
:   data[] of {id,name,slug} for each active project the token reaches. open_in_rengine: /dashboard.

Examples, written as the tool name followed by its arguments:

```text
list_projects
```

### list_targets { #list_targets }

The targets this token can reach, with project and type.

Title
:   List targets

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Telegram command
:   [`/targets`](remote-control-commands.md#targets)

Context cost
:   About 123 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `contains` | <code>string &#124; null</code> | None |  | Only targets whose value contains this text. |
| `limit` | `integer` | `50` | 1 to 100 |  |

Returns
:   data{scope ('all projects' or the project name),total,targets[{value,type,project,added_at}]} ordered by value, cut at limit. open_in_rengine: /targets.

Examples, written as the tool name followed by its arguments:

```text
list_targets
list_targets contains=acme
```

### resolve_target { #resolve_target }

For each of a target's result dimensions: whether it was scanned, what the most recent covering scan found, when, and the scan id other tools take. Call this first. covered=false means not scanned, not zero.

Title
:   Resolve target

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Telegram command
:   [`/target`](remote-control-commands.md#target)

Context cost
:   About 139 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | A domain, IP address, CIDR range, URL or ASN added as a target. |

Returns
:   data.target{id,value,type,project_id}; data.surface[] one entry per dimension {dimension,label,covered,count,observed_at,scan_id,is_latest_scan,added,gone,previous}; data.risk{total,actionable,kev,suppressed,by_severity[]}; data.scans{total,running,failed,last_completed_at}; data.sensitive_services; data.monitored. open_in_rengine: /targets/<target id>. Caveats name dimensions not scanned and scans running.

Examples, written as the tool name followed by its arguments:

```text
resolve_target target=example.com
```

### scan_status { #scan_status }

Status of a scan: stages finished, running and failed, and counts found so far. Pass a scan id, a target for its most recent run, or neither for every running scan.

Title
:   Scan status

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Telegram command
:   [`/progress`](remote-control-commands.md#progress)

Context cost
:   About 205 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `scan` | <code>string &#124; null</code> | None |  | A scan id, as returned by start_scan or focused_rescan. |
| `target` | <code>string &#124; null</code> | None |  | A target, to report its most recent run. |
| `limit` | `integer` | `5` | 1 to 20 | How many runs to list when neither scan nor target is named. |

Returns
:   With scan or target: data{scan_id,status,engine,started_at,completed_at,elapsed_seconds,stages{done,running,failed,skipped},found_so_far{label:count},error}; open_in_rengine: /scans/<scan id>. With neither: data[] of {scan_id,target,engine,status,started_at,elapsed_seconds} for live scans, or the most recent runs when nothing is running; open_in_rengine: /scans.

Examples, written as the tool name followed by its arguments:

```text
scan_status
scan_status target=example.com
scan_status scan=<id>
```

### surface_brief { #surface_brief }

The curated query library, each query counted against the target's most recent covering scan and ranked by how well it discriminates. Call it before writing a query.

Title
:   Surface brief

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 198 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | The target to brief on. |
| `dimension` | `string` | `web_assets` |  | Which surface to brief on. One of: web_assets, endpoints, services, ips, vulnerabilities, secrets. |
| `include_empty` | `boolean` | `false` |  | Include queries that matched nothing. |

Returns
:   data{dimension,scan_id,total_in_scope,total_capped,leads[{query,count,capped,means,group}]} - up to 60 curated queries counted against the most recent covering scan; zero-count queries omitted unless include_empty. open_in_rengine: /scans/<scan id>?tab=<dimension tab>.

Examples, written as the tool name followed by its arguments:

```text
surface_brief target=example.com
surface_brief target=example.com dimension=vulnerabilities
```

## Interrogate

Tools that answer questions about your results: search, count and group assets, compare runs, see what changed, and check one CVE or the mail and DNS posture of a domain.

### compare_runs { #compare_runs }

Rows that appeared, changed and disappeared between two runs of one target, per result dimension. The comparability verdict states whether the runs used the same settings and did the same work. A dimension one run did not scan reports as not covered.

Title
:   Compare runs

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 270 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | <code>string &#124; null</code> | None |  | A target, to compare its two most recent full runs. |
| `current` | <code>string &#124; null</code> | None |  | The later run's scan id. Overrides target. |
| `baseline` | <code>string &#124; null</code> | None |  | The earlier run's scan id. Defaults to the run before `current`. |
| `dimension` | <code>string &#124; null</code> | None |  | List the individual changes for one dimension. |

Returns
:   data{target,baseline{scan_id,engine,started_at},current{scan_id,engine,started_at},comparability,run_setup[{what,baseline,current,material}],runs_between,dimensions[{dimension,comparability,covered,appeared,changed,disappeared,unconfirmed,unchanged,was,now}]}; with dimension: also changes[{verb,signal,asset,where,severity,fields[{field,was,now}]}] (up to 25) and changes_total. open_in_rengine: /scans/compare?current=<id>&baseline=<id>. Flagged untrusted_content.

Examples, written as the tool name followed by its arguments:

```text
compare_runs target=example.com
compare_runs target=example.com dimension=vulnerabilities
```

### cve_exposure { #cve_exposure }

Every asset in the estate that carries one CVE, across both findings dimensions, counted on one evidence ladder. Inferred: a version fell in the affected range. Observed: a check fired. Cross-checked: two signals agree. Proven: an out-of-band artifact came back. Includes the NVD, EPSS and KEV record and how long the exposure has been held.

Title
:   CVE exposure

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 256 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `cve` | `string` | Required |  | A CVE identifier, such as CVE-2021-44228. |
| `target` | <code>string &#124; null</code> | None |  | A target in reNgine. Names the project to answer for when the token reaches more than one. |
| `project_id` | <code>string &#124; null</code> | None |  | Project to answer for. Omit when the token is scoped to one. |

Returns
:   data{cve,record{known,severity,cvss_score,epss_score,epss_percentile,known_exploited,ransomware,kev_due_date,published_at},exposure{assets,targets,software_rows,finding_rows,first_seen,ladder[{evidence,count,software,findings}]},by_target[{target,assets,software,findings,first_seen}],locations[{host,ip,port,evidence,basis,dimension,state,target,first_seen}] (up to 50),locations_total}. open_in_rengine: /surface/cve/<CVE id>. Flagged untrusted_content.

Examples, written as the tool name followed by its arguments:

```text
cve_exposure cve=CVE-2021-44228
cve_exposure cve=CVE-2024-3400 target=example.com
```

### domain_posture { #domain_posture }

Sender, mail-transport and zone checks per registrable domain of a target, from its newest settled run: SPF policy and lookup count, DMARC policy and subdomain policy, DKIM selectors found, MTA-STS mode, TLS-RPT, DNSSEC and CAA. A zone failing a sender check can be forged as a sender. Checks a zone does not qualify for are absent, not passed.

Title
:   Domain posture

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 198 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | The target whose zones to report. |
| `failing_only` | `boolean` | `true` |  | List only zones with a failing check. |

Returns
:   data{target,scan_id,zones_checked,mail_hosts_checked,warning,info,clean,spoofable,checks[{check,label,tone,failing,applicable,fix}],zones[{zone,under,web_assets,spf,spf_lookups,dmarc,dmarc_subdomains,dmarc_inherited,dkim_selectors,dkim_key_bits,mail,mta_sts,tls_rpt,dnssec,caa,failing[],evidence{}}] (up to 25)}. open_in_rengine: /targets/<target id>. Flagged untrusted_content. Errors when posture was never checked.

Examples, written as the tool name followed by its arguments:

```text
domain_posture target=example.com
```

### group_assets { #group_assets }

Count a target's surface by a group key: technology, status, ASN, country, severity, service class. Each group carries the query that isolates it.

Title
:   Group assets

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 245 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | The target to aggregate. |
| `dimension` | `string` | `web_assets` |  | Which surface to aggregate. One of: web_assets, endpoints, services, ips, vulnerabilities, secrets. |
| `group_by` | `string` | Required |  | The grouping key, for example tech, status, asn, country or severity. describe_query_language lists the keys per dimension. |
| `query` | <code>string &#124; null</code> | None |  | Optional query to aggregate within. |

Returns
:   data{dimension,group_by,rows_in_scope,rows_with_a_value,total_groups,groups[{value,count,query}]} - largest 40 groups. open_in_rengine: /scans/<scan id>?tab=<tab>&q=<query>. Flagged untrusted_content.

Examples, written as the tool name followed by its arguments:

```text
group_assets target=example.com group_by=tech
group_assets target=example.com dimension=vulnerabilities group_by=severity
```

### query_assets { #query_assets }

Search one dimension of the attack surface with the query language, on one target or across every target in the project. Returns matching rows and a total equal to the rows the returned link opens. Rows carry a subset of columns.

Title
:   Query assets

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 368 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | <code>string &#124; null</code> | None |  | The target to search within. Omit to search every target in the project. |
| `dimension` | `string` | `web_assets` |  | Which surface to search. One of: web_assets, endpoints, services, ips, vulnerabilities, secrets. |
| `query` | <code>string &#124; null</code> | None |  | A query, for example `is:live and not is:cdn`, `severity:critical or is:kev`, `port:22 and is:sensitive`. describe_query_language lists the fields per dimension. Omit to return everything in scope. |
| `limit` | `integer` | `20` | 1 to 40 | Rows to return. |
| `offset` | `integer` | `0` | 0 to | Rows to skip. |
| `project_id` | <code>string &#124; null</code> | None |  | Project to search. Omit when the token is scoped to one. |

Returns
:   data{dimension,query,total,total_capped,returned,offset,rows[]} - rows carry a subset of columns for the dimension. open_in_rengine: /scans/<scan id>?tab=<tab>&q=<query> when a target is named, else /surface/<tab>?q=<query>. Flagged untrusted_content when rows are returned.

Examples, written as the tool name followed by its arguments:

```text
query_assets target=example.com query='is:live and status:200'
query_assets target=example.com dimension=vulnerabilities query='is:kev'
query_assets dimension=vulnerabilities query='severity:critical'
```

### what_changed { #what_changed }

New web assets, services, endpoints, addresses and findings per target over a window, plus targets not scanned or stale. Counts items first reported in the window against an earlier baseline. A target's first scan reports nothing as new.

Title
:   What changed

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Telegram command
:   [`/changes`](remote-control-commands.md#changes)

Context cost
:   About 182 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `window` | `string` | `7d` |  | How far back to look. One of: 7d, 14d, 30d. |
| `project_id` | <code>string &#124; null</code> | None |  | Project to report on. Omit when the token is scoped to one. |

Returns
:   data{window,generated_at,targets{total,scanned,never_scanned,stale,monitored},risk,changes[{target,type,runs,last_scan_at,last_status,new{},first_time_covered[],web_assets_gone}]} - up to 30 targets. open_in_rengine: /dashboard.

Examples, written as the tool name followed by its arguments:

```text
what_changed window=7d
```

## Explain

Tools that explain one finding in full, or what the scanner did in a run.

### explain_finding { #explain_finding }

One finding in full: what the check tests for, impact, remediation, CVE, CWE, CVSS, EPSS and KEV signals, every location on the target, and the triage decision with its reason.

Title
:   Explain finding

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 179 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | The target the finding was reported on. |
| `finding` | `string` | Required |  | A template id, check name, CVE or finding fingerprint, as returned by query_assets in template_id, template_name, cve_ids or fingerprint. |

Returns
:   data{check{template_id,name,severity,scanner,description,impact,remediation,references,tags},risk{cve_ids,cwe_ids,cvss_score,epss_score,epss_percentile,known_exploited},review{state,reason},occurrences,set_aside,locations[{matched_at,host,ip,port,state,is_new}] (up to 25),evidence{matched_at,extracted,curl}}. open_in_rengine: /scans/<scan id>?tab=vulnerabilities&q=template="<id>". Flagged untrusted_content.

Examples, written as the tool name followed by its arguments:

```text
explain_finding target=example.com finding=CVE-2021-44228
explain_finding target=example.com finding=apache-detect
```

### scan_coverage { #scan_coverage }

The scanner's account of a run: checks selected and loaded, hosts scanned, requests sent, errors and hosts abandoned. A null count means the scanner did not report that number.

Title
:   Scan coverage

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `readOnlyHint`

Context cost
:   About 163 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | The target to report coverage for. |
| `dimension` | `string` | `vulnerabilities` |  | Which run to account for. One of: vulnerabilities, endpoints. |

Returns
:   data{dimension,scan_id,runs[coverage rows with empty values dropped],surface[{dimension,covered,count}]}. open_in_rengine: /scans/<scan id>?tab=<tab>.

Examples, written as the tool name followed by its arguments:

```text
scan_coverage target=example.com
```

## Act

Tools that act: plan a scan, add, update or delete targets, record triage decisions, and start, pause, resume or cancel scans and focused rescans.

### plan_scan { #plan_scan }

Resolve what a scan would do: stages and their order, skipped stages and the reason, footprint and estimated duration. Nothing runs and the target is not contacted.

Title
:   Plan a scan

Capability
:   `plan`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Nothing runs and the target is not contacted.

Context cost
:   About 300 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | A target value. It does not have to exist yet. |
| `engine_id` | <code>string &#124; null</code> | None |  | A saved scan engine to plan with. Omit for an ad hoc plan. |
| `stages` | `array<string>` | `[]` | At most 20 items | Capability stages to enable for an ad hoc plan, for example subdomain_discovery, port_scan, url_discovery, vulnerability_scan. |
| `intensity` | <code>string &#124; null</code> | None |  | One of: passive, normal, aggressive. |
| `project_id` | <code>string &#124; null</code> | None |  | Project to act in. Omit when the token is scoped to one. |

Returns
:   data{target,target_type,engine,context,summary,phases[{phase,stages[{stage,label,status,reason}]}],warnings}. Caveat 'Nothing ran.' No open_in_rengine link.

Examples, written as the tool name followed by its arguments:

```text
plan_scan target=example.com stages=['subdomain_discovery','vulnerability_scan']
```

### add_target { #add_target }

Add targets to a project. Records each target and queues WHOIS, DNS and routing enrichment. Runs no scan. An existing value is reused.

Title
:   Add targets

Capability
:   `write`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No scan. Queues WHOIS, DNS and routing enrichment.

Telegram command
:   [`/add`](remote-control-commands.md#add)

Context cost
:   About 272 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `targets` | `array<string>` | Required | At most 50 items. minItems 1 | The values to add, each a domain, IP address, CIDR range, URL or ASN. Existing values are reused. |
| `project_id` | <code>string &#124; null</code> | None |  | Which project to add them to. Omit when the token is scoped to one. |
| `tags` | `array<string>` | `[]` | At most 20 items | Tags applied to the targets this call creates. Existing targets keep theirs. |
| `organizations` | `array<string>` | `[]` | At most 20 items | Organizations applied to the targets this call creates. |

Returns
:   data{project,created[{id,value,type,link}],already_present[],rejected[]}. open_in_rengine: /targets/<id> when exactly one target was created and none existed, else /targets.

Examples, written as the tool name followed by its arguments:

```text
add_target targets=['example.com']
add_target targets=['example.com','1.1.1.1'] tags=['client-a']
```

### delete_target { #delete_target }

Delete a target and everything recorded against it: scans, web assets, services, endpoints, findings and triage decisions. A call without `confirm` returns what would be deleted. Call with confirm=true after the user agrees.

Title
:   Delete a target

Capability
:   `write`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Annotations
:   `destructiveHint`

Context cost
:   About 173 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | The target to delete, by value or id. |
| `confirm` | `boolean` | `false` |  | Must be true. A call without it returns what would be deleted. |

Returns
:   Without confirm=true: a tool error (isError) whose text states what the delete would remove. With confirm=true: data{value,scans_deleted,results_deleted{label:count}}; open_in_rengine: /targets.

Examples, written as the tool name followed by its arguments:

```text
delete_target target=old.example.com confirm=true
```

### record_triage { #record_triage }

Record a review decision against a finding: confirmed, false positive or accepted risk. The decision is keyed to the fingerprint and applies to every later scan of the target. Include a reason.

Title
:   Record triage

Capability
:   `write`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Context cost
:   About 245 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | The target the finding was reported on. |
| `fingerprint` | `string` | Required |  | The finding's fingerprint, as returned by query_assets. |
| `state` | `string` | Required |  | The review decision. One of: open, confirmed, false_positive, accepted. |
| `reason` | <code>string &#124; null</code> | None | At most 20000 characters | The reason for the decision. Saved as a note on the finding. |

Returns
:   data{fingerprint,state,reason,observations_updated}. open_in_rengine: /scans/<scan id>?tab=vulnerabilities.

Examples, written as the tool name followed by its arguments:

```text
record_triage target=example.com fingerprint=<hash> state=false_positive reason='Static asset, not the admin panel.'
```

### update_target { #update_target }

Change a target's display name, tags or organizations. Tags and organizations are replaced, not merged. The target value cannot be changed.

Title
:   Update a target

Capability
:   `write`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No. Reads or writes reNgine's own database.

Context cost
:   About 251 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | The target to change, by value or id. |
| `display_name` | <code>string &#124; null</code> | None | At most 200 characters | The name shown in the UI. |
| `tags` | <code>array&lt;string&gt; &#124; null</code> | None | At most 20 items | Replaces the target's tags. Pass [] to clear them. |
| `organizations` | <code>array&lt;string&gt; &#124; null</code> | None | At most 20 items | Replaces the target's organizations. |

Returns
:   data{value,display_name,tags[],organizations[]}. open_in_rengine: /targets/<target id>.

Examples, written as the tool name followed by its arguments:

```text
update_target target=example.com tags=['client-a','production']
```

### cancel_scan { #cancel_scan }

Stop a running scan. Stages in flight are aborted. Results written so far are kept. Takes effect immediately.

Title
:   Cancel a scan

Capability
:   `launch`

Sends traffic to the target
:   <span class="rn-tag active">Active</span> No new traffic: stages in flight are aborted.

Telegram command
:   [`/cancel`](remote-control-commands.md#cancel)

Context cost
:   About 145 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `scan` | <code>string &#124; null</code> | None |  | The scan id to stop. |
| `target` | <code>string &#124; null</code> | None |  | A target, to stop whichever run of it is live. |

Returns
:   data{scan_id,status,engine,kept{label:count}}. open_in_rengine: /scans/<scan id>.

Examples, written as the tool name followed by its arguments:

```text
cancel_scan target=example.com
cancel_scan scan=<id>
```

### focused_rescan { #focused_rescan }

Re-run a set of stages against named assets as a separate scan. Sends traffic to the target. Results are recorded on the new run, not on the parent scan.

Title
:   Focused rescan

Capability
:   `launch`

Sends traffic to the target
:   <span class="rn-tag active">Active</span> Yes (caveat: 'Traffic is being sent to these assets.').

Context cost
:   About 264 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | The target the assets belong to. |
| `dimension` | `string` | Required |  | Which surface to refresh. One of: web_assets, endpoints, services, ips, vulnerabilities, secrets. |
| `assets` | `array<string>` | Required | At most 200 items. minItems 1 | The assets to rescan: hostnames for web assets and endpoints, IP addresses for services and addresses. Take them from query_assets. |
| `stages` | `array<string>` | `[]` | At most 20 items | Stages to run. Omit to use the dimension's defaults. |

Returns
:   data{scan_id,parent_scan_id,dimension,assets (count),stages,status}. open_in_rengine: /scans/<new scan id>.

Examples, written as the tool name followed by its arguments:

```text
focused_rescan target=example.com dimension=web_assets assets=['a.example.com','b.example.com']
```

### pause_scan { #pause_scan }

Pause a running scan. Stages in flight stop and run again from the start when the scan resumes. Results written so far are kept.

Title
:   Pause a scan

Capability
:   `launch`

Sends traffic to the target
:   <span class="rn-tag active">Active</span> No new traffic: stages in flight stop.

Telegram command
:   [`/pause`](remote-control-commands.md#pause)

Context cost
:   About 147 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `scan` | <code>string &#124; null</code> | None |  | The scan id to pause. |
| `target` | <code>string &#124; null</code> | None |  | A target, to pause its running scan. |

Returns
:   data{scan_id,status,engine,kept{label:count}}. open_in_rengine: /scans/<scan id>.

Examples, written as the tool name followed by its arguments:

```text
pause_scan target=example.com
pause_scan scan=<id>
```

### resume_scan { #resume_scan }

Resume a paused scan. It restarts at its first unfinished stage. Stages that already succeeded are not run again.

Title
:   Resume a scan

Capability
:   `launch`

Sends traffic to the target
:   <span class="rn-tag active">Active</span> Yes: the paused run restarts at its first unfinished stage.

Telegram command
:   [`/resume`](remote-control-commands.md#resume)

Context cost
:   About 144 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `scan` | <code>string &#124; null</code> | None |  | The scan id to resume. |
| `target` | <code>string &#124; null</code> | None |  | A target, to resume its paused run. |

Returns
:   data{scan_id,status,engine}. open_in_rengine: /scans/<scan id>.

Examples, written as the tool name followed by its arguments:

```text
resume_scan target=example.com
resume_scan scan=<id>
```

### start_scan { #start_scan }

Start a scan against a target in this token's project. Sends traffic to the target. Returns a scan id and a link. The scan runs in the background. Poll scan_status for progress.

Title
:   Start a scan

Capability
:   `launch`

Sends traffic to the target
:   <span class="rn-tag active">Active</span> Yes, unless the resolved intensity is passive (caveat: 'Passive intensity. No traffic reaches the target.').

Telegram command
:   [`/scan`](remote-control-commands.md#scan)

Context cost
:   About 335 tokens for its entry in `tools/list`

You can pass these parameters.

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `target` | `string` | Required |  | The target to scan. A value not yet in the project is added when the token holds the write capability. |
| `engine_id` | <code>string &#124; null</code> | None |  | A saved scan engine. Omit for an ad hoc plan. |
| `stages` | `array<string>` | `[]` | At most 20 items | Capability stages to enable when no engine is named. |
| `intensity` | <code>string &#124; null</code> | None |  | One of: passive, normal, aggressive. |
| `context_id` | <code>string &#124; null</code> | None |  | A saved scan context for auth, scope and rate. |
| `project_id` | <code>string &#124; null</code> | None |  | Project to act in. Omit when the token is scoped to one. |

Returns
:   data{scan_id,status,engine,target,target_id,started_at}. open_in_rengine: /scans/<scan id>. Caveats state whether traffic is sent, and name the agent token.

Examples, written as the tool name followed by its arguments:

```text
start_scan target=example.com stages=['subdomain_discovery']
```

