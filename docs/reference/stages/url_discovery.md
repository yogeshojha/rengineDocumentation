---
title: URL Discovery
description: Collect the URLs and paths that exist on every live web asset. It sends traffic to your target.
sources:
  - "stages/url_discovery/stage.py:60"
  - stages/url_discovery/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 524
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `url_discovery` |
| Group | Endpoints |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 6 of 8 |
| Depends on | [HTTP Probe](http_probe.md) |
| Input | `http_assets` |
| Output | `endpoints` |
| Adds results to | [Endpoints](../query/endpoints.md) |
| Tools | `katana`, `urlfinder` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Runs, but skips what sends traffic to the target |

What it stores in the database: Endpoint rows per source and one EndpointCoverage row per source.

What changes at passive intensity: Sources with touches_target (sitemap, crawl, js, api_spec) are skipped with 'This source sends requests to the target. A passive scan does not run it.' response_mining and archive stay.

## Request rate

The stage runs `katana` with a timeout of 15 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 150 | 50 |
| Normal | 150 | 50 |
| Aggressive | 300 | 100 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Discover URLs | boolean | `true` |  | Collect the URLs and paths that exist on every live web asset. |
| `providers` | Sources | array | `response_mining` | `response_mining` Response mining, `sitemap` robots.txt and sitemaps, `crawl` Crawl, `archive` Public archives, `js` Source maps, `api_spec` API schemas | Sources URLs are collected from. Response mining reads stored response bodies and sends no request. |
| `crawl_depth` | Crawl depth | integer | `3` | 1 to 10 | Link depth followed from each site root. |
| `headless` | Use a browser | boolean | `false` |  | Render each page in a browser before reading links. Slower. |
| `max_crawl_minutes` | Crawl budget (min) | integer | `20` | 0 to 600 | Stop crawling after this long. 0 means no limit. |
| `crawl_scope` (advanced) | Crawl scope | string | `rdn` | `dn` Same domain name, `rdn` Same registrable domain and its subdomains, `fqdn` Only the exact hostname | Which hosts the crawler may follow links to. |
| `max_hosts` (advanced) | Web asset cap | integer | `500` | 1 to 10000 | Live web assets handed to each source. |
| `drop_noise` (advanced) | Drop noise | boolean | `true` |  | Static files, crawler artifacts, platform noise and URLs past the family and sibling caps are not stored. |
| `static_extensions` (advanced) | Static extensions | array | `png`, `jpg`, `jpeg`, `gif`, `svg`, `webp`, `avif`, `bmp`, `ico`, `tif`, `tiff`, `css`, and 17 more | At most 200 items | File extensions dropped as static. |
| `ignored_params` (advanced) | Ignored parameters | array | `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `utm_id`, `fbclid`, `gclid`, `dclid`, `msclkid`, `yclid`, `mc_cid`, and 23 more | At most 400 items | Query parameters removed from every URL. Tracking and cache-busting names by default. |
| `keep_per_family` (advanced) | URLs kept per family | integer | `3` | 1 to 100 | URLs stored for one path shape and parameter set. The rest are dropped. |
| `sibling_cap` (advanced) | Sibling cap | integer | `12` | 1 to 1000 | Children of one folder, of one kind, stored before the rest are dropped. |

