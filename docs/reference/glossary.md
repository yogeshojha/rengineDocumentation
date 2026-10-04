---
title: Glossary
description: What the words in reNgine mean. Use it when a term in the interface or in these pages is not clear to you, or when you want to describe your work in the same words.
sources:
  - frontend/src/lib/config/routes.ts
  - frontend/src/lib/glossary.test.ts
  - shared/definitions/surface.py
  - shared/definitions/asset_query.py
  - shared/definitions/tripwires.py
  - shared/definitions/watch.py
  - shared/definitions/interest.py
  - mcp/capabilities.py
revised: 2026-10-03
---

<!-- lint: retired nouns listed -->

Labels you see in the interface are in bold. The Never column lists words that the interface and these pages do not use for that meaning, so each term stays unambiguous.

## Assets and results

What a scan finds, and how reNgine counts it.

| Term | Meaning | Never | See |
|---|---|---|---|
| Target | What you add to a project: a domain, an IP address, a CIDR range, a URL or an ASN. A scan runs against one target. | | [Projects and targets](../pentesters/targets.md) |
| Web asset | A host name recorded by a scan, with the HTTP response probed on it. The **Web assets** dimension lists them. | host, web host, live host, subdomain, for the probed row | [Web assets](query/web-assets.md) |
| Address | An IP address. The **IP addresses** dimension lists each distinct address once, with every target it serves. | | [IP addresses](query/ips.md) |
| Service | One open port on one address, as `ip:port`, recorded by a scan. | | [Services](query/services.md) |
| Endpoint | A URL: a host, a path and a parameter shape, recorded by a scan. | | [Endpoints](query/endpoints.md) |
| Finding | One check that fired at one location in one run. | | [Findings and triage](../pentesters/findings.md) |
| Issue | The findings of one check, grouped. | | [Findings and triage](../pentesters/findings.md) |
| Software CVE | One published CVE inferred for one software name and version on one asset in one run. | | [Software](query/software.md) |
| Secret | One distinct value a detector matched in a stored response, with every place it was read. | | [Secret mining](../pentesters/secret-mining.md) |
| Dimension | One of the seven result types: **Web assets**, **Endpoints**, **Services**, **IP addresses**, **Vulnerabilities**, **Software** and **Secrets**. | | [Your attack surface](../pentesters/attack-surface.md) |
| Attack surface | The rows of the seven dimensions. The **Attack surface** section of the sidebar opens them across a project. | | [Your attack surface](../pentesters/attack-surface.md) |
| Coverage | A dimension is covered for a target when a covering stage succeeded in a run, or when a run wrote rows to it. | | [Your attack surface](../pentesters/attack-surface.md) |
| Not scanned | A dimension without coverage. Distinct from zero rows. | zero, for a dimension that was not scanned | [Your attack surface](../pentesters/attack-surface.md) |
| Exposure | An asset flagged by an exposure rule, a correlation or AI, with an interest score above zero. The **Exposures** page lists them. | | [Exposures](../pentesters/exposures.md) |
| Evidence | The rung of a finding or a software CVE on the evidence ladder: **Inferred**, **Observed**, **Corroborated** or **Proven**. | | [Exploit intelligence](../pentesters/exploit-intelligence.md) |
| Seed asset | A stored asset a run starts from, in place of discovering it again. | | [Projects and targets](../pentesters/targets.md) |

## Scanning

How you set up and run scans.

