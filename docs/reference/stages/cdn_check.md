---
title: CDN and Cloud Attribution
description: "Identify which addresses are fronted by a CDN, WAF or cloud provider. It sends no traffic to your target."
sources:
  - "stages/cdn_check/stage.py:21"
  - stages/cdn_check/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 209
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag passive">Passive</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `cdn_check` |
| Group | Addresses |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 3 of 8 |
| Depends on | [Host Discovery](host_discovery.md), [Seed Resolution](seed_resolution.md), [Subdomain Discovery](subdomain_discovery.md) |
| Input | `addresses` |
| Output | None |
| Adds results to | [IP addresses](../query/ips.md) |
| Tools | `cdncheck` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | No |
| At passive intensity | Runs unchanged |

What it stores in the database: IpAddress rows for every known address, with cdn_type, cdn_name and is_cdn.

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Attribute CDN and cloud providers | boolean | `true` |  | Identify which addresses are fronted by a CDN, WAF or cloud provider. |

