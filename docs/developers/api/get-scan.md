---
title: Follow a scan
description: Check on a run from your script, with its status, its stages, the commands it ran and what it has found so far. Poll the run, or follow the event stream to react as soon as something changes.
layout: pane
endpoint: GET /api/v1/scans/{id}
sources:
  - api/app/api/v1/scans.py
  - api/app/services/scan.py
  - api/app/api/v1/events.py
  - api/app/api/deps.py
  - shared/models/scan.py
  - shared/models/scan_activity.py
  - shared/models/scan_command.py
  - shared/enums/scan.py
  - shared/enums/sse.py
  - shared/enums/scan_schedule.py
  - shared/sse.py
  - shared/services/orchestrator/events.py
  - shared/services/orchestrator/aggregate.py
  - shared/services/scan_resolve.py
  - shared/definitions/vulnerabilities.py
revised: 2026-10-03
---

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Read a run

Use these calls to wait for a run to finish before you read its results, or to show its progress in your own tool. The Python tab polls a run until it settles.

1. **Read the run.** `GET /api/v1/scans/{id}` with `project_id` returns `ScanRead`: the status, the counts per dimension and what changed since the last run. <span class="rn-ref" data-tab="curl" data-mark="get">Shown in the pane</span>
2. **See each stage.** `GET /api/v1/scans/{id}/activities` returns one activity per stage with its status and figures. <span class="rn-ref" data-tab="curl" data-mark="activities">Shown in the pane</span>
3. **See the commands, if you need to debug.** `GET /api/v1/scans/{id}/commands` lists the tool commands of the run. `GET /api/v1/scans/{id}/commands/{command_id}` adds the output.
4. **Follow the run live.** Instead of polling, `GET /api/v1/events/stream?channels=project:<project_id>` streams the scan events of the project as they happen. <span class="rn-ref" data-tab="curl" data-mark="events">Shown in the pane</span>
5. **Read the results.** Call the search operation of a dimension with `scan_id`. See [Search web assets](search-web-assets.md).

`GET /api/v1/scans/{id}` takes these parameters:

| Name | In | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `id` | path | UUID | Yes | | Run identifier |
| `project_id` | query | UUID | Yes | | Project of the run |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Run</b><span>example.com</span></div>

/// tab | curl
<div class="rn-pane-label" data-mark="get">request · run</div>

```bash
curl -b jar "$RENGINE/api/v1/scans/$SCAN?project_id=$PROJECT"
```

<div class="rn-pane-label">response · 200</div>

```json
{
  "id": "6f1d2c8e-5b7a-4e09-a3c4-1d2e3f4a5b6c",
  "target_id": "2d7c9e14-5a3b-4f86-b1c0-8e9f7a6d5c4b",
  "engine_name": "Default",
  "scope": "full",
  "status": "completed",
  "auth_summary": "None",
  "subdomains_found": 42,
  "http_assets_found": 31,
  "vulnerabilities_found": 7,
  "error": null,
  "started_at": "2026-10-03T10:24:05.112840Z",
  "completed_at": "2026-10-03T10:51:47.903114Z",
  "duration_seconds": 1662.8,
  "new_subdomains": 3,
  "gone_subdomains": 1,
  "prev_subdomains_found": 40,
  "is_first_scan": false,
  "findings": {
    "critical": 0, "high": 1, "medium": 2,
    "covered": true,
    "scan_id": null
  },
  "queue_position": null,
  …
}
```

<div class="rn-pane-label" data-mark="activities">request · activities</div>

```bash
curl -b jar "$RENGINE/api/v1/scans/$SCAN/activities?project_id=$PROJECT"
```

<div class="rn-pane-label">response · 200</div>

```json
[
  {
    "id": "c2e4a6b8-0d1f-4e3a-9b5c-7d9e1f3a5b7c",
    "name": "http_probe",
    "title": "HTTP Probe",
    "status": "success",
    "duration_seconds": 48.3,
    "figures": [ … ],
    …
  }
]
```

<div class="rn-pane-label" data-mark="events">request · events</div>

```bash
curl -N -b jar \
  "$RENGINE/api/v1/events/stream?channels=project:$PROJECT"
```

<div class="rn-pane-label">stream</div>

```text
event: message
data: {"channel": "project:9b2f…", "type": "scan", "data": {"kind": "stage_started", "scan_id": "6f1d…", "activity_id": "c2e4…", "stage": "http_probe", "title": "HTTP Probe"}, "ts": "2026-10-03T10:30:12.408211+00:00"}

: heartbeat
```
///

/// tab | Python
<div class="rn-pane-label">poll until the run settles</div>

