---
title: Query language
description: "How to write a reNgine query: fields and operators, connectors, lists, ranges, regular expressions, dates and free text. Come here when a query does not find what you expect, or when you need an exact limit or error message."
sources:
  - shared/definitions/asset_query.py
  - shared/services/asset_query/parser.py
  - shared/services/asset_query/values.py
  - shared/services/asset_query/terms.py
revised: 2026-10-03
generated: scripts/gen_query.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_query.py` writes it from `data/query-schema.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

You write queries in three places: the query bar of every result table, the `q` field of the search operations of the HTTP API, and the `query` argument of the MCP tool `query_assets`. The grammar is the same in all three. For a guided introduction, see [Query the attack surface](../../pentesters/query.md).

## Dimensions

A dimension is one of the seven result types, and each has its own fields and flags. Open a dimension to see what you can search in it.

| Dimension | One row | Fields | Flags | Search API |
|---|---|---|---|---|
| [Web assets](web-assets.md) | One hostname recorded by one scan (a subdomains row), with the HTTP response probed on it. | 52 | 18 | `POST /api/v1/subdomains/search` |
| [Endpoints](endpoints.md) | One URL (host, path and parameter shape) recorded by one scan (an endpoints row). | 27 | 20 | `POST /api/v1/endpoints/search` |
| [Services](services.md) | One open port on one address recorded by one scan (a ports row), joined to the address, its hostnames and the HTTP response on that port. | 22 | 14 | `POST /api/v1/ports/search` |
| [IP addresses](ips.md) | One distinct IP address across the scans in scope, folded from resolved hostnames, ports, HTTP assets and ip_addresses rows. One row serves every target that shares the address. | 18 | 13 | `POST /api/v1/ips/search` |
| [Vulnerabilities](vulnerabilities.md) | One finding: one check that fired at one location in one scan (a vulnerabilities row, unique per scan and fingerprint). | 30 | 18 | `POST /api/v1/vulnerabilities/search` |
| [Software](software.md) | One software CVE: one published CVE inferred for one software name and version on one asset in one scan (a software_cves row). | 19 | 14 | `POST /api/v1/software/search` |
| [Secrets](secrets.md) | One distinct value a detector matched in a stored response, per scan (a secrets row), with its sightings. | 12 | 6 | `POST /api/v1/secrets/search` |

## Terms

A query is a list of terms. A term is `field<operator>value`, a flag such as `is:live`, or a bare word. When you put two terms side by side, a row must match both. These examples show the common shapes of a query.

| Query | Matches |
|---|---|
| `status:200`{ .rn-q } | Rows whose status equals 200 |
| `tech:nginx is:live`{ .rn-q } | Live rows whose technology contains nginx |
| `is:live and (status:403 or status:401)`{ .rn-q } | Live rows answering 403 or 401 |
| `title:"sign in"`{ .rn-q } | Rows whose title contains the phrase sign in |
| `tech:[nginx,apache]`{ .rn-q } | Rows whose technology contains either value |
| `status:200..399`{ .rn-q } | Rows with a status in the inclusive range |
| `not is:cdn`{ .rn-q } | Rows that are not served through a CDN |
| `jenkins`{ .rn-q } | Rows where any free-text field contains jenkins |

## Operators

The operator decides how reNgine compares a field with your value.

| Operator | Meaning |
|---|---|
| `:` | Contains, or equals for numbers and flags |
| `=` | Exact match |
| `!=` | Not equal |
| `>` | Greater than |
| `>=` | Greater than or equal |
| `<` | Less than |
| `<=` | Less than or equal |
| `~` | Matches regular expression |
| `!~` | Does not match regular expression |

### Operators by type

Not every operator works on every field. Find the type of a field on its dimension page, then check here which operators it accepts and how they match.

