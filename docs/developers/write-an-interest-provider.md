---
title: Write an exposure provider
description: Teach reNgine a new reason to flag a web asset on the **Exposures** page, such as a pattern in your own estate or a check against another data source. You write one provider class that gives each web asset it flags a reason and a weight.
layout: pane
sources:
  - interest/base.py
  - interest/context.py
  - interest/registry.py
  - interest/presets.py
  - interest/providers/correlation/provider.py
  - interest/providers/rules/provider.py
  - interest/providers/ai/provider.py
  - shared/definitions/interest.py
  - shared/services/interest.py
  - shared/models/interest.py
  - worker/app/tasks/interest.py
  - worker/app/orchestrator/finalize.py
  - stages/base.py
  - api/app/api/v1/interest.py
  - api/app/services/interest.py
  - frontend/src/lib/config/interest.ts
  - frontend/src/lib/types/interest.ts
  - tests/pipeline/test_exploited_software.py
revised: 2026-10-03
---

An exposure provider looks at the web assets of a run and says which ones deserve a closer look, and why. Write one when you want reNgine to flag web assets for a reason the shipped providers do not cover. In the code, exposures are called interest: the package is `interest/`, and a provider is an `InterestProvider` subclass in its own directory under `interest/providers/`.

A provider yields one signal for each web asset and reason it finds. Each signal gives the web asset a reason and a weight. The weights of a web asset's signals add up to its exposure score, from 0 to 100, and the score sets its band on the **Exposures** tab of a run and on the **Exposures** page. The `interest` package is mounted into the api and the worker, and evaluation runs on the worker.

Three providers ship with reNgine. Read them before you write your own, since yours runs alongside them:

| Provider | Order | Sources | Signals |
|---|---|---|---|
| `rules` | 10 | `keyword`, `rule` | One per web asset matched by an enabled saved rule or keyword list, at most 500 per rule |
| `correlation` | 20 | `correlation` | Network outlier, rare technology, outside the edge, distinct application, known exploited software, and new as a booster |
| `ai` | 30 | `ai` | A model's judgement of each answered web asset. Runs only when AI is configured and the feature is allowed. |

You do not register a provider anywhere. The registry imports `interest.providers.<dir>` and `interest.providers.<dir>.provider` for every directory under `interest/providers/` whose name does not start with `_` or `.`, creates each concrete `InterestProvider` subclass that has a `name`, and sorts them by `order`, then `name`.

These are the files you work with:

| Path | Content |
|---|---|
| `interest/providers/<name>/provider.py` | The `InterestProvider` subclass |
| `interest/providers/<name>/__init__.py` | The package marker |
| `interest/base.py` | `InterestProvider`, `RawSignal` |
| `interest/context.py` | `InterestContext`, `HostRow` |
| `interest/registry.py` | Discovery: `providers()` |
| `interest/presets.py` | The saved rules shipped with a fresh install, read by the `rules` provider |
| `shared/definitions/interest.py` | Sources, kinds and their weights, bands and limits, mirrored by `frontend/src/lib/config/interest.ts` and `frontend/src/lib/types/interest.ts` |
| `shared/services/interest.py` | `evaluate()`: runs the providers, prunes the signals, writes `interest_signals` and rolls up the score |
| `worker/app/tasks/interest.py` | The tasks `evaluate_scan`, `evaluate_live` and `refresh_project` |

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Add a provider

The pane follows the `correlation` provider at each step.

