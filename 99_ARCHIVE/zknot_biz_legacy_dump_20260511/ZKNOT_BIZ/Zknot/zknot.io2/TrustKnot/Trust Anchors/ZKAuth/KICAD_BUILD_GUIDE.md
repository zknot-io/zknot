# ZKAuth Module - KiCad Build Guide

## Issue with Generated Files

The auto-generated KiCad files have syntax errors because KiCad's file format is very strict. Instead of trying to fix the generated files, it's better to build the design step-by-step in KiCad's GUI.

This guide will walk you through creating the ZKAuth module from scratch in KiCad 7.0+.

---

## Prerequisites

- **KiCad 7.0 or newer** (Download from https://www.kicad.org/)
- **Component Libraries** (install via KiCad's Plugin and Content Manager)

---

## Part 1: Create New Project

### Step 1: New Project
1. Open KiCad
2. File → New Project
3. Name: `zkauth_module`
4. Save in your preferred location

### Step 2: Open Schematic Editor
1. Double-click `zkauth_module.kicad_sch` in project window

---

## Part 2: Build the Schematic

### Components Needed

| Symbol | Quantity | Library | Part |
|--------|----------|---------|------|
| J1 | 1 | Connector | Conn_01x04 |
| U1 | 1 | Security | ATECC608A (or create custom) |
| U2 | 1 | MCU_Module | Seeed_XIAO_RP2040 |
| SW1 | 1 | Switch | SW_Push |
| D1, D2 | 2 | Device | LED |
| C1, C2 | 2 | Device | C |
| R1, R2, R3, R4, R5 | 5 | Device | R |

### Step 3: Add Connector (J1)

1. Press `A` to add symbol
2. Search: `Conn_01x04`
3. Place at coordinates (50, 50)
4. Edit value: `JST_SH_I2C`
5. Edit reference: `J1`

**Pin Labels:**
- Pin 1: GND
- Pin 2: VCC
- Pin 3: SDA  
- Pin 4: SCL

### Step 4: Add ATECC608B (U1)

**Option A: Use built-in symbol (if available)**
1. Press `A`, search: `ATECC608`
2. Place at (120, 80)

**Option B: Create custom symbol**
1. Tools → Symbol Editor
2. Create new symbol: `ATECC608B`
3. Add 8 pins (SOIC-8):
   - Pin 1-3: NC (Not connected)
   - Pin 4: GND (Power input)
   - Pin 5: SDA (Bidirectional)
   - Pin 6: SCL (Input)
   - Pin 7: VCC (Power input)
   - Pin 8: NC
4. Save to project library
5. Place in schematic at (120, 80)

### Step 5: Add XIAO RP2040 (U2)

**Create custom symbol:**
1. Symbol Editor → New Symbol: `Seeed_XIAO_RP2040`
2. Create module with pins:
   - Left side (top to bottom):
     - 1: 3V3 (Power output)
     - 2: GND (Power input)
     - 3: D0 (I/O)
     - 4: D1 (I/O)
     - 5: D2 (I/O)
     - 6: D3 (I/O)
   - Right side (top to bottom):
     - 7: D10 (I/O)
     - 8: D9 (I/O)
     - 9: D8/SCL (I/O)
     - 10: D7/SDA (I/O)
     - 11: D6 (I/O)
     - 12: 5V (Power input)
3. Place in schematic at (120, 140)

### Step 6: Add Passive Components

**Button (SW1):**
1. Add `SW_Push` at (180, 100)
2. Reference: `SW1`
3. Value: `AUTH_BTN`

**LEDs (D1, D2):**
1. Add `LED` at (180, 130)
2. Reference: `D1`, Value: `LED_GREEN`
3. Add `LED` at (180, 145)
4. Reference: `D2`, Value: `LED_RED`

**Capacitors (C1, C2):**
1. Add `C` near ATECC608B at (140, 70)
2. Reference: `C1`, Value: `100nF`
3. Add `C` near button at (190, 100)
4. Reference: `C2`, Value: `100nF`

**Resistors (R1-R5):**
1. `R1` at (170, 95) - Value: `10k` (button pull-up)
2. `R2` at (170, 130) - Value: `330` (LED current limit)
3. `R3` at (170, 145) - Value: `330` (LED current limit)
4. `R4` at (90, 58) - Value: `4.7k` (I2C pull-up SDA)
5. `R5` at (90, 61) - Value: `4.7k` (I2C pull-up SCL)

### Step 7: Wire the Circuit

**Power Rails:**
1. Create power symbols:
   - `+3V3` (several instances)
   - `GND` (several instances)

2. Connect power:
   - J1 Pin 1 → GND
   - J1 Pin 2 → +3V3
   - U1 Pin 4 → GND
   - U1 Pin 7 → +3V3
   - U2 Pin 2 → GND
   - U2 Pin 1 → +3V3

**I2C Bus:**
1. Create net labels: `SDA` and `SCL`
2. Connect:
   - J1 Pin 3 → SDA → U1 Pin 5 → U2 Pin 10
   - J1 Pin 4 → SCL → U1 Pin 6 → U2 Pin 9
3. R4: +3V3 → SDA (pull-up)
4. R5: +3V3 → SCL (pull-up)

**Button Circuit:**
1. SW1 Pin 1 → R1 → +3V3 (pull-up)
2. SW1 Pin 1 → U2 Pin 3 (D0)
3. SW1 Pin 2 → GND
4. C2: SW1 Pin 1 → GND (debounce)

**LED Circuits:**
1. Green LED (D1):
   - D1 Cathode → GND
   - D1 Anode → R2 → U2 Pin 4 (D1)

2. Red LED (D2):
   - D2 Cathode → GND
   - D2 Anode → R3 → U2 Pin 5 (D2)

**ATECC608B Decoupling:**
1. C1: U1 Pin 7 (VCC) → U1 Pin 4 (GND)

### Step 8: Run Electrical Rules Check

1. Tools → Electrical Rules Checker
2. Click "Run ERC"
3. Fix any errors (should be mostly warnings about NC pins)

### Step 9: Annotate Schematic

1. Tools → Annotate Schematic
2. Click "Annotate"
3. This assigns reference designators (U1, R1, etc.)

---

## Part 3: Assign Footprints

### Step 10: Footprint Assignment

1. Tools → Assign Footprints
2. Assign each component:

| Reference | Footprint | Library |
|-----------|-----------|---------|
| J1 | Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal | Connector_JST |
| U1 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | Package_SO |
| U2 | Module:Seeed_XIAO_RP2040 | Module (or custom) |
| SW1 | Button_Switch_SMD:SW_SPST_B3U-1000P | Button_Switch_SMD |
| D1, D2 | LED_SMD:LED_0603_1608Metric | LED_SMD |
| C1, C2 | Capacitor_SMD:C_0603_1608Metric | Capacitor_SMD |
| R1-R5 | Resistor_SMD:R_0603_1608Metric | Resistor_SMD |

3. Click "Apply, Save Schematic & Continue"

### Step 11: Custom Footprint for XIAO RP2040 (if needed)

If Seeed_XIAO footprint isn't in library:

1. Open Footprint Editor
2. Create new footprint: `Seeed_XIAO_RP2040`
3. Add pads:
   - Left side: 6 pads, 2.54mm pitch
   - Right side: 6 pads, 2.54mm pitch
   - Pad size: 2.54mm x 1.27mm (SMD rectangular)
   - Spacing: 17.78mm between left and right columns
4. Add outline rectangle: 21mm x 17.5mm
5. Save to project library

---

## Part 4: PCB Layout

### Step 12: Generate Netlist and Update PCB

1. In schematic editor: File → Export → Netlist
2. Save netlist
3. Open PCB editor (zkauth_module.kicad_pcb)
4. Tools → Update PCB from Schematic (F8)
5. Click "Update PCB"
6. All components appear on screen

### Step 13: Set Board Outline

1. Select Edge.Cuts layer
2. Draw rectangle: 45mm x 22mm
   - Start at (10, 10)
   - End at (55, 32)
3. Use "Draw Rectangle" tool

### Step 14: Component Placement

**Layout Strategy:**
- Left: Connector (J1)
- Center-left: ATECC608B (U1) close to connector
- Center: XIAO RP2040 (U2)
- Right: Button (SW1) and LEDs (D1, D2)

**Placement coordinates (approximate):**

```
J1:  (15, 21)   - JST connector on left edge
U1:  (28, 21)   - ATECC608B close to J1
C1:  (32, 18)   - Decoupling cap near U1
R4:  (22, 16)   - I2C pull-up (vertical)
R5:  (24, 16)   - I2C pull-up (vertical)
U2:  (30, 25)   - XIAO RP2040 in center
SW1: (46, 16)   - Button on right edge
R1:  (46, 20)   - Button pull-up above SW1
C2:  (48, 16)   - Debounce cap near button
D1:  (46, 26)   - Green LED
R2:  (43, 26)   - LED resistor
D2:  (46, 30)   - Red LED
R3:  (43, 30)   - LED resistor
```

### Step 15: Route Traces

**Routing Guidelines:**
- Trace width: 0.25mm for signals, 0.4mm for power
- Keep I2C traces short and equal length
- Route power first, then I2C, then other signals

**Key connections:**
1. Power rails (+3V3 and GND) - use fills/zones
2. I2C traces (SDA, SCL) - keep short, route carefully
3. Button → XIAO RP2040
4. LEDs → XIAO RP2040

### Step 16: Add Ground Plane

1. Click "Add Filled Zone" tool
2. Select layer: B.Cu (bottom copper)
3. Net: GND
4. Draw zone covering entire board
5. Right-click → Zones → Fill All Zones

### Step 17: Add Text Labels

On F.SilkS layer:
- "ZKAuth v1.0" at top
- "ATECC608B Secure Element" at bottom
- Pin labels for J1 (GND, VCC, SDA, SCL)

---

## Part 5: Design Rule Check and Gerber Generation

### Step 18: Run Design Rule Check

1. Tools → Design Rule Checker
2. Click "Run DRC"
3. Fix any errors:
   - Clearance violations
   - Track width issues
   - Unconnected nets

### Step 19: 3D View (Optional)

1. View → 3D Viewer
2. Check component placement looks good
3. Verify no overlapping parts

### Step 20: Generate Gerber Files

1. File → Fabrication Outputs → Gerbers (.gbr)
2. Select layers:
   - F.Cu, B.Cu (copper)
   - F.SilkS, B.SilkS (silkscreen)
   - F.Mask, B.Mask (soldermask)
   - Edge.Cuts (board outline)
3. Click "Plot"
4. Click "Generate Drill Files"
5. Format: Excellon
6. Click "Generate Drill File"

### Step 21: Generate BOM

1. Tools → Generate BOM
2. Select format: CSV
3. Save BOM file
4. Add LCSC part numbers from documentation

### Step 22: Generate Position File

1. File → Fabrication Outputs → Component Placement (.pos)
2. Format: CSV
3. Units: Millimeters
4. Click "Generate Position File"

---

## Part 6: Order from JLCPCB

### Step 23: Prepare Files

1. Create ZIP file containing:
   - All Gerber files (.gbr)
   - Drill file (.drl)
   - BOM (CSV with LCSC part numbers)
   - Position file (CPL)

### Step 24: Upload to JLCPCB

1. Go to https://cart.jlcpcb.com/quote
2. Upload Gerber ZIP file
3. Settings:
   - **Dimensions:** Should auto-detect (45mm x 22mm)
   - **Layers:** 2
   - **Quantity:** 5 or 10
   - **PCB Thickness:** 1.6mm
   - **PCB Color:** Black (recommended)
   - **Surface Finish:** HASL or ENIG
   - **Remove Order Number:** Yes (costs extra)

4. Click "PCB Assembly"
5. Upload BOM and CPL files
6. Confirm parts placement
7. Order!

---

## Troubleshooting

### "Footprint not found" error
- Download missing libraries via Plugin and Content Manager
- Or create custom footprints as needed

### DRC errors
- Most common: trace too close to edge
- Solution: Move components 1-2mm inward

### Assembly issues
- Some parts may not be available for JLCPCB assembly
- Hand-solder unavailable parts (usually just XIAO RP2040)

---

## Alternative: Use EasyEDA

If KiCad is too complex, consider using **EasyEDA**:

1. Go to https://easyeda.com/
2. Import KiCad files OR recreate design
3. Easier interface, direct JLCPCB integration
4. Auto-matches LCSC parts

---

## Reference Files

The included files provide:
- Component values
- Connections  
- Pin assignments
- LCSC part numbers

Use them as a **reference guide** while building in KiCad.

---

## Need Help?

- KiCad Forum: https://forum.kicad.info/
- KiCad Docs: https://docs.kicad.org/
- JLCPCB Support: https://support.jlcpcb.com/

Good luck with your ZKAuth module! 🔐
