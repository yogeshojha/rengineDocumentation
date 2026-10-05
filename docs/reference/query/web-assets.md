---
title: Web assets
description: "Everything you can search, group and sort in the web assets dimension, with example queries. Keep this page open while you write a query on web assets."
sources:
  - shared/definitions/asset_query.py
  - shared/services/surface_query/web_assets.py
  - shared/definitions/notes.py
  - shared/models/subdomain.py
  - frontend/src/lib/components/scans/results/web-assets-table.svelte
revised: 2026-10-03
generated: scripts/gen_query.py
layout: reference
nav_order: 0
---

This page is generated from the reNgine 3.0 source. `scripts/gen_query.py` writes it from `data/query-schema.json`, `data/openapi.json` and `data/mcp-dimensions.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Each row in the Web assets dimension is one hostname recorded by one scan (a subdomains row), with the HTTP response probed on it. You search these rows in the query bar of the table, in the HTTP API with `POST /api/v1/subdomains/search` and from an MCP client with the tool `query_assets`. For the syntax that works in every dimension, see [Query language](index.md).

## About this dimension

The basics: what a row is, which stages fill the dimension, and where you search it.

| Property | Value |
|---|---|
| One row is | One hostname recorded by one scan (a subdomains row), with the HTTP response probed on it. |
| Singular and plural | web asset, web assets |
| Identified by | `name` |
| Stages that add rows | [`asset_seed`](../stages/asset_seed.md), [`http_probe`](../stages/http_probe.md), [`netblock_sweep`](../stages/netblock_sweep.md), [`reverse_dns`](../stages/reverse_dns.md), [`subdomain_discovery`](../stages/subdomain_discovery.md), [`vhost`](../stages/vhost.md) |
| Stages that cover it | [`netblock_sweep`](../stages/netblock_sweep.md), [`subdomain_discovery`](../stages/subdomain_discovery.md), [`vhost`](../stages/vhost.md) |
| Free-text fields | `host`, `url`, `cname`, `source`, `title`, `server`, `tech`, `redirect`, `favicon`, `body`, `header`, `ip`, `org`, `cdn`, `waf`, `cert.cn`, `cert.san`, `cert.issuer` |
| Flag prefixes | `is:`, `has:` |
| Search API | `POST /api/v1/subdomains/search` |
| Query bar placeholder | `status:>=500 not is:cdn`{ .rn-q } |

Coverage tells you whether an empty table means that nothing was found or that nothing was looked for. A dimension is covered for a target when a covering stage succeeded in a run, or when a run wrote rows to it. Without coverage, the dimension reads **Not scanned**, which is not the same as zero rows.

## Fields

Fields are the properties you search on, written `field:value`. An alias works the same as the field name. Select a field to see its operators, its values and an example.

| Field | Aliases | Type | Group | Description |
|---|---|---|---|---|
| [`target`](#f-target) | `scope` | string | Scope | Target this web asset belongs to. |
| [`host`](#f-host) | `name`, `subdomain` | string | Host | Hostname of the asset. |
| [`url`](#f-url) |  | string | Host | Probed URL, or the final URL after redirects. |
| [`path`](#f-path) |  | string | Host | Path component of the probed URL. |
| [`cname`](#f-cname) |  | string | Host | CNAME target the hostname points at. |
| [`source`](#f-source) |  | enum | Host | Tool or feed that discovered the web asset. |
| [`discovered`](#f-discovered) | `found`, `seen` | date | Host | When the web asset was recorded. |
| [`status`](#f-status) | `code`, `http.status` | number | HTTP | HTTP status code. Accepts a class such as 4xx. |
| [`title`](#f-title) |  | string | HTTP | Page title of the response. |
| [`server`](#f-server) | `webserver` | string | HTTP | Server header banner. |
| [`tech`](#f-tech) |  | enum | HTTP | Technology fingerprinted on the response. |
| [`content_type`](#f-content-type) | `ctype`, `mime` | string | HTTP | Content-Type of the response. |
| [`size`](#f-size) | `length`, `content_length` | bytes | HTTP | Response body size. Understands kb and mb. |
| [`words`](#f-words) |  | number | HTTP | Word count of the response body. |
| [`paths`](#f-paths) | `endpoints` | number | HTTP | Number of endpoints discovered on the web asset. |
| [`lines`](#f-lines) |  | number | HTTP | Line count of the response body. |
| [`time`](#f-time) | `rt`, `response_time` | duration | HTTP | Response time. Understands ms and s. |
| [`redirect`](#f-redirect) | `location` | string | HTTP | Location header the response redirects to. |
| [`favicon`](#f-favicon) |  | string | HTTP | mmh3 favicon hash. |
| [`screenshot`](#f-screenshot) | `render` | string | HTTP | Perceptual hash of the rendered page. Matches every web asset whose screenshot renders the same way. |
| [`body`](#f-body) | `response` | text | Response | Words in the captured response body. Matches whole words and prefixes. Quote a value to match a phrase. |
| [`header`](#f-header) | `headers` | text | Response | Words in the response headers. Use header.<name>:<value> to pin it to one header. |
| [`ip`](#f-ip) |  | ip | Network | Resolved IP address. Accepts a CIDR range. |
| [`asn`](#f-asn) |  | number | Network | Autonomous system number. |
| [`org`](#f-org) | `asn_org` | string | Network | Autonomous system owner. |
| [`cdn`](#f-cdn) |  | string | Network | CDN in front of the web asset. yes or no filters on presence. |
| [`waf`](#f-waf) |  | string | Network | WAF fingerprinted on the web asset. yes or no filters on presence. |
| [`port`](#f-port) |  | number | Network | Open port on a resolved IP. |
| [`service`](#f-service) |  | enum | Network | Service name on an open port. |
| [`hygiene`](#f-hygiene) | `hardening` | enum | Hygiene | A hardening check the web asset fails on any of its responses. Also takes warning, info, any or none. |
| [`posture`](#f-posture) | `dns_posture`, `mail` | enum | Hygiene | A domain posture check the web asset's zone fails: SPF, DMARC, DKIM, MTA-STS, DNSSEC or CAA. Also takes warning, info, any or none. |
| [`ai`](#f-ai) | `ai_service` | enum | AI | AI service identified on any port of the web asset. Takes a service, a category, yes or no. |
| [`ai.model`](#f-ai-model) |  | string | AI | Model an AI service on the web asset listed. yes or no filters on presence. |
| [`infostealer`](#f-infostealer) | `stealer` | enum | Infostealers | Audience of a web asset login found in infostealer logs: employee or user. Also takes any or none. |
| [`infostealer.credentials`](#f-infostealer-credentials) |  | number | Infostealers | Credentials for the web asset's logins found in infostealer logs. |
| [`cert`](#f-cert) |  | enum | Certificates | Certificate state. |
| [`cert.cn`](#f-cert-cn) |  | string | Certificates | Certificate subject common name. |
| [`cert.san`](#f-cert-san) |  | string | Certificates | Subject alternative name on the certificate. |
| [`cert.issuer`](#f-cert-issuer) |  | string | Certificates | Certificate issuer. |
| [`cert.expires`](#f-cert-expires) |  | date | Certificates | Certificate expiry date. |
| [`tls.version`](#f-tls-version) |  | string | Certificates | Negotiated TLS version. |
| [`content_hash`](#f-content-hash) | `body_hash` | string | Response | Hash of the response body. |
| [`tracking`](#f-tracking) |  | string | Response | Analytics, tag manager or advertising account ID. |
| [`jarm`](#f-jarm) |  | string | Certificates | JARM TLS fingerprint. |
| [`cert.fingerprint`](#f-cert-fingerprint) | `cert.hash` | string | Certificates | Hash of the certificate. |
| [`header_hash`](#f-header-hash) |  | string | Response | Hash of the response header set. |
| [`is`](#f-is) | `has` | flag | Flags | Property of the web asset. |
| [`vuln`](#f-vuln) | `finding`, `severity` | enum | Findings | Severity of a finding recorded on this web asset. |
| [`cve`](#f-cve) |  | string | Findings | Published vulnerability identifier reported on this web asset. |
| [`exposure`](#f-exposure) | `interest`, `worth` | enum | Findings | The reason this web asset was flagged as an exposure. |
| [`flagged`](#f-flagged) |  | enum | Findings | The source of the flag: a rule, a correlation, or AI. |
| [`exposure_band`](#f-exposure-band) | `interest_band`, `band` | enum | Findings | Strength of the exposure on this web asset. |

## Flags

Flags are yes-or-no properties of a row. Write them with `is:` or `has:`, for example `is:live`{ .rn-q }.

| Flag | Description |
|---|---|
| [`is:live`](#is-live) | Responded with 2xx or 3xx |
| [`is:web`](#is-web) | Answered on HTTP with any status |
| [`is:new`](#is-new) | Absent from every earlier scan of this target |
| [`is:resolved`](#is-resolved) | Resolves to at least one IP |
| [`is:auth`](#is-auth) | Login wall or 401/403 |
| [`is:cdn`](#is-cdn) | Served through a CDN |
| [`is:cloud`](#is-cloud) | Hosted on a cloud provider's address |
| [`is:waf`](#is-waf) | A WAF was fingerprinted |
| [`is:screenshot`](#is-screenshot) | A screenshot was captured |
| [`is:important`](#is-important) | Flagged important |
| [`is:wildcard`](#is-wildcard) | Matched a wildcard DNS record |
| [`is:issue`](#is-issue) | Has a cert, exposure or availability problem |
| [`is:sensitive`](#is-sensitive) | An admin or database port is open |
| [`is:http2`](#is-http2) | Negotiated HTTP/2 |
| [`is:redirect`](#is-redirect) | Final URL differs from the probed URL |
| [`is:vulnerable`](#is-vulnerable) | A vulnerability scan reported a finding on it |
| [`is:kev`](#is-kev) | A known-exploited weakness was found on it |
| [`is:exposed`](#is-exposed) | Flagged as an exposure by a rule, a correlation or AI |

## Group keys

Group the rows by one of these keys to count how many rows share each value. Use the **Group by** menu of the table, or the `groups` search operation of the HTTP API.

| Key | Label | Groups |
|---|---|---|
| `target` | Target | Rows belonging to the same target |
| `ip` | IP address | Names sharing a resolved address |
| `favicon` | Favicon | Names serving the same favicon |
| `screenshot` | Rendered page | Names whose screenshots render the same page |
| `title` | Page title | Names serving the same page title |
| `cname` | CNAME target | Names pointing at the same alias |
| `tech` | Technology | Names running the same technology |
| `content_hash` | Identical content | Names serving a byte-identical response |
| `jarm` | TLS fingerprint | Names sharing a JARM TLS fingerprint |
| `cert.fingerprint` | Certificate | Names presenting the same certificate |
| `cert.issuer` | Certificate issuer | Names whose certificate has the same issuer |
| `header_hash` | Header set | Names returning an identical set of response headers |
| `server` | Server banner | Names reporting the same server header |
| `cdn` | CDN | Names fronted by the same CDN |
| `status` | Status class | Names by HTTP response class |
| `hygiene` | Hygiene check | Names failing the same hardening check |
| `posture` | Posture check | Names whose zone fails the same posture check |

## Sort

The keys you can sort by, and the order you get when you do not choose one.

| Property | Value |
|---|---|
| Sort keys | `name`, `status`, `size`, `time`, `title`, `cert`, `discovered`, `ip` |
| API default | `name` asc |
| Interface default | `status` asc |
| Tie-break | Name asc, id asc. NULLs last. |

## Columns

The table always starts with its leading columns. You choose which optional columns to show. An export of this dimension writes the export columns.

| Set | Columns |
|---|---|
| Leading columns | **Host**, **Status**, **Title** |
| Optional columns | **Tech**, **IP / Network**, **Ports**, **Sources**, **Hygiene**, **First seen**, **Size**, **Time**, **Screenshot** |
| Shown by default | **Tech**, **IP / Network**, **Ports**, **Screenshot** |
| Export columns | `name`, `http_status`, `page_title`, `http_url`, `tech`, `webserver`, `resolved_ips`, `cname`, `is_cdn`, `cdn_name`, `waf`, `asn_org`, `ports`, `tls_expired` |

## Examples

Start from one of these queries and adjust it to your target.

### Takeover risk

| Query | Finds |
|---|---|
| `is:resolved and not is:web`{ .rn-q } | Resolving hostnames with no HTTP service |
| `cname:. and not is:web`{ .rn-q } | CNAME records with no HTTP service |
| `cname:elb.amazonaws.com and status:404`{ .rn-q } | Load balancer aliases returning 404 |
| `cname:[myshopify.com,github.io,herokuapp.com,azurewebsites.net,netlify.app,pantheonsite.io,wpengine.com,ghost.io]`{ .rn-q } | Aliases pointing to third-party hosting |
| `cname:. and not is:resolved`{ .rn-q } | CNAME records that fail to resolve |
| `is:wildcard`{ .rn-q } | Hostnames matched only by a wildcard record |

### Exposed services

| Query | Finds |
|---|---|
| `is:sensitive`{ .rn-q } | Administrative or database ports exposed |
| `port:[3306,5432,27017,6379,9200,11211,5984]`{ .rn-q } | Database ports reachable from the internet |
| `port:[22,23,3389,5900]`{ .rn-q } | Remote administration ports reachable |
| `body:"index of" and status:200`{ .rn-q } | Directory listings enabled |
| `body:"begin rsa private key" or body:"begin private key" or body:aws_secret_access_key`{ .rn-q } | Private key material in a response body |
| `body:traceback or body:"stack trace" or title:exception`{ .rn-q } | Application stack traces in responses |
| `body:"sql syntax" or body:"odbc driver"`{ .rn-q } | Database error messages in responses |
| `title:phpinfo or body:phpinfo`{ .rn-q } | phpinfo diagnostic pages exposed |
| `body:swagger or url:swagger or title:swagger`{ .rn-q } | API documentation publicly accessible |
| `tech:[jenkins,gitlab,grafana,kibana,prometheus,sonarqube,jira,confluence] and status:200`{ .rn-q } | Developer tooling exposed to the internet |
| `host:[jenkins,gitlab,grafana,kibana,jira,confluence,vault,consul]`{ .rn-q } | Hostnames indicating internal tooling |
| `content_type:json and status:200`{ .rn-q } | JSON endpoints served directly |

### Non-production

| Query | Finds |
|---|---|
| `host:[staging,dev,test,uat,qa,sandbox,preprod,demo]`{ .rn-q } | Non-production hostnames publicly resolvable |
| `host:[staging,dev,test,uat,qa,sandbox,preprod] and is:live and not is:auth`{ .rn-q } | Non-production web assets served without authentication |
| `(host:admin or host:portal or host:console) and is:live and not is:auth`{ .rn-q } | Administrative interfaces without authentication |

### Access control

| Query | Finds |
|---|---|
| `is:auth and is:live`{ .rn-q } | Authenticated interfaces currently serving |
| `is:auth`{ .rn-q } | Web assets requiring authentication |
| `header.access-control-allow-origin:*`{ .rn-q } | Wildcard cross-origin policy on responses |

### Certificates

| Query | Finds |
|---|---|
| `cert:expired and is:live`{ .rn-q } | Reachable web assets serving an expired certificate |
| `cert:expiring`{ .rn-q } | Certificates expiring within 30 days |
| `cert:self-signed`{ .rn-q } | Self-signed certificates in use |
| `cert.cn:internal or cert.san:internal or cert.san:local`{ .rn-q } | Internal hostnames disclosed in certificates |
| `cert.san:*. and is:live`{ .rn-q } | Wildcard certificates in use |
| `tls.version:[tls10,tls11]`{ .rn-q } | Obsolete TLS versions negotiated |

### Origin exposure

| Query | Finds |
|---|---|
| `is:live and not cdn:yes and waf:no`{ .rn-q } | Web assets served without CDN or WAF |
| `server:[apache,nginx,iis] and not cdn:yes`{ .rn-q } | Origin server banners disclosed |
| `tech:[php,tomcat,jboss,weblogic,coldfusion] and status:200`{ .rn-q } | Runtimes with significant CVE history |

### Hygiene

| Query | Finds |
|---|---|
| `hygiene:warning`{ .rn-q } | Web assets failing a warning-level hardening check |
| `hygiene:cors_credentials`{ .rn-q } | CORS credentials allowed with a wildcard or null origin |
| `hygiene:cookie_no_secure`{ .rn-q } | Cookies set over https without Secure |
| `hygiene:cookie_no_httponly`{ .rn-q } | Session cookies readable by scripts |
| `hygiene:no_frame_protection and is:live`{ .rn-q } | Pages that can be framed by another site |
| `hygiene:[csp_unsafe_inline,csp_wildcard_script]`{ .rn-q } | Content-Security-Policy that does not restrict scripts |
| `hygiene:no_https_redirect`{ .rn-q } | Plaintext http with no redirect to https |
| `hygiene:[server_version,runtime_disclosed] and not cdn:yes`{ .rn-q } | Origin software versions disclosed in headers |
| `hygiene:none and is:live`{ .rn-q } | Reachable web assets passing every hardening check |

### Change

| Query | Finds |
|---|---|
| `is:new and (status:2xx or status:3xx)`{ .rn-q } | Reachable web assets absent from every earlier scan |
| `is:new and is:auth`{ .rn-q } | Authenticated interfaces absent from every earlier scan |
| `is:new and cert:expired`{ .rn-q } | New web assets serving an expired certificate |
| `is:new`{ .rn-q } | Web assets absent from every earlier scan |
| `discovered:<7d and is:live`{ .rn-q } | Reachable web assets discovered in the last 7 days |

### Health

| Query | Finds |
|---|---|
| `status:>=500 or title:exception`{ .rn-q } | Server-side errors returned |
| `not is:resolved`{ .rn-q } | Hostnames that no longer resolve |
| `size:<500 and status:200`{ .rn-q } | Minimal-content responses returning 200 |
| `time:>5s`{ .rn-q } | Responses slower than 5 seconds |
| `is:redirect and not is:live`{ .rn-q } | Redirects terminating in an error |

### Exposures

| Query | Finds |
|---|---|
| `is:exposed`{ .rn-q } | Everything flagged as an exposure |
| `is:exposed and is:new`{ .rn-q } | New web assets flagged as an exposure |
| `flagged:ai`{ .rn-q } | Flagged by AI judgement |
| `exposure_band:critical`{ .rn-q } | Exposures in the critical band |
| `exposure:admin_interface and not is:auth`{ .rn-q } | Administrative surfaces answering without a login |

## Field reference

Each field in detail: its type, the operators it accepts, its values and an example.

### target { #f-target }

Target this web asset belongs to.

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

Matching
:   Matches the target's value.

### host { #f-host }

Hostname of the asset.

Type
:   `string`

Group
:   Host

Aliases
:   `name`, `subdomain`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `host:api`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### url { #f-url }

Probed URL, or the final URL after redirects.

Type
:   `string`

Group
:   Host

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `url:/admin`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Matches the final URL after redirects, else the probed URL. As free text only the final URL is searched.

### path { #f-path }

Path component of the probed URL.

Type
:   `string`

Group
:   Host

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `path:/api/v1`{ .rn-q }

Matching
:   Read from the host's HTTP asset.

### cname { #f-cname }

CNAME target the hostname points at.

Type
:   `string`

Group
:   Host

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cname:s3.amazonaws.com`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### source { #f-source }

