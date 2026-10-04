---
title: AGENTS.md
description: Give your coding agent the layout, commands, checks and rules of the reNgine repository in one file, so it follows the project's conventions and runs the same checks as CI. Save it at the root of your reNgine checkout.
sources:
  - Makefile
  - dev-README.md
  - .github/workflows/test.yml
  - .gitignore
  - pyproject.toml
  - frontend/src/lib/voice.test.ts
  - frontend/src/lib/glossary.test.ts
  - frontend/src/lib/type-scale.test.ts
  - frontend/src/lib/links.test.ts
  - frontend/src/lib/skeleton.test.ts
  - stages/base.py
  - mcp/ADDING_A_TOOL.md
  - connectors/README.md
revised: 2026-10-03
---

When you work on reNgine with a coding agent, the agent has to know where code lives, how to run the stack, and which rules a change must follow. AGENTS.md puts all of that in one file that coding agents read before they work in the repository. The repository does not ship it, so you add it to each checkout yourself.

## Where to put it

| Item | Value |
|---|---|
| File name | `AGENTS.md` |
| Location | The root of a reNgine checkout, beside `Makefile` |
| Version control | Untracked. The repository's `.gitignore` lists `AGENTS.md`. |
| Read by | Coding agents that read `AGENTS.md`. Claude Code reads it directly when the checkout holds no `CLAUDE.md`, or through the import in [CLAUDE.md](claude-md.md). |
| Length | Under 400 lines |

## What it covers

The file is split into sections, so your agent can find the rule it needs while it works:

| Section | Holds |
|---|---|
| Layout | The packages of the monorepo and the compose services |
| Run the development stack | First run, Make targets, reload and rebuild rules |
| Checks | `make lint`, `make test`, the deploy tests and what CI runs |
| Copy rules | The register for comments and interface text, the glossary and the tests that enforce them |
| Single source of truth | Each vocabulary's backend definition and frontend mirror |
| Backend conventions | Models and sessions, secrets, Postgres, workers, stages, counts, the query grammar, tools |
| Frontend conventions | Components, scrolling, icons, type scale, colour, links, stores |
| Extension points | Steps to add a stage, an MCP tool or a connector, and the location of other plug-ins |
| Before a change is done | The verification list |
| Never | Designs measured and rejected, and known traps |

## Install it

1. Download <https://rengine.wiki/agent-files/AGENTS.md>, or copy the file with the copy button on the block below.
2. Save it as `AGENTS.md` at the root of your checkout.
3. If you use Claude Code, add [CLAUDE.md](claude-md.md) beside it.

## The file

This is the full file, as your agent reads it.

````markdown
# AGENTS.md

This file tells you, a coding agent, how to work in the reNgine repository, `yogeshojha/rengine`, release 3.0: where code lives, how to run and check it, and the rules every change follows. Read it before your first change, then come back to the section you need while you work.

reNgine is a self-hosted attack surface management platform. A scan runs a pipeline of stages against one target and writes its results to seven dimensions: web assets, endpoints, services, IP addresses, vulnerabilities, software and secrets. The repository is a monorepo: a FastAPI api, Celery workers, a SvelteKit 5 interface and plug-in packages for stages, MCP tools, connectors, reports, toolbox tools and chat channels, run together with Docker Compose. One instance is shared by its users: settings are instance-wide, authentication is per user, and there are two privilege levels, user and administrator (`superuser` in code).

## Layout

Use this table to find where a change belongs.

