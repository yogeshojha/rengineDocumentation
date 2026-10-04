---
title: Start a scan
description: Launch scans from your script, for example right after you add targets or on a timetable of your own. Use a saved scan engine or pick the stages in the request, and launch up to 500 targets in one call.
layout: pane
endpoint: POST /api/v1/scans/batch
sources:
  - api/app/api/v1/scans.py
  - api/app/services/scan.py
  - shared/models/scan.py
  - shared/models/scan_preview.py
  - shared/services/scan_resolve.py
  - shared/services/launch_plan.py
  - shared/services/credential_access.py
  - shared/definitions/launch.py
  - shared/definitions/constants.py
  - shared/enums/scan.py
  - stages/config.py
  - frontend/src/lib/components/scans/launch/launch-state.svelte.ts
revised: 2026-10-03
---

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Start a scan

A scan engine is a saved stage selection with settings and an intensity. Name one in the launch, or leave it out and choose the stages in the request.

1. **Find the scan engine.** `GET /api/v1/engines?project_id=<project>` lists the project's scan engines with `id`, `name` and `intensity`. The list includes the built-in engine named `Default`. <span class="rn-ref" data-tab="curl" data-mark="engines">Shown in the pane</span>
2. **Preview the run, if you want to.** `POST /api/v1/scans/preview` shows what a run would do for one target before you launch it: the stages that will run, the request rate and any warnings. It stores nothing. This step is optional.
3. **Launch.** Send the targets and the engine to `POST /api/v1/scans/batch`. Each target runs as its own scan. <span class="rn-ref" data-tab="curl" data-mark="launch">Shown in the pane</span>
4. **Follow the runs.** The answer lists one run per target, in status `pending`. Keep the run ids. You can then check on each run, as [Follow a scan](get-scan.md) shows, or follow the project's event stream.

The launch takes these fields:

| Name | In | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `project_id` | query | UUID | Yes | | Project of the targets, engine and context |
| `target_ids` | body | array of UUIDs, at most 500 | No | `[]` | Existing targets of the project |
| `target_values` | body | array of strings, at most 500 | No | `[]` | Target values. A value that is not yet a target of the project is created. |
| `engine_id` | body | UUID or null | No | `null` | Saved scan engine. Null runs every stage with its default settings, changed by `overrides`. |
| `context_id` | body | UUID or null | No | `null` | Scan context: scope, authentication, rate limits and proxy for the runs |
| `overrides` | body | object | No | `{}` | Stage settings for these runs, keyed by stage id. Applied over the engine's stage settings, or over the stage defaults without an engine. |
| `intensity` | body | string or null | No | `null` | `passive`, `normal` or `aggressive`. Null uses the engine's intensity, or `normal` without an engine. |
| `new_checks` | body | boolean or null | No | `null` | Sets **Monitor against new checks** on every target of the launch. Null leaves the targets unchanged. |

Send between 1 and 500 targets in `target_ids` and `target_values` together. A target listed twice is launched once. A field outside this table is refused with 422.

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Launch</b><span>example.com</span></div>

/// tab | curl
<div class="rn-pane-label" data-mark="engines">request · engines</div>

```bash
curl -b jar "$RENGINE/api/v1/engines?project_id=$PROJECT"
```

<div class="rn-pane-label" data-mark="launch">request · launch</div>

```bash
curl -b jar -X POST \
  "$RENGINE/api/v1/scans/batch?project_id=$PROJECT" \
  -H "Content-Type: application/json" \
  -d '{"target_values": ["example.com"],
       "engine_id": "'"$ENGINE"'"}'
```

<div class="rn-pane-label">response · 201</div>

