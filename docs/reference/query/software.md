---
title: Software
description: "Everything you can search and sort in the software dimension, with example queries. Keep this page open while you write a query on software CVEs."
sources:
  - shared/definitions/asset_query.py
  - shared/services/software_match.py
  - shared/services/surface_query/software.py
  - frontend/src/lib/components/scans/results/software-table.svelte
revised: 2026-10-03
generated: scripts/gen_query.py
layout: reference
nav_order: 5
---

This page is generated from the reNgine 3.0 source. `scripts/gen_query.py` writes it from `data/query-schema.json`, `data/openapi.json` and `data/mcp-dimensions.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Each row in the Software dimension is one software CVE: one published CVE inferred for one software name and version on one asset in one scan (a software_cves row). You search these rows in the query bar of the table and in the HTTP API with `POST /api/v1/software/search`. For the syntax that works in every dimension, see [Query language](index.md).

## About this dimension

The basics: what a row is, which stages fill the dimension, and where you search it.

| Property | Value |
|---|---|
| One row is | One software CVE: one published CVE inferred for one software name and version on one asset in one scan (a software_cves row). |
| Singular and plural | software CVE, software CVEs |
| Identified by | <code>fingerprint = md5(host or ip&#124;port&#124;vendor&#124;product&#124;version&#124;cve)</code> |
| Stages that add rows | [`http_probe`](../stages/http_probe.md), [`passive_ports`](../stages/passive_ports.md), [`port_scan`](../stages/port_scan.md) |
| Stages that cover it | [`http_probe`](../stages/http_probe.md), [`port_scan`](../stages/port_scan.md) |
| Free-text fields | `cve`, `software`, `host` |
| Flag prefixes | `is:`, `has:` |
| Search API | `POST /api/v1/software/search` |
| Query bar placeholder | `severity:critical and is:stated`{ .rn-q } |

Coverage tells you whether an empty table means that nothing was found or that nothing was looked for. A dimension is covered for a target when a covering stage succeeded in a run, or when a run wrote rows to it. Without coverage, the dimension reads **Not scanned**, which is not the same as zero rows.

## Fields

Fields are the properties you search on, written `field:value`. An alias works the same as the field name. Select a field to see its operators, its values and an example.

| Field | Aliases | Type | Group | Description |
|---|---|---|---|---|
| [`cve`](#f-cve) |  | string | Vulnerability | Published identifier of the weakness. |
| [`software`](#f-software) | `name` | string | Software | Name of the software as the scan read it. |
| [`product`](#f-product) |  | string | Software | Product as NVD files it. |
| [`vendor`](#f-vendor) |  | string | Software | Vendor as NVD files it. |
| [`version`](#f-version) |  | string | Software | Version the asset reported. |
| [`source`](#f-source) |  | enum | Software | Source of the reported version. |
| [`severity`](#f-severity) |  | enum | Vulnerability | Severity NVD scored the CVE at. |
| [`cvss`](#f-cvss) |  | number | Vulnerability | CVSS base score. |
| [`epss`](#f-epss) |  | number | Vulnerability | Probability of exploitation in the next 30 days. |
| [`rank`](#f-rank) |  | number | Vulnerability | Exploitation rank built from the intelligence signals. |
| [`confidence`](#f-confidence) |  | enum | Confidence | Verification level of the match. |
| [`caveat`](#f-caveat) |  | enum | Confidence | A part of the match that is not verified. |
| [`evidence`](#f-evidence) |  | enum | Confidence | Inferred from the version alone, or corroborated by a check at the same host. |
| [`target`](#f-target) |  | string | Asset | Target the asset belongs to. |
| [`host`](#f-host) |  | string | Asset | Hostname running the software. |
| [`ip`](#f-ip) |  | ip | Asset | Address running the software. |
| [`port`](#f-port) |  | number | Asset | Port the software answers on. |
| [`seen`](#f-seen) | `discovered`, `age` | date | Asset | When the CVE was inferred. |
| [`is`](#f-is) | `has` | flag | Flags | Property of the match. |

## Flags

Flags are yes-or-no properties of a row. Write them with `is:` or `has:`, for example `is:new`{ .rn-q }.

| Flag | Description |
|---|---|
| [`is:new`](#is-new) | Not inferred by an earlier scan of this target |
| [`is:kev`](#is-kev) | Listed in CISA KEV |
| [`is:ransomware`](#is-ransomware) | Listed in CISA ransomware campaigns |
| [`is:overdue`](#is-overdue) | Past the CISA remediation deadline |
| [`is:likely`](#is-likely) | EPSS score of 0.088 or above |
| [`is:firm`](#is-firm) | Every part of the match is verified |
| [`is:conditional`](#is-conditional) | NVD names a further component not identified on the asset |
| [`is:backport`](#is-backport) | A distribution build. Fixes may land without a version change |
| [`is:fingerprinted`](#is-fingerprinted) | Version read from the page body |
| [`is:stated`](#is-stated) | Version stated in a server header |
| [`is:web`](#is-web) | Inferred from a web asset |
| [`is:service`](#is-service) | Inferred from a service banner |
| [`is:corroborated`](#is-corroborated) | A check at the same host names the same CVE |
| [`is:fixable`](#is-fixable) | A newer release on the same target is not affected |

## Group keys

These group keys are defined for software CVEs. The table of this dimension has no group menu, and the HTTP API has no `groups` operation for it.

| Key | Label | Groups |
|---|---|---|
| `target` | Target | Rows belonging to the same target |
| `cve` | CVE | Every asset affected by one published CVE |
| `product` | Product | Everything running the same software |
| `version` | Version | Everything running the same release |
| `host` | Host | Everything inferred on one hostname |
| `severity` | Severity | Matches of the same severity |
| `confidence` | Confidence | Matches with the same amount verified |
| `evidence` | Evidence | Matches with the same evidence |

## Sort

The keys you can sort by, and the order you get when you do not choose one.

| Property | Value |
|---|---|
| Sort keys | `rank`, `cvss`, `epss`, `cve`, `software`, `host`, `seen` |
| API default | `None` |
| Interface default | `rank` |
| Tie-break | Cve, id. |

## Columns

The table always starts with its leading columns. You choose which optional columns to show. An export of this dimension writes the export columns.

| Set | Columns |
|---|---|
| Leading columns | **CVE**, **Software** |
| Optional columns | **Asset**, **Severity**, **Exploitation**, **Evidence**, **Confidence**, **Seen** |
| Shown by default | **Asset**, **Severity**, **Exploitation**, **Evidence**, **Confidence** |
| Export columns | `cve`, `name`, `version`, `product`, `vendor`, `cpe`, `severity`, `cvss_score`, `epss_score`, `is_kev`, `exploit_score`, `evidence`, `confidence`, `caveats`, `version_source`, `host`, `ip`, `port`, `url` |

## Examples

Start from one of these queries and adjust it to your target.

### Priority

| Query | Finds |
|---|---|
| `is:kev`{ .rn-q } | Software carrying a CVE with confirmed exploitation |
| `is:kev and is:firm`{ .rn-q } | Confirmed exploited and fully verified |
| `severity:critical and is:stated`{ .rn-q } | Critical CVEs where the server stated its own version |
| `epss>=0.5`{ .rn-q } | EPSS probability of 0.5 or above |
| `is:kev and is:fixable`{ .rn-q } | Known exploited CVEs with an unaffected release on the same target |

### Change

| Query | Finds |
|---|---|
| `is:new`{ .rn-q } | Matches absent from every earlier scan of this target |
| `is:new and severity:[critical,high]`{ .rn-q } | Severe matches absent from every earlier scan |

### Software

| Query | Finds |
|---|---|
| `software:nginx`{ .rn-q } | Everything running nginx |
| `product:http_server and cvss>=9`{ .rn-q } | Apache builds carrying a critically scored CVE |
| `software:wordpress and is:new`{ .rn-q } | WordPress matches absent from every earlier scan |

### Confidence

| Query | Finds |
|---|---|
| `confidence:high`{ .rn-q } | Matches with no unverified part |
| `caveat:backport`{ .rn-q } | Distribution builds that may patch without a version change |
| `not caveat:conditional`{ .rn-q } | Matches NVD does not tie to a further component |
| `evidence:corroborated`{ .rn-q } | Matches that a check at the same host also names |

## Field reference

Each field in detail: its type, the operators it accepts, its values and an example.

### cve { #f-cve }

Published identifier of the weakness.

Type
:   `string`

Group
:   Vulnerability

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cve:CVE-2021-23017`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### software { #f-software }

