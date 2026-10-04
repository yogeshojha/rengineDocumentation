---
title: Write a connector
description: Connect another web proxy to reNgine, the way the Burp Suite connector does. What you browse in the proxy comes back as endpoints of your target, and findings, web assets and endpoints go from reNgine to the proxy.
layout: pane
sources:
  - connectors/README.md
  - connectors/base.py
  - connectors/registry.py
  - connectors/auth.py
  - connectors/ingest.py
  - connectors/handoff.py
  - connectors/notice.py
  - connectors/burp/connector.py
  - shared/utils/bearer.py
  - shared/definitions/connectors.py
  - shared/models/connector.py
  - shared/services/proxy_sync.py
  - api/app/api/v1/connectors.py
  - api/app/services/connector.py
  - frontend/src/lib/types/connector.ts
  - frontend/src/lib/config/connectors.ts
  - binaries/
  - clients/burp/
  - tests/api/test_connectors.py
revised: 2026-10-03
---

Write a connector when you test through a proxy other than Burp Suite and want it to work with reNgine. A connector has two halves. On the reNgine side, a `ProxyConnector` subclass in its own directory under `connectors/` describes the connector and its setup steps. On the proxy side, a client, such as a proxy extension, calls the connector endpoints with a connector token. reNgine records the traffic it receives as endpoints with source `proxy`, so the Endpoints page, the query language, reports and MCP see your browsing the same way they see a crawl.

One connector ships today: Burp Suite, through a Montoya extension built from `clients/burp/`. The `connectors` package is mounted into the api image only. You do not register a connector anywhere. The registry imports `connectors.<dir>` and `connectors.<dir>.connector` for every directory under `connectors/` whose name does not start with `_` or `.`, creates each concrete `ProxyConnector` subclass, checks it and keys it by `kind`.

A project holds one connection per kind (`uq_connector_project_kind`). Administrators create, change, rotate and delete connections. To see the Burp Suite connector from the pentester's side, read [Burp Suite](../pentesters/burp-suite.md).

These are the files you work with:

| Path | Content |
|---|---|
| `connectors/<name>/connector.py` | The `ProxyConnector` subclass |
| `connectors/<name>/__init__.py` | The package marker |
| `connectors/base.py` | `ProxyConnector`, `SetupStep`, `CLIENT_DIR`, `release_key` |
| `connectors/registry.py` | Discovery and validation: `connectors()`, `connector(kind)` |
| `connectors/auth.py` | The token format: `mint`, `PREFIX`, `looks_like_token`, `fingerprint`, `from_header` |
| `connectors/ingest.py` | `prepare()`: folds a batch of proxy items into request shapes |
| `connectors/handoff.py` | The raw requests handed to the proxy: `from_finding`, `from_asset`, `from_endpoint`, `from_candidate` |
| `connectors/notice.py` | `notices_for()`: the reasons a shape is flagged |
| `shared/definitions/connectors.py` | `ConnectorKind`, states, source tools, action kinds, notice kinds and limits, mirrored by `frontend/src/lib/config/connectors.ts` |
| `shared/services/proxy_sync.py` | The only writer of proxy endpoints |
| `binaries/` | Client builds, mounted read-only into the api at `/app/binaries` |

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Add a connector

The pane follows the Burp Suite connector at each step.

1. **Add the kind.** Add a member to `ConnectorKind` in `shared/definitions/connectors.py`, and the same value to the `ConnectorKind` type in `frontend/src/lib/types/connector.ts` so the interface knows it. A kind is at most 16 characters. <span class="rn-ref" data-tab="Kind">Shown in the pane</span>
2. **Create the directory.** Add `connectors/<name>/__init__.py` and `connectors/<name>/connector.py`. <span class="rn-ref" data-tab="Connector class">Shown in the pane</span>
3. **Declare the connector.** Subclass `ProxyConnector` and set `kind`, `title`, `short_title` and `client_pattern`, a glob under `binaries/`. Return the setup steps from `setup()`: they are the steps the setup dialog walks the user through. Give a step `control="download"` to show the client download, or `control="credentials"` to show the endpoint and token. <span class="rn-ref" data-tab="Connector class">Shown in the pane</span>
4. **Ship the client.** Put the client build in `binaries/` under a name that matches `client_pattern`. reNgine serves the highest release that matches at `GET /api/v1/connectors/client/{kind}`, so users download it from their own instance. <span class="rn-ref" data-tab="Connector class">Shown in the pane</span>
5. **Write the proxy client.** Send the connector token as `Authorization: Bearer`. Post captured requests to `/api/v1/connectors/ingest` in batches of at most 500. Poll `/api/v1/connectors/actions` for the requests users send from reNgine, and `/api/v1/connectors/notices` for the reasons reNgine flagged a request for review. Every reply is a flat object or a flat array of flat objects. <span class="rn-ref" data-tab="Proxy calls">Shown in the pane</span>
6. **Restart and check the catalog.** Restart the api so it loads your connector. Print the registry, then read `GET /api/v1/connectors/catalog` to see the entry the interface shows. <span class="rn-ref" data-tab="Check">Shown in the pane</span>
7. **Test it.** Check your setup steps, and check that your client's items fold into the shapes you expect. <span class="rn-ref" data-tab="Test">Shown in the pane</span>

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Connector</b><span>connectors/burp/</span></div>

