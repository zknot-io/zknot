# 2026-05-22 — PowerVerify New Rev: Design Review, eFuse Selection, Comparator, Validation

**Workstream:** hw
**Status:** Design decisions locked; next step is KiCad schematic capture for two board variants.

---

## Big-picture context

PowerVerify (the PUF product line that has the secure-element verification path) is getting a new
hardware rev focused on the **power-only USB-C passthrough dongle**. The pitch is a trust device:
unknown/hostile cable or charger → PowerVerify → phone, with **data physically absent** and a clear
visual signal of safe power. Two board variants decided:

- **Rev Passive (PV-PASSIVE-001)** — ship-fast validation board. VBUS/GND/CC passthrough, no data,
  green LED = VBUS present. Does NOT know direction.
- **Rev Guided (PV-GUIDED-001)** — consumer-ready. Directional, reverse-blocking eFuse on VBUS,
  green LED on VBUS_OUT (power actually delivered), no red LED in Rev 1.

Key constraint confirmed: once you add direction awareness, VBUS **cannot** be a straight wire —
both sides would see the same voltage and the board couldn't tell which side powered it. Guided
requires an active VBUS gate with reverse-current blocking. VBUS_IN and VBUS_OUT must be separate nets.

---

## Plan review — what's good, what changed

**Good as-is:** Splitting Passive vs Guided is correct (different jobs). "No data copper + silkscreen
says so" is a real part of the trust story, keep it.

**Changes pushed into the plan (do NOT lose these):**

1. **LED resistor → constant-current driver.** The proposed flat 10kΩ resistor makes the green LED
   ~4–5× brighter at 20V than at 5V. Users will misread "brighter = more correct." Use a 2-pin
   constant-current LED driver (CCL, ~SOT-23, cheap) so brightness stays flat across 5–20V PD range.
   This matters because the whole product is unambiguous visual feedback.

2. **Keep F1 polyfuse on Passive even for prototypes.** Upstream cable is unknown/potentially hostile;
   a shorted/malicious cable dumping current through our board with our name on it is the exact failure
   mode to avoid. F1 is cheap. Do not omit.

3. **Two TVS diodes, not one.** ESD can come from either connector on an inline device. Put TVS near
   J1 AND near J2. Use ~24V working-voltage TVS (NOT 5V — must survive 20V PD). Pennies.

4. **CC ESD protection = required, not optional.** CC pins are most ESD-vulnerable (low-voltage logic
   the user touches when mating).

5. **VBUS pour width: give it a number.** For 3A at 10°C rise on 1oz outer copper, ~50 mil minimum.
   Put it in the layout rules so future-me doesn't squeeze it. CC traces can stay thin (6–10 mil).

6. **Red LED — decision: DEFER to Guided Rev 2.** "No green" alone is ambiguous to a user (wrong way?
   dead cable? broken board?). Red specifically says "flip it." BUT the comparator network adds ~12
   parts. Decision: ship Guided Rev 1 with reverse-blocking + green PG-driven, validate eFuse is rock
   solid, then add red in Rev 2. Cost of deferral = one extra board spin (~$50 + ~1 week). Worth it
   for a cleaner first guided board.

---

## eFuse selection — DECIDED

**Part: TPS259472ARPWR** (Texas Instruments)

- Family TPS25947: 2.7–23V, 5.5A, 28mΩ, **true reverse-current blocking always-on**, reverse polarity
  protection, integrated back-to-back FETs, 2×2mm 10-pin HotRod QFN.
- Max input rating 28V — correct for USB-C PD (20V ceiling). Note: TPS2595 only goes to 20V → too
  close to the PD ceiling, rejected.
- Variant logic:
  - '470x = aux channel output (don't need)
  - **'472x = pin-selectable OV clamp (3.8/5.7/13.8V, 5µs response) + Power Good output ← CHOSEN**
  - '474x = adjustable OVLO + Power Good
- Why '472: the **Power Good (PG) open-drain output** is the right signal to drive the green LED — PG
  asserts only when the path is fully on and output exceeds threshold = real "power delivered" signal,
  not just "VBUS exists somewhere."
- Suffix: **'A' = latching fault** (chosen, want it to stay off until user re-mates). 'L' = auto-retry
  (rejected).
- Stock/price: TPS259470ARPWR showed 12,243 in stock at Digi-Key ~$1.48/1, ~$0.87/100. '472 should be
  similar — VERIFY '472 stock before committing footprint. Budget ~$1.50/board at proto qty.
- **TPS25947EVM** exists at Digi-Key (~$50) — option to test the part on TI's board before designing in.
- Follow datasheet exactly for EN resistor divider (sets UVLO), ILIM resistor (sets current limit),
  and C_IN/C_OUT.

---

## Comparator network for red LED (Guided Rev 2 — reference, not building yet)

Logic: **Red ON when VBUS_OUT > ~2V AND VBUS_IN < ~2V** (phone-side powered, charger-side not = wrong way).

