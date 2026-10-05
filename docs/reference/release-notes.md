---
title: Release notes 3.0.0
description: reNgine 3.0.0, codename Sirius, is a new code base with a new data model. This page lists what it contains and what to expect when you move from 2.x.
sources:
  - VERSION
  - README.md
  - docker-compose.prod.yml
  - .github/workflows/build.yml
  - install.sh
  - deploy/rengine
revised: 2026-10-05
---

Each item below links to the page that shows you how to use it.

## Upgrading from 2.x

reNgine 3.0 cannot import a 2.x database. To move to 3.0, install it as a new instance with [the installer](../pentesters/install.md) and add your targets again.

## Platform

What reNgine 3.0.0 runs on.

| Part | 3.0.0 |
|---|---|
| API | FastAPI on Python 3.13 |
| Interface | SvelteKit 5 on Node.js 22 |
| Workers | Celery: worker-scans, worker-control, worker-default and worker-beat |
| Database | PostgreSQL 16 |
| Queues and cache | Two Redis 8 instances |
| Proxy | Caddy 2, one origin for the interface and the API |
| Images | `yogeshojha/rengine-api`, `-worker` and `-frontend` on Docker Hub and the GitHub Container Registry, for amd64 and arm64 |

To see how the parts fit together, read [How reNgine works](../developers/architecture.md). For the version of each tool, see [Pinned tool versions](tool-versions.md).

## Install and run

- An installer, `install.sh`, with three exposure modes: `--domain`, `--ip` and `--local`. It sizes the instance for the memory of your host. See [Install reNgine](../pentesters/install.md).
- The `rengine` command to manage your instance, with {{ counts.cli_commands }} commands: start, stop, restart, status, logs, scale, update, backup, restore, reset-password, uninstall and version. See [rengine CLI](cli.md).
- Backup archives protected with a passphrase, database snapshots before each update, and rollback to a tagged release. See [Back up and restore](../pentesters/backup.md) and [Update and roll back](../pentesters/update.md).
- Two instance modes, bug bounty and corporate. See [Bug bounty and corporate modes](../pentesters/instance-modes.md).
- Two privilege levels, user and administrator, and two-factor authentication. See [Users and two-factor authentication](../pentesters/users.md).
- An **About reNgine** dialog with the release and every pinned tool version, ready to paste into a bug report. See [Report an issue](../pentesters/troubleshooting.md#report-an-issue).

## Scanning

- {{ counts.stages }} stages in {{ counts.steps }} execution steps. See [Stages](stages/index.md).
- Scan engines written in YAML, the built-in Default engine and four presets. See [Scan engines and intensity](../pentesters/scan-engines.md).
- Passive, Normal and Aggressive intensity, so you decide how hard a scan hits your target. See [Scan engines and intensity](../pentesters/scan-engines.md).
- Scan contexts for scope, authentication, rate limits and a proxy. See [Scan contexts](../pentesters/scan-contexts.md).
- One-off, interval, daily and cron schedules. See [Schedule scans](../pentesters/schedules.md).
- Pause, resume and cancel for running scans, focused rescans of chosen assets, and daily runs that test your targets against new checks. See [Focused rescans](../pentesters/focused-rescans.md).
- The source IP of each run, checked at the start and end of the scan through its proxy, to match a scan against the target's logs. See [Match the scan to the target's logs](../pentesters/run-a-scan.md#source-ip).

## Results

- Seven dimensions: web assets, endpoints, services, IP addresses, vulnerabilities, software and secrets. See [Your attack surface](../pentesters/attack-surface.md).
- One query language over every dimension, with {{ counts.query_fields }} fields and {{ counts.query_flags }} flags. See [Search the attack surface](../pentesters/query.md).
- Findings grouped into issues, with review states that carry over from one run to the next. See [Findings and triage](../pentesters/findings.md).
- EPSS, CISA KEV and NVD data, software CVE inference and the evidence ladder. See [Exploit intelligence](../pentesters/exploit-intelligence.md).
- Correlation across targets, exposures and saved rules. See [Correlation](../pentesters/correlation.md) and [Exposures](../pentesters/exposures.md).
- Compare two runs of a target to see what changed, and follow What's new across a project. See [Compare runs and What's new](../pentesters/compare-runs.md).
- Notes on targets, scans and assets. See [Notes](../pentesters/notes.md).
- Reports and exports. See [Reports and exports](../pentesters/reports.md).

## Detections

- Secret mining in stored responses. See [Secret mining](../pentesters/secret-mining.md).
- Lookalike domains. See [Lookalike domains](../pentesters/lookalike-domains.md).
- Tripwires: saved queries that notify you or start a scan when a result of a run matches. See [Tripwires](../pentesters/tripwires.md).
- AI detection on web assets and services. See [AI detection](../pentesters/ai-detection.md).
- Broken link hijacking. See [Broken link hijacking](../pentesters/broken-links.md).
- Subdomain takeover, zone transfer, web hygiene and domain posture checks. See [Stages](stages/index.md).

## Integrations

- The Burp Suite connector, to send findings to Burp for manual testing and bring what you find in Burp back to reNgine. See [Burp Suite](../pentesters/burp-suite.md).
- The MCP server with {{ counts.mcp_tools }} tools, so AI agents can ask questions about your attack surface and, if you allow it, start scans. See [Connect your agent](../agents/mcp/connect.md).
- Remote control over Telegram with {{ counts.chat_commands }} commands, to start scans and check results from a chat. See [Control reNgine from Telegram](../pentesters/telegram.md).
- Notifications and issue trackers. See [Notifications](../pentesters/notifications.md) and [Issue trackers](../pentesters/issue-trackers.md).
- AI providers. See [AI providers](../pentesters/ai-providers.md).
- Bounty Hub and program watches. See [Bounty Hub](../pentesters/bounty-hub.md) and [Program watches](../pentesters/program-watches.md).
- The HTTP API with {{ counts.api_paths }} paths. See [HTTP API paths](http-api.md).