Tool or feed that discovered the web asset.

Type
:   `enum`

Group
:   Host

Operators
:   `:` `=` `!=`

Example
:   `source:ctfr`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Values are not validated.

### discovered { #f-discovered }

When the web asset was recorded.

Type
:   `date`

Group
:   Host

Aliases
:   `found`, `seen`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `discovered:<7d`{ .rn-q }

Matching
:   A relative age counts back from now.

### status { #f-status }

HTTP status code. Accepts a class such as 4xx.

Type
:   `number`

Group
:   HTTP

Aliases
:   `code`, `http.status`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Values
:   `2xx`, `3xx`, `4xx`, `5xx`, `none`

Example
:   `status:>=500`{ .rn-q }

Matching
:   Also accepts 1xx-5xx classes and none (no HTTP response). '!=' also matches rows with no status.

### title { #f-title }

Page title of the response.

Type
:   `string`

Group
:   HTTP

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `title:"index of"`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### server { #f-server }

Server header banner.

Type
:   `string`

Group
:   HTTP

Aliases
:   `webserver`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `server:nginx`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### tech { #f-tech }

Technology fingerprinted on the response.

Type
:   `enum`

Group
:   HTTP

Operators
:   `:` `=` `!=`

Example
:   `tech:[jenkins,tomcat]`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### content_type { #f-content-type }

