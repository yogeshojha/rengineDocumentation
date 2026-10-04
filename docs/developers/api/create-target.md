---
title: Add a target
description: Add a domain, IP address, CIDR range, URL or ASN to a project from your script, so you can scan it. reNgine cleans up the value, works out its type and starts looking up its WHOIS, DNS or BGP details.
layout: pane
endpoint: POST /api/v1/targets
sources:
  - api/app/api/v1/targets.py
  - api/app/services/target.py
  - api/app/api/v1/projects.py
  - shared/models/target.py
  - shared/models/target_seed.py
  - shared/services/target_seeds.py
  - shared/utils/validation.py
  - shared/enums/target.py
  - shared/enums/task_status.py
  - shared/definitions/constants.py
revised: 2026-10-03
---

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Add a target

Call this when your script brings in new scope, for example from an asset inventory or a bug bounty program. If you only want to scan values right away, you can skip this page: a launch with `target_values` creates missing targets itself.

1. **Find the project slug.** `GET /api/v1/projects` lists the active projects with their `id` and `slug`. The target operations take the slug. <span class="rn-ref" data-tab="curl" data-mark="projects">Shown in the pane</span>
2. **Check the value, if you want to.** `POST /api/v1/targets/validate` with `{"target_value": "..."}` tells you whether reNgine accepts the value, without storing anything. It returns `valid`, the `target_type`, the normalised `target_value` and an `error`. This step is optional.
3. **Create the target.** Send `project_slug` and `target_value` to `POST /api/v1/targets`. You get 201 with the new target. <span class="rn-ref" data-tab="curl" data-mark="create">Shown in the pane</span>
4. **Scan it.** Pass the target `id` in `target_ids` to [Start a scan](start-scan.md).

The request body takes these fields. Only `project_slug` and `target_value` are required.

| Name | In | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `project_slug` | body | string | Yes | | Slug of the project |
| `target_value` | body | string, at most 500 characters | Yes | | A domain, IP address, CIDR range, URL or ASN |
| `display_name` | body | string or null, at most 200 characters | No | `null` | Display name of the target |
| `organization_names` | body | array of strings | No | `[]` | Organizations to attach. A name that does not exist in the project is created. |
| `tag_names` | body | array of strings | No | `[]` | Tags to attach. A name that does not exist in the project is created. |
| `seeds` | body | array of strings, at most 5,000 | No | `[]` | Seed assets: host names, addresses or URLs stored against the target, which every scan of it starts from |

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Create a target</b><span>acme project</span></div>

/// tab | curl
<div class="rn-pane-label" data-mark="projects">request · projects</div>

```bash
curl -b jar "$RENGINE/api/v1/projects"
```

<div class="rn-pane-label" data-mark="create">request · create</div>

```bash
curl -b jar -X POST "$RENGINE/api/v1/targets" \
  -H "Content-Type: application/json" \
  -d '{"project_slug": "acme",
       "target_value": "example.com",
       "organization_names": ["Acme"],
       "seeds": ["api.example.com"]}'
```

<div class="rn-pane-label">response · 201</div>

```json
{
  "id": "2d7c9e14-5a3b-4f86-b1c0-8e9f7a6d5c4b",
  "target_value": "example.com",
  "target_type": "domain",
  "display_name": null,
  "project_id": "9b2f6d4e-1c3a-4f5b-8e7d-0a1b2c3d4e5f",
  "created_at": "2026-10-03T10:20:31.204518Z",
  "updated_at": "2026-10-03T10:20:31.204518Z",
  "created_by": "4c1e8a2b-7d3f-4b6a-9e05-2f8c1d7a6b3e",
  "whois_status": "pending",
  "whois_error": null,
  "whois_record_id": null,
  "whois": null,
  "bgp_status": "pending",
  "bgp": null,
  "dns_status": "pending",
  "dns_error": null,
  "dns_lookup_id": null,
  "dns": null,
  "organizations": [
    { "id": "71a0c3e5-2b4d-4e6f-8a9b-0c1d2e3f4a5b", "name": "Acme", "slug": "acme" }
  ],
  "tags": [],
  "seed_scans": true,
  "new_checks": false,
  "seed_count": 1
}
```
///

/// tab | Python
<div class="rn-pane-label">request</div>

```python
# client: httpx.Client signed in, see Authentication
r = client.post("/targets", json={
    "project_slug": "acme",
    "target_value": "example.com",
    "organization_names": ["Acme"],
    "seeds": ["api.example.com"],
})
r.raise_for_status()
target = r.json()
print(target["id"], target["target_type"])
```

<div class="rn-pane-label">response · 201</div>

```text
2d7c9e14-5a3b-4f86-b1c0-8e9f7a6d5c4b domain
```
///

</div>
</div>

## Target values

You do not send a type. reNgine works it out from the shape of the value, trying these types in order and taking the first that matches: CIDR range, IP address, URL, ASN, domain.

| `target_type` | Example | Stored as |
|---|---|---|
| `ip_range` | `203.0.113.0/24` | `203.0.113.0/24` |
| `ip` | `198.51.100.7` | `198.51.100.7` |
| `url` | `https://Example.com/login/` | `https://example.com/login/` |
| `asn` | `AS64500` | `as64500` |
| `domain` | `*.Example.COM.` | `example.com` |

