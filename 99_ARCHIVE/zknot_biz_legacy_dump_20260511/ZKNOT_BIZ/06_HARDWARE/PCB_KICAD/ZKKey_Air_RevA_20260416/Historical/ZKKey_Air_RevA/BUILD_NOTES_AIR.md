# ZKKey Air RevA — Build Notes
**ZKNOT, INC. | PAT PEND | 2026-04-16**
**PAT-009 App# 63/995,740 | PAT-001 App# 63/960,933**

---

## Board Summary
- **Size:** 80 × 55 mm, 2-layer, 1.6mm FR4
- **This device is fully air-gapped. There is no USB data path. D+/D− do not exist on this board.**
- **SMD (reflow):** U1, U2, U3, Y1, C1–C14, R1–R10
- **THT (hand solder):** MOD1 (GM65), DSP1 (TFT), J1 (USB-C pigtail), J2 (SWD), J3 (BOOT0), SW1, D1–D4

---

## Critical Architecture Note — The Air-Gap

This device receives a cryptographic challenge by having its GM65 camera module read a QR code displayed on a phone screen. It produces a signed attestation by displaying a QR code on the ST7789 TFT, which the phone camera reads back.

**No electrical signal path exists between the signing device and the host at any point during attestation.** The only connection is optical — photons in, photons out.

The USB-C connector carries power only. The D+/D− lines are physically absent from the pigtail and the board. This is not a firmware setting. It is a physical constraint. This is the claim.

---

## Board Layout — Functional Zones

```
┌─────────────────────────────────────────────────────────────┐
│ ZKNOT  ZKKey Air  REV A                         PAT. PEND.  │
│─────────────────────────────────────────────────────────────│
│ ┌─────────────┐  ┌───────────────────────────────────────┐  │
│ │ OPTICAL     │  │  STM32F072  [center]                  │  │
│ │ INPUT       │  │                                       │  │
│ │ GM65-S QR   │  │  ┌──────────────────────────────────┐ │  │
│ │ DECODER     │  │  │ OPTICAL OUTPUT                   │ │  │
│ │ (lens →     │  │  │ ST7789 1.54" 240x240 TFT         │ │  │
│ │  enclosure  │  │  │ (display face up →               │ │  │
│ │  window)    │  │  │  enclosure window)               │ │  │
│ └─────────────┘  │  └──────────────────────────────────┘ │  │
│ ┌─────────────┐  │  ┌──────────┐  SWD  BOOT0             │  │
│ │ USB-C       │  │  │ ATECC608 │                          │  │
│ │ POWER ONLY  │  │  │ SECURE   │                          │  │
│ │ D+/D- ABSENT│  │  │ ELEMENT  │                          │  │
│ └─────────────┘  └───────────────────────────────────────┘  │
│             SIGN [button]                                    │
│  PWR  ARMED  SIGNED  ERROR  [LEDs]    SN:__________         │
│─────────────────────────────────────────────────────────────│
│  Physics enforces.  Math proves.  You verify.               │
└─────────────────────────────────────────────────────────────┘
```

---

## Build Order

### Step 1 — SMD reflow (top side)
Same order and same cautions as Connect. Paste, place, reflow.

1. **U2 (ATECC608A)** first — most rework-sensitive
2. **U3 (AMS1117)** — tab is 3.3V OUT
3. **U1 (STM32F072)** — LQFP-48, pin 1 circle mark bottom-left, inspect all 48 pins under magnification before reflow
4. **Y1 (Crystal)** — GND pads top/bottom
5. **All caps and resistors** — note R10 (10Ω) is the TFT backlight limiter, not the same as LED resistors

### Step 2 — Power verification
1. Apply 5V VBUS and GND via test points TP3, TP1
2. Measure TP2 (3V3) — must read 3.28–3.32V
3. Measure U2 pin 8 — must match 3V3
4. Do not proceed until power rails are verified

### Step 3 — THT components
1. **J2 (SWD)** — install first, needed immediately for programming
2. **J3 (BOOT0 jumper)** — install, leave shunt off
3. **D1–D4 LEDs** — square pad = cathode. Green/Yellow/Blue/Red left to right
4. **SW1 (SIGN button)** — angled, button face toward board edge
5. **MOD1 (GM65)** — see GM65 section below
6. **DSP1 (TFT)** — see TFT section below
7. **J1 (USB-C pigtail)** — see USB-C section below

