---
title: Remote control commands
description: "All 24 commands you can send to reNgine from Telegram, with their arguments, the capability each one needs, and which ones ask for your authenticator code. Use it when you run scans or check results from a chat."
sources:
  - channels/commands.py
  - channels/dispatch.py
  - channels/stepup.py
  - mcp/tools/
  - toolbox/
revised: 2026-10-03
generated: scripts/gen_chat.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_chat.py` writes it from `data/chat-commands.json` and `data/chat-help.txt`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Once an administrator has paired your Telegram chat with your reNgine account, you send these commands to the bot. Most of them run an [MCP tool](mcp-tools.md) or a toolbox lookup, within the capabilities granted to the chat. A command that needs more than the read capability is marked **Second factor**: the bot asks for the authenticator code of your account before it runs it. If your account has no authenticator enrolled, the chat can run read commands only. To set up the chat, see [Remote control over Telegram](../pentesters/telegram.md).

Write the first argument as it is, and any further arguments as `key=value`, for example `/scan example.com intensity=passive`.

## The help reply

Send `/help` and the bot replies with this list.

```text
reNgine commands

Targets
/targets <contains> · List targets
/target <target> · Resolve target
/add <targets> · Add targets · confirm

Scans
/scan <target> · Start a scan · confirm
/scans · Running scans
/progress <scan> · Scan status
/pause <scan> · Pause a scan · confirm
/resume <scan> · Resume a scan · confirm
/cancel <scan> · Cancel a scan · confirm

Results
/vulns <target> · Findings
/changes <window> · What changed

Lookups
/cve <cve> · CVE
/dns <domain> · DNS records
/http <target> · HTTP probe · confirm
/ip <ip> · IP address
/org <organization> · Domains by organization
/subs <domain> · Subdomain finder
/whois <query> · WHOIS

Chat
/help · Help
/start · Start
/project · Project
/projects · Projects
/whoami · Who am I
/unpair · Unpair

Send /help <command> for its arguments.
```

## All commands

**Runs** shows the MCP tool or toolbox lookup behind each command. <span class="rn-tag active">Active</span> marks a command that sends traffic to your target.

| Command | Group | Capability | Reach | Confirmation | Runs |
|---|---|---|---|---|---|
| [`/targets`](#targets) | Targets | read | <span class="rn-tag passive">Passive</span> |  | [`list_targets`](mcp-tools.md#list_targets) |
| [`/target`](#target) | Targets | read | <span class="rn-tag passive">Passive</span> |  | [`resolve_target`](mcp-tools.md#resolve_target) |
| [`/add`](#add) | Targets | write | <span class="rn-tag passive">Passive</span> | Second factor | [`add_target`](mcp-tools.md#add_target) |
| [`/scan`](#scan) | Scans | launch | <span class="rn-tag active">Active</span> | Second factor | [`start_scan`](mcp-tools.md#start_scan) |
| [`/scans`](#scans) | Scans | read | <span class="rn-tag passive">Passive</span> |  | [`scan_status`](mcp-tools.md#scan_status) |
| [`/progress`](#progress) | Scans | read | <span class="rn-tag passive">Passive</span> |  | [`scan_status`](mcp-tools.md#scan_status) |
| [`/pause`](#pause) | Scans | launch | <span class="rn-tag active">Active</span> | Second factor | [`pause_scan`](mcp-tools.md#pause_scan) |
| [`/resume`](#resume) | Scans | launch | <span class="rn-tag active">Active</span> | Second factor | [`resume_scan`](mcp-tools.md#resume_scan) |
| [`/cancel`](#cancel) | Scans | launch | <span class="rn-tag active">Active</span> | Second factor | [`cancel_scan`](mcp-tools.md#cancel_scan) |
| [`/vulns`](#vulns) | Results | read | <span class="rn-tag passive">Passive</span> |  | [`query_assets`](mcp-tools.md#query_assets) |
| [`/changes`](#changes) | Results | read | <span class="rn-tag passive">Passive</span> |  | [`what_changed`](mcp-tools.md#what_changed) |
| [`/cve`](#cve) | Lookups | read | <span class="rn-tag passive">Passive</span> |  | toolbox `cve` |
| [`/dns`](#dns) | Lookups | read | <span class="rn-tag passive">Passive</span> |  | toolbox `dns` |
| [`/http`](#http) | Lookups | launch | <span class="rn-tag active">Active</span> | Second factor | toolbox `http` |
| [`/ip`](#ip) | Lookups | read | <span class="rn-tag passive">Passive</span> |  | toolbox `ip` |
| [`/org`](#org) | Lookups | read | <span class="rn-tag passive">Passive</span> |  | toolbox `org_domains` |
| [`/subs`](#subs) | Lookups | read | <span class="rn-tag passive">Passive</span> |  | toolbox `subdomains` |
| [`/whois`](#whois) | Lookups | read | <span class="rn-tag passive">Passive</span> |  | toolbox `whois` |
| [`/help`](#help) | Chat | read | <span class="rn-tag passive">Passive</span> |  | Chat command |
| [`/start`](#start) | Chat | read | <span class="rn-tag passive">Passive</span> |  | Chat command |
| [`/project`](#project) | Chat | read | <span class="rn-tag passive">Passive</span> |  | Chat command |
| [`/projects`](#projects) | Chat | read | <span class="rn-tag passive">Passive</span> |  | Chat command |
| [`/whoami`](#whoami) | Chat | read | <span class="rn-tag passive">Passive</span> |  | Chat command |
| [`/unpair`](#unpair) | Chat | read | <span class="rn-tag passive">Passive</span> |  | Chat command |

## Targets { #group-targets }

### /targets { #targets }

The targets this token can reach, with project and type.

How to write it
:   `/targets <contains> [key=value]`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `contains` | `string` | No |  | Only targets whose value contains this text. |
| `limit` | `integer` | No | `50` |  |

The bot's reply to `/help targets`:

```text
/targets <contains> [key=value]
The targets this token can reach, with project and type.

