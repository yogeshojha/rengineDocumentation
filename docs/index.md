---
template: home.html
title: reNgine 3.0
description: Everything you need to install reNgine, scan your targets, find what matters in the results, and connect reNgine to Burp Suite, your own scripts and your AI agents.
sources:
  - README.md
  - VERSION
revised: 2026-10-03
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
capabilities_link: pentesters/capabilities.md
burp_link: pentesters/burp-suite.md
capabilities:
  - kind: Integration
    title: Burp Suite connector
    text: Send any finding, web asset or endpoint from reNgine to Burp Repeater, Intruder or Organizer and test it by hand. What you browse in Burp comes back to reNgine as endpoints.
    link: pentesters/burp-suite.md
  - kind: Agents
    title: MCP server
    text: "Let Claude, Cursor or any other MCP client ask questions about your attack surface and, if you allow it, start scans. {{ counts.mcp_tools }} tools, with permissions you choose for each token."
    link: agents/mcp/connect.md
  - kind: Results
    title: Query language
    text: Find exactly what you are looking for with one search syntax across all seven result types, for example `tech:jenkins is:live`. Every number on screen opens the rows behind it.
    link: pentesters/query.md
  - kind: Bug bounty
    title: Bounty Hub and program watches
    text: Bring your HackerOne and Intigriti programs and scopes into reNgine, and watch a program to hear about new in-scope domains as soon as their certificates appear.
    link: pentesters/bounty-hub.md
  - kind: Results
    title: Correlation
    text: See which web assets belong together because they share an IP address, a certificate, a favicon, a page title or a rendered page, within a scan and across your targets.
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
    text: Find API keys, tokens and credentials that your targets leak in their responses. reNgine reads the responses it already stored, so this adds no traffic.
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
    text: "Use reNgine from your phone. A paired Telegram chat gives you {{ counts.chat_commands }} commands to list targets, start and stop scans, read findings and run lookups. Anything beyond reading asks for your authenticator code."
    link: pentesters/telegram.md
  - kind: Results
    title: Reports
    text: Turn a scan or a target into a report your client or team can read, as PDF, HTML, Markdown or JSON, with your own sections and theme and an optional AI-written narrative.
    link: pentesters/reports.md
  - kind: Integration
    title: Notifications and issue trackers
    text: Hear about new results on Slack, Discord, Telegram, Microsoft Teams, email or a webhook, and file findings in Jira, GitHub or GitLab with their status shown back in reNgine.
    link: pentesters/notifications.md
  - kind: Detection
    title: Lookalike domains
    text: "Spot domains registered to imitate your targets: typos, homoglyphs, added words and other TLDs, each with its DNS records, page similarity, registration date and a verdict."
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
