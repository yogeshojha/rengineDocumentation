---
title: Configuration variables
description: "The 55 variables of `.env.example`, plus the ones an installed instance adds, with what each one does and the value the installer writes. Use it when you tune an instance or troubleshoot one."
sources:
  - .env.example
  - shared/config.py
  - api/app/config.py
  - install.sh
  - docker-compose.prod.yml
revised: 2026-10-03
generated: scripts/gen_ops.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_ops.py` writes it from `data/repo.json` and `data/env-notes.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Your instance reads its settings from `.env` and `api.env` in the install directory. The installer writes both files. `.env.example` in the repository is the template for the development stack. After you change a value, run `rengine restart` so that the services pick it up.

!!! danger "SECRET_KEY"
    `SECRET_KEY` encrypts the credentials, tokens and two-factor secrets that reNgine stores. Your backup archives contain it. If you replace it, reNgine can no longer read the stored secrets or the two-factor secrets.

Each section below follows a section of `.env.example`. **Example value** is the value in `.env.example`, **Installer** is the value the installer writes, and **Effect** is what the variable changes.

## Application

| Variable | Example value | Installer | Effect |
|---|---|---|---|
| `DEBUG` | `true` | false | Relaxes the startup checks, serves `/docs`, `/redoc` and `/openapi.json`, and skips the password strength rules. Session cookies are `Secure` only when it is off. |
| `LOG_LEVEL` | `INFO` | INFO | Log level of the api, the workers, channels and ct-stream. |
| `SQL_ECHO` | `false` | false | Logs every SQL statement and its parameters. |

## Database

| Variable | Example value | Installer | Effect |
|---|---|---|---|
| `POSTGRES_HOST` | `db` | db | Database host. |
| `POSTGRES_PORT` | `5432` | 5432 | Database port. |
| `POSTGRES_USER` | `rengine` | rengine | Database role. |
| `POSTGRES_PASSWORD` | `rengine` | Generated, 32 hexadecimal characters | Database password. |
| `POSTGRES_DB` | `rengine` | rengine | Database name. `rengine restore` asks for it to confirm a restore. |
| `POSTGRES_SHARED_BUFFERS` | `2GB` | Sized by memory | `shared_buffers` of the db service. |
| `POSTGRES_EFFECTIVE_CACHE_SIZE` | `6GB` | Sized by memory | `effective_cache_size` of the db service. |
| `POSTGRES_WORK_MEM` | `32MB` | Sized by memory | `work_mem` of the db service. |
| `POSTGRES_MAINTENANCE_WORK_MEM` | `512MB` | Sized by memory | `maintenance_work_mem` of the db service. |
| `POSTGRES_MAX_CONNECTIONS` | `250` | 250 | `max_connections` of the db service. The api logs a warning at startup when the pools can open more connections than this allows. |
| `POSTGRES_LOG_MIN_DURATION` | `2000` | 2000 | `log_min_duration_statement`, in milliseconds. |
| `POSTGRES_MAX_WAL_SIZE` | `2GB` | Sized by memory | Disk the write-ahead log may hold between checkpoints. |
| `POSTGRES_SHM_SIZE` | `1gb` | Sized by memory | `/dev/shm` of the db container. |

## Connection pools

| Variable | Example value | Installer | Effect |
|---|---|---|---|
| `DB_POOL_SIZE` | `10` | 5 | Connections in the pool of each api process. |
| `DB_MAX_OVERFLOW` | `20` | 10 | Connections above the pool size for each api process. |
| `DB_POOL_TIMEOUT` | `10` | 10 | Seconds to wait for a pooled connection. |
| `DB_POOL_RECYCLE` | `1800` | 1800 | Seconds before a pooled connection is replaced. Applies to the api and the workers. |
| `DB_IDLE_TX_TIMEOUT` | `120` | 120 | Seconds idle inside a transaction before Postgres ends the connection. `0` disables. |
| `WORKER_DB_POOL_SIZE` | `2` | 2 | Connections in the pool of each worker child process. |
| `WORKER_DB_MAX_OVERFLOW` | `3` | 3 | Connections above the pool size for each worker child process. |
| `WORKER_DB_POOL_TIMEOUT` | `30` | 30 | Seconds a worker waits for a pooled connection. |

## Redis

| Variable | Example value | Installer | Effect |
|---|---|---|---|
| `REDIS_HOST` | `redis` | redis | Redis instance for the task broker and live state. |
| `REDIS_PORT` | `6379` | 6379 | Port of the broker Redis. |
| `REDIS_DB` | `0` | 0 | Database of the broker. The task result backend uses the next database number. |
| `REDIS_PASSWORD` | Empty | Generated, 32 hexadecimal characters | Password of both Redis instances. No whitespace, quotes or backslashes. |
| `REDIS_MAXMEMORY` | `1gb` | Sized by memory | `maxmemory` of the broker Redis, which does not evict. |
| `REDIS_CACHE_HOST` | `cache` | cache | Redis instance for cached aggregates, which evicts the least recently used keys. |
| `REDIS_CACHE_PORT` | `6379` | 6379 | Port of the cache Redis. |
| `REDIS_CACHE_MAXMEMORY` | `256mb` | Sized by memory | `maxmemory` of the cache Redis. |

## Celery

