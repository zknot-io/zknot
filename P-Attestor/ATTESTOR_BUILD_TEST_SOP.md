---
doc_id: SOP-ATTESTOR-001
title: ZKNOT Rev2 Attestor — Build & Test SOP
status: controlled-draft
rev: A
workstream: hw / ops
applies_to: Rev2 Attestor (breadboard prototype + JLCPCB carrier)
references:
  - attestor_provision.py (P-Attestor/scripts) — provisioning tool
  - code.py — Pico signing firmware
  - verify_unit.py — functional-test verifier
  - atecc-provisioning-ledger.psv — serial↔pubkey record
drafted: 2026-06-13
location: ~/ZKNOT/P-Attestor/ATTESTOR_BUILD_TEST_SOP.md
---

# Rev2 Attestor — Build & Test SOP (Rev A)

Repeatable procedure for building and testing one Attestor unit. The governing
principle: **a unit passes only if it produces a signature that verifies against
its own enrolled public key.** Every test step below ladders up to that single
cryptographic fact — LEDs and buttons are indicators, not the pass criterion.

> Markdown is the editable master. The controlled, signable version is this
> rendered to PDF with "Page X of Y" footers and an operator signature block (§8).

---

## 1. Scope & tier

- Rev2 Attestor, Tier-0 self-assertion. Device-bound / presence-style signing only.
- NOT a ZKKey, NOT the YubiHSM root of trust. Records are self-asserted.
- Applies to the breadboard prototype now and the JLCPCB carrier when populated;
  the provisioning + firmware + test steps are identical across both form factors.

---

## 2. Per-unit BOM

| Item | Qty | Notes |
|------|-----|-------|
| ATECC608B-SSHDA (SOIC-8, I²C) | 1 | order code SSHDA only — SSHCZ is single-wire, will not work |
| Raspberry Pi Pico (RP2040) | 1 | I²C master + button/LED host |
| Resistor 4.7 kΩ | 2 | I²C pull-ups (SDA, SCL → 3V3) |
| Resistor 330 Ω | 4 | LED current-limit (150–220 Ω for blue/white) |
| LED | 4 | READY green / ARMED blue / BUSY amber / DONE green |
| Tactile push button | 1 | momentary, to GND |
| Capacitor 100 nF | 1 | decoupling, ATECC VCC↔GND at the chip |
| SOIC8→DIP8 adapter | 1 | so the SOIC-8 reaches the breadboard (breadboard build) |

---

## 3. Equipment

- Linux host with the P-Attestor venv (`cryptoauthlib`, `cryptography`, `pyserial`).
- FT260 USB-I²C bridge (provisioning only).
- USB cable for the Pico (power + serial).
- ESD precaution when handling the bare ATECC.

---

## 4. Stage A — Provision the secure element (FT260)

Done once per chip, before it goes on the unit. Irreversible; do not batch.

1. Seat the chip on the FT260 rig. `source ~/ZKNOT/P-Attestor/.venv/bin/activate`.
2. `python3 attestor_provision.py read` — require all three green: serial valid
   `0123…EE`, **both zones unlocked**, slot0 `0x2083 / 0x0033`. If not all green,
   reject the chip (do not provision).
3. Record the serial. Then, gated step by step (retype-confirm on each lock):
   `lock-config <serial>` → `genkey <serial>` → `verify <serial>` (must print PASS)
   → `lock-data <serial>` → `record <serial>`.
4. `record` is fail-closed: it writes a ledger row only if both zones are locked
   and a fresh signature verifies. Confirm a clean `PASS | Rev2-Attestor` row.
5. Integrity check + commit:
   `awk -F'|' '/^[0-9]/{gsub(/ /,"",$5); print $1, length($5)}' <ledger>` (all 128),
   then `git add <ledger> && git commit && git push`.

**Stage A pass:** one clean ledger row, pushed, with a 128-char pubkey.

---

## 5. Stage B — Assemble

Wire per the Attestor breadboard diagram (or populate the carrier PCB):

- ATECC pin 8→+3V3, pin 4→GND, pin 5→GP4 (SDA), pin 6→GP5 (SCL); pins 1,2,3,7 NC.
- 4.7 kΩ pull-up on SDA and on SCL, each to +3V3. **Required** — the bare chip has none.
- 100 nF across ATECC pin 8↔4, at the chip.
- LEDs: GP6/7/8/9 → 330 Ω → LED → GND (READY/ARMED/BUSY/DONE).
- Button: GP15 → button → GND (firmware uses the internal pull-up).
- Power the Pico from USB (also the serial link).

**Stage B pass:** continuity check — no SDA/SCL short to GND or each other; 3V3
present at ATECC pin 8; common ground between Pico and ATECC.

---

## 6. Stage C — Flash firmware

1. Install CircuitPython on the Pico (BOOTSEL → drag the UF2).
2. Copy the Adafruit ATECC library folder into `CIRCUITPY/lib/` (`adafruit_atecc/`).
3. Copy `code.py` to `CIRCUITPY/`. The Pico reboots and runs it.

**Stage C pass:** the firmware loads without a CircuitPython traceback on the serial console.

---

## 7. Stage D — Functional test (the real test)

Run the verifier on the host: `python3 verify_unit.py` (auto-detects `/dev/ttyACM*`).

| Step | Action | Pass criterion |
|------|--------|----------------|
| D1 | Power on, watch serial | `BOOT serial=<…> selftest=PASS`; READY LED solid within ~3 s |
| D2 | Confirm serial enrolled | the BOOT serial matches a ledger row (verifier won't verify an unenrolled unit) |
| D3 | Press the button once | ARMED off → BUSY on → DONE pulses → ARMED back on |
| D4 | Verifier output | verifier prints `[PASS] <serial> challenge=…` for that press |
| D5 | Repeat D3–D4 ×3 | three independent presses, three `[PASS]` |

**Unit passes only if D1–D5 all pass.** A lit DONE LED without a verifier `[PASS]`
is a FAIL — the LED is a local indicator, the verifier is the truth. If self-test
fails at D1, the chip/wiring is at fault, not the firmware; re-check Stage B and the
chip's ledger status before re-flashing.

---

## 8. Unit record (log every built unit)

Record, per unit: serial, build date, firmware rev, assembler/operator,
test result (PASS/FAIL), and any rework. The serial links to the pubkey in the
ledger — do not duplicate the pubkey here. Suggested: append to a unit-build log
under `P-Attestor/OPS/` (separate from the chip ledger).

Operator signature (controlled PDF): __________________________  Date: __________

---

## 9. Nonconformance

- Chip not all-green at Stage A read → reject chip, do not provision.
- `verify` FAIL before data-lock → do not seal; quarantine chip, investigate.
- D-stage FAIL → do not ship; rework wiring or re-flash; if the chip itself fails
  to sign post-seal, the chip is scrap (key is permanent) — log and discard.

---

## 10. Revision history

| Rev | Date | Change |
|-----|------|--------|
| A | 2026-06-13 | Initial SOP: provision → assemble → flash → crypto-verified functional test |