Content-Type of the response.

Type
:   `string`

Group
:   HTTP

Aliases
:   `ctype`, `mime`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `content_type:json`{ .rn-q }

### size { #f-size }

Response body size. Understands kb and mb.

Type
:   `bytes`, unit `bytes`

Group
:   HTTP

Aliases
:   `length`, `content_length`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `size:>500kb`{ .rn-q }

Matching
:   Units b, k/kb, m/mb, gb (1024-based).

### words { #f-words }

Word count of the response body.

Type
:   `number`

Group
:   HTTP

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `words:<20`{ .rn-q }

Matching
:   Read from the host's HTTP asset.

### paths { #f-paths }

Number of endpoints discovered on the web asset.

Type
:   `number`

Group
:   HTTP

Aliases
:   `endpoints`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `paths:>50`{ .rn-q }

Matching
:   Count of endpoint rows on the host in scope.

### lines { #f-lines }

Line count of the response body.

Type
:   `number`

Group
:   HTTP

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `lines:>2000`{ .rn-q }

Matching
:   Read from the host's HTTP asset.

### time { #f-time }

Response time. Understands ms and s.

Type
:   `duration`, unit `seconds`

Group
:   HTTP

Aliases
:   `rt`, `response_time`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `time:>3s`{ .rn-q }

