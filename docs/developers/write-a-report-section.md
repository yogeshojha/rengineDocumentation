---
title: Write a report section
description: Add your own block to reNgine reports, such as a table of results your team asks for or a page of your own text. You write one Python class and one HTML template, and the section appears in the report builder with its own settings.
layout: pane
sources:
  - reports/base.py
  - reports/config.py
  - reports/registry.py
  - reports/sections/ip_addresses/section.py
  - reports/sections/ip_addresses/section.html
  - reports/sections/custom_text/section.py
  - reports/render/document.py
  - reports/render/env.py
  - reports/render/text.py
  - reports/templates/section.html
  - reports/pipeline.py
  - reports/presets.py
  - reports/narrate/base.py
  - reports/themes/
  - shared/definitions/reports.py
  - api/app/services/report.py
  - worker/app/tasks/reports.py
  - tests/api/test_report_config.py
revised: 2026-10-03
---

Write a report section when the 30 sections that ship do not show something your readers need. A report is a list of section entries rendered in order, and a report template is a saved list of sections. The `reports` package also ships seven report templates and six themes, and it is mounted into the api and the worker. The api serves the catalog and checks report specs. The worker renders the report in the Celery task `app.tasks.reports.generate`.

You do not register a section anywhere. The registry imports `reports.sections.<dir>` and `reports.sections.<dir>.section` for every directory under `reports/sections/` whose name does not start with `_` or `.`, and collects each concrete `Section` subclass.

These are the files you work with:

| Path | Content |
|---|---|
| `reports/sections/<name>/section.py` | The `Section` subclass and its config model |
| `reports/sections/<name>/section.html` | The Jinja template of the section body |
| `reports/base.py` | `Section`, `RenderContext` |
| `reports/config.py` | `SectionConfig` and the field helpers |
| `reports/registry.py` | Discovery, validation, `SectionSpec`, `catalog()` |
| `reports/render/document.py` | Runs the sections, numbers them and builds the contents |
| `reports/render/env.py` | The Jinja environment, its filters and its chart globals |
| `reports/templates/` | `document.html`, the `section.html` wrapper, `macros.html`, `base.css` |
| `reports/data/source.py` | `ReportSource`, the rows a section reads |
| `reports/analysis/` | `build_brief()`, the `ReportBrief` every section shares |
| `reports/narrate/` | `Narrator`, with a deterministic and an AI implementation |
| `reports/themes/*.yaml` | The themes: `blueprint`, `consulting`, `editorial`, `midnight`, `noir`, `terminal` |
| `reports/presets.py` | The report templates seeded in each project |

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Add a section

The pane follows the **Addresses** section, `ip_addresses`, at each step.

1. **Create the directory.** Add `reports/sections/<name>/` with `section.py` and `section.html`. <span class="rn-ref" data-tab="Section class">Shown in the pane</span>
2. **Declare the settings.** Subclass `SectionConfig` and build each field with a helper from `reports/config.py`: `text`, `paragraph`, `flag`, `limit`, `choice`, `multi` or `columns`. You write no form: the model's JSON schema becomes the form in the report builder, and the API checks submitted values with it. <span class="rn-ref" data-tab="Section class">Shown in the pane</span>
3. **Declare the section.** Subclass `Section` and set `name`, `title`, `description`, `group`, `order` and `config_model`. Set `requires` to the result dimensions your section reads, so it is offered only when one of them was scanned. <span class="rn-ref" data-tab="Section class">Shown in the pane</span>
4. **Write `build`.** Read rows from `ctx.data`, facts from `ctx.brief` and prose from `ctx.narrator`. Return the variables your template needs, or `None` to leave the section out of this report, for example when there is nothing to show. <span class="rn-ref" data-tab="Section class">Shown in the pane</span>
5. **Write the template.** `section.html` renders the body only. The wrapper adds the heading, the number and the anchor. Your template can use `ctx`, `cfg` and the variables `build` returned. <span class="rn-ref" data-tab="Template">Shown in the pane</span>
6. **Add it to a report template.** To include your section in a template that ships, name it in a preset's `sections` in `reports/presets.py`, with its config. A section left out of every preset is still available: users add it with **Add section** in the builder. <span class="rn-ref" data-tab="Preset">Shown in the pane</span>
7. **Restart and check the catalog.** The api reloads by itself, but the worker that renders reports does not, so restart `worker-default`. Then read your section's entry in `GET /api/v1/reports/catalog`. <span class="rn-ref" data-tab="Check">Shown in the pane</span>
8. **Test it.** `tests/api/test_report_config.py` already builds every section's default config, yours included. Add tests for your section's own bounds and options. <span class="rn-ref" data-tab="Test">Shown in the pane</span>

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Report section</b><span>reports/sections/ip_addresses/</span></div>

