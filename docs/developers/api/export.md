---
title: Export results
description: Download the results of a run, a target or a whole project as a CSV, JSON or plain text file, for a spreadsheet, a report or another tool. reNgine writes the file in the background and keeps it for 30 days.
layout: pane
endpoint: POST /api/v1/exports
sources:
  - api/app/api/v1/exports.py
  - api/app/services/export.py
  - worker/app/tasks/export.py
  - shared/definitions/exports.py
  - shared/definitions/surface.py
  - shared/models/export.py
  - shared/services/asset_export/runner.py
  - shared/services/asset_export/columns.py
  - shared/services/asset_export/writer.py
  - shared/services/surface_query/__init__.py
revised: 2026-10-03
---

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Export results

Use an export when you need more rows than a search page returns, or a file you can hand to someone. A search filter narrows the file to the rows you care about, such as `is:live`. reNgine writes the file in the background, so you create the export, wait for it, then download it.

1. **Create the export.** Send the dimension, the scope and the search filter to `POST /api/v1/exports`. You get 202 with the export in status `queued`. <span class="rn-ref" data-tab="curl" data-mark="create">Shown in the pane</span>
2. **Wait for it to finish.** Poll `GET /api/v1/exports/{export_id}`. It reports `status`, `progress` from 0 to 100 and the current `step`. <span class="rn-ref" data-tab="curl" data-mark="poll">Shown in the pane</span>
3. **Download the file.** When `status` is `completed`, `GET /api/v1/exports/{export_id}/download` returns the file, with its name in `Content-Disposition`. <span class="rn-ref" data-tab="curl" data-mark="download">Shown in the pane</span>

| Name | In | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `project_id` | query | UUID | Yes | | Project |
| `dimension` | body | string, at most 32 characters | Yes | | `web_assets`, `endpoints`, `services`, `ips`, `vulnerabilities`, `software` or `secrets`. `bundle` writes every dimension into one ZIP archive. |
| `scan_id` | body | UUID or null | No | `null` | Export the rows of one run |
| `target_id` | body | UUID or null | No | `null` | Export the latest covering run of one target. Not read when `scan_id` is set. |
| `export_format` | body | string, at most 16 characters | No | `csv` | `csv`, `json` or `txt` |
| `filters` | body | object | No | `{}` | The search body of the dimension, such as `{"q": "is:live"}`. Not read for `bundle`. |
| `include_evidence` | body | boolean | No | `false` | For `vulnerabilities`, adds the `curl_command`, `request` and `response` columns |

A field outside this table is refused with 422.

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Export</b><span>example.com</span></div>

/// tab | curl
<div class="rn-pane-label" data-mark="create">request · create</div>

```bash
curl -b jar -X POST "$RENGINE/api/v1/exports?project_id=$PROJECT" \
  -H "Content-Type: application/json" \
  -d '{"dimension": "web_assets",
       "scan_id": "'"$SCAN"'",
       "export_format": "csv",
       "filters": {"q": "is:live"}}'
```

<div class="rn-pane-label">response · 202</div>

```json
{
  "id": "e5f7a9b1-3c4d-4e6f-8a0b-2c4d6e8f0a1b",
  "dimension": "web_assets",
  "scope": "scan",
  "subject": "example.com",
  "query": "is:live",
  "export_format": "csv",
  "status": "queued",
  "progress": 0,
  "step": "",
  "filename": null,
  "row_count": 0,
  "total_rows": 0,
  "capped": false,
  "expires_at": null,
  …
}
```

<div class="rn-pane-label" data-mark="poll">request · poll</div>

```bash
curl -b jar "$RENGINE/api/v1/exports/$EXPORT?project_id=$PROJECT"
```

<div class="rn-pane-label">response · 200</div>

```json
{
  "status": "completed",
  "progress": 100,
  "step": "Ready",
  "filename": "web-assets-example-com.csv",
  "bytes_written": 5821,
  "row_count": 31,
  "total_rows": 31,
  "capped": false,
  "expires_at": "2026-11-02T10:58:13.402917Z",
  …
}
```

<div class="rn-pane-label" data-mark="download">request · download</div>

```bash
curl -b jar -OJ \
  "$RENGINE/api/v1/exports/$EXPORT/download?project_id=$PROJECT"
```
///