Matching
:   Units ms, s, m, h. Stored in seconds.

### redirect { #f-redirect }

Location header the response redirects to.

Type
:   `string`

Group
:   HTTP

Aliases
:   `location`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `redirect:login`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Location header on the host's HTTP asset.

### favicon { #f-favicon }

mmh3 favicon hash.

Type
:   `string`

Group
:   HTTP

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `favicon:-1278323681`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   As free text the hash must equal the word exactly.

### screenshot { #f-screenshot }

Perceptual hash of the rendered page. Matches every web asset whose screenshot renders the same way.

Type
:   `string`

Group
:   HTTP

Aliases
:   `render`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `screenshot:0030242430d41010`{ .rn-q }

Matching
:   16 hex digits (optional 0x). Matches every render within 2 bits of the hash. Only the first value is read.

### body { #f-body }

Words in the captured response body. Matches whole words and prefixes. Quote a value to match a phrase.

Type
:   `text`

Group
:   Response

Aliases
:   `response`

Operators
:   `:` `=` `!=`

Example
:   `body:"internal server"`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Full-text over the stored body: a single unquoted word is a prefix match, several words are a phrase, a quoted value is matched as whole words.

### header { #f-header }

Words in the response headers. Use header.<name>:<value> to pin it to one header.

Type
:   `text`

