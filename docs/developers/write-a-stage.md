---
title: Write a stage
description: Add your own step to the scan pipeline, for example to run a new tool against every web asset or to enrich results from another source. You write one Python class in its own directory, and reNgine finds it, orders it and builds its settings form.
layout: pane
sources:
  - stages/base.py
  - stages/registry.py
  - stages/config.py
  - stages/sink.py
  - stages/presets.py
  - stages/waf_detect/stage.py
  - stages/content_discovery/stage.py
  - stages/content_discovery/config.py
  - shared/plugins.py
  - shared/definitions/intensity.py
  - shared/definitions/stage_counts.py
  - shared/services/scan_resolve.py
  - shared/services/scan_scope.py
  - shared/enums/scan.py
  - worker/app/orchestrator/stage.py
  - api/app/services/scan_engine/catalog.py
  - tests/pipeline/test_stage_knobs.py
  - tests/pipeline/test_execution_plan.py
  - tests/pipeline/test_stage_counts.py
  - tests/pipeline/test_check_severities.py
revised: 2026-10-03
---

A stage is one step of the scan pipeline. It reads what earlier stages found, runs a tool or a lookup, and writes rows into a result dimension. The pipeline holds {{ counts.stages }} stages in {{ counts.steps }} steps.

You do not register a stage anywhere. The registry imports every directory under `stages/` whose name does not start with `_` or `.`, collects each concrete `Stage` subclass, checks it, and works out its place in the plan from `depends_on`. If your module fails to import, the registry skips it and logs `plugin module skipped`, so look for that line when your stage does not show up.

These are the files you work with:

| Path | Content |
|---|---|
| `stages/<name>/stage.py` | The `Stage` subclass |
| `stages/<name>/config.py` | The `StageConfig` subclass and the stage's constants |
| `stages/base.py` | `Stage`, `StageContext`, `StageResult`, `NetOptions`, and the target type sets `ALL_TARGETS`, `IP_TARGETS`, `DOMAIN_TARGETS`, `RANGE_TARGETS` |
| `stages/config.py` | `StageConfig`, `advanced()`, `wordlist()`, `share_rate()` |
| `stages/registry.py` | Discovery, validation, `StageSpec`, `execution_plan()` |
| `stages/sink.py` | `ResultSink` |
| `stages/presets.py` | The engine presets, derived from the stage flags |

The directory name and the stage `name` can differ: `stages/subdomain/` holds `subdomain_discovery`.

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Add a stage

The pane follows two real stages: the settings of `content_discovery` and the class of `waf_detect`.

1. **Create the directory.** Add `stages/<name>/` with `config.py` and `stage.py`. You need no `__init__.py` and no registry edit. <span class="rn-ref" data-tab="Config">Shown in the pane</span>
2. **Declare the settings.** Subclass `StageConfig`, which already defines `enabled`. Give each field a `Field` with `title`, `description` and bounds: the title is the field's label and the description its help. `advanced(...)` puts a field behind the stage's **Advanced** disclosure, and `wordlist(kind, title=...)` lets the user pick a list from the library. You write no form: the model's JSON schema becomes the engine form, its `model_dump()` gives the defaults, and the API validates submitted values with it. <span class="rn-ref" data-tab="Config">Shown in the pane</span>
3. **Declare the stage.** Subclass `Stage` and set `name`, `title`, `description`, `phase`, `depends_on`, `group`, `role`, `consumes`, `produces`, `tools` and `config_model`. If your stage sends traffic with a tool, also set `transport_tool`: the transport profile that decides its rate and concurrency at each intensity. <span class="rn-ref" data-tab="Stage class">Shown in the pane</span>
4. **Write `run`.** Read your inputs from the run's rows with `self.session`, filtered on `self.ctx.scan_id`. Build the tool client from `self.net_options()`, `self.transport`, `self.ctx.recorder` and `self.ctx.resolved.tool_args(<tool>)`. Call `self._check_abort()` between units of work, so cancel and pause stop your stage, and `self.emit_progress(...)` to write a line to the activity log. Return a `StageResult`. <span class="rn-ref" data-tab="Stage class">Shown in the pane</span>
5. **Write results while the tool runs.** Open a sink with `self.results_sink(dimension, write)`, `add` each row and `close` the sink at the end. Your `write` callback commits, so users see rows while the stage is still running. <span class="rn-ref" data-tab="Write results">Shown in the pane</span>
6. **Label the counts.** Add every key of `StageResult.counts` to `STAGE_COUNT_LABELS` in `shared/definitions/stage_counts.py`, as a singular and plural pair. A count key without a label fails `tests/pipeline/test_stage_counts.py`. <span class="rn-ref" data-tab="Write results">Shown in the pane</span>
7. **Restart the workers.** The workers do not reload code on their own, so restart them to load your stage. The api reloads by itself. <span class="rn-ref" data-tab="Check">Shown in the pane</span>
8. **Check the plan and the catalog.** Print `execution_plan()` to see which step your stage landed in. Then read its entry in `GET /api/v1/engines/catalog` to see the settings the engine builder shows. <span class="rn-ref" data-tab="Check">Shown in the pane</span>
9. **Run the tests.** The registry tests already cover every stage, yours included. Add unit tests for your stage's own logic under `tests/pipeline/`. <span class="rn-ref" data-tab="Test">Shown in the pane</span>

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Stage</b><span>stages/</span></div>

