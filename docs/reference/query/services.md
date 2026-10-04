---
title: Services
description: "Everything you can search, group and sort in the services dimension, with example queries. Keep this page open while you write a query on services."
sources:
  - shared/definitions/asset_query.py
  - shared/services/surface_query/services.py
  - shared/definitions/compare.py
  - frontend/src/lib/components/scans/results/services-table.svelte
revised: 2026-10-03
generated: scripts/gen_query.py
layout: reference
nav_order: 2
---

This page is generated from the reNgine 3.0 source. `scripts/gen_query.py` writes it from `data/query-schema.json`, `data/openapi.json` and `data/mcp-dimensions.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Each row in the Services dimension is one open port on one address recorded by one scan (a ports row), joined to the address, its hostnames and the HTTP response on that port. You search these rows in the query bar of the table, in the HTTP API with `POST /api/v1/ports/search` and from an MCP client with the tool `query_assets`. For the syntax that works in every dimension, see [Query language](index.md).

## About this dimension

The basics: what a row is, which stages fill the dimension, and where you search it.

| Property | Value |
|---|---|
| One row is | One open port on one address recorded by one scan (a ports row), joined to the address, its hostnames and the HTTP response on that port. |
| Singular and plural | service, services |
| Identified by | `ip, number, protocol` |
| Stages that add rows | [`passive_ports`](../stages/passive_ports.md), [`port_scan`](../stages/port_scan.md) |
| Stages that cover it | [`port_scan`](../stages/port_scan.md) |
| Free-text fields | `service`, `product`, `version`, `banner`, `ip`, `org`, `cdn`, `host` |
| Flag prefixes | `is:`, `has:` |
| Search API | `POST /api/v1/ports/search` |
| Query bar placeholder | `class:database not is:cdn`{ .rn-q } |

Coverage tells you whether an empty table means that nothing was found or that nothing was looked for. A dimension is covered for a target when a covering stage succeeded in a run, or when a run wrote rows to it. Without coverage, the dimension reads **Not scanned**, which is not the same as zero rows.

## Fields

Fields are the properties you search on, written `field:value`. An alias works the same as the field name. Select a field to see its operators, its values and an example.

| Field | Aliases | Type | Group | Description |
|---|---|---|---|---|
| [`target`](#f-target) | `scope` | string | Scope | Target this service belongs to. |
| [`port`](#f-port) |  | number | Service | Port number. Accepts a list or a range. |
| [`seen`](#f-seen) | `discovered` | date | Service | When the service was recorded. |
| [`service`](#f-service) |  | string | Service | Service running on the port. |
| [`class`](#f-class) | `kind` | enum | Service | Service class. |
| [`protocol`](#f-protocol) |  | enum | Service | Transport protocol. |
| [`source`](#f-source) |  | enum | Service | The source that observed the service. |
| [`product`](#f-product) |  | string | Software | Software named by the service banner. |
| [`version`](#f-version) |  | string | Software | Version reported by the service. |
| [`banner`](#f-banner) |  | text | Software | Text the service returned on connect. |
| [`ai`](#f-ai) | `ai_service` | enum | Software | AI service identified on the port. Takes a service, a category, yes or no. |
| [`ai.model`](#f-ai-model) |  | string | Software | Model an AI service on the port listed. yes or no filters on presence. |
| [`ip`](#f-ip) | `address`, `addr` | ip | Address | Address the service listens on. Accepts a CIDR range. |
| [`asn`](#f-asn) |  | number | Address | Autonomous system announcing the address. |
| [`org`](#f-org) | `as_name`, `asn_org` | string | Address | Operator of the announcing network. |
| [`country`](#f-country) |  | enum | Address | Two-letter country of the address. |
| [`cdn`](#f-cdn) |  | string | Address | CDN in front of the address. yes or no filters on presence. |
| [`host`](#f-host) | `name`, `subdomain` | string | Hosts | Hostname resolving to the address. |
| [`status`](#f-status) |  | number | Hosts | HTTP status returned on this port. |
| [`is`](#f-is) | `has` | flag | Flags | Property of the service. |
| [`vuln`](#f-vuln) | `finding` | enum | Findings | Severity of a finding recorded on this service. |
| [`cve`](#f-cve) |  | string | Findings | Published vulnerability identifier reported on this service. |

## Flags

Flags are yes-or-no properties of a row. Write them with `is:` or `has:`, for example `is:new`{ .rn-q }.

| Flag | Description |
|---|---|
| [`is:new`](#is-new) | Not open in an earlier scan of this target |
| [`is:http`](#is-http) | Answered an HTTP request |
| [`is:tls`](#is-tls) | Negotiates TLS |
| [`is:sensitive`](#is-sensitive) | An administrative or datastore port |
| [`is:named`](#is-named) | Software identified |
| [`is:passive`](#is-passive) | Reported by an internet-wide scanner, not observed directly |
| [`is:confirmed`](#is-confirmed) | Observed directly |
| [`is:cdn`](#is-cdn) | On a CDN-fronted address |
| [`is:hosted`](#is-hosted) | A hostname resolves to the address |
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
| `service` | Service | Ports running the same service |
| `class` | Service class | Services of the same class |
| `port` | Port | Services on the same port number |
| `product` | Software | Services running the same software |
| `ip` | Address | Services on the same address |
| `asn` | Autonomous system | Services in the same announced network |
| `org` | Network operator | Services on the same operator's network |
| `country` | Country | Services in the same country |
| `source` | Evidence | Services with the same evidence |

## Sort

The keys you can sort by, and the order you get when you do not choose one.

| Property | Value |
|---|---|
| Sort keys | `exposure`, `port`, `ip`, `service`, `class`, `product`, `hosts`, `asn`, `country`, `status` |
| API default | `exposure` desc |
| Interface default | `exposure` desc |
| Tie-break | Address asc, port asc, id asc. NULLs last. |

## Columns

The table always starts with its leading columns. You choose which optional columns to show. An export of this dimension writes the export columns.

| Set | Columns |
|---|---|
| Leading columns | **Service**, **Software** |
| Optional columns | **Web assets**, **Web**, **Network**, **Country**, **Evidence** |
| Shown by default | **Web assets**, **Web**, **Country** |
| Export columns | `ip`, `port`, `protocol`, `service_name`, `service_class`, `product`, `version`, `is_http`, `tls`, `status_code`, `title`, `url`, `hosts`, `asn_org`, `country`, `is_cdn`, `is_sensitive`, `source`, `is_new` |

## Examples

Start from one of these queries and adjust it to your target.

### Critical exposure

| Query | Finds |
|---|---|
| `class:database`{ .rn-q } | Data stores reachable from the internet |
| `service:[redis,memcached,mongodb,elasticsearch]`{ .rn-q } | Data stores with no authentication by default |
| `service:docker`{ .rn-q } | Container runtime API exposed |
| `is:sensitive and not is:cdn`{ .rn-q } | Administrative ports on an origin address |

### Change

| Query | Finds |
|---|---|
| `is:new`{ .rn-q } | Ports not open in any earlier scan |
| `is:new and is:sensitive`{ .rn-q } | Administrative ports not open in any earlier scan |

### Remote access

| Query | Finds |
|---|---|
| `class:remote`{ .rn-q } | Interactive administration reachable |
| `service:ssh and not port:22`{ .rn-q } | SSH on a non-standard port |
| `service:[telnet,ftp,rlogin,rexec]`{ .rn-q } | Protocols that carry credentials in the clear |
| `service:rdp or service:vnc`{ .rn-q } | Remote desktop reachable from the internet |

### Web surface

| Query | Finds |
|---|---|
| `is:http and not port:[80,443]`{ .rn-q } | Web services on a non-standard port |
| `is:http and not is:tls`{ .rn-q } | Web services without TLS |
| `class:web and not is:http`{ .rn-q } | Web ports with no HTTP response |
| `status:401 or status:403`{ .rn-q } | Services requiring authentication |

### Evidence

| Query | Finds |
|---|---|
| `is:passive`{ .rn-q } | Ports reported by external scanners, not confirmed |
| `is:named`{ .rn-q } | Services with identified software |
| `is:confirmed and not is:named`{ .rn-q } | Open ports with no service identified |

### Hygiene

| Query | Finds |
|---|---|
| `class:mail and not is:tls`{ .rn-q } | Mail services without transport encryption |
| `not is:hosted`{ .rn-q } | Services on addresses with no known hostname |
| `class:infra`{ .rn-q } | Directory, file and management services |

## Field reference

Each field in detail: its type, the operators it accepts, its values and an example.

### target { #f-target }

Target this service belongs to.

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

### port { #f-port }

Port number. Accepts a list or a range.

Type
:   `number`

Group
:   Service

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `port:[22,3389]`{ .rn-q }

### seen { #f-seen }

When the service was recorded.

Type
:   `date`

Group
:   Service

Aliases
:   `discovered`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `seen:<7d`{ .rn-q }

Matching
:   A relative age counts back from now.

### service { #f-service }

Service running on the port.

Type
:   `string`

Group
:   Service

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `service:ssh`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### class { #f-class }

Service class.

Type
:   `enum`

Group
:   Service

Aliases
:   `kind`

Operators
:   `:` `=` `!=`

Values
:   `web`, `remote`, `database`, `mail`, `infra`, `other`

Example
:   `class:database`{ .rn-q }

Matching
:   Values are matched as substrings.

### protocol { #f-protocol }

Transport protocol.

Type
:   `enum`

Group
:   Service

Operators
:   `:` `=` `!=`

Values
:   `tcp`, `udp`

Example
:   `protocol:tcp`{ .rn-q }

Matching
:   Values are matched as substrings.

### source { #f-source }

The source that observed the service.

Type
:   `enum`

Group
:   Service

Operators
:   `:` `=` `!=`

Values
:   `naabu`, `internetdb`, `http_probe`, `banner`, `seed`

Example
:   `source:naabu`{ .rn-q }

Matching
:   Values are matched as substrings.

### product { #f-product }

Software named by the service banner.

Type
:   `string`

Group
:   Software

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `product:OpenSSH`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### version { #f-version }

Version reported by the service.

Type
:   `string`

Group
:   Software

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `version:8.9`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### banner { #f-banner }

Text the service returned on connect.

Type
:   `text`

Group
:   Software

Operators
:   `:` `=` `!=`

Example
:   `banner:ubuntu`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Matched as a substring.

### ai { #f-ai }

AI service identified on the port. Takes a service, a category, yes or no.

Type
:   `enum`

Group
:   Software

Aliases
:   `ai_service`

Operators
:   `:` `=` `!=`

Values
:   `yes`, `no`, `self_hosted`, `gateway`, `mcp`, `application`, `cloud`, `generic`, `ollama`, `vllm`, `sglang`, `localai`, `llama-cpp`, `huggingface-tgi`, `nvidia-nim`, `tensorrt-llm`, `triton-inference-server`, `bentoml`, `ray-serve`, `aphrodite-engine`, `baseten-truss`, `deepspeed-mii`, `fastchat-controller`, `gpt4all`, `gradio`, `jan`, `koboldcpp`, `lm-studio`, `mlc-llm`, `petals`, `powerinfer`, `tabbyapi`, `text-generation-webui`, `litellm`, `bifrost`, `envoy-ai-gateway`, `helicone`, `kong-proxy`, `omniroute`, `portkey-ai-gateway`, `tensorzero`, `mcp-server`, `anythingllm`, `astrbot`, `betterchatgpt`, `dify`, `flowise`, `h2ogpt`, `huggingface-chat-ui`, `langflow`, `librechat`, `lobehub`, `nextchat`, `onyx`, `openclaw`, `open-webui`, `privategpt`, `quivr`, `ragflow`, `sillytavern`, `aws-bedrock`, `azure-openai`, `cloudflare-ai-gateway`, `databricks-model-serving`, `fireworks-ai`, `vertex-ai`, `groq`, `modal`, `replicate`, `salesforce-einstein`, `together-ai`, `openai-compatible`

Example
:   `ai:ollama`{ .rn-q }

### ai.model { #f-ai-model }

Model an AI service on the port listed. yes or no filters on presence.

Type
:   `string`

Group
:   Software

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `ai.model~llama`{ .rn-q }

### ip { #f-ip }

Address the service listens on. Accepts a CIDR range.

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

### asn { #f-asn }

Autonomous system announcing the address.

Type
:   `number`

Group
:   Address

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `asn:13335`{ .rn-q }

Matching
:   Accepts AS13335.

### org { #f-org }

Operator of the announcing network.

Type
:   `string`

Group
:   Address

Aliases
:   `as_name`, `asn_org`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `org:cloudflare`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### country { #f-country }

Two-letter country of the address.

Type
:   `enum`

Group
:   Address

Operators
:   `:` `=` `!=`

Example
:   `country:DE`{ .rn-q }

Matching
:   Values are matched as substrings.

### cdn { #f-cdn }

CDN in front of the address. yes or no filters on presence.

Type
:   `string`

Group
:   Address

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cdn:cloudflare`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Yes/no words filter on presence.

