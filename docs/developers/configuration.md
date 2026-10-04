---
title: How reNgine is configured
description: Find where each service reads its settings, what `DEBUG` changes, why a service refuses to start, and where instance-wide settings such as the instance mode are stored.
sources:
  - shared/config.py
  - api/app/config.py
  - worker/app/config.py
  - api/app/core/security.py
  - api/app/utils/helpers.py
  - api/app/main.py
  - api/app/core/database.py
  - shared/utils/crypto.py
  - api/entrypoint.sh
  - docker-compose.yml
  - docker-compose.prod.yml
  - .env.example
  - shared/models/instance_settings.py
  - api/app/services/instance_settings.py
  - api/app/api/v1/instance_settings.py
  - shared/enums/instance.py
  - shared/definitions/mode_features.py
  - api/app/api/capability.py
  - frontend/src/lib/config/capabilities.ts
revised: 2026-10-03
---

reNgine has two kinds of configuration. Environment variables set how each service starts: database, Redis, secrets and worker sizes. Instance-wide settings, such as the instance name and mode, live in one database row that administrators change from the interface or the API. This page shows where each one is read, so you know what to change and what to restart.

For every variable, its default and the value the installer writes, see [Configuration variables](../reference/configuration.md).

## Settings classes

Each Python service reads its environment through a pydantic settings class. Use this table to find which class a variable belongs to and which services see it.

| Class | Module | Loaded by | Adds |
|---|---|---|---|
| `BaseAppSettings` | `shared/config.py` | Every Python service, through the classes below. Alembic in `migrate`, the api's Celery client and the encryption helpers read it directly. | Application, database, pool, Redis, Celery and egress variables |
| `Settings` | `api/app/config.py` | `api`, `channels`, the MCP stdio transport | `JWT_SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `GLOBAL_RATE_LIMIT_PER_MINUTE`, `API_RELOAD`, `API_WORKERS`, `ADMIN_EMAIL`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` |
| `Settings` | `worker/app/config.py` | `worker-scans`, `worker-control`, `worker-default`, `worker-beat`, `ct-stream` | No variables |

`BaseAppSettings` reads the process environment, and a `.env` file in the working directory when one exists. Names are case-sensitive, and unknown variables are ignored.

The settings classes also work out these values from the variables:

| Property | Value |
|---|---|
| `database_url_async` | `postgresql+asyncpg://…`, used by the api, `channels` and Alembic |
| `database_url_sync` | `postgresql://…`, used by the workers |
| `redis_url` | `redis://…/<REDIS_DB>`. The Celery broker. |
| `celery_result_backend` | `redis://…/<REDIS_DB + 1>` |
| `redis_cache_url` | `redis://<REDIS_CACHE_HOST>:<REDIS_CACHE_PORT>/0` |
| `ui_base_url` | The first entry of `CORS_ORIGINS`. Absolute links in notifications, issue tracker bodies, MCP results and chat replies start with it. |
| `worker_children` | `CELERY_SCAN_CONCURRENCY + CELERY_CONTROL_CONCURRENCY + CELERY_DEFAULT_CONCURRENCY` |

`APP_VERSION` comes from the `VERSION` file, or reads `unknown` when the file cannot be read.

## Environment files per service

Not every service gets every variable. This table shows which environment files each service loads, in development and in production.

