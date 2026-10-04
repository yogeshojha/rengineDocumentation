---
title: Response secret mining
description: "Credentials, tokens, keys and contacts read from stored responses. No request is sent. It sends no traffic to your target."
sources:
  - "stages/secret_mining/stage.py:17"
  - stages/secret_mining/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 730
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag passive">Passive</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `secret_mining` |
| Group | Analysis |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 8 of 8 |
| Depends on | [Endpoint Verification](endpoint_probe.md), [HTTP Probe](http_probe.md) |
| Input | `endpoints`, `http_assets` |
| Output | `secrets` |
| Adds results to | [Secrets](../query/secrets.md) |
| Tools | None |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | No |
| At passive intensity | Runs unchanged |

What it stores in the database: Secret rows read from stored responses.

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Response secret mining | boolean | `true` |  | Credentials, tokens, keys and contacts read from stored responses. No request is sent. |

