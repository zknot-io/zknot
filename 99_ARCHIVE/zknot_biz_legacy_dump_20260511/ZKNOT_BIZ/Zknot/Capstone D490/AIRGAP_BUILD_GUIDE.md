# ZKnot Witness Air-Gap v1 — Build Guide
# Pi Pico + ATECC608B + SSD1306 OLED + GM65 QR Scanner + USB Power Bank
# ─────────────────────────────────────────────────────────────────────

## THE ONE PART YOU STILL NEED TO ORDER

Search Amazon for:   GM65 barcode scanner module UART
Price:               ~$8-12
What to look for:
  - "GM65" in the title (this is the decoder chip model)
  - UART TTL output (NOT USB HID)
  - 3.3V to 5V power
  - 4-pin or 5-pin connector

Good search terms:   "CJMCU GM65 QR scanner UART"
                     "GM65-S barcode reader module serial"

The GM65 looks like a small PCB (about 30x20mm) with a camera lens
on one side and a 4-5 pin JST or bare-wire connector.

While you wait for it: everything else can be built and tested now.
The firmware runs and tests the ATECC + OLED independently.


## WHAT YOU'RE BUILDING

A completely air-gapped signing device:

  ┌─────────────────────────────────────────────┐
  │  USB Power Bank                             │
  │       │ (power only, no data)               │
  │       ▼                                     │
  │  Raspberry Pi Pico (RP2040)                 │
  │       │                                     │
  │    I2C bus (GP4/GP5) ──────────┐            │
  │       │                        │            │
  │  [ATECC608B]            [SSD1306 OLED]      │
  │  secure element         128x64 display      │
  │       │                                     │
  │  UART0 (GP0/GP1/GP2)                        │
  │       │                                     │
  │  [GM65 QR Scanner]                          │
  │  reads challenge from screen                │
  │                                             │
  │  [Button] GP15                              │
  │  confirms signing                           │
  └─────────────────────────────────────────────┘

NO USB DATA LINES CONNECTED. EVER.
Power bank → Pico VBUS (pin 40) via USB cable where
D+ and D- wires are cut or not connected.


## MAKING A POWER-ONLY USB CABLE

Option A (cleanest): Buy a "USB charge-only cable" or "USB data blocker"
  Search: "USB data blocker" or "USB condom" — ~$5-8
  These pass VBUS and GND only. No modification needed.

Option B (DIY from your parts):
  You have a USB Type A female breakout (SparkFun 1568-12700-ND).
  Use your PTC fuse (60R050XU, 500mA) on VBUS.
  Leave D+ and D- unconnected or tied to GND via 10kΩ resistors.
  Connect VBUS (pin 1) and GND (pin 4) to your breadboard rails.

  USB Type A pinout:
    Pin 1: VBUS (+5V)  ← connect to Pico VBUS via PTC fuse
    Pin 2: D-          ← leave OPEN (or tie to GND via 10kΩ)
    Pin 3: D+          ← leave OPEN (or tie to GND via 10kΩ)
    Pin 4: GND         ← connect to GND

  PTC fuse placement: between USB Pin 1 and Pico VBUS.
  Use 60R050XU (60V, 500mA) — protects against overcurrent.


## BREADBOARD WIRING

Power first:
─────────────────────────────────────────────────────────────
  USB VBUS (after PTC fuse)  →  Pico VBUS pin 40
  USB GND                    →  Pico GND  pin 38
  Pico 3V3_OUT pin 36        →  breadboard + rail (3.3V)
  Pico GND        pin 38     →  breadboard - rail (GND)

ATECC608B (via SOIC adapter — same as v1):
─────────────────────────────────────────────────────────────
  Chip VCC (pin 8)  →  3.3V rail
  Chip GND (pin 4)  →  GND rail
  Chip SDA (pin 5)  →  Pico GP4 (pin 6)
  Chip SCL (pin 6)  →  Pico GP5 (pin 7)
  0.1µF cap between VCC and GND (as close to chip as possible)

SSD1306 OLED (4-pin I2C):
─────────────────────────────────────────────────────────────
  VCC  →  3.3V rail
  GND  →  GND rail
  SDA  →  Pico GP4 (same I2C bus — fine)
  SCL  →  Pico GP5 (same I2C bus — fine)

