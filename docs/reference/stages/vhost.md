---
title: Virtual Host Discovery
description: "Find virtual hosts that DNS does not resolve, by varying the Host header. It sends traffic to your target."
sources:
  - "stages/vhost/stage.py:36"
  - stages/vhost/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 312
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `vhost` |
| Group | Hosts |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 4 of 8 |
| Depends on | [Reverse DNS](reverse_dns.md), [Subdomain Discovery](subdomain_discovery.md) |
| Input | `hosts` |
| Output | `hosts` |
| Adds results to | [Web assets](../query/web-assets.md) |
| Tools | `ffuf` |
| API keys | None |
| Target types | Domain |
| On by default | No |
| In the Default engine | No |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: Subdomain rows for virtual hosts that answered.

## Request rate

The stage runs `ffuf` with a timeout of 8 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 150 | 40 |
| Normal | 150 | 40 |
| Aggressive | 400 | 80 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Virtual host bruteforce | boolean | `false` |  | Find virtual hosts that DNS does not resolve, by varying the Host header. |
| `wordlist` | Wordlist | string | `common-vhosts` | At most 64 characters | List of host names to try. Custom lists are uploaded in the Arsenal. |