Group
:   Response

Aliases
:   `headers`

Operators
:   `:` `=` `!=`

Example
:   `header.x-powered-by:php`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Sub-fields
:   `header name`

Matching
:   header:word is full-text over the headers. A quoted value is a substring of the raw header block. Header.<name>:<value> is a substring of that one header (name lowercased, '-' read as '_').

### ip { #f-ip }

Resolved IP address. Accepts a CIDR range.

Type
:   `ip`

Group
:   Network

Operators
:   `:` `=` `!=`

Example
:   `ip:10.0.0.0/8`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### asn { #f-asn }

Autonomous system number.

Type
:   `number`

Group
:   Network

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `asn:15169`{ .rn-q }

Matching
:   Accepts 13335 or AS13335. Maximum 4294967295.

### org { #f-org }

Autonomous system owner.

Type
:   `string`

Group
:   Network

Aliases
:   `asn_org`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `org:"digital ocean"`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### cdn { #f-cdn }

CDN in front of the web asset. yes or no filters on presence.

Type
:   `string`

Group
:   Network

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cdn:cloudflare`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Yes/true/1/any/present and no/false/0/none/absent filter on presence. Anything else matches the CDN name.

### waf { #f-waf }

WAF fingerprinted on the web asset. yes or no filters on presence.

Type
:   `string`

Group
:   Network

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `waf:no`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Yes/no words filter on presence. Anything else matches the WAF name.

### port { #f-port }

Open port on a resolved IP.

Type
:   `number`

Group
:   Network

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `port:[22,3389]`{ .rn-q }

Matching
:   True when a resolved address has that port open in the row's scan.

### service { #f-service }

Service name on an open port.

Type
:   `enum`

Group
:   Network

Operators
:   `:` `=` `!=`

Example
:   `service:ssh`{ .rn-q }

Matching
:   Matched against the service name of the port. Operators `:`, `=` and `!=`.

### hygiene { #f-hygiene }

A hardening check the web asset fails on any of its responses. Also takes warning, info, any or none.

Type
:   `enum`

Group
:   Hygiene

Aliases
:   `hardening`

Operators
:   `:` `=` `!=`

Values
:   `no_https_redirect`, `cookie_no_secure`, `cookie_no_httponly`, `cacheable_session`, `cors_credentials`, `no_frame_protection`, `csp_unsafe_inline`, `csp_wildcard_script`, `internal_address`, `no_hsts`, `hsts_short`, `no_csp`, `csp_report_only`, `no_nosniff`, `no_referrer_policy`, `cors_any_origin`, `server_version`, `runtime_disclosed`, `warning`, `info`, `any`, `none`

Example
:   `hygiene:cookie_no_secure`{ .rn-q }

Matching
:   Validated: an unknown value is an error. warning / info expand to every check of that tone, any = fails at least one, none = checked and failing none.

### posture { #f-posture }

A domain posture check the web asset's zone fails: SPF, DMARC, DKIM, MTA-STS, DNSSEC or CAA. Also takes warning, info, any or none.

Type
:   `enum`

Group
:   Hygiene

Aliases
:   `dns_posture`, `mail`

Operators
:   `:` `=` `!=`

Values
:   `spf_missing`, `spf_any_sender`, `spf_multiple`, `spf_lookup_limit`, `dmarc_missing`, `dmarc_none`, `dmarc_subdomains_open`, `dkim_weak_key`, `dnssec_broken`, `spf_soft_all`, `dmarc_partial`, `dmarc_no_reporting`, `dkim_none_probed`, `mta_sts_missing`, `mta_sts_not_enforced`, `tls_rpt_missing`, `dnssec_missing`, `caa_missing`, `warning`, `info`, `any`, `none`

Example
:   `posture:dmarc_missing`{ .rn-q }

Matching
:   Validated like hygiene, over the checks of the host's zone.

### ai { #f-ai }

AI service identified on any port of the web asset. Takes a service, a category, yes or no.

Type
:   `enum`

Group
:   AI

Aliases
:   `ai_service`

Operators
:   `:` `=` `!=`

Values
:   `yes`, `no`, `self_hosted`, `gateway`, `mcp`, `application`, `cloud`, `generic`, `ollama`, `vllm`, `sglang`, `localai`, `llama-cpp`, `huggingface-tgi`, `nvidia-nim`, `tensorrt-llm`, `triton-inference-server`, `bentoml`, `ray-serve`, `aphrodite-engine`, `baseten-truss`, `deepspeed-mii`, `fastchat-controller`, `gpt4all`, `gradio`, `jan`, `koboldcpp`, `lm-studio`, `mlc-llm`, `petals`, `powerinfer`, `tabbyapi`, `text-generation-webui`, `litellm`, `bifrost`, `envoy-ai-gateway`, `helicone`, `kong-proxy`, `omniroute`, `portkey-ai-gateway`, `tensorzero`, `mcp-server`, `anythingllm`, `astrbot`, `betterchatgpt`, `dify`, `flowise`, `h2ogpt`, `huggingface-chat-ui`, `langflow`, `librechat`, `lobehub`, `nextchat`, `onyx`, `openclaw`, `open-webui`, `privategpt`, `quivr`, `ragflow`, `sillytavern`, `aws-bedrock`, `azure-openai`, `cloudflare-ai-gateway`, `databricks-model-serving`, `fireworks-ai`, `vertex-ai`, `groq`, `modal`, `replicate`, `salesforce-einstein`, `together-ai`, `openai-compatible`

Example
:   `ai:ollama`{ .rn-q }

Matching
:   A service key, a category (self_hosted, gateway, mcp, application, cloud, generic), or a yes/no word.

### ai.model { #f-ai-model }

Model an AI service on the web asset listed. yes or no filters on presence.

Type
:   `string`

Group
:   AI

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `ai.model~llama`{ .rn-q }

Matching
:   Yes/no words filter on presence.

### infostealer { #f-infostealer }

Audience of a web asset login found in infostealer logs: employee or user. Also takes any or none.

Type
:   `enum`

Group
:   Infostealers

Aliases
:   `stealer`

Operators
:   `:` `=` `!=`

Values
:   `employee`, `user`, `any`, `none`

Example
:   `infostealer:employee`{ .rn-q }

### infostealer.credentials { #f-infostealer-credentials }

Credentials for the web asset's logins found in infostealer logs.

Type
:   `number`

Group
:   Infostealers

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `infostealer.credentials>10`{ .rn-q }

### cert { #f-cert }

Certificate state.

Type
:   `enum`

Group
:   Certificates

Operators
:   `:` `=` `!=`

Values
:   `expired`, `expiring`, `self-signed`, `valid`

Example
:   `cert:expired`{ .rn-q }

Matching
:   expired: flagged expired or not-after in the past. expiring: not expired and not-after within 30 days. self-signed. valid: not-after 30 days or more away and not self-signed.

### cert.cn { #f-cert-cn }

Certificate subject common name.

Type
:   `string`

Group
:   Certificates

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cert.cn:*.internal`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### cert.san { #f-cert-san }

