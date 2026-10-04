---
title: Where the code lives
description: Find where each part of reNgine lives in the repository, which image each directory ends up in, and what the files at the root are for.
sources:
  - .gitignore
  - .dockerignore
  - api/Dockerfile
  - worker/Dockerfile
  - docker-compose.yml
  - Makefile
  - pyproject.toml
  - tools/pyproject.toml
  - shared/pyproject.toml
  - shared/config.py
  - frontend/src/lib/version.ts
revised: 2026-10-03
---

One repository holds the api, the worker and the frontend, the Python packages both images share, the deployment files and the test suite. Use this page to find where to make a change.

## Top-level directories

The Image column tells you which image contains the directory, and so where its code can run. The api and worker images both set `WORKDIR /app` and `PYTHONPATH=/app`.

| Directory | Content | Image |
|---|---|---|
| `api/` | The FastAPI service. `app/` is the Python package `app` of the api image: `main.py`, `config.py`, `api/router.py` and the routers in `api/v1/`, `core/` for security, rate limits and database sessions, `services/` with one service class per area, `utils/`. Also `Dockerfile`, `entrypoint.sh`, `pyproject.toml` and `uv.lock`. | api |
| `worker/` | The Celery worker. `app/` is the Python package `app` of the worker image: `celery.py` with the queues, routes and beat schedule, `orchestrator/` with the canvas, stage runner and finalize, `tasks/`, `ct_stream/`. Also `Dockerfile`, `chrome.sh`, `pyproject.toml` and `uv.lock`. | worker |
| `shared/` | Code both images import: `config.py`, `models/`, `schemas/`, `definitions/`, `enums/`, `services/`, `utils/`, `plugins.py`, `sse.py`, `redis.py`, `http.py`, `logging.py`. Its `pyproject.toml` installs dependencies only. | api, worker |
| `frontend/` | The SvelteKit 5 application. `src/routes/` holds the pages and `src/lib/` holds the API client, components, configuration mirrors, stores, types and utilities. Also `Dockerfile`, `Dockerfile.dev`, `vite.config.ts`, `vitest.config.ts`, `svelte.config.js`, `eslint.config.js`, `package.json`. | frontend |
| `stages/` | Scan stages. One directory per stage with `stage.py` and `config.py`, plus `base.py`, `registry.py`, `config.py`, `presets.py` and `sink.py`. The registry discovers each directory. | api, worker |
| `reports/` | PDF report generation: `registry.py`, `pipeline.py`, `presets.py`, one directory per section under `sections/` with `section.py` and `section.html`, `render/`, `charts/`, `narrate/`, `analysis/`, `data/`, `assets/`. | api, worker |
| `interest/` | Exposure providers: `base.py`, `context.py`, `registry.py`, `presets.py`, and `providers/rules`, `providers/correlation`, `providers/ai`. | api, worker |
| `toolbox/` | On-demand lookups run from the interface: `tools/` with one module per tool, `registry.py`, `runner.py`, `store.py`, `guard.py`, `pivot.py`. | api, worker |
| `mcp/` | The MCP server: `server.py`, `protocol.py`, `transport.py`, `stdio.py`, `registry.py`, `capabilities.py`, `tools/` with one module per tool, `models.py`, `README.md`, `ADDING_A_TOOL.md`. | api |
| `channels/` | Remote control over chat channels, run as `python -m channels`: `dispatch.py`, `commands.py`, `pairing.py`, `stepup.py`, `render.py`, `models.py`, and the driver in `telegram/`. | api |
| `connectors/` | Proxy connectors: `base.py`, `registry.py`, `auth.py`, `ingest.py`, `handoff.py`, `notice.py`, `burp/`, `README.md`. | api |
| `tools/` | One sub-package per external tool, with `client.py` and optionally `parser.py`. `runner/` runs a command-line tool and maps its records. `data/` holds the bundled wordlists `content.txt`, `subdomains.txt` and `vhosts.txt`. Its `pyproject.toml` installs dependencies only. | api, worker |
| `clients/` | `clients/burp/`: Java source of the Burp Suite extension, `build.sh`, `test.sh`, `README.md`. Excluded from Docker builds. | none |
| `deploy/` | `rengine`, the operator command installed with a release, and `seccomp-chromium.json`, the seccomp profile of the workers that start Chromium. | none |
| `scripts/` | `backup.sh` for backup and restore, `connector_e2e.py` and `connector_journey.py` for connector checks over the HTTP API, and `fetch_*.py` scripts that regenerate bundled data files. | none |
| `tests/` | The pytest suite: `api/`, `channels/`, `deploy/`, `grammar/`, `hygiene/`, `pipeline/`, `posture/`, `toolbox/`, `conftest.py`. Mounted into the api container in development. See [Tests and CI](tests-and-ci.md). | none |
| `alembic/` | Migrations: `env.py`, `script.py.mako` and `versions/`. The chain starts at one baseline, `initial_schema`, revision `3f8b2d6c1a94`. | api |
| `binaries/` | Built client artefacts served by the api: `rengine-connector-0.1.0.jar`. `clients/burp/build.sh` writes it. | api |
| `research/` | Design research notes of a working checkout. Ignored by git and excluded from Docker builds. | none |
| `scan_media/` | Screenshots, one directory per scan id. Ignored by git. Bind-mounted at `/app/scan_media` in the api and the workers. | mounted |
| `.github/` | `workflows/`, `ISSUE_TEMPLATE/`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `FUNDING.yml`. | none |

