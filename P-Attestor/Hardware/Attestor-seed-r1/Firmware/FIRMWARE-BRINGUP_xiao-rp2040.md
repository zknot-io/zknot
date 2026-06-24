---
doc_id: DOC-FW-SEEDR1-001
title: Attestor-seed-r1 (XIAO RP2040) — Firmware Bring-up & Provenance
status: controlled-draft
rev: A
workstream: fw / hw / ops
applies_to: Attestor-seed-r1 carrier, Seeed XIAO RP2040 (RP2040, CircuitPython)
references:
  - SOP-ATTESTOR-001 (Rev2 Attestor Build & Test SOP)
  - attestor_provision.py (P-Attestor/scripts) — chip provisioning
  - verify_unit.py (P-Attestor/scripts) — functional-test verifier
  - atecc-provisioning-ledger.psv (P-ZKKEY) — serial <-> pubkey record
  - Attestor-seed-r1-netlist.net — authoritative pin map source
drafted: 2026-06-24
operator: William Shane Wilkinson
location: ~/ZKNOT/P-Attestor/Hardware/Attestor-seed-r1/Firmware/FIRMWARE-BRINGUP_xiao-rp2040.md
note: Markdown is the editable master. Controlled/signable version is this rendered
      to PDF with "Page X of Y" footers and an operator signature block (Section 9).
---

# Attestor-seed-r1 (XIAO RP2040) — Firmware Bring-up & Provenance (Rev A)

## 0. Why this document exists (the lesson that produced it)

On 2026-06-24, a bench session to "get the XIAO signing" surfaced a provenance
gap in our own tooling: **the XIAO signing firmware had never been written or
committed.** The board on the bench was running a stale, crash-looping artifact of
unknown origin; the only `code.py` in the repo was pin-mapped for a Raspberry Pi
Pico (GP4/GP5/GP15), not the XIAO; and the `attestor-rev2-u535` directory was an
STM32 CubeMX generator for different silicon entirely.

The finding is the point: a company whose product is **verifiable provenance** had
an attestor whose firmware had no provenance — not in git, not reproducible, not
attestable. This document and the firmware it governs close that gap. The governing
rule going forward:

> **Firmware that runs an attestor must live in version control, as readable source,
> with a known runtime version — never as a board-only binary.** If it only exists
> on the device, it does not exist.

---

## 1. Hardware identity (and the Pico trap)

- Board: **Seeed Studio XIAO RP2040** — USB-C, ~21 x 17.5 mm, castellated edges,
  silk pads D0-D10 plus 3V3/GND/5V.
