---
date: 2026-06-13
topic: verifyknot-start-live-verify
workstream: sw / fw
tags: [verifyknot, web-serial, verifier, attestor, atecc608, circuitpython, deploy]
status: milestone
relates_to: 2026-06-13_attestor-first-light.md
---

# verifyknot.io/start — live-device verification in a stranger's browser

## TL;DR
Shipped `verifyknot.io/start`: a visitor plugs in a ZKNOT Attestor, presses its button,
and the signature is verified **in their own browser** against the device's enrolled
public key — the verdict is computed client-side, not asserted by the server. Reuses the
already-deployed `verifier.js` verdict engine unchanged; the only new code is the
Web Serial transport and the record assembly. Honest Tier-0 binding (`SELF-ASSERTED` /
`firmware-mediated` / `content: none`) is declared in the record, so the verifier's
headline cannot overclaim. Verified green on the bench against part `01234DF53F8AF547EE`,
then deployed.

## Decisions
- **Web Serial for /start, host-relay later.** Browser ↔ device directly: no install, no
  backend, the visitor sees their own machine do the check. The headless host-relay path
  (`verify_unit.py`) stays as the automated/CI complement — sequenced, not discarded.
- **Reuse the verdict engine; do NOT fork the crypto.** `/start` builds a v1 record from
  the live device and calls the SAME `verifyRecord()` that `/v/{code}` uses. One verifier,
  two transports (fetch vs. Web Serial). Zero new cryptographic code.
- **The sign/verify seam:** browser generates a random `payload`, sends
  `challenge = SHA-256(payload)` (64 hex) to the device; the ATECC signs that 32-byte
  challenge as a raw digest; the page sets `signed_payload_hex = payload`,
  `challenge_hash = SHA-256(payload)`. `verifyRecord` then has Web Crypto hash the payload
  and verify over the same digest the chip signed. They meet because `challenge` IS
  `SHA-256(payload)`. This is the ONLY model that works with this verifier — a
  device-self-generated challenge has no preimage the page could check.
- **Pubkey source = bundled, with a one-function swap seam.** `pubkeyForSerial()` returns
  the ledger key today (offline, auditable, no backend); the live `fetch` to `api.zknot.io`
  is two commented lines above it. Flip that function when per-unit redeploys start to hurt;
  nothing else on the page changes.
- **Honesty by construction.** Record declares `identity_tier: SELF-ASSERTED`,
  `presence_binding_type: firmware-mediated`, `content_binding_type: none`. The verifier
  generates the headline FROM those fields (VER-04), so the page states exactly what was
  proven — a firmware-enforced press, firmware-trust not silicon, no content shown.

## What happened
- Built `start/index.html` matching the site's design tokens (DM Mono/Syne/DM Sans, the
  `--bg`/`--accent` palette, noise overlay, sticky nav), importing the deployed
  `/verifier.js`.
- Bench test against `01234DF53F8AF547EE`: connect → fresh challenge sent → button press →
  **VERIFIED — in your browser** (green), with the honest SELF-ASSERTED / FIRMWARE-MEDIATED
  / NONE badges.
- Deployed to Cloudflare Pages → live at `https://verifyknot.io/start/`.

## The bug that mattered (and how it was found)
"Connected, waiting for button press, press does nothing." Added a **diagnostic device-log
panel** (raw TX/RX lines) to the page. The log immediately showed the truth:

  - `TX 16782b79…` (our challenge, sent)
  - `RX ]0;🐍code.py | 10.2.0\SIG 01234DF5… 16782b79… d068fdfb…`

The device **received our exact challenge and signed it correctly** — the round-trip and
the crypto were never broken. The page mis-parsed the `SIG` line because CircuitPython 10.2
prepends an **OSC terminal-title escape sequence** (`ESC]0;code.py|10.2.0…`) to console
output, so the line did not *start with* `"SIG "`. My parser used `startsWith("SIG ")` and
silently dropped the one good signature.

**Fix:** match the `SIG` triplet anywhere in the line with a regex
(`/SIG\s+([0-9A-Fa-f]+)\s+([0-9a-fA-F]{64})\s+([0-9a-fA-F]{128})/`) instead of requiring a
prefix; also resend the challenge until a matching SIG arrives (handles reboot-on-open).
Re-tested → green.

## Lesson
- **Make the black box talk.** A raw RX/TX log turned "nothing happens" into a precise,
  visible fact in one button press — same move as the boot self-test: surface the truth at
  the boundary instead of failing silent. Without it, this reads as a wiring/firmware/button
  mystery; with it, it's three lines of string parsing.
- **Parse-tolerance over parse-strictness.** `startsWith` is brittle against real-world
  framing junk (escape sequences, banners, partial lines). Match the expected token shape.
- The cryptographic pipeline built in first-light was sound end to end; the only defect at
  the web layer was presentation-side parsing. Worth remembering which layer a failure is
  actually in before "fixing" the wrong one.

## Personal-monopoly note
The moat isn't locking an ATECC or writing a verifier — many can. It's showing the **entire
chain of trust, honestly, with the limits marked**, such that a non-expert confirms it in
their own browser. `/start` is that, public: plug in, press, watch your own machine verify,
read a verdict that refuses to claim more than was proven.

## Artifacts produced (deployed)
- `~/verifyknot-site/start/index.html` — the live-device Web Serial verification page
- (reuses) `~/verifyknot-site/verifier.js` — unchanged verdict engine
- Live: `https://verifyknot.io/start/`

## Open threads
- [ ] **PAT-001 overclaim sweep** — kill the legacy line "Remote/automated signing is
      impossible by hardware design" wherever it's still public (`index.html` grep was
      clean; check zknot.io marketing + zknot-api). Replace with: "A deliberate human press
      is required, enforced by immutable firmware — not claimed to be physically impossible."
- [ ] **Swap `pubkeyForSerial()` to live `api.zknot.io`** once unit count makes per-unit
      redeploys painful (pairs with ZK-LocalChain `/v1/verify`).
- [ ] **Host-relay /start variant** — the headless complement to Web Serial (productionize
      `verify_unit.py` as the automated path).
- [ ] Pixel-match the `/start` nav to the full `index.html` nav (only had the first 80 lines
      when building).
- [ ] **Vault tree reconciliation** (carried from first-light) — the half-done P-/S-
      migration; deliberate session + its own journal entry.