Subject alternative name on the certificate.

Type
:   `string`

Group
:   Certificates

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cert.san:staging`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### cert.issuer { #f-cert-issuer }

Certificate issuer.

Type
:   `string`

Group
:   Certificates

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cert.issuer:"let's encrypt"`{ .rn-q }

Free text
:   Yes. A bare word searches this field

Matching
:   Searches issuer, issuer organisation and issuer common name.

### cert.expires { #f-cert-expires }

Certificate expiry date.

Type
:   `date`

Group
:   Certificates

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `cert.expires:<30d`{ .rn-q }

Matching
:   Future-facing: cert.expires:<30d is not-after earlier than 30 days from now (already expired certificates included).

### tls.version { #f-tls-version }

Negotiated TLS version.

Type
:   `string`

Group
:   Certificates

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `tls.version:tls10`{ .rn-q }

### content_hash { #f-content-hash }

Hash of the response body.

Type
:   `string`

Group
:   Response

Aliases
:   `body_hash`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `content_hash:8f4e2a`{ .rn-q }

### tracking { #f-tracking }

Analytics, tag manager or advertising account ID.

Type
:   `string`

Group
:   Response

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `tracking=UA-58851320`{ .rn-q }

### jarm { #f-jarm }

JARM TLS fingerprint.

