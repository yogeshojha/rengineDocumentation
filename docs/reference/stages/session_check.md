---
title: Session Check
description: "Check the scan context's credentials before the scan runs. It sends traffic to your target."
sources:
  - "stages/session_check/stage.py:29"
  - stages/session_check/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 104
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `session_check` |
| Group | Web |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 2 of 8 |
| Depends on | [Seed Resolution](seed_resolution.md) |
| Input | None |
| Output | None |
| Adds results to | None |
| Tools | None |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: Nothing. The verdict is the stage's own status and note.

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Check the session before scanning | boolean | `true` |  | Request the target once with the scan context's credentials and once without. Runs only when the context carries credentials. |

