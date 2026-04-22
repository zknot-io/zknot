# ZKAuth Crypto Module - Bill of Materials & Assembly Guide

## PCB Specifications
- **Board Size:** 45mm x 22mm
- **Layers:** 2 (Top and Bottom)
- **Thickness:** 1.6mm
- **Surface Finish:** HASL or ENIG
- **Solder Mask:** Black recommended
- **Silkscreen:** White

## Bill of Materials (BOM)

| Ref | Qty | Value | Device | Package | LCSC Part # | Notes |
|-----|-----|-------|--------|---------|-------------|-------|
| U1 | 1 | ATECC608B-MAHCZ-T | Secure Element | SOIC-8 | C2932020 | Microchip crypto chip |
| U2 | 1 | XIAO RP2040 | Microcontroller | Module | 102010428 | Seeed Studio module |
| J1 | 1 | SM04B-SRSS-TB | JST-SH 4-pin | SMD | C160404 | I2C connector |
| SW1 | 1 | B3U-1000P | Tactile Switch | SMD | C231329 | Auth button |
| D1 | 1 | Green LED | LED 0603 | 0603 | C72043 | Status LED |
| D2 | 1 | Red LED | LED 0603 | 0603 | C72041 | Auth LED |
| C1 | 1 | 100nF | Capacitor | 0603 | C14663 | ATECC608 decoupling |
| C2 | 1 | 100nF | Capacitor | 0603 | C14663 | Button debounce |
| R1 | 1 | 10kΩ | Resistor | 0603 | C25804 | Button pull-up |
| R2 | 1 | 330Ω | Resistor | 0603 | C23138 | Green LED current limit |
| R3 | 1 | 330Ω | Resistor | 0603 | C23138 | Red LED current limit |
| R4 | 1 | 4.7kΩ | Resistor | 0603 | C23162 | I2C SDA pull-up |
| R5 | 1 | 4.7kΩ | Resistor | 0603 | C23162 | I2C SCL pull-up |

## Component Placement Notes

### Critical Layout Requirements

1. **ATECC608B (U1)**
   - Place as close as possible to JST connector (J1)
   - Keep I2C traces (SDA/SCL) short and thick (0.25mm minimum)
   - Decoupling capacitor (C1) must be within 5mm of VCC pin
   - Ground via directly under GND pin recommended

2. **I2C Pull-up Resistors (R4, R5)**
   - Place near JST connector
   - Connect to 3.3V rail with short traces

3. **Seeed XIAO RP2040 (U2)**
   - Center of board for balanced layout
   - USB connector faces edge for easy programming
   - I2C pins (GPIO 26/27) connect to ATECC608B

4. **User Interface Components**
   - Button (SW1) and LEDs (D1, D2) on right edge
   - Accessible for user interaction
   - LEDs visible from top

## Pinout Details

### JST-SH Connector (J1)
```
Pin 1: GND
Pin 2: VCC (3.3V)
Pin 3: SDA
Pin 4: SCL
```

### ATECC608B (U1) - SOIC-8
```
Pin 1: NC (Not Connected)
Pin 2: NC
Pin 3: NC
Pin 4: GND
Pin 5: SDA (I2C Data)
Pin 6: SCL (I2C Clock)
Pin 7: VCC (3.3V)
Pin 8: NC
```

### Seeed XIAO RP2040 (U2)
```
Left Side:
1: 3V3 (Power output)
2: GND
3: D0 - Button input
4: D1 - Green LED
5: D2 - Red LED
6: D3

Right Side:
7: D10
8: D9
9: D8 - SCL (I2C to ATECC608)
10: D7 - SDA (I2C to ATECC608)
11: D6
12: 5V (from USB)
```

## Circuit Description

### Power Supply
- 3.3V supplied from keyboard via JST connector
- Powers ATECC608B directly
- XIAO RP2040 has onboard 3.3V regulator
- Total current draw: ~50mA max (with LEDs on)

### I2C Bus
- Shared between keyboard, ATECC608B, and XIAO RP2040
- ATECC608B address: 0x60
- Pull-up resistors: 4.7kΩ to 3.3V (both SDA and SCL)
- Bus speed: 400kHz (I2C Fast Mode)

### Authentication Button
- Tactile switch with 10kΩ pull-up to 3.3V
- 100nF capacitor for hardware debouncing
- Active LOW when pressed
- Connected to XIAO RP2040 GPIO D0

### Status LEDs
- Green LED: "Ready to authenticate" state
- Red LED: "Authentication in progress" state
- 330Ω current limiting resistors
- Driven directly from XIAO RP2040 GPIO pins

## Assembly Instructions

### Step 1: Solder SMD Components (Recommended Order)
1. ATECC608B (U1) - SOIC-8 (use solder paste and hot air)
2. Capacitors (C1, C2) - 0603
3. Resistors (R1-R5) - 0603
4. LEDs (D1, D2) - 0603 (watch polarity!)
5. Tactile switch (SW1)
6. JST-SH connector (J1)

### Step 2: Solder Through-Hole Module
1. XIAO RP2040 (U2) - can be socketed or soldered directly
   - Recommended: Use 2.54mm female headers for easy replacement