Type
:   `string`

Group
:   Certificates

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `jarm:29d3fd00029d29d0`{ .rn-q }

### cert.fingerprint { #f-cert-fingerprint }

Hash of the certificate.

Type
:   `string`

Group
:   Certificates

Aliases
:   `cert.hash`

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cert.fingerprint:9f2b1c`{ .rn-q }

### header_hash { #f-header-hash }

Hash of the response header set.

Type
:   `string`

Group
:   Response

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `header_hash:3ab91c`{ .rn-q }

### is { #f-is }

Property of the web asset.

Type
:   `flag`

Group
:   Flags

Aliases
:   `has`

Operators
:   `:`

Values
:   [`live`](#is-live), [`web`](#is-web), [`new`](#is-new), [`resolved`](#is-resolved), [`auth`](#is-auth), [`cdn`](#is-cdn), [`cloud`](#is-cloud), [`waf`](#is-waf), [`screenshot`](#is-screenshot), [`important`](#is-important), [`wildcard`](#is-wildcard), [`issue`](#is-issue), [`sensitive`](#is-sensitive), [`http2`](#is-http2), [`redirect`](#is-redirect), [`vulnerable`](#is-vulnerable), [`kev`](#is-kev), [`exposed`](#is-exposed)

Example
:   `is:live`{ .rn-q }

Matching
:   is:interesting is accepted as an unlisted alias of is:exposed.

### vuln { #f-vuln }

Severity of a finding recorded on this web asset.

Type
:   `enum`

Group
:   Findings

Aliases
:   `finding`, `severity`

Operators
:   `:` `=` `!=`

Values
:   `critical`, `high`, `medium`, `low`, `info`, `unknown`

Example
:   `vuln:critical`{ .rn-q }

Matching
:   Severity of any finding in scope whose host is this hostname. Matched as a substring.

### cve { #f-cve }

Published vulnerability identifier reported on this web asset.

Type
:   `string`

Group
:   Findings

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `cve:CVE-2021-44228`{ .rn-q }

Matching
:   CVE ids on any finding on this hostname.

### exposure { #f-exposure }

The reason this web asset was flagged as an exposure.

Type
:   `enum`

Group
:   Findings

Aliases
:   `interest`, `worth`

Operators
:   `:` `=` `!=`

Values
:   `admin_interface`, `developer_tooling`, `remote_access`, `business_system`, `non_production`, `legacy`, `internal_naming`, `no_authentication`, `exposed_content`, `diagnostic`, `exploited_software`, `sensitive_service`, `certificate_anomaly`, `takeover_risk`, `ai_service`, `network_outlier`, `rare_technology`, `rare_identity`, `unprotected_edge`, `newly_appeared`, `other`

Example
:   `exposure:admin_interface`{ .rn-q }

### flagged { #f-flagged }

The source of the flag: a rule, a correlation, or AI.

Type
:   `enum`

Group
:   Findings

Operators
:   `:` `=` `!=`

Values
:   `keyword`, `rule`, `correlation`, `ai`

Example
:   `flagged:ai`{ .rn-q }

### exposure_band { #f-exposure-band }

Strength of the exposure on this web asset.

Type
:   `enum`

Group
:   Findings

Aliases
:   `interest_band`, `band`

Operators
:   `:` `=` `!=`

Values
:   `critical`, `high`, `notable`

Example
:   `exposure_band:critical`{ .rn-q }

## Flag reference

Each flag in detail, with the rule a row must meet to match it.

### is:live { #is-live }

Responded with 2xx or 3xx.

Written as
:   `is:live`, `has:live`

Matches when
:   HTTP status from 200 to 399.

### is:web { #is-web }

Answered on HTTP with any status.

Written as
:   `is:web`, `has:web`

Matches when
:   An HTTP status was recorded.

### is:new { #is-new }

Absent from every earlier scan of this target.

Written as
:   `is:new`, `has:new`

Matches when
:   An earlier scan of the same target recorded at least one hostname, and none of them recorded this hostname.

### is:resolved { #is-resolved }

Resolves to at least one IP.

Written as
:   `is:resolved`, `has:resolved`

Matches when
:   Resolved_ips holds at least one address.

### is:auth { #is-auth }

Login wall or 401/403.

Written as
:   `is:auth`, `has:auth`

Matches when
:   HTTP status 401 or 403, or the page title matches login|sign ?in|log ?in|admin|dashboard|portal|console|authenticat.

### is:cdn { #is-cdn }

Served through a CDN.

Written as
:   `is:cdn`, `has:cdn`

Matches when
:   Is_cdn is true.

### is:cloud { #is-cloud }

Hosted on a cloud provider's address.

Written as
:   `is:cloud`, `has:cloud`

Matches when
:   An HTTP asset on the hostname has cdn_type 'cloud'.

### is:waf { #is-waf }

A WAF was fingerprinted.

Written as
:   `is:waf`, `has:waf`

Matches when
:   A WAF name is recorded.

### is:screenshot { #is-screenshot }

A screenshot was captured.

Written as
:   `is:screenshot`, `has:screenshot`

Matches when
:   A screenshot path is recorded.

### is:important { #is-important }

Flagged important.

Written as
:   `is:important`, `has:important`

Matches when
:   Is_important is true.

### is:wildcard { #is-wildcard }

Matched a wildcard DNS record.

Written as
:   `is:wildcard`, `has:wildcard`

Matches when
:   Is_wildcard is true.

### is:issue { #is-issue }

Has a cert, exposure or availability problem.

Written as
:   `is:issue`, `has:issue`

Matches when
:   Certificate expired, expiring within 30 days or self-signed. Or status 500 or above. Or live with no WAF and no CDN. Or a sensitive port open.

### is:sensitive { #is-sensitive }

An admin or database port is open.

Written as
:   `is:sensitive`, `has:sensitive`

Matches when
:   A resolved address has a port from SENSITIVE_PORTS open in the row's scan.

### is:http2 { #is-http2 }

Negotiated HTTP/2.

Written as
:   `is:http2`, `has:http2`

Matches when
:   An HTTP asset on the hostname supports HTTP/2.

### is:redirect { #is-redirect }

Final URL differs from the probed URL.

Written as
:   `is:redirect`, `has:redirect`

Matches when
:   Final_url is set and differs from the probed URL.

### is:vulnerable { #is-vulnerable }

A vulnerability scan reported a finding on it.

Written as
:   `is:vulnerable`, `has:vulnerable`

Matches when
:   A finding in scope has this hostname as its host.

### is:kev { #is-kev }

A known-exploited weakness was found on it.

Written as
:   `is:kev`, `has:kev`

Matches when
:   A finding in scope on this hostname is KEV-listed.

### is:exposed { #is-exposed }

Flagged as an exposure by a rule, a correlation or AI.

Written as
:   `is:exposed`, `has:exposed`

Matches when
:   Interest_score above 0.

