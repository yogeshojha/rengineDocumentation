---
title: Port Scan
description: Find listening TCP services on every address in scope. It sends traffic to your target.
sources:
  - "stages/port_scan/stage.py:45"
  - stages/port_scan/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 311
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `port_scan` |
| Group | Services |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 4 of 8 |
| Depends on | [CDN and Cloud Attribution](cdn_check.md), [Passive Port Discovery](passive_ports.md) |
| Input | `addresses` |
| Output | `ports` |
| Adds results to | [Services](../query/services.md), [IP addresses](../query/ips.md) |
| Tools | `naabu` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | No |
| In the Default engine | No |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: Port rows with source naabu. IpAddress.scan_policy and scan_policy_reason.

## Request rate

The stage runs `naabu` with a timeout of 3 s and 1 retry. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 1,000 | 100 |
| Normal | 1,000 | 100 |
| Aggressive | 3,000 | 200 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Scan ports | boolean | `false` |  | Find listening TCP services on every address in scope. |
| `profile` | Port set | string | `exposure` | `web` Web ports, `exposure` Web and sensitive, `top-100` Top 100, `top-1000` Top 1000, `full` All ports, `custom` Custom | Ports to probe. Web and sensitive covers the web surface plus administrative and datastore ports. |
| `ports` | Custom ports | string | `` | At most 2000 characters | Used only when the port set is Custom. A list or range like 80,443,8000-8100. |
| `exclude_ports` (advanced) | Exclude ports | string | `` | At most 2000 characters | Ports excluded from every scan, as a list or range. |
| `scan_type` (advanced) | Scan type | string | `connect` | `connect` Connect, `syn` SYN | Connect completes the TCP handshake. SYN needs raw sockets on the worker. |
| `cdn_policy` (advanced) | CDN-fronted addresses | string | `web` | `full` Scanned in full, `web` Web ports only, `skip` Not scanned | Port set for addresses attributed to a CDN or WAF. |
| `scan_cloud` (advanced) | Scan cloud addresses in full | boolean | `true` |  | Scan addresses attributed to a cloud provider with the full port set. |
| `skip_private` (advanced) | Skip private addresses | boolean | `true` |  | Skip loopback, link-local and RFC1918 addresses. An address or netblock named as the target is scanned. |
| `http_on_every_port` (advanced) | HTTP on every open port | boolean | `false` |  | Probe ports classed as non-web services for HTTP as well. |
| `max_addresses` (advanced) | Address budget | integer | `8192` | 1 to 100000 | Stop after this many addresses. |

