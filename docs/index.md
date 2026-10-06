---
template: home.html
title: reNgine 3.0
description: How to install reNgine, scan your targets, work through the results, and connect reNgine to Burp Suite, your own tools and your AI agents.
sources:
  - README.md
  - VERSION
  - frontend/src/lib/components/scans/results/query-bar/query-suggestions.svelte
  - frontend/src/lib/components/bounty-hub/watch-dialog.svelte
  - frontend/src/lib/components/bounty-hub/watch-host-row.svelte
  - frontend/src/lib/components/tripwires/tripwire-button.svelte
  - shared/definitions/notifications.py
  - shared/definitions/correlation.py
  - shared/definitions/threat_intel.py
  - shared/definitions/secrets.py
  - frontend/src/lib/config/ai-services.ts
  - channels/dispatch.py
  - mcp/tools/resolve_target.py
  - mcp/tools/query_assets.py
  - frontend/src/lib/components/modals/add-target-modal.svelte
  - frontend/src/lib/components/targets/list/prefs.svelte.ts
  - frontend/src/lib/components/ask/estate-composer.svelte
  - frontend/src/lib/components/ask/ask-page.svelte
  - shared/definitions/notifications.py
  - docs:data/stages.json
revised: 2026-10-06
hide:
  - navigation
  - toc
audiences:
  - title: Pentesters
    text: Install reNgine, run scans and work through what they find
    surface: Interface
    link: pentesters/index.md
  - title: Developers
    text: Learn how reNgine is built, use the HTTP API and extend it
    surface: HTTP API
    link: developers/index.md
  - title: Agents
    text: Connect AI agents over MCP and point them at these docs
    surface: MCP
    link: agents/index.md
run_title: One run, start to finish
run_text: Add a target, scan it, search and question the results, then act on what you find.
run_label: "One run in reNgine: example.com is added and scanned, the web assets are narrowed with tech:jenkins is:live, Ask lists the known exploited findings to fix first, and the first one is alerted on Telegram, sent to Burp Repeater and filed in Jira."
run:
  - scene: target
    title: Add a target
    text: A domain, an IP address, a CIDR range, a URL or an ASN. With **Scan after adding** on, the first scan starts as soon as the target is saved.
    label: Projects and targets
    link: pentesters/targets.md
  - scene: scan
    title: Scan it
    text: Each stage adds to the picture, from names and services to web assets, endpoints and findings. The counts update while the scan runs.
    label: Run a scan
    link: pentesters/run-a-scan.md
  - scene: results
    title: Search the results
    text: Seven result types share one query language. `tech:jenkins is:live` narrows 412 web assets to 2.
    label: Query language
    link: pentesters/query.md
  - scene: ask
    title: Ask a question
    text: Ask in plain language. The answer comes back as counted rows, and each number opens the rows behind it.
    label: Ask
    link: pentesters/ask.md
  - scene: act
    title: Act on it
    text: Receive the alert, send the request to Burp Repeater and file the issue in Jira, all from the finding.
    label: Burp Suite connector
    link: pentesters/burp-suite.md
layers_title: Your attack surface, layer by layer
layers_text: Each layer of your attack surface has its own page, from the programs in your scope to the secrets your targets expose. The sidebar, the tables and the query language stay the same on every one of them.
layers:
  - view: programs
    title: Bring in your bug bounty programs
    text: In bug bounty mode, Bounty Hub lists your HackerOne and Intigriti programs with their scope. You can add a program's in-scope assets as targets in one step, and watch a program to be alerted when a new in-scope host appears.
    label: Bounty Hub
    link: pentesters/bounty-hub.md
  - view: web
    title: See which web assets belong together
    text: Correlation groups web assets that share a favicon, a certificate, an address, a page title or a rendered page, so you can reach every copy of an application from any one of them.
    label: Correlation
    link: pentesters/correlation.md
  - view: services
    title: Find the AI services you are exposing
    text: AI detection identifies model servers, AI gateways, AI applications and MCP servers among your services, and marks the ones that list their models without authentication.
    label: AI detection
    link: pentesters/ai-detection.md
  - view: vulns
    title: Decide what to fix first
    text: Every finding carries its EPSS score, its CISA KEV status, an exploitation rank from 0 to 100 and the strength of its evidence, so you can order the work with the facts in front of you.
    label: Exploit intelligence
    link: pentesters/exploit-intelligence.md
  - view: secrets
    title: Find exposed keys and tokens
    text: Secret mining reads the responses reNgine has already stored and reports the API keys, tokens and credentials in them. No traffic is sent to the target.
    label: Secret mining
    link: pentesters/secret-mining.md
  - view: query
    title: Search every layer the same way
    text: One query language covers all seven result types. Each table has its own fields and flags, and a query you write in the interface runs unchanged through the HTTP API and over MCP.
    label: Query language
    link: pentesters/query.md
