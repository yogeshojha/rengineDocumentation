---
title: Stages
description: "Stages are the steps of a scan. Use this page to see what each one does, which tools it runs, and whether it sends traffic to your target."
sources:
  - stages/registry.py
  - stages/base.py
  - stages/config.py
  - stages/presets.py
  - shared/definitions/launch.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

reNgine has 31 stages. When you start a scan, reNgine runs the enabled stages in 8 steps. The stages of one step run in parallel, and the next step starts when every stage of the step has settled. A stage always runs after the stages it depends on. A deferrable stage that no other stage depends on runs in a later step.

<span class="rn-tag passive">Passive</span> marks a stage that sends no traffic to your target, and <span class="rn-tag active">Active</span> a stage that does. Check these tags before you scan a target that you must not touch.

Further down you find the intensity profiles, the presets for new scan engines, the port profiles, the built-in wordlists and the limits of focused rescans.

## Execution steps

The order in which reNgine runs the stages. The stages in one row run at the same time.

| Step | Stages |
|---|---|
| 1 | [Seed Assets](asset_seed.md) <span class="rn-tag passive">Passive</span>, [Seed Resolution](seed_resolution.md) <span class="rn-tag passive">Passive</span>, [Subdomain Discovery](subdomain_discovery.md) <span class="rn-tag active">Active</span>, [Target Enrichment](target_enrichment.md) <span class="rn-tag passive">Passive</span> |
| 2 | [Host Discovery](host_discovery.md) <span class="rn-tag active">Active</span>, [Session Check](session_check.md) <span class="rn-tag active">Active</span>, [Subdomain Takeover](takeover.md) <span class="rn-tag passive">Passive</span>, [Zone Transfer](zone_transfer.md) <span class="rn-tag passive">Passive</span> |
| 3 | [CDN and Cloud Attribution](cdn_check.md) <span class="rn-tag passive">Passive</span>, [Netblock Sweep](netblock_sweep.md) <span class="rn-tag passive">Passive</span>, [Passive Port Discovery](passive_ports.md) <span class="rn-tag passive">Passive</span>, [Reverse DNS](reverse_dns.md) <span class="rn-tag passive">Passive</span> |
| 4 | [Port Scan](port_scan.md) <span class="rn-tag active">Active</span>, [Virtual Host Discovery](vhost.md) <span class="rn-tag active">Active</span> |
| 5 | [HTTP Probe](http_probe.md) <span class="rn-tag active">Active</span> |
| 6 | [Broken Link Hijacking](broken_links.md) <span class="rn-tag passive">Passive</span>, [Content Discovery](content_discovery.md) <span class="rn-tag active">Active</span>, [Origin Probe](origin_probe.md) <span class="rn-tag active">Active</span>, [Service Fingerprint](service_fingerprint.md) <span class="rn-tag active">Active</span>, [URL Discovery](url_discovery.md) <span class="rn-tag active">Active</span>, [WAF Detection](waf_detect.md) <span class="rn-tag active">Active</span> |
| 7 | [AI Detection](ai_detection.md) <span class="rn-tag active">Active</span>, [Domain posture](dns_posture.md) <span class="rn-tag active">Active</span>, [Endpoint Verification](endpoint_probe.md) <span class="rn-tag active">Active</span>, [IP Enrichment](ip_enrichment.md) <span class="rn-tag passive">Passive</span>, [Lookalike domains](lookalike_domains.md) <span class="rn-tag active">Active</span>, [Hostname Ownership](name_ownership.md) <span class="rn-tag passive">Passive</span>, [Screenshots](screenshot.md) <span class="rn-tag active">Active</span>, [Vulnerability Scan](vulnerability_scan.md) <span class="rn-tag active">Active</span> |
| 8 | [Fuzzing](dast_scan.md) <span class="rn-tag active">Active</span>, [Response secret mining](secret_mining.md) <span class="rn-tag passive">Passive</span> |

## All stages

Every stage, with the key you use in the engine YAML, whether it sends traffic, and what it does at passive intensity.