Arguments
• contains (string): Only targets whose value contains this text.
• limit (integer, default 50)
```

### /target { #target }

For each of a target's result dimensions: whether it was scanned, what the most recent covering scan found, when, and the scan id other tools take. Call this first. covered=false means not scanned, not zero.

How to write it
:   `/target <target>`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `target` | `string` | Yes |  | A domain, IP address, CIDR range, URL or ASN added as a target. |

The bot's reply to `/help target`:

```text
/target <target>
For each of a target's result dimensions: whether it was scanned, what the most recent covering scan found, when, and the scan id other tools take. Call this first. covered=false means not scanned, not zero.

Arguments
• target (string, required): A domain, IP address, CIDR range, URL or ASN added as a target.
```

### /add { #add }

Add targets to a project. Records each target and queues WHOIS, DNS and routing enrichment. Runs no scan. An existing value is reused.

How to write it
:   `/add <targets> [key=value]`

Capability
:   `write`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

Confirmation
:   Asks for the authenticator code of your account before it runs

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `targets` | `string[]` | Yes |  | The values to add, each a domain, IP address, CIDR range, URL or ASN. Existing values are reused. |
| `project_id` | `string` | No |  | Which project to add them to. Omit when the token is scoped to one. |
| `tags` | `string[]` | No |  | Tags applied to the targets this call creates. Existing targets keep theirs. |
| `organizations` | `string[]` | No |  | Organizations applied to the targets this call creates. |

The bot's reply to `/help add`:

```text
/add <targets> [key=value]
Add targets to a project. Records each target and queues WHOIS, DNS and routing enrichment. Runs no scan. An existing value is reused.

Arguments
• targets (string[], required): The values to add, each a domain, IP address, CIDR range, URL or ASN. Existing values are reused.
• project_id (string): Which project to add them to. Omit when the token is scoped to one.
• tags (string[]): Tags applied to the targets this call creates. Existing targets keep theirs.
• organizations (string[]): Organizations applied to the targets this call creates.

