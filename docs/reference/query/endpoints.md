---
title: Endpoints
description: "Everything you can search, group and sort in the endpoints dimension, with example queries. Keep this page open while you write a query on endpoints."
sources:
  - shared/definitions/asset_query.py
  - shared/services/surface_query/endpoints.py
  - shared/definitions/notes.py
  - frontend/src/lib/components/scans/results/endpoints-table.svelte
revised: 2026-10-03
generated: scripts/gen_query.py
layout: reference
nav_order: 1
---

This page is generated from the reNgine 3.0 source. `scripts/gen_query.py` writes it from `data/query-schema.json`, `data/openapi.json` and `data/mcp-dimensions.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Each row in the Endpoints dimension is one URL (host, path and parameter shape) recorded by one scan (an endpoints row). You search these rows in the query bar of the table, in the HTTP API with `POST /api/v1/endpoints/search` and from an MCP client with the tool `query_assets`. For the syntax that works in every dimension, see [Query language](index.md).

## About this dimension

The basics: what a row is, which stages fill the dimension, and where you search it.

| Property | Value |
|---|---|
| One row is | One URL (host, path and parameter shape) recorded by one scan (an endpoints row). |
| Singular and plural | endpoint, endpoints |
| Identified by | `signature` |
| Stages that add rows | [`content_discovery`](../stages/content_discovery.md), [`url_discovery`](../stages/url_discovery.md) |
| Stages that cover it | [`content_discovery`](../stages/content_discovery.md), [`url_discovery`](../stages/url_discovery.md) |
| Free-text fields | `url`, `path`, `host`, `title` |
| Flag prefixes | `is:` |
| Search API | `POST /api/v1/endpoints/search` |
| Query bar placeholder | `is:param and is:live`{ .rn-q } |

Coverage tells you whether an empty table means that nothing was found or that nothing was looked for. A dimension is covered for a target when a covering stage succeeded in a run, or when a run wrote rows to it. Without coverage, the dimension reads **Not scanned**, which is not the same as zero rows.

## Fields

Fields are the properties you search on, written `field:value`. An alias works the same as the field name. Select a field to see its operators, its values and an example.

| Field | Aliases | Type | Group | Description |
|---|---|---|---|---|
| [`target`](#f-target) | `scope` | string | Scope | Target this endpoint belongs to. |
| [`url`](#f-url) |  | string | Location | Full URL. |
| [`path`](#f-path) |  | string | Location | Path, without the host or the query string. |
| [`dir`](#f-dir) | `directory`, `folder` | string | Location | Directory the endpoint sits in. dir: matches the whole branch, dir= only that folder. |
| [`file`](#f-file) | `filename` | string | Location | File name, without the directory. |
| [`ext`](#f-ext) | `extension` | string | Location | File extension. |
| [`host`](#f-host) |  | string | Location | Hostname the endpoint is on. |
| [`port`](#f-port) |  | number | Location | Port the endpoint is served on. |
| [`scheme`](#f-scheme) |  | enum | Location | URL scheme. |
| [`depth`](#f-depth) |  | number | Location | Directory depth of the endpoint. |
| [`class`](#f-class) | `kind` | enum | Location | The kind of content the endpoint serves. |
| [`param`](#f-param) | `parameter` | string | Parameters | Name of a query parameter the endpoint accepts. |
| [`params`](#f-params) |  | number | Parameters | Number of parameters the endpoint accepts. |
| [`interest`](#f-interest) |  | enum | Parameters | Interest pattern matched by path or parameter shape. |
| [`status`](#f-status) |  | number | Response | HTTP status the endpoint answered with. Empty until probed. |
| [`type`](#f-type) | `content_type`, `mime` | string | Response | Content type of the response. |
| [`title`](#f-title) |  | string | Response | Page title. |
| [`length`](#f-length) | `size` | bytes | Response | Response body size. |
| [`words`](#f-words) |  | number | Response | Word count of the response body. |
| [`tech`](#f-tech) |  | string | Response | Technology fingerprinted on the response. |
| [`method`](#f-method) |  | string | Response | HTTP method the endpoint was seen with. |
| [`source`](#f-source) |  | enum | Evidence | The source that discovered the endpoint. An endpoint may have several. |
| [`from`](#f-from) | `found_on`, `referrer` | string | Evidence | The URL that linked to this one. |
| [`seen`](#f-seen) |  | date | Evidence | When the endpoint was recorded. |
| [`vuln`](#f-vuln) |  | enum | Findings | Severity of a vulnerability reported at this location. |
| [`cve`](#f-cve) |  | string | Findings | CVE reported at this location. |
| [`is`](#f-is) |  | flag | Flags | Property of the endpoint. |

## Flags

Flags are yes-or-no properties of a row. Write them with `is:`, for example `is:new`{ .rn-q }.

| Flag | Description |
|---|---|
| [`is:new`](#is-new) | Absent from every earlier scan of this target |
| [`is:param`](#is-param) | Accepts at least one query parameter |
| [`is:probed`](#is-probed) | Requested directly |
| [`is:live`](#is-live) | Answered with 2xx or 3xx |
| [`is:redirect`](#is-redirect) | Answered with a redirect |
| [`is:auth`](#is-auth) | Answered 401 or 403 |
| [`is:missing`](#is-missing) | Answered 404 or 410 |
| [`is:api`](#is-api) | An API route, by path shape or content type |
| [`is:js`](#is-js) | JavaScript, including bundles and source maps |
| [`is:static`](#is-static) | Static content |
| [`is:interesting`](#is-interesting) | Matched an interest pattern in the path or a parameter |
| [`is:sensitive`](#is-sensitive) | A credential, backup or version control path |
| [`is:orphan`](#is-orphan) | Not linked from any crawled page |
| [`is:archive-only`](#is-archive-only) | Recorded by an archive and unreachable when requested |
| [`is:linked`](#is-linked) | Reached from a page on the live site |
| [`is:crawled`](#is-crawled) | Reached by the crawler |
| [`is:root`](#is-root) | The site root |
| [`is:titled`](#is-titled) | Has a page title |
| [`is:vulnerable`](#is-vulnerable) | A vulnerability scan reported a finding on it |
| [`is:kev`](#is-kev) | A known-exploited weakness was found on it |

## Group keys

Group the rows by one of these keys to count how many rows share each value. Use the **Group by** menu of the table, or the `groups` search operation of the HTTP API.

| Key | Label | Groups |
|---|---|---|
| `target` | Target | Rows belonging to the same target |
| `dir` | Directory | Endpoints in the same directory |
| `host` | Host | Endpoints on the same host |
| `class` | Kind | Endpoints of the same kind |
| `ext` | Extension | Endpoints with the same file extension |
| `status` | Status | Endpoints answering with the same status |
| `source` | Source | Endpoints found the same way |
| `param` | Parameter | Endpoints accepting the same parameter |
| `interest` | Interest | Endpoints flagged for the same reason |
| `tech` | Technology | Endpoints running the same technology |

## Sort

The keys you can sort by, and the order you get when you do not choose one.

| Property | Value |
|---|---|
| Sort keys | `relevance`, `path`, `url`, `host`, `status`, `length`, `params`, `depth`, `seen`, `class` |
| API default | `path` |
| Interface default | `relevance` |
| Tie-break | Host asc, path asc, id asc. NULLs last. |

## Columns

The table always starts with its leading columns. You choose which optional columns to show. An export of this dimension writes the export columns.

| Set | Columns |
|---|---|
| Leading columns | **Status**, **Path** |
| Optional columns | **Host**, **Kind**, **Parameters**, **Title**, **Technology**, **Size**, **Found by**, **First seen** |
| Shown by default | **Host**, **Kind**, **Parameters**, **Size**, **Found by** |
| Export columns | `url`, `host`, `path`, `status_code`, `content_type`, `content_length`, `title`, `methods`, `param_count`, `endpoint_class`, `interest`, `primary_source`, `is_probed`, `is_new` |

## Examples

Start from one of these queries and adjust it to your target.

### Attack surface

| Query | Finds |
|---|---|
| `is:param and is:live`{ .rn-q } | Live endpoints that accept input |
| `interest:open_redirect or interest:ssrf`{ .rn-q } | Parameters carrying a destination URL |
| `interest:traversal and is:live`{ .rn-q } | Live endpoints taking a file or path parameter |
| `is:sensitive`{ .rn-q } | Credential, backup and version control paths |
| `ext:[bak,old,sql,zip,tar,gz]`{ .rn-q } | Archive and backup files in the web root |
| `interest:admin and status:200`{ .rn-q } | Administrative paths answering without authentication |

### Hidden surface

| Query | Finds |
|---|---|
| `is:orphan`{ .rn-q } | Endpoints not linked from any crawled page |
| `is:archive-only`{ .rn-q } | Recorded by an archive and unreachable when requested |
| `source:archive and is:live`{ .rn-q } | Archived endpoints that respond |
| `depth:>4 and is:live`{ .rn-q } | Deeply nested live endpoints |

### Change

| Query | Finds |
|---|---|
| `is:new`{ .rn-q } | Endpoints absent from every earlier scan |
| `is:new and is:param`{ .rn-q } | Input surface absent from every earlier scan |

### API

| Query | Finds |
|---|---|
| `class:api`{ .rn-q } | API routes |
| `interest:api_doc`{ .rn-q } | Swagger, OpenAPI and GraphQL descriptions of the API |
| `class:api and is:param and not is:auth`{ .rn-q } | API routes taking input with no auth wall |

### Evidence

| Query | Finds |
|---|---|
| `not is:probed`{ .rn-q } | Endpoints not requested directly |
| `source:response_mining`{ .rn-q } | Found in stored responses |
| `source:robots or source:sitemap`{ .rn-q } | Paths declared in robots.txt or a sitemap |
| `is:vulnerable`{ .rn-q } | Endpoints a vulnerability scan reported a finding on |

### Hygiene

| Query | Finds |
|---|---|
| `interest:debug_endpoint`{ .rn-q } | Actuator, metrics and diagnostic routes |
| `status:500..599`{ .rn-q } | Endpoints answering with a server error |
| `type:json and not class:api`{ .rn-q } | JSON served outside the API surface |

## Field reference

Each field in detail: its type, the operators it accepts, its values and an example.

### target { #f-target }

Target this endpoint belongs to.

Type
:   `string`

Group
:   Scope

Aliases
:   `scope`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `target:acme.com`{ .rn-q }

### url { #f-url }

Full URL.

Type
:   `string`

Group
:   Location

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `url:/wp-admin`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### path { #f-path }

Path, without the host or the query string.

Type
:   `string`

Group
:   Location

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `path:/api/v1/users`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### dir { #f-dir }

Directory the endpoint sits in. dir: matches the whole branch, dir= only that folder.

Type
:   `string`

Group
:   Location

Aliases
:   `directory`, `folder`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `dir:"/admin/"`{ .rn-q }

Matching
:   dir: matches the directory and everything below it. dir= only that directory. A leading and trailing '/' are added.

### file { #f-file }

File name, without the directory.

Type
:   `string`

Group
:   Location

Aliases
:   `filename`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `file:config.json`{ .rn-q }

### ext { #f-ext }

File extension.

Type
:   `string`

Group
:   Location

Aliases
:   `extension`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `ext:[bak,old,sql]`{ .rn-q }

### host { #f-host }

Hostname the endpoint is on.

Type
:   `string`

Group
:   Location

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `host:api.example.com`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### port { #f-port }

Port the endpoint is served on.

Type
:   `number`

Group
:   Location

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `port:8443`{ .rn-q }

### scheme { #f-scheme }

URL scheme.

Type
:   `enum`

Group
:   Location

Operators
:   `:` `=` `!=`

Values
:   `http`, `https`

Example
:   `scheme:http`{ .rn-q }

Matching
:   Values are matched as substrings.

### depth { #f-depth }

Directory depth of the endpoint.

Type
:   `number`

Group
:   Location

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `depth:>3`{ .rn-q }

### class { #f-class }

The kind of content the endpoint serves.

Type
:   `enum`

Group
:   Location

Aliases
:   `kind`

Operators
:   `:` `=` `!=`

Values
:   `page`, `api`, `script`, `style`, `document`, `image`, `media`, `data`, `archive_file`, `other`

Example
:   `class:api`{ .rn-q }

Matching
:   Values are matched as substrings.

### param { #f-param }

Name of a query parameter the endpoint accepts.

Type
:   `string`

Group
:   Parameters

Aliases
:   `parameter`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `param:redirect`{ .rn-q }

### params { #f-params }

Number of parameters the endpoint accepts.

Type
:   `number`

Group
:   Parameters

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `params:>2`{ .rn-q }

### interest { #f-interest }

Interest pattern matched by path or parameter shape.

Type
:   `enum`

Group
:   Parameters

Operators
:   `:` `=` `!=`

Values
:   `idor`, `open_redirect`, `ssrf`, `traversal`, `sqli`, `xss`, `rce`, `ssti`, `upload`, `debug`, `vcs`, `secrets`, `backup`, `admin`, `api_doc`, `debug_endpoint`, `auth`, `infra`

Example
:   `interest:open_redirect`{ .rn-q }

### status { #f-status }

HTTP status the endpoint answered with. Empty until probed.

Type
:   `number`

Group
:   Response

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `status:200..299`{ .rn-q }

Matching
:   Also accepts 2xx, 3xx, 4xx, 5xx and none.

### type { #f-type }

Content type of the response.

Type
:   `string`

Group
:   Response

Aliases
:   `content_type`, `mime`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `type:json`{ .rn-q }

### title { #f-title }

Page title.

Type
:   `string`

Group
:   Response

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `title:"index of"`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### length { #f-length }

Response body size.

Type
:   `bytes`, unit `bytes`

Group
:   Response

Aliases
:   `size`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `length:>100000`{ .rn-q }

Matching
:   Units b, k/kb, m/mb, gb.

### words { #f-words }

Word count of the response body.

Type
:   `number`

Group
:   Response

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `words:<10`{ .rn-q }

### tech { #f-tech }

Technology fingerprinted on the response.

Type
:   `string`

Group
:   Response

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `tech:django`{ .rn-q }

### method { #f-method }

HTTP method the endpoint was seen with.

Type
:   `string`

Group
:   Response

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `method:POST`{ .rn-q }

### source { #f-source }

The source that discovered the endpoint. An endpoint may have several.

Type
:   `enum`

Group
:   Evidence

Operators
:   `:` `=` `!=`

Values
:   `seed`, `response_mining`, `crawl`, `robots`, `sitemap`, `archive`, `deep_archive`, `js`, `fuzz`, `param_mining`, `api_spec`, `vuln_scan`, `proxy`, `import`, `other`

Example
:   `source:crawl`{ .rn-q }

### from { #f-from }

The URL that linked to this one.

Type
:   `string`

Group
:   Evidence

Aliases
:   `found_on`, `referrer`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `from:/sitemap.xml`{ .rn-q }

### seen { #f-seen }

When the endpoint was recorded.

Type
:   `date`

Group
:   Evidence

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `seen:<7d`{ .rn-q }

Matching
:   A relative age counts back from now.

### vuln { #f-vuln }

Severity of a vulnerability reported at this location.

Type
:   `enum`

Group
:   Findings

Operators
:   `:` `=` `!=`

Values
:   `critical`, `high`, `medium`, `low`, `info`, `unknown`

Example
:   `vuln:critical`{ .rn-q }

Matching
:   A finding in scope on the endpoint's HTTP asset or on its host.

### cve { #f-cve }

CVE reported at this location.

Type
:   `string`

Group
:   Findings

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cve:CVE-2024`{ .rn-q }

