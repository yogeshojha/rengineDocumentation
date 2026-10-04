---
title: How reNgine works
description: See how the pieces of reNgine fit together, how a request reaches the api, and how a scan moves from launch through its stages to results. Read this before you change the pipeline or chase down a scan that does not finish.
sources:
  - docker-compose.yml
  - docker-compose.prod.yml
  - api/app/main.py
  - api/entrypoint.sh
  - api/Dockerfile
  - worker/Dockerfile
  - worker/app/celery.py
  - worker/app/tasks/scan.py
  - worker/app/orchestrator/stage.py
  - worker/app/orchestrator/finalize.py
  - shared/services/orchestrator/canvas.py
  - shared/services/celery_dispatch.py
  - shared/services/event_publisher.py
  - shared/definitions/workers.py
  - shared/sse.py
  - stages/registry.py
  - stages/base.py
  - stages/sink.py
  - api/app/api/v1/events.py
  - api/app/core/redis_sse_bridge.py
  - api/app/api/v1/mcp.py
  - mcp/stdio.py
  - connectors/README.md
  - install.sh
revised: 2026-10-03
---

## Services

reNgine runs as one Docker Compose stack. A FastAPI api, a SvelteKit frontend and Celery workers share one PostgreSQL 16 database and two Redis instances. In production, Caddy serves the interface and the API on one origin. Use this table to find which container does what, for example when you read logs or decide which service to restart.

| Service | Image | Process | Role |
|---|---|---|---|
| `api` | api | `uvicorn app.main:app`, port 8000 | HTTP API at `/api/v1`, server-sent events, the MCP server over HTTP |
| `frontend` | frontend | Vite dev server on port 5173 in development, `node build` on port 3000 in production | The interface |
| `worker-scans` | worker | `celery -A app.celery worker --queues=scans` | Scan stages. `CELERY_SCAN_CONCURRENCY` stage slots per container. |
| `worker-control` | worker | `celery -A app.celery worker --queues=scan_control` | Scan launch, step hand-over, resume and finalize |
| `worker-default` | worker | `celery -A app.celery worker --queues=critical,default` | Background jobs and toolbox runs |
| `worker-beat` | worker | `celery -A app.celery beat` | Periodic tasks |
| `channels` | api | `python -m channels` | Remote control. Long-polls every chat channel that is switched on. |
| `ct-stream` | worker | `python -m app.ct_stream` | Certificate transparency stream for watched programs |
| `db` | `postgres:16-alpine` | `postgres` with tuning flags | PostgreSQL 16 |
| `redis` | `redis:8-alpine` | `redis-server --appendonly yes --maxmemory-policy noeviction` | Celery broker and results, session revocation, the SSE channel, counters |
| `cache` | `redis:8-alpine` | `redis-server --save "" --appendonly no --maxmemory-policy allkeys-lru` | Cached aggregates and crt.sh answers. No persistence. |
| `caddy` | `caddy:2-alpine` | Caddy | Production only. TLS. Routes `/api/*` to `api:8000` and every other path to `frontend:3000`. |
| `migrate` | api | `alembic upgrade head` | Production only. One-shot before the api and the workers start. |
| `volume-init` | worker | `chown` of the data directories | Production only. One-shot. Hands the data volumes to the image user. |
| `flower` | worker | `celery -A app.celery flower --port=5555` | Celery Flower under the `debug` compose profile, on `127.0.0.1:5555` |

Compose runs every Python process through `uv run`. The worker services publish no port. In production you can run more `worker-scans` containers with `rengine scale`, which sets `WORKER_SCANS_REPLICAS`.

The diagram shows how the services talk to each other.

```text
                          browser
                             |
             caddy (production: TLS, one origin)
              | /api/*                    | other paths
              v                           v
   api (FastAPI) ---------------------  frontend (SvelteKit)
    |  /api/v1           REST
    |  /api/v1/events    server-sent events  <---- redis pub/sub "rengine:sse_events"
    |  /api/v1/mcp       MCP over HTTP                         ^
    |                                                          |
    |  send_task -> redis (broker)                              |
    v                                                          |
   worker-control   (scan_control)  launch, step, resume, finalize
   worker-scans     (scans)         one stage per slot  -------+
   worker-default   (default, critical)  jobs, toolbox runs
   worker-beat      schedule ticks and maintenance
    |
    v
   db (PostgreSQL 16)        cache (aggregates, evicts)

   channels (Telegram, api image)    ct-stream (CT log, worker image)
```

## Images

The repository builds three images: api, worker and frontend. Check this table before you add code, because the image decides where your code can run. Both Python images set `WORKDIR /app` and `PYTHONPATH=/app`, so each top-level package imports by its directory name.

