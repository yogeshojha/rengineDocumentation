---
title: HTTP API paths
description: "All 379 paths and 444 operations of the reNgine HTTP API, in 58 tags, with the access each operation requires. Use it to find the operation you want to call and check who may call it."
sources:
  - api/app/main.py
  - api/app/api/v1/
  - api/app/api/deps.py
revised: 2026-10-03
generated: scripts/gen_api.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_api.py` writes it from `data/openapi.json` and `data/route-access.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

Every path is relative to the address you open the interface on. The **Access** column tells you what an operation checks before it runs: a signed-in user, an administrator, a connector token, an MCP token, or nothing. To call the API from a script, see [Authentication](../developers/api/authentication.md). For error responses and limits, see [Errors, limits and counts](../developers/api/errors.md).

This is how the operations divide by access.

| Access | Operations |
|---|---|
| Signed-in user | 338 |
| Administrator | 93 |
| Connector token | 7 |
| None | 6 |

## Tags

Each tag below lists its operations, with a summary and the access each one requires. Where a path has its own page, the path links to it. Jump to a tag:

[About](#tag-about), [activity](#tag-activity), [ai](#tag-ai), [api-keys](#tag-api-keys), [ask](#tag-ask), [authentication](#tag-authentication), [bounty programs](#tag-bounty-programs), [bounty reports](#tag-bounty-reports), [connectors](#tag-connectors), [cves](#tag-cves), [dashboard](#tag-dashboard), [Datasets](#tag-datasets), [domain-posture](#tag-domain-posture), [endpoints](#tag-endpoints), [events](#tag-events), [exports](#tag-exports), [Health](#tag-health), [http-assets](#tag-http-assets), [instance-settings](#tag-instance-settings), [interest](#tag-interest), [ips](#tag-ips), [issue-trackers](#tag-issue-trackers), [lookalikes](#tag-lookalikes), [mcp](#tag-mcp), [media](#tag-media), [notes](#tag-notes), [notification-channels](#tag-notification-channels), [notifications](#tag-notifications), [onboarding](#tag-onboarding), [organizations](#tag-organizations), [out-of-band testing](#tag-out-of-band-testing), [ports](#tag-ports), [projects](#tag-projects), [proxies](#tag-proxies), [remote-control](#tag-remote-control), [reports](#tag-reports), [scan-contexts](#tag-scan-contexts), [scan-engines](#tag-scan-engines), [scans](#tag-scans), [schedules](#tag-schedules), [secrets](#tag-secrets), [software](#tag-software), [subdomains](#tag-subdomains), [surface](#tag-surface), [tags](#tag-tags), [targets](#tag-targets), [threat intelligence](#tag-threat-intelligence), [toolbox](#tag-toolbox), [tools/whois](#tag-tools-whois), [tripwires](#tag-tripwires), [two-factor](#tag-two-factor), [untagged](#tag-untagged), [users](#tag-users), [viewdns](#tag-viewdns), [vulnerabilities](#tag-vulnerabilities), [vulnerability templates](#tag-vulnerability-templates), [whats-new](#tag-whats-new), [wordlists](#tag-wordlists)

## About { #tag-about }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/about` | Read About | Signed-in user |

## activity { #tag-activity }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/activity` | List Activity Logs | Signed-in user |

## ai { #tag-ai }

| Method | Path | Summary | Access |
|---|---|---|---|
| `DELETE` | `/api/v1/ai/cache` | Clear Ai Cache | Administrator |
| `GET` | `/api/v1/ai/calls` | Recent Calls | Signed-in user |
| `GET` | `/api/v1/ai/catalog` | Ai Catalog | Signed-in user |
| `GET` | `/api/v1/ai/connections` | List Connections | Signed-in user |
| `POST` | `/api/v1/ai/connections` | Create Connection | Administrator |
| `PATCH` | `/api/v1/ai/connections/{connection_id}` | Update Connection | Administrator |
| `DELETE` | `/api/v1/ai/connections/{connection_id}` | Delete Connection | Administrator |
| `POST` | `/api/v1/ai/connections/{connection_id}/test` | Test Connection | Administrator |
| `POST` | `/api/v1/ai/connections/{connection_id}/use` | Use Connection | Administrator |
| `POST` | `/api/v1/ai/models` | List Models | Administrator |
| `PATCH` | `/api/v1/ai/settings` | Update Ai | Administrator |
| `GET` | `/api/v1/ai/status` | Ai Status | Signed-in user |
| `POST` | `/api/v1/ai/test` | Test Ai | Administrator |

## api-keys { #tag-api-keys }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/api-keys` | List Api Keys | Administrator |
| `POST` | `/api/v1/api-keys` | Create Api Key | Administrator |
| `GET` | `/api/v1/api-keys/providers` | List Providers | Administrator |
| `PATCH` | `/api/v1/api-keys/{key_id}` | Update Api Key | Administrator |
| `DELETE` | `/api/v1/api-keys/{key_id}` | Delete Api Key | Administrator |
| `GET` | `/api/v1/api-keys/{key_id}/reveal` | Reveal Api Key | Administrator |
| `POST` | `/api/v1/api-keys/{key_id}/test` | Test Api Key | Administrator |

## ask { #tag-ask }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/ask/brief/web-asset` | Brief Asset | Signed-in user |
| `GET` | `/api/v1/ask/brief/{vulnerability_id}` | Brief | Signed-in user |
| `GET` | `/api/v1/ask/threads` | List Threads | Signed-in user |
| `POST` | `/api/v1/ask/threads` | Create Thread | Signed-in user |
| `DELETE` | `/api/v1/ask/threads` | Delete Threads | Signed-in user |
| `GET` | `/api/v1/ask/threads/{thread_id}` | Get Thread | Signed-in user |
| `DELETE` | `/api/v1/ask/threads/{thread_id}` | Delete Thread | Signed-in user |
| `POST` | `/api/v1/ask/threads/{thread_id}/messages` | Ask | Signed-in user |

## authentication { #tag-authentication }

| Method | Path | Summary | Access |
|---|---|---|---|
| `POST` | `/api/v1/auth/change-password` | Change Password | Signed-in user |
| `POST` | `/api/v1/auth/change-username` | Change Username | Signed-in user |
| `POST` | `/api/v1/auth/login` | Login | None |
| `POST` | `/api/v1/auth/logout` | Logout | None |
| `GET` | `/api/v1/auth/me` | Get Current User Info | Signed-in user |
| `POST` | `/api/v1/auth/refresh` | Refresh Access Token | None |

## bounty programs { #tag-bounty-programs }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/bounty-programs` | List Programs | Signed-in user |
| `GET` | `/api/v1/bounty-programs/events` | List Events | Signed-in user |
| `POST` | `/api/v1/bounty-programs/events/seen` | Mark Events Seen | Signed-in user |
| `GET` | `/api/v1/bounty-programs/settings` | Read Settings | Signed-in user |
| `PUT` | `/api/v1/bounty-programs/settings` | Write Settings | Administrator |
| `GET` | `/api/v1/bounty-programs/status` | Get Status | Signed-in user |
| `POST` | `/api/v1/bounty-programs/sync` | Sync | Administrator |
| `POST` | `/api/v1/bounty-programs/sync-feed` | Sync Feed | Administrator |
| `GET` | `/api/v1/bounty-programs/vocabulary` | Vocabulary | Signed-in user |
| `GET` | `/api/v1/bounty-programs/watches` | List Watches | Signed-in user |
| `GET` | `/api/v1/bounty-programs/watches/stream` | Stream Status | Signed-in user |
| `POST` | `/api/v1/bounty-programs/watches/validate-query` | Validate Query | Signed-in user |
| `GET` | `/api/v1/bounty-programs/watches/{watch_id}` | Get Watch | Signed-in user |
| `PATCH` | `/api/v1/bounty-programs/watches/{watch_id}` | Update Watch | Signed-in user |
| `DELETE` | `/api/v1/bounty-programs/watches/{watch_id}` | Delete Watch | Signed-in user |
| `GET` | `/api/v1/bounty-programs/watches/{watch_id}/events` | List Watch Events | Signed-in user |
| `GET` | `/api/v1/bounty-programs/watches/{watch_id}/hosts` | List Watch Hosts | Signed-in user |
| `GET` | `/api/v1/bounty-programs/watches/{watch_id}/hosts/counts` | Watch Host Counts | Signed-in user |
| `POST` | `/api/v1/bounty-programs/watches/{watch_id}/hosts/{host_id}/mute` | Mute Watch Host | Signed-in user |
| `POST` | `/api/v1/bounty-programs/watches/{watch_id}/seen` | Mark Watch Seen | Signed-in user |
| `GET` | `/api/v1/bounty-programs/{platform}/{handle}` | Program Detail | Signed-in user |
| `POST` | `/api/v1/bounty-programs/{platform}/{handle}/import` | Import Program | Signed-in user |
| `POST` | `/api/v1/bounty-programs/{platform}/{handle}/sync` | Sync Program | Administrator |
| `POST` | `/api/v1/bounty-programs/{platform}/{handle}/watch` | Create Watch | Signed-in user |
| `GET` | `/api/v1/bounty-programs/{platform}/{handle}/watch/preview` | Watch Preview | Signed-in user |

## bounty reports { #tag-bounty-reports }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/bounty-reports/{platform}` | List Reports | Signed-in user |
| `GET` | `/api/v1/bounty-reports/{platform}/counts` | Counts | Signed-in user |
| `GET` | `/api/v1/bounty-reports/{platform}/programs` | Programs | Signed-in user |
| `GET` | `/api/v1/bounty-reports/{platform}/summary` | Summary | Signed-in user |
| `POST` | `/api/v1/bounty-reports/{platform}/sync` | Sync | Administrator |

## connectors { #tag-connectors }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/connectors` | List Connectors | Signed-in user |
| `POST` | `/api/v1/connectors` | Create Connector | Administrator |
| `GET` | `/api/v1/connectors/actions` | Collect Actions | Connector token |
| `GET` | `/api/v1/connectors/catalog` | Catalog | Signed-in user |
| `GET` | `/api/v1/connectors/client/{kind}` | Download Client | Signed-in user |
| `POST` | `/api/v1/connectors/findings` | Report Finding | Connector token |
| `GET` | `/api/v1/connectors/host` | Host Facts | Connector token |
| `POST` | `/api/v1/connectors/ingest` | Ingest | Connector token |
| `GET` | `/api/v1/connectors/notices` | Collect Notices | Connector token |
| `GET` | `/api/v1/connectors/scope` | Target Scope | Connector token |
| `GET` | `/api/v1/connectors/targets` | Picker Targets | Connector token |
| `PATCH` | `/api/v1/connectors/{connector_id}` | Update Connector | Administrator |
| `DELETE` | `/api/v1/connectors/{connector_id}` | Delete Connector | Administrator |
| `GET` | `/api/v1/connectors/{connector_id}/candidates` | Candidates | Signed-in user |
| `POST` | `/api/v1/connectors/{connector_id}/candidates/state` | Set Candidate State | Signed-in user |
| `GET` | `/api/v1/connectors/{connector_id}/discovered` | Discovered | Signed-in user |
| `POST` | `/api/v1/connectors/{connector_id}/discovered/add` | Add Discovered Target | Signed-in user |
| `POST` | `/api/v1/connectors/{connector_id}/discovered/dismiss` | Dismiss Discovered | Signed-in user |
| `POST` | `/api/v1/connectors/{connector_id}/handoff` | Handoff To Proxy | Signed-in user |
| `POST` | `/api/v1/connectors/{connector_id}/rotate` | Rotate Token | Administrator |
| `POST` | `/api/v1/connectors/{connector_id}/scan` | Scan Queue | Signed-in user |

## cves { #tag-cves }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/cves` | List Cves | Signed-in user |
| `GET` | `/api/v1/cves/{cve}` | Cve Exposure | Signed-in user |

## dashboard { #tag-dashboard }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/dashboard/activity` | Dashboard Activity | Signed-in user |
| `GET` | `/api/v1/dashboard/discovery` | Dashboard Discovery | Signed-in user |
| `GET` | `/api/v1/dashboard/overview` | Dashboard Overview | Signed-in user |
| `GET` | `/api/v1/dashboard/programs` | Dashboard Programs | Signed-in user |
| `GET` | `/api/v1/dashboard/readiness` | Dashboard Readiness | Signed-in user |
| `GET` | `/api/v1/dashboard/surface-risk` | Dashboard Surface Risk | Signed-in user |
| `GET` | `/api/v1/dashboard/window` | Dashboard Window | Signed-in user |

## Datasets { #tag-datasets }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/datasets` | List Datasets | Signed-in user |
| `POST` | `/api/v1/datasets/{kind}/sync` | Sync Dataset | Administrator |

## domain-posture { #tag-domain-posture }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/domain-posture` | Domain Posture | Signed-in user |
| `GET` | `/api/v1/domain-posture/project` | Project Domain Posture | Signed-in user |
| `GET` | `/api/v1/domain-posture/target/{target_id}` | Target Domain Posture | Signed-in user |

## endpoints { #tag-endpoints }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/endpoints/coverage` | Endpoint Coverage | Signed-in user |
| `GET` | `/api/v1/endpoints/facets` | Endpoint Facets | Signed-in user |
| `POST` | `/api/v1/endpoints/gone` | Endpoint Gone | Signed-in user |
| `GET` | `/api/v1/endpoints/host` | Endpoint Host Brief | Signed-in user |
| `POST` | [`/api/v1/endpoints/search`](../developers/api/search-endpoints.md) | Search Endpoints | Signed-in user |
| `POST` | `/api/v1/endpoints/search/groups` | Endpoint Groups | Signed-in user |
| `POST` | `/api/v1/endpoints/search/leads` | Endpoint Leads | Signed-in user |
| `POST` | `/api/v1/endpoints/search/tabs` | Endpoint Tabs | Signed-in user |
| `GET` | `/api/v1/endpoints/structure` | Endpoint Structure | Signed-in user |
| `GET` | `/api/v1/endpoints/summary` | Endpoint Summary | Signed-in user |
| `POST` | `/api/v1/endpoints/tree` | Endpoint Tree | Signed-in user |
| `POST` | `/api/v1/endpoints/tree/hosts` | Endpoint Tree Hosts | Signed-in user |
| `POST` | `/api/v1/endpoints/tree/leaves` | Endpoint Tree Leaves | Signed-in user |
| `POST` | `/api/v1/endpoints/verify` | Endpoint Verify Branch | Signed-in user |
| `GET` | `/api/v1/endpoints/{endpoint_id}` | Get Endpoint | Signed-in user |

## events { #tag-events }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/events/stream` | Event Stream | Signed-in user |

## exports { #tag-exports }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/exports` | List Exports | Signed-in user |
| `POST` | [`/api/v1/exports`](../developers/api/export.md) | Create Export | Signed-in user |
| `GET` | `/api/v1/exports/{export_id}` | Get Export | Signed-in user |
| `DELETE` | `/api/v1/exports/{export_id}` | Delete Export | Signed-in user |
| `GET` | `/api/v1/exports/{export_id}/download` | Download Export | Signed-in user |
| `POST` | `/api/v1/exports/{export_id}/rerun` | Rerun Export | Signed-in user |

## Health { #tag-health }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/health/health` | Health Check | None |
| `GET` | `/api/v1/health/queues` | Queue Health | Administrator |

## http-assets { #tag-http-assets }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/http-assets/{asset_id}` | Get Http Asset | Signed-in user |

## instance-settings { #tag-instance-settings }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/instance-settings` | Get Instance Settings | Signed-in user |
| `PATCH` | `/api/v1/instance-settings` | Update Instance Settings | Administrator |

## interest { #tag-interest }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/interest/catalog` | Get Catalog | Signed-in user |
| `POST` | `/api/v1/interest/dismiss` | Dismiss | Signed-in user |
| `POST` | `/api/v1/interest/dismiss/bulk` | Dismiss Many | Signed-in user |
| `GET` | `/api/v1/interest/dismissals` | List Dismissals | Signed-in user |
| `DELETE` | `/api/v1/interest/dismissals/{dismissal_id}` | Restore Dismissal | Signed-in user |
| `POST` | `/api/v1/interest/project` | Project Interest | Signed-in user |
| `GET` | `/api/v1/interest/rules` | List Rules | Signed-in user |
| `POST` | `/api/v1/interest/rules` | Create Rule | Signed-in user |
| `POST` | `/api/v1/interest/rules/preview` | Preview Rule | Signed-in user |
| `PATCH` | `/api/v1/interest/rules/{rule_id}` | Update Rule | Signed-in user |
| `DELETE` | `/api/v1/interest/rules/{rule_id}` | Delete Rule | Signed-in user |
| `POST` | `/api/v1/interest/scan/{scan_id}` | Scan Interest | Signed-in user |
| `POST` | `/api/v1/interest/scan/{scan_id}/judge` | Judge Scan | Signed-in user |
| `POST` | `/api/v1/interest/scan/{scan_id}/suggestions` | Rule Suggestions | Signed-in user |

## ips { #tag-ips }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/ips/facets` | Ip Facets | Signed-in user |
| `POST` | [`/api/v1/ips/search`](../developers/api/search-ips.md) | Ip Search | Signed-in user |
| `POST` | `/api/v1/ips/search/groups` | Ip Search Groups | Signed-in user |
| `POST` | `/api/v1/ips/search/leads` | Ip Search Leads | Signed-in user |
| `POST` | `/api/v1/ips/search/tabs` | Ip Search Tabs | Signed-in user |

## issue-trackers { #tag-issue-trackers }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/issue-trackers` | List Trackers | Signed-in user |
| `POST` | `/api/v1/issue-trackers` | Create Tracker | Administrator |
| `GET` | `/api/v1/issue-trackers/issues` | List Issues | Signed-in user |
| `POST` | `/api/v1/issue-trackers/issues` | File Issues | Signed-in user |
| `POST` | `/api/v1/issue-trackers/issues/plan` | Plan Issues | Signed-in user |
| `DELETE` | `/api/v1/issue-trackers/issues/{issue_id}` | Unlink Issue | Signed-in user |
| `POST` | `/api/v1/issue-trackers/issues/{issue_id}/refresh` | Refresh Issue | Signed-in user |
| `POST` | `/api/v1/issue-trackers/issues/{issue_id}/retry` | Retry Issue | Signed-in user |
| `GET` | `/api/v1/issue-trackers/routes` | List Routes | Signed-in user |
| `PUT` | `/api/v1/issue-trackers/routes` | Set Route | Administrator |
| `DELETE` | `/api/v1/issue-trackers/routes/{route_id}` | Delete Route | Administrator |
| `POST` | `/api/v1/issue-trackers/test` | Test Tracker Config | Administrator |
| `PATCH` | `/api/v1/issue-trackers/{tracker_id}` | Update Tracker | Administrator |
| `DELETE` | `/api/v1/issue-trackers/{tracker_id}` | Delete Tracker | Administrator |
| `GET` | `/api/v1/issue-trackers/{tracker_id}/destinations` | Tracker Destinations | Administrator |
| `GET` | `/api/v1/issue-trackers/{tracker_id}/issue-types` | Tracker Issue Types | Administrator |
| `POST` | `/api/v1/issue-trackers/{tracker_id}/test` | Test Tracker | Administrator |

## lookalikes { #tag-lookalikes }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/lookalikes` | Scan Lookalikes | Signed-in user |
| `GET` | `/api/v1/lookalikes/target/{target_id}` | Target Lookalikes | Signed-in user |
| `PATCH` | `/api/v1/lookalikes/triage` | Triage Lookalikes | Signed-in user |

## mcp { #tag-mcp }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/mcp/calls` | Mcp Calls | Administrator |
| `PATCH` | `/api/v1/mcp/settings` | Update Mcp | Administrator |
| `GET` | `/api/v1/mcp/status` | Mcp Status | Signed-in user |
| `GET` | `/api/v1/mcp/tokens` | Mcp Tokens | Administrator |
| `POST` | `/api/v1/mcp/tokens` | Create Mcp Token | Administrator |
| `PATCH` | `/api/v1/mcp/tokens/{token_id}` | Update Mcp Token | Administrator |
| `DELETE` | `/api/v1/mcp/tokens/{token_id}` | Delete Mcp Token | Administrator |
| `POST` | `/api/v1/mcp/tokens/{token_id}/revoke` | Revoke Mcp Token | Administrator |
| `GET` | `/api/v1/mcp/tools` | Mcp Tools | Signed-in user |

## media { #tag-media }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/media/screenshot` | Get Screenshot | Signed-in user |

## notes { #tag-notes }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/notes` | List Notes | Signed-in user |
| `POST` | `/api/v1/notes` | Create Note | Signed-in user |
| `GET` | `/api/v1/notes/facets` | Note Facets | Signed-in user |
| `GET` | `/api/v1/notes/tags` | List Note Tags | Signed-in user |
| `GET` | `/api/v1/notes/{note_id}` | Get Note | Signed-in user |
| `PATCH` | `/api/v1/notes/{note_id}` | Update Note | Signed-in user |
| `DELETE` | `/api/v1/notes/{note_id}` | Delete Note | Signed-in user |

## notification-channels { #tag-notification-channels }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/notification-channels` | List Channels | Administrator |
| `POST` | `/api/v1/notification-channels` | Create Channel | Administrator |
| `POST` | `/api/v1/notification-channels/test` | Test Channel Config | Administrator |
| `PATCH` | `/api/v1/notification-channels/{id}` | Update Channel | Administrator |
| `DELETE` | `/api/v1/notification-channels/{id}` | Delete Channel | Administrator |
| `POST` | `/api/v1/notification-channels/{id}/test` | Test Channel | Administrator |

## notifications { #tag-notifications }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/notifications` | List Notifications | Signed-in user |
| `DELETE` | `/api/v1/notifications` | Clear All Notifications | Signed-in user |
| `POST` | `/api/v1/notifications/read-all` | Mark All Notifications As Read | Signed-in user |
| `GET` | `/api/v1/notifications/stats` | Get Notification Stats | Signed-in user |
| `DELETE` | `/api/v1/notifications/{notification_id}` | Delete Notification | Signed-in user |
| `PATCH` | `/api/v1/notifications/{notification_id}/read` | Mark Notification As Read | Signed-in user |

## onboarding { #tag-onboarding }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/onboarding/ai` | Get Ai Step | Administrator |
| `PUT` | `/api/v1/onboarding/ai` | Save Ai Step | Administrator |
| `POST` | `/api/v1/onboarding/complete` | Complete Onboarding | Administrator |
| `PATCH` | `/api/v1/onboarding/progress` | Update Progress | Administrator |
| `GET` | `/api/v1/onboarding/status` | Get Status | Signed-in user |

## organizations { #tag-organizations }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/organizations` | List Organizations | Signed-in user |
| `POST` | `/api/v1/organizations` | Create Organization | Signed-in user |
| `PATCH` | `/api/v1/organizations/{organization_id}` | Update Organization | Signed-in user |
| `DELETE` | `/api/v1/organizations/{organization_id}` | Delete Organization | Signed-in user |

## out-of-band testing { #tag-out-of-band-testing }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/oast` | Read Oast | Signed-in user |
| `PATCH` | `/api/v1/oast` | Update Oast | Administrator |
| `POST` | `/api/v1/oast/reset` | Reset Oast | Administrator |
| `POST` | `/api/v1/oast/test` | Test Oast | Administrator |

## ports { #tag-ports }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/ports/ai` | Service Ai | Signed-in user |
| `GET` | `/api/v1/ports/exposure` | Scan Exposure | Signed-in user |
| `GET` | `/api/v1/ports/facets` | Service Facets | Signed-in user |
| `GET` | `/api/v1/ports/origins` | Origin Exposure | Signed-in user |
| `POST` | [`/api/v1/ports/search`](../developers/api/search-services.md) | Search Services | Signed-in user |
| `POST` | `/api/v1/ports/search/groups` | Service Groups | Signed-in user |
| `POST` | `/api/v1/ports/search/leads` | Service Leads | Signed-in user |
| `POST` | `/api/v1/ports/search/tabs` | Service Tabs | Signed-in user |

## projects { #tag-projects }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/projects` | List Projects | Signed-in user |
| `POST` | `/api/v1/projects` | Create Project | Administrator |

## proxies { #tag-proxies }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/proxies` | List Proxies | Administrator |
| `POST` | `/api/v1/proxies` | Create Proxy | Administrator |
| `PATCH` | `/api/v1/proxies/{id}` | Update Proxy | Administrator |
| `DELETE` | `/api/v1/proxies/{id}` | Delete Proxy | Administrator |
| `POST` | `/api/v1/proxies/{id}/set-default` | Set Default Proxy | Administrator |
| `POST` | `/api/v1/proxies/{id}/test` | Test Proxy | Administrator |

## remote-control { #tag-remote-control }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/remote-control/channels/{channel}/calls` | List Calls | Administrator |
| `GET` | `/api/v1/remote-control/channels/{channel}/chats` | List Chats | Administrator |
| `PATCH` | `/api/v1/remote-control/channels/{channel}/chats/{chat_id}` | Update Chat | Administrator |
| `DELETE` | `/api/v1/remote-control/channels/{channel}/chats/{chat_id}` | Delete Chat | Administrator |
| `POST` | `/api/v1/remote-control/channels/{channel}/chats/{chat_id}/revoke` | Revoke Chat | Administrator |
| `GET` | `/api/v1/remote-control/channels/{channel}/commands` | List Commands | Signed-in user |
| `POST` | `/api/v1/remote-control/channels/{channel}/connect` | Connect Channel | Administrator |
| `POST` | `/api/v1/remote-control/channels/{channel}/disconnect` | Disconnect Channel | Administrator |
| `GET` | `/api/v1/remote-control/channels/{channel}/pending` | Pending Pairings | Administrator |
| `POST` | `/api/v1/remote-control/channels/{channel}/pending/{code}/approve` | Approve Pairing | Administrator |
| `POST` | `/api/v1/remote-control/channels/{channel}/pending/{code}/block` | Block Pairing | Administrator |
| `PATCH` | `/api/v1/remote-control/channels/{channel}/settings` | Update Channel | Administrator |
| `GET` | `/api/v1/remote-control/channels/{channel}/status` | Channel Status | Signed-in user |

## reports { #tag-reports }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/reports` | List Reports | Signed-in user |
| `POST` | `/api/v1/reports` | Create Report | Signed-in user |
| `GET` | `/api/v1/reports/catalog` | Report Catalog | Signed-in user |
| `GET` | `/api/v1/reports/defaults` | Report Defaults | Signed-in user |
| `PUT` | `/api/v1/reports/defaults` | Set Report Defaults | Administrator |
| `POST` | `/api/v1/reports/estimate` | Estimate Report | Signed-in user |
| `POST` | `/api/v1/reports/fonts` | Upload Font | Administrator |
| `DELETE` | `/api/v1/reports/fonts/{slug}` | Delete Font | Administrator |
| `GET` | `/api/v1/reports/templates` | List Templates | Signed-in user |
| `POST` | `/api/v1/reports/templates` | Create Template | Signed-in user |
| `PATCH` | `/api/v1/reports/templates/{template_id}` | Update Template | Signed-in user |
| `DELETE` | `/api/v1/reports/templates/{template_id}` | Delete Template | Signed-in user |
| `POST` | `/api/v1/reports/themes` | Upload Theme | Administrator |
| `DELETE` | `/api/v1/reports/themes/{slug}` | Delete Theme | Administrator |
| `GET` | `/api/v1/reports/themes/{slug}/source` | Theme Source | Signed-in user |
| `GET` | `/api/v1/reports/{report_id}` | Get Report | Signed-in user |
| `DELETE` | `/api/v1/reports/{report_id}` | Delete Report | Signed-in user |
| `GET` | `/api/v1/reports/{report_id}/download` | Download Report | Signed-in user |
| `GET` | `/api/v1/reports/{report_id}/preview` | Preview Report | Signed-in user |
| `POST` | `/api/v1/reports/{report_id}/retry` | Retry Report | Signed-in user |

## scan-contexts { #tag-scan-contexts }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/contexts` | List Contexts | Signed-in user |
| `POST` | `/api/v1/contexts` | Create Context | Signed-in user |
| `GET` | `/api/v1/contexts/{id}` | Get Context | Signed-in user |
| `PATCH` | `/api/v1/contexts/{id}` | Update Context | Signed-in user |
| `DELETE` | `/api/v1/contexts/{id}` | Delete Context | Signed-in user |
| `POST` | `/api/v1/contexts/{id}/duplicate` | Duplicate Context | Signed-in user |

## scan-engines { #tag-scan-engines }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/engines` | List Engines | Signed-in user |
| `POST` | `/api/v1/engines` | Create Engine | Signed-in user |
| `GET` | `/api/v1/engines/catalog` | Engine Catalog | Signed-in user |
| `POST` | `/api/v1/engines/import` | Import Engine | Signed-in user |
| `POST` | `/api/v1/engines/preview` | Preview Engine Stages | Signed-in user |
| `GET` | `/api/v1/engines/{id}` | Get Engine | Signed-in user |
| `PATCH` | `/api/v1/engines/{id}` | Update Engine | Signed-in user |
| `DELETE` | `/api/v1/engines/{id}` | Delete Engine | Signed-in user |
| `POST` | `/api/v1/engines/{id}/duplicate` | Duplicate Engine | Signed-in user |
| `GET` | `/api/v1/engines/{id}/export` | Export Engine | Signed-in user |

## scans { #tag-scans }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/scans` | List Scans | Signed-in user |
| `POST` | [`/api/v1/scans/batch`](../developers/api/start-scan.md) | Create Scans | Signed-in user |
| `POST` | `/api/v1/scans/cancel-all` | Cancel All Scans | Signed-in user |
| `GET` | [`/api/v1/scans/compare`](../developers/api/compare-runs.md) | Compare Scans | Signed-in user |
| `GET` | `/api/v1/scans/compare/diff` | Compare Scan Diff | Signed-in user |
| `GET` | `/api/v1/scans/compare/rows` | Compare Scan Rows | Signed-in user |
| `GET` | `/api/v1/scans/daily` | Daily Runs | Signed-in user |
| `GET` | `/api/v1/scans/latest` | Latest Runs | Signed-in user |
| `POST` | `/api/v1/scans/preview` | Preview Scan | Signed-in user |
| `POST` | `/api/v1/scans/rescan` | Rescan Assets | Signed-in user |
| `POST` | `/api/v1/scans/rescan/preview` | Rescan Preview | Signed-in user |
| `GET` | `/api/v1/scans/rescan/schema` | Rescan Vocabulary | Signed-in user |
| `GET` | `/api/v1/scans/stats` | Scan Stats | Signed-in user |
| `GET` | `/api/v1/scans/trends` | Finding Trends | Signed-in user |
| `GET` | [`/api/v1/scans/{id}`](../developers/api/get-scan.md) | Get Scan | Signed-in user |
| `DELETE` | `/api/v1/scans/{id}` | Delete Scan | Signed-in user |
| `GET` | `/api/v1/scans/{id}/activities` | List Scan Activities | Signed-in user |
| `POST` | `/api/v1/scans/{id}/cancel` | Cancel Scan | Signed-in user |
| `GET` | `/api/v1/scans/{id}/commands` | List Scan Commands | Signed-in user |
| `GET` | `/api/v1/scans/{id}/commands/{command_id}` | Get Scan Command | Signed-in user |
| `GET` | `/api/v1/scans/{id}/comparable` | Comparable Runs | Signed-in user |
| `POST` | `/api/v1/scans/{id}/pause` | Pause Scan | Signed-in user |
| `POST` | `/api/v1/scans/{id}/resume` | Resume Scan | Signed-in user |
| `GET` | `/api/v1/scans/{scan_id}/rechecks` | Scan Rechecks | Signed-in user |

## schedules { #tag-schedules }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/schedules` | List Schedules | Signed-in user |
| `POST` | `/api/v1/schedules` | Create Schedule | Signed-in user |
| `PATCH` | `/api/v1/schedules/{id}` | Update Schedule | Signed-in user |
| `DELETE` | `/api/v1/schedules/{id}` | Delete Schedule | Signed-in user |
| `POST` | `/api/v1/schedules/{id}/pause` | Pause Schedule | Signed-in user |
| `POST` | `/api/v1/schedules/{id}/resume` | Resume Schedule | Signed-in user |
| `POST` | `/api/v1/schedules/{id}/run-now` | Run Schedule Now | Signed-in user |

## secrets { #tag-secrets }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/secrets/coverage` | Secret Coverage | Signed-in user |
| `GET` | `/api/v1/secrets/facets` | Secret Facets | Signed-in user |
| `POST` | [`/api/v1/secrets/search`](../developers/api/search-secrets.md) | Search Secrets | Signed-in user |
| `POST` | `/api/v1/secrets/search/counts` | Secret Search Counts | Signed-in user |
| `POST` | `/api/v1/secrets/search/groups` | Secret Groups | Signed-in user |
| `GET` | `/api/v1/secrets/{secret_id}` | Get Secret | Signed-in user |

## software { #tag-software }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/software/coverage` | Software Coverage | Signed-in user |
| `GET` | `/api/v1/software/facets` | Software Facets | Signed-in user |
| `POST` | [`/api/v1/software/search`](../developers/api/search-software.md) | Search Software | Signed-in user |
| `POST` | `/api/v1/software/search/counts` | Software Search Counts | Signed-in user |

## subdomains { #tag-subdomains }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/subdomains/correlation` | Subdomain Correlation | Signed-in user |
| `GET` | `/api/v1/subdomains/correlation-graph` | Subdomain Correlation Graph | Signed-in user |
| `GET` | `/api/v1/subdomains/facets` | Subdomain Facets | Signed-in user |
| `GET` | `/api/v1/subdomains/hosting` | Subdomain Hosting | Signed-in user |
| `GET` | `/api/v1/subdomains/hygiene` | Subdomain Hygiene | Signed-in user |
| `GET` | `/api/v1/subdomains/insights` | Subdomain Insights | Signed-in user |
| `GET` | `/api/v1/subdomains/posture` | Subdomain Posture | Signed-in user |
| `POST` | [`/api/v1/subdomains/search`](../developers/api/search-web-assets.md) | Search Subdomains | Signed-in user |
| `POST` | `/api/v1/subdomains/search/counts` | Subdomain Search Counts | Signed-in user |
| `POST` | `/api/v1/subdomains/search/groups` | Subdomain Search Groups | Signed-in user |
| `POST` | `/api/v1/subdomains/search/leads` | Subdomain Search Leads | Signed-in user |
| `POST` | `/api/v1/subdomains/search/renders` | Subdomain Search Renders | Signed-in user |
| `POST` | `/api/v1/subdomains/search/tabs` | Subdomain Search Tabs | Signed-in user |
| `GET` | `/api/v1/subdomains/tech` | Subdomain Tech | Signed-in user |

## surface { #tag-surface }

| Method | Path | Summary | Access |
|---|---|---|---|
| `POST` | `/api/v1/surface/delete` | Delete Rows | Signed-in user |
| `GET` | `/api/v1/surface/overview` | Surface Overview | Signed-in user |
| `GET` | `/api/v1/surface/schemas` | Surface Schemas | Signed-in user |

## tags { #tag-tags }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/tags` | List Tags | Signed-in user |
| `POST` | `/api/v1/tags` | Create Tag | Signed-in user |
| `PATCH` | `/api/v1/tags/{tag_id}` | Update Tag | Signed-in user |
| `DELETE` | `/api/v1/tags/{tag_id}` | Delete Tag | Signed-in user |

## targets { #tag-targets }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/targets` | List Targets | Signed-in user |
| `POST` | [`/api/v1/targets`](../developers/api/create-target.md) | Create Target | Signed-in user |
| `POST` | `/api/v1/targets/bulk` | Bulk Create Targets | Signed-in user |
| `GET` | `/api/v1/targets/counts` | Get Target Counts | Signed-in user |
| `POST` | `/api/v1/targets/enrich/bulk` | Bulk Enrich Targets | Signed-in user |
| `GET` | `/api/v1/targets/estate` | Get Project Estate | Signed-in user |
| `PATCH` | `/api/v1/targets/estate/triage` | Triage Estate | Signed-in user |
| `GET` | `/api/v1/targets/ids` | List Matching Target Ids | Signed-in user |
| `POST` | `/api/v1/targets/import/csv` | Import Targets Csv | Signed-in user |
| `POST` | `/api/v1/targets/import/json` | Import Targets Json | Signed-in user |
| `POST` | `/api/v1/targets/organizations/bulk` | Bulk Add Organizations | Signed-in user |
| `GET` | `/api/v1/targets/search` | Search Targets By Value | Signed-in user |
| `GET` | `/api/v1/targets/stats` | Get Target Stats | Signed-in user |
| `POST` | `/api/v1/targets/tags/bulk` | Bulk Add Tags | Signed-in user |
| `POST` | `/api/v1/targets/validate` | Validate Target Endpoint | Signed-in user |
| `POST` | `/api/v1/targets/validate/batch` | Validate Target Batch | Signed-in user |
| `GET` | `/api/v1/targets/{target_id}` | Get Target | Signed-in user |
| `PATCH` | `/api/v1/targets/{target_id}` | Update Target | Signed-in user |
| `DELETE` | `/api/v1/targets/{target_id}` | Delete Target | Signed-in user |
| `POST` | `/api/v1/targets/{target_id}/assets` | Search Target Assets | Signed-in user |
| `GET` | `/api/v1/targets/{target_id}/bgp` | Get Target Bgp | Signed-in user |
| `POST` | `/api/v1/targets/{target_id}/bgp/refresh` | Refresh Target Bgp | Signed-in user |
| `GET` | `/api/v1/targets/{target_id}/detail` | Get Target Detail | Signed-in user |
| `GET` | `/api/v1/targets/{target_id}/dns` | Get Target Dns | Signed-in user |
| `POST` | `/api/v1/targets/{target_id}/dns/refresh` | Refresh Target Dns | Signed-in user |
| `GET` | `/api/v1/targets/{target_id}/estate` | Get Target Estate | Signed-in user |
| `GET` | `/api/v1/targets/{target_id}/infostealer` | Get Target Infostealer | Signed-in user |
| `POST` | `/api/v1/targets/{target_id}/infostealer/refresh` | Refresh Target Infostealer | Signed-in user |
| `GET` | `/api/v1/targets/{target_id}/programs` | Get Target Programs | Signed-in user |
| `GET` | `/api/v1/targets/{target_id}/relations` | Get Target Relations | Signed-in user |
| `GET` | `/api/v1/targets/{target_id}/seeds` | List Target Seeds | Signed-in user |
| `PUT` | `/api/v1/targets/{target_id}/seeds` | Write Target Seeds | Signed-in user |
| `DELETE` | `/api/v1/targets/{target_id}/seeds/{seed_id}` | Delete Target Seed | Signed-in user |
| `GET` | `/api/v1/targets/{target_id}/summary` | Get Target Summary | Signed-in user |
| `POST` | `/api/v1/targets/{target_id}/whois/refresh` | Refresh Target Whois | Signed-in user |

## threat intelligence { #tag-threat-intelligence }

| Method | Path | Summary | Access |
|---|---|---|---|
| `PUT` | `/api/v1/threat-intel/auto-sync` | Set Auto Sync | Administrator |
| `GET` | `/api/v1/threat-intel/changes` | Changes | Signed-in user |
| `GET` | `/api/v1/threat-intel/finding/{vulnerability_id}` | Finding | Signed-in user |
| `GET` | `/api/v1/threat-intel/signal/{kind}` | Signal Findings | Signed-in user |
| `GET` | `/api/v1/threat-intel/status` | Status | Signed-in user |
| `POST` | `/api/v1/threat-intel/sync` | Sync | Administrator |

## toolbox { #tag-toolbox }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/toolbox/catalog` | Toolbox Catalog | Signed-in user |
| `POST` | `/api/v1/toolbox/run` | Run Tool | Signed-in user |
| `GET` | `/api/v1/toolbox/runs` | Toolbox Runs | Signed-in user |
| `DELETE` | `/api/v1/toolbox/runs` | Clear Toolbox Runs | Signed-in user |
| `GET` | `/api/v1/toolbox/runs/{run_id}` | Toolbox Run | Signed-in user |

## tools/whois { #tag-tools-whois }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/tools/whois/correlations/nameserver` | Find by nameserver | Signed-in user |
| `GET` | `/api/v1/tools/whois/correlations/network` | Find by network | Signed-in user |
| `GET` | `/api/v1/tools/whois/correlations/registrant` | Find by registrant | Signed-in user |
| `GET` | `/api/v1/tools/whois/correlations/registrar` | Find by registrar | Signed-in user |
| `GET` | `/api/v1/tools/whois/correlations/target/{target_id}` | Target correlations | Signed-in user |
| `GET` | `/api/v1/tools/whois/correlations/targets` | Correlations for several targets | Signed-in user |
| `GET` | `/api/v1/tools/whois/records/{record_id}` | Get WHOIS record | Signed-in user |
| `POST` | `/api/v1/tools/whois/records/{record_id}/refresh` | Refresh WHOIS record | Signed-in user |

## tripwires { #tag-tripwires }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/tripwires` | List Tripwires | Signed-in user |
| `POST` | `/api/v1/tripwires` | Create Tripwire | Signed-in user |
| `POST` | `/api/v1/tripwires/backtest` | Backtest Tripwire | Signed-in user |
| `GET` | `/api/v1/tripwires/catalog` | Tripwire Catalog | Signed-in user |
| `POST` | `/api/v1/tripwires/preview` | Preview Tripwire | Signed-in user |
| `GET` | `/api/v1/tripwires/runs/{run_id}` | Get Run | Signed-in user |
| `PATCH` | `/api/v1/tripwires/{tripwire_id}` | Update Tripwire | Signed-in user |
| `DELETE` | `/api/v1/tripwires/{tripwire_id}` | Delete Tripwire | Signed-in user |
| `GET` | `/api/v1/tripwires/{tripwire_id}/runs` | List Runs | Signed-in user |
| `GET` | `/api/v1/tripwires/{tripwire_id}/runs/counts` | Run Counts | Signed-in user |

## two-factor { #tag-two-factor }

| Method | Path | Summary | Access |
|---|---|---|---|
| `POST` | `/api/v1/auth/2fa/disable` | Disable 2Fa | Signed-in user |
| `POST` | `/api/v1/auth/2fa/login` | Login 2Fa | None |
| `POST` | `/api/v1/auth/2fa/setup` | Setup 2Fa | Signed-in user |
| `GET` | `/api/v1/auth/2fa/status` | Status 2Fa | Signed-in user |
| `POST` | `/api/v1/auth/2fa/verify` | Verify 2Fa | Signed-in user |

## untagged { #tag-untagged }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/` | Root | None |

## users { #tag-users }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/users` | List Users | Administrator |
| `POST` | `/api/v1/users` | Create User | Administrator |
| `PATCH` | `/api/v1/users/{user_id}` | Update User | Administrator |
| `DELETE` | `/api/v1/users/{user_id}` | Delete User | Administrator |
| `GET` | `/api/v1/users/{user_id}/summary` | Get User Summary | Signed-in user |

## viewdns { #tag-viewdns }

| Method | Path | Summary | Access |
|---|---|---|---|
| `POST` | `/api/v1/tools/viewdns/cached-counts` | Cached Counts | Signed-in user |
| `GET` | `/api/v1/tools/viewdns/reverse-ip/{host}` | Reverse Ip | Signed-in user |
| `GET` | `/api/v1/tools/viewdns/reverse-ns/{nameserver}` | Reverse Ns | Signed-in user |
| `GET` | `/api/v1/tools/viewdns/reverse-whois` | Reverse Whois | Signed-in user |

## vulnerabilities { #tag-vulnerabilities }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/vulnerabilities/coverage` | Vulnerability Coverage | Signed-in user |
| `GET` | `/api/v1/vulnerabilities/facets` | Vulnerability Facets | Signed-in user |
| `GET` | `/api/v1/vulnerabilities/overview` | Vulnerability Overview | Signed-in user |
| `POST` | [`/api/v1/vulnerabilities/search`](../developers/api/search-vulnerabilities.md) | Search Vulnerabilities | Signed-in user |
| `POST` | `/api/v1/vulnerabilities/search/groups` | Vulnerability Groups | Signed-in user |
| `POST` | `/api/v1/vulnerabilities/search/issues` | Search Issues | Signed-in user |
| `POST` | `/api/v1/vulnerabilities/search/leads` | Vulnerability Leads | Signed-in user |
| `POST` | `/api/v1/vulnerabilities/search/tabs` | Vulnerability Tabs | Signed-in user |
| `POST` | `/api/v1/vulnerabilities/triage/bulk` | Triage Many | Signed-in user |
| `PATCH` | `/api/v1/vulnerabilities/triage/{fingerprint}` | Triage Vulnerability | Signed-in user |
| `GET` | `/api/v1/vulnerabilities/{vulnerability_id}` | Get Vulnerability | Signed-in user |

## vulnerability templates { #tag-vulnerability-templates }

| Method | Path | Summary | Access |
|---|---|---|---|
| `POST` | `/api/v1/vuln-templates/search` | Search Templates | Signed-in user |
| `POST` | `/api/v1/vuln-templates/seen` | Templates Seen | Signed-in user |
| `POST` | `/api/v1/vuln-templates/selection` | Preview Selection | Signed-in user |
| `GET` | `/api/v1/vuln-templates/stats` | Library Stats | Signed-in user |
| `POST` | `/api/v1/vuln-templates/sync` | Sync Library | Administrator |
| `POST` | `/api/v1/vuln-templates/upload` | Upload Templates | Administrator |
| `PATCH` | `/api/v1/vuln-templates/{template_id}` | Update Template | Administrator |
| `DELETE` | `/api/v1/vuln-templates/{template_id}` | Delete Template | Administrator |
| `GET` | `/api/v1/vuln-templates/{template_id}/source` | Read Source | Signed-in user |
| `PUT` | `/api/v1/vuln-templates/{template_id}/source` | Write Source | Administrator |

## whats-new { #tag-whats-new }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/whats-new` | Whats New | Signed-in user |
| `POST` | `/api/v1/whats-new/seen` | Whats New Seen | Signed-in user |
| `GET` | `/api/v1/whats-new/unseen` | Whats New Unseen | Signed-in user |
| `GET` | `/api/v1/whats-new/visual` | Whats New Visual | Signed-in user |

## wordlists { #tag-wordlists }

| Method | Path | Summary | Access |
|---|---|---|---|
| `GET` | `/api/v1/wordlists` | List Wordlists | Signed-in user |
| `POST` | `/api/v1/wordlists` | Upload Wordlists | Administrator |
| `DELETE` | `/api/v1/wordlists/{wordlist_id}` | Delete Wordlist | Administrator |
| `GET` | `/api/v1/wordlists/{wordlist_id}/preview` | Preview Wordlist | Signed-in user |

