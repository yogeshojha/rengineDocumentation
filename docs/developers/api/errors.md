---
title: Errors, limits and counts
description: See how the API tells your script that a call failed, that a query did not parse or that it hit a limit, so you can handle each case. This page also explains how to read counts, including when they are capped and when a missing count is not a zero.
sources:
  - api/app/main.py
  - api/app/core/validation_errors.py
  - api/app/core/db_errors.py
  - api/app/core/secret_errors.py
  - api/app/core/sanitize.py
  - api/app/core/throttle.py
  - api/app/core/body_limit.py
  - api/app/core/ratelimit.py
  - api/app/api/scope.py
  - api/app/api/v1/events.py
  - api/app/api/v1/toolbox.py
  - api/app/api/v1/viewdns.py
  - api/app/api/v1/mcp.py
  - api/app/api/v1/connectors.py
  - api/app/services/subdomain.py
  - api/app/services/endpoint.py
  - api/app/services/export.py
  - api/app/services/target_summary.py
  - api/app/services/target.py
  - shared/definitions/asset_query.py
  - shared/services/asset_query/parser.py
  - shared/services/asset_query/errors.py
  - shared/services/asset_query/leads.py
  - shared/models/asset_query.py
  - shared/models/target_summary.py
  - shared/services/scan_scope.py
  - shared/utils/crypto.py
  - shared/sse.py
revised: 2026-10-03
---

Most failures come back as an HTTP status with a JSON `detail`. One case differs: a search whose query does not parse still returns 200, with an `error` object and no rows, so check `error` before you trust a search result.

## Status codes

Use this table to decide how your script reacts to each status.