| Type | Operators | Matching |
|---|---|---|
| `string` | `:` `=` `!=` `~` `!~` | ':' case-insensitive substring. '=' case-insensitive exact. '!=' not equal (rows with no value match). '~' / '!~' case-insensitive PostgreSQL regular expression. |
| `enum` | `:` `=` `!=` |  |
| `number` | `:` `=` `!=` `>` `>=` `<` `<=` | ':' and '=' equal. Accepts a list and an inclusive a..b range. '>' '>=' '<' '<=' compare. '!=' also matches rows with no value. |
| `bytes` | `:` `=` `!=` `>` `>=` `<` `<=` |  |
| `duration` | `:` `=` `!=` `>` `>=` `<` `<=` |  |
| `date` | `:` `=` `!=` `>` `>=` `<` `<=` | Calendar date or relative age. See [Dates](#dates). |
| `ip` | `:` `=` `!=` | CIDR is containment. A full IPv4 or '=' is exact. Anything else is a substring. '!=' negates. |
| `text` | `:` `=` `!=` |  |
| `flag` | `:` | One or more flag names. A list is any-of. Unknown names are an error. |

Text fields compare without regard to case. `!=` also matches rows that have no value. A field that holds a list of values matches when any element matches, so `:` finds a substring in any element.

## Connectors

Connectors combine terms. Use them to require both terms, to accept either term, to exclude rows, or to group parts of a query.

| Syntax | Meaning |
|---|---|
| `and` | Both sides must match. Two terms side by side mean and. |
| `or` | Either side may match. |
| `not` | Excludes what follows. A leading `-` or `!` does the same. |
| `( )` | Groups part of a query, as in `is:live and (status:403 or status:401)`{ .rn-q }. |
| `" "` | Treats the value as one literal phrase. |
| `[a,b]` | Any of the listed values, as in `tech:[nginx,apache]`{ .rn-q }. |
| `a..b` | Inclusive range, as in `status:200..399`{ .rn-q }. |

These spellings mean the same, so write whichever you prefer.

| Word | Same as |
|---|---|
| `and` | `AND` |
| `&&` | `AND` |
| `or` | `OR` |
| <code>&#124;&#124;</code> | `OR` |
| `not` | `NOT` |

When a query mixes connectors, reNgine applies them in this order, tightest first: `not` or `-` or `!`, then `and` (explicit, or two terms side by side), then `or`. Use parentheses to group terms another way.

To exclude rows, write `not <term>`, `-<term>` or `!<term>`. `!=` and `!~` are operators, not negation.

## Values

How to write the value part of a term.

| Topic | Rule |
|---|---|
| Quoting | A value in double quotes is one literal. Inside quotes, backslash escapes the next character (\" for a quote). Whitespace, ( and ) end an unquoted token. |
| Lists | field:[a,b,c] matches any listed value. Items may be quoted. An empty list is an error. |
| Ranges | a..b inclusive, on number, bytes and duration fields with ':' '=' or '!='. |
| Wildcards | None. *, % and _ are literal characters. |
| Status classes | Status fields also accept `2xx`, `3xx`, `4xx`, `5xx`, `none`. |
| Presence words | True: `1`, `any`, `present`, `true`, `yes`. False: `0`, `absent`, `false`, `no`, `none`. |
| Case | Field names, connectors, flags and values are case-insensitive. `=` on a list-valued field compares one element exactly. |

### Units

Size and time fields accept a unit after the number, for example `size:>1mb`{ .rn-q } or `time:>500ms`{ .rn-q } on web assets.

| Kind | Units |
|---|---|
| Bytes | `b` = 1, `kb` = 1,024, `k` = 1,024, `mb` = 1,048,576, `m` = 1,048,576, `gb` = 1,073,741,824 |
| Duration | `ms` = 0.001 s, `s` = 1 s, `m` = 60 s, `h` = 3600 s |

### Dates

Date fields take a relative age, an absolute date or a word. For example, `discovered:<7d`{ .rn-q } finds web assets recorded in the last 7 days.

| Form | Meaning |
|---|---|
| Relative age | A number and a unit: `m`, `h`, `d`, `w`, `mo`, `y`. Relative age counts back from now: field:<7d and field:7d are within the last 7 days, field:>30d is older than 30 days. |
| Future-facing | cert.expires counts forward from now: cert.expires:<30d is before now + 30 days. |
| Absolute | `%Y-%m-%d`, `%Y/%m/%d`, `%d-%m-%Y` and ISO 8601. field:2026-01-15 is that day (24 hours from the given instant); > >= < <= compare with the instant. |
| Words | `now`, `today`, both the current instant |
| Time zone | UTC when the value carries none. |

### Regular expressions

Use `~` and `!~` when a substring is not precise enough. They take a PostgreSQL regular expression, match it without regard to case, and work on string fields only. A pattern can be up to 200 characters, and reNgine checks that it is valid before it runs. Put quotes around a pattern that contains whitespace, `(` or `)`.

## Free text

When you do not know which field holds a value, type the value on its own. reNgine matches a bare word or a quoted phrase with `:` against every free-text field of the dimension, and a row matches when any of those fields does. Each dimension page lists its free-text fields. A query can hold up to 8 free-text words. If you write `name:value` and `name` is not a field, reNgine reads it as one free-text word, and the query bar shows **"name" is not a field, searched as text**.

## Limits

Every query runs within these limits. Check them when a query is refused or a count stops at the cap.

| Limit | Value |
|---|---|
| Query length | 2,000 characters |
| Terms and connectors | 40 parts |
| Free-text words | 8 |
| Regular expression length | 200 characters |
| Largest number | 2,147,483,647 |
| Count cap | 10,000 rows. A count at the cap is reported with `total_capped: true`. |
| Groups returned | 50 |
| Statement timeout | 20s |
| Queries in one count request | 32 |

## Errors

When reNgine cannot read a query, it tells you what is wrong and where. Over the HTTP API you get HTTP 200 with an `error` object and no rows. The object holds `message`, `hint`, and the `start` and `end` offsets of the problem in the query, with `end` exclusive. In the interface, the query bar underlines that part of the query. Look up a message below to see the hint that comes with it.

| Message | Hint |
|---|---|
| The query is too long. |  |
| The query has too many parts. |  |
| Too many free-text words. | Use at most 8, or narrow with a field. |
| Unknown field '<name>'. | Press ? for the full field list. |
| <field> does not support <op>. | Accepts: <ops> |
| This filter needs a value. | Quote the value if it contains a space or a bracket. |
| This list is empty. | Name at least one value. |
| Unclosed quote. | Close it with a quote. |
| Unclosed list. | Close it with ]. |
| Unclosed group. | Close it with ). |
| Unexpected '<token>'. |  |
| The query ends early. |  |
| '<token>' has no operand. |  |
| The regular expression is too long. |  |
| '<value>' is not a valid regular expression. | <re.error text> |
| Unknown flag '<name>'. | Try one of: <flags> |
| Unknown hygiene check '<name>'. | Try one of: <values> |
| Unknown posture check '<name>'. | Try one of: <values> |
| '<value>' is not a valid number. |  |
| '<value>' is not a number. |  |
| '<value>' is not a valid date. |  |
| '<value>' is not a valid AS number. |  |
| '<value>' is not a valid rendered page hash. |  |
| '<value>' is out of range. |  |
| Field '<name>' cannot be searched. |  |

### Database errors

A query can be valid and still fail in the database, for example when the search times out. You then see one of these messages.

| SQLSTATE | Message | Hint |
|---|---|---|
| `2201B` | Invalid regular expression. | PostgreSQL regular expression syntax applies. |
| `2201G` | Invalid regular expression. |  |
| `57014` | The search timed out. | Add a field filter. |
| `22003` | A number is out of range. |  |
| `22P02` | A value has the wrong type. |  |
| `54000` | A search term is too long to index. |  |