/// tab | Kind
<div class="rn-pane-label">shared/definitions/connectors.py</div>

```python
class ConnectorKind(StrEnum):
    BURP = "burp"


class SetupControl(StrEnum):
    """The control a setup step carries."""

    DOWNLOAD = "download"
    CREDENTIALS = "credentials"
```

<div class="rn-pane-label">frontend/src/lib/types/connector.ts</div>

```typescript
export type ConnectorKind = 'burp';
```
///

/// tab | Connector class
<div class="rn-pane-label">connectors/burp/connector.py</div>

```python
from connectors.base import ProxyConnector, SetupStep
from shared.definitions.connectors import ConnectorKind, SetupControl


class BurpConnector(ProxyConnector):
    kind = ConnectorKind.BURP.value
    title = "Burp Suite"
    short_title = "Burp"
    client_pattern = "rengine-connector-*.jar"

    def setup(self) -> list[SetupStep]:
        return [
            SetupStep(
                title="Download the extension",
                detail="Burp Suite Community or Professional. JRE 17 or later.",
                control=SetupControl.DOWNLOAD.value,
            ),
            SetupStep(
                title="Load it into Burp",
                detail="Extensions, Installed, Add. Extension type Java. "
                "Select the jar.",
            ),
            SetupStep(
                title="Paste the endpoint and the token",
                detail="Open the reNgine tab in Burp. Press Save and test.",
                control=SetupControl.CREDENTIALS.value,
            ),
            SetupStep(
                title="Select the target",
                detail="Select it under Working on. Press Apply scope to Burp. "
                "Tick Send captured requests to reNgine.",
            ),
        ]
```

<div class="rn-pane-label">binaries/</div>

```text
rengine-connector-0.1.0.jar
```
///

/// tab | Proxy calls
<div class="rn-pane-label">ingest</div>

```bash
# TOKEN holds the connector token shown once at creation
curl -X POST "$RENGINE/api/v1/connectors/ingest" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"client": "burp-connector/0.1.0", "items": [
        {"url": "https://www.example.com/admin/", "method": "GET",
         "status_code": 200, "authenticated": true,
         "source_tool": "proxy", "body_params": ["id"]}]}'
```

<div class="rn-pane-label">response · 200</div>

```json
{
  "accepted": 1,
  "novel": 1,
  "dropped": 0,
  "queued": 1,
  "recorded": 1,
  "flagged": [
    { "url": "https://www.example.com/admin/",
      "notices": ["admin"], "status_code": 200 }
  ]
}
```

<div class="rn-pane-label">collect actions</div>

```bash
curl "$RENGINE/api/v1/connectors/actions" -H "Authorization: Bearer $TOKEN"
```

<div class="rn-pane-label">response · 200</div>

```json
[{
  "kind": "organizer",
  "url": "https://www.example.com/api",
  "method": "POST",
  "label": "CVE-2021-44228",
  "request": "POST /api HTTP/1.1\r\nHost: www.example.com\r\n…",
  "response": "HTTP/1.1 200 OK\r\n…",
  "notes": "reNgine · Critical · CVE-2021-44228\n…",
  "color": "red"
}]
```
///

/// tab | Check
<div class="rn-pane-label">restart and print the registry</div>

```bash
docker compose restart api
docker compose exec -T api /app/.venv/bin/python -c \
  "from connectors.registry import connectors; print(sorted(connectors()))"
```

<div class="rn-pane-label">catalog</div>

```bash
# RENGINE=https://asm.example.com; jar holds the session from POST /api/v1/auth/login
curl -b jar "$RENGINE/api/v1/connectors/catalog"
```

<div class="rn-pane-label">response · 200</div>