```python
# client: httpx.Client signed in, see Authentication
import time

OPEN = {"pending", "running", "paused"}
params = {"project_id": PROJECT}

while True:
    scan = client.get(f"/scans/{SCAN}", params=params).json()
    if scan["status"] not in OPEN:
        break
    time.sleep(30)

print(scan["status"], scan["duration_seconds"], scan["error"])
for a in client.get(f"/scans/{SCAN}/activities", params=params).json():
    print(a["name"], a["status"], a["duration_seconds"])
```

<div class="rn-pane-label">output</div>

```text
completed 1662.8 None
subdomain_discovery success 312.4
http_probe success 48.3
…
```
///

</div>
</div>

## Response

You get 200 with a `ScanRead`. The launch, pause, resume and cancel operations and `GET /api/v1/scans` return the same model, so the fields below apply to all of them.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Run identifier |
| `project_id`, `target_id` | UUID | Project and target of the run |
| `engine_id` | UUID or null | Saved scan engine. Null for a run without one. |
| `engine_name` | string | Engine name, or the name built from the stages of a run without an engine |
| `context_id`, `context_name` | UUID, string, or null | Scan context of the run |
| `schedule_id` | UUID or null | Schedule that launched the run |
| `schedule_type` | string or null | `one_off`, `interval`, `daily_at` or `cron` |
| `scope` | string | `full`, or `focused` for a focused rescan |
| `parent_scan_id` | UUID or null | Focused rescans: the run the assets were chosen from |
| `run_group_id` | UUID or null | Focused rescans: the runs launched by one request |
| `seed_count` | integer | Seed assets in the run configuration |
| `execution_config` | object | The resolved configuration: `target_value`, `target_type`, `intensity`, `stages`, `transports`, `per_tool_rate_limits`, exclusions and `overrides`. Header values, the proxy URL and tool options that carry credentials are masked. |
| `auth_summary` | string | `None`, `Bearer ••••`, `Basic · {user}`, `Cookie ••••`, a header name, an API key name, or `{n} headers` |
| `status` | string | See [Statuses](#statuses) |
| `subdomains_found`, `http_assets_found`, `endpoints_found`, `open_ports_found`, `ips_found`, `vulnerabilities_found` | integer | Counters of the run per dimension. The search operation of a dimension, called with `scan_id`, returns the rows. |
| `error` | string or null | Reason of a failed or cancelled run |
| `created_by`, `created_at` | UUID, date-time | Launching user and creation time |
| `started_at`, `completed_at` | date-time or null | Start and end of the run |
| `paused_at` | date-time or null | Start of the current pause |
| `paused_seconds` | number | Time spent paused |
| `duration_seconds` | number or null | Running time without paused time, to one decimal. An open run reports the time up to now. |
| `new_subdomains` | integer or null | Web assets this run was the first to report for its target |
| `gone_subdomains` | integer or null | Web assets of the previous completed run that this run did not report |
| `prev_subdomains_found` | integer or null | For a completed full run, `subdomains_found` of the previous completed full run of the target. Null otherwise. |
| `is_first_scan` | boolean or null | The run is the first full run of its target |
| `rescans` | object or null | Focused rescans launched from this run: `total`, `running`, `failed` |
| `recheck` | object or null | Focused runs: `assets`, `changed` and per-field counts |
| `findings` | object or null | Open findings of the run with severity `critical`, `high` and `medium`, excluding findings a reviewer set aside, and `covered` |
| `target_runs` | integer or null | Runs of the target. Set by `GET /api/v1/scans` with `latest=true`. |
| `queue_position` | integer or null | Runs ahead of a `pending` run held by the instance limit on concurrent scans |

Check `findings.covered` before you report zero findings. It is `true` when the run wrote findings or a stage that covers vulnerabilities ended `success` or `partial`. A run with `covered: false` did not look for vulnerabilities at all. See [Not scanned and zero](errors.md#not-scanned-and-zero).

The launch, pause, resume and cancel operations leave out the delta fields: `new_subdomains`, `gone_subdomains`, `prev_subdomains_found`, `is_first_scan`, `rescans`, `recheck`, `findings` and `queue_position` are null there. Call `GET /api/v1/scans/{id}` to get them.

## Statuses

The status tells your script whether to keep waiting:

| Status | Meaning |
|---|---|
| `pending` | Created and queued. Waits for the worker, or for a slot under the instance limit on concurrent scans. |
| `running` | Stages are executing |
| `paused` | Stopped by `POST /api/v1/scans/{id}/pause`. `POST /api/v1/scans/{id}/resume` queues the stages left. |
| `completed` | Every stage ended `success`, `partial` or `skipped` |
| `failed` | A stage failed, or the run could not be queued |
| `cancelled` | Cancelled by `POST /api/v1/scans/{id}/cancel`, `error` `Cancelled by user.` |

`pending`, `running` and `paused` are open statuses: the run can still produce rows. `completed`, `failed` and `cancelled` are final.

## Activities

Activities show what each stage did, which helps you see why a run is `partial` or `failed`. `GET /api/v1/scans/{id}/activities?project_id=<project>` returns one `ScanActivityRead` per stage, ordered by creation.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Activity identifier |
| `scan_id` | UUID | Run |
| `name` | string | Stage id. See [Stages](../../reference/stages/index.md). |
| `title` | string | Stage title |
| `status` | string | `pending`, `running`, `paused`, `success`, `partial`, `failed`, `skipped` or `aborted` |
| `error` | string or null | Error text of the stage |
| `result` | object | Stage result data |
| `figures` | array | `key`, `value` and `label` of each figure the stage reports |
| `created_at`, `started_at`, `completed_at` | date-time | Creation, start and end |
| `duration_seconds` | number or null | End minus start, to one decimal |

## Commands

Commands show the tool command lines a run started and their exit codes. Read them when a stage fails and you want to see what the tool did. `GET /api/v1/scans/{id}/commands?project_id=<project>` returns the tool commands of the run, ordered by start. `activity_id` limits the list to one stage.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Command identifier |
| `activity_id` | UUID or null | Stage activity |
| `tool` | string | Tool name |
| `command` | string | The command line, with credentials redacted |
| `status` | string | An activity status |
| `return_code` | integer or null | Exit code |
| `error` | string or null | Error text |
| `started_at`, `completed_at`, `duration_seconds` | | Timing |

`GET /api/v1/scans/{id}/commands/{command_id}?project_id=<project>` returns the same fields and `output`, with credentials redacted.

## Event stream

The event stream tells you about a run the moment something happens, so your script does not have to poll. `GET /api/v1/events/stream` streams server-sent events. It authenticates with the `access_token` cookie or a bearer header.

| Name | In | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `channels` | query | string | Yes | | Comma-separated channels: `project:<project_id>` for the events of a project, `broadcast` for notifications |

Each event arrives as one `message` frame whose `data` is a JSON object:

| Key | Content |
|---|---|
| `channel` | The channel the event was published on |
| `type` | `scan`, `activity` or `notification` |
| `data` | The event payload |
| `ts` | Publication time |

An `activity` event carries an entry of the project activity log. A `notification` event is published on `broadcast`. A `scan` event carries `kind` and `scan_id` in `data`. Use `kind` to decide what to do, and read the fields that come with it:

| `kind` | Fields |
|---|---|
| `scan_started` | `status`, `engine` |
| `stage_started` | `activity_id`, `stage`, `title` |
| `stage_progress` | `activity_id`, `stage`, `message`, `source` |
| `command_started` | `command_id`, `activity_id`, `tool`, `command` |
| `command_finished` | `command_id`, `activity_id`, `tool`, `return_code`, `status`, `duration_seconds` |
| `results_found` | `dimension`, `counts` |
| `stage_completed` | `activity_id`, `stage`, `status`, `counts` |
| `scan_paused` | `status`, `stages_stopped` |
| `scan_resumed` | `status`, `stages_left` |
| `scan_completed` | `status`, `counts`, `duration_seconds` |
| `scan_failed` | `status`, `error` |
| `scan_cancelled` | `status` |
| `interest_ready` | `hosts`, `signals`, `bands`, `ai_used` |

Your client has to handle these cases to keep the stream open:

| Rule | Behaviour |
|---|---|
| Heartbeat | After 30 seconds without an event, the stream checks the token and sends `: heartbeat` |
| Expired or revoked token | The stream sends `event: unauthorized` and closes. Refresh the session and reconnect. |
| Slow reader | A stream with 100 undelivered events is closed |
| Capacity | 1,000 streams per api process |
| Rate limit | The stream path is exempt from the global rate limit |

## List runs

To find a run you did not launch yourself, list them. `GET /api/v1/scans?project_id=<project>` lists runs, newest start first, paged with `page` and `size`. Filters: `target_id` and `status`, repeatable, `engine`, `search`, `severity`, `short`, `added`, `started_from`, `started_to`, `include_focused` and `latest`. `sort_by` takes `started`, `duration`, `status`, `subdomains` or `vulnerabilities`, and `sort_dir` takes `asc` or `desc`.

## Errors

If a call is refused, find its status and `detail` below.

| Status | `detail` | What to do |
|---|---|---|
| 404 | `Scan not found` | Send a run of the project. |
| 404 | `Command not found` | Send a command of the run. |
| 400 | `At least one channel is required` | Send `channels`. |
| 403 | `No valid channels in request` | Send `project:<project_id>` or `broadcast`. |
| 503 | `Too many event streams` | Close unused streams. |
| 422 | Validation list | Send `id` and `project_id` as UUIDs. |
