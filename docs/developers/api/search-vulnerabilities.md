---
title: Search vulnerabilities
description: "Search findings with a query and get the matching rows with their total count. The interface runs the same search for its Vulnerabilities table, so you can pull the same rows into your own scripts."
sources:
  - api/app/api/v1/vulnerabilities.py
  - shared/definitions/asset_query.py
  - shared/services/surface_query/
revised: 2026-10-03
generated: scripts/gen_api.py
layout: pane
endpoint: POST /api/v1/vulnerabilities/search
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

Send a JSON body of type `VulnerabilityFilter`. Put your query in `q`. Most other fields are filters that the interface sets from its controls, and they combine with `q`. A field that is not listed here is refused with HTTP 422.

| Field | Type | Default | Limits | Description |
|---|---|---|---|---|
| `q` | string or null |  | At most 2,000 characters | Query in the [vulnerabilities grammar](../../reference/query/vulnerabilities.md). Empty or null returns every row in scope. |
| `ids` | array of string (uuid) |  | At most 1,000 items | Only these row ids. |
| `severities` | array of string |  | At most 8 items | A filter the interface sets from its controls. Combined with `q`. |
| `states` | array of string |  | At most 8 items | A filter the interface sets from its controls. Combined with `q`. |
| `protocols` | array of string |  | At most 12 items | A filter the interface sets from its controls. Combined with `q`. |
| `templates` | array of string |  | At most 200 items | A filter the interface sets from its controls. Combined with `q`. |
| `tags` | array of string |  | At most 100 items | A filter the interface sets from its controls. Combined with `q`. |
| `hosts` | array of string |  | At most 200 items | A filter the interface sets from its controls. Combined with `q`. |
| `scanners` | array of string |  | At most 8 items | A filter the interface sets from its controls. Combined with `q`. |
| `kev` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `cve` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `new` | boolean | `false` |  | Only rows that are new in the run. |
| `corroborated` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `proven` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `include_info` | boolean | `true` |  | A filter the interface sets from its controls. Combined with `q`. |
| `include_suppressed` | boolean | `false` |  | A filter the interface sets from its controls. Combined with `q`. |
| `sort` | string | `risk` | At most 20 characters | Sort key: `risk`, `severity`, `name`, `template`, `host`, `seen`, `cvss`, `epss`, `exploit`, `type`. |
| `order` | string | `desc` | At most 4 characters | `asc` or `desc`. |
| `limit` | integer | `50` | 1 to 200 | Rows per page. |
| `offset` | integer | `0` | 0 to 100,000,000 | Rows to skip. |

## Response

You get back a `VulnerabilityPage`.

| Field | Type | Description |
|---|---|---|
| `items` | array of VulnerabilityRead | The rows, `VulnerabilityRead`. |
| `total` | integer | Rows that match, up to the count cap. |
| `total_capped` | boolean | `true` when the count stopped at the cap. The total is then a lower bound. |
| `error` | QueryError or null | Set when the query does not parse. The rows are then empty. |

If reNgine cannot parse your query, you still get HTTP 200, with `error` set to `{message, hint, start, end}`. `start` and `end` are offsets into the query, so you can show where the problem is. A body that fails validation returns HTTP 422.

### Row fields

Each row in `items` is a `VulnerabilityRead` with 64 fields.

| Field | Type |
|---|---|
| `id` | string (uuid) |
| `scan_id` | string (uuid) |
| `target_id` | string (uuid) |
| `target_value` | string or null |
| `fingerprint` | string |
| `scanner` | string |
| `template_id` | string |
| `template_name` | string |
| `template_path` | string or null |
| `template_url` | string or null |
| `severity` | string |
| `protocol` | string |
| `matcher_name` | string or null |
| `extractor_name` | string or null |
| `extracted_results` | array of string |
| `description` | string or null |
| `impact` | string or null |
| `remediation` | string or null |
| `references` | array of string |
| `tags` | array of string |
| `authors` | array of string |
| `cve_ids` | array of string |
| `cwe_ids` | array of string |
| `cvss_metrics` | string or null |
| `cvss_score` | number or null |
| `epss_score` | number or null |
| `epss_percentile` | number or null |
| `cpe` | string or null |
| `is_kev` | boolean |
| `exploit_score` | integer |
| `intel_kinds` | array of string |
| `kev_ransomware` | boolean |
| `kev_due_date` | string (date) or null |
| `poc_count` | integer or null |
| `template_available` | boolean or null |
| `hackerone_reports` | integer or null |
| `matched_at` | string |
| `host` | string or null |
| `ip` | string or null |
| `port` | integer or null |
| `scheme` | string or null |
| `url` | string or null |
| `path` | string or null |
| `curl_command` | string or null |
| `request` | string or null |
| `response` | string or null |
| `interaction` | object |
| `observed_at` | string (date-time) or null |
| `discovered_at` | string (date-time) |
| `state` | string |
| `reason` | string or null |
| `reason_at` | string (date-time) or null |
| `reason_by` | string or null |
| `is_new` | boolean |
| `host_count` | integer |
| `sets` | array of string |
| `corroborated_by` | array of Corroboration |
| `colocated` | integer |
| `evidence` | string |
| `replayed_from_id` | string (uuid) or null |
| `replays` | integer |
| `asset` | AssetContext or null |
| `host_findings` | object |
| `tickets` | array of TicketRef |

## Related operations

You also find these operations under the same path.

| Operation | Summary |
|---|---|
| `POST /api/v1/vulnerabilities/search/groups` | Vulnerability Groups |
| `POST /api/v1/vulnerabilities/search/issues` | Search Issues |
| `POST /api/v1/vulnerabilities/search/leads` | Vulnerability Leads |
| `POST /api/v1/vulnerabilities/search/tabs` | Vulnerability Tabs |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Request</b><span>POST</span></div>

/// tab | curl
```bash
# RENGINE=https://asm.example.com; jar holds the session
curl -b jar -X POST \
  "$RENGINE/api/v1/vulnerabilities/search?project_id=$PROJECT" \
  -H "Content-Type: application/json" \
  -d '{"q": "severity:critical or is:kev", "limit": 50}'
```
///

/// tab | Python
```python
import httpx

with httpx.Client(base_url="https://asm.example.com") as client:
    client.post("/api/v1/auth/login",
                json={"username": user, "password": password})
    r = client.post("/api/v1/vulnerabilities/search",
                    params={"project_id": project},
                    json={"q": "severity:critical or is:kev", "limit": 50})
    page = r.json()
```
///

/// tab | MCP
```json
{
  "name": "query_assets",
  "arguments": {
    "target": "example.com",
    "dimension": "vulnerabilities",
    "query": "severity:critical or is:kev"
  }
}
```
///

<div class="rn-pane-label">response · 200, one row shown, fields abridged</div>

```json
{
  "items": [
    {
      "template_id": "CVE-2024-23897",
      "severity": "critical",
      "host": "ci.example.com",
      "is_kev": true,
      "cve_ids": [
        "CVE-2024-23897"
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
