---
template: home.html
title: reNgine 3.0
description: Everything you need to install reNgine, scan your targets, find what matters in the results, and connect reNgine to Burp Suite, your own scripts and your AI agents.
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
    text: Install reNgine, run scans and work through the results
    surface: Interface
    link: pentesters/index.md
  - title: Developers
    text: See how reNgine works, use the API and extend it
    surface: HTTP API
    link: developers/index.md
  - title: Agents
    text: Connect AI agents through MCP and give them these docs
    surface: MCP
    link: agents/index.md
run_title: How reNgine works
run_text: Add a target, scan it, search and ask about the results, then act on what you find.
run_label: "reNgine at work: example.com is added and scanned, the web assets are narrowed with tech:jenkins is:live, Ask lists the known exploited findings to fix first, and the first one is alerted on Telegram, sent to Burp Repeater and filed in Jira."
run:
  - scene: target
    title: Add a target
    text: A domain, an IP address, a range, a URL or an ASN. Turn on **Scan after adding** and the scan starts with it.
    label: Projects and targets
    link: pentesters/targets.md
  - scene: scan
    title: Scan it
    text: Stages find names, services, web assets, endpoints and findings, and the counts grow while the scan runs.
    label: Run a scan
    link: pentesters/run-a-scan.md
  - scene: results
    title: Search the results
    text: Seven result types share one query language. `tech:jenkins is:live` narrows 412 web assets to 2.
    label: Query language
    link: pentesters/query.md
  - scene: ask
    title: Ask a question
    text: Ask in plain words. The answer is counted rows, and every number opens the rows behind it.
    label: Ask
    link: pentesters/ask.md
  - scene: act
    title: Act on it
    text: Get the alert, test the request in Burp Repeater and file the issue in Jira.
    label: Burp Suite connector
    link: pentesters/burp-suite.md
layers_title: Your attack surface, layer by layer
layers_text: Work through your attack surface one layer at a time, from the programs you hunt on to the secrets your targets expose.
layers:
  - plane: programs
    title: Import your bug bounty programs
    text: In bug bounty mode, Bounty Hub lists your HackerOne and Intigriti programs with their scope. Add a program's in-scope assets as targets in one step, and watch a program to get an alert when a new in-scope host appears.
    label: Bounty Hub
    link: pentesters/bounty-hub.md
  - plane: web
    title: See which web assets belong together
    text: Correlation shows which web assets share a favicon, a certificate, an address, a page title or a rendered page, so you can find every copy of an application.
    label: Correlation
    link: pentesters/correlation.md
  - plane: services
    title: Find AI services on your attack surface
    text: AI detection finds model servers, AI gateways, AI applications and MCP servers among your services, and shows which ones list their models without authentication.
    label: AI detection
    link: pentesters/ai-detection.md
  - plane: vulns
    title: Decide what to fix first
    text: Exploit intelligence adds the EPSS score, CISA KEV status and an exploitation rank from 0 to 100 to your findings, and shows how strong the evidence is for each one.
    label: Exploit intelligence
    link: pentesters/exploit-intelligence.md
  - plane: secrets
    title: Detect exposed keys and tokens
    text: Secret mining reads the responses reNgine already stored and finds API keys, tokens and credentials in them, without sending any traffic to your targets.
    label: Secret mining
    link: pentesters/secret-mining.md
  - plane: query
    title: Search every layer the same way
    text: One query language works across all seven result types. Each table has its own fields and flags, and the same query works in the interface, the HTTP API and over MCP.
    label: Query language
    link: pentesters/query.md
tour_title: Everyday workflows
tour_text: Search your results, follow your programs, get alerted when something changes, and work from Telegram or your AI client.
tour:
  - scene: query
    title: Narrow any table with a query
    text: Start typing in any table and reNgine suggests fields, flags and the values your scans found. Combine them with `and`, `or` and `not`, and the table narrows to the rows you asked for.
    points:
      - text: "`tech:jenkins` keeps web assets running Jenkins"
      - text: "`is:live` keeps the ones that answer with 2xx or 3xx"
      - text: Every count on screen opens the rows behind it
    label: Query language
    link: pentesters/query.md
  - scene: watch
    title: Get alerts for new in-scope hosts
    text: Watch a bug bounty program and reNgine follows the public certificate logs for its scope. When a new in-scope host gets a certificate, reNgine probes it and alerts you with its status, title, technologies, address and a screenshot.
    points:
      - text: Hosts already known in your project send no alert
      - text: A watch follows certificates from the moment you start it, and the baseline scan covers earlier hosts
      - text: Alerts go to the channels you set up, such as Slack, Telegram or email
    label: Program watches
    link: pentesters/program-watches.md
  - scene: tripwire
    title: Turn any query into an alert
    text: Save any query as a tripwire and reNgine checks it after each scan. When new rows match, such as a newly opened remote desktop port, you get an alert. A tripwire can also start a focused scan on what it found.
    points:
      - text: "Choose when it fires: when rows appear, when a condition becomes true, or on every match"
      - text: Apply it to one target or to all of them
      - text: Appears and Becomes true do not fire on a target's first scan
    label: Tripwires
    link: pentesters/tripwires.md
  - scene: telegram
    title: Run reNgine from Telegram
    text: Pair a private Telegram chat with your account to list targets, read findings and start, pause or cancel scans from your phone. Anything beyond reading asks for your authenticator code first.
    points:
      - text: "{{ counts.chat_commands }} commands, such as `/vulns`, `/changes` and `/scan`"
      - text: Your code message is deleted as soon as it arrives
      - text: One code confirms the chat for 15 minutes
    label: Remote control over Telegram
    link: pentesters/telegram.md
  - scene: mcp
    title: Ask your AI client about your attack surface
    text: "Connect Claude, Cursor or any other MCP client to reNgine. It answers from your scan results through a key you create, and you choose how far each key can go: read, plan scans, make changes or start scans."
    points:
      - text: "{{ counts.mcp_tools }} tools, from `resolve_target` to `start_scan`"
      - text: The MCP server stays off until you start it on the Agents page
      - text: Each key has a project scope and an expiry
    label: MCP server
    link: agents/mcp/connect.md