- VBUS_OUT through R1=100k / R2=10k divider (÷11) → COMP+ . At 5V→0.45V, at 20V→1.82V.
- VBUS_IN through R4=100k / R5=10k divider (÷11) → COMP− . Identical.
- Comparator output HIGH when COMP+ > COMP− (output side has more voltage than input side).
  - Correct direction: COMP+ ≤ COMP− → red OFF.
  - Wrong direction: VBUS_IN=0, VBUS_OUT=phone backfeed → COMP+ >> COMP− → red ON.
- Comparator powered from whichever side has voltage via Schottky-OR (D1/D2) into a small 3.3V LDO.
- **Hysteresis REQUIRED:** 1MΩ feedback from COMP_OUT to COMP+ to stop flicker as VBUS_IN ramps at plug-in.
- Suggested comparator: **TLV7011DBVR** — single ch, SOT-23-5, ~$0.40/1, 1.6–5.5V supply, push-pull,
  ~3µs. Pair with MCP1700T-3302E (or similar) 3.3V LDO.
- Red LED + R_RED ~4.7k on comparator output.
- Total adder: ~6 passives + comparator + LDO + 2 Schottky + red LED ≈ 12 parts. (This count is why
  red is deferred to Rev 2.)

---

## Net names (use these in KiCad)

```
VBUS_IN, VBUS_OUT, GND, CC1_PASS, CC2_PASS, LED_GREEN, EN_VBUS
```
- Passive: VBUS_IN / VBUS_OUT joined through F1 (or net tie).
- Guided: VBUS_IN / VBUS_OUT are SEPARATE nets (mandatory).

Silkscreen: D+ ABSENT / D- ABSENT / NO DATA COPPER / POWER ONLY.

---

## Validation strategy (5 layers)

**1. Bench bring-up (every assembled board, do in real life — faster than any doc):**
- Continuity J1_VBUS→J2_VBUS through eFuse (~28mΩ); CC1/CC2 pass.
- **Data open-circuit check (CRITICAL):** D+, D−, SBU1/2, SSTX/RX all pairs J1→J2 should read
  >20MΩ (open). Log actual ohmmeter reading, pass/fail.
- Reverse current: power J2 at 5V, measure leakage back to J1 → should be <1µA.
- PD walk: cycle charger 5/9/15/20V. Green LED steady (CCL driver matters), no eFuse thermal events.

**2. Data-absence verification (the trust claim):**
- Visual: silkscreen callouts + visible trace gaps; photograph for product literature.
- Electrical: document the open-circuit ohmmeter procedure as a 30-sec QC step, log every board.
- Optional/powerful: X-ray a few per batch to confirm no hidden data copper.

**3. Adversarial cable tests (differentiator):**
- O.MG cable (Hak5, ~$180), generic no-name cables, known-good Apple/Anker control.
- Through PowerVerify into sacrificial phone or USB-C analyzer (Total Phase Advanced Cable Tester if
  borrowable). Confirm data dead, power flows, phone says "charging only."
- Photos + short video worth more than a spec sheet to customers.

**4. PD compatibility matrix:**
- Likely no full USB-IF cert needed (passive power-only), but test ≥5 PD chargers (Apple 20W, Anker
  GaN, Google, generic, laptop USB-C) × ≥5 devices. Document the matrix.

**5. Production QC per board:** visual inspect, continuity (VBUS/GND/CC pass, data open), live test
(known charger→known phone, green + charges), serialize and log.

**Doc to write:** ZKNOT-DOC-PWR-001 "PowerVerify Hardware Validation Procedure v1.0" — lives alongside
the PUF verification doc (ZKNOT-DOC-PUF-001). The published validation procedure becomes part of the
trust story (Signal-publishes-its-protocol logic).

---

## Next actions

- [ ] Verify TPS259472ARPWR live stock at Digi-Key before locking footprint.
- [ ] (Optional) Order TPS25947EVM to bench-test the part.
- [ ] KiCad: capture PV-PASSIVE-001 schematic (VBUS/GND/CC passthrough, F1, 2× TVS, CC ESD, green
      LED via CCL driver, data NC + silkscreen).
- [ ] KiCad: capture PV-GUIDED-001 schematic (TPS259472A eFuse, EN divider + ILIM per datasheet,
      C_IN/C_OUT, green LED on VBUS_OUT driven from PG, no red).
- [ ] Source O.MG cable + cable set for adversarial testing.
- [ ] Draft ZKNOT-DOC-PWR-001 validation procedure.
- [ ] Decide red-LED comparator goes to Guided Rev 2 (confirmed deferred).

---

## Open questions / watch-items

- Confirm '472 (vs '474) is right once datasheet PG threshold section (8.3.11) is read against the
  green-LED turn-on point you actually want.
- CCL constant-current LED driver: pick a specific part + verify current is visible-but-safe across
  5–20V.
- Mind the SBIR Phase I deadline (June 3) — make sure this hardware work doesn't crowd it out.