Confirmed with the account's authenticator code.
```

## Scans { #group-scans }

### /scan { #scan }

Start a scan against a target in this token's project. Sends traffic to the target. Returns a scan id and a link. The scan runs in the background. Poll scan_status for progress.

How to write it
:   `/scan <target> [key=value]`

Capability
:   `launch`

Sends traffic to the target
:   <span class="rn-tag active">Active</span> Yes

Confirmation
:   Asks for the authenticator code of your account before it runs

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `target` | `string` | Yes |  | The target to scan. A value not yet in the project is added when the token holds the write capability. |
| `engine_id` | `string` | No |  | A saved scan engine. Omit for an ad hoc plan. |
| `stages` | `string[]` | No |  | Capability stages to enable when no engine is named. |
| `intensity` | `string` | No |  | One of: passive, normal, aggressive. |
| `context_id` | `string` | No |  | A saved scan context for auth, scope and rate. |
| `project_id` | `string` | No |  | Project to act in. Omit when the token is scoped to one. |

The bot's reply to `/help scan`:

```text
/scan <target> [key=value]
Start a scan against a target in this token's project. Sends traffic to the target. Returns a scan id and a link. The scan runs in the background. Poll scan_status for progress.

Arguments
• target (string, required): The target to scan. A value not yet in the project is added when the token holds the write capability.
• engine_id (string): A saved scan engine. Omit for an ad hoc plan.
• stages (string[]): Capability stages to enable when no engine is named.
• intensity (string): One of: passive, normal, aggressive.
• context_id (string): A saved scan context for auth, scope and rate.
• project_id (string): Project to act in. Omit when the token is scoped to one.

Confirmed with the account's authenticator code.
```

### /scans { #scans }

Scans running now.

How to write it
:   `/scans`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

The bot's reply to `/help scans`:

```text
/scans
Scans running now.
```

### /progress { #progress }

Status of a scan: stages finished, running and failed, and counts found so far. Pass a scan id, a target for its most recent run, or neither for every running scan.

How to write it
:   `/progress <scan> [key=value]`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `scan` | `string` | No |  | A scan id, as returned by start_scan or focused_rescan. |
| `target` | `string` | No |  | A target, to report its most recent run. |
| `limit` | `integer` | No | `5` | How many runs to list when neither scan nor target is named. |

The bot's reply to `/help progress`:

```text
/progress <scan> [key=value]
Status of a scan: stages finished, running and failed, and counts found so far. Pass a scan id, a target for its most recent run, or neither for every running scan.

Arguments
• scan (string): A scan id, as returned by start_scan or focused_rescan.
• target (string): A target, to report its most recent run.
• limit (integer, default 5): How many runs to list when neither scan nor target is named.
```

### /pause { #pause }

Pause a running scan. Stages in flight stop and run again from the start when the scan resumes. Results written so far are kept.

How to write it
:   `/pause <scan> [key=value]`

Capability
:   `launch`

Sends traffic to the target
:   <span class="rn-tag active">Active</span> Yes

Confirmation
:   Asks for the authenticator code of your account before it runs

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `scan` | `string` | No |  | The scan id to pause. |
| `target` | `string` | No |  | A target, to pause its running scan. |

The bot's reply to `/help pause`:

```text
/pause <scan> [key=value]
Pause a running scan. Stages in flight stop and run again from the start when the scan resumes. Results written so far are kept.

Arguments
• scan (string): The scan id to pause.
• target (string): A target, to pause its running scan.

Confirmed with the account's authenticator code.
```

### /resume { #resume }

Resume a paused scan. It restarts at its first unfinished stage. Stages that already succeeded are not run again.

How to write it
:   `/resume <scan> [key=value]`

Capability
:   `launch`

Sends traffic to the target
:   <span class="rn-tag active">Active</span> Yes

Confirmation
:   Asks for the authenticator code of your account before it runs

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `scan` | `string` | No |  | The scan id to resume. |
| `target` | `string` | No |  | A target, to resume its paused run. |

The bot's reply to `/help resume`:

```text
/resume <scan> [key=value]
Resume a paused scan. It restarts at its first unfinished stage. Stages that already succeeded are not run again.