1. **Create the directory.** Add `interest/providers/<name>/__init__.py` and `interest/providers/<name>/provider.py`. <span class="rn-ref" data-tab="Provider class">Shown in the pane</span>
2. **Declare the source.** The source tells users which provider flagged a web asset. Add a member to `InterestSource` with its `SOURCE_LABELS` and `SOURCE_HELP` entries in `shared/definitions/interest.py`, and the same value to `INTEREST_SOURCE` in `frontend/src/lib/types/interest.ts`. A source is at most 16 characters. <span class="rn-ref" data-tab="Source and kind">Shown in the pane</span>
3. **Declare the kinds.** The kind names the reason, such as **Outside the edge**, and carries its weight. Reuse an `InterestKind` when one fits. Otherwise add a member with a `KindSpec` of label, help, weight and tone, then add it to the `InterestKind` enum and `KIND_ICONS` in `frontend/src/lib/config/interest.ts`. <span class="rn-ref" data-tab="Source and kind">Shown in the pane</span>
4. **Declare the provider.** Subclass `InterestProvider` and set `name`, `source`, `title` and `order`. Set `emits` if your provider writes more than one source, and `requires_ai` if it calls a model. <span class="rn-ref" data-tab="Provider class">Shown in the pane</span>
5. **Write `evaluate`.** Read the run's web assets with `ctx.session`, filtered on `ctx.scan.id` and on `is_excluded` false. Yield one `RawSignal` per web asset and reason, weighted with `kind_weight(kind)`. If your provider needs something to run, such as a configured service, override `available(ctx)` to check it. <span class="rn-ref" data-tab="Provider class">Shown in the pane</span>
6. **Restart and check the registry.** The api reloads by itself, but the worker that runs evaluations does not, so restart `worker-default`. Then print the registry to see your provider in the list. <span class="rn-ref" data-tab="Check">Shown in the pane</span>
7. **Judge a run again.** You do not need a new scan to try your provider. `POST /api/v1/interest/scan/{scan_id}/judge` queues an evaluation of an existing run with every provider. Read the result with `POST /api/v1/interest/scan/{scan_id}`, filtered on your new source. <span class="rn-ref" data-tab="HTTP API">Shown in the pane</span>
8. **Test it.** Seed a run, build an `InterestContext` and check the signals your provider yields. <span class="rn-ref" data-tab="Test">Shown in the pane</span>

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Interest provider</b><span>interest/providers/correlation/</span></div>

/// tab | Provider class
<div class="rn-pane-label">interest/providers/correlation/provider.py, shortened</div>

```python
from collections.abc import Iterable

from sqlalchemy import bindparam, text

from interest.base import InterestProvider, RawSignal
from interest.context import InterestContext
from shared.definitions.interest import (
    EDGE_MAJORITY,
    MAX_EVIDENCE,
    MIN_ESTATE_FOR_RARITY,
    InterestKind,
    InterestSource,
    kind_weight,
)

CAP = 300


class CorrelationProvider(InterestProvider):
    name = "correlation"
    source = InterestSource.CORRELATION.value
    title = "Correlation"
    order = 20

    def evaluate(self, ctx: InterestContext) -> Iterable[RawSignal]:
        yield from self._guard(self._network, ctx)
        yield from self._guard(self._edge, ctx)
        ...

    def _guard(self, fn, ctx: InterestContext) -> list[RawSignal]:
        try:
            return list(fn(ctx))
        except Exception:
            ctx.session.rollback()
            logger.warning("correlation signal failed", exc_info=True)
            return []

    def _rows(self, ctx: InterestContext, sql: str, **params):
        stmt = text(sql).bindparams(bindparam("sid", ctx.scan.id), **params)
        return ctx.session.execute(stmt).all()

    def _signal(self, row, kind: str, reason: str, evidence: str) -> RawSignal:
        return RawSignal(
            subdomain_id=row.id,
            host=row.name,
            source=InterestSource.CORRELATION.value,
            key=kind,
            kind=kind,
            weight=kind_weight(kind),
            label=self.title,
            reason=reason,
            evidence=evidence[:MAX_EVIDENCE],
        )

    def _edge(self, ctx: InterestContext) -> Iterable[RawSignal]:
        rows = self._rows(
            ctx, _EDGE_SQL, min_estate=MIN_ESTATE_FOR_RARITY,
            majority=EDGE_MAJORITY, cap=CAP,
        )
        for row in rows:
            share = round(100 * row.behind / row.estate) if row.estate else 0
            reason = (
                f"Answers directly. {share}% of the {row.estate} responding "
                "web assets are behind a CDN."
            )
            yield self._signal(
                row, InterestKind.UNPROTECTED_EDGE.value, reason, "not is:cdn"
            )
```

<div class="rn-pane-label">interest/providers/ai/provider.py, a precondition</div>

```python
class AIProvider(InterestProvider):
    name = "ai"
    source = InterestSource.AI.value
    title = "AI"
    requires_ai = True
    order = 30

    def available(self, ctx: InterestContext) -> bool:
        return ctx.ai is not None and ctx.ai.allows(FEATURE)
```
///

/// tab | Source and kind
<div class="rn-pane-label">shared/definitions/interest.py</div>