- The RP2040 *silicon* is identical to a Raspberry Pi Pico, but the **board is not**:
  different silk labels, different default `board.*` pin aliases, fewer broken-out
  GPIO, and **no GP15** (the Pico firmware's button pin). Pico firmware flashed to a
  XIAO faults at import on the missing pin.
- Consequence: firmware pin maps are **board-specific**. The XIAO `PINS` map is
  derived from the seed-r1 PCB netlist (Section 4), not copied from the Pico SOP.

---

## 2. Runtime decision — CircuitPython

**Decision: CircuitPython (8.x), not Arduino.** Rationale, both sides recorded:

- **For CircuitPython:** source (`code.py`) stays human-readable *and lives on the
  device as a file you can copy back off* — structurally prevents the "firmware is a
  binary nobody can read" failure that produced this doc. Matches the existing repo
  `code.py` lineage and the Adafruit ATECC library path already used in the SOP.
  Fast iterate-flash-test loop.
- **Against / for Arduino:** Arduino compiles to a single `.uf2` — smaller, faster
  at runtime, but **opaque**: if the `.ino` source is ever lost, the firmware is
  unrecoverable from the board. That is the exact trap we are exiting. Rejected for
  the attestor role on provenance grounds.

CircuitPython is chosen specifically because a runtime whose source *cannot silently
vanish* is itself a provenance control.

---

## 3. Tier & scope (unchanged from SOP-ATTESTOR-001)

- Tier-0 self-assertion. Device-bound / presence-style signing only.
- Button press = human-actuation gate ("sign now"). The ATECC slot-0 private key
  signs a host-issued challenge; the signature is emitted over USB serial.
- A unit **passes only if its signature verifies against its own enrolled public
  key** (the ledger row). LEDs are indicators, not the pass criterion.

---

## 4. Pin map  [TO LOCK FROM NETLIST]

The seed-r1 PCB is fabricated; pins are fixed by the layout. The authoritative
source is `Attestor-seed-r1-netlist.net`. Extract with:

```
cd ~/ZKNOT/P-Attestor/Hardware/Attestor-seed-r1
python3 - <<'PY'
import re
t = open('Attestor-seed-r1-netlist.net').read()
for m in re.finditer(r'\(net \(code[^)]*\) \(name "([^"]+)"\)(.*?)(?=\(net \(code|\Z)', t, re.S):
    name, body = m.group(1), m.group(2)
    nodes = re.findall(r'\(node \(ref "([^"]+)"\)\s*\(pin "([^"]+)"\)(?:\s*\(pinfunction "([^"]+)"\))?', body)
    print(f'{name:24} -> ' + ', '.join(f'{r}.{p}' + (f'({f})' if f else '') for r,p,f in nodes))
PY
```

Fill this table from the output, then transcribe into `code.py` `PINS`:

| Function | Net name | XIAO silk | board.* alias | GPIO |
|----------|----------|-----------|---------------|------|
| I2C SDA  | _TBD_ | _TBD_ | `board._____` | _TBD_ |
| I2C SCL  | _TBD_ | _TBD_ | `board._____` | _TBD_ |
| Button   | _TBD_ | _TBD_ | `board._____` | _TBD_ |
| LED READY| _TBD_ | _TBD_ | `board._____` | _TBD_ |
| LED ARMED| _TBD_ | _TBD_ | `board._____` | _TBD_ |
| LED BUSY | _TBD_ | _TBD_ | `board._____` | _TBD_ |
| LED DONE | _TBD_ | _TBD_ | `board._____` | _TBD_ |

> Note: XIAO RP2040 default I2C is `board.SDA` / `board.SCL` (silk D4/D5 = GP6/GP7).
> Confirm against the netlist — do not assume.

---

## 5. Dependencies (version-pinned, committed)

1. **CircuitPython UF2 — Seeed XIAO RP2040 build.** Source:
   circuitpython.org/board/seeeduino_xiao_rp2040/ (8.x stable). Record the exact
   version in Section 9; the library bundle below must match this major version.
2. **`adafruit_atecc` library.** Source: the Adafruit CircuitPython **Library
   Bundle** matching the CircuitPython major version (NOT scavenged from another
   board — a board-sourced lib of unknown version reintroduces the provenance gap).
   Commit `lib/adafruit_atecc/` into the repo alongside `code.py`.

**Buildable-unit rule:** `code.py` + `lib/adafruit_atecc/` + the recorded CP version
must all be in git, so any future board is reproducible from the repo alone.

---

## 6. Flash procedure

1. Double-tap the XIAO RESET to enter BOOTSEL (also stops any crash-loop). The board
   mounts as `RPI-RP2`.
2. Drag the Seeed XIAO RP2040 CircuitPython `.uf2` onto `RPI-RP2`. It reboots and
   mounts as `CIRCUITPY` (Trixie auto-mount: `/run/media/$USER/CIRCUITPY`).
3. Copy dependencies and source:
   ```
   CP=/run/media/$USER/CIRCUITPY
   cp -r <repo>/lib/adafruit_atecc "$CP/lib/"
   cp <repo>/code.py "$CP/"
   sync
   ```
4. The board reboots and runs `code.py`.

**Flash pass:** firmware loads with no CircuitPython traceback on the serial console.

---

## 7. Boot & functional test (Stage D — the real test)

Close any serial monitor before running the verifier (a monitor holds `/dev/ttyACM*`
exclusively; the verifier needs it). Note: opening the port may reset the board
(DTR) — expect a re-enumeration, then the banner.

| Step | Action | Pass criterion |
|------|--------|----------------|
| D1 | Power on / soft-reboot, watch serial | `BOOT serial=<...> selftest=PASS`; READY LED solid within ~3 s |
| D2 | Confirm serial enrolled | BOOT serial matches a row in the pushed ledger |
| D3 | Press the button once | ARMED off -> BUSY on -> DONE pulses -> ARMED back on |
| D4 | Verifier output | `python3 verify_unit.py` prints `[PASS] <serial> challenge=...` |
| D5 | Repeat D3-D4 x3 | three independent presses, three `[PASS]` |

**Unit passes only if D1-D5 all pass.** A lit DONE LED without a verifier `[PASS]`
is a FAIL — the LED is a local indicator; the verifier is the truth.

The chip on this board was provisioned via `attestor_provision.py` and its serial +
128-char pubkey recorded in `atecc-provisioning-ledger.psv` (P-ZKKEY). D2 closes the
loop: the board signs, the verifier checks the signature against the *enrolled* key.

---

## 8. Provenance checklist (commit before declaring bring-up done)

- [ ] `code.py` committed to `P-Attestor/Hardware/Attestor-seed-r1/Firmware/` (or
      `P-Attestor/Firmware/xiao-rp2040/`), signed commit.
- [ ] `lib/adafruit_atecc/` committed alongside.
- [ ] CircuitPython version recorded in Section 9.
- [ ] Pin map table (Section 4) filled from the netlist and matching `code.py`.
- [ ] One unit driven through D1-D5 with three `[PASS]`; result logged (Section 9).
- [ ] No firmware exists only on a board: `git` is the source of truth.

---

## 9. Bring-up record

| Field | Value |
|-------|-------|
| CircuitPython version flashed | __________ |
| adafruit_atecc bundle version | __________ |
| Board chip serial (BOOT)      | __________ |
| Ledger row matched            | __________ |
| D1-D5 result                  | __________ |
| Firmware commit hash          | __________ |

Operator signature (controlled PDF): __________________________  Date: __________

---

## 10. Revision history

| Rev | Date | Change |
|-----|------|--------|
| A | 2026-06-24 | Initial bring-up doc: runtime decision (CircuitPython), provenance rule, dependency sourcing, flash + Stage-D procedure. Pin map flagged TO-LOCK pending netlist. |