Arguments
• scan (string): The scan id to resume.
• target (string): A target, to resume its paused run.

Confirmed with the account's authenticator code.
```

### /cancel { #cancel }

Stop a running scan. Stages in flight are aborted. Results written so far are kept. Takes effect immediately.

How to write it
:   `/cancel <scan> [key=value]`

Capability
:   `launch`

Sends traffic to the target
:   <span class="rn-tag active">Active</span> Yes

Confirmation
:   Asks for the authenticator code of your account before it runs

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `scan` | `string` | No |  | The scan id to stop. |
| `target` | `string` | No |  | A target, to stop whichever run of it is live. |

The bot's reply to `/help cancel`:

```text
/cancel <scan> [key=value]
Stop a running scan. Stages in flight are aborted. Results written so far are kept. Takes effect immediately.

Arguments
• scan (string): The scan id to stop.
• target (string): A target, to stop whichever run of it is live.

Confirmed with the account's authenticator code.
```

## Results { #group-results }

### /vulns { #vulns }

Findings on a target or across the selected project.

How to write it
:   `/vulns <target> [key=value]`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

Fixed arguments
:   `dimension` = `vulnerabilities`

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `target` | `string` | No |  | The target to search within. Omit to search every target in the project. |
| `query` | `string` | No |  | A query, for example `is:live and not is:cdn`, `severity:critical or is:kev`, `port:22 and is:sensitive`. describe_query_language lists the fields per dimension. Omit to return everything in scope. |
| `limit` | `integer` | No | `20` | Rows to return. |
| `offset` | `integer` | No | `0` | Rows to skip. |
| `project_id` | `string` | No |  | Project to search. Omit when the token is scoped to one. |

The bot's reply to `/help vulns`:

```text
/vulns <target> [key=value]
Findings on a target or across the selected project.

Arguments
• target (string): The target to search within. Omit to search every target in the project.
• query (string): A query, for example `is:live and not is:cdn`, `severity:critical or is:kev`, `port:22 and is:sensitive`. describe_query_language lists the fields per dimension. Omit to return everything in scope.
• limit (integer, default 20): Rows to return.
• offset (integer, default 0): Rows to skip.
• project_id (string): Project to search. Omit when the token is scoped to one.
```

### /changes { #changes }

New web assets, services, endpoints, addresses and findings per target over a window, plus targets not scanned or stale. Counts items first reported in the window against an earlier baseline. A target's first scan reports nothing as new.

How to write it
:   `/changes <window> [key=value]`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `window` | `string` | No | `7d` | How far back to look. One of: 7d, 14d, 30d. |
| `project_id` | `string` | No |  | Project to report on. Omit when the token is scoped to one. |

The bot's reply to `/help changes`:

```text
/changes <window> [key=value]
New web assets, services, endpoints, addresses and findings per target over a window, plus targets not scanned or stale. Counts items first reported in the window against an earlier baseline. A target's first scan reports nothing as new.

Arguments
• window (string, default 7d): How far back to look. One of: 7d, 14d, 30d.
• project_id (string): Project to report on. Omit when the token is scoped to one.
```

## Lookups { #group-lookups }

### /cve { #cve }

Exploitation likelihood, known-exploited status and published exploits.

How to write it
:   `/cve <cve>`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `cve` | `string` | Yes |  | CVE-2021-44228. |

The bot's reply to `/help cve`:

```text
/cve <cve>
Exploitation likelihood, known-exploited status and published exploits.

Arguments
• cve (string, required): CVE-2021-44228
```

### /dns { #dns }

Address, mail, nameserver, text and CAA records published for a domain.

How to write it
:   `/dns <domain>`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `domain` | `string` | Yes |  | Domain name to resolve. |

The bot's reply to `/help dns`:

```text
/dns <domain>
Address, mail, nameserver, text and CAA records published for a domain.