```json
[
  {
    "id": "6f1d2c8e-5b7a-4e09-a3c4-1d2e3f4a5b6c",
    "project_id": "9b2f6d4e-1c3a-4f5b-8e7d-0a1b2c3d4e5f",
    "target_id": "2d7c9e14-5a3b-4f86-b1c0-8e9f7a6d5c4b",
    "engine_id": "0e4b6c8a-9d1f-4a3b-8c5d-7e6f5a4b3c2d",
    "engine_name": "Default",
    "context_id": null,
    "context_name": null,
    "scope": "full",
    "status": "pending",
    "execution_config": {
      "target_value": "example.com",
      "target_type": "domain",
      "intensity": "normal",
      …
    },
    "auth_summary": "None",
    "subdomains_found": 0,
    "ips_found": 0,
    "open_ports_found": 0,
    "http_assets_found": 0,
    "vulnerabilities_found": 0,
    "endpoints_found": 0,
    "error": null,
    "created_at": "2026-10-03T10:24:02.871266Z",
    "started_at": null,
    "completed_at": null,
    …
  }
]
```
///

/// tab | Python
<div class="rn-pane-label">request</div>

```python
# client: httpx.Client signed in, see Authentication
engines = client.get("/engines", params={"project_id": PROJECT}).json()
engine = next(e for e in engines if e["name"] == "Default")

r = client.post(
    "/scans/batch",
    params={"project_id": PROJECT},
    json={"target_values": ["example.com", "example.org"],
          "engine_id": engine["id"]},
)
r.raise_for_status()
for scan in r.json():
    print(scan["id"], scan["execution_config"]["target_value"],
          scan["status"])
```

<div class="rn-pane-label">response · 201</div>

```text
6f1d2c8e-5b7a-4e09-a3c4-1d2e3f4a5b6c example.com pending
a3b5c7d9-1e2f-4a6b-8c0d-2e4f6a8b0c1d example.org pending
```
///

</div>
</div>

## Choose the stages

Use `overrides` to change what runs without editing a saved engine, for example to add a port scan to one launch. With `engine_id`, `overrides` changes the engine's settings for these runs only, and the saved engine keeps its settings.

```json
{
  "target_ids": ["2d7c9e14-5a3b-4f86-b1c0-8e9f7a6d5c4b"],
  "engine_id": "0e4b6c8a-9d1f-4a3b-8c5d-7e6f5a4b3c2d",
  "overrides": { "port_scan": { "enabled": true } },
  "intensity": "aggressive"
}
```

These rules decide how reNgine reads `overrides`:

| Rule | Behaviour |
|---|---|
| Keys | Stage ids, such as `port_scan`. See [Stages](../../reference/stages/index.md). |
| Values | Settings of that stage. `enabled` turns the stage on or off. |
| Unknown stage | 400 `Unknown stage '{name}' in run overrides.` |
| Unknown setting | 400 `{stage} has no setting named '{setting}'.` |
| Invalid value | 400 `{stage}.{setting}: {reason}` |
| Stages that always run | `enabled` is ignored |
| Passive intensity | Every stage that sends traffic to the target and does not support passive intensity is disabled |

A run without an engine is named after its stages. The interface sends `overrides` and `intensity` only for **Custom scan**, and sends neither with a scan engine. See [Run a scan](../../pentesters/run-a-scan.md) and [Scan engines and intensity](../../pentesters/scan-engines.md).

## Response

You get 201 with a list of `ScanRead`, one per target, in the order `target_ids` then `target_values`. Each run starts in status `pending` and is queued. If a run cannot be queued, it comes back with status `failed` and `error` `Not queued. Check that the worker is running.`

