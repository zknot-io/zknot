---
title: WitnessMark Connect v1 — Hardware Design Reference & Pin-Allocation Plan
doc_id: (assign next SIG-HW / km-systems id)
type: Board design reference — the bridge from SIG-SPEC-006 into CubeMX (.ioc) and KiCad
status: Working — drives the CubeMX pinout and the 4-layer KiCad schematic/layout
parent: SIG-SPEC-ZKKEY-006 (canonical capability spec); SIG-FW-ZKKEY-001 (enforcement)
mcu: STM32U585QII6Q — UFBGA132 (7×7), SMPS, 2 MB flash, Cortex-M33 @160 MHz
author: William Shane Wilkinson (ZKNOT, INC.)
date: 2026-06-09
classification: ZKNOT INTERNAL
sources_verified_2026-06-09:
  - ST AN5373 (STM32U5 hardware development) Fig.3/Fig.4 — SMPS power scheme (with SMPS)
  - ST DS13086 STM32U585xx datasheet — power overview, pinout/AF (confirm exact balls in CubeMX)
---

# WitnessMark Connect v1 — Hardware Design Reference & Pin-Allocation Plan

This is the single artifact that turns the capability/firmware specs into a board. It is the literal
input to a CubeMX `.ioc` (pin + secure/NS + clock) and to the KiCad schematic (net plan + power tree).
Exact UFBGA132 ball coordinates are intentionally **deferred to CubeMX** — it owns the alternate-function
matrix for the QII6Q and prevents illegal assignments. What's fixed silicon, I've fixed here.

## 1. Locked decisions (this session)

| Item | Value |
|------|-------|
| MCU | **STM32U585QII6Q**, UFBGA132, SMPS, 2 MB flash |
| OLED | **SPI** (4-wire), module **hand-attached post-reflow** → board carries connector/pads, not a reflowed display |
| OPTIGA bus | **Dedicated secure I²C**, STM32 ↔ OPTIGA **only** (no other devices on it) |
| USB | **USB-C, bus-powered, USB Full-Speed device, CC pulldowns only, no PD, no PD controller** |
| Clocks | **HSE crystal** (USB-robust) + **LSE 32.768 kHz** populated (RTC/TAMP) |
| Button | **Secure-world GPIO** |
| Armed LED | **Secure-world GPIO** |
| Status LEDs | **Non-secure** GPIO (readiness indication, not security-critical) |
| Stackup | **Top Signal / Inner-1 GND / Inner-2 PWR / Bottom Signal** (4-layer) |
| Pre-pot access | **Custom pogo pad array (Rev A footprint)** — the jig is the truth; tiny SWD backup pads for bring-up only |
| Form | 30 × 90 mm, potted, double-sided; OPTIGA bottom-side; OLED + LEDs shine-through top |

## 2. Power tree & SMPS — VERIFIED (AN5373 Fig. 4, STM32U585xQ with SMPS)

The `Q` part uses the **internal SMPS** to generate the core rail (VCORE on VDD11). The board still
needs an **external 3.3 V regulator** from USB VBUS (5 V); the SMPS only steps VDD→VCORE internally and
**cannot** power external components.

```
USB-C VBUS (5V) ── 3.3V regulator ──┬─ VDD       (n× 100 nF + 10 µF bulk)
                                    ├─ VDDA      (ferrite + 1 µF + 100 nF, isolated)
                                    ├─ VDDUSB    (100 nF)              ← MUST be powered for USB
                                    ├─ VDDIO2    (100 nF, if any VDDIO2-grouped I/O used)
                                    └─ VBAT      (3.3V for v1; see Redoubt note)
VDD ─ VDDSMPS (10 µF) ─[internal SMPS]─ VLXSMPS ─ 2.2 µH coil ─ VDD11 (×2)  (2× 2.2 µF)
VSSSMPS ─ GND
```

BOM/layout consequences (do not skip):
- **2.2 µH inductor** on VLXSMPS→VDD11; **2× 2.2 µF** on the two VDD11 pins; **10 µF** on VDDSMPS.
  Keep the SMPS switching loop (VLXSMPS–coil–VDD11–VSSSMPS) **tight and guarded** — it's the one
  noisy node on the board.