tour_title: Everyday work
tour_text: Search your results, follow your programs, be told when something changes, and work from Telegram or your AI client.
tour:
  - scene: query
    title: Narrow any table with a query
    text: As you type in any table, reNgine suggests fields, flags and the values your scans have recorded. Combine them with `and`, `or` and `not`, and the table narrows to the matching rows.
    points:
      - text: "`tech:jenkins` keeps the web assets running Jenkins"
      - text: "`is:live` keeps the ones that answer with 2xx or 3xx"
      - text: Each count on screen opens the rows behind it
    label: Query language
    link: pentesters/query.md
  - scene: watch
    title: Be told about new in-scope hosts
    text: When you watch a bug bounty program, reNgine follows the public certificate logs for its scope. When a new in-scope host receives a certificate, reNgine probes it and sends you its status, title, technologies, address and a screenshot.
    points:
      - text: Hosts already known in your project do not raise an alert
      - text: A watch follows certificates from the moment it starts, and the baseline scan covers earlier hosts
      - text: Alerts reach the channels you set up, such as Slack, Telegram or email
    label: Program watches
    link: pentesters/program-watches.md
  - scene: tripwire
    title: Turn a query into an alert
    text: A tripwire is a saved query that reNgine checks after each scan. When new rows match, such as a newly opened remote desktop port, you receive an alert, and the tripwire can start a focused scan on what it found.
    points:
      - text: "Choose when it fires: when rows appear, when a condition becomes true, or on every match"
      - text: Scope it to one target or to all of them
      - text: Appears and Becomes true do not fire on a target's first scan
    label: Tripwires
    link: pentesters/tripwires.md
  - scene: telegram
    title: Work from Telegram
    text: A private Telegram chat paired with your account lets you list targets, read findings and start, pause or cancel scans from your phone. Anything beyond reading asks for your authenticator code first.
    points:
      - text: "{{ counts.chat_commands }} commands, such as `/vulns`, `/changes` and `/scan`"
      - text: The message with your code is deleted as soon as it arrives
      - text: One code confirms the chat for 15 minutes
    label: Remote control over Telegram
    link: pentesters/telegram.md
  - scene: mcp
    title: Give your AI client a view of your attack surface
    text: "Claude, Cursor or any other MCP client connects to reNgine through a key you create. It answers from your scan results, and each key sets how far it can go: read, plan scans, make changes or start scans."
    points:
      - text: "{{ counts.mcp_tools }} tools, from `resolve_target` to `start_scan`"
      - text: The MCP server is off until you start it on the Agents page
      - text: Each key has a project scope and an expiry
    label: MCP server
    link: agents/mcp/connect.md
