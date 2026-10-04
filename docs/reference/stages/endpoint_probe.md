---
title: Endpoint Verification
description: Request the discovered URLs and record each status. It sends traffic to your target.
sources:
  - "stages/endpoint_probe/stage.py:65"
  - stages/endpoint_probe/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 625
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `endpoint_probe` |
| Group | Endpoints |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 7 of 8 |
| Depends on | [URL Discovery](url_discovery.md) |
| Input | `endpoints` |
| Output | None |
| Adds results to | [Endpoints](../query/endpoints.md) |
| Tools | `httpx` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: Status, content type, length, title, hash, tech and stored response on Endpoint rows. One EndpointCoverage row.

## Request rate

The stage runs `httpx` with a timeout of 10 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 150 | 40 |
| Normal | 150 | 40 |
| Aggressive | 400 | 80 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Verify endpoints | boolean | `true` |  | Request the discovered URLs and record each status. |
| `skip_static` (advanced) | Skip images and media | boolean | `true` |  | Skip images, stylesheets, fonts and other static files. |
| `max_urls` (advanced) | URLs to verify | integer | `0` | 0 to 100000 | Most endpoints to request, best first. 0 fits the list to 30 minutes at the scan's rate. |