A run stays in `pending` while the instance is already running its limit of concurrent scans, and starts when a slot frees up. [Follow a scan](get-scan.md#response) lists the fields of `ScanRead`.

## Preview a run

A preview lets your script check a launch before it sends any traffic: which stages will run, how fast, and what might stop them. `POST /api/v1/scans/preview` resolves the same configuration for one target and returns what the run would do. It creates no scan and no target.

It takes these fields:

| Name | In | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `project_id` | query | UUID | Yes | | Project |
| `target_id` | body | UUID or null | One of the two | `null` | An existing target |
| `target_value` | body | string or null, at most 500 characters | One of the two | `null` | A target value, not stored |
| `engine_id` | body | UUID or null | No | `null` | Saved scan engine |
| `context_id` | body | UUID or null | No | `null` | Scan context |
| `overrides` | body | object | No | `{}` | Stage settings, as in the launch |
| `intensity` | body | string or null | No | `null` | Run intensity |

Send exactly one of `target_id` and `target_value`. A body with both or neither returns 422 `Value error, Provide either target_id or target_value.`

The preview answers with these fields:

| Response field | Content |
|---|---|
| `target_value`, `target_type`, `engine_name`, `context_name` | The resolved launch |
| `phases[]` | `phase`, `label` and `tools[]`. Each tool has `capability`, `label`, `status`, `reason`, `rate`, `threads` and `timeout`. |
| `phases[].tools[].status` | `will_run`, `skipped_disabled`, `skipped_needs_key`, `skipped_not_applicable` or `skipped_no_input` |
| `summary` | `auth_summary`, `rate_summary`, `thread_multiplier`, `timeout_multiplier`, `http_protocol`, `follow_redirects`, exclusions, `seed_count`, `proxy_name`, `estimated_duration_seconds` and `estimated_duration_human` |
| `warnings[]` | Sentences such as `1 run in progress on example.com.` |

`summary.rate_summary` reads `~{n}/s to target`, or `no target traffic`, followed by `, ceiling {n}/s per tool` when the context sets a ceiling.

## Pause, resume or cancel a run

Use these operations to stop a run that is hitting the wrong thing, or to pause it and carry on later. The second column shows the statuses in which each one works.

| Operation | Accepted in | Effect | Refusal |
|---|---|---|---|
| `POST /api/v1/scans/{id}/pause` | `running` | Stops the stages in progress. Their activities become `paused` and their commands `aborted`. The run becomes `paused`. | 409 `The scan is not running.` 409 `A watch probe cannot be paused. Cancel it to stop the run.` |
| `POST /api/v1/scans/{id}/resume` | `paused` | The run becomes `running` and the stages left are queued again. | 409 `The scan is not paused.` 503 `The scan was not resumed. Check that the worker service is running.` |
| `POST /api/v1/scans/{id}/cancel` | `pending`, `running`, `paused` | The run becomes `cancelled` with `error` `Cancelled by user.` Unfinished activities and commands become `aborted`. A run in another status is returned unchanged. | |
| `POST /api/v1/scans/cancel-all` | | Cancels every open run of the project, or of the repeated `target_id` query values. Returns `{"cancelled": n}`. | |
| `DELETE /api/v1/scans/{id}` | Any status | Deletes the run and the rows it recorded. 204. | |

Each one takes `project_id` in the query. Pause, resume and cancel return the updated `ScanRead`.

## Errors

If the launch is refused, find its status and `detail` below.

| Status | `detail` | What to do |
|---|---|---|
| 400 | `Unrecognised target: {value}. Enter a domain, IP address, CIDR range, URL or ASN.` | Correct the value in `target_values`. |
| 400 | `Intensity must be one of passive, normal, aggressive.` | Send a listed intensity. |
| 400 | `Unknown stage '{name}' in run overrides.` | Use a stage id from [Stages](../../reference/stages/index.md). |
| 403 | `Engine {name} carries credentials. Its creator or an administrator can launch with it.` | Launch as the engine's creator or an administrator. |
| 403 | `Context {name} carries credentials. Its creator or an administrator can launch with it.` | Launch as the context's creator or an administrator. |
| 404 | `Scan engine not found` | Send an engine of the project. |
| 404 | `Scan context not found` | Send a context of the project. |
| 404 | `Target not found: {id}` | Send targets of the project. |
| 404 | `Project not found` | Send an existing `project_id`. |
| 422 | `Value error, Select at least one target.` | Send a target. |
| 422 | `Value error, Select at most 500 targets.` | Split the launch. |
