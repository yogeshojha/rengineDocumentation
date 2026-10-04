---
title: Secrets
description: "Everything you can search, group and sort in the secrets dimension, with example queries. Keep this page open while you write a query on secrets."
sources:
  - shared/definitions/asset_query.py
  - shared/services/surface_query/secrets.py
  - shared/definitions/notes.py
  - frontend/src/lib/components/scans/results/secrets-table.svelte
revised: 2026-10-03
generated: scripts/gen_query.py
layout: reference
nav_order: 6
---

This page is generated from the reNgine 3.0 source. `scripts/gen_query.py` writes it from `data/query-schema.json`, `data/openapi.json` and `data/mcp-dimensions.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Each row in the Secrets dimension is one distinct value a detector matched in a stored response, per scan (a secrets row), with its sightings. You search these rows in the query bar of the table, in the HTTP API with `POST /api/v1/secrets/search` and from an MCP client with the tool `query_assets`. For the syntax that works in every dimension, see [Query language](index.md).

## About this dimension

The basics: what a row is, which stages fill the dimension, and where you search it.

| Property | Value |
|---|---|
| One row is | One distinct value a detector matched in a stored response, per scan (a secrets row), with its sightings. |
| Singular and plural | secret, secrets |
| Identified by | `fingerprint` |
| Stages that add rows | [`secret_mining`](../stages/secret_mining.md) |
| Stages that cover it | [`secret_mining`](../stages/secret_mining.md) |
| Free-text fields | `subject`, `host`, `url` |
| Flag prefixes | `is:`, `has:` |
| Search API | `POST /api/v1/secrets/search` |
| Query bar placeholder | `group:cloud and is:exposed`{ .rn-q } |

Coverage tells you whether an empty table means that nothing was found or that nothing was looked for. A dimension is covered for a target when a covering stage succeeded in a run, or when a run wrote rows to it. Without coverage, the dimension reads **Not scanned**, which is not the same as zero rows.

## Fields

Fields are the properties you search on, written `field:value`. An alias works the same as the field name. Select a field to see its operators, its values and an example.

| Field | Aliases | Type | Group | Description |
|---|---|---|---|---|
| [`secret`](#f-secret) | `kind` | enum | Secret | Kind of value the detector matched. |
| [`group`](#f-group) |  | enum | Secret | Family the detector belongs to. |
| [`vendor`](#f-vendor) |  | string | Secret | Provider the value belongs to. |
| [`subject`](#f-subject) |  | string | Secret | Who or what the value names, such as an email domain or DSN host. |
| [`fingerprint`](#f-fingerprint) |  | string | Secret | Identity of one value across scans and targets. |
| [`state`](#f-state) |  | enum | State | Whether the value is exposed, public by design or expired. |
| [`source`](#f-source) |  | enum | State | Where in the response it was read. |
| [`target`](#f-target) |  | string | Asset | Target the value belongs to. |
| [`host`](#f-host) |  | string | Asset | Hostname the value was read on. |
| [`url`](#f-url) |  | string | Asset | URL the value was read from. |
| [`seen`](#f-seen) | `discovered`, `age` | date | Asset | When the value was read. |
| [`is`](#f-is) | `has` | flag | Flags | Property of the value. |

## Flags

Flags are yes-or-no properties of a row. Write them with `is:` or `has:`, for example `is:new`{ .rn-q }.

| Flag | Description |
|---|---|
| [`is:new`](#is-new) | Not read by an earlier scan of this target |
| [`is:exposed`](#is-exposed) | A private value readable in a stored response |
| [`is:public`](#is-public) | A value meant to be in the page |
| [`is:expired`](#is-expired) | A token whose expiry is in the past |
| [`is:secret`](#is-secret) | A private value, not a public identifier |
| [`is:shared`](#is-shared) | Read on more than one web asset |

## Group keys

Group the rows by one of these keys to count how many rows share each value. Use the **Group by** menu of the table, or the `groups` search operation of the HTTP API.

| Key | Label | Groups |
|---|---|---|
| `value` | Value | One row per distinct value, however many places carry it |
| `target` | Target | Values belonging to the same target |
| `secret` | Kind | Values of the same kind |
| `group` | Family | Values in the same family |
| `vendor` | Provider | Values from the same provider |
| `state` | State | Values in the same state |
| `host` | Host | Values read on one host |
| `subject` | Subject | Values naming the same subject |

## Sort

The keys you can sort by, and the order you get when you do not choose one.

| Property | Value |
|---|---|
| Sort keys | `state`, `kind`, `hosts`, `sightings`, `seen` |
| API default | `None` |
| Interface default | `state` |
| Tie-break |  |

## Columns

The table always starts with its leading columns. An export of this dimension writes the export columns.

| Set | Columns |
|---|---|
| Leading columns | **Secret** |
| Optional columns |  |
| Shown by default |  |
| Export columns | `value`, `kind`, `group`, `vendor`, `state`, `subject`, `host`, `url`, `source`, `sightings`, `hosts`, `is_secret` |

## Examples

Start from one of these queries and adjust it to your target.

### Priority

| Query | Finds |
|---|---|
| `is:exposed`{ .rn-q } | Private values readable in a response |
| `group:cloud and is:exposed`{ .rn-q } | Exposed cloud provider credentials |

### Change

| Query | Finds |
|---|---|
| `is:exposed and is:new`{ .rn-q } | Exposed values absent from every earlier scan |

### Kind

| Query | Finds |
|---|---|
| `secret:jwt and is:expired`{ .rn-q } | Expired JSON web tokens |
| `secret:aws_access_key`{ .rn-q } | AWS access keys |

### Contacts

| Query | Finds |
|---|---|
| `secret:email`{ .rn-q } | Email addresses printed in responses |
| `secret:email and subject:example.com`{ .rn-q } | Addresses on one email domain |

## Field reference

Each field in detail: its type, the operators it accepts, its values and an example.

### secret { #f-secret }

Kind of value the detector matched.

Type
:   `enum`

Group
:   Secret

Aliases
:   `kind`

Operators
:   `:` `=` `!=`

Values
:   `aws_access_key`, `aws_secret_key`, `google_api_key`, `google_oauth_secret`, `google_oauth_client_id`, `azure_storage_key`, `digitalocean_token`, `github_token`, `github_fine_grained_token`, `gitlab_token`, `npm_token`, `pypi_token`, `huggingface_token`, `stripe_secret_key`, `stripe_publishable_key`, `square_access_token`, `square_secret`, `shopify_token`, `slack_token`, `slack_webhook`, `discord_webhook`, `telegram_bot_token`, `sendgrid_api_key`, `twilio_api_key`, `mailgun_api_key`, `mailchimp_api_key`, `openai_api_key`, `anthropic_api_key`, `private_key`, `jwt`, `credential_url`, `vault_token`, `age_secret_key`, `database_url`, `sentry_dsn`, `mapbox_secret_token`, `mapbox_public_token`, `doppler_token`, `linear_api_key`, `notion_token`, `figma_token`, `postman_api_key`, `grafana_token`, `email`

Example
:   `secret:aws_access_key`{ .rn-q }

Matching
:   Values are matched as substrings of the detector key.

### group { #f-group }

Family the detector belongs to.

Type
:   `enum`

Group
:   Secret

Operators
:   `:` `=` `!=`

Values
:   `cloud`, `code`, `payments`, `messaging`, `ai`, `auth`, `data`, `platform`, `contact`

Example
:   `group:cloud`{ .rn-q }

Matching
:   Values are matched as substrings.

### vendor { #f-vendor }

Provider the value belongs to.

Type
:   `string`

Group
:   Secret

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `vendor:stripe`{ .rn-q }

### subject { #f-subject }

Who or what the value names, such as an email domain or DSN host.

Type
:   `string`

Group
:   Secret

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `subject:acme.com`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### fingerprint { #f-fingerprint }

Identity of one value across scans and targets.

Type
:   `string`

Group
:   Secret

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `fingerprint=3a9f…`{ .rn-q }

### state { #f-state }

Whether the value is exposed, public by design or expired.

Type
:   `enum`

Group
:   State

Operators
:   `:` `=` `!=`

Values
:   `exposed`, `public`, `expired`

Example
:   `state:exposed`{ .rn-q }

Matching
:   Values are matched as substrings.

### source { #f-source }

Where in the response it was read.

Type
:   `enum`

Group
:   State

Operators
:   `:` `=` `!=`

Values
:   `body`, `header`, `endpoint_body`, `endpoint_header`, `finding`

Example
:   `source:body`{ .rn-q }

Matching
:   Values are matched as substrings.

### target { #f-target }

Target the value belongs to.

Type
:   `string`

Group
:   Asset

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `target:example.com`{ .rn-q }

### host { #f-host }

Hostname the value was read on.

Type
:   `string`

Group
:   Asset

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `host:www.example.com`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### url { #f-url }

URL the value was read from.

Type
:   `string`

Group
:   Asset

Operators
:   `:` `=` `!=` `~` `!~`

Example
:   `url:/config.json`{ .rn-q }

Free text
:   Yes. A bare word searches this field

### seen { #f-seen }

When the value was read.

Type
:   `date`

Group
:   Asset

Aliases
:   `discovered`, `age`

Operators
:   `:` `=` `!=` `>` `>=` `<` `<=`

Example
:   `seen:<24h`{ .rn-q }

Matching
:   A relative age counts back from now.

### is { #f-is }

Property of the value.

Type
:   `flag`

Group
:   Flags

Aliases
:   `has`

Operators
:   `:`

Values
:   [`new`](#is-new), [`exposed`](#is-exposed), [`public`](#is-public), [`expired`](#is-expired), [`secret`](#is-secret), [`shared`](#is-shared)

Example
:   `is:exposed`{ .rn-q }

## Flag reference

Each flag in detail, with the rule a row must meet to match it.

### is:new { #is-new }

Not read by an earlier scan of this target.

Written as
:   `is:new`, `has:new`

Matches when
:   An earlier scan of the target recorded at least one secret, and none had this fingerprint.

### is:exposed { #is-exposed }

A private value readable in a stored response.

Written as
:   `is:exposed`, `has:exposed`

Matches when
:   State is exposed.

### is:public { #is-public }

A value meant to be in the page.

Written as
:   `is:public`, `has:public`

Matches when
:   State is public.

### is:expired { #is-expired }

A token whose expiry is in the past.

Written as
:   `is:expired`, `has:expired`

Matches when
:   State is expired.

### is:secret { #is-secret }

A private value, not a public identifier.

Written as
:   `is:secret`, `has:secret`

Matches when
:   Is_secret is true.

### is:shared { #is-shared }

Read on more than one web asset.

Written as
:   `is:shared`, `has:shared`

Matches when
:   Read on more than one web asset (hosts above 1)

