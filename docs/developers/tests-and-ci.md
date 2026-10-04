---
title: Tests and CI
description: Run the tests CI runs before you open a pull request, find which suite covers the code you changed, and see what each source check looks for when it fails.
sources:
  - tests/conftest.py
  - pyproject.toml
  - frontend/vitest.config.ts
  - frontend/package.json
  - frontend/src/lib/voice.test.ts
  - frontend/src/lib/glossary.test.ts
  - frontend/src/lib/links.test.ts
  - frontend/src/lib/type-scale.test.ts
  - frontend/src/lib/skeleton.test.ts
  - .github/workflows/
  - .pre-commit-config.yaml
  - clients/burp/test.sh
  - Makefile
revised: 2026-10-03
---

reNgine has two test suites. The Python suite runs with pytest inside the api container, against a database of its own. The frontend suite runs with vitest and includes source checks for copy, links and the type scale. GitHub Actions runs both on every push and pull request to master and the release branches.

## Python tests

The suite lives in `tests/`, and the api container mounts `tests/` and the root `pyproject.toml`. Use this table to find the directory for the code you changed, and its marker if you want to run only that part.

| Directory | Marker | Covers |
|---|---|---|
| `tests/api/` | `api` | Routes and services exercised through the HTTP surface: auth, sessions, two-factor, throttling, connectors, MCP, dashboards, reports, scan scope |
| `tests/channels/` | `channels`, set in `tests/channels/conftest.py` | Remote control: the command set, dispatch guards, rendering, step-up |
| `tests/deploy/` | | The deployment files: compose services, Dockerfiles, the installer, backup and update, the release workflow |
| `tests/grammar/` | `grammar` | The asset query language, counts, and the frontend mirrors of backend vocabularies |
| `tests/hygiene/` | `hygiene` | Web hygiene checks read off stored responses |
| `tests/pipeline/` | `pipeline` | Scan orchestration and stage behaviour: canvas shape, pause and resume, tool arguments, redaction, parsers |
| `tests/posture/` | `posture` | Sender, mail and zone checks read from DNS |
| `tests/toolbox/` | | Toolbox lookups |

`tests/channels/` has no `__init__.py`, and must not get one: an `__init__.py` there makes `tests.channels` shadow the `channels` package under pytest.

`pyproject.toml` configures pytest: `testpaths = ["tests"]`, `asyncio_mode = "auto"`, `addopts = "-q --strict-markers --strict-config"`, and the six markers above.

### Test database

Your tests never touch the development data. `tests/conftest.py` creates a database of its own for each run:

1. Takes a Postgres advisory lock for the database name.
2. Drops and creates `POSTGRES_TEST_DB`, default `rengine_test`.
3. Runs `alembic upgrade head` against it.
4. Gives each test one transaction and rolls it back.

The suite needs `db`, `redis` and `cache` running.

### Run the Python tests

Run the whole suite, or only the directory or file you are working on:

```bash
# the whole suite, as make test runs it
docker compose exec -T api /app/.venv/bin/python -m pytest tests -q

# one directory or one file
docker compose exec -T api /app/.venv/bin/python -m pytest tests/pipeline -q
docker compose exec -T api /app/.venv/bin/python -m pytest tests/grammar/test_promise.py -q
```

Inside `/app`, the deployment tests skip with `deployment files are not mounted here`. To run them, mount the repository:

```bash
docker compose run --rm --no-deps -v "$PWD:/repo:ro" -w /repo api \
  /app/.venv/bin/python -m pytest tests/deploy -q -p no:cacheprovider
```

The mirror tests in `tests/grammar/` read the frontend configuration from `/app/frontend-config`, which the development compose file mounts read-only from `frontend/src/lib/config`.

## Frontend tests

`frontend/vitest.config.ts` runs every `src/**/*.test.ts` in the Node environment. Put a unit test beside the module it tests, for example `src/lib/utilities/dates.test.ts`.

Five tests in `src/lib/` read the source tree itself and fail when a file breaks a project rule. Each one walks `frontend/src` and skips `lib/components/ui`. If one of them fails on your change, this table tells you what it looks for:

| Test | Reads | Fails on |
|---|---|---|
| `voice.test.ts` | `.svelte` files | Interface copy that breaks the writing rules. See [Product copy rules](copy-rules.md). |
| `glossary.test.ts` | `.svelte` and `.ts` files, tests excluded | `web host` or `live host`, singular or plural |
| `links.test.ts` | `.svelte` and `.ts` files | A link attribute bound to anything other than a route, a literal or `externalHref` and `safeHref` from `utilities/links.ts`. A `window.open` outside `utilities/links.ts`. |
| `type-scale.test.ts` | `.svelte` and `.ts` files | An arbitrary text size such as `text-[13px]` |
| `skeleton.test.ts` | `.svelte` files | `Loading`, `Searching` or `Fetching` text where a skeleton belongs, outside the three boot screens. Pulsing text. Table skeletons not built from the table columns. |

### Run the frontend checks

Run these in `frontend/` on the host:

```bash
cd frontend
npm ci
npm run check                          # svelte-kit sync and svelte-check
npm run lint                           # prettier --check and eslint
npm run test                           # vitest run
npx vitest run src/lib/voice.test.ts   # one file
```

## Burp Suite extension

If you change the Burp Suite extension, test it yourself, because CI does not. `clients/burp/test.sh` compiles the extension and its harnesses with `javac --release 17 -Werror` and runs the offline `ActionsHarness`. It needs a JDK 17 or later, and downloads the Montoya API jar on the first run.

## Pre-commit hooks

Pre-commit hooks check your changes each time you commit. `.pre-commit-config.yaml` runs ruff 0.14.14 (fix, format and check) on the Python packages, prettier on `frontend/`, and the `pre-commit-hooks` v6.0.0 checks: trailing whitespace, end of file, YAML, JSON, files over 1,000 KB, merge conflicts and private keys.

## CI workflows

The workflows live in `.github/workflows/`. On your pull request, `test.yml` runs the tests and `build-pr.yml` checks that the images still build. The others build and publish releases and scan the code.

| File | Name | Triggers | Runs |
|---|---|---|---|
| `test.yml` | Tests | Push and pull request to `master` and `release/*` | Three jobs, below |
| `build-pr.yml` | Build Docker images for pull request | Pull request to `master` and `release/*` | Builds the production images without pushing: api amd64, worker amd64 and arm64, frontend amd64 |
| `build.yml` | Build and Push Docker images | Push to `master`, tags `v*` | Builds the api, worker and frontend images for amd64 and arm64 on native runners, pushes them to Docker Hub and `ghcr.io`, publishes the multi-architecture manifests, and drafts the GitHub release for a tag. Runs only in `yogeshojha/rengine`. |
| `auto-release.yml` | Update Version and Changelog and Readme | Release published | Writes the tag to `VERSION`, prepends the release notes to `CHANGELOG.md`, updates the version badge in `README.md`, and commits to the default branch |
| `codeql-analysis.yml` | Code Quality | Push and pull request to `master`, and weekly on Friday at 18:00 UTC | CodeQL for JavaScript and Python |
| `github-pages-deploy.yml` | Deploy README to GitHub Pages | Push to `master`, manual | Renders `README.md` to HTML and publishes it to the `gh-pages` branch |
| `auto-comment.yml` | Auto Comment | Issue opened, pull request opened or closed | Posts a comment on the issue or pull request |

`test.yml` runs three jobs:

| Job | Steps |
|---|---|
| `lint` | `uvx ruff@0.14.14 check` and `uvx ruff@0.14.14 format --check` over every Python package |
| `frontend` | Node.js 22: `npm ci`, `npm run lint`, `npm run check`, `npm run test` |
| `pytest` | Writes a throwaway `.env` with `DEBUG=true`, builds the api image, starts `db`, `redis` and `cache`, runs `pytest tests`, runs the deployment tests with the repository mounted, prints the `db` and `api` logs on failure, and removes the stack with its volumes |

A newer push to the same ref cancels a running `test.yml` or `build-pr.yml`.

## Before a pull request

Check these four things before you open a pull request:

1. `make lint` passes.
2. `make test` passes.
3. `docker compose exec -T api /app/.venv/bin/python -c "import app.main"` returns without error.
4. Every new comment and interface string follows the [product copy rules](copy-rules.md).
