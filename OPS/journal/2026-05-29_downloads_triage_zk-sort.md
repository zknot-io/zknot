# 2026-05-29 — Downloads Triage + zk-sort Tool

## Summary
Built a reusable triage script (`zk-sort`) and ran the first full cleanup of a
long-overflowing `~/Downloads`. Root went from ~160 mixed files to near-empty.
Second journal of the day (see also `2026-05-29_outreach_and_deploy.md`).

## What I built
`~/bin/zk-sort` — safe Downloads triage. Behavior:
- Auto-files dated journal entries (`YYYY-MM-DD_topic.md`) into `~/ZKNOT/3_OPS/journal/`.
- Sorts everything else into `~/Downloads/_sorted/<category>/` for manual review:
  code-python, code-web, hardware-kicad, images, docs-pdf, docs-office, archives,
  markdown-other, misc.
- Dry-run by default; `--apply` to execute.
- Never overwrites (collisions left in place + reported), never recurses into dirs,
  never writes into a git repo.
- Case-insensitive extension match (handles .PDF and .pdf).

Design choice (deliberate): did NOT automate routing files into repos
(~/zknot-api, ~/verifyknot-site). Inferring repo destinations risks silently
polluting git working trees. Staging gets clutter out of the way; final repo
placement stays a human decision.

## First run results
- Journals filed: 15
- Staged for review: 149
- Dirs skipped: 2 (adafruit bundle, _inspect-graip)
- Collisions: 4 (dated journals already present in vault — left in Downloads root
  to reconcile via `diff -q`)

## Still open (not done — staging is step 1 of 2)
- Resolve 4 collisions: `diff -q` each leftover dated .md against its vault twin;
  delete if identical, reconcile if differs.
- Route `code-python` and `code-web` staged files into their real repos (these are
  the buckets that matter — code shouldn't drift from version control). images /
  docs-pdf / archives can sit in staging indefinitely.
- Many `(1)`/`(2)` duplicate pairs (ZKKEY_CONNECT_BOM_REV1 x3, topic_ARM... set) —
  now grouped by type, so easy to dedupe.

## Toolkit note
Second reusable helper this session. Personal CLI toolkit forming in `~/bin/`.
Pattern to keep: dry-run-by-default for anything that moves/deletes files.

## Concepts reviewed
deterministic vs. inferred file routing · dry-run-by-default safety pattern ·
don't auto-write into git repos · staging tree · `diff -q` for dedupe ·
PATH / ~/bin for personal scripts.

---
*Commit: `cd ~/ZKNOT && git add 3_OPS/journal/2026-05-29_downloads_triage_zk-sort.md && git commit -m "journal: downloads triage + zk-sort tool"`*