### host { #f-host }

Hostname resolving to the address.

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

Matching
:   True when a hostname in scope resolving to the address matches.

### status { #f-status }

HTTP status returned on this port.

Type
:   `number`

Group
:   Hosts

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `status:200`{ .rn-q }

Matching
:   HTTP status on this port. No status classes here.

### is { #f-is }

Property of the service.

Type
:   `flag`

Group
:   Flags

Aliases
:   `has`

Operators
:   `:`

Values
:   [`new`](#is-new), [`http`](#is-http), [`tls`](#is-tls), [`sensitive`](#is-sensitive), [`named`](#is-named), [`passive`](#is-passive), [`confirmed`](#is-confirmed), [`cdn`](#is-cdn), [`hosted`](#is-hosted), [`private`](#is-private), [`v4`](#is-v4), [`v6`](#is-v6), [`vulnerable`](#is-vulnerable), [`kev`](#is-kev)

Example
:   `is:sensitive`{ .rn-q }

### vuln { #f-vuln }

Severity of a finding recorded on this service.

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
:   A finding in scope on the same address and port.

### cve { #f-cve }

Published vulnerability identifier reported on this service.

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

Not open in an earlier scan of this target.

Written as
:   `is:new`, `has:new`

Matches when
:   An earlier scan of the target recorded at least one port, and none recorded this address and port.

### is:http { #is-http }

Answered an HTTP request.

Written as
:   `is:http`, `has:http`

Matches when
:   Is_http is true.

### is:tls { #is-tls }

Negotiates TLS.

Written as
:   `is:tls`, `has:tls`

Matches when
:   Tls is true.

### is:sensitive { #is-sensitive }

An administrative or datastore port.

Written as
:   `is:sensitive`, `has:sensitive`

Matches when
:   Port number is in SENSITIVE_PORTS.

### is:named { #is-named }

Software identified.

Written as
:   `is:named`, `has:named`

Matches when
:   A product is recorded.

### is:passive { #is-passive }

Reported by an internet-wide scanner, not observed directly.

Written as
:   `is:passive`, `has:passive`

Matches when
:   Source is internetdb.

### is:confirmed { #is-confirmed }

Observed directly.

Written as
:   `is:confirmed`, `has:confirmed`

Matches when
:   Source is anything but internetdb.

### is:cdn { #is-cdn }

On a CDN-fronted address.

Written as
:   `is:cdn`, `has:cdn`

Matches when
:   The address is CDN-fronted.

### is:hosted { #is-hosted }

A hostname resolves to the address.

Written as
:   `is:hosted`, `has:hosted`

Matches when
:   At least one hostname in scope resolves to the address.

### is:private { #is-private }

In a private address range.

Written as
:   `is:private`, `has:private`

Matches when
:   Address inside 10/8, 172.16/12, 192.168/16, 127/8, 169.254/16, 100.64/10, ::1, fc00::/7 or fe80::/10.

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
:   A finding in scope has the same address and port.

### is:kev { #is-kev }

A known-exploited weakness was found on it.

Written as
:   `is:kev`, `has:kev`

Matches when
:   Such a finding is KEV-listed.

