---
title: Search web assets
description: "Search web assets with a query and get the matching rows with their total count. The interface runs the same search for its Web assets table, so you can pull the same rows into your own scripts."
sources:
  - api/app/api/v1/subdomains.py
  - shared/definitions/asset_query.py
  - shared/services/surface_query/
revised: 2026-10-03
generated: scripts/gen_api.py
layout: pane
endpoint: POST /api/v1/subdomains/search
---

This page is generated from the reNgine 3.0 source. `scripts/gen_api.py` writes it from `data/openapi.json` and `data/query-schema.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Query parameters

These go in the URL. They decide which project, runs and targets the search covers.

| Name | Type | Required | Description |
|---|---|---|---|
| `project_id` | string (uuid) | Yes | Project ID. |
| `scan_id` | string (uuid) or null | No | Scan ID. |
| `target_id` | array of string (uuid) or null | No | Only these targets. |
| `organization_id` | string (uuid) or null | No | Only targets of this organization. |
| `tag_id` | string (uuid) or null | No | Only targets with this tag. |

`project_id` scopes the search to one project. Add `scan_id` to search one run, or `target_id`, repeated for several, to search some targets. Any signed-in user can call this operation.

## Request body

Send a JSON body of type `SubdomainFilter`. Put your query in `q`. Most other fields are filters that the interface sets from its controls, and they combine with `q`. A field that is not listed here is refused with HTTP 422.

| Field | Type | Default | Limits | Description |
|---|---|---|---|---|
| `q` | string or null |  | At most 2,000 characters | Query in the [web assets grammar](../../reference/query/web-assets.md). Empty or null returns every row in scope. |
| `ids` | array of string (uuid) |  | At most 1,000 items | Only these row ids. |
| `statuses` | array of string |  | At most 10 items | A filter the interface sets from its controls. Combined with `q`. |
| `tech` | array of string |  | At most 200 items | A filter the interface sets from its controls. Combined with `q`. |
| `services` | array of string |  | At most 200 items | A filter the interface sets from its controls. Combined with `q`. |
| `cert` | array of string |  | At most 10 items | A filter the interface sets from its controls. Combined with `q`. |
| `hygiene` | array of string |  | At most 40 items | A filter the interface sets from its controls. Combined with `q`. |
| `posture` | array of string |  | At most 40 items | A filter the interface sets from its controls. Combined with `q`. |
| `sources` | array of string |  | At most 200 items | A filter the interface sets from its controls. Combined with `q`. |
| `cdn` | string | `any` | At most 10 characters | A filter the interface sets from its controls. Combined with `q`. |
| `waf` | string | `any` | At most 20 characters | A filter the interface sets from its controls. Combined with `q`. |
| `live` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `screenshot` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `issues` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `new` | boolean | `false` |  | Only rows that are new in the run. |
| `sort` | string | `name` | At most 20 characters | Sort key: `name`, `status`, `size`, `time`, `title`, `cert`, `discovered`, `ip`. |
| `order` | string | `asc` | At most 4 characters | `asc` or `desc`. |
| `limit` | integer | `50` | 1 to 200 | Rows per page. |
| `offset` | integer | `0` | 0 to 100,000,000 | Rows to skip. |

## Response

You get back a `SubdomainSearchResult`.

| Field | Type | Description |
|---|---|---|
| `items` | array of SubdomainRow | The rows, `SubdomainRow`. |
| `total` | integer | Rows that match, up to the count cap. |
| `total_capped` | boolean | `true` when the count stopped at the cap. The total is then a lower bound. |
| `error` | QueryError or null | Set when the query does not parse. The rows are then empty. |

If reNgine cannot parse your query, you still get HTTP 200, with `error` set to `{message, hint, start, end}`. `start` and `end` are offsets into the query, so you can show where the problem is. A body that fails validation returns HTTP 422.

### Row fields

Each row in `items` is a `SubdomainRow` with 52 fields.

| Field | Type |
|---|---|
| `id` | string (uuid) |
| `scan_id` | string (uuid) |
| `target_id` | string (uuid) |
| `name` | string |
| `sources` | array of string |
| `resolved_ips` | array of string |
| `cname` | string or null |
| `is_active` | boolean |
| `is_wildcard` | boolean |
| `is_excluded` | boolean |
| `is_important` | boolean |
| `http_url` | string or null |
| `final_url` | string or null |
| `http_status` | integer or null |
| `page_title` | string or null |
| `content_type` | string or null |
| `content_length` | integer or null |
| `response_time` | number or null |
| `webserver` | string or null |
| `tech` | array of string |
| `is_cdn` | boolean |
| `cdn_name` | string or null |
| `waf` | string or null |
| `asn` | integer or null |
| `asn_org` | string or null |
| `favicon_hash` | string or null |
| `tls_not_after` | string (date-time) or null |
| `tls_expired` | boolean or null |
| `tls_self_signed` | boolean or null |
| `screenshot_path` | string or null |
| `hygiene_issues` | array of string |
| `hygiene_checked` | array of string |
| `posture_issues` | array of string |
| `posture_checked` | array of string |
| `ai_services` | array of string or null |
| `discovered_at` | string (date-time) |
| `target_value` | string or null |
| `ports` | array of integer |
| `endpoint_count` | integer |
| `title_count` | integer |
| `title_targets` | integer |
| `favicon_count` | integer |
| `favicon_targets` | integer |
| `render_hash` | string or null |
| `render_count` | integer |
| `render_targets` | integer |
| `vuln_count` | integer |
| `vuln_severity` | string or null |
| `vuln_severities` | object |
| `vuln_kev` | boolean |
| `matched_in` | array of MatchEvidence |
| `cross_links` | array of CrossLink |

## Related operations

You also find these operations under the same path.

| Operation | Summary |
|---|---|
| `POST /api/v1/subdomains/search/counts` | Subdomain Search Counts |
| `POST /api/v1/subdomains/search/groups` | Subdomain Search Groups |
| `POST /api/v1/subdomains/search/leads` | Subdomain Search Leads |
| `POST /api/v1/subdomains/search/renders` | Subdomain Search Renders |
| `POST /api/v1/subdomains/search/tabs` | Subdomain Search Tabs |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Request</b><span>POST</span></div>

/// tab | curl
```bash
# RENGINE=https://asm.example.com; jar holds the session
curl -b jar -X POST \
  "$RENGINE/api/v1/subdomains/search?project_id=$PROJECT" \
  -H "Content-Type: application/json" \
  -d '{"q": "tech:jenkins is:live", "limit": 50}'
```
///

/// tab | Python
```python
import httpx

with httpx.Client(base_url="https://asm.example.com") as client:
    client.post("/api/v1/auth/login",
                json={"username": user, "password": password})
    r = client.post("/api/v1/subdomains/search",
                    params={"project_id": project},
                    json={"q": "tech:jenkins is:live", "limit": 50})
    page = r.json()
```
///

/// tab | MCP
```json
{
  "name": "query_assets",
  "arguments": {
    "target": "example.com",
    "dimension": "web_assets",
    "query": "tech:jenkins is:live"
  }
}
```
///

<div class="rn-pane-label">response · 200, one row shown, fields abridged</div>

```json
{
  "items": [
    {
      "name": "ci.example.com",
      "http_status": 200,
      "page_title": "Dashboard [Jenkins]",
      "tech": [
        "Jenkins",
        "Jetty"
      ],
      "resolved_ips": [
        "203.0.113.10"
      ]
    }
  ],
  "total": 3,
  "total_capped": false,
  "error": null
}
```

</div>
</div>
