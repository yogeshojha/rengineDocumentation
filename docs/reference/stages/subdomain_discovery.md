---
title: Subdomain Discovery
description: "Enumerate subdomains from passive sources, certificates, wordlists and permutations. It sends traffic to your target."
sources:
  - "stages/subdomain/stage.py:162"
  - stages/subdomain/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 7
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `subdomain_discovery` |
| Group | Hosts |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 1 of 8 |
| Depends on | None |
| Input | None |
| Output | `addresses`, `hosts` |
| Adds results to | [Web assets](../query/web-assets.md) |
| Tools | `amass`, `assetfinder`, `crtname`, `ctfr`, `github-subdomains`, `netlas`, `subfinder`, `tlsx` |
| API keys | `securitytrails`, `chaos`, `netlas`, `github` (optional) |
| Target types | Domain |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Runs, but skips what sends traffic to the target |

What it stores in the database: Subdomain rows with sources, resolved_ips, cname, is_active, is_wildcard, is_excluded.

What changes at passive intensity: Zone transfer, bruteforce and permutations are skipped with 'a passive scan does not query the target's nameservers'. A source with touches_target (tlsx) is skipped with 'a passive scan does not connect to the target'. Names are still resolved with dnsx.

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
| `enabled` | Subdomain discovery | boolean | `true` |  | Enumerate subdomains from passive sources, certificates, wordlists and permutations. |
| `passive_tools` | Passive sources | array | `subfinder`, `crtname` | `amass`, `assetfinder`, `crtname`, `ctfr`, `github-subdomains`, `netlas`, `subfinder`, `tlsx` | Public sources to query for subdomains. |
| `tls_discovery` | TLS certificate discovery | boolean | `true` |  | Pull subject alternative names from the target's certificates. |
| `zone_transfer` | Attempt zone transfer | boolean | `false` |  | Request the whole zone from each of its nameservers. |
| `bruteforce` | Bruteforce names | boolean | `false` |  | Resolve wordlist names against the target's nameservers. |
| `wordlist` | Wordlist | string | `common-subdomains` | At most 64 characters | List to guess from. Custom lists are uploaded in the Arsenal. |
| `wordlist_limit` | Words to try | integer | `1000` | 100 to 1000000 | Names tried per apex, from the top of the list. |
| `permutations` | Permute discovered names | boolean | `false` |  | Resolve variants of discovered names, such as api-dev and api2. |
| `skip_address_names` (advanced) | Skip address-shaped names | boolean | `true` |  | Names that spell an IP address, such as 10-20-30-40.example.com, are dropped unless a certificate or DNS answer names them. |

