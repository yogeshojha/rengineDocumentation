---
title: Search software
description: "Search software CVEs with a query and get the matching rows with their total count. The interface runs the same search for its Software table, so you can pull the same rows into your own scripts."
sources:
  - api/app/api/v1/software.py
  - shared/definitions/asset_query.py
  - shared/services/surface_query/
revised: 2026-10-03
generated: scripts/gen_api.py
layout: pane
endpoint: POST /api/v1/software/search
---

This page is generated from the reNgine 3.0 source. `scripts/gen_api.py` writes it from `data/openapi.json` and `data/query-schema.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Query parameters

These go in the URL. They decide which project, runs and targets the search covers.

| Name | Type | Required | Description |
|---|---|---|---|
| `scan_id` | string (uuid) or null | No | Scan ID. |
| `project_id` | string (uuid) or null | No | Project ID. |
| `target_id` | array of string (uuid) or null | No | Only these targets. |
| `organization_id` | string (uuid) or null | No | Only targets of this organization. |
| `tag_id` | string (uuid) or null | No | Only targets with this tag. |

`project_id` scopes the search to one project. Add `scan_id` to search one run, or `target_id`, repeated for several, to search some targets. Any signed-in user can call this operation.

## Request body

Send a JSON body of type `SoftwareFilter`. Put your query in `q`. Most other fields are filters that the interface sets from its controls, and they combine with `q`. A field that is not listed here is refused with HTTP 422.

| Field | Type | Default | Limits | Description |
|---|---|---|---|---|
| `q` | string or null |  | At most 2,000 characters | Query in the [software grammar](../../reference/query/software.md). Empty or null returns every row in scope. |
| `ids` | array of string (uuid) |  | At most 1,000 items | Only these row ids. |
| `limit` | integer | `50` | 1 to 200 | Rows per page. |
| `offset` | integer | `0` | 0 to 100,000,000 | Rows to skip. |
| `sort` | string or null |  |  | Sort key: `rank`, `cvss`, `epss`, `cve`, `software`, `host`, `seen`. |
| `direction` | string or null |  |  | `asc` or `desc`. |

## Response

You get back a `SoftwarePage`.

| Field | Type | Description |
|---|---|---|
| `items` | array of SoftwareCveRead | The rows, `SoftwareCveRead`. |
| `total` | integer | Rows that match, up to the count cap. |
| `total_capped` | boolean | `true` when the count stopped at the cap. The total is then a lower bound. |
| `error` | QueryError or null | Set when the query does not parse. The rows are then empty. |

If reNgine cannot parse your query, you still get HTTP 200, with `error` set to `{message, hint, start, end}`. `start` and `end` are offsets into the query, so you can show where the problem is. A body that fails validation returns HTTP 422.

### Row fields

Each row in `items` is a `SoftwareCveRead` with 38 fields.

| Field | Type |
|---|---|
| `id` | string (uuid) |
| `scan_id` | string (uuid) |
| `target_id` | string (uuid) |
| `target_value` | string or null |
| `cve` | string |
| `name` | string |
| `version` | string |
| `vendor` | string |
| `product` | string |
| `cpe` | string |
| `version_source` | string |
| `version_source_label` | string |
| `severity` | string |
| `cvss_score` | number or null |
| `epss_score` | number or null |
| `epss_percentile` | number or null |
| `band` | string or null |
| `is_kev` | boolean |
| `kev_ransomware` | boolean |
| `kev_due_date` | string (date) or null |
| `exploit_score` | integer |
| `intel_kinds` | array of string |
| `confidence` | string |
| `confidence_label` | string |
| `caveats` | array of object |
| `evidence` | string |
| `evidence_label` | string |
| `fixed_in` | string or null |
| `fixed_in_assets` | integer or null |
| `description` | string or null |
| `host` | string or null |
| `ip` | string or null |
| `port` | integer or null |
| `url` | string or null |
| `http_asset_id` | string (uuid) or null |
| `port_id` | string (uuid) or null |
| `discovered_at` | string (date-time) |
| `is_new` | boolean |

## Related operations

You also find these operations under the same path.

| Operation | Summary |
|---|---|
| `POST /api/v1/software/search/counts` | Software Search Counts |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Request</b><span>POST</span></div>

/// tab | curl
```bash
# RENGINE=https://asm.example.com; jar holds the session
curl -b jar -X POST \
  "$RENGINE/api/v1/software/search?project_id=$PROJECT" \
  -H "Content-Type: application/json" \
  -d '{"q": "severity:critical and is:stated", "limit": 50}'
```
///

/// tab | Python
```python
import httpx

with httpx.Client(base_url="https://asm.example.com") as client:
    client.post("/api/v1/auth/login",
                json={"username": user, "password": password})
    r = client.post("/api/v1/software/search",
                    params={"project_id": project},
                    json={"q": "severity:critical and is:stated", "limit": 50})
    page = r.json()
```
///

<div class="rn-pane-label">response · 200, one row shown, fields abridged</div>

```json
{
  "items": [
    {
      "cve": "CVE-2023-25690",
      "name": "Apache HTTP Server",
      "version": "2.4.54",
      "severity": "critical",
      "version_source": "banner",
      "host": "www.example.com"
    }
  ],
  "total": 3,
  "total_capped": false,
  "error": null
}
```

</div>
</div>
