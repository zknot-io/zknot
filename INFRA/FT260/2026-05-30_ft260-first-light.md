---
date: 2026-05-30
topic: ft260-first-light
workstream: hw
tags: [ft260, atecc608, provisioning, cryptoauthlib, bench]
status: milestone
---

# FT260 → ATECC608 first light

## TL;DR
Took the FT260 USB-I²C bridge from "nothing detects" to **six genuine ATECC608 parts
verified alive** (valid `0123…ee` serials, all read-only). Settled the HAL question:
the in-tree `hid_ft260` kernel driver exposes the bridge as `/dev/i2c-6`, so
cryptoauthlib's stock Linux I²C HAL works directly — **no custom HAL needed** (Path A,
not the Path B the session assumed). Root cause of the long dead-bench stretch was a
**physical connection**, not software. Durable mechanics promoted to
`km/systems/ft260-provisioning.md`.

## Decisions
- **HAL = Path A (stock kernel `/dev/i2c-6`).** Path B (custom HAL over libft260/hidraw)
  is shelved as a fallback only; it was never required.
- **Part choice = SSHDA (SOIC-8, I²C).** SSHCZ (`C` = single-wire) is the trap and is
  excluded; UDFN (MAHDA) excluded for hand-soldering — reflow only.
- **Address = 8-bit `0xC0`** (7-bit `0x60` << 1) for this batch.
- **Provenance recorded:** all parts answer at non-default `0x60` → preconfigured before
  receipt. Fine for the open/educational tier; flagged for config-zone read before any
  write. Not to be treated as trust-critical parts.
- **No locks issued.** Everything this session was read-only.

## What happened
- Bridge enumerated clean: `hid_ft260` loaded, FT260 on `input0` (I²C) / `input1` (UART),
  cooked adapter at `/dev/i2c-6`. Board EEPROM ACKs at `0x50` — used that as the
  bus-health tell throughout.
- Long stretch of blank scans + `ATCA_COMM_FAIL` across several chips. Chased it in
  software (clock/sysfs) longer than warranted; the evidence was pointing at the bench.
- Once the physical connection was fixed, the target ACKed at `0x60` immediately and
  `alive.py` returned a real serial. Repeated across the batch: six distinct serials.
- Soldering the bare SOIC-8 by hand was failing (blobbing on drag) — switched approach;
  the takeaway is to use a clip/socket for a provisioning workflow rather than burning a
  part per attempt.

## Lesson (the one worth keeping)
Five-plus identical failures = **one systematic cause**, not five dead parts. The
convenient next move was always another command, because that's the layer where the
assistant is most useful — but the unmeasured physical layer was the actual blocker.
**Let bench evidence override the convenient software move.** A marginal joint produces
a perfect impersonation of a software bug.

## Open items
- [ ] Read config zone on one part (reversible) — see what the preconfiguration is.
- [ ] Read back actual FT260 I²C clock rate via sysfs (input0 node); confirm 100 kHz.
- [ ] Decide slot-config recipe; version-control the recipe (never secrets) before any lock.
- [ ] Mechanical: settle on SOIC-8 clip vs socket for the batch workflow.

## Backup / VC status
- Serials = device identifiers, not secrets → safe in the systems doc under git.
- Nothing irreplaceable created this session (all reads). The first irreversible moment
  is the zone lock, which is gated behind explicit confirmation.
