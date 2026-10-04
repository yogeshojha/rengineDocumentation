---
title: Pinned tool versions
description: "The exact version of every scanning tool, runtime and base image in reNgine 3.0.0. Use it to find out which version of a tool ran your scan, or to check a tool against a known issue."
sources:
  - worker/Dockerfile
  - api/Dockerfile
  - frontend/Dockerfile
  - docker-compose.prod.yml
revised: 2026-10-03
generated: scripts/gen_ops.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_ops.py` writes it from `data/repo.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Each version is pinned in a Dockerfile or in the compose file, so every install of 3.0.0 runs the same scanning tools.

## Scanning tools

The scanning tools in the worker image, each built or installed at the version below.

| Tool | Version | Source | Pinned in |
|---|---|---|---|
| `dnsx` | `v1.3.1` | `github.com/projectdiscovery/dnsx/cmd/dnsx` | worker/Dockerfile |
| `subfinder` | `v2.16.0` | `github.com/projectdiscovery/subfinder/v2/cmd/subfinder` | worker/Dockerfile |
| `tlsx` | `v1.4.0` | `github.com/projectdiscovery/tlsx/cmd/tlsx` | worker/Dockerfile |
| `alterx` | `v0.1.0` | `github.com/projectdiscovery/alterx/cmd/alterx` | worker/Dockerfile |
| `assetfinder` | `v0.1.1` | `github.com/tomnomnom/assetfinder` | worker/Dockerfile |
| `github-subdomains` | `v1.2.2` | `github.com/gwen001/github-subdomains` | worker/Dockerfile |
| `amass` | `v4.2.0` | `github.com/owasp-amass/amass/v4/...` | worker/Dockerfile |
| `naabu` | `v2.6.1` | `github.com/projectdiscovery/naabu/v2/cmd/naabu` | worker/Dockerfile |
| `httpx` | `v1.12.0` | `github.com/projectdiscovery/httpx/cmd/httpx` | worker/Dockerfile |
| `cdncheck` | `v1.3.0` | `github.com/projectdiscovery/cdncheck/cmd/cdncheck` | worker/Dockerfile |
| `ffuf` | `v2.3.0` | `github.com/ffuf/ffuf/v2` | worker/Dockerfile |
| `katana` | `v1.7.0` | `github.com/projectdiscovery/katana/cmd/katana` | worker/Dockerfile |
| `urlfinder` | `v0.0.3` | `github.com/projectdiscovery/urlfinder/cmd/urlfinder` | worker/Dockerfile |
| `nuclei` | `v3.11.1` | `github.com/projectdiscovery/nuclei/v3/cmd/nuclei` | worker/Dockerfile |
| `certspotter` | `v0.24.2` | `software.sslmate.com/src/certspotter/cmd/certspotter` | worker/Dockerfile |
| `dalfox` | `v3.2.2` | release binary | worker/Dockerfile |
| `julius` | `v1.4.19` | release binary | worker/Dockerfile |
| `wafw00f` | `2.4.2` | PyPI | worker/Dockerfile |

## Build toolchain

The toolchain the worker image uses to build the scanning tools.

| Tool | Version | Pinned in |
|---|---|---|
| Go toolchain | `1.25.7` | worker/Dockerfile |

## System packages

The images also install these packages from the Debian archive of their base image. They are not pinned, so you get the version the archive holds when the image is built: `chromium`, `libpcap0.8t64`, `libpango-1.0-0`, `libpangoft2-1.0-0`, `libharfbuzz-subset0`, `fontconfig`.

## Base images

The images that each reNgine image is built on, and the images that the compose file runs directly.

| Image | File | Stage |
|---|---|---|
| `python:3.13-slim` | api/Dockerfile | base |
| `node:22-slim` | frontend/Dockerfile | build |
| `node:22-slim` | frontend/Dockerfile | production |
| `node:22-slim` | frontend/Dockerfile.dev |  |
| `python:3.13-slim` | worker/Dockerfile | base |
| `caddy:2-alpine` | docker-compose.prod.yml |  |
| `postgres:16-alpine` | docker-compose.prod.yml |  |
| `redis:8-alpine` | docker-compose.prod.yml |  |