---

## GM65 QR Decoder Module Installation

The GM65-S is a self-contained QR/barcode decoder. It has its own processor and illumination LEDs. It communicates over UART at 9600 baud by default (configurable).

**Physical mounting:**
- The module connects to MOD1 header (8-pin, at x=8mm on the board)
- The module body extends LEFT from the header toward the board edge
- The camera lens must face toward the enclosure window opening
- The module is ~30×17mm — it will extend past the board edge slightly in some enclosure configs — plan the enclosure cutout accordingly
- Use M2 standoffs through the module's mounting holes if the enclosure allows

**Wiring to MOD1:**

| MOD1 Pin | Signal | Wire to GM65 |
|----------|--------|--------------|
| 1 | +3.3V | VCC |
| 2 | GND | GND |
| 3 | UART_RX (MCU) | TX (GM65 transmits decoded string) |
| 4 | UART_TX (MCU) | RX (MCU sends config commands) |
| 5 | GM65_TRIG | TRIG (pull low to trigger scan) |
| 6–8 | NC | Leave unconnected |

**GM65 default UART:** 9600 baud, 8N1, 3.3V logic — compatible directly with STM32F072.

**Trigger mode:** TRIG pin pulled low by MCU triggers a single scan. GM65 outputs the decoded string over UART then goes idle. Configure continuous scan mode via UART command if preferred.

**First test:** With power applied and firmware loaded, pull TRIG low and point the module at a QR code on your phone. UART RX on TP7 should show the decoded string at 9600 baud.

---

## ST7789 TFT Display Module Installation

The ST7789 is a 1.54" 240×240 color TFT with SPI interface. Buy the breakout with the 8-pin header (GND VCC SCL SDA RES DC CS BL).

**Physical mounting:**
- The module connects to DSP1 header (8-pin, at x=66mm, y=38mm)
- The display face points UP toward the enclosure window opening
- The module body is ~35×35mm and extends upward (toward lower y) from the header
- The active display area is ~34×34mm
- Design the enclosure window to expose the full active area

**Wiring to DSP1:**

| DSP1 Pin | Signal | Wire to TFT |
|----------|--------|-------------|
| 1 | GND | GND |
| 2 | +3.3V | VCC |
| 3 | SPI_SCK | SCL |
| 4 | SPI_MOSI | SDA (data in) |
| 5 | TFT_RST | RES |
| 6 | TFT_DC | DC |
| 7 | TFT_CS | CS |
| 8 | TFT_BL | BL (backlight, via R10 10Ω) |

**Note:** The ST7789 uses SPI write-only (MOSI only, no MISO) — no SPI MISO line needed.

**Backlight:** BL is driven by PB10 (TFT_BL) through R10 (10Ω current limit). PWM dimming is possible from firmware. At 3.3V through 10Ω the backlight LEDs in most modules draw ~50–100mA — verify with your specific module and reduce R10 if too dim or increase if too bright.

---

## USB-C Power-Only Pigtail

**This is the most important assembly step on this board.**

The USB-C pigtail for Air carries ONLY: VBUS, CC1, CC2, GND.

**D+ and D− wires must not be present.** Options in order of preference:
1. Use a pigtail with D+/D− physically cut at the cable entry — cut, heat-shrink, label "CUT"
2. Use a 4-wire USB-C power-only pigtail (some vendors sell these)
3. Use a standard 6-wire pigtail but leave D+/D− holes empty and tape/epoxy the wire ends

The D+/D− holes exist in the PCB layout (J1 pads 2/3) but are labeled on silkscreen. Do not populate them. Their absence is the physical enforcement of the air-gap.

**Wiring J1:**

| J1 Pin | Silkscreen | Wire |
|--------|------------|------|
| 1 (square) | VBUS | Red |
| 2 | CC1 | — |
| 3 | CC2 | — |
| 4 | GND | Black |

Wire entry from board bottom face. Flood solder. Strain relief cable through the two 3mm holes flanking J1.