reNgine also cleans up the value: it trims whitespace, removes a leading `*.`, removes a trailing `/` and `.` from values without a scheme, and lowercases the value. A URL keeps its path and has its host lowercased. A project holds one target per cleaned-up value, so `Example.COM` and `example.com` are the same target.

These values are refused:

| Value | `detail` |
|---|---|
| Not a recognised shape | `Unrecognised target: {value}. Enter a domain, IP address, CIDR range, URL or ASN.` |
| Loopback, link-local, multicast or reserved address or range | `{value} is out of scope. Loopback, link-local, multicast and reserved address space are not scanned.` |
| A range with prefix length 0 | `{value} covers every address. Enter a narrower range.` |
| An AS number outside 1 to 4294967295 | `{value} is out of range. An AS number runs from 1 to 4294967295.` |

## Seed assets

Seed assets let you hand reNgine assets you already know about, so every scan of the target starts from them. A seed asset is one host name, IP address or URL stored against the target. Scans use them while `seed_scans` is `true`.

Each target type accepts these seed assets:

| Target type | Accepted seed assets |
|---|---|
| `domain` | Host names and URLs under the domain |
| `url` | Host names and URLs on the URL's host |
| `ip` | That address |
| `ip_range` | Addresses inside the range |
| `asn` | Addresses outside loopback, link-local, multicast and reserved space |

A seed line holds at most 2,000 characters. On create, reNgine drops the lines the target does not accept, and `seed_count` tells you how many seed assets it stored. To add seed assets to an existing target, send `PUT /api/v1/targets/{target_id}/seeds` with `{"values": [...], "replace": false}`. It returns `total`, `added`, `removed` and a `rejected` list with a `reason` for each refused line. A target holds at most 5,000 seed assets.

## Response

You get 201 with a `TargetRead`. Keep its `id`: the scan and result operations take it.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Target identifier |
| `target_value` | string | Normalised value |
| `target_type` | string | `domain`, `ip`, `ip_range`, `asn` or `url` |
| `display_name` | string or null | Display name |
| `project_id` | UUID | Project of the target |
| `created_at`, `updated_at` | date-time | Creation and last change |
| `created_by` | UUID | User who created the target |
| `whois_status`, `dns_status`, `bgp_status` | string | Enrichment state: `pending`, `querying`, `success`, `failed`, `skipped` or `not_applicable` |
| `whois`, `dns`, `bgp` | object or null | Enrichment summaries once available |
| `whois_error`, `dns_error` | string or null | Enrichment error |
| `organizations` | array | `id`, `name` and `slug` of each organization |
| `tags` | array | `id`, `name`, `slug` and `color` of each tag |
| `seed_scans` | boolean | Scans start from the seed assets. Default `true`. |
| `new_checks` | boolean | Monitor against new checks. Default `false`. |
| `seed_count` | integer or null | Stored seed assets |

When you create a target, reNgine queues a WHOIS lookup for it, a DNS lookup for `domain` and `url` targets, and BGP enrichment for `ip`, `ip_range` and `asn` targets. The `*_status` fields start at `pending`. Read the target again later to get the results.

## Related operations

To add many targets at once, check values in bulk, or manage existing targets, use these operations:

| Operation | Use |
|---|---|
| `POST /api/v1/targets/bulk` | Up to 1,000 values in `targets` with one `project_slug`, `organization_names`, `tag_names` and `seeds`. Each new target keeps the seed lines inside its own scope. Returns 201 with `total`, `imported`, `failed`, `skipped_duplicates` and one result per value. |
| `POST /api/v1/targets/validate/batch` | Up to 500 `values`. With `project_slug`, each valid result carries the `target_id` of an existing target. |
| `POST /api/v1/targets/import/csv` | A CSV file of at most 10 MB and 500 targets, with `project_slug` in the query |
| `GET /api/v1/targets` | Targets of a project, filtered by `project_slug`, `search`, `organization_ids`, `tag_ids`, `target_type` or `signal`. Paged with `page` and `size`. |
| `GET`, `PATCH`, `DELETE /api/v1/targets/{target_id}` | Read, change or delete one target |

A bulk request returns 201 even when some values are refused, so check each result. A refused value has `success: false` and an `error`. A value that already exists in the project also carries `duplicate: true` and its `target_id`.

## Errors

If the call is refused, find its status and `detail` below.

| Status | `detail` | What to do |
|---|---|---|
| 400 | `Unrecognised target: {value}. Enter a domain, IP address, CIDR range, URL or ASN.` | Send a supported value. |
| 400 | `{value} is out of scope. Loopback, link-local, multicast and reserved address space are not scanned.` | Send a routable address or range. |
| 404 | `Project not found` | Send the `slug` from `GET /api/v1/projects`. |
| 409 | `Target exists in this project` | Use the existing target. `POST /api/v1/targets/validate/batch` with `project_slug` returns its id. |
| 422 | Validation list | Send `project_slug` and `target_value` within their limits. |
