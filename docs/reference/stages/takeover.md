---
title: Subdomain Takeover
description: Report hostnames whose CNAME points at a hosting provider but resolves nowhere. It sends no traffic to your target.
sources:
  - "stages/takeover/stage.py:77"
  - stages/takeover/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 119
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag passive">Passive</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `takeover` |
| Group | Hosts |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 2 of 8 |
| Depends on | [Seed Resolution](seed_resolution.md), [Subdomain Discovery](subdomain_discovery.md) |
| Input | `hosts` |
| Output | `vulnerabilities` |
| Adds results to | [Vulnerabilities](../query/vulnerabilities.md) |
| Tools | None |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | No |
| At passive intensity | Runs unchanged |
| Findings | Reported as findings of [Vulnerability Scan](vulnerability_scan.md), severities <span class="rn-sev medium">medium</span> |

What it stores in the database: Findings with template rengine-dangling-cname, severity medium.

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Check for takeover | boolean | `true` |  | Report hostnames whose CNAME points at a provider but resolves nowhere. |