capabilities_link: pentesters/capabilities.md
burp_link: pentesters/burp-suite.md
capabilities:
  - kind: Integration
    title: Burp Suite connector
    text: Send any finding, web asset or endpoint to Burp Repeater, Intruder or Organizer and test it by hand. The requests you make in Burp return to reNgine as endpoints.
    link: pentesters/burp-suite.md
  - kind: Results
    title: Ask
    text: Ask questions about your scan results in plain language, across every target or within one scan. Answers come back as counted rows, and each number opens the rows behind it.
    link: pentesters/ask.md
  - kind: Agents
    title: MCP server
    text: "Give Claude, Cursor or any other MCP client a view of your attack surface: {{ counts.mcp_tools }} tools, with the permissions of each key set by you, from reading results to starting scans."
    link: agents/mcp/connect.md
  - kind: Results
    title: Query language
    text: Search all seven result types with one syntax, for example `tech:jenkins is:live`. The same query runs in the interface, the HTTP API and over MCP.
    link: pentesters/query.md
  - kind: Bug bounty
    title: Bounty Hub and program watches
    text: Bring your HackerOne and Intigriti programs and their scopes into reNgine, and watch a program to be alerted when a new in-scope host receives a certificate.
    link: pentesters/bounty-hub.md
  - kind: Results
    title: Correlation
    text: Group the web assets that share an address, a certificate, a favicon, a page title or a rendered page, so you can find every copy of an application.
    link: pentesters/correlation.md
  - kind: Results
    title: Compare runs and What's new
    text: "Review what changed between runs: what appeared, what changed and what disappeared, with a feed of new critical and high findings and changed screenshots."
    link: pentesters/compare-runs.md
  - kind: Results
    title: Exploit intelligence
    text: Order your findings with the facts in view. Findings and software CVEs carry EPSS scores, CISA KEV status, NVD data, an exploitation rank from 0 to 100 and the strength of their evidence.
    link: pentesters/exploit-intelligence.md
  - kind: Detection
    title: Secret mining
    text: Find API keys, tokens and credentials in the responses reNgine has already stored. No further traffic is sent to the target.
    link: pentesters/secret-mining.md
  - kind: Scanning
    title: Scan contexts
    text: Scan behind a login. You set authentication headers, scope exclusions, rate limits and a proxy once, and reNgine checks that the session works before the scan starts.
    link: pentesters/scan-contexts.md
  - kind: Scanning
    title: Focused rescans
    text: Re-test a chosen set of assets. Pick up to 5,000 assets from finished scans and run the stages you need, without enumerating the target again.
    link: pentesters/focused-rescans.md
  - kind: Integration
    title: Remote control over Telegram
    text: "Work from a paired Telegram chat with {{ counts.chat_commands }} commands: list targets, start, pause and cancel scans, read findings and run lookups. Anything beyond reading asks for your authenticator code."
    link: pentesters/telegram.md
  - kind: Results
    title: Reports
    text: Produce a report from a scan or a target as PDF, HTML, Markdown or JSON, with your own sections and theme and an optional AI-written narrative.
    link: pentesters/reports.md
  - kind: Integration
    title: Notifications and issue trackers
    text: Receive new results on Slack, Discord, Telegram, Microsoft Teams, email or a webhook, and file findings in Jira, GitHub or GitLab with their status shown back in reNgine.
    link: pentesters/notifications.md
  - kind: Detection
    title: Lookalike domains
    text: "Find registered domains that resemble your targets' domains, including typos, homoglyphs, added words and other TLDs, each with its DNS records, page similarity, registration date and a verdict."
    link: pentesters/lookalike-domains.md
  - kind: Detection
    title: Tripwires
    text: Save a query and receive an alert when a scan produces rows that match it, such as a new admin panel. A tripwire can also start a focused scan on what it found.
    link: pentesters/tripwires.md
  - kind: Detection
    title: AI detection
    text: "Identify the AI services on your attack surface: model servers, AI gateways, AI applications, cloud AI endpoints and MCP servers, with the models they expose."
    link: pentesters/ai-detection.md
  - kind: Detection
    title: Broken link hijacking
    text: Find scripts, frames, stylesheets, images and links on your pages that point at domains that no longer resolve and that someone else could register.
    link: pentesters/broken-links.md
reference:
  - title: Query fields
    count: query_fields
    link: reference/query/index.md
  - title: Query flags
    count: query_flags
    link: reference/query/index.md
  - title: Stages
    count: stages
    link: reference/stages/index.md
  - title: MCP tools
    count: mcp_tools
    link: reference/mcp-tools.md
  - title: HTTP API paths
    count: api_paths
    link: reference/http-api.md
  - title: rengine CLI commands
    count: cli_commands
    link: reference/cli.md
  - title: Installer flags
    count: installer_flags
    link: reference/installer.md
  - title: Configuration variables
    count: env_variables
    link: reference/configuration.md
  - title: Remote control commands
    count: chat_commands
    link: reference/remote-control-commands.md
  - title: Pinned tools
    count: pinned_tools
    link: reference/tool-versions.md
install_link: pentesters/install.md
install_note: The installer checks your server, offers to install Docker if it is missing, writes the configuration and starts reNgine.
install: curl -fsSL https://raw.githubusercontent.com/yogeshojha/rengine/master/install.sh -o install.sh && sudo bash install.sh
---
