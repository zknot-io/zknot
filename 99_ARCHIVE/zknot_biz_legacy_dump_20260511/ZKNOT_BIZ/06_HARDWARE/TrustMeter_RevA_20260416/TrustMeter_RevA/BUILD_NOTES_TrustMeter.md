# TrustMeter RevA — Build Notes
**ZKNOT, INC. | PAT-015 App# 64/007,931 | PAT-016 App# 64/007,934 | 2026-04-16**

---

## Board Summary
- **Size:** 80 × 50mm, 2-layer, 1.6mm FR4
- **Function:** Inline USB-C interposer — measures current, voltage, signal activity, classifies hardware, produces ATECC608A-signed attestation records
- **SMD (reflow):** U1 U2 U3 U4 Y1 R1–R15 R_SH1 C1–C12 C_ADC1–5 C_INA1–2 J1 J2
- **THT (hand solder):** DSP1 D1 D2 SW1 J3 J4 H1–H4

---

## Critical Layout Notes — Read Before Building

### The Shunt (R_SH1) is the most important component on this board

The 10mΩ shunt must use **Kelvin connections** to the INA228. This means:

- The VBUS power current flows through the shunt via the wide (2mm) power pads
- The sense voltage is read by the INA228 via separate thin (0.2mm) traces connected as close to the shunt body as possible
- The sense traces (VBUS_SHUNT_HI and VBUS_SHUNT_LO) must **not share any copper** with the power current path
- The silk legend says "DO NOT REROUTE" — this is serious. If you modify the shunt routing in KiCad, re-read the INA228 datasheet section on Kelvin connections before proceeding.

Without Kelvin connections, the voltage drop in the power traces adds to the sense voltage and your current reading is wrong. At 10mΩ, 500mA of VBUS current creates only 5mV of shunt voltage. A 10mΩ trace resistance error doubles your reading.

### VBUS traces must be 2mm wide minimum

J1 → Shunt → J2 VBUS path carries up to 5A (USB-PD). At 1oz copper, 2mm trace handles 5A with ~50°C rise — acceptable for bench use. Do not reduce below 2mm on this path.

### Signal tap resistors are high-impedance by design

R1–R10 (the divider network) present 100kΩ–200kΩ to the USB signals. This is intentional — the monitoring is passive and must not affect signal integrity on the monitored connection. Do not substitute lower values.

### INA228 I2C address

A0 and A1 (pins 4 and 5) are tied to GND in this design → I2C address **0x40**. ATECC608A default address is **0x60**. Both devices share I2C1 (PB6/PB7) with 4.7kΩ pull-ups. The firmware must address each device correctly.

---

## Build Order

### Step 1 — SMD reflow (top side)
1. **U2 (INA228)** first — VSSOP-10 is the hardest package on this board. 10 pads at 0.5mm pitch. Use fine-tip iron or hot air, not paste-and-oven if hand-soldering. Under magnification: confirm no bridges between IN+/IN-/GND pins (pads 1/2/3).
2. **U3 (ATECC608A)** — SOIC-8, same as Connect/Air.
3. **J1, J2 (USB-C receptacles)** — SMD, reflow with paste. Shell pads are large thermal mass — ensure full reflow.
4. **U4 (AMS1117)** — SOT-223, tab is 3.3V OUT.
5. **U1 (STM32F072)** — LQFP-48, inspect all 48 pins.
6. **R_SH1 (10mΩ shunt)** — 2512, large pads, high thermal mass. Apply extra paste. Let oven dwell.
7. **Y1 (crystal)** and all caps/resistors.

### Step 2 — Power verification
1. Apply 5V between TP1 (VBUS) and TP2 (GND).
2. Measure 3.3V at TP3 — should read 3.28–3.32V.
3. Measure U2 pin 6 (VS) — should equal VBUS_SHUNT_LO (≈5V).
4. Measure U3 pin 8 (VCC) — should equal 3.3V.

### Step 3 — INA228 basic verification
With 5V applied and firmware loaded:
1. I2C scan should find device at 0x40 (INA228) and 0x60 (ATECC608A).
2. Read INA228 MANUFACTURER_ID register (0x3E) — should return 0x5449 (Texas Instruments).
3. Read DEVICE_ID register (0x3F) — should return 0x2280.
4. With no load connected, VBUS current reading should be near 0. Any offset > 5mA indicates a Kelvin connection problem.

### Step 4 — Signal tap verification
1. Connect a known USB cable between J1 and J2.
2. With no data activity, ADC_DM and ADC_DP readings should be near 0V.
3. Connect a USB device — data lines should show activity (voltage transitions visible on scope at TP6/TP7).
4. VBUS divider: with 5V VBUS, ADC_VBUS should read 5V × (10k/(100k+10k)) = **0.455V**. Verify at TP4/TP5 with multimeter.

### Step 5 — THT
1. J3 (SWD) — install first.
2. J4 (BOOT0) — install, leave shunt off.
3. DSP1 (OLED) — 7-pin header, display face up.
4. D1 (green OK), D2 (red FAULT) — square pad = cathode.
5. SW1 (MEASURE button).

---

## Voltage Divider Reference