/// tab | Config
<div class="rn-pane-label">stages/content_discovery/config.py</div>

```python
from pydantic import Field

from shared.definitions.wordlists import WordlistKind
from stages.config import StageConfig, advanced, wordlist


class ContentDiscoveryConfig(StageConfig):
    enabled: bool = Field(
        default=False,
        title="Guess paths and files",
        description="Request wordlist paths on every live site. "
        "One request per word per site.",
    )
    wordlist: str = wordlist(
        WordlistKind.CONTENT.value,
        title="Wordlist",
        description="List to guess from. Custom lists are uploaded in the Arsenal.",
    )
    max_minutes: int = Field(
        default=20,
        ge=1,
        le=480,
        title="Time budget (minutes)",
        description="The run stops after this many minutes "
        "and reports partial coverage.",
    )
    max_hosts: int = advanced(
        25,
        ge=1,
        le=1_000,
        title="Sites to guess against",
        description="Sites tried. Sites that answered are picked first.",
    )
```
///

/// tab | Stage class
<div class="rn-pane-label">stages/waf_detect/stage.py, shortened</div>

```python
from sqlalchemy import select, update

from shared.definitions.intensity import TransportTool
from shared.enums.scan import AssetKind, Phase, StageGroup, StageRole
from shared.models.http_asset import HttpAsset
from stages.base import Stage, StageResult
from stages.waf_detect.config import WafDetectConfig
from tools.wafw00f.client import Wafw00fClient, Wafw00fError


class WafDetectStage(Stage):
    name = "waf_detect"
    title = "WAF Detection"
    description = "Fingerprint web application firewalls in front of live web assets."
    phase = Phase.EXPANSION.value
    depends_on = frozenset({"http_probe"})
    group = StageGroup.WEB.value
    role = StageRole.SUPPORT.value
    consumes = frozenset({AssetKind.HTTP_ASSETS.value})
    tools = ("wafw00f",)
    transport_tool = TransportTool.HTTPX.value
    thread_weight = 1 / 25
    config_model = WafDetectConfig

    def run(self) -> StageResult:
        self._check_abort()
        net = self.net_options()
        live = self.session.execute(
            select(HttpAsset.id, HttpAsset.url).where(
                HttpAsset.scan_id == self.ctx.scan_id,
                HttpAsset.status_code.isnot(None),
            )
        ).all()
        if not live:
            return StageResult(counts={"waf": 0})
        try:
            client = Wafw00fClient(
                proxy_url=net.proxy_url,
                headers=net.headers,
                concurrency=self.transport.threads,
                recorder=self.ctx.recorder,
                extra_args=self.ctx.resolved.tool_args("wafw00f"),
            )
        except Wafw00fError as exc:
            return StageResult(counts={"waf": 0}, warnings=[str(exc)], partial=True)

        by_url = {url: asset_id for asset_id, url in live}
        scan = client.detect([url for _, url in live][:_MAX_URLS])
        updates = [
            {"id": by_url[url], "waf": firewall[:100]}
            for url, firewall in scan.found.items()
            if url in by_url
        ]
        if updates:
            self.session.execute(update(HttpAsset), updates)
            self.session.commit()
        self.emit_progress(f"{len(updates)} web assets behind a WAF")
        warnings = []
        if scan.unfinished:
            warnings.append(
                f"wafw00f did not finish {scan.unfinished:,} of "
                f"{scan.scanned + scan.unfinished:,} web assets."
            )
        return StageResult(
            counts={"waf": len(updates), "checked": scan.scanned},
            warnings=warnings,
            partial=bool(warnings),
        )
```
///

