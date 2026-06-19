---
doc-id: WM-HW-PINMUX-001
title: WitnessMark STM32U585 — Pinmux & Peripheral Plan
status: PROPOSED — confirm before KiCad pin assignment
date: 2026-06-15
product: P-WitnessMark
target-deadline: 2026-06-19 (KiCad placeholder spin)
mcu: STM32U585 (Cortex-M33, TrustZone) + Infineon OPTIGA Trust M
---

# WitnessMark — STM32U585 Pinmux & Peripheral Plan

## TL;DR
For the 6/19 KiCad spin you do **not** need full firmware. You need a **validated
pinmux** so the MCU footprint in KiCad has the right signal on every pin. This doc
is the proposed peripheral set. Confirm/correct it, lock it in CubeMX once, export
the pinout CSV (`witnessmark-cubemx-gen.sh pinout`), and build the schematic to match
that CSV — not to memory.

## Decisions (each with a recommendation)

### 1. Part number / package — **GATES EVERYTHING**
- Proposed: **STM32U585RIT6** (LQFP64, 2 MB flash, LDO).
- **[VERIFY] before committing:** is this exact MPN in the JLCPCB catalog and in
  stock? Basic vs Extended part = whether you pay a feeder fee and risk a stockout
  killing the assembly run. This is the same trap as the Trust&GO pivot — check the
  catalog *first*.
- LQFP64 chosen over LQFP48 (room for USB + display + debug without fighting) and
  over BGA (LQFP is hand- and JLC-assembly-friendly; BGA is not).

| | LDO (no Q) | SMPS (…RIT6**Q**) |
|---|---|---|
| BOM/layout | simpler, fewer passives | adds inductor + caps |
| Power | slightly higher run/idle current | better efficiency |
| First spin | **easier to assemble** | more to get wrong |

**Recommendation:** LDO for this placeholder spin. SMPS only if a measured power
budget demands it — and the part number changes, so decide before you order.

### 2. System + USB clock
- Proposed: **HSI48 + CRS** (clock-recovery locked to USB SOF) → **no main crystal**.
  Frees 2 pins, drops 2 passives + a crystal from the BOM, meets USB-FS tolerance.
- **Add LSE 32.768 kHz crystal** (2 pins) for the RTC. WitnessMark is an *attestation*
  device — timestamps matter — so spend the cheap crystal on a stable real-time clock.

**Recommendation:** HSI48+CRS for system/USB, LSE for RTC. Skip HSE entirely.
Tradeoff: if you later find you need ultra-low-jitter timing, you've left the HSE
pins free anyway (HSI48 uses none), so this costs you nothing to reverse.

### 3. OPTIGA Trust M interface
- **I2C** (Fast-mode Plus capable pins), dedicated bus, external pull-ups
  (2.2k–4.7k — value depends on bus capacitance). Default OPTIGA addr 0x30. [VERIFY variant/addr]
- **Keep the secure element OFF the display bus.** Do not share I2C with a display.

### 4. Hash display (the PAT-001 surface)
| | SPI TFT (ST7789 240×240) | I2C OLED (SSD1306 128×64) |
|---|---|---|
| Pins | ~6 (SCK/MOSI/CS/DC/RST/BL) | 2 (shared-risk) |
| Hash legibility | good | cramped |
| QR for verify URL | yes | no |

**Recommendation:** **SPI TFT (ST7789).** "Display the hash" is core IP, and a QR to
the verifyknot.io verify URL is a natural fit — the OLED can't do that well. Costs
4 pins; LQFP64 has them.

### 5. Buttons (the human-actuation gate)
- **CONFIRM** button on an EXTI-capable GPIO — this is the PAT-001
  *actuate-while-hash-is-displayed* gate. Debounce in firmware, not RC.
- Optional second button (CANCEL). Both on free GPIO with interrupt capability.

### 6. TrustZone — phase it
TrustZone changes *which world owns* a peripheral; it does **not** change which
physical pin a peripheral lands on. So for the KiCad footprint it is pinmux-neutral.

**Recommendation:** Lock the pinmux now with TrustZone **disabled** to keep bring-up
simple, get the board out the door 6/19, then enable TZEN + partition secure/non-secure
in firmware after the hardware is validated. You lose nothing on the PCB by deferring.

## Pins you must reserve (fixed, do not reassign)
| Signal | Pins | Note |
|---|---|---|
| SWD debug | PA13 (SWDIO), PA14 (SWCLK) | leave free for programming |
| USB FS | PA11 (DM), PA12 (DP) | **[VERIFY]** against U585 datasheet AF table |
| BOOT0 | BOOT0 pin | pulldown |
| NRST | NRST | reset cap |
| LSE | OSC32_IN/OSC32_OUT | 32.768 kHz crystal |

## Pins CubeMX assigns (let the tool resolve legal AF mappings)
Do **not** hand-pick these from memory — CubeMX knows the alternate-function table.
Feed it the peripherals below, let it assign, then trust the exported CSV.

| Function | Peripheral | Pull-ups / notes |
|---|---|---|
| OPTIGA Trust M | I2Cx (FM+) | external pull-ups required |
| Hash display | SPIx + 3 GPIO (CS/DC/RST) + 1 GPIO (backlight) | |
| CONFIRM button | GPIO EXTI | the actuation gate |
| CANCEL button (opt) | GPIO EXTI | |
| Status LED(s) | GPIO | |
| RTC | internal (LSE) | timestamps |
| RNG / AES / PKA / SAES | internal | no pins |

## VERIFY checklist (clear before ordering)
- [ ] Exact MPN + package confirmed against board intent
- [ ] **MPN present in JLCPCB catalog AND in stock** (Basic vs Extended)
- [ ] LDO vs SMPS locked (changes MPN + passives)
- [ ] OPTIGA Trust M variant, I2C address, pull-up values
- [ ] Display controller confirmed (ST7789 vs SSD1306) + bus
- [ ] LSE 32.768 kHz crystal footprint included
- [ ] USB DM/DP pins confirmed on U585 (datasheet AF table)
- [ ] Pinout CSV exported and diffed against KiCad netlist before fab

## Workflow (order of operations)
1. `./witnessmark-cubemx-gen.sh skeleton`  → proves toolchain + codegen work.
2. Open the generated `.ioc` in CubeMX GUI **once**; add the peripherals above; save.
3. `./witnessmark-cubemx-gen.sh pinout`     → exports the validated pinmux CSV.
4. Build the KiCad schematic so every MCU pin label == the CSV signal name.
5. `./witnessmark-cubemx-gen.sh regen`      → whenever the .ioc changes thereafter.
6. Run Gerbers + BOM + CPL past review before the JLCPCB order.
