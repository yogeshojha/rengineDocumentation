---
title: Keyboard shortcuts
description: "Work through targets, scans and findings without reaching for the mouse. This page lists the keyboard shortcuts of the reNgine interface, page by page."
sources:
  - frontend/src/routes/(app)/targets/+page.svelte
  - frontend/src/lib/components/scans/scan-history-table.svelte
  - frontend/src/lib/components/scans/results/vulnerabilities-table.svelte
  - frontend/src/lib/config/whats-new.ts
  - "frontend/src/routes/(app)/bounty-hub/[platform]/+page.svelte"
  - frontend/src/lib/components/layout/command-search.svelte
  - frontend/src/lib/components/toolbox/toolbox-menu.svelte
  - frontend/src/lib/components/ui/sidebar/constants.ts
  - frontend/src/lib/components/activity/activity-panel.svelte
  - frontend/src/lib/components/scans/results/query-bar/query-bar.svelte
  - frontend/src/lib/components/scans/results/web-assets-table.svelte
  - frontend/src/lib/components/scans/results/endpoints-table.svelte
  - "frontend/src/routes/(app)/scans/[id]/+page.svelte"
  - "frontend/src/routes/(app)/targets/[id]/+page.svelte"
  - frontend/src/lib/components/scans/results/sheet.ts
  - frontend/src/lib/components/scans/results/vulnerability-detail-sheet.svelte
  - frontend/src/routes/(app)/scans/compare/+page.svelte
  - frontend/src/lib/components/whats-new/visual-compare-dialog.svelte
  - "frontend/src/routes/(app)/automation/engines/[id]/+page.svelte"
  - "frontend/src/routes/(app)/automation/contexts/[id]/+page.svelte"
  - frontend/src/lib/components/scans/launch/launch-dialog.svelte
  - frontend/src/lib/components/notes/note-composer.svelte
  - frontend/src/lib/components/scans/results/endpoints/proxy-request-dialog.svelte
  - frontend/src/lib/components/scans/results/vulnerabilities/ask/ask-composer.svelte
  - frontend/src/lib/components/reports/preview/report-preview-dialog.svelte
revised: 2026-10-03
generated: scripts/gen_shortcuts.py
layout: reference
---