Arguments
• domain (string, required): Domain name to resolve
```

### /http { #http }

Status, title, server, technologies, certificate and CDN for a host.

How to write it
:   `/http <target> [key=value]`

Capability
:   `launch`

Sends traffic to the target
:   <span class="rn-tag active">Active</span> Yes

Confirmation
:   Asks for the authenticator code of your account before it runs

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `target` | `string` | Yes |  | example.com · https://example.com/login · 93.184.216.34. |
| `follow_redirects` | `boolean` | No | `true` | Report the final response in the redirect chain. |
| `screenshot` | `boolean` | No | `true` | Render the page in a headless browser. |

The bot's reply to `/help http`:

```text
/http <target> [key=value]
Status, title, server, technologies, certificate and CDN for a host.

Arguments
• target (string, required): example.com · https://example.com/login · 93.184.216.34
• follow_redirects (boolean, default true): Report the final response in the redirect chain
• screenshot (boolean, default true): Render the page in a headless browser

Confirmed with the account's authenticator code.
```

### /ip { #ip }

Network, operator, country and reverse DNS for an address, with its scan history.

How to write it
:   `/ip <ip>`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `ip` | `string` | Yes |  | 8.8.8.8 · 2606:4700::1111. |

The bot's reply to `/help ip`:

```text
/ip <ip>
Network, operator, country and reverse DNS for an address, with its scan history.

Arguments
• ip (string, required): 8.8.8.8 · 2606:4700::1111
```

### /org { #org }

Domains and networks registered to an organization, from certificate transparency, reverse WHOIS and the routing registry.

How to write it
:   `/org <organization>`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `organization` | `string` | Yes |  | Cloudflare, Inc. · github.com · hostmaster@example.com. |

The bot's reply to `/help org`:

```text
/org <organization>
Domains and networks registered to an organization, from certificate transparency, reverse WHOIS and the routing registry.

Arguments
• organization (string, required): Cloudflare, Inc. · github.com · hostmaster@example.com
```

### /subs { #subs }

Hostnames for a domain from passive sources.

How to write it
:   `/subs <domain> [key=value]`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `domain` | `string` | Yes |  | Registrable domain to enumerate. |
| `sources` | `string[]` | No | `['certificates', 'subfinder', 'assetfinder']` | Passive sources to query. |

The bot's reply to `/help subs`:

```text
/subs <domain> [key=value]
Hostnames for a domain from passive sources.

Arguments
• domain (string, required): Registrable domain to enumerate
• sources (string[], default ['certificates', 'subfinder', 'assetfinder']): Passive sources to query
```

### /whois { #whois }

Registration and allocation records for a domain, address block or autonomous system.

How to write it
:   `/whois <query>`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

It takes these arguments.

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | `string` | Yes |  | example.com · 8.8.8.8 · 1.1.1.0/24 · AS13335. |

The bot's reply to `/help whois`:

```text
/whois <query>
Registration and allocation records for a domain, address block or autonomous system.

Arguments
• query (string, required): example.com · 8.8.8.8 · 1.1.1.0/24 · AS13335
```

## Chat { #group-chat }

### /help { #help }

The command list, or the usage of one command.

How to write it
:   `/help [command]`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

The bot's reply to `/help help`:

```text
/help
The command list, or the usage of one command.
```

### /start { #start }

Pair this chat, or show its status once paired.

How to write it
:   `/start`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

The bot's reply to `/help start`:

```text
/start
Pair this chat, or show its status once paired.
```

### /project { #project }

Show or switch the selected project.

How to write it
:   `/project`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

The bot's reply to `/help project`:

```text
/project
Show or switch the selected project.
```

### /projects { #projects }

The projects this account can select.

How to write it
:   `/projects`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

The bot's reply to `/help projects`:

```text
/projects
The projects this account can select.
```

### /whoami { #whoami }

This chat's account, project and capabilities.

How to write it
:   `/whoami`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

The bot's reply to `/help whoami`:

```text
/whoami
This chat's account, project and capabilities.
```

### /unpair { #unpair }

Remove this chat's access.

How to write it
:   `/unpair`

Capability
:   `read`

Sends traffic to the target
:   <span class="rn-tag passive">Passive</span> No

The bot's reply to `/help unpair`:

```text
/unpair
Remove this chat's access.
```