| Stage | Key | Group | Role | Reach | Passive intensity | Default |
|---|---|---|---|---|---|---|
| [Seed Assets](asset_seed.md) | `asset_seed` | Hosts | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | No |
| [Seed Resolution](seed_resolution.md) | `seed_resolution` | Addresses | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [Subdomain Discovery](subdomain_discovery.md) | `subdomain_discovery` | Hosts | capability | <span class="rn-tag active">Active</span> | Runs in part | Yes |
| [Target Enrichment](target_enrichment.md) | `target_enrichment` | Hosts | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [Host Discovery](host_discovery.md) | `host_discovery` | Addresses | capability | <span class="rn-tag active">Active</span> | Skipped | Yes |
| [Session Check](session_check.md) | `session_check` | Web | support | <span class="rn-tag active">Active</span> | Skipped | Yes |
| [Subdomain Takeover](takeover.md) | `takeover` | Hosts | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [Zone Transfer](zone_transfer.md) | `zone_transfer` | Hosts | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [CDN and Cloud Attribution](cdn_check.md) | `cdn_check` | Addresses | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [Netblock Sweep](netblock_sweep.md) | `netblock_sweep` | Hosts | capability | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [Passive Port Discovery](passive_ports.md) | `passive_ports` | Services | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [Reverse DNS](reverse_dns.md) | `reverse_dns` | Addresses | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [Port Scan](port_scan.md) | `port_scan` | Services | capability | <span class="rn-tag active">Active</span> | Skipped | No |
| [Virtual Host Discovery](vhost.md) | `vhost` | Hosts | capability | <span class="rn-tag active">Active</span> | Skipped | No |
| [HTTP Probe](http_probe.md) | `http_probe` | Web | support | <span class="rn-tag active">Active</span> | Skipped | Yes |
| [Broken Link Hijacking](broken_links.md) | `broken_links` | Hosts | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [Content Discovery](content_discovery.md) | `content_discovery` | Endpoints | capability | <span class="rn-tag active">Active</span> | Skipped | No |
| [Origin Probe](origin_probe.md) | `origin_probe` | Services | support | <span class="rn-tag active">Active</span> | Skipped | Yes |
| [Service Fingerprint](service_fingerprint.md) | `service_fingerprint` | Services | support | <span class="rn-tag active">Active</span> | Skipped | Yes |
| [URL Discovery](url_discovery.md) | `url_discovery` | Endpoints | capability | <span class="rn-tag active">Active</span> | Runs in part | Yes |
| [WAF Detection](waf_detect.md) | `waf_detect` | Web | support | <span class="rn-tag active">Active</span> | Skipped | Yes |
| [AI Detection](ai_detection.md) | `ai_detection` | Analysis | capability | <span class="rn-tag active">Active</span> | Skipped | Yes |
| [Domain posture](dns_posture.md) | `dns_posture` | Hosts | support | <span class="rn-tag active">Active</span> | Runs in part | Yes |
| [Endpoint Verification](endpoint_probe.md) | `endpoint_probe` | Endpoints | support | <span class="rn-tag active">Active</span> | Skipped | Yes |
| [IP Enrichment](ip_enrichment.md) | `ip_enrichment` | Addresses | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [Lookalike domains](lookalike_domains.md) | `lookalike_domains` | Analysis | capability | <span class="rn-tag active">Active</span> | Runs in part | Yes |
| [Hostname Ownership](name_ownership.md) | `name_ownership` | Hosts | support | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |
| [Screenshots](screenshot.md) | `screenshot` | Web | capability | <span class="rn-tag active">Active</span> | Skipped | Yes |
| [Vulnerability Scan](vulnerability_scan.md) | `vulnerability_scan` | Vulnerabilities | capability | <span class="rn-tag active">Active</span> | Skipped | No |
| [Fuzzing](dast_scan.md) | `dast_scan` | Vulnerabilities | capability | <span class="rn-tag active">Active</span> | Skipped | No |
| [Response secret mining](secret_mining.md) | `secret_mining` | Analysis | capability | <span class="rn-tag passive">Passive</span> | Runs unchanged | Yes |

