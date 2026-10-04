---
title: Get started with the API
description: Use the HTTP API to pull reNgine results into your own scripts and tools, or to add targets and launch scans from them. Start here to find your base URL and the conventions every call follows.
sources:
  - api/app/main.py
  - api/app/config.py
  - api/app/api/router.py
  - api/app/api/pagination.py
  - api/app/api/scope.py
  - api/app/api/v1/celery_health.py
  - api/app/api/v1/projects.py
  - install.sh
  - docker-compose.yml
  - docker-compose.prod.yml
  - frontend/vite.config.ts
  - shared/config.py
  - shared/models/asset_query.py
  - VERSION
revised: 2026-10-03
---

The interface uses the same API, which answers JSON under `/api/v1`. There is one version, described by an OpenAPI 3.1 document with `info.version` 3.0.0.

## Find your base URL

Your base URL is the address of the reNgine interface followed by `/api/v1`. The interface, MCP clients and connectors all use it. Caddy forwards every path under `/api/` to the api service unchanged, and serves the interface for every other path.

The base URL depends on how reNgine was installed:

| Exposure | Base URL |
|---|---|
| Public domain, `--domain <name>` | `https://<name>/api/v1` |
| Server address, `--ip [address]` | `https://<address>/api/v1`, or `https://<address>:<UI port>/api/v1` |
| Local, `--local` | `http://localhost:<UI port>/api/v1` |
| API port, `--api-port <port>` | `http://127.0.0.1:<port>/api/v1` |
| Development stack | `http://127.0.0.1:8000/api/v1`, or `http://127.0.0.1:5173/api/v1` through the Vite proxy |

[Install reNgine](../../pentesters/install.md) explains the exposure modes.

### Call the api directly on the host

Use the API port when a script on the reNgine host should call the api without going through Caddy. `--api-port <port>` publishes the api service over plain HTTP on `127.0.0.1:<port>`. It is not published by default, and `--no-api-port` removes it. When the port is published, the installer prints an `API` line with `http://127.0.0.1:<port>`.

Outside `DEBUG`, the session cookies carry the `Secure` attribute. curl still sends them to `127.0.0.1` over plain HTTP, but the Python standard cookie jar, which httpx uses, does not. So on the API port, send the access token as `Authorization: Bearer` from a Python client. [Sign in to the API](authentication.md) shows how.

### Check that the api is up

Use these requests in a health check or a monitoring script.

| Request | Authentication | Response |
|---|---|---|
| `GET /api/v1/health/health` | None | `{"status": "healthy"}` |
| `GET /` on the API port | None | `{"message": "reNgine API", "version": "3.0.0"}` |
| `GET /api/v1/health/queues` | Administrator | `responded`, and per queue its `name`, `label`, `service` and number of `workers` |

## Versioning

Check these values when you generate a client or compare your code with the OpenAPI document.

| Item | Value |
|---|---|
| Path prefix | `/api/v1` |
| Versions | One. The version is part of the path. |
| OpenAPI | 3.1.0 |
| `info.title` | `reNgine` |
| `info.version` | `3.0.0`, read from the `VERSION` file of the release |
| Paths | 377 paths, 442 operations |
| Security scheme | `HTTPBearer`, `bearerFormat: JWT` |

The MCP endpoint `POST /api/v1/mcp` is left out of the document. To use it, see [Connect your agent](../../agents/mcp/connect.md).

## The OpenAPI document

The OpenAPI document describes every path, parameter and body, so you can browse the API or generate a client from it. The api service serves the document and two viewers at its own root.

| Path | Content | `DEBUG=true` | `DEBUG=false` |
|---|---|---|---|
| `/openapi.json` | OpenAPI 3.1 document | Served | 404 |
| `/docs` | Swagger UI | Served | 404 |
| `/redoc` | ReDoc | Served | 404 |

The installer writes `DEBUG=false`, so an installed instance does not serve them. The development stack runs with `DEBUG=true` and serves the document at `http://127.0.0.1:8000/openapi.json`. These paths sit outside `/api/`, so the interface origin does not route them to the api service. To read the document without a development stack, use the 3.0.0 copy this site publishes at <https://rengine.wiki/developers/api/openapi.json>, or browse [All paths](../../reference/http-api.md).

## Requests and responses

Every call follows these conventions, apart from the exceptions the table names.

| Item | Convention |
|---|---|
| Request body | JSON, `Content-Type: application/json`. `POST /api/v1/targets/import/csv` takes `multipart/form-data`. |
| Response body | JSON, except the files and streams below |
| Event streams | `GET /api/v1/events/stream` and `POST /api/v1/ask/threads/{thread_id}/messages`, `text/event-stream` |
| Plain text | `GET /api/v1/scans/compare/diff`, `text/plain` |
| Files | Export and report downloads, screenshots under `/api/v1/media`, the connector client jar |
| Timestamps | UTC `date-time` strings, for example `2026-10-01T09:12:44.512031Z` |
| Unknown body fields | Refused with 422 on bodies that forbid extra fields, such as `ScanBatchCreate` and `ExportCreate` |
| Success codes | 200, 201 on create, 202 on a queued job, 204 on delete and refresh |