In development, the source directories are mounted into the containers instead of copied, so your edits reach the containers right away. See [Set up a development environment](development-environment.md).

## Python projects

The Python code is split into four uv projects. Check this table when you add a dependency, to see which lock file it belongs in.

| Project | File | Installs |
|---|---|---|
| `rengine-api` | `api/pyproject.toml`, `api/uv.lock` | The api's dependencies, `shared` and `tools` |
| `rengine-worker` | `worker/pyproject.toml`, `worker/uv.lock` | The worker's dependencies, `shared` and `tools` |
| `rengine-shared` | `shared/pyproject.toml` | Dependencies only, `packages = []` |
| `rengine-tools` | `tools/pyproject.toml` | Dependencies only, `packages = []` |

Both images run `uv sync --locked`. The root `pyproject.toml` holds the ruff and pytest configuration only.

## Root files

These are the files at the top of the repository and what each one is for.

| File | Content |
|---|---|
| `Makefile` | Development commands. See [Make commands](make-targets.md). |
| `docker-compose.yml` | The development stack: images built from the `development` stages, source mounted, ports on `127.0.0.1` |
| `docker-compose.prod.yml` | The production stack: published images, Caddy, the `migrate` and `volume-init` one-shot services. Published ports live in `ports.yml`, written by the installer. |
| `install.sh` | The installer. See [Install reNgine](../pentesters/install.md) and [Installer flags](../reference/installer.md). |
| `VERSION` | The release number, `3.0.0`. Read by `shared/config.py` as `APP_VERSION` and by `frontend/src/lib/version.ts`. A release build of the api and worker images writes the tag into `/app/VERSION`. |
| `.env.example` | The environment template. See [Configuration variables](../reference/configuration.md). |
| `pyproject.toml` | ruff and pytest configuration |
| `.pre-commit-config.yaml` | pre-commit hooks: ruff, prettier and the standard file checks |
| `alembic.ini` | Alembic configuration. Revision files are named `<year>_<month>_<day>_<revision>_<slug>.py`. |
| `dev-README.md` | First run, migrations, releasing and checks |
| `README.md`, `CHANGELOG.md`, `LICENSE` | Project documents. The licence is GNU GPL v3. |
| `.dockerignore` | Excludes `.git`, `.github`, `research`, `scan_media`, `clients/` and build caches from Docker builds |
| `.gitattributes` | LF line endings for Dockerfiles, shell scripts and `deploy/rengine` |
| `CLAUDE.md`, `NOTES.md` | Maintainer working notes for coding agents. Listed in `.gitignore` and absent from a clone. |