---

## Programming — Same as Connect

1. BOOT0 shunt installed → DFU mode
2. ST-Link V2 to J2: `1=3V3, 2=SWDIO, 3=GND, 4=SWCLK`
3. Power via USB-C (VBUS from bench supply or hub, no data needed)
4. Flash via STM32CubeProgrammer or dfu-util
5. Remove BOOT0 shunt → run mode

Air shares the same ATECC608A provisioning flow as Connect. On first boot, firmware:
1. Writes ATECC config and locks zone
2. Generates P-256 keypair in slot 0
3. Returns public key + device serial
4. Registers at `api.zknot.io/v1/provision`

---

## Test Points (left edge)

| Ref | Signal | Use |
|-----|--------|-----|
| TP1 | GND | Ground reference |
| TP2 | +3.3V | LDO output |
| TP3 | +5V | VBUS |
| TP4 | I2C_SCL | Scope ATECC bus |
| TP5 | I2C_SDA | Scope ATECC bus |
| TP6 | UART_TX | Scope GM65 TRIG commands |
| TP7 | UART_RX | Scope GM65 decoded output |
| TP8 | GM65_TRIG | Scope trigger signal |

---

## Attestation Flow (what the firmware does)

```
1. IDLE
   → PWR LED on (green)
   → Display: ZKNOT logo + "Aim at QR code"

2. USER AIMS DEVICE AT QR CODE ON PHONE SCREEN
   → GM65 TRIG pulled low by firmware
   → GM65 decodes QR → UART string (nonce/challenge hash)
   → Firmware validates format
   → ARMED LED on (yellow)
   → Display: "Challenge received — Press SIGN"

3. USER PRESSES SIGN BUTTON
   → Firmware passes challenge to ATECC608A over I2C
   → ATECC signs with private key (key never leaves chip)
   → SIGNED LED on (blue, brief flash)
   → Display: QR code of (signature + device ID + timestamp)

4. USER AIMS PHONE CAMERA AT TFT DISPLAY
   → Phone reads QR code
   → Phone sends to verifyknot.io/{short_code}
   → Verification result returned

5. RETURN TO IDLE
   → ERROR LED (red) if any step fails
```

---

## JLCPCB Order Checklist

- [ ] Gerbers from KiCad → Plot → all layers → zip `gerbers/`
- [ ] Drill file → Excellon format
- [ ] SMT BOM: `ZKNOT_BOM-003_ZKKeyAir_jlcpcb_bom_20260416.csv`
- [ ] CPL: `File → Fabrication Outputs → Component Placement`
- [ ] Board: 2-layer, 1.6mm, HASL lead-free, green, 1oz copper
- [ ] Assembly: top side SMD only
- [ ] Extended parts: U1 (C81720), U2 (C3395330) — surcharge applies
- [ ] Qty: minimum 5 for first run

---

## Key Differences vs Connect

| Feature | ZKKey Connect | ZKKey Air |
|---------|--------------|-----------|
| Challenge input | USB-C data (D+/D−) | Camera reads QR from screen |
| Output | USB-C data | TFT displays QR for phone camera |
| USB data path | Present | **Physically absent** |
| MCU | STM32F072CBT6 | STM32F072CBT6 (same) |
| Secure element | ATECC608A (same) | ATECC608A (same) |
| Extra peripherals | None | GM65 module + ST7789 TFT |
| Board size | 60×40mm | 80×55mm |
| Air-gap | No | **Yes — fully air-gapped** |

---

## File Naming (ZKNOT Convention)
```
ZKNOT_PCB-003_ZKKeyAir_kicad_project_RevA_20260416/
  ZKKey_Air_RevA.kicad_pro
  ZKKey_Air_RevA.kicad_sch
  ZKKey_Air_RevA.kicad_pcb
  ZKNOT_BOM-003_ZKKeyAir_jlcpcb_bom_20260416.csv
  BUILD_NOTES_AIR.md  ← this file
  gerbers/
```

---

*ZKNOT, INC. — When physics is policy, trust is optional.*
*Patent pending: PAT-009 App# 63/995,740 | PAT-001 App# 63/960,933*
*No cable. No contact. No compromise.*
