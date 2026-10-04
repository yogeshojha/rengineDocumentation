---
title: Search secrets
description: "Search secrets with a query and get the matching rows with their total count. The interface runs the same search for its Secrets table, so you can pull the same rows into your own scripts."
sources:
  - api/app/api/v1/secrets.py
  - shared/definitions/asset_query.py
  - shared/services/surface_query/
revised: 2026-10-03
generated: scripts/gen_api.py
layout: pane
endpoint: POST /api/v1/secrets/search
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

Send a JSON body of type `SecretFilter`. Put your query in `q`. Most other fields are filters that the interface sets from its controls, and they combine with `q`. A field that is not listed here is refused with HTTP 422.

| Field | Type | Default | Limits | Description |
|---|---|---|---|---|
| `q` | string or null |  | At most 2,000 characters | Query in the [secrets grammar](../../reference/query/secrets.md). Empty or null returns every row in scope. |
| `ids` | array of string (uuid) |  | At most 1,000 items | Only these row ids. |
| `limit` | integer | `50` | 1 to 500 | Rows per page. |
| `offset` | integer | `0` | 0 to | Rows to skip. |
| `sort` | string or null |  |  | Sort key: `state`, `kind`, `hosts`, `sightings`, `seen`. |
| `direction` | string or null |  |  | `asc` or `desc`. |

## Response

You get back a `SecretPage`.

| Field | Type | Description |
|---|---|---|
| `items` | array of SecretRead | The rows, `SecretRead`. |
| `total` | integer | Rows that match, up to the count cap. |
| `total_capped` | boolean | `true` when the count stopped at the cap. The total is then a lower bound. |
| `error` | QueryError or null | Set when the query does not parse. The rows are then empty. |

If reNgine cannot parse your query, you still get HTTP 200, with `error` set to `{message, hint, start, end}`. `start` and `end` are offsets into the query, so you can show where the problem is. A body that fails validation returns HTTP 422.

### Row fields

Each row in `items` is a `SecretRead` with 25 fields.

| Field | Type |
|---|---|
| `id` | string (uuid) |
| `scan_id` | string (uuid) |
| `target_id` | string (uuid) |
| `target_value` | string or null |
| `fingerprint` | string |
| `kind` | string |
| `kind_label` | string |
| `group` | string |
| `group_label` | string |
| `vendor` | string |
| `state` | string |
| `state_label` | string |
| `is_secret` | boolean |
| `value` | string |
| `subject` | string or null |
| `meta` | object |
| `host` | string |
| `url` | string |
| `http_asset_id` | string (uuid) or null |
| `source` | string |
| `source_label` | string |
| `sightings` | integer |
| `hosts` | integer |
| `discovered_at` | string (date-time) |
| `is_new` | boolean |

## Related operations

You also find these operations under the same path.

| Operation | Summary |
|---|---|
| `POST /api/v1/secrets/search/counts` | Secret Search Counts |
| `POST /api/v1/secrets/search/groups` | Secret Groups |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Request</b><span>POST</span></div>

/// tab | curl
```bash
# RENGINE=https://asm.example.com; jar holds the session
curl -b jar -X POST \
  "$RENGINE/api/v1/secrets/search?project_id=$PROJECT" \
  -H "Content-Type: application/json" \
  -d '{"q": "group:cloud and is:exposed", "limit": 50}'
```
///

/// tab | Python
```python
import httpx

with httpx.Client(base_url="https://asm.example.com") as client:
    client.post("/api/v1/auth/login",
                json={"username": user, "password": password})
    r = client.post("/api/v1/secrets/search",
                    params={"project_id": project},
                    json={"q": "group:cloud and is:exposed", "limit": 50})
    page = r.json()
```
///

/// tab | MCP
```json
{
  "name": "query_assets",
  "arguments": {
    "target": "example.com",
    "dimension": "secrets",
    "query": "group:cloud and is:exposed"
  }
}
```
///

<div class="rn-pane-label">response · 200, one row shown, fields abridged</div>

```json
{
  "items": [
    {
      "kind": "aws_access_key",
      "group": "cloud",
      "state": "exposed",
      "host": "app.example.com",
      "url": "https://app.example.com/static/app.js"
    }
  ],
  "total": 3,
  "total_capped": false,
  "error": null
}
```

</div>
</div>
