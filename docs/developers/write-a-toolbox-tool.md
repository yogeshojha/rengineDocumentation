---
title: Write a toolbox tool
description: Add a one-off lookup, such as DNS records or WHOIS for a value, that users run from the **Toolbox** dialog without starting a scan. You write one Python module, and the same tool also answers over the HTTP API and as a chat command.
layout: pane
sources:
  - toolbox/base.py
  - toolbox/registry.py
  - toolbox/runner.py
  - toolbox/store.py
  - toolbox/guard.py
  - toolbox/pivot.py
  - toolbox/tools/__init__.py
  - toolbox/tools/dns.py
  - toolbox/tools/ip_intel.py
  - toolbox/tools/http_probe.py
  - shared/definitions/toolbox.py
  - shared/definitions/channels.py
  - api/app/api/v1/toolbox.py
  - worker/app/tasks/toolbox.py
  - channels/commands.py
  - frontend/src/lib/config/toolbox.ts
  - frontend/src/lib/components/toolbox/toolbox-menu.svelte
  - tests/toolbox/
  - tests/channels/test_commands.py
revised: 2026-10-03
---

Write a toolbox tool when users need a quick answer about one value, outside a scan. Users open the **Toolbox** dialog from the top bar or with <kbd>Ctrl</kbd> <kbd>Shift</kbd> <kbd>K</kbd> (<kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>K</kbd> on macOS). Each tool has its own form, shows its answer as result blocks, and keeps the run in the user's history. The same tool answers `POST /api/v1/toolbox/run` and a chat command in the **Lookups** group, so you write it once for all three.

These are the tools that ship with reNgine:

| Tool | Title | Group | Execution | Sends traffic | Chat command |
|---|---|---|---|---|---|
| `cve` | CVE | Intelligence | inline | No | `/cve` |
| `dns` | DNS records | Lookup | queued | No | `/dns` |
| `http` | HTTP probe | Discovery | queued | Yes | `/http` |
| `ip` | IP address | Lookup | inline | No | `/ip` |
| `org_domains` | Domains by organization | Intelligence | inline | No | `/org` |
| `subdomains` | Subdomain finder | Discovery | queued | No | `/subs` |
| `whois` | WHOIS | Lookup | inline | No | `/whois` |

You do not register a tool anywhere. `toolbox/tools/__init__.py` imports every module in the directory whose name does not start with `_`, collects each concrete `Tool` subclass and keys it by `name`. The registry checks each class once, and `registry.catalog()` turns each `Input` into form fields for the interface, so you write no form.

These are the files you work with:

| Path | Content |
|---|---|
| `toolbox/tools/<name>.py` | One tool: its `Input` model and its `Tool` subclass |
| `toolbox/base.py` | `Tool`, `ToolInput`, `ToolContext`, `ToolOutcome`, `ToolError` and the block helpers |
| `toolbox/registry.py` | Validation, `ToolSpec`, `catalog()` |
| `toolbox/runner.py` | Input validation, run completion and run deadlines |
| `toolbox/store.py` | Run records in Redis, per user |
| `toolbox/guard.py` | `require_public`, the destination check for a tool that sends traffic |
| `toolbox/pivot.py` | `target_pivot`, `target_pivot_sync`: a link to the target that matches the value |
| `shared/definitions/toolbox.py` | Groups, execution modes, run statuses, block kinds, tones and limits, mirrored by `frontend/src/lib/config/toolbox.ts` and `frontend/src/lib/types/toolbox.ts` |

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Add a tool

The pane follows the `dns` tool, a queued tool, with `ip` as an example of an inline one.

