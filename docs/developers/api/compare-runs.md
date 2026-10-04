---
title: Compare two runs
description: Find out what changed on a target between two runs, such as new web assets, closed services or new findings. The answer first tells you whether the runs compare fairly, so a change in settings is not mistaken for a change on the target.
layout: pane
endpoint: GET /api/v1/scans/compare
sources:
  - api/app/api/v1/scans.py
  - api/app/services/scan_compare.py
  - shared/definitions/compare.py
  - shared/models/compare.py
  - shared/definitions/surface.py
  - shared/services/scan_scope.py
  - shared/enums/scan.py
revised: 2026-10-03
---

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Compare two runs

Use a comparison to report what is new since last week, or to alert on changes from a scheduled scan. You only need the later run: reNgine picks the earlier one unless you name it.

1. **See which runs you can compare with.** `GET /api/v1/scans/{id}/comparable` returns up to 40 other runs of the same target, newest first, each with `comparable` and a `reason`. <span class="rn-ref" data-tab="curl" data-mark="comparable">Shown in the pane</span>
2. **Compare.** Call `GET /api/v1/scans/compare` with `current` set to the later run. If you leave out `baseline`, reNgine uses the newest finished run of the same target and scope that started before `current`. <span class="rn-ref" data-tab="curl" data-mark="compare">Shown in the pane</span>
3. **Check `comparability` first.** `like_for_like` means both runs finished, scanned the same dimensions and ran with the same settings, so the changes are real changes on the target. Any other value names what differs between the runs, and `suggestion` proposes an earlier run that compares like for like.
4. **Read the changed rows.** `GET /api/v1/scans/compare/rows` returns the changed rows of one dimension, with the most important changes first. <span class="rn-ref" data-tab="curl" data-mark="rows">Shown in the pane</span>
5. **Get a text diff, if you want one.** `GET /api/v1/scans/compare/diff` returns the comparison as plain text in a unified diff layout, ready to paste into a ticket or a chat message. <span class="rn-ref" data-tab="curl" data-mark="diff">Shown in the pane</span>

| Name | In | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `project_id` | query | UUID | Yes | | Project of the runs |
| `current` | query | UUID | Yes | | The later run |
| `baseline` | query | UUID | No | The previous run | The earlier run |

reNgine computes the comparison on each request and stores nothing, so you can compare any two runs as often as you like.

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Compare</b><span>example.com</span></div>

/// tab | curl
<div class="rn-pane-label" data-mark="comparable">request · comparable runs</div>

```bash
curl -b jar \
  "$RENGINE/api/v1/scans/$SCAN/comparable?project_id=$PROJECT"
```

<div class="rn-pane-label" data-mark="compare">request · compare</div>

```bash
curl -b jar \
  "$RENGINE/api/v1/scans/compare?project_id=$PROJECT&current=$SCAN"
```

<div class="rn-pane-label">response · 200</div>

```json
{
  "target_value": "example.com",
  "baseline": { "scan_id": "1b3d…", "engine_name": "Default", "status": "completed", … },
  "current": { "scan_id": "6f1d…", "engine_name": "Default", "status": "completed", … },
  "comparability": "like_for_like",
  "headline": "4 web assets changed",
  "summary": "39 rows matched by identity.",
  "changes_total": 4,
  "live": false,
  "dimensions": [
    {
      "dimension": "web_assets",
      "total_baseline": 40, "total_current": 42,
      "appeared": 3, "changed": 0, "disappeared": 1,
      "unconfirmed": 0, "unchanged": 39,
      "verdict": { "comparability": "like_for_like", "confirmed": true, … },
      …
    },
    …
  ],
  "run_diff": [],
  "setting_diff": [],
  "suggestion": null,
  …
}
```

<div class="rn-pane-label" data-mark="rows">request · rows</div>

```bash
curl -b jar "$RENGINE/api/v1/scans/compare/rows?project_id=$PROJECT\
&current=$SCAN&dimension=web_assets&verb=appeared"
```

<div class="rn-pane-label" data-mark="diff">request · diff</div>

```bash
curl -b jar "$RENGINE/api/v1/scans/compare/diff?project_id=$PROJECT\
&current=$SCAN&dimension=web_assets"
```

<div class="rn-pane-label">response · 200 text/plain</div>

```text
--- Default  01 Oct 2026 09:00  1,204 rows
+++ Default  03 Oct 2026 10:24  1,231 rows
# example.com
# Comparable · 39 rows matched by identity.
# web_assets 40→42 +3~0-1

@@ web_assets  40 → 42  +3 ~0 -1 @@
+ beta.example.com  Sign in
+ cdn2.example.com
+ status.example.com  Status
- old.example.com
```
///

/// tab | Python
<div class="rn-pane-label">request</div>

