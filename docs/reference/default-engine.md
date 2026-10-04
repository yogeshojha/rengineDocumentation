---
title: Default scan engine
description: "The Default engine is the scan engine built into reNgine. Use this page to see what it runs on each type of target, and the YAML behind it."
sources:
  - shared/definitions/default_engine.py
  - api/app/services/scan_engine/service.py
  - stages/presets.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json` and `data/default-engine.yaml`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Its name, description and intensity, and how it differs from the catalog defaults.

| Property | Value |
|---|---|
| Name | Default |
| Description | Subdomain discovery on subfinder and crt.name, HTTP probe, screenshots, response mining and a nuclei vulnerability scan at Normal intensity. |
| Intensity | Normal |
| Built in | Yes |
| Changes from the catalog defaults | `vulnerability_scan` enabled |

The engine runs every stage that is on by default, plus the vulnerability scan. The port scan is off.

## Stages per target type

What a run of the Default engine does on each type of target, at Normal intensity. Use it to find out why a stage did not run on your target.

| Stage | Domain | URL | IP address | CIDR range | ASN |
|---|---|---|---|---|---|
| [Seed Assets](stages/asset_seed.md) | Off | Off | Off | Off | Off |
| [Seed Resolution](stages/seed_resolution.md) | Not applicable | Runs | Runs | Runs | Runs |
| [Subdomain Discovery](stages/subdomain_discovery.md) | Runs | Not applicable | Not applicable | Not applicable | Not applicable |
| [Target Enrichment](stages/target_enrichment.md) | Runs | Runs | Runs | Runs | Runs |
| [Host Discovery](stages/host_discovery.md) | Not applicable | Not applicable | Not applicable | Runs | Runs |
| [Session Check](stages/session_check.md) | Runs | Runs | Runs | Runs | Runs |
| [Subdomain Takeover](stages/takeover.md) | Runs | Runs | No input | No input | No input |
| [Zone Transfer](stages/zone_transfer.md) | Runs | Runs | No input | No input | No input |
| [CDN and Cloud Attribution](stages/cdn_check.md) | Runs | Runs | Runs | Runs | Runs |
| [Netblock Sweep](stages/netblock_sweep.md) | Runs | Not applicable | Not applicable | Not applicable | Not applicable |
| [Passive Port Discovery](stages/passive_ports.md) | Runs | Runs | Runs | Runs | Runs |
| [Reverse DNS](stages/reverse_dns.md) | Runs | Runs | Runs | Runs | Runs |
| [Port Scan](stages/port_scan.md) | Off | Off | Off | Off | Off |
| [Virtual Host Discovery](stages/vhost.md) | Off | Off | Off | Off | Off |
| [HTTP Probe](stages/http_probe.md) | Runs | Runs | Runs | Runs | Runs |
| [Broken Link Hijacking](stages/broken_links.md) | Runs | Runs | Runs | Runs | Runs |
| [Content Discovery](stages/content_discovery.md) | Off | Off | Off | Off | Off |
| [Origin Probe](stages/origin_probe.md) | Runs | Runs | Runs | Runs | Runs |
| [Service Fingerprint](stages/service_fingerprint.md) | Runs | Runs | Runs | Runs | Runs |
| [URL Discovery](stages/url_discovery.md) | Runs | Runs | Runs | Runs | Runs |
| [WAF Detection](stages/waf_detect.md) | Runs | Runs | Runs | Runs | Runs |
| [AI Detection](stages/ai_detection.md) | Runs | Runs | Runs | Runs | Runs |
| [Domain posture](stages/dns_posture.md) | Runs | Runs | Not applicable | Not applicable | Not applicable |
| [Endpoint Verification](stages/endpoint_probe.md) | Runs | Runs | Runs | Runs | Runs |
| [IP Enrichment](stages/ip_enrichment.md) | Runs | Runs | Runs | Runs | Runs |
| [Lookalike domains](stages/lookalike_domains.md) | Runs | Runs | Not applicable | Not applicable | Not applicable |
| [Hostname Ownership](stages/name_ownership.md) | Runs | Not applicable | Not applicable | Not applicable | Not applicable |
| [Screenshots](stages/screenshot.md) | Runs | Runs | Runs | Runs | Runs |
| [Vulnerability Scan](stages/vulnerability_scan.md) | Runs | Runs | Runs | Runs | Runs |
| [Fuzzing](stages/dast_scan.md) | Off | Off | Off | Off | Off |
| [Response secret mining](stages/secret_mining.md) | Runs | Runs | Runs | Runs | Runs |

**Off** means the engine does not enable the stage. **Not applicable** means the stage does not work on this type of target. **No input** means no earlier stage produces what this stage needs.

## Engine YAML

The YAML the engine editor exports for the Default engine. Use it as a starting point when you write your own engine.

```yaml
name: Default
description: Subdomain discovery on subfinder and crt.name, HTTP probe, screenshots,
  response mining and a nuclei vulnerability scan at Normal intensity.
