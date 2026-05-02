# Handoff — KM / Project Management / Life Fixer

**From:** Previous Claude conversation (2026-04-24)
**To:** Next Claude conversation
**Purpose:** Help Shane pick and set up a knowledge management + project tracking system that actually works for his situation.

---

## What Shane needs

A real tool (not an artifact, not a one-off spreadsheet) to track everything he's got going. In his words: *"I am going 1000 different directions, and I need a proper km solution, a tracker of projects with a method to track based on time, cost, priority, involvement, etc but I need to be able to put for example the next task can't happen until the boards arrive so I need to make sure things flow smoothly as well."*

Key capabilities he explicitly named:
- Track projects by **time, cost, priority, involvement**
- **Dependency tracking** — Task B blocks on Task A completing (e.g., "can't assemble until boards arrive")
- Knowledge management layer, not just tasks
- Scales across hardware, software, legal/IP, business/acquisition workstreams

## Context about Shane and ZKNOT

Shane is the solo founder of ZKNOT, INC. (active SAM.gov registration, UEI C4SKW13JPEL5). He's running multiple simultaneous workstreams:

- **Hardware:** Embedded security devices (PowerVerify, ZKey, ZKM-series), STM32 + ATECC608 architecture, PCB design, BOM management, Saleae Logic 2 integration via MCP
- **Software:** FastAPI backend on Railway (api.zknot.io), ZK-LocalChain in production, verifyknot.io frontend pending Cloudflare Pages deploy
- **IP portfolio:** 16 provisional patents filed, 6 non-provisional conversions coming up in the next 12 months ($18K+ committed), 1 trademark pending, various pending decisions like PAT-019 (optical PUF) documented today
- **Business:** 6-month acquisition window, 8 named acquirers being courted, Axon and federal procurement stories

He works Linux CLI-native (arm-none-eabi-gcc, OpenOCD, GDB). Prefers CLI tooling over GUI where reasonable. Integrates AI/Claude into his workflow heavily.

## What we decided NOT to do in the previous conversation

Do **not** build a custom tracker in a Claude artifact. It would be brittle, live in one chat, and Shane would outgrow it in a week. He needs a real tool he owns.

Also do not default to "just use Notion" without understanding his actual workflow. The previous conversation flagged several candidates worth weighing: Notion, Linear, Obsidian+Tasks, Google Sheets with good structure. Each has real trade-offs for his situation.

## Where to start

Do **not** just recommend a tool out of the gate. First understand his constraints. Useful questions to ask early (use the ask_user_input_v0 tool — he's on mobile sometimes and tapping is easier than typing):

1. Is he willing to pay for a tool, or does it need to be free/open-source?
2. Does he want cloud-hosted SaaS, self-hosted, or local-only?
3. How important is collaboration (does anyone else need access — lawyer, contractor, future hires) vs pure solo use?
4. Does he want the tool to be CLI-accessible (fits his Linux workflow) or is web/app fine?
5. Has he tried anything before that didn't stick, and why?

## Frameworks worth considering (initial shortlist — not a recommendation)

- **Notion** — best for flexible KM + basic project tracking, weak on real dependencies, has a mobile app, SaaS, $
- **Linear** — excellent for engineering-style project tracking, good dependencies, less good as a KM/notes tool, SaaS, $
- **Obsidian + Tasks/Dataview/Projects plugins** — local markdown files, git-trackable, CLI-friendly, steep setup, free
- **Logseq** — similar to Obsidian, more opinionated outliner, open-source
- **ClickUp / Height / Airtable** — more featureful but also more overhead
- **Linear + Obsidian combo** — Linear for tasks/deps, Obsidian as the knowledge vault. Two-tool cost in attention.
- **Custom: SQLite + markdown + scripts** — fits his CLI preference but is a project of its own, probably wrong answer right now

Don't anchor him on any of these yet. Elicit constraints first, then narrow.

## Important meta-note

Shane explicitly said in his preferences: *"Tell me when it's easier for me to do things in real life to limit the use of tokens, or when a walkthrough step by step is more useful than a document."*

Respect that. If setup is three clicks, just tell him the three clicks. Don't write a 2000-word deployment guide when a short paragraph and a link will do. Save long-form docs for when there's a real artifact (e.g., a template he can import, a schema spec).

Also: keep the conversation scoped. Don't let it sprawl into "and while we're at it, let's redesign your whole life." The goal is one working KM/PM system selected and stood up within the session or the next few days, not an aspirational vision doc.

## Existing artifacts to be aware of

Shane has a patent tracker spreadsheet (`ZKNOT_DOC-001_patent_tracker_20260328.xlsx`) that works well for its scope. Don't try to replace that — it's a source-of-truth document for IP, and it's fine where it is. The new KM system should coexist with it and probably link to it, not absorb it.

## Anchoring the priority

The single most important capability for Shane right now is **dependency tracking across workstreams**. He said it explicitly: things like "boards must arrive before assembly, firmware must flash before test, test must pass before ship" need to be visible so he doesn't context-switch himself into paralysis. Any tool recommendation that doesn't handle dependencies well should be eliminated early.

## First message to send Shane

Open with something like: *"Before I recommend anything, a few quick questions so we don't end up with a tool you'll abandon in two weeks."* Then ask_user_input_v0 with the constraint questions above. Do not send a comparison table or a long intro. Get the constraints, then narrow.