Name of the software as the scan read it.

Type
:   `string`

Group
:   Software

Aliases
:   `name`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `software:nginx`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### product { #f-product }

Product as NVD files it.

Type
:   `string`

Group
:   Software

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `product:http_server`{ .rn-q }

### vendor { #f-vendor }

Vendor as NVD files it.

Type
:   `string`

Group
:   Software

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `vendor:apache`{ .rn-q }

### version { #f-version }

Version the asset reported.

Type
:   `string`

Group
:   Software

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `version:2.4.52`{ .rn-q }

### source { #f-source }

Source of the reported version.

Type
:   `enum`

Group
:   Software

Operators
:   `:` `=` `!=`

Values
:   `banner`, `fingerprint`

Example
:   `source:banner`{ .rn-q }

Matching
:   Values are matched as substrings.

### severity { #f-severity }

Severity NVD scored the CVE at.

Type
:   `enum`

Group
:   Vulnerability

Operators
:   `:` `=` `!=`

Values
:   `critical`, `high`, `medium`, `low`, `info`, `unknown`

Example
:   `severity:critical`{ .rn-q }

Matching
:   Values are matched as substrings.

### cvss { #f-cvss }

CVSS base score.

Type
:   `number`

Group
:   Vulnerability

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `cvss>=9`{ .rn-q }