[Errors, limits and counts](errors.md) explains the error answers.

## Identifiers

Resources are identified by UUIDs in their canonical text form, in paths, query parameters and bodies. Notifications are the exception and use integer identifiers.

Most operations need to know the project. They take it as the `project_id` query parameter, a UUID. The target operations take `project_slug` instead, in the query or the body. Call `GET /api/v1/projects` once to get both for every active project:

```json
[{ "id": "9b2f6d4e-1c3a-4f5b-8e7d-0a1b2c3d4e5f", "slug": "acme", "name": "acme", "is_active": true, … }]
```

## Pagination

Large lists come back one page at a time. List operations count in pages, and the dimension searches count by offset.

| Convention | Where | Parameters | Response |
|---|---|---|---|
| Page | List operations such as `GET /api/v1/targets`, `GET /api/v1/scans`, `GET /api/v1/notes`, `GET /api/v1/activity` | Query `page`, 1 to 100,000, default 1. Query `size`, 1 to 100, default 50. | `items`, `total`, `page`, `size`, `pages` |
| Offset | Dimension search bodies, `POST /api/v1/<dimension>/search` | Body `limit`, 1 to 200, default 50. Body `offset`, 0 to 100,000,000, default 0. | `items`, `total`, `total_capped`, `error` |

Two dimension searches page differently:

| Operation | Paging |
|---|---|
| `POST /api/v1/endpoints/search` | Body `page`, default 1, and `size`, default 50, clamped to 1 to 200. The response adds `page` and `size`. |
| `POST /api/v1/secrets/search` | Body `limit` 1 to 500. `offset` has no maximum. |

Search counts stop at 10,000. When more rows match, `total_capped` is `true`. See [Counts](errors.md#counts).

## Choose which results you get

The result operations need a scope: one run, or the latest results of a whole project. You set it in the query string, and you can narrow a project down to some targets.

| Parameter | Effect |
|---|---|
| `scan_id` | One run |
| `project_id` | The latest covering run of every target in the project |
| `target_id` | Only these targets. Repeatable. |
| `organization_id` | Only targets of this organization |
| `tag_id` | Only targets with this tag |

A request with neither `scan_id` nor `project_id` returns 422 `Pass scan_id for one run, or project_id for the whole project.` The web asset operations under `/api/v1/subdomains` require `project_id`.

## Tags

The OpenAPI document groups operations under tags, which helps you find the operations for one area. Tag names are written as the routers declare them, including their case and spaces. Each tag has a section in [All paths](../../reference/http-api.md), for example [scans](../../reference/http-api.md#tag-scans).

| Area | Tags |
|---|---|
| Session and accounts | `authentication`, `two-factor`, `users`, `onboarding` |
| Organisation | `projects`, `organizations`, `tags`, `targets`, `notes`, `activity`, `notifications`, `whats-new`, `dashboard` |
| Scanning | `scan-engines`, `scan-contexts`, `schedules`, `scans` |
| Results | `subdomains`, `http-assets`, `endpoints`, `ports`, `ips`, `vulnerabilities`, `software`, `secrets`, `surface`, `cves`, `domain-posture`, `lookalikes`, `interest`, `tripwires`, `exports`, `reports`, `media` |
| Libraries and intelligence | `vulnerability templates`, `wordlists`, `threat intelligence`, `Datasets`, `out-of-band testing`, `toolbox`, `tools/whois`, `viewdns` |
| Integrations | `mcp`, `remote-control`, `connectors`, `issue-trackers`, `bounty programs`, `bounty reports`, `notification-channels`, `ask`, `ai` |
| Instance | `instance-settings`, `api-keys`, `proxies`, `Health`, `events` |

Each result dimension has its own path prefix and its own search page:

| Dimension | Prefix | Search page |
|---|---|---|
| Web assets | `/api/v1/subdomains` | [Search web assets](search-web-assets.md) |
| Endpoints | `/api/v1/endpoints` | [Search endpoints](search-endpoints.md) |
| Services | `/api/v1/ports` | [Search services](search-services.md) |
| IP addresses | `/api/v1/ips` | [Search IP addresses](search-ips.md) |
| Vulnerabilities | `/api/v1/vulnerabilities` | [Search vulnerabilities](search-vulnerabilities.md) |
| Software | `/api/v1/software` | [Search software](search-software.md) |
| Secrets | `/api/v1/secrets` | [Search secrets](search-secrets.md) |

## How to read the examples

The examples on these pages use these names. Set them once in your shell and you can paste the examples as they are.

| Name | Value |
|---|---|
| `RENGINE` | The interface origin, for example `https://asm.example.com` |
| `jar` | A curl cookie jar holding the session from `POST /api/v1/auth/login` |
| `PROJECT` | A project UUID from `GET /api/v1/projects` |
| `client` | An `httpx.Client` with `base_url` set to `$RENGINE/api/v1`, signed in as shown in [Sign in to the API](authentication.md) |

```bash
# RENGINE=https://asm.example.com; jar holds the session from POST /api/v1/auth/login
curl -b jar "$RENGINE/api/v1/projects"
```