| Path | Content |
|---|---|
| `api/` | FastAPI application. Routers in `api/app/api/v1/`, services in `api/app/services/`, middleware in `api/app/core/`. |
| `worker/` | Celery application, tasks in `worker/app/tasks/`, pipeline steps in `worker/app/orchestrator/`, the certificate stream in `worker/app/ct_stream/`. |
| `shared/` | Models, enums, definitions (`shared/definitions/`), services and utilities used by the api and the workers. |
| `stages/` | One directory per pipeline stage, discovered at import. |
| `tools/` | One wrapper per command-line tool (`tools/<tool>/client.py`, `parser.py`) and the process runner (`tools/runner/`). |
| `mcp/` | The MCP server. Tools in `mcp/tools/`, one file each. |
| `channels/` | Remote control over Telegram, a transport over the MCP tool layer. |
| `connectors/` | Proxy connectors. `clients/burp/` holds the Burp Suite extension source, `binaries/` the built jar. |
| `reports/` | Report sections (`reports/sections/<name>/`), templates, themes and rendering. |
| `interest/` | Exposure providers: rules, correlation and AI (`interest/providers/<name>/`). |
| `toolbox/` | Toolbox tools, one module each in `toolbox/tools/`. |
| `frontend/` | SvelteKit 5 interface on shadcn-svelte. Shared code in `frontend/src/lib/`. |
| `alembic/` | Hand-written migrations on one baseline, `initial_schema`. |
| `tests/` | pytest suites: `api/`, `grammar/`, `pipeline/`, `channels/`, `deploy/`, `hygiene/`, `posture/`, `toolbox/`. |
| `deploy/`, `install.sh`, `docker-compose.prod.yml` | The `rengine` command, the Chromium seccomp profile, the installer and the production stack. |
| `docker-compose.yml`, `Makefile` | The development stack and its commands. |

Compose services: `db` (Postgres 16), `redis`, `cache`, `api`, `worker-scans`, `worker-control`, `worker-default`, `worker-beat`, `ct-stream`, `channels`, `frontend`, and `flower` under the `debug` profile.

## Run the development stack

On a fresh checkout, run these commands to bring up the stack and create the database schema.

```bash
cp .env.example .env
sed -i "s/^SECRET_KEY=.*/SECRET_KEY=$(openssl rand -hex 32)/" .env
make up
make migrate
docker compose restart api
```

The interface answers on `http://localhost:5173` and the api on `http://127.0.0.1:8000`. Sign in with the first administrator, which comes from `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`.

Use these Make targets for everyday work:

| Target | Runs |
|---|---|
| `make up`, `make down`, `make build` | `docker compose up -d`, `down`, `build` |
| `make logs`, `make logs-api`, `make logs-worker` | Follow the logs of every service, the api, the three workers |
| `make lint` | `ruff check` and `ruff format --check` over every Python package, then `npm run lint` in `frontend/` |
| `make test` | pytest in the api container, then `npm run check` and `npm run test` in `frontend/` |
| `make migrate` | `alembic upgrade head` in the api container |
| `make migrate-create m="name"` | An empty revision to hand-write |
| `make migrate-draft m="name"` | An autogenerated draft to edit down |
| `make migrate-history`, `make migrate-downgrade` | Show the chain, roll back one revision |
| `make db-reset` | Drops every table and migrates again. Destructive. Reads a confirmation from the terminal. |
| `make shell-api`, `make shell-worker`, `make db-shell` | A shell in the api, in `worker-default`, or `psql` |

Know what reloads on its own and what needs a restart or a rebuild. Check this list when a change seems to have no effect:

- The api and the frontend reload on change. The workers do not: restart `worker-scans`, `worker-control` and `worker-default` after changing code they run (`worker/`, `shared/`, `stages/`, `tools/`, `reports/`, `interest/`, `toolbox/`).
- Run Python in the api container as `docker compose exec -T api /app/.venv/bin/python`. The default `python` there has no dependencies.
- Apply a migration with `make migrate`, then restart the api.
- A new compose volume needs `docker compose up -d`. `restart` keeps the old mounts. A new worker volume also goes into `volume-init` in `docker-compose.prod.yml` and into both Dockerfiles' mount points.
- A new Python dependency needs a new lock and an image build. Both images run `uv sync --locked`. Lock inside the built image with no compose mounts, then `docker compose build`:

```bash
docker run --rm --entrypoint sh -v "$PWD/api:/out" \
  -v "$PWD/shared/pyproject.toml:/src/shared.toml:ro" -v "$PWD/tools/pyproject.toml:/src/tools.toml:ro" \
  rengine-api:latest -c 'cd /app && cp /src/shared.toml shared/pyproject.toml && cp /src/tools.toml tools/pyproject.toml && cp /out/pyproject.toml /out/uv.lock . && uv lock && cp uv.lock /out/uv.lock'
```