```python
class InterestSource(StrEnum):
    KEYWORD = "keyword"
    RULE = "rule"
    CORRELATION = "correlation"
    AI = "ai"


SOURCE_LABELS: dict[str, str] = {
    ...
    InterestSource.CORRELATION.value: "Correlation",
}

SOURCE_HELP: dict[str, str] = {
    ...
    InterestSource.CORRELATION.value: "Stands out from the rest of this estate.",
}

KINDS: tuple[KindSpec, ...] = (
    ...
    KindSpec(
        InterestKind.UNPROTECTED_EDGE.value,
        "Outside the edge",
        "Answers directly while the rest of this estate sits behind a CDN.",
        20,
        TONE_INFO,
    ),
)
```

<div class="rn-pane-label">frontend/src/lib/types/interest.ts</div>

```typescript
export const INTEREST_SOURCE = {
	KEYWORD: 'keyword',
	RULE: 'rule',
	CORRELATION: 'correlation',
	AI: 'ai'
} as const;
```
///

/// tab | Check
<div class="rn-pane-label">restart and print the registry</div>

```bash
docker compose restart worker-default
docker compose exec -T api /app/.venv/bin/python -c \
  "from interest.registry import providers; print([(p.name, p.sources()) for p in providers()])"
```

<div class="rn-pane-label">output</div>

```text
[('rules', ('keyword', 'rule')), ('correlation', ('correlation',)), ('ai', ('ai',))]
```
///

/// tab | HTTP API
<div class="rn-pane-label">judge a run again</div>

```bash
# RENGINE=https://asm.example.com; jar holds the session from POST /api/v1/auth/login
curl -b jar -X POST "$RENGINE/api/v1/interest/scan/$SCAN/judge"
```

<div class="rn-pane-label">response · 202</div>

```json
{ "status": "queued" }
```

<div class="rn-pane-label">read the exposures of one source</div>

```bash
curl -b jar -X POST "$RENGINE/api/v1/interest/scan/$SCAN" \
  -H "Content-Type: application/json" \
  -d '{"sources": ["correlation"], "limit": 20}'
```

<div class="rn-pane-label">response · 200, one row</div>

```json
{
  "host": "legacy.example.com",
  "score": 20,
  "band": "notable",
  "kinds": ["unprotected_edge"],
  "sources": ["correlation"],
  "signals": [{
    "source": "correlation",
    "kind": "unprotected_edge",
    "kind_label": "Outside the edge",
    "label": "Correlation",
    "reason": "Answers directly. 92% of the 48 responding web assets are behind a CDN.",
    "evidence": "not is:cdn",
    "weight": 20,
    "judgement": false
  }],
  …
}
```
///

/// tab | Test
<div class="rn-pane-label">tests/pipeline/test_exploited_software.py, shortened</div>

```python
import pytest

from interest.context import InterestContext
from interest.providers.correlation.provider import CorrelationProvider
from shared.definitions.interest import InterestKind
from shared.models.scan import Scan

pytestmark = pytest.mark.pipeline


async def _signals(estate, scan: str) -> list:
    def run(session):
        row = session.get(Scan, estate.scans[scan])
        ctx = InterestContext(session=session, scan=row)
        return list(CorrelationProvider()._exploited(ctx))

    return await estate.session.run_sync(run)


async def test_a_catalogued_product_is_flagged(estate, now):
    await _seed(estate, now, [TOMCAT])
    await _kev(estate, "CVE-2016-8735", "Apache", "Tomcat", ransomware=True)

    signals = await _signals(estate, "run")

    assert len(signals) == 1
    assert signals[0].kind == InterestKind.EXPLOITED_SOFTWARE.value
    assert "Version not identified" in signals[0].reason
```
///

</div>
</div>

## Provider attributes

Use this table to decide what your provider sets. Only `evaluate` is required, but a provider without a `name` is ignored.

| Attribute | Default | Meaning |
|---|---|---|
| `name` | `""` | The provider id. A class with an empty `name` is ignored. |
| `source` | `""` | The `InterestSource` the provider writes |
| `emits` | `()` | Every source the provider writes, when there is more than one. `sources()` returns `emits`, or `(source,)`. |
| `title` | `""` | The label written on its signals |
| `requires_ai` | `False` | The provider calls a model. Skipped when an evaluation runs without AI. |
| `order` | `50` | Run order, ascending |
| `available(ctx)` | `True` | `False` skips the provider for this evaluation |
| `evaluate(ctx)` | required | Yields `RawSignal` objects |

## RawSignal

Each signal your provider yields carries these fields. Users read the reason and the evidence when they open a flagged web asset on the **Exposures** tab of a run.