1. **Create the module.** Add `toolbox/tools/<name>.py`. A module whose name starts with `_` is not imported. <span class="rn-ref" data-tab="Tool class">Shown in the pane</span>
2. **Declare the input.** Subclass `ToolInput`. Give each field `title`, `description` and `max_length=MAX_INPUT_LENGTH`. Add a validator that normalises the value, or raises `ValueError` with the message the user reads. Unknown fields are refused. <span class="rn-ref" data-tab="Tool class">Shown in the pane</span>
3. **Declare the tool.** Set `name`, `title`, `description`, `group`, `icon`, `execution`, `order`, `value_field`, `placeholder`, `examples` and `Input`. If your tool sends traffic to the value, set `touches_target = True`. <span class="rn-ref" data-tab="Tool class">Shown in the pane</span>
4. **Write `run`.** Choose inline for a fast lookup and queued for anything slower or anything that runs a binary. An `inline` tool implements `async def run` on the api's `AsyncSession`. A `queued` tool implements `def run` on the worker's sync `Session`, and is the only kind that may call a tool binary. To report a problem, raise `ToolError`: the user sees its message word for word. <span class="rn-ref" data-tab="Tool class">Shown in the pane</span>
5. **Build the result.** Return a `ToolOutcome` with a one-line `summary`, `blocks` built with the helpers in `toolbox/base.py`, `caveats`, a `pivot` that links to the matching target, and the machine-readable `raw` payload. <span class="rn-ref" data-tab="Result">Shown in the pane</span>
6. **Map the icon.** Add the `icon` slug to `TOOL_ICONS` in `frontend/src/lib/config/toolbox.ts`. A slug that is not listed shows the wrench icon. <span class="rn-ref" data-tab="Result">Shown in the pane</span>
7. **Restart and check the registry.** The api reloads by itself. Restart `worker-default` for a queued tool, and `channels` for the chat command. Then print the registry to see your tool listed. <span class="rn-ref" data-tab="Check">Shown in the pane</span>
8. **Run it over the HTTP API.** `POST /api/v1/toolbox/run` validates the input and runs the tool. A queued run returns at once with status `queued`, and you poll it for the result. <span class="rn-ref" data-tab="HTTP API">Shown in the pane</span>
9. **Test it.** Add the chat command to `EXPECTED` in `tests/channels/test_commands.py`, and your tool's tests under `tests/toolbox/`. <span class="rn-ref" data-tab="Test">Shown in the pane</span>

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Toolbox tool</b><span>toolbox/tools/dns.py</span></div>

/// tab | Tool class
<div class="rn-pane-label">toolbox/tools/dns.py, shortened</div>

```python
from pydantic import Field, field_validator

from shared.definitions.toolbox import MAX_INPUT_LENGTH, ToolExecution, ToolGroup
from shared.utils.validation import normalize_domain, validate_domain
from toolbox.base import Tool, ToolContext, ToolError, ToolInput, ToolOutcome
from toolbox.pivot import target_pivot_sync
from tools.dnsx.service import DnsxService, DnsxServiceError


class Input(ToolInput):
    domain: str = Field(
        ...,
        min_length=1,
        max_length=MAX_INPUT_LENGTH,
        title="Domain",
        description="Domain name to resolve",
    )

    @field_validator("domain")
    @classmethod
    def _domain(cls, value: str) -> str:
        cleaned = normalize_domain(value)
        if not validate_domain(cleaned):
            msg = f"{value} is not a domain name."
            raise ValueError(msg)
        return cleaned


class DnsLookup(Tool):
    name = "dns"
    title = "DNS records"
    description = (
        "Address, mail, nameserver, text and CAA records published for a domain."
    )
    group = ToolGroup.LOOKUP.value
    icon = "list-tree"
    execution = ToolExecution.QUEUED.value
    order = 20
    value_field = "domain"
    placeholder = "example.com"
    examples = ("example.com",)
    Input = Input

    def run(self, ctx: ToolContext, args: Input) -> ToolOutcome:
        try:
            recon = DnsxService().do_recon(args.domain)
        except DnsxServiceError as exc:
            raise ToolError(str(exc)) from exc
        ...
```

<div class="rn-pane-label">toolbox/tools/ip_intel.py, an inline tool</div>

```python
class IpIntel(Tool):
    name = "ip"
    execution = ToolExecution.INLINE.value
    ...

    async def run(self, ctx: ToolContext, args: Input) -> ToolOutcome:
        row = (await ctx.session.execute(ADDRESS_LOOKUP_SQL, {"ip": args.ip})).first()
        ...
```
///

/// tab | Result
<div class="rn-pane-label">toolbox/tools/dns.py, shortened</div>

```python
rows = _rows(recon)
blocks = [
    hero(
        args.domain,
        sub=f"{len(rows)} record{'s' if len(rows) != 1 else ''}",
        identity=nameserver(recon.ns[0]) if recon.ns else None,
        metric=metric(addresses, "Addresses"),
        marks=[
            mark(
                "Mail",
                note=str(len(recon.mx)) if recon.mx else "none",
                tone=Tone.NEUTRAL.value if recon.mx else Tone.MUTED.value,
            ),
        ],
    ),
    table(
        ["Type", "Value"],
        rows,
        title="Records",
        empty="No records returned",
        total=len(rows),
    ),
]
summary = (
    f"{len(rows)} record{'s' if len(rows) != 1 else ''} · "
    f"{addresses} address{'es' if addresses != 1 else ''}"
    if rows
    else f"No records returned: {status or 'no answer'}"
)
return ToolOutcome(
    summary=summary,
    blocks=blocks,
    pivot=target_pivot_sync(ctx, args.domain),
    raw=recon.model_dump(mode="json"),
)
```

<div class="rn-pane-label">a cell that chains to another tool</div>

```python
cell(value, mono=True, lookup=lookup(value, "ip"))
```