Repeat with `worker` and `rengine-worker:latest` for `worker/uv.lock`.

- The eslint config, `node_modules` and `frontend/static` are built into the frontend image. After editing `frontend/eslint.config.js`, run `docker compose cp frontend/eslint.config.js frontend:/app/eslint.config.js`. A new npm dependency or static asset needs an image build.
- Two Redis instances: `redis` holds the broker, results, sessions and `rev:*` keys, `cache` holds evictable aggregates. Tests need both up.

## Checks

Run these before you report a change as done. CI runs the same checks.

```bash
make lint
make test
docker compose run --rm --no-deps -v "$PWD:/repo:ro" -w /repo api \
  /app/.venv/bin/python -m pytest tests/deploy -p no:cacheprovider
```

- `make lint` runs ruff 0.14.14 through `uvx`. `make lint RUFF=ruff` uses a ruff on the `PATH`. The container's ruff is a different version and is not the gate.
- Ruff targets Python 3.13, line length 88. The rule set includes `EM` (assign an exception message to `msg` before `raise`), `T20` (no `print`), `DTZ` (time-zone-aware datetimes), `S` (bandit) and `ERA` (no commented-out code).
- `npm run check` must report 0 errors. `npm run lint` is `prettier --check . && eslint .`. `npm run test` is vitest.
- CI (`.github/workflows/test.yml`) runs the same lint, the frontend checks on Node 22, pytest in the api image against `db`, `redis` and `cache`, and the deploy tests. `build-pr.yml` builds the api, worker and frontend images.
- The deploy tests skip under `/app`. Run them with the repository mounted, as above.

## Copy rules

These rules govern the product's own copy: code comments, interface text and the backend strings people read. They apply to what you write into the source, not to your messages to the user. Follow them for every comment and string you add. CI enforces part of them.

- **Comments.** One line at most. No narration, no module-header explainers, no docstring whose second sentence argues for the first. Keep functional directives (`# noqa`, `ts-expect-error`, `eslint-disable`), section dividers (`# ---------- catalog ----------`) and short labels. A fact followed by a comma and a reason: write the fact and stop. Rationale stays out of the source.
- **Interface copy.** Plain and declarative. Name the thing and state what happened. A control says what it does (`Start scan`, then `Scan started`). An error states what went wrong and how to fix it, with no apology. An empty state names what is absent.
- **Banned.** LLM register (`seamless`, `robust`, `powerful`, `leverage`, `unlock`, `elevate`, `comprehensive`, `effortlessly`, `simply`, `just`, `dive in`, `let's`), marketing adjectives, punning titles, emoji, `!`, rhetorical questions, em dashes, scare copy (`This is permanent`, `Are you absolutely sure`).
- **Tells to delete.** Justification (`because`, `so that`, `which means`, `otherwise`, `rather than`, `instead of`). Reassurance (`never`, `always`, `still`, `already`, `cannot be undone`). Reader address (`you`, `your`, `we`, `reNgine` as a subject). Metaphor. Semicolons and parentheses in prose, `?` in a title, `e.g.`, `please`. A description that restates its title is removed.
- **Canonical forms.** `<Noun> <name> and its <children> are removed.` / `Shown once. Only a hash is stored.` / `Unsaved changes are discarded.` / `<Noun> is read-only.` / `Not scanned` / `<Noun> not <verbed>.` for a failure, `<Noun> <verbed>` for a success.
- **A subtitle is a fact.** It decodes a visual encoding, names the measure the title omits, glosses a coined term or states a scope nothing on screen shows. It never restates the title, narrates the query, repeats scope a control renders or explains a sort.
- **Backend strings are product copy:** `Field(description=)`, `HTTPException(detail=)`, labels and help in `shared/definitions/`, stage config help, report prose and MCP tool descriptions.
- **Glossary.** Target (what a user adds), web asset (a probed host name, never `host`, `web host` or `live host` for that row), address, service (one `ip:port`), endpoint, finding, issue, exposure, scan and run, scan engine, scan context, schedule, stage. A stage is never called an engine. On the Agents page: agent, key and access, never token.
- **Enforced by** `frontend/src/lib/voice.test.ts` (register words, reader address, scope narration, question headings, imperative descriptions, a title restated in its description), `glossary.test.ts` (`web host`, `live host`) and `skeleton.test.ts` (a loading state is a skeleton built from the table columns, never `Loading` text or pulsing text).

