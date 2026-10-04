---
title: rengine CLI
description: "Use the `rengine` command on your server to start and stop reNgine, check its health, read its logs, update it, and back it up or restore it. This page lists all 11 commands and what each one runs."
sources:
  - deploy/rengine
  - scripts/backup.sh
revised: 2026-10-03
generated: scripts/gen_ops.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_ops.py` writes it from `data/repo.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

The installer puts the command in `bin/rengine` inside the install directory and links it into `/usr/local/bin` or `~/.local/bin`. It runs Docker Compose in the install directory and needs the `.env` file that the installer wrote. If root owns the install directory, run it with `sudo`. When a command fails, it prints `error: <message>` and exits with status 1.

Run `rengine` with no command, or `rengine help`, to print this summary:

```text
Usage: rengine <command>

  start          start the stack
  stop           stop the stack
  restart        stop and start the stack
  status         services and API health
  logs [svc]     follow logs, all services or one
  scale <n>      run n scan worker containers
  update [tag]   move to a release, the latest when no tag is given
                 --no-backup skips the database snapshot taken first
  backup         write a backup archive to ./backups
  restore <f>    replace this instance's data with an archive
  uninstall      remove containers and data volumes
  version        installed release
```

## Commands

Each command, with a link to its details below.

| Command | What it does |
|---|---|
| [`rengine start`](#start) | Start the stack. |
| [`rengine stop`](#stop) | Stop the stack. |
| [`rengine restart`](#restart) | Stop and start the stack. |
| [`rengine status`](#status) | Services and API health. |
| [`rengine logs [svc]`](#logs) | Follow logs, all services or one. |
| [`rengine scale <n>`](#scale) | Run n scan worker containers. |
| [`rengine update [tag]`](#update) | Move to a release, the latest when no tag is given. `--no-backup`: skips the database snapshot taken first. |
| [`rengine backup`](#backup) | Write a backup archive to ./backups. |
| [`rengine restore <f>`](#restore) | Replace this instance's data with an archive. |
| [`rengine uninstall`](#uninstall) | Remove containers and data volumes. |
| [`rengine version`](#version) | Installed release. |

## start { #start }

```bash
rengine start
```

Start the stack.

Runs
:   `docker compose up -d`

## stop { #stop }

```bash
rengine stop
```

Stop the stack.

Runs
:   `docker compose down`. Containers and the network are removed, volumes are kept.

## restart { #restart }

```bash
rengine restart
```

Stop and start the stack.

Runs
:   `docker compose down`, then `docker compose up -d`

## status { #status }

```bash
rengine status
```

Services and API health.

Runs
:   `docker compose ps`, then a request to `<PUBLIC_ORIGIN>/api/v1/health/health`

What it prints
:   `API answering at <origin>`, or `The API did not respond. Check that the api service is running.`

Guide
:   [Troubleshooting](../pentesters/troubleshooting.md)

## logs { #logs }

```bash
rengine logs [svc]
```

Follow logs, all services or one.

Runs
:   `docker compose logs -f --tail 200`, for every service or the named ones.

Guide
:   [Troubleshooting](../pentesters/troubleshooting.md)

## scale { #scale }

```bash
rengine scale <n>
```

Run n scan worker containers.

Runs
:   Writes `WORKER_SCANS_REPLICAS=<n>` to `.env`, then `docker compose up -d worker-scans`

What it prints
:   `error: usage: rengine scale <n>`

Guide
:   [Troubleshooting](../pentesters/troubleshooting.md)

## update { #update }

```bash
rengine update [tag]
```

Move to a release, the latest when no tag is given.

Runs
:   Downloads the release, pulls its images, saves a database snapshot, stops the services that hold a database connection, replaces the compose file, the CLI and the backup script, and starts the stack.

`--no-backup`
:   Skips the database snapshot taken first.

What it prints
:   `Already on <tag>.`, `Updated to <tag>.`, `Running scans: <n>. Stages in flight run again after the update.`

Guide
:   [Update and roll back](../pentesters/update.md)

## backup { #backup }

```bash
rengine backup
```

Write a backup archive to ./backups.

Runs
:   `scripts/backup.sh dump`, into `./backups` or the directory given.

Guide
:   [Back up and restore](../pentesters/backup.md)

## restore { #restore }

```bash
rengine restore <f>
```

Replace this instance's data with an archive.

Runs
:   `scripts/backup.sh restore <archive>`

What it prints
:   `error: usage: rengine restore <archive>`

Guide
:   [Back up and restore](../pentesters/backup.md)

## uninstall { #uninstall }

```bash
rengine uninstall
```

Remove containers and data volumes.

Runs
:   Asks for confirmation, then `docker compose down --volumes --remove-orphans` and removes the `rengine` link.

What it prints
:   `Containers and data volumes are removed. Backups and .env stay in <dir>.`

Guide
:   [Uninstall reNgine](../pentesters/uninstall.md)

## version { #version }

```bash
rengine version
```

Installed release.

Runs
:   Prints `RENGINE_TAG` from `.env`