```json
[{
  "kind": "burp",
  "title": "Burp Suite",
  "short_title": "Burp",
  "client_file": "rengine-connector-0.1.0.jar",
  "steps": [
    { "title": "Download the extension",
      "detail": "Burp Suite Community or Professional. JRE 17 or later.",
      "control": "download" },
    …
  ],
  "download_url": "/api/v1/connectors/client/burp"
}]
```
///

/// tab | Test
<div class="rn-pane-label">tests/api/test_connectors.py, shortened</div>

```python
import pytest

from connectors.ingest import prepare
from connectors.registry import connector as connector_for
from shared.models.connector import IngestItem

pytestmark = pytest.mark.api


def _item(url: str, **kw) -> IngestItem:
    return IngestItem(url=url, status_code=kw.pop("status", 200), **kw)


def test_catalog_carries_setup_steps():
    steps = connector_for("burp").spec()["steps"]
    assert steps[0]["title"] == "Download the extension"
    assert all(s["detail"] for s in steps)


def test_identifiers_fold_into_one_shape():
    batch = prepare(
        [
            _item("https://www.example.com/api/users/1234"),
            _item("https://www.example.com/api/users/9999"),
        ],
        include_static=False,
        ingest_tools=[],
    )
    assert len(batch.prepared) == 1
    assert batch.prepared[0].shape == "/api/users/{id}"
```
///

</div>
</div>

## The connector class

Use this table to decide what your connector sets. Only `kind` and `title` are required.

| Attribute | Meaning |
|---|---|
| `kind` | A `ConnectorKind` value. Required. The key of the connector in the catalog and the `kind` of a connection. |
| `title` | The product name. Required. The default name of a new connection. |
| `short_title` | The short name. Defaults to `title`. |
| `client_pattern` | A glob under `binaries/`. Empty means no client download. |
| `setup()` | The list of `SetupStep(title, detail, control)` shown in the setup dialog |
| `client_file` | Property. The file in `binaries/` matching `client_pattern` with the highest release numbers. |
| `spec()` | The catalog entry: `kind`, `title`, `short_title`, `client_file`, `steps` |

When a declaration is wrong, the registry refuses it with one of these messages:

| Registration message | Cause |
|---|---|
| ``<class> must set `kind`.`` or ``<class> must set `title`.`` | The attribute is empty |
| `<class> declares unknown kind '<kind>'.` | `kind` is not a `ConnectorKind` value |

The registry raises `ConnectorRegistrationError`. If your module fails to import, the registry skips it and logs `plugin module skipped`, so look for that line when your connector does not show up.

## The token

Your proxy client authenticates with a connector token. reNgine shows the token once, when an administrator creates the connection or rotates its token, and the user pastes it into the client together with the endpoint.

| Item | Value |
|---|---|
| Format | `rngconn_` followed by 48 hexadecimal characters |
| Stored | A SHA-256 hash and the display prefix, `rngconn_` and 8 characters |
| Shown | Once, by `POST /api/v1/connectors` and `POST /api/v1/connectors/{id}/rotate` |
| Header | `Authorization: Bearer <token>`. A bare token is also accepted. |
| Validity | While the administrator who created the connection is active and an administrator |
| Failed attempts | 20 in 15 minutes per client address, then `429` |

`connectors/auth.py` defines the format with `TokenFormat("rngconn_")` from `shared/utils/bearer.py`. The MCP token uses the same format with `rngmcp_`.

## Endpoints your client calls

These are the endpoints a proxy client can call. Every one of them authenticates with the connector token. A call from a connection that is not paused marks it as connected for 15 seconds, so polling also keeps the connection shown as connected.

| Method and path | Effect |
|---|---|
| `POST /api/v1/connectors/ingest` | Records a batch of captured requests |
| `GET /api/v1/connectors/actions` | Pending hand-offs. Each action is delivered once. |
| `GET /api/v1/connectors/notices` | Pending notices. Each notice is delivered once. |
| `GET /api/v1/connectors/targets` | The options of the proxy's target picker |
| `GET /api/v1/connectors/scope?target_id=` or `?program_id=` | The scope rules the proxy applies to its own target scope |
| `GET /api/v1/connectors/host?host=` | Stored facts about a host name |
| `POST /api/v1/connectors/findings` | Records a finding reported from the proxy |

If a call is refused, the message tells you why:

| Message | Status | Cause |
|---|---|---|
| `Unknown connector token.` | 401 | The token matches no connection |
| `The connector is paused.` | 403 | The connection is paused |
| `Too many attempts. Try again in <n> seconds.` | 429 | 20 failed tokens from one address in 15 minutes |
| `Pass exactly one of target_id or program_id.` | 400 | `/scope` named neither or both |