| Variable | Example value | Installer | Effect |
|---|---|---|---|
| `CELERY_SCAN_CONCURRENCY` | `16` | Sized by memory | Stage slots in each worker-scans container. Each slot runs one tool. |
| `CELERY_CONTROL_CONCURRENCY` | `8` | Sized by memory | Slots of worker-control: launch, step hand-over, resume and finalize. |
| `CELERY_DEFAULT_CONCURRENCY` | `4` | Sized by memory | Slots of worker-default: background jobs and toolbox runs. |
| `TASK_SOFT_TIME_LIMIT` | `21600` | 21600 | Seconds before a task is asked to stop, 6 hours. |
| `TASK_HARD_TIME_LIMIT` | `28800` | 28800 | Seconds before a task is ended, 8 hours. The broker visibility timeout and the result expiry are this value plus one hour. |

## API

| Variable | Example value | Installer | Effect |
|---|---|---|---|
| `SECRET_KEY` | Empty | Generated, 64 hexadecimal characters, in `.env` | Instance key. Encrypts stored credentials, tokens and two-factor secrets. Required. Outside `DEBUG` it must be at least 32 characters. |
| `JWT_SECRET_KEY` | Empty | Generated, 64 hexadecimal characters, in `api.env` | Signs sessions. Read by the api service alone. Required unless `DEBUG=true`, where an empty value is derived from `SECRET_KEY`. Must differ from `SECRET_KEY`. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Not written, the default applies | Lifetime of an access token and its cookie, in minutes. |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Not written, the default applies | Lifetime of a refresh token and its cookie, in days. |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | `["<origin>"]` | JSON list of allowed origins. `*` is refused. The first entry is also the base URL of links to the interface. |
| `API_RELOAD` | `true` | false | `true` runs one api process with reload. `false` runs `API_WORKERS` processes. |
| `API_WORKERS` | `4` | Sized by memory | api processes when `API_RELOAD` is `false`. |
| `GLOBAL_RATE_LIMIT_PER_MINUTE` | `600` | 600 | Requests a minute per signed-in user, or per client address without a valid session. `0` or less disables. `/api/v1/events` and `/api/v1/media` are exempt. Over the limit the api answers 429 with `Retry-After`. |
| `TRUSTED_PROXIES` | Empty | The Caddy address, `172.29.0.253` | Comma-separated CIDRs whose `X-Forwarded-For` header is read. |

## First administrator

| Variable | Example value | Installer | Effect |
|---|---|---|---|
| `ADMIN_EMAIL` | `admin@rengine.local` | In `api.env` | Email of the first administrator, created when no user exists. |
| `ADMIN_USERNAME` | `rengine` | In `api.env` | Username of the first administrator. |
| `ADMIN_PASSWORD` | `rengine@123` | In `api.env`, given or generated | Password of the first administrator. Outside `DEBUG`, the api refuses to start with the example value or fewer than 10 characters when no user exists. |

## Published ports

| Variable | Example value | Installer | Effect |
|---|---|---|---|
| `BIND_ADDR` | `127.0.0.1` | Not used | Development compose: address of the published db, redis and flower ports. |
| `APP_BIND_ADDR` | `127.0.0.1` | Not used | Development compose: address of the published api and frontend ports. `0.0.0.0` publishes on every interface. |

## Flower

Under the debug profile: `docker compose --profile debug up -d flower`

| Variable | Example value | Installer | Effect |
|---|---|---|---|
| `FLOWER_USER` | `admin` | admin | Flower user, under the `debug` compose profile. |
| `FLOWER_PASSWORD` | `admin` | Generated, 24 hexadecimal characters | Flower password. |

## Outbound calls that are not scan traffic

Intel feeds, RDAP, RIPEstat.

| Variable | Example value | Installer | Effect |
|---|---|---|---|
| `EGRESS_PROXY_URL` | Empty | Empty | Proxy for outbound calls that are not scan traffic: intel feeds, RDAP and RIPEstat. |
| `EGRESS_TIMEOUT` | `30` | 30 | Timeout of those calls, in seconds. |

## Variables outside .env.example

An installed instance also uses these variables, which `.env.example` does not list.

| Variable | Where | Effect |
|---|---|---|
| `COMPOSE_PROJECT_NAME` | Production `.env` | `rengine3`. |
| `COMPOSE_FILE` | Production `.env` | `docker-compose.prod.yml:ports.yml`. |
| `RENGINE_IMAGE` | Production `.env` | Image repository prefix, `yogeshojha/rengine` by default. |
| `RENGINE_TAG` | Production `.env` | Image tag of the installed release. `rengine version` prints it. |
| `RENGINE_SRC` | Production `.env` | The checkout path of a source install, empty otherwise. |
| `PUBLIC_ORIGIN` | Production `.env` | The origin of the interface. `rengine status` checks the API at this origin. |
| `RENGINE_HOST` | Production `.env` | The domain in domain mode, empty otherwise. |
| `ACME_EMAIL` | Production `.env` | Let's Encrypt account email. |
| `DOCKER_SUBNET` | Production `.env` | `172.29.0.0/24`. |
| `CADDY_ADDR` | Production `.env` | `172.29.0.253`. |
| `WORKER_SCANS_REPLICAS` | Production `.env`, written by `rengine scale` | Number of worker-scans containers, 1 by default. |
| `EGRESS_USER_AGENT` | `shared/config.py` | User agent of outbound calls that are not scan traffic. |
| `RENGINE_ADMIN_PASSWORD` | `install.sh` | Administrator password for the installer. |
| `RENGINE_BACKUP_PASSPHRASE` | `scripts/backup.sh` | Supplies the passphrase of a backup or a restore without a prompt. |
| `POSTGRES_TEST_DB` | `tests/conftest.py` | Test database name, `rengine_test` by default. |