## Single source of truth

Follow this whenever you add or change a value the interface shows, so the backend and the frontend cannot drift apart. Define every enum and constant once and route through it, defaults and fallbacks included: `Field(default=InstanceMode.BUG_BOUNTY.value)`, never `"bug_bounty"`. The frontend mirrors the backend. Adding a value means editing the definition, updating the mirror and checking both sides. The mirror tests in `tests/grammar/` read `frontend/src/lib/config/` and fail on drift.

| Vocabulary | Backend | Frontend mirror |
|---|---|---|
| Instance mode, mode capabilities | `shared/enums/instance.py`, `shared/definitions/mode_features.py` | `config/capabilities.ts` |
| Result dimensions | `shared/definitions/surface.py` | `config/surface.ts` |
| Ports and services | `shared/definitions/ports.py` | `config/service-classes.ts` |
| Vulnerabilities, exploit signals, evidence | `shared/definitions/vulnerabilities.py`, `threat_intel.py`, `evidence.py` | `config/vulnerabilities.ts`, `threat-intel.ts`, `evidence.ts` |
| Endpoints, exposures, correlation | `shared/definitions/endpoints.py`, `interest.py`, `correlation.py` | `config/endpoints.ts`, `interest.ts`, `correlation.ts` |
| Run comparison | `shared/definitions/compare.py` | `config/compare.ts` |
| Connectors, issue trackers, bounty reports | `shared/definitions/connectors.py`, `issue_trackers.py`, `bounty_reports.py` | `config/connectors.ts`, `issue-trackers.ts`, `bounty-reports.ts` |
| Toolbox, web hygiene, domain posture | `shared/definitions/toolbox.py`, `hygiene.py`, `domain_posture.py` | `config/toolbox.ts`, `hygiene.ts`, `domain-posture.ts` |
| Software inference, scan surface plan | `shared/definitions/software.py`, `scan_surface.py` | `config/software.ts`, `scan-surface.ts` |
| AI services, lookalike domains | `shared/definitions/ai_services.py`, `lookalikes.py` | `config/ai-services.ts`, `lookalikes.ts` |
| Concurrent scan limit, retention | `shared/definitions/scan_admission.py`, `retention.py` | `config/scan-admission.ts`, `retention.ts` |
| API key groups | `shared/enums/api_key.py`, `shared/definitions/api_keys.py` | `config/api-keys.ts` |
| Notification events and levels | `shared/definitions/notification_events.py` | `config/notification-events.ts` |
| OAST, tripwires | `shared/definitions/oast.py`, `tripwires.py` | `config/oast.ts`, `tripwires.ts` |
| MCP capabilities | `mcp/capabilities.py` | `types/mcp.ts` |
| Target types and groups | `shared/enums/target.py` | `types/target.ts` |

These frontend constants have one home each. Import them, never re-declare them: routes in `config/routes.ts`, localStorage keys in `config/storage-keys.ts`, `MASK` and `SELECT_NONE` in `lib/constants.ts`, the icon type in `config/icons.ts`, intensity in `types/scan-engine.ts`, scan status in `utilities/scan-status.ts`, dates and relative time in `utilities/dates.ts`.

## Backend conventions

Follow these when you change Python code in `api/`, `worker/`, `shared/` or any plug-in package.

### Models and sessions

- SQLModel, three schemas per entity: the table model plus `…Create`, `…Read`, `…Update`. UUID primary keys with `default_factory=uuid.uuid4`. Timestamps from `shared.utils.datetime.utc_now`. Every datetime is time-zone-aware UTC, `timestamptz`.
- A `…Read` field typed `X | None` without `= None` is required. Its serializer must fill it.
- `AsyncSession` in the api, sync `Session` in the worker.
- `shared/` never imports `fastapi` at module level. Import it lazily or under `TYPE_CHECKING`.
- Every `asn` column is `bigint`.
- Build `ip:port` with `shared/utils/net.py:host_port`, split it with `split_host_port`. Never by string formatting or by counting colons.
- New large collections page with `fastapi-pagination`.
- Log through `shared/logging.py:get_logger`. Its keyword fields crash a bare stdlib logger in the worker.

