---
title: IP Enrichment
description: "Resolve ASN, network operator and country for every IP address the scan found. It sends no traffic to your target."
sources:
  - "stages/ip_enrichment/stage.py:50"
  - stages/ip_enrichment/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 626
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag passive">Passive</span> <span class="rn-tag neutral">support</span> <span class="rn-tag neutral">always on</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `ip_enrichment` |
| Group | Addresses |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 7 of 8 |
| Depends on | [Origin Probe](origin_probe.md), [Passive Port Discovery](passive_ports.md), [Reverse DNS](reverse_dns.md), [Service Fingerprint](service_fingerprint.md) |
| Input | None |
| Output | None |
| Adds results to | [IP addresses](../query/ips.md) |
| Tools | None |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | No |
| At passive intensity | Runs unchanged |

What it stores in the database: IpAddress rows for every address the scan found, with ASN, operator and country.

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Enrich IPs | boolean | `true` |  | Resolve ASN, network operator and country for every IP address. |

