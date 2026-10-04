---
title: How data is stored
description: See how reNgine stores targets, scans and results in PostgreSQL 16, how it tells one result row from another, and how it compares runs and deletes old data. Read this before you write a migration, add a result table or query the database.
sources:
  - alembic/versions/2026_10_03_3f8b2d6c1a94_initial_schema.py
  - shared/models/
  - shared/models/scan.py
  - shared/models/instance_settings.py
  - shared/models/note.py
  - shared/services/scan_scope.py
  - api/app/services/surface_scope.py
  - shared/services/retention.py
  - shared/definitions/retention.py
  - shared/definitions/endpoints.py
  - tools/nuclei/parser.py
  - shared/services/software_match.py
  - shared/services/secret_mining/record.py
  - stages/base.py
  - stages/sink.py
revised: 2026-10-03
---

reNgine keeps everything in PostgreSQL 16. The idea to hold on to: every result row belongs to one run of one target, and each dimension identifies its rows by a key that is unique within that run.

## Conventions

Every table follows these conventions. Follow them too when you add one.

| Convention | Rule |
|---|---|
| Models | SQLModel classes in `shared/models/`. Each entity has a table model and `Create`, `Read` and `Update` schemas. |
| Primary keys | UUID, generated in Python with `uuid.uuid4` |
| Time | Every datetime column is `timestamptz`, in UTC |
| Lists and maps | JSON or JSONB columns |
| Migrations | Hand-written Alembic revisions in `alembic/versions/`. The chain starts at the baseline `initial_schema`, revision `3f8b2d6c1a94`, which creates 110 tables. |
| Extensions | `pg_trgm`, `pg_stat_statements` |

## Ownership

Everything hangs off a project. The tree shows what belongs to what:

```text
users
  └─ projects (created_by)
       ├─ targets            unique (target_value, project_id)
       │    ├─ target_seeds, target_tags, target_organizations
       │    └─ scans          one row per run
       │         ├─ scan_activities   one row per stage
       │         │    └─ scan_commands
       │         └─ result rows: subdomains, http_assets, endpoints, ports,
       │                         ip_addresses, vulnerabilities, software_cves,
       │                         secrets, interest_signals
       ├─ scan_engines, scan_contexts, scan_schedules
       ├─ organizations, tags
       ├─ interest_rules
       └─ notes  (target, optional scan and asset)
```

Every result row carries `scan_id`, `target_id` and `project_id`. Deletes cascade down the tree: deleting a target deletes its scans, and deleting a scan deletes its result rows, its activities and their commands. These foreign keys use `ON DELETE CASCADE`.

## Core tables

These tables hold the accounts, projects, targets and scans that the results hang from.

| Table | Holds | Relations |
|---|---|---|
| `users` | Accounts. `is_superuser` marks an administrator. | Unique `username` and `email` |
| `projects` | Projects | Unique `slug` |
| `targets` | Domains, IP addresses, CIDR ranges, URLs and ASNs a user adds | `project_id`. Unique `(target_value, project_id)`. |
| `target_seeds` | Seed values of a target | `target_id`. Unique `(target_id, value)`. |
| `organizations`, `tags` | Labels for targets | `project_id`. Joined to targets through `target_organizations` and `target_tags`. |
| `scans` | One row per run: status, scope, the resolved `execution_config`, counters, timings | `target_id`, `project_id`. `engine_id`, `context_id` and `schedule_id` are stored with `engine_name` and `context_name` and carry no foreign key. |
| `scan_activities` | One row per stage of a run: status, error, result | `scan_id` |
| `scan_commands` | Commands a stage ran | `activity_id`, `scan_id` |
| `scan_engines` | Saved stage selections | `project_id`. One built-in engine per project, `ux_scan_engines_builtin_project`. |
| `scan_contexts` | Scope, authentication, rate limits and proxy | `project_id` |
| `scan_schedules` | Recurring launches | `project_id` |
| `notes` | Notes on a target, a run or one asset | `project_id`, `target_id`. `scan_id` is set to null when the run is deleted. An asset is named by `dimension` and `asset_key`. |
| `interest_rules` | Saved exposure rules | `project_id` |
| `interest_signals` | Exposure signals on a web asset: source, kind, weight and reason | `scan_id`, `subdomain_id`. Unique `(scan_id, subdomain_id, source, key)`. |
| `instance_settings` | One row of instance-wide settings | Unique `singleton_key` |
| `mcp_tokens` | Agent keys, stored as a hash | Unique `token_hash` |
| `connectors` | Proxy connector connections | Unique `(project_id, kind)` |

## Result tables

Each result dimension has one table. A row's identity key is unique within its run, so the same asset seen by two runs is two rows. That is what lets reNgine compare one run with another.