/// tab | Section class
<div class="rn-pane-label">reports/sections/ip_addresses/section.py</div>

```python
from reports.base import RenderContext, Section
from reports.config import SectionConfig, flag, limit
from shared.definitions.reports import SectionGroup
from shared.definitions.surface import SurfaceDimension


class IpAddressesConfig(SectionConfig):
    max_rows: int = limit(60, title="Rows shown", minimum=5, maximum=2000)
    show_ptr: bool = flag(False, title="Show reverse DNS")
    show_hosts: bool = flag(True, title="Show hostnames")
    only_open: bool = flag(False, title="Only addresses with an open port")


class IpAddressesSection(Section):
    name = "ip_addresses"
    title = "Addresses"
    description = "Addresses with network, country and open ports."
    group = SectionGroup.SURFACE.value
    order = 40
    requires = frozenset({SurfaceDimension.IPS.value})
    config_model = IpAddressesConfig

    def build(self, ctx: RenderContext, cfg: IpAddressesConfig) -> dict | None:
        rows = ctx.data.address_rows
        if cfg.only_open:
            rows = [a for a in rows if a.open_ports]
        if not rows:
            return None
        rows = sorted(rows, key=lambda a: (-a.open_ports, a.ip))
        total = len(rows)
        return {
            "rows": rows[: cfg.max_rows],
            "total": total,
            "hidden": max(0, total - cfg.max_rows),
            "show_ptr": cfg.show_ptr,
            "show_hosts": cfg.show_hosts,
            "networks": len({a.asn for a in rows if a.asn}),
            "countries": len({a.country for a in rows if a.country}),
        }
```

<div class="rn-pane-label">reports/sections/custom_text/section.py, a heading from the config</div>

```python
return {
    "title": cfg.heading,
    "body": cfg.body,
    "callout": cfg.style != "plain",
    "kind": kind,
}
```
///

/// tab | Template
<div class="rn-pane-label">reports/sections/ip_addresses/section.html, shortened</div>

```html
<p class="block muted small">{{ total|num }} addresses across {{ networks|num }}
  networks and {{ countries|num }} countries.</p>
<table class="table table--fixed">
  <thead>
    <tr>
      <th style="width:32mm">Address</th><th class="num" style="width:14mm">Ports</th>
      <th style="width:44mm">Network</th><th style="width:14mm">Country</th>
      {% if show_hosts %}<th>Hostnames</th>{% endif %}
    </tr>
  </thead>
  <tbody>
    {% for row in rows %}
    <tr>
      <td class="micro mono-break">{{ row.ip }}</td>
      <td class="num micro">{{ row.open_ports|num }}</td>
      <td class="micro muted wrap">{% if row.asn %}AS{{ row.asn }} {% endif %}{{ row.asn_org|clip(38) }}</td>
      <td class="micro">{{ row.country or '—' }}</td>
      {% if show_hosts %}<td class="micro mono-break wrap">{{ row.hosts[:2]|join(', ')|clip(46) }}</td>{% endif %}
    </tr>
    {% endfor %}
  </tbody>
</table>
{% if hidden %}<p class="micro faint">{{ hidden|num }} further addresses are not listed.</p>{% endif %}
```

<div class="rn-pane-label">reports/templates/section.html, the wrapper</div>

```html
<section class="section {{ 'section--flow' if flow else '' }} section--{{ heading_style }}" id="{{ anchor }}">
  <div class="section__head">
    {% if kicker %}<span class="kicker">{{ kicker }}</span>{% endif %}
    <h1 class="section__title" ...>{{ title }}</h1>
  </div>
  {{ body|safe }}
</section>
```
///

/// tab | Preset
<div class="rn-pane-label">reports/presets.py, shortened</div>

