---
title: Vulnerabilities
description: "Everything you can search, group and sort in the vulnerabilities dimension, with example queries. Keep this page open while you write a query on findings."
sources:
  - shared/definitions/asset_query.py
  - tools/nuclei/parser.py
  - shared/services/vuln_inventory.py
  - shared/services/surface_query/vulnerabilities.py
  - api/app/services/vulnerability.py
  - frontend/src/lib/components/scans/results/vulnerabilities-table.svelte
revised: 2026-10-03
generated: scripts/gen_query.py
layout: reference
nav_order: 4
---

This page is generated from the reNgine 3.0 source. `scripts/gen_query.py` writes it from `data/query-schema.json`, `data/openapi.json` and `data/mcp-dimensions.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Each row in the Vulnerabilities dimension is one finding: one check that fired at one location in one scan (a vulnerabilities row, unique per scan and fingerprint). You search these rows in the query bar of the table, in the HTTP API with `POST /api/v1/vulnerabilities/search` and from an MCP client with the tool `query_assets`. For the syntax that works in every dimension, see [Query language](index.md).

## About this dimension

The basics: what a row is, which stages fill the dimension, and where you search it.

| Property | Value |
|---|---|
| One row is | One finding: one check that fired at one location in one scan (a vulnerabilities row, unique per scan and fingerprint). |
| Singular and plural | finding, findings |
| Identified by | <code>fingerprint = sha256(scanner&#124;template_id&#124;matcher&#124;matched_at)</code> |
| Stages that add rows | [`broken_links`](../stages/broken_links.md), [`dast_scan`](../stages/dast_scan.md), [`name_ownership`](../stages/name_ownership.md), [`origin_probe`](../stages/origin_probe.md), [`takeover`](../stages/takeover.md), [`vulnerability_scan`](../stages/vulnerability_scan.md), [`zone_transfer`](../stages/zone_transfer.md) |
| Stages that cover it | [`dast_scan`](../stages/dast_scan.md), [`vulnerability_scan`](../stages/vulnerability_scan.md) |
| Free-text fields | `name`, `template`, `extracted`, `cve`, `host`, `location` |
| Flag prefixes | `is:`, `has:` |
| Search API | `POST /api/v1/vulnerabilities/search` |
| Query bar placeholder | `severity:critical and not is:cdn`{ .rn-q } |

Coverage tells you whether an empty table means that nothing was found or that nothing was looked for. A dimension is covered for a target when a covering stage succeeded in a run, or when a run wrote rows to it. Without coverage, the dimension reads **Not scanned**, which is not the same as zero rows.

## Fields

Fields are the properties you search on, written `field:value`. An alias works the same as the field name. Select a field to see its operators, its values and an example.

| Field | Aliases | Type | Group | Description |
|---|---|---|---|---|
| [`target`](#f-target) | `scope` | string | Scope | Target this finding belongs to. |
| [`name`](#f-name) | `title` | string | Finding | Title of the check that fired. |
| [`template`](#f-template) | `check`, `rule`, `id` | string | Finding | Identifier of the check that fired. |
| [`severity`](#f-severity) | `sev` | enum | Finding | Severity the check declares. |
| [`type`](#f-type) | `protocol` | enum | Finding | Protocol the check speaks. |
| [`scanner`](#f-scanner) |  | enum | Finding | Tool that produced the finding. |
| [`tag`](#f-tag) | `tags` | string | Finding | Tag carried by the check. |
| [`matcher`](#f-matcher) |  | string | Finding | Named matcher inside the check that fired. |
| [`extracted`](#f-extracted) |  | string | Finding | Value the check pulled out of the response. |
| [`author`](#f-author) |  | string | Finding | Author of the check. |
| [`exploit`](#f-exploit) | `rank` | number | Classification | Exploitation rank, 0-100, from the signals behind the finding. |
| [`poc`](#f-poc) | `exploits` | number | Classification | Number of published proof-of-concept exploits. |
| [`signal`](#f-signal) |  | enum | Classification | Exploitation signal carried by the finding. |
| [`cve`](#f-cve) |  | string | Classification | Published vulnerability identifier. |
| [`cwe`](#f-cwe) |  | string | Classification | Weakness class. |
| [`cvss`](#f-cvss) |  | number | Classification | CVSS base score. |
| [`epss`](#f-epss) |  | number | Classification | Probability of exploitation in the next 30 days, 0 to 1. |
| [`host`](#f-host) | `name.host`, `subdomain` | string | Asset | Hostname the finding sits on. |
| [`location`](#f-location) | `matched`, `url`, `path` | string | Asset | Exact place the check matched. |
| [`ip`](#f-ip) | `address`, `addr` | ip | Asset | Address behind the finding. Accepts a CIDR range. |
| [`port`](#f-port) |  | number | Asset | Port the finding is on. |
| [`status`](#f-status) |  | number | Asset | HTTP status the asset returned. |
| [`tech`](#f-tech) |  | string | Asset | Technology fingerprinted on the asset. |
| [`asn`](#f-asn) |  | number | Asset | Autonomous system announcing the address. |
| [`country`](#f-country) |  | enum | Asset | Two-letter country of the address. |
| [`state`](#f-state) |  | enum | Review | Review decision recorded for this finding. |
| [`ticket`](#f-ticket) |  | enum | Review | Tracker status of the issue filed for this finding. |
| [`evidence`](#f-evidence) |  | enum | Finding | How the finding was established: observed, cross-checked or proven. |
| [`seen`](#f-seen) | `discovered`, `age` | date | Review | When the finding was recorded. |
| [`is`](#f-is) | `has` | flag | Flags | Property of the finding. |

## Flags

Flags are yes-or-no properties of a row. Write them with `is:` or `has:`, for example `is:new`{ .rn-q }.

| Flag | Description |
|---|---|
| [`is:new`](#is-new) | Not reported by an earlier scan of this target |
| [`is:kev`](#is-kev) | Listed in CISA KEV |
| [`is:ransomware`](#is-ransomware) | Listed in CISA ransomware campaigns |
| [`is:overdue`](#is-overdue) | Past the CISA remediation deadline |
| [`is:weaponised`](#is-weaponised) | A public exploit is published |
| [`is:untestable`](#is-untestable) | No scanner template covers this CVE |
| [`is:cve`](#is-cve) | Carries a published vulnerability identifier |
| [`is:exploitable`](#is-exploitable) | Known exploited, or above the EPSS threshold |
| [`is:cross-checked`](#is-cross-checked) | A second signal at the same location names the same CVE or weakness class |
| [`is:proven`](#is-proven) | The asset produced an out-of-band interaction |
| [`is:recorded`](#is-recorded) | The request and response that produced it were stored |
| [`is:extracted`](#is-extracted) | The check pulled a value out of the response |
| [`is:web`](#is-web) | Found on an HTTP asset |
| [`is:cdn`](#is-cdn) | On an asset served through a CDN |
| [`is:triaged`](#is-triaged) | Reviewed |
| [`is:open`](#is-open) | Not reviewed |
| [`is:suppressed`](#is-suppressed) | Reviewed and set aside as a false positive or accepted risk |
| [`is:ticketed`](#is-ticketed) | Linked to an issue |

## Group keys

Group the rows by one of these keys to count how many rows share each value. Use the **Group by** menu of the table, or the `groups` search operation of the HTTP API.

| Key | Label | Groups |
|---|---|---|
| `severity` | Severity | Findings of the same severity |
| `template` | Check | The same weakness across every asset it was found on |
| `tag` | Category | Findings the checks categorise the same way |
| `cve` | CVE | Findings sharing a published identifier |
| `evidence` | Evidence | Findings with the same evidence |
| `state` | Review state | Findings at the same point in review |
| `scanner` | Scanner | Findings from the same tool |
| `type` | Protocol | Findings on the same protocol |
| `host` | Web asset | Everything found on one hostname |
| `location` | Location | Every check that fired at the same place |
| `port` | Port | Findings on the same port |
| `target` | Target | Rows belonging to the same target |

## Sort

The keys you can sort by, and the order you get when you do not choose one.

| Property | Value |
|---|---|
| Sort keys | `risk`, `severity`, `name`, `template`, `host`, `seen`, `cvss`, `epss`, `exploit`, `type` |
| API default | `risk` desc |
| Interface default | `risk` desc |
| Tie-break | Template_id asc, matched_at asc, id asc. NULLs last. |

## Columns

The table always starts with its leading columns. An export of this dimension writes the export columns.

| Set | Columns |
|---|---|
| Leading columns | **Finding**, **Location** |
| Optional columns |  |
| Shown by default |  |
| Export columns | `fingerprint`, `template_id`, `template_name`, `severity`, `scanner`, `matched_at`, `host`, `ip`, `port`, `cve_ids`, `cvss_score`, `epss_score`, `is_kev`, `state`, `is_new`, `tags` |

## Examples

Start from one of these queries and adjust it to your target.

### Priority

| Query | Finds |
|---|---|
| `is:kev`{ .rn-q } | Weaknesses with confirmed exploitation in the wild |
| `severity:critical`{ .rn-q } | Findings rated critical |
| `is:cross-checked`{ .rn-q } | Findings a second check confirms at the same location |
| `is:cross-checked and severity:[critical,high]`{ .rn-q } | Severe findings that more than one check agrees on |
| `evidence:proven`{ .rn-q } | Findings the asset answered with an out-of-band callback |
| `is:exploitable and not is:suppressed`{ .rn-q } | Exploited or likely to be, and not suppressed |
| `severity:[critical,high] and not is:cdn`{ .rn-q } | Severe findings on origin infrastructure |
| `cvss>=9`{ .rn-q } | Findings scored 9.0 or above |

### Change

| Query | Finds |
|---|---|
| `is:new`{ .rn-q } | Findings absent from every earlier scan of this target |
| `is:new and severity:[critical,high]`{ .rn-q } | Severe findings absent from every earlier scan |
| `seen:<24h and is:cve`{ .rn-q } | Published vulnerabilities recorded in the last day |

### Access control

| Query | Finds |
|---|---|
| `tag:default-login`{ .rn-q } | Default credentials accepted |
| `tag:panel and severity:[critical,high,medium]`{ .rn-q } | Administrative interfaces reachable from the internet |
| `tag:[unauth,auth-bypass]`{ .rn-q } | Protected functionality reachable without credentials |

### Data exposure

| Query | Finds |
|---|---|
| `tag:[exposure,disclosure]`{ .rn-q } | Files and data disclosed over HTTP |
| `tag:[backup,config,files]`{ .rn-q } | Source, configuration and backups reachable over HTTP |
| `is:extracted`{ .rn-q } | Findings that pulled a concrete value out of the response |

### Infrastructure

| Query | Finds |
|---|---|
| `tag:takeover`{ .rn-q } | Hostnames pointing at claimable third-party infrastructure |
| `type:ssl`{ .rn-q } | Transport security defects |
| `type:[network,dns]`{ .rn-q } | Findings outside the web surface |
| `tag:misconfig`{ .rn-q } | Misconfigured services |

### Review

| Query | Finds |
|---|---|
| `is:open and severity:[critical,high]`{ .rn-q } | Severe findings not reviewed |
| `state:false_positive`{ .rn-q } | Findings a reviewer rejected |
| `is:triaged`{ .rn-q } | Findings with a review decision |
| `ticket:done`{ .rn-q } | Findings whose issue is done |

## Field reference

Each field in detail: its type, the operators it accepts, its values and an example.

### target { #f-target }

Target this finding belongs to.

Type
:   `string`

Group
:   Scope

Aliases
:   `scope`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `target:acme.com`{ .rn-q }

### name { #f-name }

Title of the check that fired.

Type
:   `string`

Group
:   Finding

Aliases
:   `title`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `name:log4j`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### template { #f-template }

Identifier of the check that fired.

Type
:   `string`

Group
:   Finding

Aliases
:   `check`, `rule`, `id`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `template:CVE-2021-44228`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### severity { #f-severity }

Severity the check declares.

Type
:   `enum`

Group
:   Finding

Aliases
:   `sev`

Operators
:   `:` `=` `!=`

Values
:   `critical`, `high`, `medium`, `low`, `info`, `unknown`

Example
:   `severity:[critical,high]`{ .rn-q }

Matching
:   Values are matched as substrings.

### type { #f-type }

Protocol the check speaks.

Type
:   `enum`

Group
:   Finding

Aliases
:   `protocol`

Operators
:   `:` `=` `!=`

Values
:   `http`, `network`, `dns`, `ssl`, `file`, `headless`, `javascript`, `websocket`, `whois`, `other`

Example
:   `type:ssl`{ .rn-q }

Matching
:   Values are matched as substrings.

### scanner { #f-scanner }

Tool that produced the finding.

Type
:   `enum`

Group
:   Finding

Operators
:   `:` `=` `!=`

Values
:   `nuclei`, `dalfox`, `rengine`, `manual`

Example
:   `scanner:nuclei`{ .rn-q }

Matching
:   Values are matched as substrings.

### tag { #f-tag }

Tag carried by the check.

Type
:   `string`

Group
:   Finding

Aliases
:   `tags`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `tag:takeover`{ .rn-q }

### matcher { #f-matcher }

Named matcher inside the check that fired.

Type
:   `string`

Group
:   Finding

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `matcher:unauthenticated`{ .rn-q }

### extracted { #f-extracted }

Value the check pulled out of the response.

Type
:   `string`

Group
:   Finding

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `extracted:admin`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Matches the extracted values as text.

### author { #f-author }

Author of the check.

Type
:   `string`

Group
:   Finding

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `author:pdteam`{ .rn-q }

### exploit { #f-exploit }

Exploitation rank, 0-100, from the signals behind the finding.

Type
:   `number`

Group
:   Classification

Aliases
:   `rank`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `exploit:>=80`{ .rn-q }

### poc { #f-poc }

Number of published proof-of-concept exploits.

Type
:   `number`

Group
:   Classification

Aliases
:   `exploits`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `poc:>0`{ .rn-q }

### signal { #f-signal }

Exploitation signal carried by the finding.

Type
:   `enum`

Group
:   Classification

Operators
:   `:` `=` `!=`

Values
:   `kev`, `ransom_path`, `ransomware`, `fresh_exploit`, `overdue`, `weaponised`, `likely`, `reachable`, `bypassed`, `crowd`, `untestable`

Example
:   `signal:ransom_path`{ .rn-q }

### cve { #f-cve }

Published vulnerability identifier.

Type
:   `string`

Group
:   Classification

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cve:CVE-2021-44228`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### cwe { #f-cwe }