Matching
:   Decimal value.

### epss { #f-epss }

Probability of exploitation in the next 30 days.

Type
:   `number`

Group
:   Vulnerability

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `epss>=0.5`{ .rn-q }

Matching
:   Decimal value.

### rank { #f-rank }

Exploitation rank built from the intelligence signals.

Type
:   `number`

Group
:   Vulnerability

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `rank>=40`{ .rn-q }

### confidence { #f-confidence }

Verification level of the match.

Type
:   `enum`

Group
:   Confidence

Operators
:   `:` `=` `!=`

Values
:   `high`, `medium`, `low`

Example
:   `confidence:high`{ .rn-q }

Matching
:   Values are matched as substrings.

### caveat { #f-caveat }

A part of the match that is not verified.

Type
:   `enum`

Group
:   Confidence

Operators
:   `:` `=` `!=`

Values
:   `backport`, `conditional`, `fingerprint`, `coarse`

Example
:   `caveat:backport`{ .rn-q }

### evidence { #f-evidence }

Inferred from the version alone, or corroborated by a check at the same host.

Type
:   `enum`

Group
:   Confidence

Operators
:   `:` `=` `!=`

Values
:   `inferred`, `corroborated`

Example
:   `evidence:corroborated`{ .rn-q }

Matching
:   Values are matched as substrings.

### target { #f-target }

Target the asset belongs to.

Type
:   `string`

Group
:   Asset

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `target:example.com`{ .rn-q }

### host { #f-host }

Hostname running the software.

Type
:   `string`

Group
:   Asset

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `host:www.example.com`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### ip { #f-ip }

Address running the software.

Type
:   `ip`

Group
:   Asset

Operators
:   `:` `=` `!=`

Example
:   `ip:203.0.113.10`{ .rn-q }

### port { #f-port }

Port the software answers on.

Type
:   `number`

Group
:   Asset

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `port:443`{ .rn-q }

### seen { #f-seen }

When the CVE was inferred.

Type
:   `date`

Group
:   Asset

Aliases
:   `discovered`, `age`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `seen:<24h`{ .rn-q }

Matching
:   A relative age counts back from now.

### is { #f-is }

Property of the match.

Type
:   `flag`

Group
:   Flags

Aliases
:   `has`

Operators
:   `:`

Values
:   [`new`](#is-new), [`kev`](#is-kev), [`ransomware`](#is-ransomware), [`overdue`](#is-overdue), [`likely`](#is-likely), [`firm`](#is-firm), [`conditional`](#is-conditional), [`backport`](#is-backport), [`fingerprinted`](#is-fingerprinted), [`stated`](#is-stated), [`web`](#is-web), [`service`](#is-service), [`corroborated`](#is-corroborated), [`fixable`](#is-fixable)

Example
:   `is:kev`{ .rn-q }

## Flag reference

Each flag in detail, with the rule a row must meet to match it.

### is:new { #is-new }

Not inferred by an earlier scan of this target.

Written as
:   `is:new`, `has:new`

Matches when
:   An earlier scan of the target recorded at least one software CVE, and none had this fingerprint.

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

### is:likely { #is-likely }

EPSS score of 0.088 or above.

Written as
:   `is:likely`, `has:likely`

Matches when
:   EPSS at or above 0.088.

### is:firm { #is-firm }

Every part of the match is verified.

Written as
:   `is:firm`, `has:firm`

Matches when
:   Confidence is high.

### is:conditional { #is-conditional }

NVD names a further component not identified on the asset.

Written as
:   `is:conditional`, `has:conditional`

Matches when
:   Caveats include conditional.

### is:backport { #is-backport }

A distribution build. Fixes may land without a version change.

Written as
:   `is:backport`, `has:backport`

Matches when
:   Caveats include backport.

### is:fingerprinted { #is-fingerprinted }

Version read from the page body.

Written as
:   `is:fingerprinted`, `has:fingerprinted`

Matches when
:   Version_source is fingerprint.

### is:stated { #is-stated }

Version stated in a server header.

Written as
:   `is:stated`, `has:stated`

Matches when
:   Version_source is banner.

### is:web { #is-web }

Inferred from a web asset.

Written as
:   `is:web`, `has:web`

Matches when
:   Bound to an HTTP asset.

### is:service { #is-service }

Inferred from a service banner.

Written as
:   `is:service`, `has:service`

Matches when
:   Bound to a port.

### is:corroborated { #is-corroborated }

A check at the same host names the same CVE.

Written as
:   `is:corroborated`, `has:corroborated`

Matches when
:   Evidence is corroborated.

### is:fixable { #is-fixable }

A newer release on the same target is not affected.

Written as
:   `is:fixable`, `has:fixable`

Matches when
:   Fixed_in is set.