**Role** tells you how a stage gets into a run. You select a capability stage in a scan engine or a custom scan. A support stage runs when a stage you selected needs what it produces, or when its own input is available. An always-on stage is added as soon as any stage is selected. **Runs in part** means the stage runs but skips what sends traffic to the target. **Default** shows whether the stage is on in the catalog defaults.

## Intensity

Intensity decides how hard reNgine hits your target. Use Passive when you must not send any traffic, Normal for most scans, and Aggressive when you own the target and want results faster. This is the text the interface shows for each choice.

| Intensity | Interface text |
|---|---|
| Passive | Findings come from public sources only. No request reaches the target. |
| Normal | 150 requests a second per tool. 1,000 packets a second for the port scan. |
| Aggressive | 400 requests a second per tool. 3,000 packets a second for the port scan, and higher concurrency. |
| Custom | Rates and concurrency set per tool. An empty value uses the preset. |

### Profiles

Each cell shows the rate per second and the number of threads a tool uses at that intensity. Passive and Normal share one transport profile. At Passive intensity, the stages that send traffic do not run.

| Tool | Passive | Normal | Aggressive | Timeout |
|---|---|---|---|---|
| `httpx` | 150 / 150 | 150 / 150 | 400 / 300 | 10 s |
| `naabu` | 1000 / 100 | 1000 / 100 | 3000 / 200 | 3 s |
| `nuclei` | 150 / 25 | 150 / 25 | 400 / 50 | 10 s |
| `katana` | 150 / 50 | 150 / 50 | 300 / 100 | 15 s |
| `ffuf` | 150 / 40 | 150 / 40 | 400 / 80 | 8 s |
| `julius` | 150 / 20 | 150 / 20 | 400 / 40 | 5 s |
| `dnsx` | not limited / 30 | not limited / 30 | not limited / 50 | 5 s |
| `banner` | not limited / 32 | not limited / 32 | not limited / 64 | 4 s |

With a custom transport you can set a rate of up to 10,000 a second, up to 1,000 threads and a timeout of up to 3,600 seconds.

### Stages at passive intensity

What still runs when you choose Passive.

| Behaviour | Stages |
|---|---|
| Skipped | [AI Detection](ai_detection.md), [Content Discovery](content_discovery.md), [Fuzzing](dast_scan.md), [Endpoint Verification](endpoint_probe.md), [Host Discovery](host_discovery.md), [HTTP Probe](http_probe.md), [Origin Probe](origin_probe.md), [Port Scan](port_scan.md), [Screenshots](screenshot.md), [Service Fingerprint](service_fingerprint.md), [Session Check](session_check.md), [Virtual Host Discovery](vhost.md), [Vulnerability Scan](vulnerability_scan.md), [WAF Detection](waf_detect.md) |
| Run in part, skipping what sends traffic to the target | [Domain posture](dns_posture.md), [Lookalike domains](lookalike_domains.md), [Subdomain Discovery](subdomain_discovery.md), [URL Discovery](url_discovery.md) |
| Run unchanged | [Seed Assets](asset_seed.md), [Broken Link Hijacking](broken_links.md), [CDN and Cloud Attribution](cdn_check.md), [IP Enrichment](ip_enrichment.md), [Hostname Ownership](name_ownership.md), [Netblock Sweep](netblock_sweep.md), [Passive Port Discovery](passive_ports.md), [Reverse DNS](reverse_dns.md), [Response secret mining](secret_mining.md), [Seed Resolution](seed_resolution.md), [Subdomain Takeover](takeover.md), [Target Enrichment](target_enrichment.md), [Zone Transfer](zone_transfer.md) |

## Presets

When you create a scan engine, you start from a preset: a ready-made stage selection that you can then adjust. You pick it in the new engine dialog. The Passive Recon preset is a stage selection with passive intensity. Passive intensity itself is a separate, run-level switch.