intensity: normal
global_headers: []
stages:
  lookalike_domains:
    enabled: true
    tld_swap: true
    page_similarity: true
    registration: true
    words:
    - login
    - secure
    - account
    - support
    - portal
    - verify
    - auth
    - sso
    - mail
    - online
  seed_resolution:
    enabled: true
    asn_scan_mode: smart
  target_enrichment:
    enabled: true
  session_check:
    enabled: true
  netblock_sweep:
    enabled: true
    max_sweep: 8192
  reverse_dns:
    enabled: true
  subdomain_discovery:
    enabled: true
    passive_tools:
    - subfinder
    - crtname
    tls_discovery: true
    zone_transfer: false
    bruteforce: false
    wordlist: common-subdomains
    wordlist_limit: 1000
    permutations: false
    skip_address_names: true
  host_discovery:
    enabled: true
  cdn_check:
    enabled: true
  passive_ports:
    enabled: true
  port_scan:
    enabled: false
    profile: exposure
    ports: ''
    exclude_ports: ''
    scan_type: connect
    cdn_policy: web
    scan_cloud: true
    skip_private: true
    http_on_every_port: false
    max_addresses: 8192
  vhost:
    enabled: false
    wordlist: common-vhosts
  http_probe:
    enabled: true
  origin_probe:
    enabled: true
    max_addresses: 2048
  service_fingerprint:
    enabled: true
    max_services: 2000
  waf_detect:
    enabled: true
  screenshot:
    enabled: true
    max_screenshots: 0
  dns_posture:
    enabled: true
    dkim_selectors:
    - default
    - google
    - selector1
    - selector2
    - k1
    - k2
    - s1
    - s2
    - dkim
    - mail
    - smtp
    - mandrill
    - mailjet
    - sendgrid
    - zendesk1
    - amazonses
    - pm
    - protonmail
    - mimecast20190108
    - fm1
  takeover:
    enabled: true
  zone_transfer:
    enabled: true
  ai_detection:
    enabled: true
    mcp_paths: true
    max_minutes: 30
    max_assets: 5000
  broken_links:
    enabled: true
  content_discovery:
    enabled: false
    wordlist: common-content
    wordlist_limit: 1000
    max_minutes: 20
    max_hosts: 25
  url_discovery:
    enabled: true
    providers:
    - response_mining
    crawl_depth: 3
    headless: false
    max_crawl_minutes: 20
    crawl_scope: rdn
    max_hosts: 500
    drop_noise: true
    static_extensions:
    - png
    - jpg
    - jpeg
    - gif
    - svg
    - webp
    - avif
    - bmp
    - ico
    - tif
    - tiff
    - css
    - scss
    - less
    - map
    - woff
    - woff2
    - ttf
    - eot
    - otf
    - mp4
    - webm
    - mov
    - avi
    - mp3
    - wav
    - ogg
    - m4a
    - flac
    ignored_params:
    - utm_source
    - utm_medium
    - utm_campaign
    - utm_term
    - utm_content
    - utm_id
    - fbclid
    - gclid
    - dclid
    - msclkid
    - yclid
    - mc_cid
    - mc_eid
    - _ga
    - _gl
    - _hsenc
    - _hsmi
    - ref
    - v
    - ver
    - version
    - _
    - cb
    - cache
    - nocache
    - rand
    - random
    - t
    - ts
    - timestamp
    - hash
    - rev
    - build
    - itok
    - cachebuster
    keep_per_family: 3
    sibling_cap: 12
  endpoint_probe:
    enabled: true
    skip_static: true
    max_urls: 0
  ip_enrichment:
    enabled: true
  name_ownership:
    enabled: true
  vulnerability_scan:
    enabled: true
    severities:
    - critical
    - high
    - medium
    - low
    template_sets:
    - kev
    - cve
    - panel
    - exposure
    - misconfiguration
    - default-login
    - takeover
    - injection
    custom_templates: []
    surface: web
    headless: false
    max_minutes: 0
    scanners:
    - nuclei
    include_tags: []
    exclude_tags: []
    exclude_templates: []
    template_ids: []
    blind_sweep: true
    max_targets: 0
    interactsh: true
    store_evidence: true
  dast_scan:
    enabled: false
    scanners:
    - nuclei
    severities:
    - critical
    - high
    - medium
    - low
    directories: false
    headless: false
    max_minutes: 30
    max_requests_per_origin: 50
    max_requests: 1500
  secret_mining:
    enabled: true
transport_overrides: {}
tool_options: {}
```
