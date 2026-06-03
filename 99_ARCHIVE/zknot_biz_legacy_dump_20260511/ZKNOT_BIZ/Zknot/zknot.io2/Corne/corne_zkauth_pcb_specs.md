# Corne ZKAuth Keyboard - PCB Design Specifications
**Ready for JLCPCB Order Tomorrow**

## Project Overview
**Product:** Corne 4.1 split keyboard + ATECC608 crypto authentication
**Goal:** Ship-ready PCB design tonight, order tomorrow, deliver March 2026
**USP:** "The only keyboard that cryptographically proves YOU are typing"

---

## Design Strategy: PANELIZED PRODUCTION

### Panel Layout (100mm x 100mm for cheapest JLCPCB pricing)
```
┌─────────────────────────────────────────┐
│  Left Half    │    Right Half           │  ← Main Corne boards
├───────────────┼─────────────────────────┤
│  ZKAuth       │    ZKAuth              │  ← Crypto modules (2x)
│  Module #1    │    Module #2           │
└─────────────────────────────────────────┘

Dimensions:
- Full panel: 100mm x 100mm (JLCPCB sweet spot)
- Left/Right halves: 95mm x 45mm each
- ZKAuth modules: 45mm x 22mm each
- V-score or mouse-bite breakaway tabs
```

**Why panelize:**
- 1 PCB order = 2 complete keyboards + 4 auth modules
- JLCPCB charges per panel, not per design
- Amortize setup cost across multiple products

---

## Base Design: Corne 4.1