- **VDDUSB must be supplied** (3.3 V + 100 nF) or USB won't enumerate.
- **VBAT** powers LSE/RTC/TAMP/backup. v1: tie to 3.3 V. *Redoubt note:* if you later want tamper
  detection to persist while the unit is unpowered, VBAT needs a backup source (coin cell / supercap) —
  reserve the footprint now, populate per run (D-0).
- Per-supply decoupling: one 100 nF per VDD/VDDIO2 pin + bulk; VDDA filtered.
- **Confirm the exact VDD11/VDDSMPS/VLXSMPS/VSSSMPS ball locations** for the QII6Q against the DS13086
  pinout before layout (§9).

## 3. Functional pin-allocation plan

Fixed = silicon-fixed (assign exactly here). Flex = CubeMX picks the ball from the AF matrix; instance
is chosen here. **Sec/NS** is the GTZC/TrustZone designation (the security-critical column).

| Function | Peripheral / instance | Pin(s) | Fixed/Flex | Sec/NS | Net name | Notes |
|----------|----------------------|--------|-----------|--------|----------|-------|
| Core debug | SWD | **PA13** SWDIO, **PA14** SWCLK | Fixed | Sec¹ | `SWDIO`,`SWCLK` | Locked at RDP2 in production; pre-pot jig only |
| Trace (opt) | SWO | PB3 | Fixed | — | `SWO` | Optional factory log |
| Reset | NRST | NRST (dedicated) | Fixed | — | `NRST` | Jig-driven |
| Boot mode | BOOT0 | BOOT0 (dedicated) | Fixed | — | `BOOT0` | Jig recovery; confirm ball in DS13086 |
| HSE | RCC OSC | **PH0** OSC_IN, **PH1** OSC_OUT | Fixed | — | `HSE_IN/OUT` | 16 MHz crystal + 2 load caps |
| LSE | RCC OSC32 | **PC14** OSC32_IN, **PC15** OSC32_OUT | Fixed | Sec² | `LSE_IN/OUT` | 32.768 kHz + 2 caps; RTC/TAMP |
| USB FS | USB_OTG_FS | **PA11** DM, **PA12** DP | Fixed | **NS** | `USB_DM`,`USB_DP` | 90 Ω matched pair; transport only |
| USB-C CC | (resistors) | — | — | — | `CC1`,`CC2` | 5.1 kΩ pulldowns to GND (UFP, no PD) |
| OPTIGA bus | **I²C (dedicated)** | SCL + SDA | Flex | **Sec** | `OPTIGA_SCL/SDA` | STM32↔OPTIGA only; 2× pull-ups; shielded |
| OPTIGA ctrl | GPIO | RST_N, (PWR_EN opt) | Flex | **Sec** | `OPTIGA_RST` | Reset/power-enable if used |
| OLED | **SPI (4-wire)** | SCK, MOSI, CS, DC | Flex | **Sec** | `OLED_*` | + RST; framebuffer in secure domain |
| Button | GPIO (EXTI) | 1 pin | Flex | **Sec** | `BTN_SIGN` | Debounced; the actuation gate (C-G3) |
| Armed LED | GPIO | 1 pin | Flex | **Sec** | `LED_ARMED` | Secure-owned readiness |
| Status LEDs | GPIO ×3 | 3 pins | Flex | **NS** | `LED_STAT[0..2]` | Series R; non-secure |
| Tamper | TAMP / RTC | TAMP_INx | Fixed-ish | **Sec** | `TAMP[1..2]` | Confirm exact balls (memory: PE4/PE5) — §9 |
| Fixture-detect | GPIO | 1 pin | Flex | **Sec** | `JIG_DET` | Pulled by jig; firmware reads "jig mode" |
| Factory UART (opt) | USART | TX, RX | Flex | NS | `FAC_TXD/RXD` | Pre-pot log only |

