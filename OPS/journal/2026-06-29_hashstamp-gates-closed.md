---
doc_id: JOURNAL-2026-06-29-hashstamp-gates-closed
title: HashStamp launch gates closed — capture loop live, notification still open
date: 2026-06-29
band: 3_OPS
product: S-HashStamp
tags: [hashstamp, launch, cloudflare, worker, kv, cors, rate-limit, claude-code]
status: FINAL
---

# 2026-06-29 — HashStamp launch gates closed

## TL;DR

The three launch-critical gates on HashStamp are deployed and verified live: (A) the
"Reserve a spot" button — which previously logged to the browser console and discarded
the email — now persists to Cloudflare KV and the lead is readable back out; (B) the
Worker CORS is locked from `*` to `https://hashstamp.io`; (C) the attest and reserve
endpoints are rate-limited and return 429 under burst. The signing path was proven
byte-for-byte unchanged. **One thing is NOT done: push notification.** Capture is closed
(pull-based — leads sit in KV until you list them), but no alert fires when a reserve
lands. That is the top open item, not a finished feature.

## Decisions

- **D1 — Reserve capture: Worker route + Cloudflare KV** (chosen over Formspree for
  in-house control; no third party holds the prospect list). Implemented as `POST /reserve`.
- **D2 — Do NOT distribute the capabilities one-pager / drive paid traffic yet.** Capture
  works, but with no notification a lead can sit unseen, and the live UI click-through
  (Test 5) is still pending. Distribution waits on notification + UI confirmation.
- **D3 — ops@zknot.io: Cloudflare Email Routing first (free, receive-only), Google
  Workspace before any federal BD send-from.** Not yet executed — carried to next thread.
- **D4 — git init both repos next session** (`~/hashstamp-worker`, `~/hashstamp-site`),
  with `~/zknot-provision/` and `*.bak-*` gitignored from the first commit. Currently
  neither is under version control — production code touching the signing key has no
  history beyond `.bak` files + `wrangler rollback`.

## What shipped

- Worker `hashstamp-worker` → version 62029017-5e0f-48d1-873b-0ee68568e576
- Frontend → hashstamp.pages.dev (single clean `index.html`; backups moved to
  `~/hashstamp-site-backups/`, out of the deploy dir after one accidental upload)
- KV namespace `hashstamp_reserves` → id b670259e28cc4ee99324f5d0c3d2f93e
- Secret `HASHSTAMP_PRIVATE_KEY_PKCS8` confirmed intact across the deploy
- Stale byte-identical twin at `~/Downloads/_sorted/code-web/index.html` deleted

## Verification (Phase 4, live)

| Test | Result |
|---|---|
| 1 — Signing smoke | ok:true, bare-code verify_url, chain pos 26 — signing intact |
| 2 — Chain verify | verified:true, chain_integrity:true (idempotent: returned existing artifact, no dup) |
| 3 — CORS negative | foreign origin gets `https://hashstamp.io`, never its own — lockdown holds |
| 4 — Reserve capture | valid → 200 persisted {email,intent,ts,ua,ip_country}; garbage → 400, nothing stored; ops@zknot.io confirmed readable back out |
| C — Rate limit | 40-parallel burst → 28×429; single requests unaffected; 429 carries locked CORS header + Vary: Origin |

Signing path proven byte-for-byte unchanged (whitespace-ignoring diff; live verify
confirms valid signatures). Rate limiter is per-colo / eventually-consistent by design —
sequential loops pass, concurrent bursts trip; expected behavior, not a defect.

## Still open (carried to next thread)

1. **Push notification** (the literal ask "I just need to be notified"). Worker → a
   transactional email provider (Resend free tier ~3k/mo) → one-line alert to ops@zknot.io
   on each reserve. Workers can't originate mail directly (MailChannels-free retired 2024).
2. **ops@zknot.io** stand-up (Cloudflare Email Routing now; Workspace later). Check whether
   an existing Google Workspace tenant can just add zknot.io as a secondary domain.
3. **Test 5 — live UI click-through** on hashstamp.io (stamp a real unique file → verify
   page; submit reserve → success state → read browser-UA record back from KV). Backend is
   curl-proven; the human-in-the-loop UI pass is not yet done.
4. **git init both repos** (D4).
5. **Rate-limit tuning** once real traffic shows the ceiling (attest 8/min, reserve 5/min
   per IP per colo today; legit-batch of 15 deliverables would hit the attest wall at 8).

## Personal-monopoly thread

This closes the funnel HashStamp's capabilities one-pager was built to feed — but the
deeper move is still ahead: anchoring the ZK-LocalChain (TimeAnchor / OpenTimestamps) so
HashStamp proofs survive ZKNOT itself. That's the objection AI search already raises and
the one the whole "honest witness" thesis was built to answer. The freelancer tier is the
cheap, public place to prove skeptic-verifiability before the federal story leans on it.

---

*ZKNOT, Inc. — HashStamp is a ZKNOT product. When physics is policy, trust is optional.*