### Secrets and authentication

Apply these whenever your code touches credentials, sessions or requests to user-supplied URLs.

- Encryption is Fernet in `shared/utils/crypto.py`, keyed from `SECRET_KEY`. API keys, proxy credentials and notification secrets are encrypted at rest. Read paths decrypt and mask.
- Masked output embeds `MASK` (`••••••••`). Update paths detect it as a substring and restore the stored secret. Never persist a value containing `MASK`.
- A context or engine that carries credentials belongs to its creator (`shared/services/credential_access.py`). Only the creator or a superuser launches, schedules, edits or deletes it.
- Only a superuser sets engine `tool_options`. `shared/definitions/tools.py:DENIED_FLAGS` refuses flags that read or write worker files, load remote templates or upload results.
- Sessions travel in httpOnly cookies, never in a response body. JWT types `access`, `refresh` and `mfa` are validated at separate gates. A new sensitive verify endpoint gets the failure limiter in `api/app/core/ratelimit.py`.
- A request to a user-supplied URL goes through `shared/http.py:PublicTransport`. Test endpoints require https, a public address and no redirect.
- An httpx error never reaches a message or a log unredacted: its text carries the URL and the query string. Raise the client's own error `from None` and pass text through `shared/utils/net.py:redact_url_queries`.
- The instance mode is `bug_bounty` or `corporate`, never both.

### Postgres and migrations

Apply these when you change the schema or write queries.

- Migrations are hand-written in `alembic/versions/`. Native enum types (`apiprovider`, `notificationtype`, `targettype`, `activitylevel`, `notificationseverity`, `dnsrecordtype`, `taskstatus`, `whoislookuptype`) need `ALTER TYPE … ADD VALUE`, run outside the transaction that uses the value.
- A new result table gets indexes on `(scan_id, discovered_at)` and `(target_id, discovered_at)`. Every free-text query column gets a `pg_trgm` GIN index.
- Postgres refuses NUL. Strip with `shared/utils/text.py:strip_nul`. Catch `shared/utils/text.py:REFUSED_ROW`, never `DatabaseError` or `StatementError` alone.
- Column widths are caps defined in `shared/definitions/`. An over-long value is rejected, never truncated.
- Postgres tuning lives in the `db` service's `command:` block. Statement logging is `SQL_ECHO`, not `DEBUG`.
- Guard singleton invariants in the database: catch `IntegrityError`, take `pg_advisory_xact_lock`, add a unique constraint.

### Workers and runs

Apply these when you add a task or change how a scan runs.

- Three workers, one job each: `worker-scans` runs stages (queue `scans`), `worker-control` runs launch, hand-over, resume and finalize (`scan_control`), `worker-default` runs `default` and `critical`.
- Register a daily job in `DAILY_JOBS` in `worker/app/tasks/daily.py`, never as its own beat entry. Every beat entry carries `expires`.
- Cancel never revokes a running task: in-flight stages stop through their abort check. A tool starts in its own process group and is stopped with `killpg` in a `finally`.
- Paused is not terminal. Use the open statuses (`SCAN_OPEN_STATUSES`, `isOpenStatus`) for "will this run still produce rows" and the live statuses for spinners and clocks. Every status branch that renders a verdict needs a paused arm.
- A task that dispatches a canvas carries the run epoch it was queued for.

### Stages and the pipeline

Apply these when you add or change a stage. The steps are under Add a stage, in Extension points.

