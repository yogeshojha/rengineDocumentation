# Writing rengine.wiki

Authoring guide for the reNgine documentation site. This file is not published.

## Stack and commands

MkDocs 1.6.1 with Material for MkDocs 9.7.7, Python only, no Node build step.

| Command | Effect |
|---|---|
| `make serve` | Regenerates the reference and serves the site on `http://127.0.0.1:8008` |
| `make gen` | Writes the generated reference pages from `data/` |
| `make build` | `mkdocs build --strict` into `site/` |
| `make lint` | Checks every page against the copy rules |
| `make check` | `build`, `lint` and the link check |
| `make snapshot` | Refreshes `data/repo.json` from a reNgine checkout at `../rengine` |

`hooks/rengine.py` adds the page metadata block, the Markdown copy of every page, `llms.txt` and `llms-full.txt`. `overrides/` holds the theme templates. `docs/assets/stylesheets/rengine.css` and `docs/assets/javascripts/rengine.js` hold the styling and the pane behaviour.

A running `make serve` rebuilds pages when templates, styles or data change, but it keeps the `hooks/rengine.py` it imported at start. After editing the hook, restart `make serve`, or the served pages keep the old behaviour, for example home-page links that point at `.` and empty step text.

## Front matter

Every page starts with front matter. The build fails on a page without `title`, `description`, `sources` or `revised`.

```yaml
---
title: Run a scan
description: A scan runs a scan engine, or a custom stage selection, against one target at one intensity.
layout: pane
sources:
  - frontend/src/lib/components/scans/launch/launch-dialog.svelte
  - api/app/api/v1/scans.py
revised: 2026-10-03
---
```

| Key | Use |
|---|---|
| `title` | The page title. The template renders it as the H1. A page body has no `# ` heading. |
| `description` | One or two declarative sentences. Rendered as the lede under the title, used for `<meta name="description">` and for the entry in `llms.txt`. Backticks and `**bold**` render. Do not repeat it as the first paragraph. |
| `sources` | Repository paths in `yogeshojha/rengine`, relative to the root. `path:line` and `path:start-end` link to lines. A path ending in `/` links to a directory. A path with the prefix `docs:` names a file of this documentation repository, for example `docs:hooks/rengine.py`. |
| `revised` | The date of the last factual review, `YYYY-MM-DD`. |
| `layout` | `pane` for a task page, an API operation page or an MCP page. Omit for every other page. `pane` hides the table of contents. |
| `endpoint` | API operation pages: `POST /api/v1/subdomains/search`. Rendered under the title. |
| `generated` | Generated pages only: the script that wrote the page. |
| `nav_order` | Generated pages in a directory listed in the nav as `reference/stages/`. |

## Page types

| Type | Layout | Examples |
|---|---|---|
| Task | `pane` | Run a scan, Burp Suite connector, Connect an MCP client |
| API operation | `pane` | Search web assets |
| MCP page | `pane` | Recipes, Connect an MCP client |
| Concept, install, administration | full width, table of contents on the right | Install reNgine, Security model |
| Reference | full width | Query language fields, Stages |

## Writing rules

Write the way an experienced pentester explains reNgine to a colleague who is about to use it: plainly, directly, and with the purpose first. The reader is a person, not a parser.

- **Talk to the reader as "you".** The reader is a pentester, a security engineer, a developer, or someone connecting an AI agent to reNgine.
- **Start with the purpose.** Every page, and every section that introduces something, opens with one or two sentences on what it lets you do and when you would want it. Then how to do it. Then the details.
- **Use everyday words.** Use, run, set up, connect, find, send, check. Avoid machine words such as operate, drive, record, ingest, fold, surface, emit or ceiling, unless you explain them.
- **Explain reNgine terms on first use.** Do it in plain words, for example: "A scan context holds the login headers, scope rules and rate limits for a target, so you set them once and every scan uses them."
- **Say who does what.** Use the active voice and one idea per sentence: "reNgine sends the request to Burp", not "The request is sent".
- **Show an example.** A query, a command or a screen does more than an abstract description.
- **Stay accurate.** Every fact, number, label and limit stays exactly as verified in the code. A friendlier sentence must not change what is true, and a fact that cannot be verified is left out.
- **Introduce tables.** Keep tables of limits, flags and fields, and introduce each one with a sentence that says why you would look at it.
- **No hype.** Not powerful, seamless, robust, cutting-edge, best-in-class, game-changing or amazing. Not "simply", "just" or "easily", which make the reader feel slow when something does not work. No exclamation marks and no emoji.
- **No arguing.** Do not argue for reNgine or compare it with other tools. Saying what a feature is good for is not arguing; it is the point of the page.
- **Bold interface labels** exactly as the interface prints them. Verify each label in `frontend/src`.

### Before and after

