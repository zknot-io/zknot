# ZKNOT Knowledge Map

Start here. Three tiers, three different rules.

## "How does <system> work / how do I deploy it?"
→ `3_OPS/km/systems/<system>.md` — **living docs, overwritten to reflect truth-now.**
- `zknot-site.md` — public site (Cloudflare **Worker**, `wrangler deploy`)
- `zknot-api.md` — FastAPI backend on Railway *(TODO)*
- `verifyknot.md` — verify UI *(TODO)*
- `hashstamp.md` *(TODO)* · `provisioning-station.md` *(TODO)*

## "What did I do / decide / learn on <date>?"
→ `3_OPS/journal/YYYY-MM-DD_topic.md` — **append-only daily log, never edited after.**
Find fast:
- by system:    `grep -l 'systems:.*zknot-site' 3_OPS/journal/*.md`
- by workstream:`grep -l 'workstream:.*biz'      3_OPS/journal/*.md`
- by tag/text:  `grep -ril 'wrangler'             3_OPS/journal/`
(Full-text grep works on un-headered old entries too; the front-matter just makes it precise.)

## "What's the formal write-up for <period>?"
→ `3_OPS/km/session-notes/*.docx` — periodic milestone/acquirer retros, generated via
`3_OPS/km/ZKNOT_Journal_Format_Template.md`. Not a daily artifact.

## "Why did I decide X?"
→ `3_OPS/km/decisions/` (ADR-style, one file per cross-cutting decision) + existing `DECISIONS_*.md`.

## The promotion habit (what keeps runbooks true)
When a daily entry nails a durable fact, copy that one line into the relevant
`systems/<x>.md` and bump its `last_verified`. The journal is the lab notebook;
the runbook is the manual.

## Templates
- Daily journal: `3_OPS/km/templates/daily-journal.md`
- System runbook: `3_OPS/km/templates/system-runbook.md`
- Formal .docx retro: `3_OPS/km/ZKNOT_Journal_Format_Template.md`
