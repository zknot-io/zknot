# ZKAuth Crypto Authentication Module

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)

A hardware cryptographic authentication module for the Corne split keyboard, featuring the ATECC608B secure element for hardware-based digital signatures.

## 🎯 Overview

The ZKAuth module adds cryptographic authentication capabilities to your keyboard. Press the AUTH key on your keyboard and a physical button on this module to generate a cryptographic signature that proves **you** are typing.

### Use Cases

- **Git commit signing** with hardware keys
- **2FA authentication** without phone
- **Cryptocurrency transaction signing**
- **SSH key authentication**
- **Secure remote work verification**
- **Document signing**

## ✨ Features

- **ATECC608B Secure Element** - Hardware-protected ECDSA P-256 key storage
- **Physical Authentication Button** - Requires physical presence to sign
- **Dual Status LEDs** - Visual feedback for authentication state
- **I2C Interface** - Connects to keyboard via JST-SH connector
- **Seeed XIAO RP2040** - Powerful ARM Cortex-M0+ microcontroller
- **Compact Design** - Only 45mm x 22mm footprint

## 📦 What's Included

This repository contains complete production-ready files:

```
zkauth-module/
├── zkauth_module.kicad_sch      # Schematic (KiCad format)
├── zkauth_module.kicad_pcb      # PCB layout (KiCad format)
├── zkauth_module.kicad_pro      # KiCad project file
├── zkauth_BOM_assembly.md       # Bill of Materials & assembly guide
├── zkauth_firmware.ino          # Arduino firmware for XIAO RP2040
└── README.md                    # This file
```

## 🛠️ Hardware Specifications

### PCB Details
- **Size:** 45mm × 22mm
- **Layers:** 2 (Top/Bottom copper)
- **Thickness:** 1.6mm
- **Components:** All SMD except XIAO RP2040 module

### Key Components
| Component | Part Number | Function |
|-----------|-------------|----------|
| Secure Element | ATECC608B-MAHCZ-T | Crypto chip with key storage |
| Microcontroller | Seeed XIAO RP2040 | Main controller |
| Connector | JST SM04B-SRSS-TB | I2C interface to keyboard |
| Button | B3U-1000P | Physical auth trigger |
| LEDs | 0603 Green/Red | Status indicators |

### Pinout

**JST-SH Connector (to Keyboard)**
```
Pin 1: GND
Pin 2: VCC (3.3V)
Pin 3: SDA (I2C Data)
Pin 4: SCL (I2C Clock)
```

**XIAO RP2040 Connections**
```
D0  → Auth Button
D1  → Green LED (Ready)
D2  → Red LED (Busy)
D7  → I2C SDA
D8  → I2C SCL
3V3 → Power from keyboard
GND → Ground
```

## 🔧 Assembly Instructions

### Required Tools
- Soldering iron (temperature controlled, 300-350°C)
- Solder (leaded or lead-free)
- Tweezers
- Multimeter
- Magnifying glass or microscope (recommended)

### Assembly Steps

1. **Solder ATECC608B (U1)**
   - Use solder paste + hot air OR
   - Hand solder with fine-tip iron
   - Check for bridges between pins!

2. **Solder SMD Components**
   - Start with smallest (0603 resistors/capacitors)
   - Then LEDs (watch polarity!)
   - Then button and connector

3. **Solder XIAO RP2040**
   - Can be soldered directly or use sockets
   - Align carefully before soldering

4. **Visual Inspection**
   - Check all solder joints
   - No bridges on SOIC-8 pins
   - LED polarity correct

5. **Test**
   - Apply 3.3V to JST connector
   - Measure current: should be <10mA
   - Green LED should light up

## 💻 Firmware Setup

### Prerequisites

Install Arduino IDE and add board support:

1. **Install Arduino IDE** (1.8.19 or newer)
   ```
   https://www.arduino.cc/en/software
   ```

2. **Add RP2040 Board Support**
   - File → Preferences → Additional Board URLs
   - Add: `https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json`
   - Tools → Board → Boards Manager
   - Search "rp2040" and install "Raspberry Pi Pico/RP2040"

3. **Install Required Libraries**
   - Sketch → Include Library → Manage Libraries
   - Install: `CryptoAuthLib by Microchip`

### Upload Firmware

1. **Connect XIAO RP2040**
   - USB-C cable to computer
   - Board appears as USB drive

2. **Select Board**
   - Tools → Board → Raspberry Pi Pico/RP2040 → Seeed XIAO RP2040

3. **Upload Sketch**
   - Open `zkauth_firmware.ino`
   - Click Upload button
   - Wait for "Done uploading" message

4. **Verify Operation**
   - Open Serial Monitor (115200 baud)
   - Should see: "ZKAuth Module v1.0"
   - Green LED should be ON

## 🔐 Key Provisioning

**⚠️ WARNING: This is a ONE-TIME operation!**

The ATECC608B must be provisioned with a private key before use. Once locked, the key **cannot** be changed or extracted.

### Provisioning Steps

1. **Uncomment Provisioning Code**
   ```cpp
   // In zkauth_firmware.ino, in setup() function:
   provisionDevice(); // Uncomment this line
   ```

2. **Upload Firmware**
   - Upload modified sketch to XIAO RP2040

3. **Trigger Provisioning**
   - Open Serial Monitor
   - Press auth button within 10 seconds when prompted
   - Wait for "PROVISIONING COMPLETE"