| Before | After |
|---|---|
| reNgine 3.0 documentation | reNgine 3.0 |
| Install and operate reNgine, query the attack surface, and drive it from the HTTP API or an MCP client. | Everything you need to install reNgine, scan your targets, find what matters in the results, and connect reNgine to Burp Suite, your own scripts and your AI agents. |
| A finding opens in Burp Repeater with the request nuclei sent. Requests repeated in Burp return to reNgine as endpoints with `source:proxy`. | Burp Suite and reNgine now work together. Send a finding to Burp Repeater in one click and test it by hand, starting from the exact request nuclei sent. What you find in Burp comes back to reNgine as endpoints, so your manual testing and your scans stay in one place. |
| The connector is a Burp Suite extension paired with one connection in a reNgine project. | The connector is a small Burp Suite extension. Load it in Burp, paste in a token from reNgine, and the two stay connected while you work. |
| Intensity sets the request rate of every tool. | Intensity decides how hard reNgine hits your target. Use Passive when you must not send any traffic, Normal for most scans, and Aggressive when you own the target and want results faster. |

`make lint` checks the mechanical rules: banned words, emoji, exclamation marks and retired nouns. `python3 scripts/lint_copy.py <file>` checks one file. Reading the page aloud checks the rest.

`make lint` enforces the mechanical part of these rules. `python3 scripts/lint_copy.py <file>` checks one file.

### Glossary

| Term | Meaning | Never |
|---|---|---|
| target | What a user adds: a domain, IP address, CIDR range, URL or ASN | |
| web asset | A probed host name recorded by a scan | host, web host, live host, subdomain, for the probed row |
| address | An IP address | |
| service | One `ip:port` | |
| endpoint | A URL | |
| finding | One result of a check on one asset | |
| issue | Findings grouped by check | |
| exposure | A saved rule over the attack surface and the rows that match it | |
| scan, run | A scan is launched. Each execution of it is a run. | |
| scan engine | A saved stage selection with settings and an intensity | |
| scan context | Saved scope, authentication, rate limits and proxy for a run | |
| schedule | A recurring launch | |
| stage | One unit of the pipeline | |

"Passive" has three meanings. Keep them apart: the Passive preset (a stage selection in an engine), passive intensity (a run-level switch) and stage names such as `passive_ports`.

## The pane

A task page puts the prose on the left and a sticky dark pane on the right. The pane shows the same task on each surface: **Interface**, **HTTP API** and **MCP**, plus **rengine CLI** or **Telegram** where they apply. The first tab is the default surface of the section: Interface for Pentesters, HTTP API for Developers, MCP for Agents.

```markdown
<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Start a scan

1. **Open the launch dialog.** Select **New scan** on the **Scans** page.
2. **Add the targets.** Type a domain in **Targets**. <span class="rn-ref" data-tab="Interface" data-mark="targets">Shown in the pane</span>

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Launch dialog</b><span>example.com</span></div>

/// tab | Interface
<div class="rn-ui" aria-label="New scan dialog with the target example.com">
<span class="rn-ui-dlg">
<span class="rn-ui-dlg__head"><b>New scan</b><span>1 target</span></span>
<span class="rn-ui-fld" data-mark="targets"><span class="rn-ui-label">Targets</span><span class="rn-ui-in"><span class="rn-ui-chip">example.com</span></span></span>
</span>
</div>
///

/// tab | HTTP API
<div class="rn-pane-label">request</div>

```bash
curl -b jar -X POST "$RENGINE/api/v1/scans/batch?project_id=$PROJECT" ...
```
///

/// tab | MCP
<div class="rn-pane-label">tools/call</div>

```json
{ "name": "start_scan", "arguments": { "target": "example.com" } }
```
///

</div>
</div>
```

Rules:

- The wrapper is `div.rn-split` holding `div.rn-prose` and `div.rn-pane`, each with the `markdown` attribute. A page may hold several splits, one per task.
- Tabs use `pymdownx.blocks.tab`: `/// tab | Label` on its own line, the content, then `///`. Consecutive tabs form one tab set. The indented `===` syntax of `pymdownx.tabbed` cannot hold raw HTML and is not used.
- An ordered list in `rn-prose` renders as numbered steps. The first `**bold**` run of a step is its title.
- A step that refers to the pane ends with `<span class="rn-ref" data-tab="<tab label>" data-mark="<name>">Shown in the pane</span>`. Selecting or scrolling to the step selects that tab and highlights every element with `data-mark="<name>"` in it. `data-mark` takes several names separated by spaces.
- `div.rn-pane-head` names the view and its scope. `div.rn-pane-label` labels a block inside a tab, such as `request` or `response · 200`.
- On screens narrower than 1,056 pixels the pane stacks under the prose.

### Interface recreations

An interface recreation is HTML, not a screenshot. Its labels are verified against the frontend source. Examples use `example.com`, `asm.example.com`, `acme` and other reserved names, never data from a real instance.

An interface recreation is exactly one `<div class="rn-ui" aria-label="...">` with inline elements only inside it: `span`, `b`, `i`, `em`, `small`, `code`, `kbd`, `svg`. A `<p>`, a nested `<div>` or a list inside it breaks the Markdown parser, and the build warns. The classes set the layout. The `aria-label` describes the view in one sentence and replaces the recreation in the Markdown copy of the page.