| Service | Development compose | Production compose |
|---|---|---|
| `api` | `.env` | `.env` and `api.env`. `API_RELOAD` is set to `false`. `TRUSTED_PROXIES` defaults to the Caddy address. |
| `channels`, workers, `worker-beat`, `ct-stream` | `.env`, with `ADMIN_PASSWORD` and `JWT_SECRET_KEY` set to empty | Same |
| `migrate` | Not present | `.env`, with `ADMIN_PASSWORD` and `JWT_SECRET_KEY` set to empty |
| `flower` | `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, `REDIS_PASSWORD` only | Same |
| `frontend` | `NODE_ENV=development` | `ORIGIN` from `PUBLIC_ORIGIN` |

The installer writes `api.env`, mode `600`, with `JWT_SECRET_KEY` and the first administrator. The development stack has no `api.env`: these variables come from `.env` and reach the api alone.

Some variables are read outside the settings classes, by Compose or by a script:

| Reader | Variables |
|---|---|
| Compose interpolation | `POSTGRES_SHARED_BUFFERS`, `POSTGRES_EFFECTIVE_CACHE_SIZE`, `POSTGRES_WORK_MEM`, `POSTGRES_MAINTENANCE_WORK_MEM`, `POSTGRES_MAX_CONNECTIONS`, `POSTGRES_LOG_MIN_DURATION`, `POSTGRES_MAX_WAL_SIZE`, `POSTGRES_SHM_SIZE`, `REDIS_MAXMEMORY`, `REDIS_CACHE_MAXMEMORY`, the three `CELERY_*_CONCURRENCY` worker flags, `FLOWER_USER`, `FLOWER_PASSWORD`, `BIND_ADDR` and `APP_BIND_ADDR` in development, `RENGINE_IMAGE`, `RENGINE_TAG`, `RENGINE_SRC`, `WORKER_SCANS_REPLICAS`, `CADDY_ADDR`, `DOCKER_SUBNET` and `PUBLIC_ORIGIN` in production |
| `api/entrypoint.sh` | `API_RELOAD`, `API_WORKERS`, `TRUSTED_PROXIES` |
| `scripts/backup.sh` | `RENGINE_BACKUP_PASSPHRASE` |
| `tests/conftest.py` | `POSTGRES_TEST_DB` |
| `mcp/stdio.py` | `RENGINE_MCP_TOKEN` |

## What DEBUG changes { #debug }

`DEBUG` turns off checks that protect a real instance and serves the API document, so keep it for development. `.env.example` sets `DEBUG=true`, and the installer writes `DEBUG=false`. This table shows everything it changes:

| Behaviour | `DEBUG=true` | `DEBUG=false` |
|---|---|---|
| `/docs`, `/redoc`, `/openapi.json` on the api | Served | Not served |
| `Secure` flag on the session cookies | Off | On |
| Password length and strength rules | Skipped | At least 10 characters and a zxcvbn score of 3 |
| `SECRET_KEY` length check | Skipped | At least 32 characters, not the published placeholder |
| `JWT_SECRET_KEY` | Derived from `SECRET_KEY` when empty | Required, at least 32 characters |
| First administrator password | Any value | At least 10 characters, not `rengine@123` |

To log SQL statements, use `SQL_ECHO`. `DEBUG` does not log them.

## When a service refuses to start

A service checks its secrets and settings when it starts, and stops with a message when one is missing or weak. Find the message below to see what to fix.

| Message | Condition | Raised by |
|---|---|---|
| `SECRET_KEY is not set. Generate one with: openssl rand -hex 32` | `SECRET_KEY` is empty | The api settings, in `api` and `channels`. The workers raise the same message on the first encryption or decryption. |
| `SECRET_KEY must be a generated value of at least 32 characters. Generate one with: openssl rand -hex 32` | `DEBUG` is off and `SECRET_KEY` is shorter than 32 characters or equals `change-me-in-production-use-openssl-rand-hex-32` | Every Python service |
| `JWT_SECRET_KEY is not set. Generate one with: openssl rand -hex 32, and give it to the api service alone.` | `DEBUG` is off and `JWT_SECRET_KEY` is empty | api startup |
| `JWT_SECRET_KEY must differ from SECRET_KEY.` | `JWT_SECRET_KEY` equals `SECRET_KEY` | api startup |
| `JWT_SECRET_KEY must be at least 32 characters. Generate one with: openssl rand -hex 32` | `DEBUG` is off and `JWT_SECRET_KEY` is shorter than 32 characters | The api settings |
| `ADMIN_PASSWORD must be set to at least 10 characters, not the default, before the first start.` | `DEBUG` is off, the `users` table is empty, and `ADMIN_PASSWORD` is `rengine@123` or shorter than 10 characters | api startup |
| `REDIS_PASSWORD must not contain whitespace, quotes or backslashes. Generate one with: openssl rand -hex 32` | `REDIS_PASSWORD` holds whitespace, a quote or a backslash | Every Python service |
| `CORS_ORIGINS must be an explicit allowlist (no '*') when credentials are enabled` | `CORS_ORIGINS` contains `*` | api import |

The api starts in this order: the signing key check, the AI call ledger, the first administrator seed, the connection pool check, the Redis SSE bridge. If any of them fails, the api logs `Failed to initialize the application: <error>` and stops.

The pool check tells you whether PostgreSQL can serve every connection the pools may open. It compares the connections every pool can open with `max_connections` minus the reserved superuser connections, and logs one line:

| Level | Line |
|---|---|
| Warning | `database pools can outgrow the server`, with `demand`, `usable` and `hint=raise POSTGRES_MAX_CONNECTIONS or lower the pool sizes` |
| Info | `database pool headroom`, with `demand` and `usable` |

## Instance settings in the database

Settings that apply to the whole instance, such as its name, time zone, mode and retention, are kept in the database rather than in the environment, and administrators change them from the interface or the API. They are one row of `instance_settings`, with `singleton_key` set to `instance` and a unique constraint on it. The api creates the row on first read.

Anyone signed in can read them. Only administrators can change them:

| Operation | Access |
|---|---|
| `GET /api/v1/instance-settings` | Any signed-in user |
| `PATCH /api/v1/instance-settings` | Administrator |

These are the fields, with their defaults and the values each one accepts:

| Field | Default | Accepted values |
|---|---|---|
| `instance_name` | `reNgine` | Non-empty, cut at 120 characters |
| `timezone` | `UTC` | An IANA time zone name |
| `mode` | `bug_bounty` | `bug_bounty`, `corporate` |
| `scan_history_retention_days` | 90 | 30, 60, 90, 180, 365, 0 |
| `screenshot_retention_days` | 30 | 7, 14, 30, 60, 90, 0 |
| `cert_recheck_enabled` | `false` | Boolean |
| `concurrent_scans` | 0, automatic | 0 to 50 |

The response adds `capabilities`, the features of the current mode, and `concurrent_scans_auto`, the limit automatic resolves to.

A change with a value outside these gets one of these answers:

| Status | Detail |
|---|---|
| 400 | `Instance name is required.` |
| 400 | `Invalid timezone '<value>'.` |
| 400 | `Invalid mode '<value>'. Must be one of bug_bounty, corporate.` |
| 400 | `Scan history retention must be 30, 60, 90, 180, 365 days, or 0 to keep forever.` |
| 400 | `Screenshot retention must be 7, 14, 30, 60, 90 days, or 0 to keep forever.` |
| 422 | `concurrent_scans` outside 0 to 50 |

The same row holds the MCP server switch and settings (`mcp_enabled`, `mcp_settings`), the AI switch and connection, onboarding state, bounty sync intervals and the OAST settings. Each feature changes its own fields through its own API. API keys, proxies, notification channels and chat channel settings have their own tables.

## Instance modes

The instance mode decides which features reNgine offers. Bug bounty mode adds bounty platforms, programs and program watches. Corporate mode leaves them out. The mode is one column, `instance_settings.mode`, and an instance runs in one mode at a time: `bug_bounty` or `corporate`.

| Mode | Label | Capabilities |
|---|---|---|
| `bug_bounty` | Bug bounty | `bounty_platforms`, `bounty_programs`, `program_watches` |
| `corporate` | Corporate | None |

The modes are defined in `shared/enums/instance.py` and `shared/definitions/mode_features.py`, and `frontend/src/lib/config/capabilities.ts` mirrors them. An unknown mode value reads as `bug_bounty`.

These gates refuse a bug bounty feature in corporate mode, with the answer shown:

| Gate | Refusal |
|---|---|
| Bounty program routes | 403 `Bug bounty programs require bug bounty mode.` |
| Program watch routes | 403 `Program watches require bug bounty mode.` |
| API key for HackerOne or Intigriti | 403 `<provider> requires bug bounty mode.` The provider list leaves them out in corporate mode. |

You choose the mode in the setup wizard and change it later in **Settings**, **General**, **Mode**. See [Bug bounty and corporate modes](../pentesters/instance-modes.md).
