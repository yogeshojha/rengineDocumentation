---
title: Installer flags
description: "Every option of `install.sh`, the script that installs reNgine. Use it when you install without the guided questions, for example from a provisioning script. It covers 17 flags and the one environment variable the installer reads."
sources:
  - install.sh
  - README.md
revised: 2026-10-03
generated: scripts/gen_ops.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_ops.py` writes it from `data/repo.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Run the installer without flags and it asks you for each setting. Give it a reachability flag and it runs without asking, which suits automated installs. For a walkthrough, see [Install reNgine](../pentesters/install.md).

Run `install.sh --help` to print this summary:

```text
Usage: install.sh [options]

Run without flags for the guided setup.

Reachability, one of
  --domain <name>       public domain, HTTPS certificate from Let's Encrypt
  --ip [address]        server address, self-signed certificate
  --local               this machine only, no TLS

Options
  --ui-port <port>      published UI port, fixed at 443 with --domain
  --api-port <port>     publish the API over plain HTTP on 127.0.0.1
  --no-api-port         stop publishing the API port
  --admin-user <name>   first administrator, default rengine
  --admin-email <mail>
  --admin-password-stdin
                        read the administrator password from stdin
  --acme-email <mail>   Let's Encrypt account email
  --dir <path>          install directory
  --tag <tag>           release to install, default the latest
  --image <prefix>      image repository prefix, default yogeshojha/rengine
                        ghcr.io/yogeshojha/rengine holds the same images
  --build               build images from this checkout instead of pulling
  --no-start            write the configuration and stop
  --no-backup           skip the database snapshot taken before an upgrade
  --force               skip the memory, disk and port checks

Environment
  RENGINE_ADMIN_PASSWORD  administrator password, default a generated one
```

The installer checks the host first. It stops if the host has less than 4 GB of memory or 10 GB of free disk. The recommended size is 8 GB of memory and 25 GB of disk. `--force` skips these checks.

## Reachability

Reachability decides how people reach your instance: on a public domain, on the address of the server, or only from the machine itself. Pick one of these flags.

| Flag | What it does |
|---|---|
| `--domain <name>` | Public domain, HTTPS certificate from Let's Encrypt. |
| `--ip [address]` | Server address, self-signed certificate. |
| `--local` | This machine only, no TLS. |

## Options

These set the ports, the first administrator, the install directory, the release and the other details of an install.

| Flag | What it does |
|---|---|
| `--ui-port <port>` | Published UI port, fixed at `443` with `--domain`. |
| `--api-port <port>` | Publish the API over plain HTTP on `127.0.0.1`. |
| `--no-api-port` | Stop publishing the API port. |
| `--admin-user <name>` | First administrator, default rengine. |
| `--admin-email <mail>` | Email of the first administrator. |
| `--admin-password-stdin` | Read the administrator password from stdin. |
| `--acme-email <mail>` | Let's Encrypt account email. |
| `--dir <path>` | Install directory. |
| `--tag <tag>` | Release to install, default the latest. |
| `--image <prefix>` | Image repository prefix, default `yogeshojha/rengine`. `ghcr.io/yogeshojha/rengine` holds the same images. |
| `--build` | Build images from this checkout instead of pulling. |
| `--no-start` | Write the configuration and stop. |
| `--no-backup` | Skip the database snapshot taken before an upgrade. |
| `--force` | Skip the memory, disk and port checks. |

## Environment

The installer also reads this from the environment.

| Variable | What it does |
|---|---|
| `RENGINE_ADMIN_PASSWORD` | Administrator password, default a generated one. |