```python
Preset(
    slug="vapt",
    name="Penetration test report",
    description="Scope, methodology, findings with evidence, remediation and appendices.",
    scope=ReportScope.SCAN.value,
    theme="consulting",
    sections=(
        ("cover", {}),
        ("document_control", {}),
        ("contents", {}),
        ("executive_summary", {}),
        ("risk_summary", {}),
        ("attack_paths", {}),
        ("findings_detail", {"max_issues": 100, "show_evidence": True}),
        ("remediation_plan", {}),
        ("methodology", {}),
        ("coverage", {}),
        ("severity_definitions", {}),
        ("signoff", {}),
    ),
),
```
///

/// tab | Check
<div class="rn-pane-label">restart and print the registry</div>

```bash
docker compose restart worker-default
docker compose exec -T api /app/.venv/bin/python -c \
  "from reports.registry import sections; print(list(sections()))"
```

<div class="rn-pane-label">catalog</div>

```bash
# RENGINE=https://asm.example.com; jar holds the session from POST /api/v1/auth/login
curl -b jar "$RENGINE/api/v1/reports/catalog"
```

<div class="rn-pane-label">response · 200, one entry of sections[]</div>

```json
{
  "name": "ip_addresses",
  "title": "Addresses",
  "description": "Addresses with network, country and open ports.",
  "group": "surface",
  "role": "content",
  "requires": ["ips"],
  "repeatable": false,
  "default_enabled": true,
  "always_available": false,
  "fields": [
    { "name": "max_rows", "label": "Rows shown", "type": "number",
      "default": 60, "minimum": 5.0, "maximum": 2000.0, "launch": false },
    { "name": "show_ptr", "label": "Show reverse DNS", "type": "flag",
      "default": false, "launch": false },
    …
  ],
  "defaults": { "max_rows": 60, "show_ptr": false, "show_hosts": true,
                "only_open": false }
}
```
///

/// tab | Test
<div class="rn-pane-label">tests/api/test_report_config.py, extended</div>

```python
import pytest
from pydantic import ValidationError

from reports.registry import section, sections


def test_every_section_default_is_one_of_its_options():
    for spec in sections().values():
        spec.config({})


def test_rows_below_the_minimum_are_refused():
    spec = section("ip_addresses")
    assert spec is not None
    with pytest.raises(ValidationError):
        spec.config({"max_rows": 1})
```
///

</div>
</div>

## Class attributes

Use this table to decide what your section sets. Only `name` and `title` are required.

| Attribute | Default | Meaning |
|---|---|---|
| `name` | required | The section id, the `section` of a section entry. Unique. |
| `title` | required | The heading and the label in the builder |
| `description` | `""` | One sentence, shown in the builder |
| `group` | `summary` | `front_matter`, `summary`, `findings`, `surface`, `intelligence` or `appendix`, shown as **Front matter**, **Summary**, **Findings**, **Attack surface**, **Intelligence** and **Appendices** |
| `role` | `content` | `content`, or `furniture` for document structure such as the cover, the contents and the sign-off. A template row in the interface lists its content sections only. |
| `order` | `100` | Position inside the group |
| `requires` | empty | Result dimensions. The section is available when at least one of them was scanned. Empty means always available. |
| `launch_fields` | empty | Config fields offered in the **Generate report** dialog |
| `repeatable` | `False` | The section may appear more than once in a report |
| `default_enabled` | `True` | The section is on when added |
| `in_toc` | `True` | The section is numbered and listed in the contents |
| `page_break` | `auto` | `auto` starts the section on the theme's chapter break. `flow` continues on the same page. |
| `template` | `""` | A template path in place of `<name>/section.html` |
| `config_model` | `SectionConfig` | The settings model |

The registry sorts sections by group order, then `order`, then `title`. When a declaration is wrong, it raises `SectionRegistrationError` with ``<class> must set a `name`.``, `Duplicate section name '<name>': <class>.` or `<name>: unknown group '<group>'.`

## Config helpers

Each helper builds one field and decides the control the report builder shows for it:

| Helper | Field | Builder control |
|---|---|---|
| `text(default, title=, description=, max_length=500)` | `str` | A text input |
| `paragraph(default, title=, description=, max_length=20000)` | `str` | A Markdown editor |
| `flag(default, title=, description=)` | `bool` | A switch |
| `limit(default, title=, description=, minimum=0, maximum=5000)` | `int` | A number input with bounds |
| `choice(default, title=, options={value: label})` | `str` | One option. A value outside the options is refused. |
| `multi(default, title=, options={value: label})` | `list[str]` | Several options. A value outside the options is refused. |
| `columns(default, title=, options={value: label})` | `list[str]` | A column picker |

When a value is outside the options, the refusal reads `<title> must be one of <values>.`

## The render context

`build(ctx, cfg)` receives the `RenderContext` and the checked config. The context holds everything your section can read:

| Member | Content |
|---|---|
| `ctx.spec` | The `ReportSpec`: title, scope, sections, style, branding, narrative options |
| `ctx.data` | `ReportSource`: findings, web asset, address, service and endpoint rows, coverage, certificates, hygiene and domain posture rollups, facets and trends |
| `ctx.brief` | `ReportBrief`: posture score and grade, ranked risks, attack paths, remediation actions, change lines and caveats, computed once per report |
| `ctx.narrator` | `executive_summary`, `risk_narrative`, `remediation_plan`, `surface_narrative`, `attack_path`, `issue_explainer` |
| `ctx.theme` | The resolved theme tokens |
| `ctx.now` | The render time |
| `ctx.style`, `ctx.branding` | Shortcuts to the spec's style and branding |
| `ctx.palette`, `ctx.sev(severity)`, `ctx.hue(index)` | Resolved colours for inline SVG |

The narrator writes prose from the brief. With AI turned on, the AI narrator writes from the same brief and falls back to the deterministic narrator on any failure, so your section gets prose either way.

## Rendering

`render_html` goes through the section entries of the spec in order. This table shows what happens to your section in each case:

| Case | Result |
|---|---|
| The entry is disabled | Left out |
| No section has that name | Warning `Unknown section '<name>'.` |
| None of `requires` was scanned | Skipped and named in `skipped` |
| `build` returns `None` | Skipped and named in `skipped` |
| `build` raises | Warning `<title> not rendered: <error>` |
| `build` returns a dict | The body template is rendered and wrapped |

The renderer reads three keys of the returned dict and removes them before the template renders: `title` replaces the section title unless the entry carries its own, `toc_subs` lists `(title, anchor)` pairs added to the contents, and `bare` set to `True` emits the body without the wrapper. The anchor of a section is `s<index>-<name>`.

PDF and HTML are rendered from the sections. Markdown and JSON are written from the brief, so a new section does not appear in them.

## Template environment

Your template can use these filters to format values the way the other sections do:

| Filter | Output |
|---|---|
| `num` | A number with thousands separators, or `—` for `None` |
| `date`, `at` | `03 October 2026`, or `03 Oct 2026, 09:12 UTC` |
| `clip(n)` | Text cut at `n` characters |
| `sev`, `svc` | Severity and service class labels |
| `plural(word)` | The word with `s` unless the count is 1 |
| `md` | Markdown rendered to HTML, images that are not data URIs removed |
| `shot` | A screenshot path as a data URI |
| `pairs` | `(name, count)` pairs for a chart |

Chart globals: `donut`, `bars`, `stack_bar`, `dial`, `sparkline`, `cover_art` and `Slice`. Autoescape is on.

The renderer loads `data:` URIs and `file://` paths under `reports/assets`, `/app/report-fonts` and `/app/scan_media` only. WeasyPrint does not resolve `var()` inside inline SVG attributes, so take a chart's colours from `ctx.palette`, `ctx.sev()` and `ctx.hue()`.

## Validation

A report request, a page estimate, and creating or updating a template all check the section list, and answer `400` when they refuse it. The message tells you what to fix:

| Message | Cause |
|---|---|
| `A report may hold at most 60 sections.` | More than 60 entries |
| `Unknown section '<name>'.` | No section has that name |
| `'<title>' can only appear once in a report.` | A section that is not `repeatable` appears twice |
| `<title>: <error>` | The entry's config fails the section's model |

To estimate the page count, reNgine reads each section's config: a section with a `max_rows` field counts its rows at 42 a page, `findings_detail`, `appendix_assets` and `screenshots` have their own rules, and any other section counts as one page.

To see the report builder and the generated files from the user's side, read [Reports and exports](../pentesters/reports.md).