/// tab | Python
<div class="rn-pane-label">create, poll, download</div>

```python
# client: httpx.Client signed in, see Authentication
import time

params = {"project_id": PROJECT}
r = client.post("/exports", params=params, json={
    "dimension": "vulnerabilities",
    "target_id": TARGET,
    "export_format": "json",
    "filters": {"q": "severity:[critical,high]"},
    "include_evidence": True,
})
r.raise_for_status()
export = r.json()

while export["status"] in ("queued", "running"):
    time.sleep(5)
    export = client.get(f"/exports/{export['id']}", params=params).json()

if export["status"] != "completed":
    raise RuntimeError(export["error"])

file = client.get(f"/exports/{export['id']}/download", params=params)
with open(export["filename"], "wb") as out:
    out.write(file.content)
print(export["row_count"], "rows", "capped" if export["capped"] else "")
```
///

</div>
</div>

## Scope

The scope decides which run's rows go into the file. reNgine resolves it when the export runs, not when you create it.

| Request | `scope` | Rows |
|---|---|---|
| `scan_id` | `scan` | The run |
| `target_id` | `target` | The latest run of the target that covered the dimension |
| Neither | `project` | The latest covering run of every target in the project |

For a `bundle` with `target_id` or no scope, each dimension takes its own latest covering run.

## Formats

Pick CSV for a spreadsheet, JSON for another program, and plain text when you want a list of values to feed into a tool.

| `export_format` | Content | Media type |
|---|---|---|
| `csv` | UTF-8 with a byte order mark and a header row. Lists are joined with `; `, booleans are `true` or `false`, objects are written as JSON. A cell that starts with `=`, `+`, `-`, `@`, a tab or a carriage return is prefixed with `'`. | `text/csv` |
| `json` | An array with one object per row, keyed by column | `application/json` |
| `txt` | One value per line, empty values left out | `text/plain` |
| `bundle` with any format | A ZIP archive of one file per dimension, named `{dimension}.{csv,json,txt}` | `application/zip` |

A `txt` file holds one value per row. This table shows which value each dimension writes:

| Dimension | Value |
|---|---|
| `web_assets` | `name` |
| `endpoints` | `url` |
| `services` | `ip` and `port` as `host:port` |
| `ips` | `ip` |
| `vulnerabilities` | `matched_at` |
| `software` | `cve` |
| `secrets` | `value` |

reNgine names the file after the dimension label followed by the subject, in lowercase with hyphens, for example `web-assets-example-com.csv` or `all-dimensions-acme.zip`. The subject is the target value for a run or target scope and the project name for a project scope.

## Columns

CSV and JSON files hold these columns, in this order, so you can rely on them when you read the file in another tool.

| Dimension | Columns |
|---|---|
| `web_assets` | `name`, `http_status`, `page_title`, `http_url`, `tech`, `webserver`, `resolved_ips`, `cname`, `is_cdn`, `cdn_name`, `waf`, `asn_org`, `ports`, `tls_expired` |
| `endpoints` | `url`, `host`, `path`, `status_code`, `content_type`, `content_length`, `title`, `methods`, `param_count`, `endpoint_class`, `interest`, `primary_source`, `is_probed`, `is_new` |
| `services` | `ip`, `port`, `protocol`, `service_name`, `service_class`, `product`, `version`, `is_http`, `tls`, `status_code`, `title`, `url`, `hosts`, `asn_org`, `country`, `is_cdn`, `is_sensitive`, `source`, `is_new` |
| `ips` | `ip`, `version`, `asn`, `asn_org`, `country`, `prefix`, `is_cdn`, `cdn_name`, `is_alive`, `ports`, `port_count`, `host_count`, `hosts`, `has_sensitive` |
| `vulnerabilities` | `fingerprint`, `template_id`, `template_name`, `severity`, `scanner`, `matched_at`, `host`, `ip`, `port`, `cve_ids`, `cvss_score`, `epss_score`, `is_kev`, `state`, `is_new`, `tags`. With `include_evidence`: `curl_command`, `request`, `response`. |
| `software` | `cve`, `name`, `version`, `product`, `vendor`, `cpe`, `severity`, `cvss_score`, `epss_score`, `is_kev`, `exploit_score`, `evidence`, `confidence`, `caveats`, `version_source`, `host`, `ip`, `port`, `url` |
| `secrets` | `value`, `kind`, `group`, `vendor`, `state`, `subject`, `host`, `url`, `source`, `sightings`, `hosts`, `is_secret` |