| Class | Renders |
|---|---|
| `rn-ui-dlg`, `rn-ui-sheet` | A dialog or sheet frame |
| `rn-ui-dlg__head` | Dialog title in `b`, scope in `span` |
| `rn-ui-bar` | A sheet or page header row |
| `rn-ui-fld` | A form field. Holds `rn-ui-label`, a control and an optional `rn-ui-help`. |
| `rn-ui-in` | A text input or select. `is-placeholder` greys the text. `is-secret` for a masked value. |
| `rn-ui-chip` | A chip inside an input |
| `rn-ui-seg` | A segmented control. Set `style="--rn-n:3"` to the number of options. The selected option has class `on`. |
| `rn-ui-toggle` with `rn-ui-switch` | A labelled switch. `rn-ui-switch on` is enabled. |
| `rn-ui-check` | A checkbox row. `on` is checked. |
| `rn-ui-foot` with `rn-ui-btn` | Dialog buttons. `pri` is the primary button, `danger` a destructive one. |
| `rn-ui-qb` | The query bar. Holds an icon `svg`, a `rn-q` query with `f` field spans, and `rn-ui-qb__count`. |
| `rn-ui-scope` | Scope chips above a table. `on` is selected. |
| `rn-ui-tabs` | A row of tabs, with an optional `small` count. `on` is selected. |
| `rn-ui-rows` with `rn-ui-rows__head` and `rn-ui-row` | A result table. Set columns with `style="--rn-cols: 1.4fr 3rem 1fr"`. |
| `rn-ui-host`, `rn-ui-mono`, `rn-ui-status`, `rn-ui-title`, `rn-ui-text`, `rn-ui-muted`, `rn-ui-tech` | Cells. `rn-ui-status--3xx`, `--4xx`, `--5xx` colour a status. |
| `rn-ui-list`, `rn-ui-item` | A list of rows with a `b` name, a `small` detail and a trailing control |
| `rn-ui-kv` | Key and value pairs, alternating `span` elements |
| `rn-ui-code` | A token or configuration value |
| `rn-ui-chat`, `rn-ui-msg`, `rn-ui-msg out` | A chat transcript. `rn-ui-btns` holds inline buttons. |
| `rn-ui-note` | A muted line |
| `rn-ui-stack` | Stacks children with a gap |

Severity chips and reach tags work inside recreations.

## Inline elements

| Element | Markup |
|---|---|
| Reach tag | `<span class="rn-tag passive">Passive</span>`, `<span class="rn-tag active">Active</span>` |
| Severity chip | `<span class="rn-sev critical">critical</span>`, also `high`, `medium`, `low`, `info` |
| Query chip | `` `tech:jenkins is:live`{ .rn-q } ``. Field names are coloured. |
| Keys | `++ctrl+k++` or `<kbd>Ctrl</kbd>` |
| Count | `{{ counts.stages }}`. Keys are computed by `hooks/rengine.py` from `data/`: `query_dimensions`, `query_fields`, `query_flags`, `stages`, `steps`, `mcp_tools`, `mcp_capabilities`, `api_paths`, `api_operations`, `api_tags`, `cli_commands`, `installer_flags`, `env_variables`, `chat_commands`, `pinned_tools`. |
| Section index | `{{ section_index }}` on a line of its own, in a section landing page, expands to one table per group of the section with each page and its `description`. |

## Callouts

Three kinds only: `note`, `warning`, `danger`. An empty title shows no title line.

```markdown
!!! note ""
    Passive intensity is a run-level switch. The Passive preset is a stage selection.

!!! danger "SECRET_KEY"
    Rotating SECRET_KEY makes stored secrets and two-factor secrets unreadable.
```

## Links

Link to pages by their source path: `[Run a scan](run-a-scan.md)`, `[Stages](../reference/stages/index.md)`. The build fails on a broken link or anchor.

## Generated pages

Pages under `docs/reference/` that carry `generated:` front matter are written by `scripts/gen_*.py` from `data/`. Edit the generator or the data, then run `make gen`. `data/README.md` names the dump script and the command that refreshes each snapshot.

## Redirects

`extra.redirects` in `mkdocs.yml` maps an old path to a page. The hook writes a page at the old path that sends the browser to the new one. The interface links to `/import/targets/`, `/import/json/` and `/import/csv/`, and the 2.x site used paths such as `/getting-started/`. Keep those entries.

## Lint pragmas

`<!-- lint: retired nouns listed -->` in a page lets it name the retired nouns, as the glossary does. The comment is removed from the Markdown copy.

## Agent outputs

The hook writes, for every page:

- a Markdown copy at the page URL with `.md` in place of the trailing slash, for example `/pentesters/install.md`. The home page is `/index.md`.
- an entry in `/llms.txt`, grouped by section, with the page description.
- the full Markdown in `/llms-full.txt`.
- the files under `agent-files/` at `/agent-files/`, for example `/agent-files/AGENTS.md`.

The Markdown copy is built from the page source: wrappers are removed, tabs become bold labels, interface recreations become their `aria-label`, callouts become block quotes, and links point at Markdown copies.
