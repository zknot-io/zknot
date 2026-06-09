---
date: 2026-05-29
topic: verify-trust-model-review
workstream: [sw, ip]
author: William Shane Wilkinson
tags: [trust-model, verifyknot, crypto, marketing-claims, hsm]
status: findings-recorded
---

# Verify Trust Model Review — Are "No trust required" / "Independent of ZKNOT" true?

## TL;DR
Both hero claims on verifyknot.io are **false today**. `GET /v1/verify/{code}`
returns `verified: true` as a **hardcoded constant** gated only by a DB row
existing — it is a `SELECT` wearing a crypto costume. The response carries real
crypto fields (signature, public_key, challenge_hash, chain hashes) but **nothing
checks them**: `verify.py` never calls `verify_signature` (grep = 0 hits). Demo
sigs are placeholder hex, so the check has never run in this codebase's life.
This is **expected** — real sigs are blocked on the YubiHSM2 (provisioning real
chip keys + manufacturer root). The fix is sequencing, not panic. Retire both
claims until the full chain is wired.

## What I confirmed (from my own grep/sed output)
- `build_verify_response` returns `verified=True` literally. Only gate is
  `lookup_by_short_code` / `lookup_by_artifact_id` finding a row → else 404.
  Meaning of `verified:true` = "this string is a primary key in my Postgres."
- `grep verify_signature app/routers/verify.py` → **zero hits**. Sig + pubkey
  are read off the row and passed through to JSON untouched (DOM fields, not
  inputs to any check).
- Encoding contradiction in `_parse_signature`: docstring/code expect raw r‖s
  (64 bytes) and re-encode to DER, but live wire data is *already* DER (3045...).
  Repo holds three conflicting opinions on sig format (DER stored, raw-r‖s
  parser, P1363 needed for WebCrypto).
- Seed sigs (`3045022100a1b2c3d4...`) are placeholder patterns, not real
  signatures → ingest never ran a real verify or it would have thrown.
- PowerVerify hand-assembled units sign with **server-side HMAC** (units.py),
  keyed by salt in 99_SENSITIVE/api_secrets.env. HMAC is symmetric →
  **categorically un-verifiable by any third party**. This is the consumer line.
- ZK-LocalChain integrity = walk my own Postgres, recompute my own hashes.
  `chain_integrity:true` = "my DB agrees with itself." No external anchor.

## Verdict
A verifier must trust ZKNOT's server completely. "No trust required" and
"Independent of ZKNOT" are theater **as currently shipped**. Not a bug — the
root of trust (HSM-held manufacturer key) does not exist yet.

## Decisions
1. **Pull both hero claims now.** Interim copy: "No account required to verify"
   (true) and "Publicly auditable" (true once frontend + verify logic are
   open-source). Do NOT use blanket "cryptographically signed" — false for the
   HMAC'd PowerVerify units.
2. **Sequence is fixed and non-negotiable:** YubiHSM2 → real ECDSA sigs +
   manufacturer root key → wire `verify_signature` into the verify path → pin
   manufacturer pubkey in the FRONTEND trust domain (not served by API) →
   anchor chain root externally (OpenTimestamps→BTC). Marketing copy may not
   outrun whichever step is actually live.
3. **Pin one signature encoding end-to-end** before wiring verification, or every
   existing record fails. Decision pending: raw r‖s (P1363) is the target since
   ATECC + WebCrypto both want it; needs a migration to re-encode stored DER rows.
4. **Open hardware question to resolve before writing final copy:** do consumer
   PowerVerify units get onboard secure elements (device self-attests → "independent
   of ZKNOT" reachable) OR does the HSM just let the server sign birth certs with a
   real key (server-vouched → honest, but NOT "independent of ZKNOT")? Words must
   match the hardware.

## BACKUP / IRREPLACEABLE FLAGS
- **HMAC salt** (api_secrets.env) is currently the ENTIRE trust anchor for every
  PowerVerify unit. Leak = silent total forgeability, chain still reports
  integrity:true, no rotation story (units hold no keys). Confirm backed up +
  compromise plan. STATUS: ⬜ unverified.
- **YubiHSM2 manufacturer key (future):** will be the root every pinned-pubkey
  claim rests on. Must never export plaintext. Decide backup (wrap-key to 2nd
  HSM / M-of-N restore / accept single-HSM risk + document) and run the key
  ceremony BEFORE the device arrives. Lost = orphaned device certs; leaked =
  forgeable chain. STATUS: ⬜ ceremony not planned.

## Next actions
- [ ] Update verifyknot.io copy to interim wording (this week, pre-deploy).
- [ ] Promote durable trust-model facts to km/systems/trust-model.md.
- [ ] On HSM arrival: build WebCrypto verifier (DER↔P1363) + FastAPI response_model
      + canonical-serialization helper + DER→raw migration.
- [ ] Resolve self-attested vs server-vouched hardware question.
- [ ] Plan YubiHSM2 key ceremony + backup strategy.

## Concepts to internalize (running list)
Trustlessness = relative to a root of trust · HMAC vs ECDSA (symmetric =
un-verifiable by third party) · circular-key bootstrapping · trust-domain
separation (API origin vs open-source frontend) · pubkey pinning + manufacturer
cert chain · verified-by-DB-lookup vs verified-by-crypto · DER vs raw r‖s / P1363
· canonical serialization · self-attesting log vs externally-anchored ledger ·
OpenTimestamps / CT / Merkle inclusion proofs · tamper-evident vs tamper-proof ·
key compromise & rotation threat model · HSM key custody · server-vouched vs
device-self-attested.