¹ SWD pins are physically present but **debug-disabled at RDP2**; "Sec" reflects that debug touches secure memory.
² LSE/RTC/TAMP live in the backup domain; tamper configuration is secure.

## 4. Secure / Non-secure partition map (GTZC) — the moat, as a pin policy

This is C-G3/C-G4 expressed as silicon configuration; it's what the verifier ultimately trusts.

- **SECURE (SPE-owned, GTZC-locked):** OLED SPI bus + all its pins; button GPIO; armed LED; OPTIGA I²C
  + OPTIGA control GPIO; TAMP; fixture-detect; the signing key, FSM, and display framebuffer.
- **NON-SECURE (NSPE):** USB_OTG_FS (challenge-in / artifact-out *transport*; the signed record crosses
  the NSC boundary — the secure domain validates and signs, the NS side only moves bytes); status LEDs;
  factory UART.

The rule that makes content-binding real: **the domain that drives the OLED is the domain that holds
the key.** A secure peripheral cannot have non-secure I/O — so binding the OLED SPI and the button to
the secure world via GTZC is what closes the show-X-sign-Y hole (SIG-SPEC-006 §2.1 C-G4).

## 5. Pre-pot Design-for-Test — the pogo jig footprint (Rev A)

Your jig list, formalized, with the OEM2 correction folded in. **The OEM2 password injection is over
SWD at reset — there is no separate OEM2 pin; SWDIO/SWCLK/NRST *are* the lock/regression path.**

| Pogo signal | Purpose | Phase it serves |
|-------------|---------|-----------------|
| VDD / 3V3 sense | power + test | test |
| GND | reference | all |
| SWDIO, SWCLK | program / debug / **OEM2 inject** | flash, lock, regress |
| NRST | reset control | all |
| BOOT0 | recovery / boot mode | recovery |
| UART TX/RX (opt) | factory log | test |
| OPTIGA I²C SCL/SDA | **field-personalization** (CSR→YubiHSM cert→write slot) | personalize |
| OPTIGA RST / PWR_EN (if used) | SE control | personalize |
| JIG_DET (fixture-detect) | firmware enters jig/provisioning mode | all |

The five manufacturing questions your footprint forces — answered:
- **Reachable before potting:** everything above (SWD, OPTIGA I²C, power, reset, jig-detect).
- **Locked before potting:** firmware loaded + measured; secure boot; **RDP2 + OEM2 password set**;
  WRP/HDP protections.
- **Tested before potting:** power-up, USB enumerate, OLED + button + LED bring-up, signing self-test,
  OPTIGA comms.
- **Personalized before potting:** enclave signing key on-die keygen; **OPTIGA identity cert chained to
  the YubiHSM root** (DIY field-perso); cross-cert attestation written; serials bound.
- **Inaccessible after potting:** SWD/debug, OPTIGA I²C, all test access — the unit is final at cast.
  This is why the order is fixed: **provision + cross-cert + lock at the jig, then pot.**

Keep the **tiny SWD backup pads** for early Rev-A bring-up, but the jig array is the production truth.
`JIG_DET` is secure-readable, but the real gate on provisioning is the **lifecycle state**
(Open/Provisioning → Closed), not just the pin — the pin is a convenience/safety interlock.

## 6. Clock tree (CubeMX)

- **HSE 16 MHz** crystal → PLL1 → **160 MHz SYSCLK**; PLL1Q → **48 MHz** for USB_OTG_FS. With a real
  HSE crystal you do **not** need CRS/HSI48 trimming for USB — the crystal meets FS accuracy directly.
- **LSE 32.768 kHz** → RTC + TAMP timestamping (time is *untrusted* per SIG-SPEC-006 §4A, but the RTC
  is still useful for ordering/monotonic context and tamper event stamps).
- SMPS range set for 160 MHz operation per the U585 power/voltage-scaling table.

## 7. CubeMX driving order (do it in this sequence)

