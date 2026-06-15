---
date: 2026-06-14
topic: attestor-seed-r1-review
version: 3
variant: seeed-xiao
related: 2026-06-13_attestor-first-light   # sibling (Pico breadboard), NOT lineage
workstream: hw
tags: [attestor, seed-r1, xiao-rp2040, atecc608b, kicad, decoupling, eco, island-net, drc, erc]
status: resolved
---

# Rev2 Attestor — Seed-r1 (Seeed/XIAO "PRESENCE-TIER") review + ECO, resolved

## TL;DR
Reviewed `Attestor-seed-r1` (Seeed XIAO RP2040 variant, "PRESENCE-TIER"). Board was fully
routed and ERC-clean, but a schematic review found the ATECC608B (U3) had **no decoupling
cap**. Added decoupling (C1 100nF + C2 1µF) and hardened the actuation line (R7 10k pull-up
+ C3 debounce). **A pin-by-pin netlist trace then caught that all four added parts had formed
auto-named "island" nets** — U3's VCC was stranded (ATECC unpowered) and the button was
non-functional — a class of error DRC's "0 unconnected" reports as clean. Fixed in the
schematic via explicit net labels, pushed to PCB (F8), re-routed, and re-verified in the PCB
file itself. **End state: ERC 0, no island nets in schematic or PCB, 0 unconnected, only two
benign `lib_footprint_mismatch` warnings remain (ignore-for-fab). Board is fab-ready.**

> Standalone variant. The Pico build is a separate parallel track (split because doing both
> together got too complex). First-light (2026-06-13) was the Pico breadboard — sibling, not
> parent. No cross-build regression reasoning applies.

## Decisions
- **ATECC decoupling — done.** C1 = 100nF X7R 0603 and C2 = 1µF X7R 0603, both VCC↔GND at U3.
  Datasheet-mandated; stands on the ATECC608B's own requirements.
- **Actuation hardened — done.** R7 = 10k pull-up (`/3V3`↔`/BTN`) for a hardware-defined idle;
  C3 = 100nF debounce (`/BTN`↔`GND`). RC ≈ 1 ms.
- **Connect new parts with net labels, not drawn wires.** Root cause of the island-net bug:
  the four hand-added parts were tied to rails with wires that didn't land, creating orphan
  nets. The existing rails (SDA/SCL/LEDs) used labels and were clean. Standing rule: power,
  ground, and shared signals get explicit net labels.
- **Footprint mismatches — ignore for this fab, push board→library after.** The U1/S1
  `lib_footprint_mismatch` warnings are sync notices; the validated board instances are the
  source of truth for these custom footprints.
- **Verify connectivity in the PCB artifact, not the schematic.** A correct schematic does not
  imply correct copper; confirm island nets are absent in `.kicad_pcb`, not just `.kicad_sch`.

## What happened (the sequence worth keeping)
1. Schematic review (ERC clean, board fully routed: 114 seg / 16 via / 0 unrouted) found
   **zero capacitors** — U3 had no decoupling. Flagged as the one mandatory fix.
2. Added C1, C2, C3, R7. DRC came back 0 unconnected → looked done.
3. **Netlist trace (not DRC) caught the real problem:** all four parts had formed island nets.
   - `Net-(U3-VCC)` = U3.8 + C2.2 → ATECC VCC reached 3V3 only through C2 in series (DC block)
     → **chip unpowered**. (This was the true cause of the `power_pin_not_driven` ERC error,
     not a missing PWR_FLAG.)
   - `Net-(U1-P26/A0/D0)` = U1.1 + R7.2 → MCU input not on `/BTN`; R7 in series, not a pull-up.
   - `Net-(C3-Pad2)` = C3.2 + S1.1/S1.2 → switch's ground terminal reached GND only through C3
     → **button can't pull BTN low**.
4. Fixed with explicit net labels (U3.8→/3V3, C2.2→GND, U1.1→/BTN, R7.2→/3V3, S1.1/2→GND,
   C3.2→/BTN). ERC → 0, island nets gone.
5. Pushed to PCB (F8), re-routed the changed nets, re-verified **in the PCB file**:
   `grep` for island net names in `.kicad_pcb` → 0. DRC → 0 unconnected, 2 benign warnings.

## Final verified state
- **ERC:** 0 violations.
- **Schematic rails (traced):**
  - `/3V3`: C1.2, C2.2, R1.1, R2.1, R7.2, U1.12, U3.8
  - `/BTN`: C3.2, R7.1, S1.3, S1.4, U1.1
  - `GND`: C1.1, C2.1, C3.1, D1–D4 cathodes, S1.1, S1.2, U1.13, U3.4
- **PCB:** 0 island nets present, 0 unconnected. Remaining: 2× `lib_footprint_mismatch`
  (U1 `MODULE_102010428`, S1 `SW_TL1100F160Q`) — cosmetic, ignore-for-fab.
- **Board:** Seeed XIAO RP2040 (U1, Seeed `102010428`) + ATECC608B-SSHDA (U3), 4 status LEDs
  (G/Y/B/R), tactile button (S1), 2-layer, user-facing front silk.

## Open threads
- [ ] **Silkscreen polish** — text ≥0.8mm, clear U1/S1 overlaps + edge clipping. Front silk is
      user-facing product copy ("PRESENCE-TIER", "Prove this moment. Anyone can check.",
      "verifyknot.io/start", LED state labels), so it's worth doing before fab.
- [ ] **Footprint sync** — push U1/S1 board footprints to the `attestor` library (cleanup).
- [ ] **ATECC provisioning path for assembled seed-r1** *(confirm)* — no FT260 on this board;
      decide pre-assembly jig vs. XIAO-hosted provisioning over native USB before a build SOP.
- [ ] **Promote the verification awk into the vault** as a standing pre-fab gate (see below).
- [ ] **Pico variant** — its own board + journal when started.
- [ ] **Vault reconciliation** (carried) — KiCad project still under `P-ZKKEY/Attestor`.

## Standing pre-fab gate (save this)
Net-membership trace that catches island nets DRC can't — run on every netlist before fab:
```
awk '
  /\(name "/ {nm=$0; sub(/.*\(name "/,"",nm); sub(/".*/,"",nm)}
  /\(ref "/  {r=$0; sub(/.*\(ref "/,"",r); sub(/".*/,"",r); ref=r}
  /\(pin "/  {p=$0; sub(/.*\(pin "/,"",p); sub(/".*/,"",p); printf "%-8s %s.%s\n", nm, ref, p}
' NETLIST.net | sort
# then: grep -c 'Net-(' to count auto-named (island-suspect) nets in schematic AND .kicad_pcb
```

## Lesson (the one worth keeping)
**DRC "0 unconnected" means every pad is on *a* net, not the *right* net.** Four added parts
all routed clean and still left the ATECC unpowered and the button dead, because each formed an
island net that DRC happily treats as connected. The only thing that caught it was tracing pin
membership against an expected rail list. Two corollaries earned here: (1) tie shared nets with
labels, not wires that can dangle; (2) verify in the artifact that gets manufactured — the PCB —
because a correct schematic says nothing about whether the copper followed.