| Preset | Key | Description | Intensity | Changes from the catalog defaults |
|---|---|---|---|---|
| Standard Recon | `standard` | Every stage at its default settings. | Normal | Catalog defaults |
| Passive Recon | `passive` | Only stages that send no traffic to the target. | Passive | `-session_check`, `-host_discovery`, `-origin_probe`, `-service_fingerprint`, `-waf_detect`, `-screenshot`, `-ai_detection`, `-endpoint_probe` |
| Full Sweep | `full` | Every stage enabled. | Normal | `+port_scan`, `+vhost`, `+content_discovery`, `+vulnerability_scan`, `+dast_scan` |
| Blank | `blank` | Always-on stages only. | Normal | `-lookalike_domains`, `-seed_resolution`, `-target_enrichment`, `-session_check`, `-netblock_sweep`, `-reverse_dns`, `-subdomain_discovery`, `-host_discovery`, `-cdn_check`, `-passive_ports`, `-origin_probe`, `-service_fingerprint`, `-waf_detect`, `-screenshot`, `-dns_posture`, `-takeover`, `-zone_transfer`, `-ai_detection`, `-broken_links`, `-url_discovery`, `-endpoint_probe`, `-name_ownership`, `-secret_mining` |

## Port profiles

A port profile is the set of ports that [Port Scan](port_scan.md) checks. Choose it with the `profile` option of the stage.

| Profile | Key | Ports | Description |
|---|---|---|---|
| Web ports | `web` | 119 | Ports that commonly serve HTTP. |
| Web and sensitive | `exposure` | 161 | Web ports plus remote-access and datastore ports. The default. |
| Top 100 | `top-100` | 100 | The 100 most common ports. |
| Top 1000 | `top-1000` | 1,000 | The 1,000 most common ports. |
| All ports | `full` | 65,535 | Every port from 1 to 65535. |
| Custom | `custom` |  | The list or range set on the stage. |

## Wordlists

reNgine ships with these wordlists. [Subdomain Discovery](subdomain_discovery.md), [Virtual Host Discovery](vhost.md) and [Content Discovery](content_discovery.md) use the wordlist of their kind by default. Upload your own in Arsenal when you need other words.

| Wordlist | Key | Kind | Words | Description |
|---|---|---|---|---|
| Common subdomains | `common-subdomains` | subdomain | 4,860 | Names ranked by frequency in public DNS data. A word budget reads from the top. |
| Common virtual hosts | `common-vhosts` | vhost | 103 | Short list of virtual host names. |
| Common paths and files | `common-content` | content | 6,000 | Paths ranked by frequency on real sites, directories first. A word budget reads from the top. |

A custom wordlist can be up to 8 MB, with words of up to 63 characters.

## Focused rescans

A focused rescan runs chosen stages again on assets you pick from completed scans, without discovering the target again. These are its limits.

| Property | Value |
|---|---|
| Stages a rescan can run | [HTTP Probe](http_probe.md), [Port Scan](port_scan.md), [Screenshots](screenshot.md), [Response secret mining](secret_mining.md), [URL Discovery](url_discovery.md), [Virtual Host Discovery](vhost.md), [Vulnerability Scan](vulnerability_scan.md) |
| Assets per rescan | 5,000 |
| Runs per rescan | 25 |
| Checks per rescan | 50 |

When you start a rescan from a dimension, reNgine seeds it with the host or the address of each row and selects these stages by default.

| Dimension | Seed | Default stages |
|---|---|---|
| Web assets | host | [HTTP Probe](http_probe.md) |
| Endpoints | host | [HTTP Probe](http_probe.md), [URL Discovery](url_discovery.md) |
| Services | address | [Port Scan](port_scan.md) |
| IP addresses | address | [Port Scan](port_scan.md) |
| Vulnerabilities | host | [HTTP Probe](http_probe.md), [Vulnerability Scan](vulnerability_scan.md) |
| Secrets | host | [HTTP Probe](http_probe.md), [Response secret mining](secret_mining.md) |

