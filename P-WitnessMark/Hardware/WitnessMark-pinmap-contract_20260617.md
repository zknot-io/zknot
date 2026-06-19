---
doc_id: SIG-HW-WitnessMark-003
title: WitnessMark STM32U585 Pinmap Contract (locked)
project: P-WitnessMark
mcu: STM32U585RIT6 (LQFP64)
source_of_truth: Firmware/witnessmark/witnessmark.ioc
derived_from: CubeMX 6.17.0 pinout export (witnessmark-pinout.csv) + validated config screenshots
status: LOCKED for first board spin
date: 2026-06-17
honesty_note: This is a bring-up pinmap, not a security claim. Reset lines default HIGH (parts not held in reset). No absolute claims made about the design.
---

# WitnessMark — STM32U585 Pinmap Contract

## TL;DR
Locked MCU pinmap for the WitnessMark first board spin. Every KiCad schematic net for the
STM32U585RIT6 must be diffed against this table before fabrication. CubeMX `.ioc` is the
master; this file is the human-readable contract derived from it and cross-checked against
the validated configuration. No pin collisions; all peripheral functions verified as legal
alternate functions for their assigned pins. Two items flagged for final eyeball (USART1_RX
pin choice; LCD_BL presence).

## Decisions
- **D1 — MCU:** STM32U585RIT6, LQFP64, no-TrustZone-at-bringup (TZ enabled in firmware later; pinmux-neutral).
- **D2 — Crystal-less USB:** HSI48 + CRS SYNC = USB; LSE 32.768 kHz on PC14/PC15 for RTC. No HSE.
- **D3 — SPI display:** SPI1 Transmit-Only Master, 8-bit, Mode 0 (CPOL=Low/CPHA=1Edge). MISO (PA6) freed.
- **D4 — Secure element:** OPTIGA Trust M on I2C1 (PB6 SCL / PB3 SDA), hardware RST on PB12.
- **D5 — Human-actuation gate (PAT-001):** CONFIRM_BTN on PC0, EXTI, pull-up, FALLING edge (fires on press).
- **D6 — Scanner UART (airgap on-ramp):** USART1 reserved (TX PA9), header not populated this spin.
- **D7 — Reset defaults:** LCD_RST and OPTIGA_RST initial state HIGH so neither part boots held-in-reset.

---

## 1. Locked pin assignments

| # | MCU Pin | Function | Net / User Label | AF | Notes |
|---|---------|----------|------------------|----|-------|
| 46 | PA13 | DEBUG_JTMS-SWDIO | SWDIO | AF0 | Programming/debug — do not repurpose |
| 49 | PA14 | DEBUG_JTCK-SWCLK | SWCLK | AF0 | Programming/debug — do not repurpose |
| 3  | PC14 | RCC_OSC32_IN | LSE_IN | — | 32.768 kHz crystal |
| 4  | PC15 | RCC_OSC32_OUT | LSE_OUT | — | 32.768 kHz crystal |
| 15 | PA1  | SPI1_SCK | LCD_SCK | AF5 | Display clock |
| 23 | PA7  | SPI1_MOSI | LCD_MOSI | AF5 | Display data (one-way) |
| —  | PA6  | (unused) | — | — | SPI1_MISO freed by Transmit-Only |
| 58 | PB6  | I2C1_SCL | OPTIGA_SCL | AF4 | + 10K pull-up to VCC (schematic) |
| 55 | PB3  | I2C1_SDA | OPTIGA_SDA | AF4 | + 10K pull-up to VCC (schematic) |
| 42 | PA9  | USART1_TX | SCAN_TX | AF7 | Scanner UART — reserved header |
| 43 | PA10 | USART1_RX | SCAN_RX | AF7 | **VERIFY** (alt: PB7) |
| 44 | PA11 | USB_OTG_FS_DM | USB_DM | AF10 | + USBLC6-2 ESD on line |
| 45 | PA12 | USB_OTG_FS_DP | USB_DP | AF10 | + USBLC6-2 ESD on line |
| 26 | PB0  | GPIO_Output | LCD_CS | — | Push-pull |
| 27 | PB1  | GPIO_Output | LCD_DC | — | Push-pull |
| 28 | PB2  | GPIO_Output | LCD_RST | — | Push-pull, init HIGH |
| 29 | PB10 | GPIO_Output | LCD_BL | — | **VERIFY present**; PWM-capable later |
| 33 | PB12 | GPIO_Output | OPTIGA_RST | — | Push-pull, init HIGH |
| 8  | PC0  | GPIO_EXTI0 | CONFIRM_BTN | — | Pull-up, FALLING edge, NVIC EXTI0 |
| 9  | PC1  | GPIO_Output | STATUS_LED | — | Push-pull |

---

## 2. Schematic action items (carry into KiCad)
These are NOT in the MCU pinmux — they live on the schematic and must be added by hand:

1. **I2C1 pull-ups:** 10K from PB6 (SCL) and PB3 (SDA) to VCC. (Datasheet Figs 2–5 spec 10K. At FM+/1MHz may need lower; start 10K.)
2. **OPTIGA decoupling:** 100nF from OPTIGA VCC (pin 10) to GND, close to the chip.
3. **OPTIGA RST:** pin 9 → PB12 (OPTIGA_RST). Active-low; weak internal pull-up present.
4. **OPTIGA unused pins:** pins 2,4,5,6,7 = NC, leave floating. Pin 1 = GND.
5. **USB ESD:** USBLC6-2SC6 across USB_DM/USB_DP (PA11/PA12) near the connector.
6. **USB-C receptacle:** CC/VBUS/shield per connector datasheet; bus-powered (no VBUS sense).
7. **Display header:** route LCD_SCK/MOSI/CS/DC/RST/BL + 3V3 + GND to a 0.1" header/test-points.
   Defer FPC connector to production spin — bring-up uses Adafruit 4313 breakout.
8. **CONFIRM button:** tactile switch from PC0 to GND (active-low matches the pull-up + falling edge).
9. **Status LED:** PC1 → resistor → LED → GND (or to VCC, pick polarity in firmware).
10. **BOOT0 (PH3):** pull low for normal boot.

---

## 3. Open verification items (before lock is final)
- [ ] **USART1_RX pin:** confirm PA10 (recommended, keeps UART off the I2C neighborhood) vs PB7.
- [ ] **LCD_BL on PB10:** confirm the assignment survived (was labeled, not in last grep filter).
- [ ] **OPTIGA MTR/MM host-library support:** confirm `optiga-trust-m` library targets the
      SLS32AIA010MM (MTR) variant before committing firmware. Footprint unaffected.

---

## 4. Reconciliation protocol (KiCad)
1. In KiCad, every STM32U585 net label must match column "Net / User Label" above exactly.
2. After schematic capture, diff the KiCad netlist's MCU pins against this table — no extras, no missing.
3. Re-run `scripts/witnessmark-cubemx-gen.sh pinout` if the `.ioc` changes; this contract must be
   regenerated to match. The `.ioc` is the master; this file follows it.
4. Only after a clean diff: proceed to DRC/ERC, then Gerber/BOM/CPL review before JLCPCB.

Page 1 of 1
