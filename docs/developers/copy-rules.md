---
title: Product copy rules
description: Write interface text, backend messages and code comments the way the reNgine product expects. Tests in CI check part of these rules, so a string that breaks a checked rule fails your pull request.
sources:
  - frontend/src/lib/voice.test.ts
  - frontend/src/lib/glossary.test.ts
  - frontend/src/lib/skeleton.test.ts
  - frontend/src/lib/test-utils/source-files.ts
  - frontend/src/lib/api/client.ts
revised: 2026-10-03
---

These rules are for the reNgine product itself: what people read in the interface, the messages the api and the MCP tools return, and the comments in the source. Product copy uses plain declarative sentences that address no reader, and it names assets with the product glossary. That is stricter than the style of these docs. Interface copy never says "you", for example, while these pages do.

## Where the rules apply

Follow them in every string a person reads in the product and in every comment in the source:

| Surface | Includes |
|---|---|
| Interface | Labels, buttons, headings, descriptions, toasts, empty states, errors and confirmations in `frontend/src` |
| Backend strings | `Field(description=)`, `HTTPException(detail=)`, labels and help in `shared/definitions`, stage configuration help, report prose, MCP tool descriptions |
| Source | Comments and docstrings in every package |

## Interface copy

Write interface copy plain and declarative. Name the thing and state what happened. Name objects as a person sees them: a person manages notifications, not a webhook configuration.

Each kind of element follows its own rule:

| Element | Rule | Example |
|---|---|---|
| Control | States what it does | **Start scan** |
| Success | `<Noun> <verbed>` | `Scan started for <target>` |
| Failure | `<Noun> not <verbed>.` | |
| Error | States what went wrong and how to fix it, with no apology | `The API did not respond. Check that the api service is running.` |
| Empty state | Names what is absent. A widget, not a sentence, fills the space. | `Not scanned` |
| Confirmation | Names what is removed and stops | `<Noun> <name> and its <children> are removed.` |

Reuse these canonical forms wherever they fit, so the same situation reads the same way across the product:

| Form | Use |
|---|---|
| `<Noun> <name> and its <children> are removed.` | Confirmation of a deletion |
| `Shown once. Only a hash is stored.` | A secret displayed at creation |
| `The API did not respond. Check that the api service is running.` | The API is unreachable |
| `Unsaved changes are discarded.` | Leaving a form with changes |
| `<Noun> is read-only.` | A locked object |
| `Not scanned` | No scan covered the dimension |

## Words and tokens to leave out

Leave these out of product copy. Some of them appear in these docs, which address you directly, but none of them belongs in an interface string, a backend message or a comment.

| Category | Not used |
|---|---|
| Register | `seamlessly`, `robust`, `powerful`, `leverage`, `unlock`, `elevate`, `comprehensive`, `effortlessly`, `simply`, `just`, `dive in`, `let's`, marketing adjectives |
| Justification | `because`, `so that`, `so`, `which means`, `otherwise`, `rather than`, `instead of`, a fact followed by a comma and a reason |
| Reassurance | `never`, `always`, `still`, `already`, `keeps working`, `nothing leaves`, `cannot be undone` |
| Reader address | `you`, `your`, `we`, and `reNgine` as the subject of a sentence |
| Colour | `the story behind it`, `worth a look`, `forgotten`, `an attacker gets`, metaphors, clever or punning titles |
| Tokens | The em dash, a semicolon in prose, parentheses, a question mark in a title, the exclamation mark, `e.g.`, `please`, emoji |
| Scare copy | `This is permanent`, `Are you absolutely sure?` |

## Headings and descriptions

Add a description under a heading only when it states one fact that the heading and the widget beside it do not show. A description can do one of these four things:

| A description may | Example |
|---|---|
| Decode a visual encoding | `<Items> sized by <measure> and tinted by <measure>` |
| Name the measure the title omits | Title `Geography`, description `IP addresses by country` |
| Gloss a coined term | Arsenal, Hygiene, Scan context, MCP |
| State a scope nothing on screen shows | Title `Settings`, description `Instance-wide configuration` |

A description does not restate its title, narrate the query (`from the latest scan of each target`), repeat a scope a control already renders (`in this project`, `across all targets`), or explain a sort the columns show. A description that restates its title is removed.

## Glossary

Use these terms in interface copy and backend strings, so every screen names the same thing the same way.

