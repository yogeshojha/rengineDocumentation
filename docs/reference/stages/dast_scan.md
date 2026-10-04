---
title: Fuzzing
description: Send payloads to the parameters and directories this scan discovered. It sends traffic to your target.
sources:
  - "stages/dast_scan/stage.py:29"
  - stages/dast_scan/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 729
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `dast_scan` |
| Group | Vulnerabilities |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 8 of 8 |
| Depends on | [Endpoint Verification](endpoint_probe.md), [Vulnerability Scan](vulnerability_scan.md), [WAF Detection](waf_detect.md) |
| Input | `endpoints`, `http_assets` |
| Output | `vulnerabilities` |
| Adds results to | [Vulnerabilities](../query/vulnerabilities.md) |
| Tools | `nuclei`, `dalfox`, `httpx` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | No |
| In the Default engine | No |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: Vulnerability rows, VulnerabilityCoverage rows and scan surface items of class request and base.

## Request rate

The stage runs `nuclei` with a timeout of 10 s and 1 retry. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 50 | 25 |
| Normal | 50 | 25 |
| Aggressive | 133 | 50 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Fuzz discovered requests | boolean | `false` |  | Send payloads to the parameters this scan discovered. |
| `scanners` | Fuzzers | array | `nuclei` | `nuclei` Nuclei, `dalfox` Dalfox | Tools that fuzz a request. |
| `severities` | Severities | array | `critical`, `high`, `medium`, `low` | `critical` Critical, `high` High, `medium` Medium, `low` Low, `info` Info, `unknown` Unknown | Severities to run. |
| `directories` | Directory exposure checks | boolean | `false` |  | Run the exposure checks under each discovered directory. |
| `headless` | Browser fuzzing | boolean | `false` |  | Run the fuzzing checks that need a rendered page. Most DAST checks do. |
| `max_minutes` | Time budget (min) | integer | `30` | 0 to 1440 | Stop starting batches after this many minutes. 0 runs until the system time limit. |
| `max_requests_per_origin` (advanced) | Requests per origin | integer | `50` | 1 to 1000 | Parameter sets fuzzed per origin at most. |
| `max_requests` (advanced) | Request budget | integer | `1500` | 1 to 20000 | Parameter sets fuzzed in one scan at most. |