Weakness class.

Type
:   `string`

Group
:   Classification

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cwe:CWE-89`{ .rn-q }

### cvss { #f-cvss }

CVSS base score.

Type
:   `number`

Group
:   Classification

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `cvss>=9`{ .rn-q }

Matching
:   Decimal value.

### epss { #f-epss }

Probability of exploitation in the next 30 days, 0 to 1.

Type
:   `number`

Group
:   Classification

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `epss>=0.5`{ .rn-q }

Matching
:   Decimal 0 to 1.

### host { #f-host }

Hostname the finding sits on.

Type
:   `string`

Group
:   Asset

Aliases
:   `name.host`, `subdomain`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `host:api`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### location { #f-location }

Exact place the check matched.

Type
:   `string`

Group
:   Asset

Aliases
:   `matched`, `url`, `path`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `location:/actuator`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### ip { #f-ip }

Address behind the finding. Accepts a CIDR range.

Type
:   `ip`

Group
:   Asset

Aliases
:   `address`, `addr`

Operators
:   `:` `=` `!=`

Example
:   `ip:104.16.0.0/12`{ .rn-q }

### port { #f-port }

Port the finding is on.

Type
:   `number`

Group
:   Asset

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `port:8080`{ .rn-q }

### status { #f-status }

HTTP status the asset returned.

Type
:   `number`

Group
:   Asset

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `status:200`{ .rn-q }

Matching
:   HTTP status of the asset the finding sits on.

### tech { #f-tech }

Technology fingerprinted on the asset.

Type
:   `string`

Group
:   Asset

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `tech:nginx`{ .rn-q }

Matching
:   Technology on the finding's HTTP asset or host.

### asn { #f-asn }

Autonomous system announcing the address.

Type
:   `number`

Group
:   Asset

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `asn:13335`{ .rn-q }

### country { #f-country }

Two-letter country of the address.

Type
:   `enum`

Group
:   Asset

Operators
:   `:` `=` `!=`

Example
:   `country:DE`{ .rn-q }

### state { #f-state }

Review decision recorded for this finding.

Type
:   `enum`

Group
:   Review

Operators
:   `:` `=` `!=`

Values
:   `open`, `confirmed`, `false_positive`, `accepted`

Example
:   `state:false_positive`{ .rn-q }

Matching
:   '-' and spaces are read as '_'. Defaults to open when nobody has decided.

### ticket { #f-ticket }

Tracker status of the issue filed for this finding.

Type
:   `enum`

Group
:   Review

Operators
:   `:` `=` `!=`

Values
:   `todo`, `in_progress`, `done`

Example
:   `ticket:done`{ .rn-q }

Matching
:   '-' and spaces are read as '_'. Matches findings held by a filed tracker issue in that category.

### evidence { #f-evidence }

How the finding was established: observed, cross-checked or proven.

Type
:   `enum`

Group
:   Finding

Operators
:   `:` `=` `!=`

Values
:   `observed`, `cross-checked`, `proven`

Example
:   `evidence:cross-checked`{ .rn-q }

Matching
:   Proven, corroborated (and not proven), observed (and not corroborated).

### seen { #f-seen }

When the finding was recorded.

Type
:   `date`

Group
:   Review

Aliases
:   `discovered`, `age`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `seen:<24h`{ .rn-q }

Matching
:   A relative age counts back from now.

### is { #f-is }

Property of the finding.

Type
:   `flag`

Group
:   Flags

Aliases
:   `has`

Operators
:   `:`

Values
:   [`new`](#is-new), [`kev`](#is-kev), [`ransomware`](#is-ransomware), [`overdue`](#is-overdue), [`weaponised`](#is-weaponised), [`untestable`](#is-untestable), [`cve`](#is-cve), [`exploitable`](#is-exploitable), [`cross-checked`](#is-cross-checked), [`proven`](#is-proven), [`recorded`](#is-recorded), [`extracted`](#is-extracted), [`web`](#is-web), [`cdn`](#is-cdn), [`triaged`](#is-triaged), [`open`](#is-open), [`suppressed`](#is-suppressed), [`ticketed`](#is-ticketed)

Example
:   `is:kev`{ .rn-q }

## Flag reference

Each flag in detail, with the rule a row must meet to match it.

### is:new { #is-new }

Not reported by an earlier scan of this target.

Written as
:   `is:new`, `has:new`

Matches when
:   An earlier scan of the target recorded at least one finding, and none had this fingerprint.

### is:kev { #is-kev }

Listed in CISA KEV.

Written as
:   `is:kev`, `has:kev`

Matches when
:   Is_kev is true.

### is:ransomware { #is-ransomware }

Listed in CISA ransomware campaigns.

Written as
:   `is:ransomware`, `has:ransomware`

Matches when
:   Kev_ransomware is true.

### is:overdue { #is-overdue }

Past the CISA remediation deadline.

Written as
:   `is:overdue`, `has:overdue`

Matches when
:   Kev_due_date is before today.

### is:weaponised { #is-weaponised }

A public exploit is published.

Written as
:   `is:weaponised`, `has:weaponised`

Matches when
:   Poc_count above 0.

### is:untestable { #is-untestable }

No scanner template covers this CVE.

Written as
:   `is:untestable`, `has:untestable`

Matches when
:   Template_available is false.

### is:cve { #is-cve }

Carries a published vulnerability identifier.

Written as
:   `is:cve`, `has:cve`

Matches when
:   At least one CVE id.

### is:exploitable { #is-exploitable }

Known exploited, or above the EPSS threshold.

Written as
:   `is:exploitable`, `has:exploitable`

Matches when
:   KEV-listed, or EPSS at or above 0.5.

### is:cross-checked { #is-cross-checked }

A second signal at the same location names the same CVE or weakness class.

Written as
:   `is:cross-checked`, `has:cross-checked`

### is:proven { #is-proven }

The asset produced an out-of-band interaction.

Written as
:   `is:proven`, `has:proven`

Matches when
:   Evidence is proven (an out-of-band interaction was recorded)

### is:recorded { #is-recorded }

The request and response that produced it were stored.

Written as
:   `is:recorded`, `has:recorded`

Matches when
:   Request and response are both stored.

### is:extracted { #is-extracted }

The check pulled a value out of the response.

Written as
:   `is:extracted`, `has:extracted`

Matches when
:   Extracted_results is not empty.

### is:web { #is-web }

Found on an HTTP asset.

Written as
:   `is:web`, `has:web`

Matches when
:   Bound to an HTTP asset.

### is:cdn { #is-cdn }

On an asset served through a CDN.

Written as
:   `is:cdn`, `has:cdn`

Matches when
:   Its HTTP asset is CDN-fronted.

### is:triaged { #is-triaged }

Reviewed.

Written as
:   `is:triaged`, `has:triaged`

Matches when
:   Review state is not open.

### is:open { #is-open }

Not reviewed.

Written as
:   `is:open`, `has:open`

Matches when
:   Review state is open.

### is:suppressed { #is-suppressed }

Reviewed and set aside as a false positive or accepted risk.

Written as
:   `is:suppressed`, `has:suppressed`

Matches when
:   Review state is false_positive or accepted.

### is:ticketed { #is-ticketed }

Linked to an issue.

Written as
:   `is:ticketed`, `has:ticketed`

Matches when
:   Held by a tracker issue in a ticketed state.