capabilities_link: pentesters/capabilities.md
burp_link: pentesters/burp-suite.md
capabilities:
  - kind: Integration
    title: Burp Suite connector
    text: Send any finding, web asset or endpoint from reNgine to Burp Repeater, Intruder or Organizer and test it by hand. What you browse in Burp comes back to reNgine as endpoints.
    link: pentesters/burp-suite.md
  - kind: Results
    title: Ask
    text: Ask a question about your scan results in plain words, across every target or one scan. The answer is counted rows, and every number opens the rows behind it.
    link: pentesters/ask.md
  - kind: Agents
    title: MCP server
    text: "Let Claude, Cursor or any other MCP client ask questions about your attack surface and, if you allow it, start scans. {{ counts.mcp_tools }} tools, with permissions you choose for each key."
    link: agents/mcp/connect.md
  - kind: Results
    title: Query language
    text: Search all seven result types with one query syntax, for example `tech:jenkins is:live`. Every number on screen opens the rows behind it.
    link: pentesters/query.md
  - kind: Bug bounty
    title: Bounty Hub and program watches
    text: Bring your HackerOne and Intigriti programs and scopes into reNgine, and watch a program to get an alert when a new in-scope host gets a certificate.
    link: pentesters/bounty-hub.md
  - kind: Results
    title: Correlation
    text: See which web assets belong together because they share an address, a certificate, a favicon, a page title or a rendered page.
    link: pentesters/correlation.md
  - kind: Results
    title: Compare runs and What's new
    text: "See what changed since the last scan: what appeared, what changed and what disappeared, with a feed of new critical and high findings and changed screenshots."
    link: pentesters/compare-runs.md
  - kind: Results
    title: Exploit intelligence
    text: Decide what to fix first. Findings and software CVEs carry EPSS scores, CISA KEV status, NVD data, an exploitation rank from 0 to 100 and how strong the evidence is.
    link: pentesters/exploit-intelligence.md
  - kind: Detection
    title: Secret mining
    text: Find API keys, tokens and credentials exposed in your targets' responses. reNgine reads the responses it already stored, so this adds no traffic.
    link: pentesters/secret-mining.md
  - kind: Scanning
    title: Scan contexts
    text: Scan behind a login. Set authentication headers, scope exclusions, rate limits and a proxy once, and reNgine checks that the session works before the scan starts.
    link: pentesters/scan-contexts.md
  - kind: Scanning
    title: Focused rescans
    text: Re-test only what you care about. Pick up to 5,000 assets from finished scans and run the stages you choose, without enumerating the target again.
    link: pentesters/focused-rescans.md
  - kind: Integration
    title: Remote control over Telegram
    text: "Use reNgine from your phone. A paired Telegram chat gives you {{ counts.chat_commands }} commands to list targets, start, pause and cancel scans, read findings and run lookups. Anything beyond reading asks for your authenticator code."
    link: pentesters/telegram.md
  - kind: Results
    title: Reports
    text: Turn a scan or a target into a report your client or team can read, as PDF, HTML, Markdown or JSON, with your own sections and theme and an optional AI-written narrative.
    link: pentesters/reports.md
  - kind: Integration
    title: Notifications and issue trackers
    text: Get new results on Slack, Discord, Telegram, Microsoft Teams, email or a webhook, and file findings in Jira, GitHub or GitLab with their status shown back in reNgine.
    link: pentesters/notifications.md
  - kind: Detection
    title: Lookalike domains
    text: "Find registered domains that look like your targets' domains: typos, homoglyphs, added words and other TLDs, each with its DNS records, page similarity, registration date and a verdict."
    link: pentesters/lookalike-domains.md
  - kind: Detection
    title: Tripwires
    text: Save a query and get alerted when a scan finds something that matches it, such as a new admin panel. A tripwire can also start a focused scan on what it found.
    link: pentesters/tripwires.md
  - kind: Detection
    title: AI detection
    text: "Find AI on your attack surface: model servers, AI gateways, AI applications, cloud AI endpoints and MCP servers, with the models they expose."
    link: pentesters/ai-detection.md
  - kind: Detection
    title: Broken link hijacking
    text: Find scripts, frames, stylesheets, images and links on your pages that point at domains that no longer resolve, which someone else could register and take over.
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