```python
# client: httpx.Client signed in, see Authentication
params = {"project_id": PROJECT, "current": SCAN}
report = client.get("/scans/compare", params=params).json()

if report["comparability"] != "like_for_like":
    print(report["summary"], report["suggestion"])

for d in report["dimensions"]:
    v = d["verdict"]
    if v["comparability"] == "not_covered":
        print(d["dimension"], v["note"])
        continue
    print(d["dimension"], d["appeared"], d["changed"],
          d["disappeared"], d["unconfirmed"])

rows = client.get("/scans/compare/rows", params={
    **params, "dimension": "web_assets", "size": 100,
}).json()
for row in rows["items"]:
    print(row["verb"], row["signal"], row["title"])
```
///

</div>
</div>

## Which runs you can compare

Both runs must belong to the same target, and the earlier one must have finished. Focused runs have rules of their own. When a pair does not compare, you get one of these answers:

| Condition | Response |
|---|---|
| The runs belong to different targets | 422 `Both runs must cover the same target.` |
| `baseline` is `pending`, `running` or `paused` | 422 `This run has not finished.` |
| `current` is a full run and `baseline` a focused run | 422 `A focused run is compared with its parent run only. Open the focused run.` |
| `current` is a focused run and `baseline` a full run | 422 `A full run cannot be compared with a focused run. Select two full runs.` |
| `baseline` equals `current` | 422 `Pick two different runs.` |
| No `baseline` and no earlier finished run of the same scope | 404 `No earlier run of this target to compare with.` |
| A run is not in the project | 404 `Scan not found.` |

`current` can still be open, which lets you watch changes while a scan runs. The response then has `live: true`, and `headline` reads `Scan in progress` or `Scan paused`.

`GET /api/v1/scans/{id}/comparable` returns `ComparableRun` items: `scan_id`, `engine_name`, `status`, `scope`, `started_at`, `duration_seconds`, `counts` of rows per dimension, the `dimensions` the run covered, `comparable` and the refusal `reason`, empty when the run compares.

## Comparability

A change between two runs only means something if both runs looked the same way. The comparability verdict tells you whether they did, and if not, what differs:

| Value | Label | Cause |
|---|---|---|
| `like_for_like` | Comparable | No difference below |
| `settings_differ` | Settings differ | A stage that produces the dimension ran with different settings |
| `quality_differs` | Runs differ in depth | The producing stage of the later run did not end `success`, or the measured coverage of the runs differs |
| `not_covered` | Coverage differs | One run did not scan the dimension |

Each dimension carries its own verdict in `verdict.comparability`. The top-level `comparability` is the first of `not_covered`, `settings_differ`, `quality_differs` and `like_for_like` found among:

- the verdicts of the dimensions that either run scanned,
- `settings_differ` when any stage setting or any material run setting differs,
- `quality_differs` when a run ended `failed` or `cancelled`.

A dimension with `not_covered` reports zero changes and a `note`: `Not scanned in the earlier run.`, `Not scanned in the later run.` or `Neither run scanned this.` Its rows are not reported as appeared or disappeared, so a dimension one run skipped does not show up as everything new or everything gone.

## Response

You get 200 with a `ScanComparison`:

| Field | Type | Description |
|---|---|---|
| `target_id`, `target_value`, `target_type` | | The target |
| `baseline`, `current` | object | Each run: `scan_id`, `engine_name`, `context_name`, `intensity`, `scope`, `status`, `started_at`, `completed_at`, `duration_seconds`, `stages_ran`, `stages_planned` and `counts` of rows per dimension |
| `dimensions[]` | array | One `DimensionDelta` per dimension |
| `setting_diff[]` | array | Stage settings that differ: `stage`, `title`, `field`, `label`, `before`, `after` |
| `settings_identical` | integer | Stage settings found equal in both runs |
| `run_diff[]` | array | Run settings that differ: `key`, `label`, `baseline`, `current`, `material`. At most 12. |
| `runs_between` | integer | Finished runs of the target and scope that started between the two |
| `comparability` | string | The overall verdict |
| `headline`, `summary` | string | One-line description and summary of the comparison |
| `changes_total` | integer | Appeared, changed, disappeared and unconfirmed rows over every dimension |
| `live` | boolean | `current` is open |
| `suggestion` | object or null | When the runs do not compare like for like, the nearest earlier completed run of the same scope with the same run and stage settings, as a `ComparableRun` |
| `generated_at` | date-time | Time of the computation |

Each entry of `dimensions[]` is a `DimensionDelta`. Its counts tell you how many rows changed in each way:

