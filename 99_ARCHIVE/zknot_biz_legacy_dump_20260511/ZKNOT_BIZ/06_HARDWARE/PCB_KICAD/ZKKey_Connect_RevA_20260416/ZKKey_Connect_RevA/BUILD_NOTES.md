# ZKKey Connect RevA — Build Notes
**ZKNOT, INC. | PAT PEND | 2026-04-16**

---

## Board Summary
- **Size:** 60 × 40 mm, 2-layer, 1.6mm FR4
- **SMD (reflow oven):** U1, U2, U3, Y1, C1–C12, R1–R9
- **THT (hand solder):** J1 (USB-C pigtail), J2 (SWD), J3 (BOOT0), SW1, D1–D4, H1–H4
- **GND pour:** Both layers, stitching vias, thermal reliefs on THT pads

---

## Build Order (prevents rework headaches)

### Step 1 — SMD reflow (top side only)
Apply paste with stencil. Place in this order:
1. **U2 (ATECC608A)** — SOIC-8, pin 1 = top-left chamfer mark. Place first, most rework-sensitive.
2. **U3 (AMS1117)** — SOT-223, tab = pin 2 (3.3V OUT). Large tab goes toward board center.
3. **U1 (STM32F072)** — LQFP-48, pin 1 = circle mark, bottom-left corner of chip. Use magnification. All 4 sides must be flat before reflow.
4. **Y1 (Crystal)** — 3225 4-pad. GND pads go to top/bottom (pins 3,4).
5. **All caps and resistors** — 0805, hard to get wrong. C10/C11 (12pF) are crystal load caps — keep them matched.

Reflow. Inspect all 48 pins on U1 under magnification before proceeding.

### Step 2 — Power verification (before THT)
1. Do NOT install THT components yet.
2. Apply 5V to VBUS and GND test points (TP3, TP1).
3. Measure TP2 (3V3_EDGE) — should read **3.28–3.32V**.
4. Measure U2 pin 8 — should match 3V3.
5. If 0V: check U3 orientation, check C8/C9 polarity if using electrolytic.

### Step 3 — THT components
1. **J2 (SWD header)** — install first. You'll use this immediately.
2. **J3 (BOOT0 jumper)** — install. Leave shunt OFF (run mode) by default.
3. **R1–R4 LED resistors** — if you placed these SMD already, skip. Otherwise these are on the SMD BOM.
4. **D1–D4 LEDs** — flat side (cathode) = square pad. Green=D1, Yellow=D2, Blue=D3, Red=D4.
5. **SW1 (SIGN button)** — center of button body should face board edge for easy press.
6. **J1 (USB-C pigtail)** — see section below.

### Step 4 — USB-C pigtail wiring
The pigtail has 6 wires. Thread each wire through its labeled THT hole from the **bottom face**. Flood solder on bottom.

| Hole | Label | Wire Color (typical) |
|------|-------|----------------------|
| 1    | VBUS  | Red |
| 2    | DM    | White |
| 3    | DP    | Green |
| 4    | CC1   | — |
| 5    | CC2   | — |
| 6    | GND   | Black |

Wrap strain relief cable through the two 3mm holes above/below the pigtail cluster and zip-tie or epoxy before stressing the joints.

> **Note:** CC1 and CC2 on the board connect to R8/R9 (5.1kΩ to GND). This tells the host this device is a UFP (device, not host). Some pigtails omit CC wires — if so, leave holes 4/5 empty, the resistors still need to be on the board.

---

## Programming — First Flash

### Hardware setup
1. Install BOOT0 shunt (J3 pins 1+2 shorted) → DFU mode.
2. Connect ST-Link V2 to J2: `1=3V3, 2=SWDIO, 3=GND, 4=SWCLK`.
3. Power via USB pigtail (5V VBUS from host) OR via ST-Link 3V3 (remove U3 output if powering from ST-Link 3V3 to avoid conflict).

