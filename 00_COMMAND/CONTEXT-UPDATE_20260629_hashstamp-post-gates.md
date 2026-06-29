---
doc_id: CONTEXT-UPDATE_20260629_hashstamp-post-gates
title: HashStamp — state after launch-gate closure (fresh-thread context)
date: 2026-06-29
band: 00_COMMAND
product: S-HashStamp
status: ACTIVE
supersedes_for_hashstamp: extends HASHSTAMP-HANDOFF-001 + HASHSTAMP-PRIMER-001
use: Paste into a new thread (with root CONTEXT.md) to resume HashStamp work.
---

# CONTEXT UPDATE — HashStamp after gate closure (2026-06-29)

## TL;DR

HashStamp's three launch-critical gates are closed and live: reserve capture now persists
to Cloudflare KV (was console-only/discarded), Worker CORS is locked to hashstamp.io, and
the attest + reserve endpoints are rate-limited. Signing path proven unchanged. The funnel
captures, but does NOT yet notify — push alerts, ops@zknot.io, the live UI test, git init,
and chain-anchoring are the open work. Read HASHSTAMP-HANDOFF-001 for architecture and the
signing quirk; this doc is the delta since.

## Current production state

- **Worker** `hashstamp-worker` (shane-systems.workers.dev), version
  62029017-5e0f-48d1-873b-0ee68568e576. Routes: `POST /` (stamp), `POST /reserve`
  (email→KV), `OPTIONS *` (preflight).
- **Frontend** hashstamp.io / hashstamp.pages.dev — single `index.html`, reserve form
  POSTs to `WORKER_URL + /reserve`, shows success only on 2xx {ok:true}, inline error
  otherwise. No silent console fallback remains.
- **KV** namespace `hashstamp_reserves` (id b670259e28cc4ee99324f5d0c3d2f93e), binding
  `HASHSTAMP_RESERVES`. Records: `reserve:<ISO8601>:<rand>` →
  `{email,intent,ts,ua,ip_country}`.
- **Rate limits** (native `[[ratelimits]]`, per IP per colo): ATTEST 8/60s, RESERVE 5/60s.
  Per-colo + eventually-consistent → bursts trip, slow sequences may not. By design.
- **CORS**: canonical `https://hashstamp.io`; optional single `DEV_ORIGIN` via var; never
  wildcard. Applied to all responses incl. 429 and OPTIONS, with `Vary: Origin`.
- **Secret** `HASHSTAMP_PRIVATE_KEY_PKCS8` intact. Keys live only in `~/zknot-provision/`
  (off git, single copy — still a single point of failure; see open items).

## Read captured reserves

```
cd ~/hashstamp-worker && wrangler kv key list --binding HASHSTAMP_RESERVES --remote
wrangler kv key get --binding HASHSTAMP_RESERVES "<key>" --remote
```

## DO-NOT-BREAK invariants (from HASHSTAMP-HANDOFF-001 §3)

- Signing is PREHASHED double-hash on purpose: Worker signs fileHashBytes; challenge_hash
  = SHA-256(fileHashBytes); real fingerprint in `metadata.file_sha256`. Do not "fix."
- verify_url = `https://verifyknot.io/` + bare code. No `/v/`.
- artifact_type = COMBINED_SESSION until a DOCUMENT_TIMESTAMP enum + `/v1/timestamp` route.

## Open items (priority order)

1. **Notification** — Worker → Resend (free ~3k/mo) → ops@zknot.io alert on each reserve.
   Workers can't send mail natively (MailChannels-free retired 2024). This is the literal
   "I just need to be notified" ask; capture works, push does not.
2. **ops@zknot.io** — Cloudflare Email Routing (free, receive-only) now; Google Workspace
   before federal BD send-from. Check for an existing Workspace tenant to add zknot.io as a
   secondary domain instead of a new subscription.
3. **Test 5 — live UI click-through** (human-in-the-loop): stamp a real unique file → verify
   page; submit reserve → success state → confirm browser-UA record in KV. Backend is
   curl-proven only.
4. **git init** `~/hashstamp-worker` and `~/hashstamp-site`; gitignore `~/zknot-provision/`
   and `*.bak-*` from first commit. Production code currently has no version history.
5. **Rate-limit tuning** when real traffic reveals the ceiling (legit batch of ~15 stamps
   hits the attest 8/min wall).
6. **Fast-follow product** (pre-existing backlog): `/v1/timestamp` route (kills double-hash),
   freelancer-legible verify view, pricing test, distribution.
7. **Strategic / moat**: anchor ZK-LocalChain (TimeAnchor PAT-022 / OpenTimestamps) so
   proofs survive ZKNOT — answers the "niche service could vanish" objection AI search
   already raises. Turns the biggest weakness into the differentiator.

## Distribution gate (still holding)

Do not drive paid traffic to the capabilities one-pager until notification (#1) and the
live UI test (#3) are done — a captured-but-unseen lead with no UI confirmation is a wasted
cold-audience shot. Also re-check the Cloudflare AI-crawler setting (default-block) so AI
search can actually read hashstamp.io.

---

*ZKNOT, Inc. — HashStamp is a ZKNOT product. When physics is policy, trust is optional.*