<div class="rn-pane-label">frontend/src/lib/config/toolbox.ts</div>

```typescript
export const TOOL_ICONS: Record<string, IconComponent> = {
	'scroll-text': ScrollText,
	'list-tree': ListTree,
	network: Network,
	'git-fork': GitFork,
	globe: Globe,
	'shield-alert': ShieldAlert,
	'building-2': Building2
};
```
///

/// tab | Check
<div class="rn-pane-label">restart</div>

```bash
docker compose restart worker-default channels
```

<div class="rn-pane-label">print the registry</div>

```bash
docker compose exec -T api /app/.venv/bin/python -c \
  "from toolbox.registry import registry; print(sorted(registry()))"
```

<div class="rn-pane-label">output</div>

```text
['cve', 'dns', 'http', 'ip', 'org_domains', 'subdomains', 'whois']
```
///

/// tab | HTTP API
<div class="rn-pane-label">request</div>

```bash
# RENGINE=https://asm.example.com; jar holds the session from POST /api/v1/auth/login
curl -b jar -X POST "$RENGINE/api/v1/toolbox/run" \
  -H "Content-Type: application/json" \
  -d '{"tool": "dns", "input": {"domain": "example.com"},
       "project_id": "'"$PROJECT"'"}'
```

<div class="rn-pane-label">response · 200, queued</div>

```json
{
  "id": "5c2e…",
  "tool": "dns",
  "title": "DNS records",
  "label": "example.com",
  "input": {"domain": "example.com"},
  "status": "queued",
  "blocks": [],
  "caveats": [],
  "queued_at": "2026-10-03T09:12:04+00:00"
}
```

<div class="rn-pane-label">poll</div>

```bash
curl -b jar "$RENGINE/api/v1/toolbox/runs/$RUN"
```

<div class="rn-pane-label">chat</div>

```text
/dns example.com
```
///

/// tab | Test
<div class="rn-pane-label">tests/toolbox/</div>

```python
import pytest

from toolbox import registry
from toolbox.base import ToolError
from toolbox.runner import validate


def test_the_domain_is_normalised():
    args = validate(registry.get("dns"), {"domain": " Example.COM "})
    assert args.domain == "example.com"


def test_a_value_that_is_not_a_domain_is_refused():
    with pytest.raises(ToolError, match="is not a domain name"):
        validate(registry.get("dns"), {"domain": "not a domain"})
```

<div class="rn-pane-label">tests/channels/test_commands.py</div>

```python
EXPECTED = {
    ...
    "whois",
    "dns",
    "ip",
    "cve",
    "http",
    "subs",
    "org",
    ...
}
```
///

</div>
</div>

## Class attributes

Use this table to decide what your tool sets. `name`, `title`, `description` and `Input` are required, and `value_field` must name an `Input` field.

| Attribute | Default | Meaning |
|---|---|---|
| `name` | required | The tool id, the `tool` of a run request |
| `title` | required | The label in the dialog and the run history |
| `description` | required | One sentence, shown under the title and as the chat help |
| `Input` | required | The `ToolInput` model. Its JSON schema is the form and the chat arguments. |
| `group` | `lookup` | `lookup`, `discovery` or `intel`, shown as **Lookup**, **Discovery** and **Intelligence** |
| `icon` | `search` | A slug from `TOOL_ICONS` |
| `execution` | `inline` | `inline` runs on the api within the request. `queued` runs on the worker. |
| `touches_target` | `False` | The tool sends traffic to the value |
| `order` | `50` | Position inside the group |
| `value_field` | `""` | The `Input` field a chained value or a bare chat argument fills. Required: the registry refuses a name that is not an `Input` field. |
| `command` | `""` | The chat command. Empty means the tool `name`. |
| `placeholder` | `""` | The input placeholder |
| `examples` | `()` | Example values shown in the dialog |

A chat command matches `^[a-z][a-z0-9]{1,15}$`. If your tool's `name` holds an underscore, set `command`, as `org_domains` sets `org`.

## Execution

The execution mode decides where your tool runs and how long it may take.

| Mode | `run` | Runs on | Limit |
|---|---|---|---|
| `inline` | `async def run(self, ctx, args)` with an `AsyncSession` | The api, inside the request | 45 seconds |
| `queued` | `def run(self, ctx, args)` with a sync `Session` | Celery task `app.tasks.toolbox.run` on the `critical` queue, consumed by `worker-default` | Soft 300 seconds, hard 360 seconds |

The api image carries no tool binaries, so a tool that shells out is `queued`. A queued run that no worker accepts within 120 seconds is recorded as failed, and so is a running run with no report for 420 seconds.

