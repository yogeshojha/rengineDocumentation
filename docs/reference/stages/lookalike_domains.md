---
title: Lookalike domains
description: "Registered typo, homoglyph and TLD variants of the target's domain. It sends traffic to your target."
sources:
  - "stages/lookalike_domains/stage.py:143"
  - stages/lookalike_domains/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 601
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `lookalike_domains` |
| Group | Analysis |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 7 of 8 |
| Depends on | None |
| Input | None |
| Output | None |
| Adds results to | None |
| Tools | `dnsx` |
| API keys | None |
| Target types | Domain, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Runs, but skips what sends traffic to the target |

What it stores in the database: Lookalike rows for the target apex (lookalikes table). Not a surface dimension.

What changes at passive intensity: Lookalike pages are not fetched, whatever page_similarity says. DNS lookups and RDAP run.

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
| `enabled` | Lookalike domains | boolean | `true` |  | Registered typo, homoglyph and TLD variants of the target's domain. |
| `tld_swap` | Other TLDs | boolean | `true` |  | Check the same name under common TLDs. |
| `page_similarity` | Page comparison | boolean | `true` |  | Fetch each lookalike's page and compare it to the target's. |
| `registration` | Registration date | boolean | `true` |  | Read the registrar and creation date over RDAP. |
| `words` (advanced) | Words | array | `login`, `secure`, `account`, `support`, `portal`, `verify`, `auth`, `sso`, `mail`, `online` | At most 50 items | Words joined to the name: login-example.com, examplelogin.com. |

