---
title: Content Discovery
description: Guess common paths and files on every live site. It sends traffic to your target.
sources:
  - "stages/content_discovery/stage.py:41"
  - stages/content_discovery/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 523
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `content_discovery` |
| Group | Endpoints |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 6 of 8 |
| Depends on | [HTTP Probe](http_probe.md) |
| Input | `http_assets` |
| Output | `endpoints` |
| Adds results to | [Endpoints](../query/endpoints.md) |
| Tools | `ffuf` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | No |
| In the Default engine | No |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: Endpoint rows with source fuzz.

## Request rate

The stage runs `ffuf` with a timeout of 8 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 50 | 40 |
| Normal | 50 | 40 |
| Aggressive | 133 | 80 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Guess paths and files | boolean | `false` |  | Request wordlist paths on every live site. One request per word per site. |
| `wordlist` | Wordlist | string | `common-content` | At most 64 characters | List to guess from. Custom lists are uploaded in the Arsenal. |
| `wordlist_limit` | Words to try | integer | `1000` | 50 to 200000 | Words tried per site, from the top of the list. |
| `max_minutes` | Time budget (minutes) | integer | `20` | 1 to 480 | The run stops after this many minutes and reports partial coverage. |
| `max_hosts` (advanced) | Sites to guess against | integer | `25` | 1 to 1000 | Sites tried. Sites that answered are picked first. |

