---
title: Developers
description: Learn how reNgine works inside, script against its HTTP API, and add your own stages, tools and connectors. This section also covers the development setup and the checks your change has to pass.
sources:
  - README.md
  - dev-README.md
  - docker-compose.yml
  - api/app/main.py
revised: 2026-10-03
---

reNgine 3.0 lives in one repository that builds three images: a FastAPI api, a Celery worker and a SvelteKit frontend. Shared Python packages hold the models, the scan stages, the MCP server and the connectors, and Docker Compose runs them together. The HTTP API answers at `/api/v1` on the same origin as the interface, and the interface uses it too.

Where you start depends on what you want to do:

- To understand how a scan runs from launch to results, read [How reNgine works](architecture.md).
- To pull results into your own scripts, start with [the HTTP API](api/index.md) and [signing in](api/authentication.md).
- To add a stage, a tool wrapper, a connector or another plug-in, pick a page under Extend below.
- To work on reNgine itself, [set up a development environment](development-environment.md) first.

{{ section_index }}
