---
date: 2026-06-01
topic: ft260-batch-provisioning
workstream: hw
tags: [ft260, atecc608, provisioning, cryptoauthlib, tier0, selfknot]
status: milestone
---

# FT260 → ATECC608 batch provisioning — 5 Tier-0 devices done

## TL;DR
Proved the full provisioning recipe on one test article, then replicated to 4 more:
**5 fully-provisioned, signature-verified Tier-0 self-assertion devices.** Each is
config-locked, slot-0 P256 keyed (key born on-chip, non-extractable), host-verified,
and data-locked. All recorded in `km/systems/atecc-provisioning-ledger.psv` with full
public keys; integrity-checked (every pubkey 128 hex chars). This unblocks the SelfKnot
Pico build per the root primer's critical path.

## Decisions
- **Recipe = config-lock → GenKey(slot0) → HOST-side verify → data-lock.** Proven, then
  replicated unchanged across 5 parts.
- **Verify is done host-side** (python `cryptography`), NOT chip-side
  (`atcab_verify_extern`). Chip-side verify COMM_FAIL'd on the FT260 bridge; host-side is
  both more reliable AND the path a real verifier actually uses (they hold the pubkey, not
  the chip). This is the correct test, not a workaround.
- **Per-part serial guard, step-by-step (not a batch loop).** Each part: read seated
  serial → confirm it's new + unlocked → hardcode that serial as EXPECT in each script →
  run. Deliberately chose manual confirm over automation because the locks are irreversible
  and the one expensive failure mode is locking the wrong/duplicate part to a ledger row.
- **Tier 0 only.** These are SelfKnot/DIY self-asserted parts. NOT official ZKNOT, NOT
  ZK-numbered, NOT PUF-tracked. Commercial path (YubiHSM2 ceremony) is separate and untouched.

## Provisioned parts (full records in ledger)
| n | serial | role |
|---|--------|------|
| 1 | 012337d1a9f0eb45ee | test article (recipe proof) |
| 2 | 0123fc0bbdc63b4dee | batch |
| 3 | 01231e45e5c5b0f8ee | batch |
| 4 | 0123c9eaa2bdd913ee | batch |
(plus the original first-light part 012337d1 = #1 above)

## Gotchas banked
- **`ATCA_COMM_FAIL` on verify ≠ bad signature.** It's a comm-layer error. Read *which
  call* failed: sign succeeded, verify failed → not a crypto problem. Host-verify sidesteps it.
- **Ledger pubkey truncation.** Hand-editing once abbreviated a pubkey to `fc9e...bd6289`.
  A truncated pubkey can't verify anything and the private key is gone — the pubkey is the
  one field you can never sloppily abbreviate. Added an `awk` integrity check: every data
  row's pubkey must be 128 chars.
- **`sed` with `|0|` in the data** reads the `0` as a substitution flag and errors
  ("number option may not be zero"). Hand-edit pipe-delimited rows; don't fight sed.

## Open / next
- [ ] SelfKnot Pico reference build using one of these provisioned parts (next session).
- [ ] Promote the proven sequence into km/systems/ft260-provisioning.md (durable facts).
- [ ] 6 known-good parts remain unprovisioned (had ~10 known-good of 30+ total).
- [ ] Guide/video writeup — keep on the giveaway side of the PAT-001 line: presence/
      device-binding only, never the display-then-confirm method (see product-ladder doc).

## Backup / VC status
- Ledger committed across commits up to 89367ca; pushed to zknot-io remote (off-box).
- Locks are physical/permanent on-chip — not backupable. The ledger is the ONLY
  serial↔pubkey record; it must stay backed up. Private keys non-extractable by design.
- No secrets in any committed file (pubkeys + procedure only).