| Package | api image | worker image |
|---|---|---|
| `app` | `api/app` | `worker/app` |
| `shared`, `tools` | Yes | Yes |
| `stages`, `reports`, `interest`, `toolbox` | Yes | Yes |
| `mcp`, `channels`, `connectors` | Yes | No |
| `alembic`, `alembic.ini`, `binaries` | Yes | No |
| Scanner binaries in `/usr/local/bin` | No | Yes |

A tool that runs an external binary has to run in the worker image, since the api image holds no scanner binaries. In production, the Python images run as the user `rengine`, uid 10001, and the frontend runs as `node`.

## How a request reaches the api

Follow one request from the browser to the database. Your own scripts take the same path from step 2 on.

1. The browser calls a relative URL under `/api/v1` with `credentials: 'include'`.
2. In production, Caddy forwards `/api/*` to `api:8000` with `flush_interval -1` and a 128 MB request body limit. In development, the Vite dev server proxies `/api` to `http://api:8000`.
3. Middleware runs in this order: CORS, NUL rejection, the global rate limit, the body size limit.
4. The route dependency resolves the user from the `Authorization: Bearer` header or the `access_token` cookie.
5. The handler takes an `AsyncSession` and calls a service class in `api/app/services/`.

The api talks to PostgreSQL with async sessions on asyncpg. The workers use sync sessions on psycopg2.

## How a scan runs

This is what happens between **Start scan** and the results. Read it when you add a stage, or when you need to know why a scan is still `pending`.

1. **Launch.** `POST /api/v1/scans/batch` creates one `scans` row per target with status `pending`. `scans.execution_config` holds the resolved configuration, with header values, the proxy URL and tool arguments sealed. After the commit, the api sends `app.tasks.scan.run_scan` to the `scan_control` queue. The schedule tick, every 60 seconds, creates rows and dispatches `run_scan` the same way.
2. **Admission.** `run_scan` runs on `worker-control`. It locks the row and admits the scan when running scans stay under the instance limit, `instance_settings.concurrent_scans`. A held scan stays `pending` and is admitted when another run settles.
3. **Steps.** `run_scan` sets the status to `running`, builds the canvas and dispatches its first step. The steps come from `Stage.depends_on`: `stages/registry.py:execution_plan` layers the stages by longest path and places stages that nothing waits on in the last steps. A step with several stages is a Celery chord, and its callback `app.tasks.scan.run_scan_step` dispatches the next step.
4. **Stages.** Each stage is one `app.tasks.scan.run_scan_stage` task on the `scans` queue. `run_stage` opens a `scan_activities` row, emits `stage_started`, and records `skipped` when the target type is outside the stage's `applies_to` or the stage is not enabled for the run. Otherwise the stage runs and records `success`, `partial`, `failed`, `aborted` or `paused`.
5. **Results.** A stage writes rows while its tool runs, through `ResultSink`, which commits every 500 rows or 2 seconds. Each flush updates the scan's counters and emits `results_found`.
6. **Finalize.** After the last step, `app.tasks.scan.finalize_scan` aggregates the stage outcomes into `completed` or `failed`, stores the counts, admits waiting scans, settles the scan surface plan and the run's deltas, writes the activity log entry and emits the terminal event. A completed full scan then dispatches the exposure evaluation, which sends the digest notification. A failed scan sends its notification directly.

A canvas is the Celery plan of a run. The canvas of a new run holds all {{ counts.stages }} stages in {{ counts.steps }} steps, and a stage that does not run records `skipped`. This table shows which stages share a step:

| Step | Stages |
|---|---|
| 1 | `asset_seed`, `seed_resolution`, `subdomain_discovery`, `target_enrichment` |
| 2 | `host_discovery`, `session_check`, `takeover`, `zone_transfer` |
| 3 | `cdn_check`, `netblock_sweep`, `passive_ports`, `reverse_dns` |
| 4 | `port_scan`, `vhost` |
| 5 | `http_probe` |
| 6 | `broken_links`, `content_discovery`, `origin_probe`, `service_fingerprint`, `url_discovery`, `waf_detect` |
| 7 | `ai_detection`, `dns_posture`, `endpoint_probe`, `ip_enrichment`, `lookalike_domains`, `name_ownership`, `screenshot`, `vulnerability_scan` |
| 8 | `dast_scan`, `secret_mining` |

[Stages](../reference/stages/index.md) describes each stage.

### Cancel, pause and resume

Here is what each action does to a run that is in progress.

| Action | Effect |
|---|---|
| Cancel | Sets the status. Running stages stop through their abort check, polled every 2 seconds. Queued stages record `aborted`. The api dispatches finalize. |
| Pause | Sets the scan and its running activities to `paused` in one transaction, then revokes the queued tasks. Running stages stop through the abort check and run again on resume. |
| Resume | Sets `running`, increments `scans.run_epoch` and dispatches `app.tasks.scan.resume_scan`, which builds a new canvas from the first unfinished step. A task carrying an earlier epoch returns without running. |