| Term | Meaning | Not used for it |
|---|---|---|
| target | What a user adds: a domain, IP address, CIDR range, URL or ASN | |
| web asset | A probed host name recorded by a scan | `host`, `web host`, `live host` |
| address | An IP address | |
| service | One `ip:port` | |
| endpoint | A URL | |
| finding | One result of a check on one asset | |
| scan engine | A saved configuration of stages | stage |
| stage | One capability that runs in a scan | engine |
| agent, key, access | An MCP client, its credential and its capabilities, in interface copy | `token`, `service token` |

The column header **Host** is a label and stays as printed. The full glossary is in [Glossary](../reference/glossary.md).

## Comments

Comments in the source follow the same register and stay short:

- One line at most. No narration, no module-header explainers, no multi-line docstrings.
- A comment states a fact. A fact followed by a comma and a justification is cut at the comma.
- Kept: functional directives (`# noqa`, `ts-expect-error`, `eslint-disable`), section dividers, short field labels, a terse marker for a trap.
- Rationale is kept out of the source.

Here is what that looks like in practice:

| Not used | Used |
|---|---|
| `# a bearer token deserves the same brute-force ceiling as a password` | `"""Aggregate the filtered endpoints into a directory tree."""` |
| A docstring whose second sentence argues for the first | `# ---------- catalog ----------`, `# fingerprint`, `# noqa: S501` |

## Checks that run in CI

Three vitest files in `frontend/src/lib` catch part of these rules for you. They read the source tree under `frontend/src`, skip `lib/components/ui`, and each one fails the build on a match. The other rules have no automated check, so read your strings against them yourself.

### voice.test.ts

This test checks the register of descriptions, subtitles and headings. It reads every `.svelte` file and collects three kinds of string:

| String | Source |
|---|---|
| Description | Every literal `description="…"` attribute of 4 to 200 characters |
| Subtitle | The `<p>` with `text-muted-foreground` directly under an `<h1>` |
| Heading | The literal `title` of `Widget`, `PanelHead`, `SectionHead` and `EmptyState` |

Then it runs these checks on them:

| Check | Applies to | Fails on |
|---|---|---|
| keeps LLM register out of copy | Descriptions, subtitles | `REGISTER` |
| does not address the reader | Descriptions, subtitles | `ADDRESS` |
| does not narrate scope a control already shows | Descriptions, subtitles | `SCOPE_NARRATION` |
| does not pose a heading or description as a question | Descriptions, subtitles, headings | `RHETORICAL` |
| does not instruct the reader from a description | Descriptions, subtitles | `IMPERATIVE` |
| does not restate a title in its own description | `Widget` and `PanelHead` with a title and a description | Every title word, after dropping short and stop words, appears in the description, compared on the first five letters. A description that matches `ENCODING` passes. |

These are the expressions the checks use:

```ts
const REGISTER =
	/\b(seamless(ly)?|robust|powerful|leverage|unlock|elevate|comprehensive|effortless(ly)?|supercharge|streamline|cutting-edge|best-in-class|empower|holistic|dive in|at a glance)\b/i;
const ADDRESS = /\b(you|your|you're|we|we'll|our|let's|please)\b/i;
const SCOPE_NARRATION =
	/\b(in this project|across all targets|of each target|from the latest (scan|run|covering run))\b/i;
const ENCODING = /\b(sized|tinted|coloured|colored|ranked|ordered|scaled|shaded) by\b/i;
const RHETORICAL = /^(What|Where|Why|How|Who)\b/;
const IMPERATIVE = /^(Leave|Pick|Tick|Press|Make sure|Please|Head|Go|Click|Hover)\b/;
```

### glossary.test.ts

This test keeps retired nouns out of the interface. It reads every `.svelte` and `.ts` file except tests and fails on either expression:

```ts
const RETIRED = [/\bweb hosts?\b/gi, /\blive hosts?\b/gi];
```

### skeleton.test.ts

This test makes sure a loading state is a skeleton, not text.

| Check | Fails on |
|---|---|
| never prints a sentence where a skeleton belongs | Text starting with `Loading`, `Searching` or `Fetching`, outside `routes/+page.svelte`, `routes/(app)/+layout.svelte` and `routes/onboarding/+page.svelte` |
| never fakes a skeleton by pulsing text | A `span` with `animate-pulse` that holds text |
| builds table skeletons from the table columns | `{#each Array(…)}` around a `Skeleton` in a `-table.svelte` file |

### Run the checks

Run the three tests on their own while you write copy:

```bash
cd frontend
npx vitest run src/lib/voice.test.ts src/lib/glossary.test.ts src/lib/skeleton.test.ts
```

`npm run test` runs them with the rest of the suite, and CI runs `npm run test` on pushes and pull requests to `master` and `release/*`. See [Tests and CI](tests-and-ci.md).