/// tab | Write results
<div class="rn-pane-label">stages/content_discovery/stage.py, shortened</div>

```python
sink = self.results_sink(
    SurfaceDimension.ENDPOINTS.value, self._write, rows=_SINK_ROWS
)
with ThreadPoolExecutor(max_workers=workers) as pool:
    futures = {pool.submit(self._one, args, host, ...) for host in hosts}
    remaining = futures
    while remaining:
        done, remaining = wait(remaining, timeout=_DRAIN_SECONDS)
        for future in done:
            for parsed in future.result().kept:
                sink.add(_observation(parsed, label))
        self._check_abort()
written = sink.close()


def _write(self, batch: list[EndpointObservation]) -> int:
    result = endpoint_inventory.upsert(
        self.session,
        scan_id=self.ctx.scan_id,
        target_id=self.ctx.target_id,
        project_id=self.ctx.project_id,
        source=EndpointSource.FUZZ.value,
        observations=batch,
        policy=NoisePolicy.protected(),
    )
    self.session.commit()
    return result.created + result.updated
```

<div class="rn-pane-label">shared/definitions/stage_counts.py</div>

```python
STAGE_COUNT_LABELS: dict[str, Label] = {
    "checked": ("checked", "checked"),
    "endpoints": noun(_ENDPOINTS),
    "waf": ("firewall identified", "firewalls identified"),
}

STAGE_COUNT_OVERRIDES: dict[tuple[str, str], Label] = {
    ("waf_detect", "checked"): noun(_WEB, after="checked"),
}
```
///

/// tab | Check
<div class="rn-pane-label">restart the workers</div>

```bash
docker compose restart worker-default worker-scans worker-control
```

<div class="rn-pane-label">print the steps</div>

```bash
docker compose exec -T api /app/.venv/bin/python -c \
  "from stages.registry import execution_plan; print(execution_plan())"
```

<div class="rn-pane-label">read the catalog entry</div>

```bash
# RENGINE=https://asm.example.com; jar holds the session from POST /api/v1/auth/login
curl -b jar "$RENGINE/api/v1/engines/catalog"
```

<div class="rn-pane-label">response · 200, one entry of stages[]</div>

```json
{
  "name": "waf_detect",
  "title": "WAF Detection",
  "phase": "expansion",
  "level": 5,
  "tools": ["wafw00f"],
  "touches_target": true,
  "passive_capable": false,
  "group": "web",
  "role": "support",
  "consumes": ["http_assets"],
  "produces": [],
  "transport": {
    "tool": "httpx",
    "rates": {"passive": 150, "normal": 150, "aggressive": 400},
    "threads": {"passive": 6, "normal": 6, "aggressive": 12},
    "timeout": 10
  },
  "defaults": {"enabled": true},
  "fields": [{"name": "enabled", "title": "Detect WAFs", "tier": "basic", …}]
}
```
///

/// tab | Test
<div class="rn-pane-label">tests/pipeline/, after test_check_severities.py</div>