This page is generated from the reNgine 3.0 source. `scripts/gen_shortcuts.py` writes it from `data/repo.json` and `data/shortcuts-extra.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

On macOS, press <kbd>Cmd</kbd> wherever this page says <kbd>Ctrl</kbd>. Single-key shortcuts do not work while you are typing in a text field. Some pages also list their keys in a dialog, which you open with their **Keyboard shortcuts** button or with <kbd>?</kbd>.

## Pages with a shortcut dialog

These pages show the same keys in their own dialog.

### Targets list

| Keys | Action |
|---|---|
| <kbd>j</kbd> or <kbd>k</kbd> | Move between targets |
| <kbd>o</kbd> | Expand or collapse the row |
| <kbd>Enter</kbd> | Open target |
| <kbd>s</kbd> | Scan |
| <kbd>x</kbd> | Select target |
| <kbd>/</kbd> | Search |
| <kbd>Esc</kbd> | Collapse or clear selection |

### Scans list

| Keys | Action |
|---|---|
| <kbd>j</kbd> or <kbd>k</kbd> | Move between runs |
| <kbd>o</kbd> | Expand or collapse the run brief |
| <kbd>1</kbd> to <kbd>4</kbd> | Switch brief tab |
| <kbd>Enter</kbd> | Open results |
| <kbd>x</kbd> | Select run |
| <kbd>c</kbd> | Compare runs |
| <kbd>/</kbd> | Search |
| <kbd>Esc</kbd> | Collapse or clear selection |

### Vulnerabilities table

| Keys | Action |
|---|---|
| <kbd>j</kbd> or <kbd>k</kbd> | Move between findings |
| <kbd>e</kbd> | Expand or collapse the row |
| <kbd>1</kbd> to <kbd>5</kbd> | Switch row tab |
| <kbd>Enter</kbd> | Open finding |
| <kbd>x</kbd> | Select finding |
| <kbd>b</kbd> | Send the open finding to Burp Suite |
| <kbd>o</kbd> or <kbd>c</kbd> or <kbd>f</kbd> or <kbd>a</kbd> | Open, Confirmed, False positive, Risk accepted |
| <kbd>/</kbd> | Search |
| <kbd>Esc</kbd> | Collapse or clear |

### What's new, events

| Keys | Action |
|---|---|
| <kbd>j</kbd> or <kbd>k</kbd> | Move between events |
| <kbd>Enter</kbd> or <kbd>o</kbd> | Expand or collapse the event |
| <kbd>g</kbd> | Go to the run or program |
| <kbd>s</kbd> | Scan the target |
| <kbd>1</kbd> <kbd>2</kbd> | Switch tab |
| <kbd>/</kbd> | Filter |
| <kbd>Esc</kbd> | Collapse or clear selection |

### What's new, visual changes

| Keys | Action |
|---|---|
| <kbd>j</kbd> or <kbd>k</kbd> | Move between changes |
| <kbd>Enter</kbd> | Compare the captures |
| <kbd>s</kbd> | Scan the target |

### Bounty reports

| Keys | Action |
|---|---|
| <kbd>j</kbd> or <kbd>k</kbd> | Move between reports |
| <kbd>o</kbd> | Expand or collapse the report |
| <kbd>p</kbd> | Filter to the report program |
| <kbd>Enter</kbd> | Open the report |
| <kbd>/</kbd> | Search |
| <kbd>?</kbd> | Keyboard shortcuts |
| <kbd>Esc</kbd> | Collapse the report |

## Other shortcuts

These shortcuts have no dialog in the interface, so this page is where you find them.

### Anywhere

| Keys | Action |
|---|---|
| <kbd>Ctrl</kbd>+<kbd>K</kbd> | Open or close the command palette |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>K</kbd> | Open or close the Toolbox |
| <kbd>Ctrl</kbd>+<kbd>B</kbd> | Show or hide the sidebar |
| <kbd>Esc</kbd> | Close the Activity panel when it is open and not pinned |

### Query bar

| Keys | Action |
|---|---|
| <kbd>/</kbd> | Focus the query bar of the table |
| <kbd>Enter</kbd> | Search, or insert the highlighted suggestion |
| <kbd>Up</kbd> or <kbd>Down</kbd> | Choose a suggestion |
| <kbd>Tab</kbd> | Complete a field or a value |
| <kbd>Esc</kbd> | Dismiss the suggestions, or clear the query when none are open |
| <kbd>?</kbd> | Open the syntax guide, in an empty query bar |

### Result tables

| Keys | Action |
|---|---|
| <kbd>j</kbd> or <kbd>k</kbd> or <kbd>Down</kbd> or <kbd>Up</kbd> | Move between rows |
| <kbd>Enter</kbd> | Open the row |
| <kbd>Esc</kbd> | Clear the cursor |
| <kbd>r</kbd> | Rescan the selection, in the web assets table |
| <kbd>[</kbd> or <kbd>]</kbd> | Previous or next host, inside a host in the endpoints table |
| <kbd>Backspace</kbd> | Leave the host, in the endpoints table |
| <kbd>1</kbd> to <kbd>N</kbd> | Switch to the Nth tab of a run page or a target page |

### Detail sheets

| Keys | Action |
|---|---|
| <kbd>j</kbd> or <kbd>Down</kbd> | Next row |
| <kbd>k</kbd> or <kbd>Up</kbd> | Previous row |
| <kbd>1</kbd> to <kbd>9</kbd> | Switch the tab of the finding detail sheet |

### Compare runs

| Keys | Action |
|---|---|
| <kbd>j</kbd> | Open the first change, then the next |
| <kbd>k</kbd> | Previous change |
| <kbd>s</kbd> | Swap the two runs |

### Visual compare

| Keys | Action |
|---|---|
| <kbd>Right</kbd> or <kbd>j</kbd> | Next change |
| <kbd>Left</kbd> or <kbd>k</kbd> | Previous change |
| <kbd>Space</kbd>, held | Show the earlier capture |
| <kbd>1</kbd> or <kbd>2</kbd> or <kbd>3</kbd> | Switch the view mode |

### Editors and dialogs

| Keys | Action |
|---|---|
| <kbd>Ctrl</kbd>+<kbd>S</kbd> | Save, in the scan engine editor and the scan context editor |
| <kbd>Enter</kbd> | Start the scan, in the launch dialog |
| <kbd>Ctrl</kbd>+<kbd>Enter</kbd> | Save a note, or send a request from the proxy request dialog |
| <kbd>Esc</kbd> | Cancel an edit of a note |
| <kbd>Enter</kbd> | Send a message in Ask. Shift+Enter adds a line. |

### Report preview

| Keys | Action |
|---|---|
| <kbd>Right</kbd> or <kbd>PageDown</kbd> | Next page |
| <kbd>Left</kbd> or <kbd>PageUp</kbd> | Previous page |
| <kbd>+</kbd> or <kbd>=</kbd> | Zoom in |
| <kbd>-</kbd> | Zoom out |
| <kbd>Home</kbd> or <kbd>End</kbd> | First or last page |

