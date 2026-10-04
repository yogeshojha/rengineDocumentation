---
title: Set up a development environment
description: Run reNgine from a checkout on your own machine, with the source mounted into the containers so the api and the interface reload as you edit. This page covers the first run, the addresses, and what reloads by itself and what needs a restart.
sources:
  - dev-README.md
  - docker-compose.yml
  - .env.example
  - Makefile
  - api/entrypoint.sh
  - api/app/utils/helpers.py
  - frontend/Dockerfile.dev
  - frontend/vite.config.ts
  - frontend/package.json
  - README.md
revised: 2026-10-03
---

The development stack is `docker-compose.yml` in a checkout. It builds the images from their development stages, mounts your source into the containers, and publishes every port on 127.0.0.1 only.

## Requirements

Install these on your machine first:

| Item | Use |
|---|---|
| Docker Engine with the Compose v2 plugin | Runs the stack |
| `openssl` | Generates `SECRET_KEY` on the first run |
| `uv` | `make lint` runs the pinned ruff through `uvx` |
| Node.js 22 and npm | `make lint` and `make test` run the frontend checks on the host, in `frontend/` |

CI and the frontend images use Node.js 22. Run `npm ci` in `frontend/` once before you run the host checks.

## First run

These steps take you from a fresh checkout to a signed-in interface.

1. **Create the environment file.** Every service reads `.env`, and compose does not start without it.

    ```bash
    cp .env.example .env
    sed -i "s/^SECRET_KEY=.*/SECRET_KEY=$(openssl rand -hex 32)/" .env
    ```

2. **Start the stack.** `make up` runs `docker compose up -d` and builds the images that do not exist yet.

    ```bash
    make up
    ```

3. **Apply the migrations, then restart the api.**

    ```bash
    make migrate
    docker compose restart api
    ```

4. **Sign in.** Open `http://127.0.0.1:5173` and sign in with `ADMIN_USERNAME` and `ADMIN_PASSWORD` from `.env`. The setup wizard opens after your first sign-in. See [Sign in and set up](../pentesters/first-sign-in.md).

`.env.example` sets `DEBUG=true`, which relaxes the startup checks for development: `JWT_SECRET_KEY` can stay empty, and any administrator password is accepted. See [What DEBUG changes](configuration.md#debug).

## The first administrator

When the `users` table is empty, the api creates one administrator at start from these variables:

| Variable | `.env.example` |
|---|---|
| `ADMIN_USERNAME` | `rengine` |
| `ADMIN_PASSWORD` | `rengine@123` |
| `ADMIN_EMAIL` | `admin@rengine.local` |

Changing these variables later does not change an account that already exists. To change its credentials, use **Settings**.

## Addresses

Once the stack runs, you reach each service here:

| Service | Address | Bound by |
|---|---|---|
| Interface | `http://127.0.0.1:5173` | `APP_BIND_ADDR` |
| API | `http://127.0.0.1:8000` | `APP_BIND_ADDR` |
| API documentation | `http://127.0.0.1:8000/docs`, `/redoc`, `/openapi.json` | Served while `DEBUG=true` |
| PostgreSQL | `127.0.0.1:5432` | `BIND_ADDR` |
| Redis | `127.0.0.1:6379` | `BIND_ADDR` |
| Flower | `http://127.0.0.1:5555` | `BIND_ADDR`, `debug` profile |

`cache` is not published. To reach the interface and the API from another machine, set `APP_BIND_ADDR=0.0.0.0`, which publishes them on every network interface. To check that the api is up, call the health route, which needs no authentication:

```bash
curl http://127.0.0.1:8000/api/v1/health/health
# {"status":"healthy"}
```

The interface calls the API at `/api/v1` on its own origin. The Vite dev server proxies `/api` to `http://api:8000` and flushes the headers of `text/event-stream` responses, so live updates reach the browser.

## What reloads and what needs a restart

The api and the interface pick up your edits by themselves. The workers do not: after you change code they run, restart them, or they keep running the old code.

| Service | Mounted source | After a change |
|---|---|---|
| `api` | `api/app`, `shared`, `tools`, `stages`, `reports`, `interest`, `mcp`, `channels`, `connectors`, `toolbox`. `alembic` and `tests` are mounted as well. | Reloads on a change in the first ten directories. One uvicorn process runs with `--reload` and file polling. |
| `frontend` | `frontend/src`, `frontend/vite.config.ts` | Reloads through the Vite dev server |
| `worker-scans`, `worker-control`, `worker-default` | `worker/app`, `shared`, `tools`, `stages`, `reports`, `interest`, `toolbox` | No reload. Run `docker compose restart worker-scans worker-control worker-default`. |
| `worker-beat`, `ct-stream` | Same as the workers | No reload. Restart the service. |
| `channels` | Same as the api | No reload. Restart the service. |

Some changes need more than a reload or a restart:

| Change | Action |
|---|---|
| A Python dependency in the `pyproject.toml` of `api`, `worker`, `shared` or `tools` | Run `uv lock` inside the image with no compose mounts, copy the result to `api/uv.lock` and `worker/uv.lock`, then `make build`. Both images run `uv sync --locked`. |
| A frontend dependency or a file in `frontend/static` | `docker compose build frontend`, then `docker compose up -d frontend`. `node_modules` and `static` are part of the image. |
| `frontend/eslint.config.js` | `docker compose cp frontend/eslint.config.js frontend:/app/eslint.config.js`. The ESLint configuration is part of the image. |
| A new volume in `docker-compose.yml` | `docker compose up -d`. A restart keeps the old mounts. |
| A migration | `make migrate`, then restart the api |

## The frontend service

`frontend/Dockerfile.dev` builds on `node:22-slim`. It runs `npm ci`, downloads the technology logos with `scripts/fetch-tech-icons.mjs`, and starts `npm run dev`, which is `vite dev --host` on port 5173.

You can run these in `frontend/` on the host:

| Command, in `frontend/` | Runs |
|---|---|
| `npm run check` | `svelte-kit sync` and `svelte-check` |
| `npm run lint` | `prettier --check .` and `eslint .` |
| `npm run format` | `prettier --write .` |
| `npm run test` | `vitest run` |
| `npm run test:watch` | `vitest` in watch mode |

## Working in the containers

These commands cover the everyday tasks inside the stack.

| Task | Command |
|---|---|
| Python with the api's dependencies | `docker compose exec -T api /app/.venv/bin/python` |
| Import check of the api | `docker compose exec -T api /app/.venv/bin/python -c "import app.main"` |
| Shell in the api or a worker | `make shell-api`, `make shell-worker` |
| PostgreSQL shell | `make db-shell` |
| Logs | `make logs`, `make logs-api`, `make logs-worker` |
| Flower | `docker compose --profile debug up -d flower`, signed in with `FLOWER_USER` and `FLOWER_PASSWORD` |

The `python` on the container's `PATH` has none of the dependencies, so always call the virtual environment at `/app/.venv`.

## Migrations

When you change a table, write a migration for it. Migrations are hand-written under `alembic/versions/`, and the chain starts at the baseline `initial_schema`. Apply migrations before you restart the api.

```bash
make migrate-create m="add a column"   # an empty revision to hand-write
make migrate-draft  m="add a column"   # an autogenerated draft to edit down
make migrate                           # apply every pending revision
```

[Make commands](make-targets.md) lists every target. [Tests and CI](tests-and-ci.md) covers the checks CI runs.