- The stage's config model is the single source for its settings: `GET /api/v1/engines/catalog` serves its JSON Schema, the interface renders forms from it, the api validates with it. Never mirror engine settings or hand-write a stage form.
- A config field is a decision, never a transport knob. Rate, concurrency, timeout and retries come from `shared/definitions/intensity.py` per tool and intensity. A stage declares `transport_tool` and reads `self.transport`. A knob whose only safe value is its default is a constant in the stage's `config.py`.
- Mark advanced fields with `advanced(...)` from `stages/config.py`.
- `depends_on` is the execution graph. Levels are derived. `phase` is display only.
- `touches_target` states whether any part of a stage sends traffic. A stage with passive sources also sets `passive_capable = True` and gates its own active providers.
- `always_on` marks a stage that cannot be switched off. Passive intensity still turns it off when it touches the target.
- A support stage that writes findings declares `check_of` and `finding_severities`.
- A PATCH of an engine's `stages` replaces the map. `merge_engine_context` is the only place defaults are filled.
- The built-in engine is defined in `shared/definitions/default_engine.py`. It is editable and never deleted.
- Never build a vulnerability scanner's target list inside a stage. `shared/services/scan_surface/` plans it.

### Results and counts

Every number the interface shows has to match the rows it opens. These rules keep it that way.

- A stage writes while its tool runs through `stages/sink.py:ResultSink`. The `write` callback commits. Clear the previous attempt inside the first flush. Only the stage thread writes.
- `shared/services/ip_inventory.py` and `port_inventory.py` are the only writers of their tables.
- Nothing about a run is dropped silently. A scanner that raises gets a `failed` coverage row, a missing one `skipped`.
- The count is a promise: a displayed number equals the rows its link opens. Counts, leads, facets, widgets, hubs and MCP `pivot` links use the same scope, filter and compiler as the search they open. Click every new number.
- A dimension no scan produced reports `covered=false`, rendered `Not scanned`, never zero. A null count means "not reported", never zero. Read counts from the tables, never from the `scans.*_found` rollup columns.
- `is:new` needs a baseline: a target's first scan reports nothing as new.
- A run's row, first-seen and retired counts are stored with a revision stamp in `shared/services/scan_deltas.py`. Never recount per request.

### Query grammar

Apply these when you add a query field or change the compiler.

- Fields live in one registry, `shared/definitions/asset_query.py`. Adding a field is one `QueryField` plus one builder. Help, autocomplete and validation follow.
- Import the compiler from `shared/services/asset_query`, never from a submodule. Reuse `terms.py` and `predicates.py`.
- `NOT` is null-safe through `_negate()`. Every `_*_baseline` stays non-correlated.
- A parse error returns `200` with `error`, never a 4xx.
- A view is scoped by a `QueryScope`, never a bare scan id.
- Take nouns from `shared/definitions/surface.py:SURFACE_NOUN`, never a literal `host` or `address` in a component.

### Tools

Apply these when you wrap a command-line tool or pass it flags.

- A tool that shells out lives in the worker image only. Binaries are pinned in `worker/Dockerfile`.
- Tool args add flags, never restate one. `tools/runner/executor.py:merge_extra_args` drops a flag the stage already set.
- Measure a flag before relying on it. Known cases: naabu and dnsx take `-timeout` as a duration (`3s`), the others take seconds. `urlfinder` has no `-t`. `alterx` and `julius` read input on stdin. The header flag differs per tool (`HEADER_FLAG` in each client, pinned by `tests/pipeline/test_tool_header_flags.py`). `CLIToolRunner.run` adds `json_flag` only with `OutputFormat.JSONL`.
- A rate is a budget for the stage, shared by every process it starts (`stages/config.py:share_rate`).
- Decode tool output with `errors="replace"`.

## Frontend conventions

Follow these when you change code in `frontend/`. Tests enforce several of them.