If your tool sends traffic, call `require_public(value)` from `toolbox/guard.py` before it sends a request. It resolves the value and checks that every address is publicly routable, so a user cannot point the tool at private or reserved addresses. In chat, a tool with `touches_target = True` needs the `launch` capability and the account's authenticator code. Every other toolbox command needs `read`.

## Result blocks

Blocks are how your answer looks in the dialog and in a chat reply. `ToolOutcome.blocks` is a list of `Block` models, and the helpers in `toolbox/base.py` build them and drop blank values.

| Helper | Block kind | Use |
|---|---|---|
| `hero(headline, sub=, identity=, metric=, meter=, marks=, tone=)` | `hero` | The headline of the answer |
| `facts(fact(...), ..., title=, empty=)` | `facts` | Label and value rows. `fact` returns `None` for a blank value. |
| `table(columns, rows, title=, empty=, total=, action=, keys=)` | `table` | Rows of `cell(...)`. `action="add_targets"` with `keys` makes rows selectable. |
| `tags(values, title=, empty=)` | `tags` | A list of `tag(...)` |
| `code(text, lang=, title=)` | `code` | A raw record |
| `image(src, title=, sub=)` | `image` | An image |
| `note(text, tone=)` | `note` | A line of text |

`metric`, `meter` and `mark` decorate a hero. `tech`, `flag`, `glyph` and `nameserver` attach an identity. `lookup(value, tool)` makes a value open another tool, so users can follow an answer from one lookup to the next. Tones are `neutral`, `success`, `warning`, `critical`, `info` and `muted`. An empty block without empty-state text is not shown. The same blocks make up a chat reply.

## Runs and limits

Every tool runs under these limits:

| Item | Value |
|---|---|
| Runs per user | 30 a minute |
| Input size | 16 KB |
| History | The last 40 runs per user, kept 7 days in Redis |
| Run statuses | `queued`, `running`, `completed`, `failed` |

When a run is refused or fails, the user sees one of these messages:

| Message | Cause |
|---|---|
| `No tool called '<tool>'.` | 404. The `tool` is not registered. |
| `Too many toolbox runs. Try again in a minute.` | 429. More than 30 runs in a minute. |
| `The tool input is larger than 16 KB.` | 422. The input exceeds `MAX_TOOL_INPUT_BYTES`. |
| `<field>: <message>` | The input failed validation. The run is stored as `failed` with this `error`. |
| `The lookup did not answer within 45 seconds.` | An inline run reached its limit |
| `The lookup failed with an unexpected error. It is recorded in the api log.` | An inline run raised an exception other than `ToolError` |
| `The run failed with an unexpected error. It is recorded in the worker log.` | A queued run raised an exception other than `ToolError` |
| `The task queue did not accept the run.` | The broker refused a queued run |
| `No worker accepted this run.` | A queued run waited more than 120 seconds |
| `The worker stopped reporting on this run.` | A running run sent no update for 420 seconds |
| `Run expired.` | 404. `GET /api/v1/toolbox/runs/{run_id}` for a run past its retention |

## Registration errors

When a declaration is wrong, the registry raises `ToolRegistrationError` with one of these messages. A clash between chat commands raises when the chat catalog loads. The cause tells you what to fix.

| Message | Cause |
|---|---|
| ``<class> must set `<attribute>`.`` | `name`, `title`, `description` or `Input` is missing |
| `<class> declares unknown group '<group>'.` | `group` is not a `ToolGroup` value |
| `<class> declares unknown execution '<execution>'.` | `execution` is not `inline` or `queued` |
| `<class> names value_field '<field>', which its Input has no field for.` | `value_field` is empty or names no `Input` field |
| ``<class> declares execution='<mode>' but its `run` is <async or sync>; inline runs on the api, queued on the worker.`` | `run` is async for a queued tool, or sync for an inline tool |
| `/<command> is declared twice (<source>, <source>).` | The command is taken by an MCP tool or another toolbox tool |
| `/<command> is not one short word.` | The command does not match `^[a-z][a-z0-9]{1,15}$` |

## HTTP API

Use these operations to list the tools, run one and read the history from your own scripts.

| Method and path | Effect |
|---|---|
| `GET /api/v1/toolbox/catalog` | Groups and tools with their form fields |
| `POST /api/v1/toolbox/run` | Body `{"tool", "input", "project_id"}`. Returns the run. |
| `GET /api/v1/toolbox/runs` | The user's recent runs |
| `GET /api/v1/toolbox/runs/{run_id}` | One run |
| `DELETE /api/v1/toolbox/runs` | Clears the user's history |

`project_id` selects the project whose targets and records a tool reads, such as the `pivot` to a matching target and the scan history of an address. For the chat side, see [Control reNgine from Telegram](../pentesters/telegram.md).