```python
import uuid

import pytest

from shared.services.scan_resolve import ResolvedScanConfig
from stages.base import StageContext
from stages.waf_detect.stage import WafDetectStage

pytestmark = pytest.mark.pipeline


def _context(stages: dict) -> StageContext:
    return StageContext(
        scan_id=uuid.uuid4(),
        target_id=uuid.uuid4(),
        project_id=uuid.uuid4(),
        target_value="example.com",
        target_type="domain",
        resolved=ResolvedScanConfig(
            target_value="example.com", target_type="domain", stages=stages
        ),
    )


def test_a_disabled_stage_does_not_run():
    ctx = _context({"waf_detect": {"enabled": False}})
    assert not WafDetectStage(None, ctx).should_run()
```

<div class="rn-pane-label">run</div>

```bash
docker compose exec -T api /app/.venv/bin/python -m pytest tests/pipeline -q
```
///

</div>
</div>

## Class attributes

Use this table to decide what your stage sets. Only `name`, `group` and `role` are required, and every other attribute has a default. `Stage` declares each attribute as a class variable, and the registry copies them into a `StageSpec`.

| Attribute | Default | Meaning |
|---|---|---|
| `name` | required | The stage id. Unique across the registry. The key of the stage in an engine's `stages` map. |
| `title` | `name` in title case | The stage's label in the catalog and the interface |
| `description` | `""` | One sentence, shown in the catalog |
| `phase` | `expansion` | Display grouping: `discovery`, `expansion`, `depth`, `finalize`. It does not order execution. |
| `depends_on` | empty | Stage names that settle before this stage starts. The execution graph. |
| `applies_to` | `ALL_TARGETS` | Target types the stage runs for: `domain`, `ip`, `ip_range`, `asn`, `url`. The runner enforces it. |
| `group` | `""` | The launch picker row: `hosts`, `addresses`, `services`, `web`, `endpoints`, `vulnerabilities`, `analysis`. Required. |
| `role` | `""` | `capability`, a stage a user asks for, or `support`, a stage that runs when its inputs exist. Required. |
| `consumes` | empty | Asset kinds the stage reads |
| `produces` | empty | Asset kinds the stage writes. Decides the result dimension it fills and covers. |
| `tools` | `()` | Tool names listed in the catalog |
| `api_keys` | `()` | API key providers the stage reads |
| `requires_api_keys` | `False` | The stage needs one of `api_keys` to run |
| `touches_target` | `True` | Any part of the stage sends traffic to the target |
| `passive_capable` | `False` | The stage keeps its public sources at passive intensity and gates its own active providers |
| `deferrable` | `True` | `False` keeps a stage nothing waits on in its own step. `session_check` sets it. |
| `always_on` | `False` | The stage cannot be switched off. `http_probe` and `ip_enrichment` set it. |
| `catalog_hidden` | `False` | Hidden from the catalog. Reserved for `asset_seed`. |
| `launch_fields` | `()` | Config fields offered at launch |
| `transport_tool` | `None` | The tool profile in `shared/definitions/intensity.py` that sets rate, concurrency, timeout and retries |
| `rate_weight`, `thread_weight` | `1.0` | Multipliers on the profile's rate and concurrency |
| `transport_timeout` | `None` | A per-request timeout in seconds in place of the profile's |
| `config_model` | `StageConfig` | The settings model |
| `check_of` | `None` | The stage whose `severities` field filters this stage's findings |
| `finding_severities` | `()` | Severities this stage writes. Set together with `check_of`. |

The asset kinds for `consumes` and `produces` are `hosts`, `addresses`, `ports`, `http_assets`, `endpoints`, `vulnerabilities` and `secrets` (`shared/enums/scan.py:AssetKind`).

`should_run()` returns `cfg.enabled`. Override it only when your stage needs an extra condition. `self.cfg` is the config model, built from the run's resolved settings for your stage.

## Execution order