GM65 QR Scanner (4 or 5 pin):
─────────────────────────────────────────────────────────────
  VCC   →  3.3V rail  (some modules want 5V — check yours)
  GND   →  GND rail
  TX    →  Pico GP1   (UART0 RX on Pico)
  RX    →  Pico GP0   (UART0 TX on Pico)
  TRIG  →  Pico GP2   (pull LOW = trigger scan)

  NOTE: If your GM65 module label says "KEY" instead of "TRIG",
  that's the same pin. Some modules also have a "BUZZ" pin for
  the internal buzzer — leave that unconnected.

  If your GM65 VCC is 5V only:
    Connect VCC to Pico VBUS (5V via USB) not the 3.3V rail.
    TX/RX are still 3.3V logic — no level shifting needed.
    Most GM65 modules accept 3.3V logic even at 5V power.

Tactile button:
─────────────────────────────────────────────────────────────
  One pin  →  Pico GP15 (pin 20)
  Other    →  GND rail


## GM65 CONFIGURATION (one-time setup)

The GM65 needs to be configured for triggered mode (single scan
on TRIG pulse) rather than continuous mode. By default it may
be in continuous mode (scans constantly, drains battery).

Configure via serial command (from Pico REPL or test script):

  from machine import UART, Pin
  import time
  u = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
  
  # Set to triggered mode (single scan on TRIG pulse)
  # GM65 command: 0x7E 0xFF 0x02 0x01 0x00 0x00 0xFF
  # (proprietary protocol — refer to GM65 datasheet)
  u.write(bytes([0x7E, 0xFF, 0x02, 0x01, 0x00, 0x00, 0xFF]))
  time.sleep_ms(100)
  resp = u.read()
  print(resp)  # should respond with ACK

If you can't find the GM65 datasheet, the simpler approach:
Just use continuous mode and let the Pico manage power by
cutting VCC via a GPIO-controlled transistor (enhancement later).


## FIRMWARE INSTALLATION

Same as ZKnot Witness v1 — copy all firmware files:

  cd zknot-airgap/firmware/
  
  mpremote connect /dev/ttyACM0 cp atecc608b.py  :atecc608b.py
  mpremote connect /dev/ttyACM0 cp ssd1306.py    :ssd1306.py
  mpremote connect /dev/ttyACM0 cp qrcode.py     :qrcode.py
  mpremote connect /dev/ttyACM0 cp gm65.py       :gm65.py
  mpremote connect /dev/ttyACM0 cp main.py       :main.py

Test I2C first (without GM65):
  mpremote connect /dev/ttyACM0 repl
  >>> from machine import I2C, Pin
  >>> i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)
  >>> i2c.scan()
  [60, 96]    ← OLED (0x3C) and ATECC608B (0x60)


## BROWSER SETUP

The browser page requires no server. Open index.html directly:
  firefox browser/index.html
  # or
  chromium browser/index.html

For webcam QR scanning you need HTTPS or localhost.
Easiest on Linux:
  python3 -m http.server 8080 --directory browser/
  # then open http://localhost:8080

Camera permission will be requested on first use.


## THE SIGNING FLOW (end to end)

1. Open browser page → nonce QR appears on screen
2. Power the ZKnot Air-Gap device (USB power bank → device)
3. Splash screen appears on OLED
4. Press button → scanner activates → point camera at screen QR
5. Device reads and parses the challenge
6. OLED shows "Sign NONCE? [digest]" confirmation
7. Press button → ATECC608B signs
8. OLED shows "Sig part 1/2" label then QR1 appears
9. Hold device OLED up to computer webcam → browser scans QR1
10. Press button on device → QR2 appears
11. Hold device OLED up to webcam → browser scans QR2
12. Browser shows verified signature record → download .zksig
13. Press button on device → return to splash


## THE CONSTRAINT MODEL

What makes this a true constraint:
  - USB cable carries only VBUS + GND
  - D+ and D- are physically absent
  - There is no software path to exfiltrate key material
  - The signing key never leaves the ATECC608B silicon
  - The only data output is optical (OLED → camera)
  - The only data input is optical (screen → GM65)

A policy can be changed. A missing wire cannot.
This is the patent claim: physical constraint replaces procedural trust.


## NEXT STEPS (STM32 migration path)

The STM32U585 you ordered supports:
  - USB Full Speed (can enumerate as HID for power-only mode)
  - I2C for ATECC608B
  - DCMI (Digital Camera Interface) for direct camera modules
  - Much lower deep-sleep current (~1µA vs ~0.8mA for Pico)
  
The Pico version is the proof-of-concept.
The STM32U585 version is the production device.
The firmware architecture is identical — only the HAL layer changes.