**Source:** [foostan/crkbd](https://github.com/foostan/crkbd)
**License:** MIT (commercial use OK)

### Core Specifications
- **Layout:** 42-key split (3x6 + 3 thumb keys per side)
- **Controller:** RP2040 (NOT Pro Micro - modern, cheaper, faster)
- **Switch support:** MX or Choc v1 hotswap
- **TRRS connection:** 3.5mm jack for half-to-half communication
- **Power:** USB-C on BOTH halves (can use either as master)

### Modifications from Stock Corne 4.1

**CRITICAL CHANGES:**
1. **Add RP2040 footprint** (instead of Pro Micro header)
   - Use Raspberry Pi Pico footprint OR
   - Use Adafruit KB2040 footprint OR
   - Direct RP2040 chip (harder but cheaper)

2. **Add I2C bus to TRRS cable**
   - TRRS pinout:
     - Tip: GND
     - Ring 1: VCC (3.3V)
     - Ring 2: I2C SDA
     - Ring 3: I2C SCL
   - Pull-up resistors: 4.7kΩ on SDA/SCL (both halves)

3. **Add I2C header for ZKAuth module**
   - 4-pin JST-SH connector (like STEMMA QT)
   - Pinout: GND, VCC, SDA, SCL
   - Location: Near thumb cluster (easy cable routing)

4. **Add USB-C on both halves** (already standard in Corne 4.1)

---

## ZKAuth Module (Separate Breakout Board)

### What It Does
- Plugs into keyboard via JST-SH I2C connector
- ATECC608B stores user's private key
- Physical button + LED for "Press to authenticate"
- Small OLED (optional) shows "Auth OK" / "Waiting..."

### Module Specifications

**PCB Size:** 45mm x 22mm (fits in palm rest or external case)

**Components:**
1. **ATECC608B-MAHCZ-T** (Microchip secure element)
   - Footprint: SOIC-8 (easiest to solder)
   - I2C address: 0x60 (configurable)
   - Decoupling: 0.1µF ceramic cap close to VCC

2. **Authentication Button**
   - Tactile switch: 6mm x 6mm (e.g., Omron B3F-1000)
   - Connect to GPIO via 10kΩ pull-up
   - Debounce: 100nF capacitor

3. **Status LED**
   - Green LED: "Ready to authenticate"
   - Red LED: "Authentication in progress"
   - Current limiting: 330Ω resistor
   - Drive via small MOSFET (BSS138) or directly from RP2040 GPIO

4. **OLED Display (OPTIONAL)**
   - 0.91" I2C OLED (128x32)
   - Same I2C bus as ATECC608
   - Address: 0x3C (doesn't conflict)
   - Footprint: 4-pin header (GND, VCC, SCL, SDA)

5. **JST-SH 4-pin Connector**
   - Input from keyboard: GND, 3.3V, SDA, SCL
   - Use JST SH series (1mm pitch, robust)

6. **Microcontroller (OPTION A - Simpler)**
   - Small Seeed XIAO RP2040 module ($5)
   - Handles button press, LED control, ATECC608 communication
   - Bridges I2C from keyboard to ATECC608

   **OR (OPTION B - Cheaper, harder)**
   - Use keyboard's RP2040 directly (no separate MCU)
   - Requires firmware mod to QMK/ZMK

**I RECOMMEND OPTION A** for v1: separate MCU = easier firmware, faster iteration

### Schematic (ZKAuth Module)

```
Keyboard I2C Bus (JST-SH connector)
    ├── ATECC608B (0x60)
    ├── OLED Display (0x3C) [OPTIONAL]
    └── Seeed XIAO RP2040
         ├── Button (GPIO0 + pull-up)
         ├── Green LED (GPIO1)
         └── Red LED (GPIO2)

Power: 3.3V from keyboard USB
Current draw: ~50mA max (OLED on, LEDs on)
```

### PCB Layout Tips
- ATECC608B as close as possible to I2C connector (short traces)
- Ground plane on bottom layer
- Star ground from I2C connector
- Keep ATECC608 traces short and thick (I2C noise immunity)

---

## Firmware Strategy

### Keyboard Firmware (QMK or ZMK)
**Recommend:** ZMK (better RP2040 support)

**Custom Keycode:** `AUTH` key (triggers authentication)
- When pressed: Send I2C command to ZKAuth module
- Module response: "Press button to confirm"
- User presses physical button on module
- Module generates signature with ATECC608
- Signature sent back to keyboard as USB HID packet

### ZKAuth Module Firmware (Arduino/CircuitPython)
**Recommend:** Arduino + CryptoAuthLib

**Flow:**
1. Listen on I2C for command from keyboard
2. On `AUTH` command: 
   - Light up Green LED ("Ready")
   - Wait for button press (with timeout)
3. On button press:
   - Light up Red LED ("Signing")
   - Generate ECDSA signature using ATECC608
   - Send signature back to keyboard via I2C
   - Green LED blinks (success)

**Libraries:**
- CryptoAuthLib (Microchip official)
- Wire (Arduino I2C)
- Adafruit_SSD1306 (for OLED, optional)

---

## BOM (Bill of Materials) - Per Keyboard Set

### Main Keyboard PCBs (Left + Right)
| Component | Qty | Part Number | Price | Source |
|-----------|-----|-------------|-------|--------|
| RP2040 MCU | 2 | Raspberry Pi RP2040 | $0.70 | LCSC |
| USB-C connector | 2 | TYPE-C-31-M-12 | $0.30 | LCSC |
| TRRS jack | 2 | PJ-320A | $0.10 | LCSC |
| Kailh hotswap sockets | 42 | CPG135001S30 | $0.08 | LCSC |
| JST-SH 4-pin | 2 | SM04B-SRSS-TB | $0.15 | LCSC |
| Diodes (1N4148) | 42 | 1N4148W | $0.01 | LCSC |
| Resistors, caps | - | Various | $2.00 | LCSC |
| **PCB fabrication** | 1 panel | - | $5.00 | JLCPCB |
| **PCB assembly** | 1 panel | - | $15.00 | JLCPCB |
| **Subtotal** | | | **~$35** | |

### ZKAuth Modules (x2 per keyboard)
| Component | Qty | Part Number | Price | Source |
|-----------|-----|-------------|-------|--------|
| ATECC608B-MAHCZ-T | 2 | ATECC608B | $0.65 | Mouser/LCSC |
| Seeed XIAO RP2040 | 2 | 102010428 | $5.00 | Seeed |
| Tactile button | 2 | B3F-1000 | $0.10 | LCSC |
| LEDs (green/red) | 4 | Various | $0.05 | LCSC |
| JST-SH connector | 2 | SM04B-SRSS-TB | $0.15 | LCSC |
| OLED 0.91" (opt) | 2 | - | $2.00 | AliExpress |
| Resistors, caps | - | Various | $1.00 | LCSC |
| **PCB (panelized)** | 1 panel | - | $2.00 | JLCPCB |
| **Subtotal** | | | **~$22** | |

### Other Parts (Per Keyboard)
| Component | Qty | Price | Source |
|-----------|-----|-------|--------|
| Keycaps (blank PBT) | 42 | $15 | AliExpress |
| Switches (Gateron) | 42 | $14 | AliExpress |
| TRRS cable | 1 | $2 | Amazon |
| USB-C cable | 1 | $3 | Amazon |
| Case (acrylic layers) | 1 set | $15 | Ponoko/local |
| JST-SH cables | 2 | $1 | AliExpress |
| **Subtotal** | | **$50** | |

### **TOTAL COST PER KEYBOARD:** ~$107
### **SELL PRICE:** $450-550
### **MARGIN:** $343-443 (76-80%)

---

## PCB Design Tonight: Action Items

### Step 1: Get Base Files (30 min)
```bash
git clone https://github.com/foostan/crkbd.git
cd crkbd/corne-classic
# Find the KiCad project files
```

**Files you need:**
- `.kicad_pcb` (PCB layout)
- `.kicad_pro` (project)
- `.kicad_sch` (schematic)

### Step 2: Modify Left/Right Halves (2 hours)

**Changes in KiCad:**

1. **Replace Pro Micro with RP2040**
   - Delete Pro Micro footprint
   - Add RP2040 footprint (use [Adafruit KB2040 as reference](https://github.com/adafruit/Adafruit-KB2040-PCB))
   - Route USB-C directly to RP2040
   - Add crystal (12MHz), decoupling caps, reset button

2. **Add I2C to TRRS**
   - Modify TRRS schematic:
     - Pin 1 (Tip): GND
     - Pin 2 (Ring1): VCC
     - Pin 3 (Ring2): SDA (from RP2040 GPIO 0)
     - Pin 4 (Sleeve): SCL (from RP2040 GPIO 1)
   - Add 4.7kΩ pull-ups on SDA/SCL

3. **Add JST-SH I2C Connector**
   - Place near thumb cluster
   - Pinout: GND, VCC, SDA, SCL (same as TRRS)
   - Share I2C bus with TRRS (parallel connection)

4. **Verify routing:**
   - All diodes connected
   - All hotswap sockets connected
   - USB-C data lines (D+/D-) have 22Ω series resistors
   - No floating nets

### Step 3: Design ZKAuth Module (1.5 hours)

**Create NEW KiCad project:**

**Schematic:**
```
[JST-SH Input] --+-- [ATECC608B (I2C 0x60)]
                 |
                 +-- [Seeed XIAO RP2040]
                      |
                      +-- Button (GPIO0)
                      +-- Green LED (GPIO1)
                      +-- Red LED (GPIO2)
                      +-- OLED header (GPIO2/3, optional)
```

**Component placement:**
- JST connector on left edge
- ATECC608B next to connector (short I2C traces)
- XIAO RP2040 in center
- Button + LEDs on right edge (user-facing)
- OLED header on top edge

**PCB size:** 45mm x 22mm (fits 2 per panel section)

### Step 4: Panelize (30 min)

**Using KiCad's "Append Board":**
1. Create new 100x100mm PCB
2. Import left half at (0, 0)
3. Import right half at (50, 0)
4. Import ZKAuth #1 at (0, 50)
5. Import ZKAuth #2 at (50, 50)

**Add V-scores or mouse bites:**
- V-score between halves: horizontal at Y=48mm
- V-score between main/auth: vertical at X=48mm
- Add 3mm breakaway tabs with mouse bite holes

### Step 5: Generate Gerbers (15 min)

**Export from KiCad:**
- File → Fabrication Outputs → Gerbers
- Include all layers: F.Cu, B.Cu, F.Mask, B.Mask, F.Silkscreen, B.Silkscreen, Edge.Cuts
- Drill files: PTH and NPTH
- Zip everything

**JLCPCB Upload:**
- Gerber files
- BOM (for assembly)
- CPL (component placement file)

---

## JLCPCB Order Specs (For Tomorrow)

### PCB Specifications
- **Size:** 100mm x 100mm
- **Quantity:** 5 panels (= 10 keyboards)
- **Layers:** 2
- **Thickness:** 1.6mm
- **Surface finish:** HASL (cheapest) or ENIG (nicer, +$10)
- **Solder mask:** Black or white (looks professional)
- **Silkscreen:** White or black (opposite of solder mask)

### Assembly Options
- **Assembly side:** Top only (cheaper)
- **Tooling holes:** Added by JLCPCB (auto)
- **Qty:** 5 panels assembled
- **Cost estimate:** ~$50 PCB + $75 assembly = **$125 total**

### Lead Time
- PCB fab: 2-3 days
- Assembly: 3-5 days
- Shipping to US: 7-10 days (DHL) or 15-20 days (ePacket)
- **Total: Delivered by March 10-20** (lines up with PowerVerify™ delivery!)

---

## First 10 Units: Execution Plan

### Week 1 (Tonight - Tomorrow)
- [ ] Clone Corne 4.1 repo
- [ ] Modify schematics (RP2040, I2C, JST connector)
- [ ] Design ZKAuth module schematic
- [ ] Layout both PCBs
- [ ] Panelize into 100x100mm
- [ ] Generate Gerbers
- [ ] Upload to JLCPCB (ORDER BY TOMORROW EOD)

### Week 2-4 (Feb 11 - Mar 1)
- [ ] Source keycaps, switches, cases (AliExpress orders)
- [ ] Write ZMK firmware for keyboard (add AUTH keycode)
- [ ] Write Arduino firmware for ZKAuth module
- [ ] Design laser-cut acrylic case (Ponoko order)
- [ ] Create product page on your site

### Week 5 (Mar 3-9) - ASSEMBLY WEEK
- [ ] Receive PCBs from JLCPCB
- [ ] Receive PowerVerify™ + ZKKey™ from JLCPCB
- [ ] Receive switches, keycaps, cables
- [ ] Assemble first prototype (test everything)
- [ ] Flash firmware, provision ATECC608 with test key
- [ ] Validate full authentication flow

### Week 6 (Mar 10-16) - LAUNCH
- [ ] Assemble 5 units for early adopters
- [ ] Film demo video (typing → press AUTH → crypto signature)
- [ ] Post to r/mechanicalkeyboards, r/olkb, r/ErgoMechKeyboards
- [ ] Launch on your site at $450 (pre-order for next batch)
- [ ] Target: 10 pre-orders in first week

---

## Quick-Start Shortcuts (If You're Rushing)

### Option A: Skip RP2040 Integration (Use Pro Micro Footprint)
- Faster: Use stock Corne 4.1 with Pro Micro headers
- Add separate I2C breakout for ZKAuth
- **Downside:** Not as clean, requires external controller
- **Upside:** Working PCB design in 2 hours instead of 6

### Option B: Buy Pre-Made Corne PCBs
- Order stock Corne 4.1 PCBs from foostan's shop
- Only design ZKAuth module tonight
- **Downside:** Can't panelize, higher per-unit cost
- **Upside:** Guaranteed working keyboard base

**MY RECOMMENDATION:** Do Option B for FIRST 5 units (speed), then migrate to Option A for production (cost).

---

## File Checklist for Tomorrow's JLCPCB Order

### Must-Have Files:
1. **Gerber files** (`.zip`)
   - Generated from KiCad: Plot → Gerber
   
2. **BOM (Bill of Materials)** (`.csv`)
   - Format: Designator, Footprint, LCSC Part #
   - Export from KiCad: Tools → Generate BOM

3. **CPL (Component Placement List)** (`.csv`)
   - Format: Designator, Mid X, Mid Y, Rotation, Layer
   - Export from KiCad: File → Fabrication Outputs → Component Placement

4. **Assembly notes** (`.txt` or `.pdf`)
   - Special instructions: "Do not assemble U1, U2 (hand-solder only)"
   - Orientation notes for LEDs, connectors

---

## Marketing Copy (For Launch)

**Product Name:** "Corne ZKAuth" or "CryptoCorne"

**Tagline:** "The only keyboard that cryptographically proves YOU are typing."

**Elevator Pitch:**
"Split ergonomic keyboard with built-in ATECC608 secure element. Press the AUTH key and a physical button to generate a cryptographic signature proving your identity. Perfect for:
- Signing git commits with hardware keys
- 2FA authentication without phone
- Cryptocurrency transaction signing
- Secure remote work verification
- Privacy enthusiasts who want FOSS hardware"

**Price:** $450 (early bird) / $550 (regular)

**First batch:** 10 units, ships March 2026

**Waitlist CTA:** "Reserve yours now - only 10 units in first production run"

---

## Tonight's Absolute Minimum (3-hour version)

If you're exhausted and need to order SOMETHING tomorrow:

1. **Order stock Corne 4.1 PCBs** from foostan or JLCPCB (2 hours to prepare order)
2. **Design ONLY the ZKAuth module** tonight (1 hour schematic + 1 hour layout + 30 min panelize)
3. **Upload ZKAuth panel to JLCPCB** tomorrow (this is the novel part)
4. **Source switches/keycaps/cases** from AliExpress (30 min to place orders)

**Result:** You'll have working Corne keyboards + custom crypto auth modules in 3-4 weeks.

**Next iteration:** Design full integrated version with panelization.

---

## Questions to Answer BEFORE You Start Tonight

1. **MX or Choc switches?** (MX = more keycap options, Choc = lower profile)
2. **Hotswap or soldered?** (Hotswap = easier for customers, +$0.08/socket)
3. **OLED on ZKAuth module?** (Looks cool, adds $2, needs firmware work)
4. **Case style?** (Acrylic sandwich, 3D printed, aluminum - affects launch timeline)
5. **Color scheme?** (Black PCB + white silkscreen is cleanest)

**My defaults:** MX hotswap, no OLED (v1), acrylic sandwich case, black PCB.

---

Ready to start? Let me know if you need:
- KiCad library for ATECC608B footprint
- Sample ZMK keymap with AUTH key
- Arduino code for ZKAuth module
- Detailed JLCPCB upload tutorial

**GO BUILD.** This is a winner. 🚀