You never set a step number. You list what your stage waits for in `depends_on`, and reNgine works out the order. `depends_on` is the execution graph. The registry assigns each stage a level, the longest path to it over `depends_on`, and `execution_plan()` turns the levels into steps. A step of several stages is a Celery chord and a step of one stage is a chain: the stages of a step run in parallel, and the next step starts when every one has settled. A cycle or an unknown name in `depends_on` stops the registry from loading.

Some stages are deferred, which moves them toward the end of the run. A stage is deferred when no stage depends on it, no stage consumes what it produces, `deferrable` is `True`, and it either sends traffic to the target or sits past the last awaited level. A deferred stage runs in the last gating step or later, after the deferred stages it depends on. Every stage is dispatched for every run. A disabled stage, or one that does not apply to the target, records a `skipped` activity.

`ip_enrichment` is always on and runs in step 6. If your stage writes addresses in an earlier step, they get enriched.

## Intensity and transport

Intensity decides how hard a scan hits the target, and your stage has to follow it. So a config field is a decision for the user, never a transport setting. Rate, concurrency, timeout and retries come from the profile of `transport_tool` at the run's intensity, after the scan context's multipliers, per-tool overrides and ceiling. Your stage reads them from `self.transport`.

These are the profiles you can name in `transport_tool`:

| Profile | Normal rate, concurrency | Aggressive rate, concurrency | Timeout | Retries |
|---|---|---|---|---|
| `httpx` | 150, 150 | 400, 300 | 10 s | 0 |
| `naabu` | 1,000, 100 | 3,000, 200 | 3 s | 1 |
| `nuclei` | 150, 25 | 400, 50 | 10 s | 1 |
| `katana` | 150, 50 | 300, 100 | 15 s | 0 |
| `ffuf` | 150, 40 | 400, 80 | 8 s | 0 |
| `dnsx` | no limit, 30 | no limit, 50 | 5 s | 0 |
| `banner` | no limit, 32 | no limit, 64 | 4 s | 0 |
| `julius` | 150, 20 | 400, 40 | 5 s | 0 |

Passive intensity uses the Normal row. A weight scales the profile: `thread_weight = 1 / 25` gives `waf_detect` 6 threads at Normal. If your stage runs several tool processes, split its rate between them with `share_rate(rate, processes)`.

At passive intensity, the resolver sets `enabled` to `False` on every stage with `touches_target` and without `passive_capable`. A `passive_capable` stage reads `self.ctx.resolved.intensity` and skips its own active providers at `passive`.

The engine presets are built from the same flags, so your flags decide which presets include your stage:

| Preset | Stages enabled |
|---|---|
| Standard Recon | Every stage at its config default |
| Passive Recon | Stages with `touches_target` off, or `passive_capable` on. Passive intensity. |
| Full Sweep | Every stage |
| Blank | Always-on stages only |

The Default engine runs every stage at its config default, with `vulnerability_scan` on. An engine that does not name a stage runs it at its config default. So the `enabled` default of your new stage decides whether existing engines start running it.

## Writing results

Write results as your tool produces them, so users can follow the scan while it runs. `ResultSink` buffers rows and flushes on size, 500 rows by default, or on age, 2 seconds by default. Each flush calls `write`. After a flush, at most once every 2 seconds and always on `close()`, the sink calls `publish_results(dimension)`, which updates the run's live counters, emits `results_found` and starts the live tripwire pass for the dimension. A `web_assets` flush also starts the live exposure pass.

Follow these rules when you write:

- The `write` callback commits. A flush that only calls `session.flush()` is not visible to the interface while the stage runs.
- A previous attempt is cleared inside the first flush, never before it.
- Only the stage thread writes. A thread pool hands its rows back to the stage thread, as in `content_discovery`.
- `shared/services/ip_inventory.py` and `shared/services/port_inventory.py` are the only writers of the `ip_addresses` and `ports` tables.
- `flush_rows(batch)` writes a batch in a savepoint, retries row by row when the database refuses the batch, and returns the number of rows refused.
- A tool that is missing or fails is a warning and a `partial` result, never an empty success.
- A null count means not reported. A stage reports a count only when it measured it.

