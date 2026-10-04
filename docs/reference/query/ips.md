---
title: IP addresses
description: "Everything you can search, group and sort in the ip addresses dimension, with example queries. Keep this page open while you write a query on addresses."
sources:
  - shared/definitions/asset_query.py
  - shared/services/surface_query/ips.py
  - frontend/src/lib/components/scans/results/ips-table.svelte
revised: 2026-10-03
generated: scripts/gen_query.py
layout: reference
nav_order: 3
---

This page is generated from the reNgine 3.0 source. `scripts/gen_query.py` writes it from `data/query-schema.json`, `data/openapi.json` and `data/mcp-dimensions.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Each row in the IP addresses dimension is one distinct IP address across the scans in scope, folded from resolved hostnames, ports, HTTP assets and ip_addresses rows. One row serves every target that shares the address. You search these rows in the query bar of the table, in the HTTP API with `POST /api/v1/ips/search` and from an MCP client with the tool `query_assets`. For the syntax that works in every dimension, see [Query language](index.md).

## About this dimension

The basics: what a row is, which stages fill the dimension, and where you search it.

| Property | Value |
|---|---|
| One row is | One distinct IP address across the scans in scope, folded from resolved hostnames, ports, HTTP assets and ip_addresses rows. One row serves every target that shares the address. |
| Singular and plural | address, addresses |
| Identified by | `ip` |
| Stages that add rows | [`asset_seed`](../stages/asset_seed.md), [`host_discovery`](../stages/host_discovery.md), [`seed_resolution`](../stages/seed_resolution.md), [`subdomain_discovery`](../stages/subdomain_discovery.md) |
| Stages that cover it | [`host_discovery`](../stages/host_discovery.md), [`subdomain_discovery`](../stages/subdomain_discovery.md) |
| Free-text fields | `ip`, `ptr`, `org`, `prefix`, `cdn`, `service`, `host` |
| Flag prefixes | `is:`, `has:` |
| Search API | `POST /api/v1/ips/search` |
| Query bar placeholder | `is:sensitive not cdn:yes`{ .rn-q } |

Coverage tells you whether an empty table means that nothing was found or that nothing was looked for. A dimension is covered for a target when a covering stage succeeded in a run, or when a run wrote rows to it. Without coverage, the dimension reads **Not scanned**, which is not the same as zero rows.

## Fields

Fields are the properties you search on, written `field:value`. An alias works the same as the field name. Select a field to see its operators, its values and an example.

| Field | Aliases | Type | Group | Description |
|---|---|---|---|---|
| [`target`](#f-target) | `scope` | string | Scope | Target this address belongs to. |
| [`ip`](#f-ip) | `address`, `addr` | ip | Address | IP address. Accepts a CIDR range. |
| [`ptr`](#f-ptr) | `reverse`, `rdns` | string | Address | PTR record for the address. |
| [`seen`](#f-seen) | `discovered` | date | Address | When these scans first recorded the address. |
| [`asn`](#f-asn) |  | number | Network | Autonomous system number announcing the address. |
| [`org`](#f-org) | `asn_org`, `operator` | string | Network | Operator of the autonomous system. |
| [`country`](#f-country) |  | enum | Network | Two-letter registered country of the network block. |
| [`prefix`](#f-prefix) |  | string | Network | Announced prefix containing the address. |
| [`cdn`](#f-cdn) |  | string | Network | CDN in front of the address. yes or no filters on presence. |
| [`port`](#f-port) |  | number | Services | Open port on the address. |
| [`service`](#f-service) |  | enum | Services | Service name on an open port. |
| [`ports`](#f-ports) | `port_count` | number | Services | Number of open ports on the address. |
| [`host`](#f-host) | `name`, `subdomain` | string | Hosts | Hostname that resolves to the address. |
| [`hosts`](#f-hosts) | `host_count` | number | Hosts | Number of hostnames resolving to the address. |
| [`assets`](#f-assets) | `asset_count` | number | Hosts | Number of HTTP services probed on the address. |
| [`is`](#f-is) | `has` | flag | Flags | Property of the address. |
| [`vuln`](#f-vuln) | `finding` | enum | Findings | Severity of a finding recorded on this address. |
| [`cve`](#f-cve) |  | string | Findings | Published vulnerability identifier reported on this address. |

## Flags

Flags are yes-or-no properties of a row. Write them with `is:` or `has:`, for example `is:new`{ .rn-q }.

| Flag | Description |
|---|---|
| [`is:new`](#is-new) | Not recorded by an earlier scan of this target |
| [`is:alive`](#is-alive) | Responded to a probe |
| [`is:open`](#is-open) | One or more ports are open |
| [`is:sensitive`](#is-sensitive) | An admin or database port is open |
| [`is:hosted`](#is-hosted) | One or more hostnames resolve to it |
| [`is:web`](#is-web) | An HTTP service was probed on it |
| [`is:cdn`](#is-cdn) | Fronted by a CDN |
| [`is:ptr`](#is-ptr) | Has a PTR record |
| [`is:private`](#is-private) | In a private address range |
| [`is:v4`](#is-v4) | IPv4 address |
| [`is:v6`](#is-v6) | IPv6 address |
| [`is:vulnerable`](#is-vulnerable) | A vulnerability scan reported a finding on it |
| [`is:kev`](#is-kev) | A known-exploited weakness was found on it |

## Group keys

Group the rows by one of these keys to count how many rows share each value. Use the **Group by** menu of the table, or the `groups` search operation of the HTTP API.

| Key | Label | Groups |
|---|---|---|
| `target` | Target | Rows belonging to the same target |
| `asn` | Autonomous system | Addresses announced by the same AS |
| `org` | Network operator | Addresses run by the same operator |
| `prefix` | Announced prefix | Addresses inside the same announced prefix |
| `country` | Country | Addresses registered in the same country |
| `cdn` | CDN | Addresses fronted by the same CDN |
| `port` | Open port | Addresses exposing the same port |
| `service` | Service | Addresses running the same service |

## Sort

The keys you can sort by, and the order you get when you do not choose one.

| Property | Value |
|---|---|
| Sort keys | `ip`, `hosts`, `ports`, `assets`, `asn`, `country` |
| API default | `hosts` desc |
| Interface default | `hosts` desc |
| Tie-break | Address asc (numeric). NULLs last. |

## Columns

The table always starts with its leading columns. You choose which optional columns to show. An export of this dimension writes the export columns.

| Set | Columns |
|---|---|
| Leading columns | **Address**, **Network** |
| Optional columns | **Web assets**, **Ports**, **Country**, **Prefix**, **PTR**, **Web** |
| Shown by default | **Web assets**, **Ports**, **Country** |
| Export columns | `ip`, `version`, `asn`, `asn_org`, `country`, `prefix`, `is_cdn`, `cdn_name`, `is_alive`, `ports`, `port_count`, `host_count`, `hosts`, `has_sensitive` |

## Examples

Start from one of these queries and adjust it to your target.

### Exposed services

| Query | Finds |
|---|---|
| `is:sensitive`{ .rn-q } | Administrative or database ports exposed |
| `port:[3306,5432,27017,6379,9200,11211,5984]`{ .rn-q } | Database ports reachable from the internet |
| `port:[22,23,3389,5900]`{ .rn-q } | Remote administration ports reachable |
| `service:[ftp,telnet,rlogin,vnc]`{ .rn-q } | Cleartext remote-access services running |
| `ports:>10`{ .rn-q } | Addresses exposing more than ten ports |

### Origin exposure

| Query | Finds |
|---|---|
| `is:open and not is:cdn`{ .rn-q } | Open ports on addresses without a CDN |
| `is:web and not is:cdn`{ .rn-q } | HTTP served directly from the origin address |
| `is:cdn and is:open`{ .rn-q } | Open ports on CDN-fronted addresses |

### Hosting

| Query | Finds |
|---|---|
| `hosts:>10`{ .rn-q } | Addresses shared by more than ten hostnames |
| `is:open and not is:hosted`{ .rn-q } | Open ports on addresses with no hostname |
| `is:v6`{ .rn-q } | IPv6 addresses in the attack surface |
| `is:alive and not is:ptr`{ .rn-q } | Responding addresses with no PTR record |

### Hygiene

| Query | Finds |
|---|---|
| `is:private`{ .rn-q } | Private addresses published in public DNS |
| `is:hosted and not is:alive`{ .rn-q } | Hostnames resolving to an unresponsive address |
| `ptr:. and not is:hosted`{ .rn-q } | Addresses with a PTR record but no known hostname |

### Change

| Query | Finds |
|---|---|
| `is:new`{ .rn-q } | Addresses absent from every earlier scan |
| `is:new and is:sensitive`{ .rn-q } | Administrative ports on new addresses |

## Field reference

Each field in detail: its type, the operators it accepts, its values and an example.

### target { #f-target }

Target this address belongs to.

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

Matching
:   True when any target the address serves matches.

### ip { #f-ip }

IP address. Accepts a CIDR range.

Type
:   `ip`

Group
:   Address

Aliases
:   `address`, `addr`

Operators
:   `:` `=` `!=`

Example
:   `ip:104.16.0.0/12`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### ptr { #f-ptr }

PTR record for the address.

Type
:   `string`

Group
:   Address

Aliases
:   `reverse`, `rdns`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `ptr:.internal`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### seen { #f-seen }

When these scans first recorded the address.

Type
:   `date`

Group
:   Address

Aliases
:   `discovered`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `seen:<7d`{ .rn-q }

Matching
:   A relative age counts back from now.

### asn { #f-asn }

Autonomous system number announcing the address.

Type
:   `number`

Group
:   Network

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `asn:13335`{ .rn-q }

Matching
:   Accepts AS13335.

### org { #f-org }

Operator of the autonomous system.

Type
:   `string`

Group
:   Network

Aliases
:   `asn_org`, `operator`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `org:"digital ocean"`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### country { #f-country }

Two-letter registered country of the network block.

Type
:   `enum`

Group
:   Network

Operators
:   `:` `=` `!=`

Example
:   `country:DE`{ .rn-q }

Matching
:   Values are matched as substrings.

### prefix { #f-prefix }

Announced prefix containing the address.

Type
:   `string`

Group
:   Network

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `prefix:104.16`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### cdn { #f-cdn }

CDN in front of the address. yes or no filters on presence.

Type
:   `string`

Group
:   Network

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cdn:cloudflare`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Yes/no words filter on presence.

