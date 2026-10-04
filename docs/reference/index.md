---
title: Reference
description: Look up the exact details of reNgine 3.0, from query fields and stages to MCP tools, API paths, commands and settings. Most of these pages are generated from the reNgine source, so they match the release.
sources:
  - shared/definitions/asset_query.py
  - stages/registry.py
  - mcp/registry.py
  - api/app/main.py
  - deploy/rengine
  - install.sh
  - .env.example
revised: 2026-10-03
---

Come here when you know what you want to do and need the precise name, value or limit. To learn how to do a task step by step, start with [Pentesters](../pentesters/index.md), [Developers](../developers/index.md) or [Agents](../agents/index.md).

## Generated pages

These pages are written from snapshots of the reNgine source. Each one names its snapshot and the script that writes it at the top of the page. The snapshots are refreshed with the commands in `data/README.md` of the documentation repository.

| Page | Use it to | Count |
|---|---|---|
| [Query language](query/index.md) | Write a query: grammar, operators, limits and error messages | {{ counts.query_dimensions }} dimensions |
| [Web assets](query/web-assets.md), [Endpoints](query/endpoints.md), [Services](query/services.md), [IP addresses](query/ips.md), [Vulnerabilities](query/vulnerabilities.md), [Software](query/software.md), [Secrets](query/secrets.md) | Find the fields, flags, group keys, sort keys, columns and examples of each dimension | {{ counts.query_fields }} fields, {{ counts.query_flags }} flags |
| [Stages](stages/index.md) | See what each stage does, its options and defaults, its tools, whether it sends traffic and what it does at passive intensity | {{ counts.stages }} stages in {{ counts.steps }} steps |
| [Default scan engine](default-engine.md) | See what the built-in engine runs on each type of target, and its YAML | |
| [MCP tools](mcp-tools.md) | Look up the capability, reach, parameters and return shape of each tool | {{ counts.mcp_tools }} tools |
| [HTTP API paths](http-api.md) | Find an API path by tag, with the access it requires | {{ counts.api_paths }} paths, {{ counts.api_operations }} operations |
| [Remote control commands](remote-control-commands.md) | Look up a Telegram command, its arguments and whether it asks for your authenticator code | {{ counts.chat_commands }} commands |
| [Keyboard shortcuts](keyboard-shortcuts.md) | Find the shortcuts of each page of the interface | |
| [rengine CLI](cli.md) | Manage an installed instance from the shell | {{ counts.cli_commands }} commands |
| [Installer flags](installer.md) | Install without the guided questions | {{ counts.installer_flags }} flags |
| [Configuration variables](configuration.md) | Check or change a setting in `.env`, including the variables an install adds | {{ counts.env_variables }} variables |
| [Pinned tool versions](tool-versions.md) | Check the version of each scanning tool, runtime and base image | {{ counts.pinned_tools }} tools |

## Other pages

These pages are written by hand.

| Page | Use it to |
|---|---|
| [Glossary](glossary.md) | Check what a reNgine term means |
| [Release notes 3.0.0](release-notes.md) | See what reNgine 3.0.0 contains |