| Field | Description |
|---|---|
| `dimension`, `label`, `noun`, `noun_plural` | The dimension, such as `web_assets`, `Web assets`, `web asset`, `web assets` |
| `total_baseline`, `total_current` | Rows in each run |
| `appeared` | Rows only in `current` |
| `changed` | Rows in both runs with a watched field that differs |
| `disappeared` | Rows only in `baseline`, when the producing stage of `current` ended `success` |
| `unconfirmed` | Rows only in `baseline`, when the producing stage of `current` did not end `success` |
| `unchanged` | Rows in both runs with equal watched fields |
| `intel_moved` | Vulnerabilities only: unchanged findings whose exploit intelligence differs, such as KEV or EPSS |
| `verdict` | `comparability`, `covered_baseline`, `covered_current`, `compared`, `confirmed`, `note`, `stages`, `settings` and `coverage` |

To tell whether a row is the same row in both runs, reNgine matches it by identity:

| Dimension | Identity |
|---|---|
| `web_assets` | Host name |
| `endpoints` | Endpoint signature |
| `services` | Address, port number and protocol |
| `ips` | Address |
| `vulnerabilities`, `software`, `secrets` | Fingerprint |

`run_diff` compares the run settings. A material setting changes the verdict. These are material: engine, scan context, authentication, extra headers, intensity, proxy, HTTP protocol, excluded hosts, excluded paths, excluded addresses, included hosts and seed assets. The launch source, global rate limit, thread multiplier and timeout multiplier are reported with `material: false` and do not change the verdict. A proxy is compared as set or not set.

## Rows

Read the rows to see exactly what changed in one dimension. `GET /api/v1/scans/compare/rows` returns `ChangeRows` for that dimension, and takes these parameters:

| Name | In | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `project_id` | query | UUID | Yes | | Project of the runs |
| `current` | query | UUID | Yes | | The later run |
| `baseline` | query | UUID | No | The previous run | The earlier run |
| `dimension` | query | string | Yes | | `web_assets`, `endpoints`, `services`, `ips`, `vulnerabilities`, `software` or `secrets` |
| `verb` | query | string, repeatable | No | Every change | `appeared`, `changed`, `disappeared`, `unconfirmed` or `unchanged` |
| `page` | query | integer, at least 1 | No | `1` | Page number |
| `size` | query | integer, 1 to 100 | No | `50` | Rows per page |

Without `verb`, you get the `appeared`, `changed`, `disappeared` and `unconfirmed` rows. You get `unchanged` rows only when you ask for them. A row missing from `current` is `disappeared` when its producing stage ended `success`, and `unconfirmed` otherwise, since a stage that did not finish may have missed it. Asking for the other of the two verbs returns no rows.

The response holds `dimension`, `items`, `total`, `page` and `size`. Rows are ordered by `rank`, then by identity, so the changes that matter most come first. Each item is a `ChangeRow`:

| `ChangeRow` field | Description |
|---|---|
| `key` | Identity of the row |
| `verb` | The change |
| `signal`, `rank` | The named signal of the row and its rank. Lower ranks come first. `rank` 99 marks a row without a named signal. |
| `title`, `subtitle` | Display name and detail, such as the host name and the page title |
| `scan_id` | The run the row was read from: `baseline` for a missing row, `current` otherwise |
| `fields[]` | For a changed row: `field`, `label`, `before`, `after` and `tone` |
| `severity`, `status`, `port`, `is_kev`, `sensitive` | Row facts |
| `screenshots` | `baseline` and `current` screenshot paths, for web assets |

These are the signals, from the first rank to the last: `kev_appeared`, `critical_appeared`, `sensitive_service_opened`, `auth_dropped`, `finding_appeared`, `severity_raised`, `cert_expired`, `posture_weakened`, `waf_gone`, `exposed_host_appeared`, `hosting_moved`, `host_woke`, `cdn_gone`, `service_opened`, `body_changed`, `host_appeared`, `address_appeared`, `endpoint_appeared`, `attributes_changed`, `finding_gone`, `service_closed`, `host_gone`, `asset_gone`.

An unknown `dimension` returns 404 `Unknown dimension '{dimension}'.`

## Diff

The diff gives you the whole comparison as text that a person can read, for a ticket, an email or a chat message. `GET /api/v1/scans/compare/diff` returns it as `text/plain`. It takes `project_id`, `current`, `baseline`, an optional `dimension` and repeatable `verb` values.

Each line starts with a marker that tells you what it holds:

| Line | Content |
|---|---|
| `--- ` and `+++ ` | Engine, start time and row total of the earlier and the later run |
| `# ` | Target, verdict label and summary, material run differences, runs between, per-dimension tally |
| `@@ {dimension}  {before} → {after}  +{n} ~{n} -{n} ?{n} @@` | Start of a dimension |
| `+ ` | Appeared |
| `~ ` | Changed, followed by one indented line per changed field |
| `- ` | Disappeared |
| `? ` | Unconfirmed |

A dimension that one run did not scan is written as one `#` line with its note. The text stops at 5,000 lines with `# truncated at 5,000 lines`.