### port { #f-port }

Open port on the address.

Type
:   `number`

Group
:   Services

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `port:[22,3389]`{ .rn-q }

### service { #f-service }

Service name on an open port.

Type
:   `enum`

Group
:   Services

Operators
:   `:` `=` `!=`

Example
:   `service:ssh`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Values are matched as substrings of the service name.

### ports { #f-ports }

Number of open ports on the address.

Type
:   `number`

Group
:   Services

Aliases
:   `port_count`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `ports:>10`{ .rn-q }

### host { #f-host }

Hostname that resolves to the address.

Type
:   `string`

Group
:   Hosts

Aliases
:   `name`, `subdomain`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `host:api`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### hosts { #f-hosts }

Number of hostnames resolving to the address.

Type
:   `number`

Group
:   Hosts

Aliases
:   `host_count`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `hosts:>5`{ .rn-q }

### assets { #f-assets }

Number of HTTP services probed on the address.

Type
:   `number`

Group
:   Hosts

Aliases
:   `asset_count`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `assets:>0`{ .rn-q }

### is { #f-is }

Property of the address.

Type
:   `flag`

Group
:   Flags

Aliases
:   `has`

Operators
:   `:`

Values
:   [`new`](#is-new), [`alive`](#is-alive), [`open`](#is-open), [`sensitive`](#is-sensitive), [`hosted`](#is-hosted), [`web`](#is-web), [`cdn`](#is-cdn), [`ptr`](#is-ptr), [`private`](#is-private), [`v4`](#is-v4), [`v6`](#is-v6), [`vulnerable`](#is-vulnerable), [`kev`](#is-kev)

Example
:   `is:sensitive`{ .rn-q }

### vuln { #f-vuln }

Severity of a finding recorded on this address.

Type
:   `enum`

Group
:   Findings

Aliases
:   `finding`

Operators
:   `:` `=` `!=`

Values
:   `critical`, `high`, `medium`, `low`, `info`, `unknown`

Example
:   `vuln:critical`{ .rn-q }

Matching
:   A finding in scope on the address.

### cve { #f-cve }

Published vulnerability identifier reported on this address.

Type
:   `string`

Group
:   Findings

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cve:CVE-2021-44228`{ .rn-q }

## Flag reference

Each flag in detail, with the rule a row must meet to match it.

### is:new { #is-new }

Not recorded by an earlier scan of this target.

Written as
:   `is:new`, `has:new`

Matches when
:   Single scan: an earlier scan of the target recorded at least one address and none recorded this one. Project scope: earlier rows exist for a target the address serves and none of them hold this address.

### is:alive { #is-alive }

Responded to a probe.

Written as
:   `is:alive`, `has:alive`

Matches when
:   Is_alive is true (falls back to: has a port or an HTTP asset)

### is:open { #is-open }

One or more ports are open.

Written as
:   `is:open`, `has:open`

Matches when
:   Port_count above 0.

### is:sensitive { #is-sensitive }

An admin or database port is open.

Written as
:   `is:sensitive`, `has:sensitive`

Matches when
:   A port from SENSITIVE_PORTS is open.

### is:hosted { #is-hosted }

One or more hostnames resolve to it.

Written as
:   `is:hosted`, `has:hosted`

Matches when
:   Host_count above 0.

### is:web { #is-web }

An HTTP service was probed on it.

Written as
:   `is:web`, `has:web`

Matches when
:   Asset_count above 0.

### is:cdn { #is-cdn }

Fronted by a CDN.

Written as
:   `is:cdn`, `has:cdn`

Matches when
:   Is_cdn is true.

### is:ptr { #is-ptr }

Has a PTR record.

Written as
:   `is:ptr`, `has:ptr`

Matches when
:   At least one PTR hostname.

### is:private { #is-private }

In a private address range.

Written as
:   `is:private`, `has:private`

Matches when
:   Address inside a private or reserved range (same list as services)

### is:v4 { #is-v4 }

IPv4 address.

Written as
:   `is:v4`, `has:v4`

Matches when
:   IPv4.

### is:v6 { #is-v6 }

IPv6 address.

Written as
:   `is:v6`, `has:v6`

Matches when
:   IPv6.

### is:vulnerable { #is-vulnerable }

A vulnerability scan reported a finding on it.

Written as
:   `is:vulnerable`, `has:vulnerable`

Matches when
:   A finding in scope has this address.

### is:kev { #is-kev }

A known-exploited weakness was found on it.

Written as
:   `is:kev`, `has:kev`

Matches when
:   Such a finding is KEV-listed.