| Field | Content |
|---|---|
| `subdomain_id` | The web asset row |
| `host` | Its name |
| `source` | An `InterestSource` value |
| `key` | The reason's identity within the source. A web asset carries one signal per `(source, key)`. |
| `kind` | An `InterestKind` value |
| `weight` | Points added to the score. `kind_weight(kind)` gives the kind's weight. |
| `label` | A short label, stored up to 80 characters |
| `reason` | One sentence |
| `evidence` | The fact behind the reason, up to `MAX_EVIDENCE`, 300 characters |
| `rule_id` | The saved rule, for the `rules` provider |
| `model`, `prompt_version` | The model, for the `ai` provider |
| `booster` | The signal adds weight but never flags a web asset on its own |

## The context

`evaluate(ctx)` receives an `InterestContext`. It holds everything your provider can read:

| Member | Content |
|---|---|
| `ctx.session` | A sync `Session` on the worker |
| `ctx.scan` | The run being judged |
| `ctx.rules` | The enabled saved rules of the instance and the project |
| `ctx.ai` | The AI configuration, or `None` |
| `ctx.now` | The evaluation time |
| `ctx.answered_hosts` | The run's web assets with an HTTP status, excluded ones left out, as `HostRow(id, name, http_status, page_title, tech)` |
| `ctx.judgeable()` | `answered_hosts` with at most 3 per response shape and at most 1,500 in all |

## When providers run

reNgine evaluates a run at several moments. This table shows when, and which providers take part, so you know when your signals appear and when they are refreshed.

| Task | When | Providers |
|---|---|---|
| `evaluate_live` | During a run, after web assets are written, at most once every 90 seconds | `keyword` and `rule` sources only |
| `evaluate_scan` | When a run finishes, followed by the digest notification, and on `POST /api/v1/interest/scan/{scan_id}/judge` | Every provider, with AI |
| `evaluate_scan` without AI | When a read of a finished run's exposures finds the saved rules changed since its last evaluation | Every provider except those with `requires_ai` |
| `refresh_project` | After a saved rule is created, changed or deleted, for the 25 most recent completed runs of the project whose rules changed | Every provider except those with `requires_ai` |

`evaluate()` runs the providers in order. A provider whose `available(ctx)` is `False` is skipped. A provider that raises is logged as `interest provider failed` and skipped, and its earlier signals are kept, so one failing provider does not wipe its last good result. For every provider that ran, the run's earlier signals of its sources are deleted and the new ones written.

Before the write, reNgine prunes the signals:

- A signal on a web asset and kind the user dismissed for the target is dropped, and so is every signal on a dismissed web asset.
- A web asset with booster signals only is not flagged.
- Per web asset, signals are kept by descending weight, one per `(source, key)`, at most 8.
- A weight is clamped to 0 to 100.

The score of a web asset is the sum of its signal weights, capped at 100. The score decides the band:

| Band | Score |
|---|---|
| Critical | 55 and above |
| High | 30 to 54 |
| Notable | 1 to 29 |

## Kinds and weights

Check these weights when you pick a kind for your signals. A kind of weight 30 alone puts a web asset in the High band, while lighter kinds need company to get there.

| Kind | Label | Weight |
|---|---|---|
| `admin_interface` | Administrative interface | 30 |
| `exposed_content` | Exposed content | 30 |
| `takeover_risk` | Takeover risk | 30 |
| `developer_tooling` | Developer tooling | 28 |
| `remote_access` | Remote access | 28 |
| `exploited_software` | Known exploited software | 28 |
| `no_authentication` | No authentication | 26 |
| `diagnostic` | Diagnostic output | 26 |
| `sensitive_service` | Sensitive service | 26 |
| `ai_service` | AI service | 26 |
| `business_system` | Business system | 24 |
| `legacy` | Legacy | 22 |
| `non_production` | Non-production | 20 |
| `unprotected_edge` | Outside the edge | 20 |
| `internal_naming` | Internal naming | 18 |
| `network_outlier` | Network outlier | 18 |
| `rare_technology` | Rare technology | 16 |
| `certificate_anomaly` | Certificate anomaly | 14 |
| `rare_identity` | Distinct application | 14 |
| `other` | Other reason | 12 |
| `newly_appeared` | New | 10 |

`GET /api/v1/interest/catalog` returns the kinds, the sources, the bands and the score cap.

## Registration error

If two classes share the same `name`, the registry raises `ProviderRegistrationError` with `Two providers claim the name '<name>'.` If your module fails to import, the registry skips it and logs `plugin module skipped`, so look for that line when your provider does not show up.

To see exposures from the user's side, read [Exposures](../pentesters/exposures.md).