A scan is always in one of these statuses: `pending`, `running`, `paused`, `completed`, `failed`, `cancelled`. A stage is in one of these: `pending`, `running`, `paused`, `success`, `partial`, `failed`, `skipped`, `aborted`.

## Queues

Each worker listens on its own queues. Scan stages run on `worker-scans`, so they do not take the slots that launch, hand-over and finalize need on `worker-control`. Use this table to find where a task runs.

| Queue | Label | Consumer | Tasks |
|---|---|---|---|
| `scan_control` | Scan control | `worker-control` | `app.tasks.scan.*`: launch, step hand-over, resume, finalize, admission |
| `scans` | Scan stages | `worker-scans` | `app.tasks.scan.run_scan_stage` |
| `default` | Background jobs | `worker-default` | Every other task, and `app.tasks.scan.reap_stalled` |
| `critical` | Toolbox | `worker-default` | `app.tasks.toolbox.*` |

Every worker shares these Celery settings: JSON serialisation, `task_acks_late`, `worker_prefetch_multiplier=1`, `task_reject_on_worker_lost`, prefork pool, `worker_max_tasks_per_child=100`. The soft and hard task limits are `TASK_SOFT_TIME_LIMIT` and `TASK_HARD_TIME_LIMIT`. The broker visibility timeout and the result expiry are the hard limit plus 3,600 seconds. Workers start with `--without-mingle --without-gossip`.

To show it is alive, each worker touches `/tmp/worker-heartbeat` every 30 seconds while it consumes. The compose healthcheck reads it with `find /tmp/worker-heartbeat -mmin -2`.

### Periodic tasks

`worker-beat` starts these jobs on a timer: launching scheduled scans, resuming runs whose workers died, refreshing threat intelligence, cleaning up reports and more. Look here when you want to know what runs in the background and how often. Each entry expires after its own interval.

| Entry | Task | Interval |
|---|---|---|
| `scan-schedule-tick` | `app.tasks.schedule.tick` | 60 seconds |
| `scan-stall-reap` | `app.tasks.scan.reap_stalled` | 5 minutes |
| `retention-enforce` | `app.tasks.retention.enforce` | 24 hours |
| `daily-jobs` | `app.tasks.daily.run` | 24 hours |
| `threat-intel-refresh` | `app.tasks.threat_intel.refresh` | 24 hours |
| `certificate-recheck` | `app.tasks.freshness.certificates` | 4 hours |
| `ip-range-refresh` | `app.tasks.ip_asn.refresh` | 7 days |
| `ip-range-backfill` | `app.tasks.ip_asn.backfill` | 5 minutes |
| `hygiene-backfill`, `screenshot-backfill`, `software-backfill`, `secret-backfill`, `estate-enrich`, `scan-deltas-backfill` | One task each | 5 minutes |
| `watch-recheck` | `app.tasks.watch.recheck` | 10 minutes |
| `report-reap`, `export-reap` | `app.tasks.reports.reap`, `app.tasks.export.reap` | 10 minutes |
| `report-cleanup`, `export-cleanup` | `app.tasks.reports.cleanup`, `app.tasks.export.cleanup` | 24 hours |
| `notification-cleanup` | `app.tasks.notifications.cleanup` | 6 hours |
| `bounty-program-sync`, `bounty-report-sync`, `bounty-feed-sync` | `app.tasks.bounty_programs.*` | 1 hour. Each task checks its own configured interval. |
| `issue-status-refresh` | `app.tasks.issue_trackers.refresh` | `STATUS_REFRESH_SECONDS` |
| `tripwire-prune` | `app.tasks.tripwires.prune` | 24 hours |

`worker-beat` keeps its state in `/app/beat-state/celerybeat-schedule` on the `beat_state` volume.

## Live updates

The interface updates while a scan runs, without a reload. reNgine does this with server-sent events (SSE), in three steps:

1. A worker or the api publishes `{"channel", "event_type", "data"}` to the Redis channel `rengine:sse_events`.
2. Each api process runs `RedisSSEBridge`, started in the application lifespan. It subscribes to that channel and hands each message to the in-process `SSEManager`.
3. The browser holds one `EventSource` on `GET /api/v1/events/stream?channels=<list>`.

If you listen to the stream yourself, these are the channels, event types and limits:

| Item | Value |
|---|---|
| Channels | `broadcast`, `project:<project id>` |
| Event types | `notification` on `broadcast`, `activity` and `scan` on `project:<id>` |
| Scan event kinds | `scan_started`, `scan_completed`, `scan_failed`, `scan_cancelled`, `scan_paused`, `scan_resumed`, `stage_started`, `stage_progress`, `stage_completed`, `command_started`, `command_finished`, `results_found`, `interest_ready` |
| Frame | `event: message` with `data: {"channel", "type", "data", "ts"}` |
| Heartbeat | After 30 seconds without a message the server checks the token and sends `: heartbeat`, or `event: unauthorized` and closes |
| Limits | 1,000 streams per api process, 100 queued messages per stream |
| Rate limit | `/api/v1/events` is exempt from the global rate limit |

The stream refuses a request with one of these answers:

| Status | Detail |
|---|---|
| 400 | `At least one channel is required` |
| 403 | `No valid channels in request` |
| 503 | `Too many event streams` |

## The shared package

`shared/` holds the code both Python images import. Put your code here when the api and the workers both need it.

| Path | Content |
|---|---|
| `shared/config.py` | `BaseAppSettings`, `APP_VERSION` read from `VERSION` |
| `shared/models/` | SQLModel tables and their `Create`, `Read` and `Update` schemas |
| `shared/definitions/` | Constants and vocabularies, one definition per concept |
| `shared/enums/` | Enumerations |
| `shared/services/` | Services used by the api and the workers: the asset query compiler, the orchestrator canvas, inventories, the notifier, retention, scan admission |
| `shared/utils/` | Helpers: encryption, network parsing, text scrubbing, time |
| `shared/plugins.py` | Discovery of plug-in classes in a directory |
| `shared/sse.py`, `shared/redis.py`, `shared/http.py`, `shared/logging.py` | SSE fan-out, Redis clients, outbound HTTP clients, the field logger |

`shared/` does not import `fastapi` at module level, because the worker image has no FastAPI.

Each enum and constant is defined once. Vocabularies the interface shows are defined in `shared/definitions/` or `shared/enums/` and mirrored under `frontend/src/lib/config/` or `frontend/src/lib/types/`. Tests under `tests/grammar/` compare mirrors with their definitions, reading the frontend files from `/app/frontend-config`, a read-only mount in the development compose file.

## The MCP server

The MCP server lets AI agents query and work with reNgine. It is the `mcp/` package inside the api image and offers {{ counts.mcp_tools }} tools over three entry points:

| Transport | Entry |
|---|---|
| HTTP | `POST /api/v1/mcp`, authenticated by an `rngmcp_` token in `Authorization: Bearer`. The route is not part of the OpenAPI document. |
| stdio | `docker compose exec -T -e RENGINE_MCP_TOKEN api /app/.venv/bin/python -m mcp.stdio` |
| Chat | The `channels` service calls the same tool layer for remote control commands |

reNgine writes every tool call, refusals included, to a capped Redis list. To connect an agent, see [Agents](../agents/index.md). Every tool is listed in [MCP tools](../reference/mcp-tools.md).

## Connectors

A connector links reNgine with the proxy you test in, so findings travel to the proxy and what you browse comes back as endpoints. `connectors/` holds the proxy connectors, and the api serves them under `/api/v1/connectors`. Burp Suite is the one connector kind.

| Part | Location |
|---|---|
| Extension source | `clients/burp/`, Java on the Montoya API |
| Built extension | `binaries/rengine-connector-0.1.0.jar`, mounted read-only into the api and served for download |
| Ingest | `POST /api/v1/connectors/ingest` with an `rngconn_` token |
| Hand-off | `GET /api/v1/connectors/actions` delivers queued Repeater, Intruder, Organizer and site map actions |

reNgine writes what it sees through the proxy as `endpoints` rows with source `proxy`, into the scan that covers the target. A target with no full scan gets a `Browsing · <connector>` run instead. To set one up, see [Burp Suite](../pentesters/burp-suite.md).

## Where state lives

When you back up, debug or reset an instance, this table tells you where each kind of state is kept.

| State | Location |
|---|---|
| Entities, results, settings, token hashes | PostgreSQL |
| Resolved configuration of a run | `scans.execution_config`, secrets sealed |
| Sessions | JWTs in httpOnly cookies. Revocation state in `redis`. |
| Celery messages and results | `redis`, database `REDIS_DB` and `REDIS_DB + 1` |
| Cached aggregates | `cache` |
| Toolbox runs, MCP call log | Capped Redis lists |
| Screenshots | `scan_media/`, mounted at `/app/scan_media` |
| Check library, wordlists | Volumes `vuln_templates`, `wordlists` |
| Reports, exports, report fonts | Volumes `reports_out`, `exports_out`, `report_fonts` |
| Beat and CT stream state | Volumes `beat_state`, `ct_state` |
