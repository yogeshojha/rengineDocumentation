---
title: Target Enrichment
description: "Resolve the target and attach DNS, WHOIS and BGP context. It sends no traffic to your target."
sources:
  - "stages/target_enrichment/stage.py:36"
  - stages/target_enrichment/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 3
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag passive">Passive</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `target_enrichment` |
| Group | Hosts |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 1 of 8 |
| Depends on | None |
| Input | None |
| Output | None |
| Adds results to | None |
| Tools | `dnsx`, `whois` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | No |
| At passive intensity | Runs unchanged |

What it stores in the database: The target's DNS lookup, WHOIS record and BGP summary. Not a surface dimension.

## Request rate

The stage runs `dnsx` with a timeout of 5 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | Not limited | 30 |
| Normal | Not limited | 30 |
| Aggressive | Not limited | 50 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Target enrichment | boolean | `true` |  | Resolve the target and attach DNS, WHOIS and BGP context. |