### Flash via STM32CubeProgrammer
```
Target: STM32F072CBT6
Interface: SWD
Speed: 4000 kHz
```
Or via DFU (USB, BOOT0 shunted):
```
dfu-util -d 0483:df11 -a 0 -s 0x08000000:leave -D zkkey_firmware.bin
```

### After first flash
- Remove BOOT0 shunt → run mode.
- Power cycle.
- D1 (PWR/green) should illuminate steady within 500ms.
- Device should enumerate as USB HID or CDC-ACM depending on firmware.

---

## ATECC608A First Provisioning

The ATECC608A ships in an unlocked state. On first power-up with firmware:
1. Firmware checks configuration zone — if blank, writes config and locks zone.
2. Generates ECC P-256 key pair in slot 0 — private key never leaves chip.
3. Returns public key + device serial (derived from 9-byte ATECC serial).
4. Register serial + public key at `api.zknot.io/v1/provision` — this ties the physical device to verifyknot.io.

**The ATECC serial is permanently set at silicon — it is the hardware root of trust. Losing it = losing provenance.**

---

## JLCPCB Order Checklist

- [ ] Gerbers: export from KiCad → `Plot` → all layers → zip `gerbers/` folder
- [ ] Drill file: `Generate Drill Files` → Excellon format → include in gerbers zip
- [ ] SMT assembly: upload `ZKNOT_BOM-002_ZKKeyConnect_jlcpcb_bom_20260416.csv`
- [ ] CPL file: export from KiCad `File → Fabrication Outputs → Component Placement`
- [ ] Board spec: 2-layer, 1.6mm, HASL lead-free, green, 1oz copper
- [ ] Assembly: **top side SMD only** — THT assembled by hand
- [ ] Confirm extended parts: U1 (C81720), U2 (C3395330) — both in JLCPCB extended lib, small surcharge applies
- [ ] Order qty: minimum 5 recommended for first run (JLCPCB SMT minimum)

---

## Known Callouts / Rework Notes

| Item | Note |
|------|------|
| U1 pin 1 | Bottom-left, circle mark on silkscreen. Check under magnification before reflow. |
| U2 pin 1 | Top-left, line on silkscreen. ATECC is sensitive to static — handle at grounded bench. |
| C10/C11 | Crystal load caps must match. 12pF nominal — verify against Y1 datasheet CL spec. |
| R8/R9 | 5.1kΩ CC pull-downs are mandatory for USB-C host enumeration. Do not omit. |
| Y1 | The F072 has an internal RC oscillator (8MHz) usable for USB — Y1 is optional if you use HSI48 trimmed by USB SOF. Check firmware config. |
| LED polarity | Square pad = cathode (−). Round pad = anode (+). Confirm with meter before soldering. |
| SWD J2 | Pin 1 (square pad) = 3V3. Standard ST-Link pinout. Label on silkscreen. |
| BOOT0 J3 | Shorted = DFU. Open = run. Always remove shunt after programming. |

---

## Test Points (left edge, 1.5mm pads)

| Ref | Signal | Use |
|-----|--------|-----|
| TP1 | GND | Ground reference |
| TP2 | +3.3V | Verify LDO output |
| TP3 | +5V | Verify VBUS |
| TP4 | USB_DM | Scope D− |
| TP5 | USB_DP | Scope D+ |
| TP6 | I2C_SCL | Scope I2C clock |
| TP7 | I2C_SDA | Scope I2C data |

---

## File Naming (ZKNOT Convention)
```
ZKNOT_PCB-002_ZKKeyConnect_kicad_project_RevA_20260416/
  ZKKey_Connect_RevA.kicad_pro
  ZKKey_Connect_RevA.kicad_sch
  ZKKey_Connect_RevA.kicad_pcb
  ZKNOT_BOM-002_ZKKeyConnect_jlcpcb_bom_20260416.csv
  BUILD_NOTES.md  ← this file
  gerbers/        ← generate from KiCad before ordering
```

---

*ZKNOT, INC. — When physics is policy, trust is optional.*
*Patent pending: PAT-001 App# 63/960,933*
