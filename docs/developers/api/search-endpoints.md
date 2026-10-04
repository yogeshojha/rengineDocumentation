---
title: Search endpoints
description: "Search endpoints with a query and get the matching rows with their total count. The interface runs the same search for its Endpoints table, so you can pull the same rows into your own scripts."
sources:
  - api/app/api/v1/endpoints.py
  - shared/definitions/asset_query.py
  - shared/services/surface_query/
revised: 2026-10-03
generated: scripts/gen_api.py
layout: pane
endpoint: POST /api/v1/endpoints/search
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

Send a JSON body of type `EndpointFilter`. Put your query in `q`. Most other fields are filters that the interface sets from its controls, and they combine with `q`. A field that is not listed here is refused with HTTP 422.

| Field | Type | Default | Limits | Description |
|---|---|---|---|---|
| `q` | string or null |  | At most 2,000 characters | Query in the [endpoints grammar](../../reference/query/endpoints.md). Empty or null returns every row in scope. |
| `ids` | array of string (uuid) |  | At most 1,000 items | Only these row ids. |
| `host` | string or null |  |  | A filter the interface sets from its controls. Combined with `q`. |
| `dir_path` | string or null |  |  | A filter the interface sets from its controls. Combined with `q`. |
| `subtree` | boolean | `true` |  | A filter the interface sets from its controls. Combined with `q`. |
| `endpoint_class` | string or null |  |  | A filter the interface sets from its controls. Combined with `q`. |
| `source` | string or null |  |  | A filter the interface sets from its controls. Combined with `q`. |
| `interest` | string or null |  |  | A filter the interface sets from its controls. Combined with `q`. |
| `status_class` | string or null |  |  | A filter the interface sets from its controls. Combined with `q`. |
| `probed` | boolean or null |  |  | A filter the interface sets from its controls. Combined with `q`. |
| `new` | boolean | `false` |  | Only rows that are new in the run. |
| `hide_static` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `hide_root_only` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `sort` | string | `path` |  | Sort key: `relevance`, `path`, `url`, `host`, `status`, `length`, `params`, `depth`, `seen`, `class`. |
| `direction` | string | `asc` |  | `asc` or `desc`. |
| `page` | integer | `1` |  | Page number. |
| `size` | integer | `50` |  | Rows per page. |

## Response

You get back a `EndpointPage`.

| Field | Type | Description |
|---|---|---|
| `items` | array of EndpointRead | The rows, `EndpointRead`. |
| `total` | integer | Rows that match, up to the count cap. |
| `total_capped` | boolean | `true` when the count stopped at the cap. The total is then a lower bound. |
| `page` | integer | The page returned. |
| `size` | integer | Rows per page. |
| `error` | QueryError or null | Set when the query does not parse. The rows are then empty. |

If reNgine cannot parse your query, you still get HTTP 200, with `error` set to `{message, hint, start, end}`. `start` and `end` are offsets into the query, so you can show where the problem is. A body that fails validation returns HTTP 422.

### Row fields

Each row in `items` is a `EndpointRead` with 40 fields.

| Field | Type |
|---|---|
| `id` | string (uuid) |
| `scan_id` | string (uuid) |
| `target_id` | string (uuid) |
| `target_value` | string or null |
| `signature` | string |
| `url` | string |
| `host` | string |
| `port` | integer |
| `scheme` | string |
| `path` | string |
| `dir_path` | string |
| `filename` | string or null |
| `extension` | string or null |
| `depth` | integer |
| `params` | array of string |
| `param_count` | integer |
| `variants` | integer |
| `more_variants` | boolean |
| `methods` | array of string |
| `sources` | array of string |
| `primary_source` | string |
| `evidence` | array of SourceEvidence |
| `found_on` | string or null |
| `is_probed` | boolean |
| `status_code` | integer or null |
| `content_type` | string or null |
| `content_length` | integer or null |
| `title` | string or null |
| `words` | integer or null |
| `lines` | integer or null |
| `response_time` | number or null |
| `redirect_location` | string or null |
| `tech` | array of string |
| `endpoint_class` | string |
| `interest` | array of string |
| `http_asset_id` | string (uuid) or null |
| `subdomain_id` | string (uuid) or null |
| `archive_last_seen` | string (date-time) or null |
| `discovered_at` | string (date-time) |
| `is_new` | boolean |

## Related operations

You also find these operations under the same path.

| Operation | Summary |
|---|---|
| `POST /api/v1/endpoints/search/groups` | Endpoint Groups |
| `POST /api/v1/endpoints/search/leads` | Endpoint Leads |
| `POST /api/v1/endpoints/search/tabs` | Endpoint Tabs |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Request</b><span>POST</span></div>

/// tab | curl
```bash
# RENGINE=https://asm.example.com; jar holds the session
curl -b jar -X POST \
  "$RENGINE/api/v1/endpoints/search?project_id=$PROJECT" \
  -H "Content-Type: application/json" \
  -d '{"q": "is:param and is:live", "size": 50}'
```
///

/// tab | Python
```python
import httpx

with httpx.Client(base_url="https://asm.example.com") as client:
    client.post("/api/v1/auth/login",
                json={"username": user, "password": password})
    r = client.post("/api/v1/endpoints/search",
                    params={"project_id": project},
                    json={"q": "is:param and is:live", "size": 50})
    page = r.json()
```
///

/// tab | MCP
```json
{
  "name": "query_assets",
  "arguments": {
    "target": "example.com",
    "dimension": "endpoints",
    "query": "is:param and is:live"
  }
}
```
///

<div class="rn-pane-label">response · 200, one row shown, fields abridged</div>

```json
{
  "items": [
    {
      "url": "https://shop.example.com/api/cart?id=",
      "status_code": 200,
      "param_count": 1,
      "endpoint_class": "api",
      "sources": [
        "crawl"
      ]
    }
  ],
  "total": 3,
  "total_capped": false,
  "page": 1,
  "size": 50,
  "error": null
}
```

</div>
</div>