| Signal | Top R | Bottom R | Ratio | Max Input | ADC Reading at Max |
|--------|-------|----------|-------|-----------|-------------------|
| VBUS | 100kΩ | 10kΩ | 11:1 | 20V (USB-PD) | 1.818V ✓ |
| D− | 100kΩ | 100kΩ | 2:1 | 3.3V | 1.65V ✓ |
| D+ | 100kΩ | 100kΩ | 2:1 | 3.3V | 1.65V ✓ |
| CC1 | 100kΩ | 100kΩ | 2:1 | 3.3V | 1.65V ✓ |
| CC2 | 100kΩ | 100kΩ | 2:1 | 3.3V | 1.65V ✓ |

STM32F072 ADC reference = 3.3V. All readings safely within range. ✓

---

## INA228 Configuration (firmware reference)

```c
// INA228 register map (I2C address 0x40)
#define INA228_CONFIG       0x00  // Configuration
#define INA228_ADC_CONFIG   0x01  // ADC configuration
#define INA228_SHUNT_CAL    0x02  // Shunt calibration
#define INA228_SHUNT_VOLT   0x04  // Shunt voltage (raw)
#define INA228_BUS_VOLT     0x05  // Bus voltage
#define INA228_POWER        0x08  // Power
#define INA228_CURRENT      0x07  // Current (after calibration)
#define INA228_TEMP         0x06  // Die temperature

// Shunt calibration for 10mΩ shunt, max current = 5A
// SHUNT_CAL = 13107.2e6 * CURRENT_LSB * R_SHUNT
// CURRENT_LSB = MAX_CURRENT / 2^19 = 5A / 524288 = 9.537μA
// SHUNT_CAL = 13107.2e6 * 9.537e-6 * 0.010 = 1250
#define SHUNT_CAL_VALUE     1250

// ADC config: continuous mode, 16-bit, 16 samples average
// VBUSCT=4 (1052μs), VSHCT=4, VTCT=4, AVG=3 (16 samples)
#define ADC_CONFIG_VALUE    0x4B23

// Current LSB = 9.537μA → 1 count = 9.537μA
// At 500mA: 500000μA / 9.537μA = 52429 counts
// At 5A:    5000000μA / 9.537μA = 524288 counts (full scale)
```

---

## Measurement Session Flow (firmware state machine)

```
IDLE
  → User presses MEASURE button (SW1)
  → Firmware begins session
  → OLED shows: "Measuring..."
  → Green LED blinks

MEASURING (30-second default session)
  → INA228: sample VBUS current at 860 Hz
  → ADC: sample DM/DP/CC1/CC2 at 1 kHz
  → Detect transitions on DM/DP (signal activity)
  → Accumulate: mean, peak, stddev of current
  → Classify vs reference profiles

SIGNING
  → Session record assembled
  → ATECC608A signs record
  → Short code generated
  → Record posted to api.zknot.io/v1/attest

OUTPUT
  → OLED shows: classification + short code
  → OK LED (green): NORMAL classification
  → FAULT LED (red): HIGH_RISK classification
  → Wait for USB CDC host to retrieve full record

IDLE
```

---

## OLED Display Layout (128×64 pixels)

```
┌────────────────────────────────┐  ← 128px wide
│ TrustMeter  [session count]    │  line 0 — 8px
│ ████████████████░░░░░░░░ 4.2A │  line 1 — current bar
│ VBUS: 5.03V  I: 423mA         │  line 2 — live readings
│ ─────────────────────────────  │  line 3 — separator
│ ✓ NORMAL  0.89 similarity     │  line 4 — classification
│ Code: A3F7-K2M9               │  line 5 — short code
│ verifyknot.io                  │  line 6
│ [████████████░░░░░░░░] 22s    │  line 7 — session timer
└────────────────────────────────┘
```

---

## JLCPCB Order Checklist

- [ ] Gerbers from KiCad → Plot → all layers → zip `gerbers/`
- [ ] Drill file → Excellon
- [ ] SMT BOM: `ZKNOT_BOM-004_TrustMeter_jlcpcb_bom_20260416.csv`
- [ ] CPL: `File → Fabrication Outputs → Component Placement`
- [ ] Board: 2-layer, 1.6mm, HASL lead-free, green, 1oz copper
- [ ] Assembly: **top side SMD only** — THT by hand
- [ ] Extended parts: U1 (C81720), U2 (C2678360), U3 (C3395330), J1/J2 (C2765186)
- [ ] Qty: minimum 5

---

## Key Differences from Connect/Air

| Feature | Connect | Air | TrustMeter |
|---------|---------|-----|------------|
| USB role | Signs via USB | Air-gapped | Monitors USB inline |
| ATECC use | Signs attestation | Signs attestation | Signs measurement records |
| New ICs | — | GM65 + TFT | **INA228 + 2× USB-C** |
| Shunt resistor | — | — | **10mΩ 2512 Kelvin** |
| Voltage dividers | — | — | **5× RC tap networks** |
| Output | USB CDC | TFT QR code | OLED + USB CDC |
| Patent | PAT-001/008 | PAT-009/001 | **PAT-015/016** |

---

*ZKNOT, INC. — When physics is policy, trust is optional.*
*PAT-015 App# 64/007,931 | PAT-016 App# 64/007,934*