A stage that produces a dimension's asset kind can write that dimension. A `capability` stage that produces it and succeeds marks the dimension covered for the run (`shared/services/scan_scope.py`). Coverage is what lets the interface tell **Not scanned** apart from zero.

## Tool flags

Check every flag a client passes against the tool's own help in the worker image, and never assume one. These rules apply to your stage:

- A rate is a budget for the stage, not for each process it starts.
- A provider that sends its own requests sizes its pool from `transport.threads` and spaces requests at `transport.rate`.
- Engine tool args add flags and never restate one. `merge_extra_args` drops any flag the client already set.
- The header flag differs per tool. Each client holds its own `HEADER_FLAG`.

[Write a tool wrapper](write-a-tool-wrapper.md) lists the flags already measured.

## Run outcome

The runner opens a `scan_activities` row, runs your stage and records the outcome in the activity log. This table shows which status each case gives.

| Outcome | Status | Stored |
|---|---|---|
| `run()` returns with `partial=False` | `success` | `counts` |
| `run()` returns with `partial=True` | `partial` | `counts`, and the warnings as the activity note |
| `run()` raises | `failed` | The error and the traceback, with run secrets removed |
| `StageAbortedError` | `aborted` or `paused` | Set by the scan's state |
| Target type outside `applies_to` | `skipped` | `not applicable to this target type` |
| `should_run()` is `False` | `skipped` | `not applicable to this target or configuration` |

## Registration errors

When a declaration is wrong, the registry raises `StageRegistrationError` with one of these messages. The cause tells you what to fix.

| Message | Cause |
|---|---|
| ``<class> must set a `name`.`` | `name` is empty |
| `Duplicate stage name '<name>': <class>.` | Two classes share a `name` |
| `<name>: unknown phase '<phase>'.` | `phase` is not a `Phase` value |
| `<name>: group must be one of [...]` | `group` is empty or unknown |
| `<name>: role must be one of [...]` | `role` is empty or unknown |
| `<name>: unknown asset kind '<kind>'.` | A `consumes` or `produces` value is not an `AssetKind` |
| `<name>: unknown severity '<severity>'.` | A `finding_severities` value is unknown |
| `<name>: check_of and finding_severities are set together.` | One is set without the other |
| `<name>: a check must produce vulnerabilities.` | A check does not produce `vulnerabilities` |
| `<name>: no transport profile for '<tool>'.` | `transport_tool` has no profile |
| `<name>: check_of must name a stage with a severities field.` | `check_of` names a stage without `severities` |
| `<name>: depends_on names unknown stage '<dep>'.` | `depends_on` names no stage |
| `Stage dependency cycle through '<name>'.` | `depends_on` forms a cycle |

## Checks inside the vulnerability scan

If your support stage writes its own findings, make it a check of `vulnerability_scan`, so the severities the user selects for the vulnerability scan apply to it too. To do that, set `check_of = "vulnerability_scan"` and `finding_severities`. The engine builder lists it with the **Vulnerability Scan** stage. While `vulnerability_scan` runs, `Stage.selected_findings` drops the findings outside its selected severities. `takeover`, `zone_transfer`, `broken_links`, `name_ownership` and `origin_probe` are checks.

## Tests that cover every stage

These tests run against every stage, yours included. Each one catches a common mistake.

| Test | Fails when |
|---|---|
| `tests/pipeline/test_execution_plan.py` | A stage is dispatched twice, starts before a dependency, or runs in the same step as a stage it produces for |
| `tests/pipeline/test_stage_knobs.py` | A config field is read by nothing, a field is named like a transport setting (`rate`, `threads`, `timeout`, `retries`, `dns_threads`, `dns_timeout`), or a stage that sends traffic with a tool declares no `transport_tool` |
| `tests/pipeline/test_stage_counts.py` | A count key a stage reports has no label |
| `tests/pipeline/test_check_severities.py` | A support stage writes findings and is not in the `CHECKS` set |

`make test` runs the full suite. See [Tests and CI](tests-and-ci.md). The [Stages](../reference/stages/index.md) reference is generated from the same registry.