| Code | Use |
|---|---|
| 200 | Success. Also a search whose query did not parse or that the database refused. See [Query errors](#query-errors). |
| 201 | Resource created |
| 202 | Job queued: exports, reports, issue creation, interest judging, bounty report sync |
| 204 | No body: deletions and `POST /api/v1/auth/refresh` |
| 400 | A value is refused: an unrecognised target, an invalid stage override, a value longer than its column, a NUL byte in the query string |
| 401 | No session, or an expired, revoked or wrong-type token. See [Sign in to the API](authentication.md). |
| 403 | Inactive account, administrator-only operation, an engine or context that carries credentials, a feature of the other instance mode |
| 404 | The resource does not exist in the project |
| 409 | State conflict: a target that exists, a scan that is not running or not paused, too many exports running |
| 413 | Request body over the size limit |
| 422 | Request validation, a run comparison refusal, a result operation without a scope |
| 424 | A ViewDNS lookup without a configured key |
| 429 | Rate limit |
| 502 | An upstream service failed: WHOIS refresh, ViewDNS lookup, issue tracker |
| 503 | A dependency is unavailable: the rate limiter, the worker on resume, the event stream capacity, a stored secret that cannot be decrypted |

## Error bodies

Every error body is a JSON object with one key, `detail`. Its shape tells you what kind of error you got.

An application error carries a string:

```json
{ "detail": "Scan not found" }
```

A request validation error, 422, carries a list. Each item has `type`, `loc` and `msg`, so you can point at the field that was refused. The submitted value is not echoed back.

```json
{
  "detail": [
    { "type": "missing", "loc": ["query", "project_id"], "msg": "Field required" },
    { "type": "value_error", "loc": ["body"], "msg": "Value error, Select at least one target." }
  ]
}
```

A rule that spans several fields reports `loc` `["body"]` and a `msg` that starts with `Value error, `.

If you send a value the database cannot store, you get 400 with one of these messages:

| `detail` | Cause |
|---|---|
| `A value in the request is longer than the field allows.` | A string over the column length |
| `A number in the request is outside the range the field allows.` | A number over the column range |
| `A value in the request contains a NUL byte.` | A NUL character in a stored string |
| `A value in the request is not valid for its field.` | Any other data exception |

These errors concern the request as a whole:

| Status | `detail` |
|---|---|
| 400 | `Query parameters must not contain NUL bytes.` |
| 413 | `The request body is larger than the 128 MB limit.` |
| 413 | `The request body is larger than the 64 KB limit.` |
| 503 | `{label} was sealed with a different SECRET_KEY and cannot be read. Restore the SECRET_KEY this instance was set up with, or enter the credential again.` |

## Query errors

When your query has a mistake, the search tells you where it is and how to fix it. The dimension search operations, `POST /api/v1/<dimension>/search`, return a query language error as 200 with an `error` object, an empty `items` list and `total` 0. When `error` is set, `total` is not a match count.

```json
{
  "items": [],
  "total": 0,
  "total_capped": false,
  "error": {
    "message": "Unclosed group.",
    "hint": "Close it with ).",
    "start": 15,
    "end": 26
  }
}
```

This response answers `{"q": "status:200 and (tech:nginx"}`. The `error` object holds these fields, which you can use to underline the faulty part of the query:

| Field | Type | Description |
|---|---|---|
| `message` | string | What is wrong |
| `hint` | string or null | How to correct it |
| `start` | integer | Offset of the first character of the faulty part in `q` |
| `end` | integer | Offset after the last character of the faulty part. `start` and `end` are 0 when the database refused the query. |

A query can also parse and then fail while the database runs it. You then get one of these:

| `message` | `hint` |
|---|---|
| `Invalid regular expression.` | `PostgreSQL regular expression syntax applies.` |
| `The search timed out.` | `Add a field filter.` |
| `A number is out of range.` | |
| `A value has the wrong type.` | |
| `A search term is too long to index.` | |

The grammar and the field list of each dimension are in [Query language](../../reference/query/index.md).

### Query limits

Keep your queries inside these limits. The last column shows what you get when one is exceeded.

| Limit | Value | Outcome |
|---|---|---|
| Length of `q` | 2,000 characters | 422 on the search body |
| Parts of one query | 40 | `The query has too many parts.` |
| Free-text words | 8 | `Too many free-text words.` with `Use at most 8, or narrow with a field.` |
| Length of a regular expression | 200 characters | `The regular expression is too long.` |
| Statement time | 20 seconds | `The search timed out.` |
| Queries in one `POST /api/v1/<dimension>/search/counts` | 32 | 422 |

## Global rate limit

Every user, or client address when there is no valid session, gets one budget of requests per minute. If your script sends many requests, pace them or retry after the time the API gives you.

| Item | Value |
|---|---|
| Limit | `GLOBAL_RATE_LIMIT_PER_MINUTE`, default 600 requests |
| Window | The calendar minute |
| Key | The user named by a valid access token, from the bearer header or the `access_token` cookie. Otherwise the client address. |
| Exempt | `OPTIONS` requests, paths under `/api/v1/events` and `/api/v1/media` |
| Disabled | A limit of 0 or less |
| Redis unreachable | The limit is not applied |

A request over the limit gets this answer:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 23
Content-Type: application/json

{"detail": "Rate limit exceeded. Try again in a minute."}
```

`Retry-After` holds the seconds left in the current minute, so wait that long before you retry.

### Operation limits

Some operations have limits of their own, on top of the global one:

| Operation | Limit | Response |
|---|---|---|
| Sign-in and second factor | See [Sign-in limits](authentication.md#sign-in-limits) | 429 `Too many attempts. Try again in {n} seconds.` |
| `POST /api/v1/mcp` with an unknown token | 20 failures per client address in 15 minutes | 429 `Too many attempts. Try again in {n} seconds.` |
| Connector operations with an unknown token | 20 failures per client address in 15 minutes | 429 `Too many attempts. Try again in {n} seconds.` |
| Toolbox runs | 30 per user per minute | 429 `Too many toolbox runs. Try again in a minute.` |
| ViewDNS lookups | 30 per user and lookup kind per minute | 429 `Too many attempts. Try again in {n} seconds.` |
| `POST /api/v1/scans/batch` | 500 targets | 422 `Value error, Select at most 500 targets.` |
| `POST /api/v1/exports` | 3 queued or running exports per project | 409 `{n} exports are running. Wait for one to finish.` |
| `GET /api/v1/events/stream` | 1,000 streams per api process | 503 `Too many event streams` |

## Body size limits

These limits apply to the size of what you send:

| Path | Limit | Response |
|---|---|---|
| Under `/api/v1/auth/` | 64 KB | 413 `The request body is larger than the 64 KB limit.` |
| Every other path | 128 MB | 413 `The request body is larger than the 128 MB limit.` |
| `POST /api/v1/targets/import/csv` file | 10 MB | 400 `The CSV file is larger than the 10 MB limit.` |

Caddy applies the same 128 MB limit to `/api/*` on the interface origin.

## Counts

Counts tell you how many rows match before you page through them. Read them with the rules below, so a capped count or a missing count does not mislead your script.

### The cap

Search counts stop at 10,000. Two fields tell you whether the count is exact:

| Field | Value |
|---|---|
| `total` | The number of matching rows, or 10,000 when more match |
| `total_capped` | `true` when more than 10,000 rows match |

Lead, tab and count operations apply the same cap to each count and return a `capped` flag beside it. These counts use the scope, the filter and the query compiler of the search they open, so a count equals the rows the matching search returns, up to the cap.

### Counts that were not computed

An empty or missing count is not a zero. These cases tell you that no count was computed:

| Response | Meaning |
|---|---|
| `QueryCounts` or `QueryLeads` with `computed: false` | No count was computed. The query did not compile or the database refused it. The empty `counts` is not a zero count. |
| A query absent from `counts` in `POST /api/v1/<dimension>/search/counts` | That query did not compile |
| `error` set on a search response | `total` is not a match count |

### Not scanned and zero

"Nothing found" and "never looked" are different answers, and the API keeps them apart. A dimension that no run produced is reported as not scanned, not as zero. A run covers a dimension when a stage that produces it succeeded or when the run wrote rows for it.

This is how each response tells the two cases apart:

| Response | Not scanned | Scanned, nothing found |
|---|---|---|
| `GET /api/v1/targets/{target_id}/summary`, `surface[]` | `covered: false`, `value: null` | `covered: true`, `value: 0` |
| `ScanRead.findings` on a run | `covered: false` | `covered: true` with zero counts |
| `GET /api/v1/scans/compare`, `dimensions[].verdict` | `comparability: "not_covered"` and a `note` | Counts of 0 |

In the target summary, `previous` and `delta` are null when only one run covered the dimension.

### New rows

`is:new` and the `new` body filter show what appeared since earlier runs, so they need an earlier run to compare with, a baseline. A row is new when an earlier run of its target recorded rows of the dimension and none of the earlier runs recorded that row. The first run of a target reports no row as new.