## Send captured requests

Your client posts what the proxy captures to `/api/v1/connectors/ingest`. Each item describes one request, and these are its fields and their limits:

| Field of an item | Limit |
|---|---|
| `url` | 2,000 characters. Required. |
| `method` | 16 characters. Default `GET`. |
| `status_code`, `content_length` | Integers |
| `content_type` | 120 characters |
| `title` | 500 characters |
| `authenticated` | Boolean |
| `source_tool` | `proxy`, `repeater` or `other`. Only `proxy` and `repeater` are recorded. |
| `body_params` | 40 names |
| `request_sample` | 4,000 characters. The request line and headers, credential values masked. Kept when the connection's `capture_bodies` is on. |
| `observed_at` | A timestamp |

A batch is `{"client", "target_id", "program_id", "items"}` with at most 500 items. Unknown fields are refused. reNgine handles each batch in six steps:

| Step | Effect |
|---|---|
| Shape | `shape_for` collapses identifier segments: `/api/users/1234` and `/api/users/9999` are `/api/users/{id}` |
| Fold | `prepare()` merges items that share a signature: scheme, host, port, path shape and parameter names |
| Scope | Each host name is resolved to a target. A host name outside every target is recorded as unassigned and attaches when a target appears. With `only_known_hosts` on, it is dropped. |
| Known | A shape is known when a scan recorded the same host name and shape. Parameters no scan saw raise `new_params`. `unseen_by_scans` is raised only when a settled census scan covers the target. |
| Record | `shared/services/proxy_sync.py` writes each shape into the target's covering scan as an endpoint with source `proxy`. A target with no census scan gets a `Browsing · <connection>` run. |
| Notice | `connectors/notice.py` derives the reasons a shape warrants review |

The answer tells your client what happened to the batch:

| Result field | Content |
|---|---|
| `accepted` | Shapes kept from the batch |
| `novel` | Shapes not seen before on this connection |
| `dropped` | Items rejected, and shapes dropped by `only_known_hosts` |
| `queued` | Shapes of the connection in state `new` |
| `recorded` | Endpoint rows written |
| `flagged` | Up to 20 shapes with a `sensitive`, `admin`, `server_error` or `out_of_scope` notice |

## Requests sent to the proxy

When a user sends a finding, web asset, endpoint or browsed shape to the proxy, `POST /api/v1/connectors/{id}/handoff` builds one raw request for each one and queues it as an action. Your client collects the actions from `/api/v1/connectors/actions` and opens them in the proxy. Each action carries these fields:

| Field | Content |
|---|---|
| `kind` | `repeater`, `intruder`, `organizer` or `sitemap` |
| `url`, `method`, `label` | The request target and its label |
| `request` | Raw HTTP with CRLF line endings, at most 64,000 characters |
| `response` | The stored response, at most 100,000 characters. A decoded body ships without `Transfer-Encoding` and `Content-Encoding`, with its own `Content-Length` and `charset=utf-8`. A binary response ships its headers alone. |
| `notes` | The finding's note, for Organizer and the site map |
| `color` | A Burp highlight name: `red` critical, `orange` high, `yellow` medium, `blue` low, `gray` info and unknown |

A poll returns at most 50 actions, oldest first. An action your client does not collect within 60 minutes is deleted. A connection holds at most 200 pending actions, and past that the sender gets `The action queue holds 200. Wait for the proxy to collect them.` Masked header values stay masked in the queue. With `restore_credentials` on, reNgine fills them in from the sending run's sealed headers when your client collects the action.

## Connection states

reNgine shows each connection in one of these states, based on when your client last called and when traffic last arrived:

| State | Condition |
|---|---|
| `paused` | The connection is paused |
| `live` | A request arrived in the last 2 minutes |
| `connected` | The client called an endpoint in the last 15 seconds |
| `stale` | Traffic arrived once, but not in the last 2 minutes, and the client is not polling |
| `idle` | No traffic has arrived |

## How the Burp client behaves

The Burp extension is a working example of a client. Use its behaviour as a model for yours.

The Burp extension holds a batch and retries it on a timeout, a `429` or a `5xx`, with a backoff from 2 to 30 seconds. A `4xx` is final. A `2xx` reply counts as delivered only when it carries `accepted`. The extension hands Burp UTF-8 bytes and follows the endpoint's scheme: HTTP/2 over TLS, negotiated down to HTTP/1.1, and HTTP/1.1 over plain HTTP.