4. **Save Public Key**
   - Copy the displayed public key (128 hex characters)
   - Save to secure location (you'll need this!)

5. **Re-comment Provisioning Code**
   ```cpp
   // provisionDevice(); // Comment out again
   ```

6. **Upload Normal Firmware**
   - Upload sketch again (without provisioning)

### Example Public Key Output
```
Public key (X): 1A2B3C4D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3E4F5A6B7C8D9E0F1A2B
Public key (Y): 2B3C4D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3E4F5A6B7C8D9E0F1A2B3C
```

## 🔌 Integration with Keyboard

### Hardware Connection

1. **Prepare Cable**
   - Use JST-SH 4-pin cable (1mm pitch)
   - Or create custom cable with 28AWG wire

2. **Connect to Keyboard**
   - Match pinout: GND, VCC, SDA, SCL
   - Secure cable with tape or cable tie

3. **Power On**
   - Connect keyboard to computer via USB
   - Module should power up (green LED on)

### I2C Communication Protocol

The module acts as an I2C slave at address `0x50`.

**Commands:**
- `0x01` - Authentication request (followed by 32-byte challenge)
- `0x02` - Status query
- `0x03` - Get public key

**Status Codes:**
- `0x00` - Idle
- `0x01` - Ready (waiting for button)
- `0x02` - Busy (signing)
- `0x03` - Success (signature ready)
- `0xFF` - Error

**Example Flow:**
```
Keyboard → Module: 0x01 [32-byte challenge]
Module → Keyboard: 0x01 (Status: Ready)
[User presses button]
Module → Keyboard: 0x03 (Status: Success)
Keyboard → Module: Request data
Module → Keyboard: [64-byte signature]
```

## 📊 LED Status Indicators

| Green | Red | Meaning |
|-------|-----|---------|
| ON | OFF | Idle/Ready |
| Blinking | OFF | Waiting for button press |
| OFF | ON | Authentication in progress |
| Blinking | Blinking | Success! |
| OFF | Blinking | Error |

## 🧪 Testing

### Basic Functionality Test

```cpp
// Simple I2C scanner sketch
#include <Wire.h>

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  Serial.println("Scanning I2C bus...");
  
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("Device found at 0x");
      if (addr < 16) Serial.print("0");
      Serial.println(addr, HEX);
    }
  }
}

void loop() {}
```

Expected output:
```
Device found at 0x50  (ZKAuth module)
Device found at 0x60  (ATECC608B)
```

### Authentication Test

1. Send auth request with random challenge
2. Green LED should blink (ready)
3. Press button
4. Red LED turns on (busy)
5. Green LED blinks rapidly (success)
6. Read back 64-byte signature

## 📐 PCB Manufacturing

### Recommended Manufacturers

- **JLCPCB** (China) - Cheapest, good quality
- **PCBWay** (China) - Premium quality
- **OSH Park** (USA) - High quality, slower

### JLCPCB Order Settings

```yaml
PCB Specifications:
  Size: 45mm × 22mm
  Quantity: 5 or 10
  Layers: 2
  Thickness: 1.6mm
  Color: Black (recommended)
  Surface Finish: HASL or ENIG
  Copper Weight: 1 oz
  Remove Order Number: Yes

Assembly (Optional):
  Assembly Side: Top
  Confirm Parts Placement: Yes
```

### Cost Estimate

| Quantity | PCB Only | PCB + Assembly |
|----------|----------|----------------|
| 5 units | $5 | $25 |
| 10 units | $8 | $40 |

*Plus components (~$8.60 per unit)*

## 🐛 Troubleshooting

### ATECC608B Not Detected

**Symptoms:** I2C scanner doesn't find device at 0x60

**Solutions:**
- Check solder joints on pins 4-7
- Verify 3.3V on pin 7 with multimeter
- Check I2C pull-up resistors (R4, R5)
- Try slower I2C speed (100kHz)

### Button Not Working

**Symptoms:** Pressing button has no effect

**Solutions:**
- Check R1 (10kΩ pull-up) installed
- Verify C2 (100nF debounce) installed
- Test button continuity
- Check GPIO D0 connection

### LEDs Not Lighting

**Symptoms:** LEDs don't turn on

**Solutions:**
- Verify LED polarity (cathode to GND)
- Check current limiting resistors (R2, R3)
- Test with direct 3.3V connection
- Replace LED if damaged

## 📚 Resources

- **ATECC608B Datasheet:** [Microchip](https://www.microchip.com/wwwproducts/en/ATECC608B)
- **CryptoAuthLib:** [GitHub](https://github.com/MicrochipTech/cryptoauthlib)
- **XIAO RP2040 Wiki:** [Seeed Studio](https://wiki.seeedstudio.com/XIAO-RP2040/)
- **KiCad Documentation:** [KiCad.org](https://docs.kicad.org/)

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

Based on Corne keyboard by foostan (MIT License).

## 🙏 Acknowledgments

- **foostan** - Original Corne keyboard design
- **Microchip** - ATECC608B secure element
- **Seeed Studio** - XIAO RP2040 module
- **Community** - Testing and feedback

## 📬 Support

For questions or issues:
- Open GitHub issue
- Email: [your-email]
- Discord: [your-discord]

## 🚀 Roadmap

### v1.1 (Planned)
- [ ] Optional OLED display support
- [ ] Multiple key slots (up to 16 keys)
- [ ] Battery power option
- [ ] Wireless authentication via BLE

### v2.0 (Future)
- [ ] FIDO2/WebAuthn support
- [ ] Touch sensor instead of button
- [ ] USB-C pass-through
- [ ] Integrated into keyboard PCB

---

**Built with ❤️ for the mechanical keyboard community**

*"The only keyboard that cryptographically proves YOU are typing"*
