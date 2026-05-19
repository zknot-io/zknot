# Lesson — software first, hardware later
## 2026-05-19

## The trap
Spent ~3 days assuming Rev 0 needed hardware-protected keys to ship. Bricked two
ATECC608B chips trying to provision on a Pico breadboard before realizing that
software signing satisfies enough of the patent claims (PAT-006 FSM, PAT-007 ZK
number, PAT-001 §§6-7) to be a legitimate Rev 0 embodiment. The only missing
claim is PAT-001 §4 (hardware-protected private key) — and that's a Rev 1
upgrade, not a Rev 0 blocker.

## The realization
"I should've done a software sign a long time ago and just got moving."
Marking the firmware version (`fw: "0.1-pc-keys"`) on every artifact gives
forensic auditability later: any verifier can distinguish software-signed
Rev 0 artifacts from ATECC-signed Rev 1+ artifacts.

## Policy that makes this OK
Early customers get free Rev 1 swap when ATECC-backed firmware ships. This is
standard for security-grade hardware shipped pre-1.0 — customers know they're
buying into a product on the way to v1, not v1 itself.

## Rule for future revisions
1. Identify the smallest set of patent claims that constitute a legitimate
   embodiment.
2. Ship that set if it unblocks the business goal.
3. Tag the firmware version on every artifact so the difference is auditable.
4. Reserve "full embodiment" for the production revision.

## What I won't repeat
- Don't gate Rev 0 shipping on Rev 1+ component reliability
- Don't burn chips trying to provision in conditions known to be marginal
  (breadboard + CRC mismatch documented in adafruit_atecc GitHub issues)
- Software-first when there's any uncertainty about hardware integration timeline

## Carryforward
Software signer at ~/.zkkey/, signing today. ATECC migration deferred to
MCP2221 arrival + Pimoroni Pico Plus 2 + decoupling caps + Saleae bus capture.
Patent embodiment migration: 0.1-pc-keys -> 0.2-atecc-pico -> 1.0-atecc-pcb.
