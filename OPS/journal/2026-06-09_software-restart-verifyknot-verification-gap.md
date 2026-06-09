---
date: 2026-06-09
topic: Software-track restart — wire-format/firmware decisions, CubeMX bring-up primer, verifyknot verification-gap finding
tags: [zkkey, witnessmark, verifyknot, software, firmware, cubemx, cose, transparency-log, decisions]
status: complete
related:
  - SIG-FW-ZKKEY-002 (CubeMX/CubeIDE TrustZone setup primer — working)
  - verifyknot-primer v2 (3_OPS/km/systems/verifyknot-primer.md)
  - SIG-VER-ZKKEY-001 + ADD-001 (verifier spec + time-binding decision)
  - SIG-FW-ZKKEY-001 (firmware/secure-config enforcement)
  - SIG-SPEC-ZKKEY-005 (canonical capability spec)
---

# 2026-06-09 — Software-track restart + verifyknot verification-gap finding

## TL;DR

Re-entered the software side after the architecture/IP arc. Locked the software-stack decisions (COSE/CBOR
records, CubeIDE-first firmware, CLI/CMake+TF-M for Redoubt, CT-modeled transparency layer, TS+Python
verifier), produced a CubeMX TrustZone bring-up primer so the firmware thread can start on a dev kit, and —
the consequential finding of the day — verified verifyknot live and discovered the deployed verifier
**asserts a verdict from the server rather than proving it client-side, over placeholder demo data.** Caught
before any contracting-officer demo. verifyknot primer re-leveled to v2 with the honest two-state status.

## Decisions (confirmed today)

- **Record serialization = COSE/CBOR (RFC 9052).** Compact (Air QR ceiling), deterministic for signing,
  IETF-standard for offline interop. Wrinkle to handle in the wire-format spec: event sig + identity-domain
  attestation + combined sessions ⇒ not a plain `COSE_Sign1`.
- **WitnessMark firmware: STM32CubeIDE first.** Get a TrustZone-split project with GTZC isolation + the
  signing-ceremony skeleton working; defer OEMiRoT/SBSFU secure-boot hardening to a refactor. Bring up on
  the **B-U585I-IOT02A dev kit** — not blocked on the custom board.
- **Redoubt firmware: CLI/CMake + TF-M build route** (the hardened SKU earns the rigorous build).
- **Transparency layer: build small now, modeled on existing patterns (RFC 6962 CT / Trillian / C2SP), not
  invented.** Same prior-art discipline as the PAT-021 Sigstore finding.
- **Verifier libs: TypeScript (browser/client) + Python (reference/test/backend).** Public usability + a
  test oracle from one design.

## Decisions pending / recommendations made today (not yet actioned by me-the-owner)

- **verifyknot URL form:** make `/v/{code}` canonical + add `bare → /v/` redirect; update SOP-001. (`/v/`
  confirmed serving live.)
- **Do not run the "math verified it, you didn't trust us" demo line** until the client-side verifier ships
  AND a real signed record exists.
- **Replace placeholder demo records** with at least one genuine signature over a real artifact hash, labeled
  at honest tier (SELF-ASSERTED is fine; mock asserting VERIFIED is not).

## The finding (the why worth keeping)

verifyknot was believed "deployed and live." Live checks (2026-06-09) showed the frontend is serving and the
backend `/health` is ok — but `GET /v1/verify/ZK-6GUA-7DV` returns `verified:true` with a **placeholder
signature** (`a1b2c3d4…` repeating), filler public key, and `challenge_hash` = SHA-256("test"), and the
browser displays the server's boolean. So the live product currently does the **opposite of its one job**:
the stranger is trusting ZKNOT's server, not re-checking math. The platform's headline ("Math is the
testimony / no trust required") is aspirational, not yet true.

Why it mattered to catch now: the audience is government/CO; a security-literate evaluator can `curl` the
endpoint, see the filler signature, and the "verifiable, not trust-me" differentiator collapses — worse than
an ordinary bug because the whole pitch is "don't trust us." The fix is exactly the already-decided TS
client-side verifier (VER-33) + real records. This is a candor/honest-translation issue, not just backlog.

## Artifacts produced

- **SIG-FW-ZKKEY-002** — CubeMX/CubeIDE TrustZone setup primer (working). Maps SIG-FW-001 to concrete CubeMX
  config; front-loads the SAU↔GTZC-match and RCC_GTZC-clock gotchas; stop-line = TZ split + GTZC + ceremony
  skeleton on the dev kit; CubeMX pinout drives the KiCad pinmux (do it before copper).
- **verifyknot-primer v2** — re-leveled §0 to the honest two-state picture; folded in today's decisions;
  re-prioritized open items with the client-side verifier + real records as the gating pre-demo work.

## Open / next

- **Top priority (verifyknot):** ship the TS client-side verifier so the verdict is browser-computed; seed
  real signed records; implement `/v/` canonical + redirect.
- **Firmware (fw):** start the CubeMX project on the dev kit per SIG-FW-002; export pinout for KiCad.
- **Software (sw):** record wire-format + canonicalization spec (COSE structure for multi-sig + combined
  sessions) — the ungated device↔verifier contract; transparency-log evolution (CT-modeled).
- **Re-entry ritual:** paste root CONTEXT + project primer; glance the architecture-map carry-list; name the
  day's thread. Keystone gap: the **WitnessMark project primer** still needs rebuilding to current truth.
- **Standing (unchanged):** file PAT-020; PAT-021 + counsel note to July 1 (Sigstore distinction);
  WitnessMark/Redoubt trademark knockout.

## Version-control status

- `verifyknot-primer.md` v2 → `~/ZKNOT/3_OPS/km/systems/` (canonical path); supersedes v1 (same day).
- `SIG-FW-ZKKEY-002_cubemx-trustzone-setup-primer` → `6_SIG/firmware/`.
- This journal → `3_OPS/journal/`.
- Nothing backed up until committed. Vault reorg still settling — add explicit paths; no `git clean -fd`.