- Svelte 5 runes (`$state`, `$derived`, `$effect`, `$props`) and shadcn-svelte components only. No hand-rolled equivalents.
- Scrolling is `ScrollArea` only, never raw `overflow`. It needs a definite or `flex-1 min-h-0` height to clip.
- Icons from `@lucide/svelte` only, one default import per icon: `import Globe from '@lucide/svelte/icons/globe'`. Country flags from `flag-icons`, never emoji. Tech logos are vendored by `frontend/Dockerfile.dev`. The only mapping is `tech-icons.ts:ICON_ALIASES`.
- Type scale: `text-2xs`, `text-xs`, `text-sm`, `text-base`, `text-lg`. Never `text-[Npx]`. `lib/type-scale.test.ts` fails on one.
- Colour comes from the OKLch tokens and the semantic layer (`--destructive`, `--success`, `--warning`, `--info`, `--chart-1..5`), never raw palette classes or hex. Colour encodes outcome or identity. No gradients. Do not reorder `--chart-1..5`.
- Every link to a value something else wrote goes through `utilities/links.ts` (`externalHref`, `safeHref`, `openExternal`). `lib/links.test.ts` fails on an `href` bound to anything else and on `window.open` outside that module.
- Code renders through `code-block.svelte` (read-only) or `yaml-editor.svelte` (editable), as spans. Never `{@html}` for target-written text. No bare `<pre>`.
- Hover hints use `hint.svelte`, never `title=`. Never nest `Tooltip.Trigger` inside a `DropdownMenu.Trigger` or `Popover.Trigger`.
- Reuse the shared primitives in `frontend/src/lib/components/`: `confirm-dialog`, `loading-button`, `scan-status-badge`, `empty-state`, `form-field`, `count-tabs`, `hint`, `panel-head`, `section-head`, `code-block`, `yaml-editor`, and `scans/results/table/` and `scans/results/query-bar/`. Destructive flows go through `confirm-dialog`.
- Column widths live in the table's `columns.ts`. Result tables pin actions right, wrap text, show no count of one and put state on the value.
- Catalog-driven surfaces render from the served schema: the engine builder, the query bar, the report builder, the toolbox forms. A new stage, section or tool needs no frontend work.
- Reset every data-caching store in `stores/auth.svelte.ts:clearSession`. A per-project store refetches when `fetchedProjectId !== activeProject.id`.
- A tab renders when its count is above zero, or while a live scan has a planned producer. `Not scanned` is the one absence a page states in words.
- Disclosure starts closed. Motion only where it encodes a live value. `animate-pulse` is for skeletons.
- Every scan tab body sits in a `<svelte:boundary>`.
- Requests per page are a budget. A per-row fetch gets a batch endpoint. Several counts over one scope are one `POST */search/counts`.
- In the query bar, Enter searches, Tab completes, nothing is pre-highlighted.
- Svelte traps: a `$state` proxy cannot be `structuredClone`d. A `{#snippet}` declared in a component body becomes a prop. A `$derived` named `state` breaks the `$state` rune. Write `onclick={() => run()}`, not `onclick={run}`.

## Extension points

New stages, MCP tools, connectors and the other plug-ins below each live in their own directory or file. Use these steps when you add one.

### Add a stage

1. Create `stages/<name>/stage.py` with a `Stage` subclass from `stages/base.py`: `name`, `title`, `description`, `depends_on`, `consumes`, `produces` (`AssetKind` values), `group` (`StageGroup`), `role` (`StageRole`), `touches_target`, `transport_tool`, `config_model`, and `run() -> StageResult`.
2. Create `stages/<name>/config.py` with a `StageConfig` subclass. Each `Field` carries the label (`title`), the help (`description`) and the bounds.
3. No registry edit and no `__init__.py`. The registry validates the declaration at import.
4. Restart the workers and the api. List the stages: `docker compose exec -T api /app/.venv/bin/python -c "from stages.registry import stages; print([s.name for s in stages()])"`.
5. Run `tests/pipeline/`. `test_stage_knobs.py` fails on a field named like a transport knob or read by no code. `test_check_severities.py` fails on a finding writer without `check_of` and `finding_severities`.

### Add an MCP tool

1. Create one file in `mcp/tools/` with a `Tool` subclass from `mcp/tools/base.py`: `name` (snake case, unique), `title`, `description` (written for the model, says when to call it), `capability`, `group`, `Input` (a `ToolInput` model, each field with a `description`) and `async run(ctx, args) -> ToolResult`.
2. `capability` is `launch` for a tool that sends traffic to a target and at least `write` for a tool that writes. Set `destructive = True` for a tool that destroys data and refuse the call without an explicit confirm.
3. Set `pivot` wherever a count is reported. A tool with no such link reports no count. Set `untrusted=True` wherever target-written text is returned. Put what the answer cannot state in `caveats`.
4. Read targets inside the token scope through `mcp/tools/_scope.py` (`find_target`, `resolve`, `scan_in_scope`). Call `scope.require(dim)` before reporting a dimension. Import services inside `run`. Raise `ToolError` with a message the model can act on.
5. A chat command is `command` (`^[a-z][a-z0-9]{1,15}$`) plus `value_field`, placed in `COMMAND_GROUPS` in `shared/definitions/channels.py`. `tests/channels/test_commands.py` pins the set.
6. Run `ruff check mcp`, restart the api and check `docker compose exec -T api /app/.venv/bin/python -c "from mcp.registry import registry; print(sorted(registry()))"`. The full contract is in `mcp/ADDING_A_TOOL.md`.