### is { #f-is }

Property of the endpoint.

Type
:   `flag`

Group
:   Flags

Operators
:   `:`

Values
:   [`new`](#is-new), [`param`](#is-param), [`probed`](#is-probed), [`live`](#is-live), [`redirect`](#is-redirect), [`auth`](#is-auth), [`missing`](#is-missing), [`api`](#is-api), [`js`](#is-js), [`static`](#is-static), [`interesting`](#is-interesting), [`sensitive`](#is-sensitive), [`orphan`](#is-orphan), [`archive-only`](#is-archive-only), [`linked`](#is-linked), [`crawled`](#is-crawled), [`root`](#is-root), [`titled`](#is-titled), [`vulnerable`](#is-vulnerable), [`kev`](#is-kev)

Example
:   `is:orphan`{ .rn-q }

## Flag reference

Each flag in detail, with the rule a row must meet to match it.

### is:new { #is-new }

Absent from every earlier scan of this target.

Written as
:   `is:new`

Matches when
:   An earlier scan of the target recorded at least one endpoint, and none recorded this signature.

### is:param { #is-param }

Accepts at least one query parameter.

Written as
:   `is:param`

Matches when
:   Param_count above 0.

### is:probed { #is-probed }

Requested directly.

Written as
:   `is:probed`

Matches when
:   Is_probed is true.

### is:live { #is-live }

Answered with 2xx or 3xx.

Written as
:   `is:live`

Matches when
:   Status from 200 to 399.

### is:redirect { #is-redirect }

Answered with a redirect.

Written as
:   `is:redirect`

Matches when
:   Status from 300 to 399.

### is:auth { #is-auth }

Answered 401 or 403.

Written as
:   `is:auth`

Matches when
:   Status 401 or 403.

### is:missing { #is-missing }

Answered 404 or 410.

Written as
:   `is:missing`

Matches when
:   Status 404 or 410.

### is:api { #is-api }

An API route, by path shape or content type.

Written as
:   `is:api`

Matches when
:   Class is api.

### is:js { #is-js }

JavaScript, including bundles and source maps.

Written as
:   `is:js`

Matches when
:   Class is script.

### is:static { #is-static }

Static content.

Written as
:   `is:static`

Matches when
:   Class is style, image or media.

### is:interesting { #is-interesting }

Matched an interest pattern in the path or a parameter.

Written as
:   `is:interesting`

Matches when
:   At least one interest pattern matched.

### is:sensitive { #is-sensitive }

A credential, backup or version control path.

Written as
:   `is:sensitive`

Matches when
:   Interest includes vcs, secrets or backup.

### is:orphan { #is-orphan }

Not linked from any crawled page.

Written as
:   `is:orphan`

Matches when
:   No source among crawl, response_mining, sitemap, js, and no found_on URL.

### is:archive-only { #is-archive-only }

Recorded by an archive and unreachable when requested.

Written as
:   `is:archive-only`

Matches when
:   Source includes archive or deep_archive, no linked source, and not probed or no status or status 400 and above.

### is:linked { #is-linked }

Reached from a page on the live site.

Written as
:   `is:linked`

Matches when
:   Source includes crawl, response_mining, sitemap or js.

### is:crawled { #is-crawled }

Reached by the crawler.

Written as
:   `is:crawled`

Matches when
:   Source includes crawl.

### is:root { #is-root }

The site root.

Written as
:   `is:root`

Matches when
:   Path is '/' with no parameters.

### is:titled { #is-titled }

Has a page title.

Written as
:   `is:titled`

Matches when
:   Title is set and not empty.

### is:vulnerable { #is-vulnerable }

A vulnerability scan reported a finding on it.

Written as
:   `is:vulnerable`

Matches when
:   A finding in scope sits on the endpoint's HTTP asset or host.

### is:kev { #is-kev }

A known-exploited weakness was found on it.

Written as
:   `is:kev`

Matches when
:   Such a finding is KEV-listed.