The query reference page of each dimension lists the same columns. See [Query language](../../reference/query/index.md).

## Limits

Keep these limits in mind when you plan large exports:

| Limit | Value |
|---|---|
| Rows per file | 50,000, in the sort order of the dimension's search |
| Exports queued or running per project | 3 |
| Statement time | 600 seconds |
| Retention | 30 days after completion |
| Exports returned by `GET /api/v1/exports` | 100, newest first |

Check `capped` after an export: it is `true` when more than 50,000 rows matched and the file holds only the first 50,000. To get the rest, narrow the filter or the scope and export again. `total_rows` counts the matching rows up to 50,001. In a `bundle`, `row_count` and `total_rows` are the sums over the dimensions and `capped` is `true` when any dimension was capped.

## Statuses

Poll until the status is no longer `queued` or `running`:

| `status` | Meaning |
|---|---|
| `queued` | Created, waiting for the worker |
| `running` | Writing. `progress` and `step` report the position, such as `Reading 31 rows` and `Wrote 1000 rows`. |
| `completed` | The file is ready. `step` reads `Ready`. `expires_at` is 30 days after completion. |
| `failed` | `error` reads `The export did not finish. Run it again.`, or `The export stopped without finishing. Run it again.` for an export queued or running an hour after creation |
| `expired` | The file was removed after 30 days. The recipe is kept. |

Check your filter before you export: a `filters` object that does not validate against the search body of the dimension, or a `q` that does not parse, fails the export. A failed export also sends the notification **Export failed**.

## Other operations

Use these to list, rerun or delete exports:

| Operation | Effect |
|---|---|
| `GET /api/v1/exports` | Exports of the project, newest first. `scan_id` or `target_id` narrows the list. |
| `GET /api/v1/exports/{export_id}` | One export |
| `GET /api/v1/exports/{export_id}/download` | The file of a completed export |
| `POST /api/v1/exports/{export_id}/rerun` | A new export with the same recipe, 202. Runs an expired or failed export again. |
| `DELETE /api/v1/exports/{export_id}` | Deletes the export and its file, 204 |

Each takes `project_id` in the query.

## Response

The create, read and rerun operations return an `ExportRead`:

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Export identifier |
| `project_id` | UUID | Project |
| `dimension` | string | Dimension, or `bundle` |
| `scope` | string | `scan`, `target` or `project` |
| `scan_id`, `target_id` | UUID or null | Scope of the request |
| `subject` | string | Target value or project name |
| `query` | string | `q` of the filters |
| `export_format` | string | `csv`, `json` or `txt` |
| `include_evidence` | boolean | Evidence columns requested |
| `status` | string | See [Statuses](#statuses) |
| `progress` | integer | 0 to 100 |
| `step` | string | Current step |
| `error` | string or null | Failure text |
| `filename` | string or null | File name once completed |
| `bytes_written` | integer | File size |
| `row_count` | integer | Rows written |
| `total_rows` | integer | Rows that matched, counted up to 50,001 |
| `capped` | boolean | More than 50,000 rows matched |
| `created_at`, `completed_at` | date-time | Creation and end |
| `duration_seconds` | number or null | Running time |
| `expires_at` | date-time or null | Removal time of the file |

## Errors

If a call is refused, find its status and `detail` below.

| Status | `detail` | What to do |
|---|---|---|
| 400 | `'{dimension}' cannot be exported.` | Send a listed dimension or `bundle`. |
| 400 | `'{format}' is not an export format.` | Send `csv`, `json` or `txt`. |
| 404 | `Scan not found` | Send a run of the project. |
| 404 | `Target not found` | Send a target of the project. |
| 404 | `Export not found` | Send an export of the project. |
| 404 | `The export has no file. Run it again.` | Wait for `completed`, or rerun an expired or failed export. |
| 409 | `{n} exports are running. Wait for one to finish.` | Wait for an export to complete. |
| 422 | Validation list | Send the fields above only. |