### Add a connector

1. Create `connectors/<name>/__init__.py` and `connectors/<name>/connector.py` with a `ProxyConnector` subclass from `connectors/base.py`: `kind` (a `ConnectorKind` member), `title`, `client_pattern` (a glob under `binaries/`) and `setup()` returning the setup steps.
2. Add the kind to `shared/definitions/connectors.py` and its mirror `frontend/src/lib/config/connectors.ts`.
3. Proxy-facing responses stay flat JSON objects or flat arrays of flat objects. A connector setting exists only when the server acts on it. The contract is in `connectors/README.md`.

### Other plug-ins

For these plug-ins, start from the location below and follow an existing one of the same kind.

| Plug-in | Location |
|---|---|
| Toolbox tool | One module in `toolbox/tools/` with a `Tool` subclass from `toolbox/base.py` |
| Report section | `reports/sections/<name>/section.py` and `section.html` |
| Exposure provider | `interest/providers/<name>/provider.py` with an `InterestProvider` subclass |
| Query field | One `QueryField` in `shared/definitions/asset_query.py` plus one builder |
| Downloaded dataset | One `DatasetSpec` in `shared/definitions/datasets.py` and one loader |
| Bounty platform | A provider in `shared/services/bounty_providers/`, an `APIProvider` value with its `ALTER TYPE`, `PlatformSpec.api_provider`, and a tester in `API_KEY_TESTERS` |
| DAST fuzzer | A module in `stages/dast_scan/scanners/` |
| MCP client snippet | One `ClientSpec` in `mcp/clients.py` |

## Before a change is done

Work through this list before you report a change as finished.

1. `make lint` is clean.
2. `docker compose exec -T api /app/.venv/bin/python -c "import app.main"` succeeds.
3. `make test` is green: pytest, `npm run check` with 0 errors, vitest.
4. The changed endpoint answers: sign in, then call it. A new count, clicked, opens exactly that many rows.
5. A migration applied with `make migrate`, then the api restarted.
6. Every comment and string added reads against the copy rules.
7. Before deleting code, count references across the repository. vulture and ts-prune report false positives here.

## Never

These designs were measured and rejected. Do not build them again, even when one looks like an improvement:

- Parallel dnsx resolver batches. `DNS_BATCH_CONCURRENCY` stays 1.
- amass in the default passive tool set.
- Per-address GIN lookups in place of the `hosts` CTE for service baselines.
- An `ix_ports(target_id, ip, number)` index.
- A `cert.issued` correlation kind.
- Parameter mining by status and length.
- Streaming level 0 of the pipeline into level 2.
- One toolbox query box that runs every matching tool.
- Hiding the `always_on` control.
- MaxMind, DB-IP or httpx `-asn` for address to ASN. A keyless install still gets ASN and country.
- Chromium or Typst for report rendering, the `mcp` package from PyPI, a durable `mcp_calls` table, a second matcher for interest rules.
- A cached aggregate per target summed into a project figure.
- Dropping `ix_subdomains_name`.

Avoid these traps:

- Never add a stage config field for rate, concurrency, timeout or retries. Transport comes from the intensity profile.
- Never set `visibility_timeout` or `result_expires` below the task hard time limit.
- Never terminate a revoked scan task. A killed child orphans its tool.
- Never write `f"{ip}:{port}"`.
- Never persist `MASK`.
- Never default the public OAST server on.
- Never attribute an address to the network of its target. Only an ASN target states the network of its own sweep.
- Never add the `mcp` PyPI package without renaming the local `mcp` package it shadows.
````