| Dimension | Table | Row | Identity within a run |
|---|---|---|---|
| Web assets | `subdomains` | web asset | `(scan_id, name)` |
| Services | `ports` | service | `(scan_id, ip, number, protocol)` |
| IP addresses | `ip_addresses` | address | `(scan_id, ip)` |
| Endpoints | `endpoints` | endpoint | `(scan_id, signature)`. `signature` is the SHA-256 of `scheme://host:port`, the path and the sorted parameter names. |
| Vulnerabilities | `vulnerabilities` | finding | `(scan_id, fingerprint)`. `fingerprint` is the SHA-256 of the scanner, the template id, the matcher name and the location. |
| Software | `software_cves` | software CVE | `(scan_id, fingerprint)`. `fingerprint` is the MD5 of the host name or address, the port, the vendor, the product, the version and the CVE. |
| Secrets | `secrets` | secret | `(scan_id, fingerprint)`. `fingerprint` is the SHA-256 of the kind and the value. |

These supporting tables hold the detail behind the result rows:

| Table | Holds | Identity |
|---|---|---|
| `http_assets` | The HTTP response of each probed URL: status, headers, TLS, technologies, screenshot, stored body | `(scan_id, url)` |
| `endpoint_responses` | The response headers and body `endpoint_probe` read for an endpoint | Primary key `endpoint_id` |
| `secret_sightings` | Each place a secret was seen | `(secret_id, url, source)` |
| `vulnerability_coverage`, `secret_coverage`, `endpoint_coverage` | What a run tested and what it could not | Per run |

The query language maps its fields to these tables. See [Query language](../reference/query/index.md).

## Writing rows

Rows are written while a scan runs, so the interface can show them before the scan ends. This is the order of events:

1. A stage writes rows while its tool runs, through `ResultSink`. The sink commits every 500 rows or 2 seconds.
2. A stage that runs again clears its earlier rows of the same run inside its first flush.
3. After each flush, `Stage.publish_results` recomputes the run's counters and emits the `results_found` event.
4. Finalize stores the settled counts on the `scans` row.

Each counter on the `scans` row matches one dimension:

| Counter on `scans` | Dimension |
|---|---|
| `subdomains_found` | Web assets |
| `ips_found` | IP addresses |
| `open_ports_found` | Services |
| `http_assets_found` | Probed URLs |
| `endpoints_found` | Endpoints |
| `vulnerabilities_found` | Vulnerabilities |
| `secrets_found` | Secrets |

`shared/services/ip_inventory.py` and `shared/services/port_inventory.py` are the only writers of `ip_addresses` and `ports`. Identity columns and `discovered_at` are not updated in place.

## Runs and the project view

A project-wide page has to choose which run to show for each target. This section explains how it does that.

`scans.scope` is `full` or `focused`. A full scan describes the whole surface of its target. A focused run tests selected assets only.

A project-wide result page reads, for each target and dimension, the newest full scan that covers the dimension. A scan covers a dimension when it wrote rows for it or when a stage that covers it succeeded. The vulnerabilities dimension also reads the completed new-checks runs started after that scan. A target with no covering scan is **Not scanned** for the dimension, which is distinct from zero rows.

A page for one run reads the rows of that `scan_id`.

## Change across runs

reNgine shows what is new and what went away by comparing the rows of two runs by their identity key. A row is new when no earlier scan of the same target recorded its key. The first scan of a target has no baseline, so it reports nothing as new.

reNgine stores these counts instead of counting them again on every request:

| Table | Holds |
|---|---|
| `scan_deltas` | Row and first-seen counts per run and dimension |
| `scan_retired` | Count of rows of the previous run that a run no longer records, per dimension |
| `scan_revisions` | `rows_rev` and `history_rev` per run and dimension |

Statement triggers on the seven dimension tables bump `scan_revisions` on every insert and delete. A stored count is valid while its revision matches. Finalize computes the counts of a run, and the `scan-deltas-backfill` task computes the rest every 5 minutes.

## Retention

Retention deletes old scans and old evidence on a schedule. Two windows on `instance_settings` control it, and the `retention-enforce` task applies both every 24 hours.

| Setting | Default | Values | Deletes |
|---|---|---|---|
| `scan_history_retention_days` | 90 | 30, 60, 90, 180, 365, or 0 to keep | Finished scans older than the window, with their result rows, activity log entries and screenshots |
| `screenshot_retention_days` | 30 | 7, 14, 30, 60, 90, or 0 to keep | Screenshots of finished scans older than the window, the stored response bodies of `http_assets`, and the `endpoint_responses` rows |

These rules decide what a pass deletes:

- A scan is finished when its status is `completed`, `failed` or `cancelled`. Its age is measured from `completed_at`, or `created_at` when it has none.
- The scan window keeps the most recent finished scan of every target, and the most recent finished full scan of every target.
- One pass deletes at most 200 scans.
- Deleting evidence clears `screenshot_path` on `subdomains` and `http_assets` and removes `/app/scan_media/<scan id>`.

`PATCH /api/v1/instance-settings` refuses other values with 400, for example `Scan history retention must be 30, 60, 90, 180, 365 days, or 0 to keep forever.` See [How reNgine is configured](configuration.md).
