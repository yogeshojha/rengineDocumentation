---
title: Search services
description: "Search services with a query and get the matching rows with their total count. The interface runs the same search for its Services table, so you can pull the same rows into your own scripts."
sources:
  - api/app/api/v1/ports.py
  - shared/definitions/asset_query.py
  - shared/services/surface_query/
revised: 2026-10-03
generated: scripts/gen_api.py
layout: pane
endpoint: POST /api/v1/ports/search
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

Send a JSON body of type `ServiceFilter`. Put your query in `q`. Most other fields are filters that the interface sets from its controls, and they combine with `q`. A field that is not listed here is refused with HTTP 422.

| Field | Type | Default | Limits | Description |
|---|---|---|---|---|
| `q` | string or null |  | At most 2,000 characters | Query in the [services grammar](../../reference/query/services.md). Empty or null returns every row in scope. |
| `ids` | array of string (uuid) |  | At most 1,000 items | Only these row ids. |
| `classes` | array of string |  | At most 10 items | A filter the interface sets from its controls. Combined with `q`. |
| `ports` | array of integer |  | At most 200 items | A filter the interface sets from its controls. Combined with `q`. |
| `services` | array of string |  | At most 200 items | A filter the interface sets from its controls. Combined with `q`. |
| `sources` | array of string |  | At most 10 items | A filter the interface sets from its controls. Combined with `q`. |
| `asns` | array of integer |  | At most 100 items | A filter the interface sets from its controls. Combined with `q`. |
| `countries` | array of string |  | At most 100 items | A filter the interface sets from its controls. Combined with `q`. |
| `cdn` | string | `any` | At most 10 characters | A filter the interface sets from its controls. Combined with `q`. |
| `http` | string | `any` | At most 10 characters | A filter the interface sets from its controls. Combined with `q`. |
| `sensitive` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `named` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `new` | boolean | `false` |  | Only rows that are new in the run. |
| `sort` | string | `exposure` | At most 20 characters | Sort key: `exposure`, `port`, `ip`, `service`, `class`, `product`, `hosts`, `asn`, `country`, `status`. |
| `order` | string | `desc` | At most 4 characters | `asc` or `desc`. |
| `limit` | integer | `50` | 1 to 200 | Rows per page. |
| `offset` | integer | `0` | 0 to 100,000,000 | Rows to skip. |

## Response

You get back a `ServicePage`.

| Field | Type | Description |
|---|---|---|
| `items` | array of ServiceRead | The rows, `ServiceRead`. |
| `total` | integer | Rows that match, up to the count cap. |
| `total_capped` | boolean | `true` when the count stopped at the cap. The total is then a lower bound. |
| `error` | QueryError or null | Set when the query does not parse. The rows are then empty. |

If reNgine cannot parse your query, you still get HTTP 200, with `error` set to `{message, hint, start, end}`. `start` and `end` are offsets into the query, so you can show where the problem is. A body that fails validation returns HTTP 422.

### Row fields

Each row in `items` is a `ServiceRead` with 36 fields.

| Field | Type |
|---|---|
| `id` | string (uuid) |
| `scan_id` | string (uuid) or null |
| `target_id` | string (uuid) or null |
| `target_value` | string or null |
| `ip` | string |
| `port` | integer |
| `protocol` | string |
| `state` | string |
| `service_name` | string or null |
| `service_class` | string |
| `description` | string |
| `registered` | boolean |
| `source` | string |
| `is_http` | boolean |
| `tls` | boolean |
| `product` | string or null |
| `version` | string or null |
| `banner` | string or null |
| `asn` | integer or null |
| `asn_org` | string or null |
| `country` | string or null |
| `prefix` | string or null |
| `is_cdn` | boolean |
| `cdn_name` | string or null |
| `scan_policy` | string or null |
| `host_count` | integer |
| `hosts` | array of string |
| `web_count` | integer |
| `status_code` | integer or null |
| `url` | string or null |
| `title` | string or null |
| `screenshot_path` | string or null |
| `is_sensitive` | boolean |
| `is_new` | boolean |
| `ai_services` | array of string |
| `ai_models` | array of string |

## Related operations

You also find these operations under the same path.

| Operation | Summary |
|---|---|
| `POST /api/v1/ports/search/groups` | Service Groups |
| `POST /api/v1/ports/search/leads` | Service Leads |
| `POST /api/v1/ports/search/tabs` | Service Tabs |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Request</b><span>POST</span></div>

/// tab | curl
```bash
# RENGINE=https://asm.example.com; jar holds the session
curl -b jar -X POST \
  "$RENGINE/api/v1/ports/search?project_id=$PROJECT" \
  -H "Content-Type: application/json" \
  -d '{"q": "port:22 and is:sensitive", "limit": 50}'
```
///

/// tab | Python
```python
import httpx

with httpx.Client(base_url="https://asm.example.com") as client:
    client.post("/api/v1/auth/login",
                json={"username": user, "password": password})
    r = client.post("/api/v1/ports/search",
                    params={"project_id": project},
                    json={"q": "port:22 and is:sensitive", "limit": 50})
    page = r.json()
```
///

/// tab | MCP
```json
{
  "name": "query_assets",
  "arguments": {
    "target": "example.com",
    "dimension": "services",
    "query": "port:22 and is:sensitive"
  }
}
```
///

<div class="rn-pane-label">response · 200, one row shown, fields abridged</div>

```json
{
  "items": [
    {
      "ip": "203.0.113.10",
      "port": 22,
      "service_name": "ssh",
      "product": "OpenSSH",
      "version": "9.6",
      "is_sensitive": true
    }
  ],
  "total": 3,
  "total_capped": false,
  "error": null
}
```

</div>
</div>
