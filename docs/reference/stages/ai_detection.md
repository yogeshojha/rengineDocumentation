---
title: AI Detection
description: "Identify model servers, AI gateways, AI applications and MCP servers on every web asset. It sends traffic to your target."
sources:
  - "stages/ai_detection/stage.py:76"
  - stages/ai_detection/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 621
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `ai_detection` |
| Group | Analysis |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 7 of 8 |
| Depends on | [HTTP Probe](http_probe.md) |
| Input | `http_assets` |
| Output | None |
| Adds results to | [Web assets](../query/web-assets.md) |
| Tools | `julius` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: AI service verdicts on HttpAsset rows, folded onto host rows.

## Request rate

The stage runs `julius` with a timeout of 5 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 150 | 20 |
| Normal | 150 | 20 |
| Aggressive | 400 | 40 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | AI detection | boolean | `true` |  | Identify model servers, AI gateways, AI applications and MCP servers on every web asset. About 55 requests per web asset. |
| `mcp_paths` | MCP paths | boolean | `true` |  | Send an MCP handshake to /mcp and /api/mcp on every web asset. |
| `max_minutes` | Time budget (min) | integer | `30` | 1 to 480 | Stop starting batches after this many minutes. Web assets not reached are reported. |
| `max_assets` (advanced) | Web asset budget | integer | `5000` | 1 to 100000 | Stop after this many web assets. Non-standard ports are probed first. |

