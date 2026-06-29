---
doc_id: HASHSTAMP-CC-HANDOFF-002
version: 1.0
date: 2026-06-29
author: William Shane Wilkinson
product: S-HashStamp
status: ACTIVE — Claude Code task brief (next session)
intended_runner: Claude Code (agentic CLI)
source_of_truth: HASHSTAMP-HANDOFF-001 (architecture), CONTEXT-UPDATE_20260629 (current state)
predecessor: HASHSTAMP-CC-HANDOFF-001 (gates A/B/C — DONE)
---

# HashStamp — Claude Code Handoff 002: Reserve notification + ops@zknot.io

## TL;DR (for the agent)

Gates A/B/C are already deployed and verified (capture→KV, CORS lock, rate limit). The
reserve loop captures but does NOT notify. Job: make a reserve submission fire a push
alert to ops@zknot.io, and stand up that address to receive. Do NOT touch the signing
path or the existing gate logic. Investigate and report before changing anything.

## Guardrails (unchanged from 001 — re-read)

1. Do NOT modify signing / challenge_hash / verify_url logic. Prove it untouched via a
   whitespace-ignoring diff before showing changes.
2. Keys stay in `~/zknot-provision/`, off git. Any new API key/secret goes there or into a
   Worker secret (`wrangler secret put`), never into committed files.
3. Explicit `git add <file>` only. (Note: repos may be freshly git-init'd this session —
   see Phase 0.)
4. wrangler needs Node >= 22: `export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 22`.
5. No deploy without human-approved diff. Build + dry-run locally first.
6. Verify current provider + Cloudflare API syntax against live docs before writing config.

## Phase 0 — investigate + report (no edits)

1. Confirm current Worker `/reserve` handler shape and where to insert a post-store hook.
2. Report whether `~/hashstamp-worker` / `~/hashstamp-site` are git repos yet. If not,
   recommend `git init` with `.gitignore` covering `~/zknot-provision/` patterns and
   `*.bak-*` BEFORE any further commits (do not commit until human confirms .gitignore).
3. Confirm whether a Google Workspace tenant already exists that could add zknot.io as a
   secondary domain (ask the human; do not assume).
4. List exact files to change and the chosen email provider, with the tradeoff.

STOP and let the human confirm before Phase 1.

## Phase 1 — ops@zknot.io receives (human-confirmed path)

Default: **Cloudflare Email Routing** on zknot.io (free, receive-only) → forwards to the
human's real inbox. Steps are dashboard-driven (auto-adds MX + SPF); document them, the
human executes (account-mutating). If the human already runs Workspace, document the
"add secondary domain + create ops user" path instead.

Acceptance: a test email to ops@zknot.io arrives at the destination inbox.

## Phase 2 — reserve push notification

Goal: every successful `POST /reserve` also sends a one-line alert email to ops@zknot.io.

- Workers cannot originate mail directly (MailChannels-free retired 2024). Use a
  transactional provider with a free tier — **default: Resend** (~3k/mo free). Verify the
  current API + that the sending domain (or a subdomain like mail.zknot.io) is set up with
  the SPF/DKIM records the provider requires; deliverability depends on it.
- Store the provider API key as a Worker secret (`wrangler secret put RESEND_API_KEY`).
- In `handleReserve`, AFTER a successful KV write, fire the notification. It must be
  best-effort: a notification failure must NOT fail the reserve (the lead is already
  stored). Wrap in try/catch; log but still return {ok:true}.
- Alert body: email, intent, ts, ip_country, and the KV key — enough to act without
  opening the dashboard.
- Rate/abuse note: the reserve endpoint is already limited 5/60s per IP per colo, so the
  notification volume is bounded. Do not add a second notification per request.

Acceptance:
- A live test reserve produces a real email in ops@zknot.io within seconds.
- A simulated provider failure still returns {ok:true} and still persists to KV.
- Signing path diff proves stamp logic untouched.

## Phase 3 — retest + (optional) git baseline

- Re-run the Phase-4 suite from 001 (signing smoke, chain verify, CORS negative, reserve
  capture+readback, rate-limit 429) to confirm no regression.
- If the human approved git init in Phase 0: stage named files only, confirm no keys/secrets
  or `.bak-*` staged, GPG-signed commit.

## Definition of done

- [ ] ops@zknot.io receives mail
- [ ] Reserve fires a push alert to ops@zknot.io; failure is non-fatal to capture
- [ ] Provider key stored as Worker secret, not committed
- [ ] Phase-4 regression suite green; signing path proven unchanged
- [ ] (if approved) both repos under git with keys + backups gitignored

---

*ZKNOT, Inc. — HashStamp is a ZKNOT product. When physics is policy, trust is optional.*