### Step 3: Inspection
- Check for solder bridges, especially on SOIC-8 pins
- Verify LED polarity (cathode to GND)
- Test continuity on I2C lines
- Measure resistance between VCC and GND (should be >10kΩ)

## Testing Procedure

### Visual Inspection
- [ ] No solder bridges on ATECC608B pins
- [ ] All SMD components properly oriented
- [ ] JST connector firmly attached
- [ ] XIAO RP2040 seated correctly

### Electrical Testing
1. **Power Test**
   - Connect 3.3V to JST pins 1 (GND) and 2 (VCC)
   - Measure voltage at ATECC608B pin 7: should be 3.3V
   - Measure current draw: should be <10mA without LEDs

2. **I2C Bus Test**
   - With logic analyzer or I2C scanner
   - Should detect ATECC608B at address 0x60
   - Pull-up resistors should show ~3.3V when idle

3. **Button Test**
   - Measure voltage at SW1: should be 3.3V (pulled up)
   - Press button: should read 0V (GND)
   - Release: should return to 3.3V

4. **LED Test**
   - Apply 3.3V through 330Ω resistor to LED anodes
   - Green LED should light (forward voltage ~2.0V)
   - Red LED should light (forward voltage ~1.8V)

## Firmware Programming

### XIAO RP2040 Firmware
1. Connect USB-C cable to XIAO RP2040
2. Enter bootloader mode (hold BOOT button, press RESET)
3. Flash CircuitPython or Arduino sketch
4. Install required libraries:
   - CryptoAuthLib (for ATECC608B)
   - Wire (I2C communication)

### Initial ATECC608B Configuration
```python
# Python/CircuitPython example
import board
import busio
from cryptoauthlib import device

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize ATECC608B
atecc = device.get_device(i2c, 0x60)

# Lock configuration (ONE-TIME OPERATION!)
# atecc.lock_config()
# atecc.lock_data()
```

## Troubleshooting Guide

### ATECC608B Not Detected
- Check solder joints on pins 4 (GND), 5 (SDA), 6 (SCL), 7 (VCC)
- Verify 3.3V on pin 7
- Check I2C pull-up resistors are installed
- Try slower I2C speed (100kHz)

### Button Not Working
- Check R1 (10kΩ pull-up) is installed
- Verify C2 (100nF debounce) is installed
- Test button continuity with multimeter

### LEDs Not Lighting
- Verify LED polarity (anode to resistor, cathode to GND)
- Check R2/R3 (330Ω) are installed
- Test with direct 3.3V connection

## Design Files Included

1. `zkauth_module.kicad_sch` - Schematic
2. `zkauth_module.kicad_pcb` - PCB layout
3. `zkauth_module.kicad_pro` - KiCad project file

## JLCPCB Order Configuration

### PCB Order
- **PCB Qty:** 5 or 10
- **PCB Thickness:** 1.6mm
- **PCB Color:** Black
- **Surface Finish:** HASL (or ENIG for premium)
- **Copper Weight:** 1 oz
- **Remove Order Number:** Yes

### Assembly Service
- **Assembly Side:** Top side only
- **Tooling Holes:** Added by Customer
- **Confirm Production File:** No

### Component Sourcing
- Most components available from JLCPCB's component library
- XIAO RP2040 (U2) must be sourced separately from Seeed
- ATECC608B available on LCSC

## Cost Estimate (Per Unit)

| Item | Quantity | Unit Cost | Total |
|------|----------|-----------|-------|
| PCB (5 units) | 1 | $2.00 | $2.00 |
| ATECC608B | 1 | $0.65 | $0.65 |
| XIAO RP2040 | 1 | $5.00 | $5.00 |
| Passive Components | ~10 | $0.50 | $0.50 |
| JST Connector | 1 | $0.15 | $0.15 |
| LEDs + Button | 3 | $0.30 | $0.30 |
| **Total per unit** | | | **$8.60** |

*Note: Prices are approximate and subject to change*

## Production Timeline

1. **Design Review** - 1 day
2. **Gerber Generation** - 1 hour
3. **JLCPCB Order** - 15 minutes
4. **PCB Manufacturing** - 2-3 days
5. **Assembly** - 3-5 days (if using JLCPCB assembly)
6. **Shipping** - 7-10 days (DHL) or 15-20 days (standard)

**Total Time to Delivery:** 12-18 days

## Revision History

- **v1.0** (2026-02-13) - Initial design release
  - ATECC608B secure element
  - Seeed XIAO RP2040 controller
  - Physical auth button
  - Dual status LEDs
  - JST-SH I2C connector

## License & Attribution

Design based on Corne keyboard specifications by foostan (MIT License)
ZKAuth modifications © 2026

## Support & Contact

For design questions or assembly issues, refer to:
- ATECC608B Datasheet: https://www.microchip.com/ATECC608B
- XIAO RP2040 Wiki: https://wiki.seeedstudio.com/XIAO-RP2040/
- CryptoAuthLib: https://github.com/MicrochipTech/cryptoauthlib

---
**Document Version:** 1.0  
**Last Updated:** February 13, 2026  
**Status:** Ready for Production
