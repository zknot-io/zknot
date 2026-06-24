---
date: 2026-06-24
topic: attestor-seed-r1-firmware-bringup
workstream: fw / hw / ops
doc_id: JRNL-2026-06-24-SEEDR1-BRINGUP
status: complete
operator: William Shane Wilkinson
applies_to: Attestor-seed-r1 (Seeed XIAO RP2040 + ATECC608B-SSHDA)
references:
  - SOP-ATTESTOR-001 (Rev2 Attestor Build & Test SOP)
  - DOC-FW-SEEDR1-001 (XIAO firmware bring-up doc)
  - attestor_provision.py / verify_unit.py (P-Attestor/scripts)
  - atecc-provisioning-ledger.psv (P-ZKKEY)
  - commits: 154d6e3 (ledger), e9a462f (fw+doc), d08a32a (fw fix)
---

# Attestor-seed-r1 — Firmware Bring-up to First Verified Signature

## TL;DR

The Attestor-seed-r1 (Seeed XIAO RP2040 + ATECC608B) is **proven**: it produces
ECDSA-P256 signatures that verify against its enrolled public key in the pushed
ledger. Stage D passed — four independent button presses, four `[PASS]` from
verify_unit.py, distinct challenge each time (rules out replay). The chip signing
(serial 0123D8623398C140EE) is one of the three provisioned bare on the FT260 rig
earlier the same day (ledger row 7) — closing the full loop: sealed on the bench
-> reflowed/wired on the board -> signing -> verified against its own enrolled key.

The firmware is written, committed, and pushed (CircuitPython, board-matched pins
from the netlist). The provenance gap that opened the day — XIAO signing firmware
that had never been written or committed — is closed.

## What was accomplished

1. Three ATECC608B provisioned + sealed + ledger-pushed (rows 6/7/8, separate
   journal JRNL-2026-06-24-ATTESTOR-PROV).
2. XIAO firmware ported from the proven Pico code.py: crypto path preserved
   verbatim, board layer (PINS dict, button pull) rewritten from the seed-r1
   netlist. Committed + pushed.
3. CircuitPython 10.2.1 (Seeed XIAO RP2040 build) flashed; adafruit_atecc +
   adafruit_bus_device + adafruit_binascii libs installed (version-matched 10.x
   bundle).
4. Stage D: BOOT serial=0123D8623398C140EE selftest=PASS, then 4x [PASS] on
   verify_unit.py. Unit proven.

## Pin map (locked from Attestor-seed-r1-netlist.net, U1 = XIAO)

| Function | Net | XIAO | board.* | GPIO |
|----------|-----|------|---------|------|
| I2C SDA  | /SDA   | D4 | board.SDA | GP6 |
| I2C SCL  | /SCL   | D5 | board.SCL | GP7 |
| Button   | /BTN   | D0 | board.D0  | GP26 (ext pull-up R7 + debounce C3) |
| READY (green) | /LED_G | D1 | board.D1 | GP27 |
| ARMED (blue)  | /LED_B | D3 | board.D3 | GP29 |
| BUSY (yellow) | /LED_Y | D2 | board.D2 | GP28 |
| DONE (red)    | /LED_R | D6 | board.D6 | GP0 |

## Decisions

1. **Runtime: CircuitPython** (not Arduino). Source stays readable and
   copyable off the device; a runtime whose source can't silently become an
   unreadable binary is itself a provenance control.
2. **Firmware lives in git, board-matched.** The committed code.py is now the
   XIAO port (board.SDA), not the stale Pico file. Repo is source of truth.
3. **Button uses external pull (pull=None)** — matches R7/C3 on the PCB, not the
   Pico's internal pull.
4. **DONE = red LED** — forced by available colors (board has R/G/B/Y, one each);
   cosmetic, remappable in one line.

## Debugging chain (root causes, so they don't cost an afternoon twice)

1. **Empty $LEDGER -> stdin hang.** Stage-A integrity `find` searched P-Attestor;
   the ledger lives in P-ZKKEY. Empty var made awk read stdin and hang. Fix:
   hardcode ~/ZKNOT/P-ZKKEY/atecc-provisioning-ledger.psv.
2. **GPG "Bad passphrase".** pinentry had no TTY. Fix: export GPG_TTY=$(tty);
   gpgconf --kill gpg-agent; re-commit. (Add GPG_TTY to ~/.zshrc — action item.)
3. **Misleading push success.** A clean `A..B main->main` shipped an older
   unpushed commit, not the ledger. Lesson: verify origin/main top commit +
   --show-signature, don't trust the push line.
4. **Wrong-board firmware in repo.** The repo code.py was the Pico version
   (board.GP4); the XIAO had no GP15/GP4. Symptom looked like many things
   (REPL drops, AttributeError GP4) — root cause was the committed file.
5. **BOOTSEL entry.** Double-tap RESET failed repeatedly; the documented Seeed
   method (hold BOOT through replug) caught it. dmesg storm-stop + Mass Storage
   line = confirmed bootloader.
6. **lib/ vs requirements/ dependency hunt.** adafruit_atecc needs
   adafruit_binascii (single .mpy in lib/) + adafruit_bus_device. A lib/*-only
   extract and wrong path assumptions caused repeated identical ImportErrors.
   Lesson: same error after a "fix" = the fix didn't land; verify the file is on
   the board, not just that cp returned 0.
7. **Flaky CIRCUITPY drive.** Failed writes + board re-enumeration corrupted the
   FAT ("No space" / I/O error were the corrupted-mount lying, not real). Fix:
   lazy umount + remount; copy then umount-to-flush then remount-to-verify.
8. **ROOT CAUSE of the long tail: non-unique download filename.** A generic
   "code.py" download collided with stale code.py variants in 00_INBOX; the mv
   grabbed the wrong one, so every subsequent "copy succeeded, nothing changed"
   traced back to copying the wrong file. STANDING RULE NOW: every downloaded
   file gets a unique qualified name (board/version/type/date), never a bare
   reused name.

## Verification evidence

```
BOOT serial=0123D8623398C140EE selftest=PASS
[PASS] 0123D8623398C140EE  challenge=5dc37773d8d6...
[PASS] 0123D8623398C140EE  challenge=58c74d44bd55...
[PASS] 0123D8623398C140EE  challenge=7699f448ce15...
[PASS] 0123D8623398C140EE  challenge=acedd1134974...
```

Distinct challenge per press = fresh signatures, not replay. Serial matches
ledger row 7 (provisioned + pushed 2026-06-24 07:22). Adversarial verifiability
demonstrated: a third party holding only the ledger can verify these signatures
without trusting ZKNOT, the board, or the operator.

## Action items

- [ ] Add `export GPG_TTY=$(tty)` to ~/.zshrc (permanent fix for signed commits).
- [ ] Patch SOP-ATTESTOR-001 §8: canonical ledger path = P-ZKKEY (not P-Attestor).
- [ ] Commit the working lib set reference (CP 10.2.1 + adafruit_atecc +
      adafruit_bus_device + adafruit_binascii) into the bring-up doc so the
      buildable unit is fully reproducible from git.
- [ ] Optionally provision rows 6 + 8 onto boards and run Stage D (only row 7
      proven so far).
- [ ] In-circuit provisioning path for reflowed carriers (still open).
- [ ] Vault-reorg reconciliation pass (working tree still drifting).

## Note

Three of today's commits are signed and on origin/main: 154d6e3 (ledger),
e9a462f (fw+bring-up doc), d08a32a (fw fix). The durable, irreversible work —
provisioned chips and committed firmware — is banked.