1. New project → **STM32U585QII6Q**. Enable **TrustZone (TZEN)** at project creation (can't cleanly add later).
2. Clock: HSE on (PH0/PH1), LSE on (PC14/PC15), PLL → 160 MHz + 48 MHz USB; set SMPS.
3. Peripherals: USB_OTG_FS (Device, FS); the **I²C instance** for OPTIGA; the **SPI instance** for OLED;
   GPIOs for button, LEDs, OPTIGA RST, JIG_DET; TAMP; optional USART.
4. **Assign secure/non-secure** per §4 (GTZC/TZSC): OLED SPI, button, armed LED, OPTIGA I²C+RST, TAMP,
   JIG_DET → **Secure**; USB, status LEDs, UART → **Non-secure**. Verify a secured peripheral's pins
   show as secure.
5. Generate under the **TF-M / OEMiRoT** project structure (matches SIG-FW-001). Export the `.ioc` as the
   board's pin source of truth — KiCad nets should match it 1:1.

## 8. KiCad 4-layer — schematic blocks, then layout

Schematic blocks: (a) MCU + decoupling; (b) **power tree + SMPS** (§2); (c) USB-C receptacle + CC
pulldowns + ESD; (d) OPTIGA + dedicated I²C + pull-ups; (e) OLED connector + SPI; (f) HSE + LSE crystals
+ load caps; (g) button; (h) LEDs + series R; (i) **pogo pad array** (§5); (j) tamper; (k) backup SWD pads.

Layout / DFM / potting checklist:
- Stackup **Sig / GND / PWR / Sig**; keep a solid GND reference under all signals.
- **USB D+/D−**: 90 Ω differential, matched length, reference to GND, short.
- **SMPS loop** tight and guarded (§2); coil away from the crystals and USB pair.
- **HSE/LSE**: short traces, guard ring, ground the can; keep the SMPS coil away from LSE.
- **OLED window + LED light-pipes**: align the top-side optical features to the potting/enclosure;
  confirm the clear-epoxy shine-through path for the 4 LEDs and the armed LED.
- **Pogo pad array**: on a face that stays accessible during the pre-pot jig step; defined pitch for your
  Rev-A fixture; keep-out from potting dam.
- **OPTIGA** bottom-side; short secure-I²C routing; pull-ups near the MCU.
- Potting keep-outs: connector mate height, OLED, any pre-pot-only feature.
- I can't generate real KiCad files — that's your bench. Run the schematic/layout; I'll review net plans,
  values, and DFM against this doc.

## 9. Verify-before-build residuals (confirm in CubeMX / datasheet before order)

1. **Exact UFBGA132 balls** for VDD11 (×2), VDDSMPS, VLXSMPS, VSSSMPS, VDDUSB, VBAT, VDDA, VDDIO2,
   BOOT0, and the TAMP_INx pins — against DS13086 pinout for the **QII6Q** specifically.
2. **PSA-L3/SESIP3 cert attachment:** confirm it attaches to STM32U585 (QII6Q) before any federal claim.
3. **Tamper pin mapping** (memory says PE4/PE5 = external tamper) — confirm against the datasheet TAMP AF.
4. **I²C/SPI instance choice** that keeps the secure peripherals on pins that don't collide with USB/SWD/OSC.
5. **VBAT backup source** decision (v1 tie-to-3V3 vs Redoubt backup cell) — footprint now either way.

## 10. What this unblocks → new threads (sequenced)

1. **BOM + exact OPNs** (next small thread): MCU, OPTIGA (std V3 part #), OLED module, USB-C receptacle,
   HSE 16 MHz + LSE 32.768 kHz crystals + caps, 3.3 V regulator, **2.2 µH SMPS coil**, ESD, passives.
   *I build it, datasheet-verified.*
2. **CubeMX `.ioc`** (you) — driven by §3/§6/§7; export as pin source of truth.
3. **KiCad schematic → 4-layer layout** (you) — §8; I review.
4. **TF-M secure-display spike** (you, once you have a B-U585I-IOT02A) — proves C-G4 before you trust the
   custom board; I have the verified runbook ready to version to your Cube package.

*Backup/VC: this doc + the canonical set (v6, PAT-021, HW resolution, spike runbook) still live only in
outputs — commit to the vault and mark v5 superseded before branching into board files.*