| Term | Meaning | Never | See |
|---|---|---|---|
| Project | A set of targets with the scan engines, scan contexts and schedules that run against them. | | [Projects and targets](../pentesters/targets.md) |
| Scan, run | A scan is one launch against one target. Each scan is listed as a run on the **Scans** page, and you can compare two runs of a target. | | [Run a scan](../pentesters/run-a-scan.md) |
| Stage | One unit of the scan pipeline, such as **HTTP Probe** or **Vulnerability Scan**. A run executes its stages in steps. | step, for a stage | [Stages](stages/index.md) |
| Capability stage | A stage selected in a scan engine or a custom scan. | | [Stages](stages/index.md) |
| Support stage | A stage that runs when a selected stage needs what it produces, or when its own input is available. | | [Stages](stages/index.md) |
| Execution step | A group of stages that run in parallel within a run. The next step starts when every stage of the step has settled. | | [Stages](stages/index.md) |
| Scan engine | A saved stage selection with stage settings and an intensity. | profile, template, for an engine | [Scan engines and intensity](../pentesters/scan-engines.md) |
| Custom scan | A stage selection you choose in the launch dialog for one launch, instead of a saved scan engine. | | [Run a scan](../pentesters/run-a-scan.md) |
| Preset | The starting stage selection of a new scan engine: **Standard Recon**, **Passive Recon**, **Full Sweep** or **Blank**. | | [Stages](stages/index.md#presets) |
| Intensity | The request rates of a run, which decide how hard reNgine hits your target: **Passive**, **Normal** or **Aggressive**. At Passive, the stages that send traffic to the target are skipped. | | [Scan engines and intensity](../pentesters/scan-engines.md) |
| Passive | Three separate meanings: the **Passive Recon** preset (a stage selection), passive intensity (a run-level switch) and stage names such as `passive_ports`. | | [Scan engines and intensity](../pentesters/scan-engines.md) |
| Scan context | Saved scope, authentication, rate limits, runtime settings and a proxy, applied to a run on top of its scan engine. You save it once and choose it when you launch a scan. | | [Scan contexts](../pentesters/scan-contexts.md) |
| Schedule | A recurring launch of a scan engine against targets. | | [Schedule scans](../pentesters/schedules.md) |
| Focused rescan | A run of chosen stages against assets picked from completed scans, without enumerating the target again. | | [Focused rescans](../pentesters/focused-rescans.md) |
| Monitor against new checks | A daily focused run that tests the web assets of a target with checks added to the check library since its last scan. | | [Run a scan](../pentesters/run-a-scan.md#monitor-against-new-checks) |
| Tripwire | A saved query with actions. It notifies or starts a scan when a result of a run matches. | | [Tripwires](../pentesters/tripwires.md) |

## Interface and integrations

The pages and the connections around your scans.

| Term | Meaning | See |
|---|---|---|
| Arsenal | The page that holds the check library, wordlists, threat intelligence and the callback server. | [Settings](../pentesters/settings.md) |
| Toolbox | Lookups that run outside a scan, such as WHOIS, DNS records and the subdomain finder. | [Remote control commands](remote-control-commands.md#group-lookups) |
| What's new | The feed of changes across every target of a project. | [Compare runs and What's new](../pentesters/compare-runs.md) |
| Connector | A link between reNgine and a proxy tool. Burp Suite is the connector of this release. | [Burp Suite](../pentesters/burp-suite.md) |
| Remote control | Commands sent to reNgine from a paired Telegram chat. | [Control reNgine from Telegram](../pentesters/telegram.md) |
| Agent | An MCP client that holds a key issued on the **Agents** page. | [Connect your agent](../agents/mcp/connect.md) |
| Capability | A permission of an MCP key: `read`, `plan`, `write` or `launch`. | [Control what an agent can do](../agents/mcp/capabilities.md) |
| Instance ceiling | The capabilities an administrator allows for every MCP key on the instance. `launch` is off by default. | [Control what an agent can do](../agents/mcp/capabilities.md) |
| Bounty Hub | The bug bounty mode pages for HackerOne and Intigriti programs and reports. | [Bounty Hub](../pentesters/bounty-hub.md) |
| Program watch | Continuous discovery for one bug bounty program: certificate transparency monitoring and scheduled scans inside the program scope. | [Program watches](../pentesters/program-watches.md) |
| Instance mode | **Bug bounty** or **Corporate**, one per instance. | [Bug bounty and corporate modes](../pentesters/instance-modes.md) |
| Administrator | One of the two privilege levels. The other is user. There are no roles and no per-project permissions. | [Users and two-factor authentication](../pentesters/users.md) |

## Reach tags

These tags tell you whether something sends traffic to your target.

| Tag | Meaning |
|---|---|
| <span class="rn-tag passive">Passive</span> | A stage, a tool or a command that sends no traffic to the target |
| <span class="rn-tag active">Active</span> | A stage, a tool or a command that sends traffic to the target |
