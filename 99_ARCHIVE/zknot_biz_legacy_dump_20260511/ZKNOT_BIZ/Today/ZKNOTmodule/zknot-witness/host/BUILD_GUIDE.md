# ZKnot Witness v1 — Build Guide
# Raspberry Pi Pico + ATECC608B + SSD1306 OLED + Tactile Button
# ─────────────────────────────────────────────────────────────

## WHAT YOU'RE BUILDING

A USB signing device. You plug it into your computer, send it a
32-byte SHA-256 digest, it shows the digest on the OLED screen,
waits for you to press the physical button, then the ATECC608B
secure element signs it with its internal P256 private key and
sends the 64-byte signature back.

The private key never leaves the ATECC608B chip. Ever.


## PARTS FROM YOUR ORDER (what to pull out)

FROM DIGIKEY ORDER (web ID 368076685):
  [ ] 1x  ATECC608B-SSHDA-T      (IC AUTHENTICATION CHIP 8-SOIC)
  [ ] 3x  LCQT-SOIC8-8           (SOCKET ADAPTER SOIC TO 8DIP)  ← critical
  [ ] 1x  0.1uF 0805 cap         (any of the KGM21KR51H104KU variants)

FROM AMAZON ORDERS:
  [ ] 1x  Raspberry Pi Pico      (RP2040 board)
  [ ] 1x  SSD1306 0.96" OLED     (128x64, I2C, 4-pin)
  [ ] 1x  Tactile button (6x6x5mm, from the 160-piece kit)
  [ ] 1x  Breadboard (830 tie-point)
  [ ] Jumper wires (various lengths from the BOJACK kit)
  [ ] 10kΩ resistor (from the BOJACK resistor kit) — for button pullup
                                                      (Pico has internal
                                                       pullup, optional)

NOT NEEDED YET (save for PCB version):
  STM32F072, STM32U585, crystals, regulators, fuses, USB breakouts


## ATECC608B SOIC ADAPTER — DO THIS FIRST

The ATECC608B-SSHDA-T is an 8-pin SOIC surface-mount chip.
The LCQT-SOIC8-8 adapter lets you plug it into a breadboard.

1. Place the ATECC608B chip into the SOIC socket on the adapter.
   Pin 1 indicator: the chip has a small dot or notch at pin 1.
   The socket has a matching indicator. Align them.

2. Press the chip down firmly until it seats. The socket has
   a locking mechanism — press the sides down.

3. The adapter now has 8 DIP pins that fit a standard breadboard.

ATECC608B-SSHDA-T PINOUT (8-SOIC, pin 1 = dot/notch end):
  Pin 1: NC    (no connect)
  Pin 2: NC    (no connect)  
  Pin 3: NC    (no connect)
  Pin 4: GND   ← connect to GND
  Pin 5: SDA   ← connect to Pico GP4
  Pin 6: SCL   ← connect to Pico GP5
  Pin 7: NC    (no connect)
  Pin 8: VCC   ← connect to 3.3V

  The SSHDA variant = I2C address 0x60 (default, no strapping needed)


## BREADBOARD WIRING

─────────────────────────────────────────────────────────────────
POWER RAILS (set these up first):
  Pico 3V3(OUT) pin 36  →  breadboard + rail (red)
  Pico GND      pin 38  →  breadboard - rail (black)
  
  Note: Pico has two GND pins (3, 8, 13, 18, 23, 28, 33, 38).
        Use any of them.

─────────────────────────────────────────────────────────────────
ATECC608B (via SOIC adapter on breadboard):
  Chip Pin 8 (VCC)  →  3.3V rail
  Chip Pin 4 (GND)  →  GND rail
  Chip Pin 5 (SDA)  →  Pico GP4  (pin 6 on Pico)
  Chip Pin 6 (SCL)  →  Pico GP5  (pin 7 on Pico)

  DECOUPLING CAPACITOR (important for stable operation):
  0.1uF ceramic cap between VCC and GND, placed as close to
  the chip as possible on the breadboard.

─────────────────────────────────────────────────────────────────
SSD1306 OLED (4-pin I2C module):
  VCC  →  3.3V rail
  GND  →  GND rail
  SDA  →  Pico GP4  (same I2C bus as ATECC608B — this is fine)
  SCL  →  Pico GP5  (same I2C bus as ATECC608B — this is fine)

  I2C address: 0x3C (default for most SSD1306 modules)
  The ATECC608B is at 0x60. Both share the same SDA/SCL lines.
  I2C is a shared bus — multiple devices work fine.

─────────────────────────────────────────────────────────────────
TACTILE BUTTON:
  One side of button  →  Pico GP15  (pin 20 on Pico)
  Other side of button →  GND rail

  The firmware enables the internal pull-up on GP15, so no
  external resistor is needed. Button press = GP15 goes LOW.

─────────────────────────────────────────────────────────────────
PICO USB:
  Just plug the Pico's micro-USB into your Linux machine.
  It appears as /dev/ttyACM0 (or ACM1 if something else is on ACM0).

─────────────────────────────────────────────────────────────────


## PICO PIN REFERENCE (physical pin numbers)

    USB
  ┌─────┐
  │     │  1  GP0
  │     │  2  GP1
  │     │  3  GND
  │     │  4  GP2
  │     │  5  GP3
  │     │  6  GP4  ←── SDA (OLED + ATECC608B)
  │     │  7  GP5  ←── SCL (OLED + ATECC608B)
  │     │  8  GND
  │     │  9  GP6
  │     │  10 GP7
  │     │  11 GP8
  │     │  12 GP9
  │     │  13 GND
  │     │  14 GP10
  │     │  15 GP11
  │     │  16 GP12
  │     │  17 GP13
  │     │  18 GND
  │     │  19 GP14
  │     │  20 GP15 ←── BUTTON (to GND)
  │     │  21 GP16
  │     │  22 GP17
  │     │  23 GND
  │     │  24 GP18
  │     │  25 GP19
  │     │  26 GP20
  │     │  27 GP21
  │     │  28 GND
  │     │  29 GP22
  │     │  30 RUN
  │     │  31 GP26
  │     │  32 GP27
  │     │  33 GND
  │     │  34 GP28
  │     │  35 ADC_VREF
  │     │  36 3V3_OUT ←── 3.3V power rail
  │     │  37 3V3_EN
  │     │  38 GND    ←── GND rail
  │     │  39 VSYS
  │     │  40 VBUS
  └─────┘
    USB


## FIRMWARE INSTALLATION (Linux)

─────────────────────────────────────────────────────────────────
STEP 1: Install MicroPython on the Pico

  a. Download the latest MicroPython UF2 for Pico:
     https://micropython.org/download/RPI_PICO/

  b. Hold the BOOTSEL button on the Pico while plugging in USB.
     The Pico appears as a USB drive called RPI-RP2.

  c. Copy the .uf2 file to the RPI-RP2 drive:
     cp ~/Downloads/RPI_PICO-*.uf2 /media/$USER/RPI-RP2/

  d. The Pico reboots and appears as /dev/ttyACM0.

─────────────────────────────────────────────────────────────────
STEP 2: Install mpremote (MicroPython file tool)

  pip install mpremote

─────────────────────────────────────────────────────────────────
STEP 3: Copy firmware files to Pico

  cd zknot-witness/firmware/

  mpremote connect /dev/ttyACM0 cp atecc608b.py :atecc608b.py
  mpremote connect /dev/ttyACM0 cp ssd1306.py   :ssd1306.py
  mpremote connect /dev/ttyACM0 cp main.py       :main.py

  # Verify files are there:
  mpremote connect /dev/ttyACM0 ls

─────────────────────────────────────────────────────────────────
STEP 4: Test with REPL (before running main.py)

  mpremote connect /dev/ttyACM0 repl

  # At the >>> prompt, test I2C scanning:
  from machine import I2C, Pin
  i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)
  print(i2c.scan())
  # Should print something like: [60, 96]
  # 60 = 0x3C (OLED), 96 = 0x60 (ATECC608B)
  # If you only see one address, check your wiring for that device.

  # Ctrl+X to exit REPL

─────────────────────────────────────────────────────────────────
STEP 5: Run main.py

  mpremote connect /dev/ttyACM0 run main.py

  # Or to make it run automatically on boot:
  # main.py already IS the boot file — MicroPython runs main.py
  # automatically on every power-up. You're done.

  # Reset the Pico (unplug/replug or press RUN pin to GND briefly)
  # and it will start automatically.


## HOST SETUP (Linux)

  pip install pyserial cryptography

  # Find your device:
  ls /dev/ttyACM*

  # Test it:
  python3 host/witness_cli.py --port /dev/ttyACM0 ping

  # First-time key generation (DO THIS ONCE):
  python3 host/witness_cli.py --port /dev/ttyACM0 provision
  # Press button on device when prompted
  # Public key is saved to zknot_pubkey.txt

  # Sign a file:
  python3 host/witness_cli.py --port /dev/ttyACM0 sign photo.jpg
  # Press button when the digest appears on OLED
  # Signing record saved as photo.jpg.zksig

  # Verify a signature (no device needed):
  python3 host/verify_sig.py photo.jpg.zksig --file photo.jpg


## TROUBLESHOOTING

Problem: i2c.scan() returns []
  → Check VCC (3.3V) and GND connections
  → Check SDA/SCL are on GP4/GP5
  → ATECC608B: confirm chip is seated fully in SOIC adapter
  → Try the 0.1uF decoupling cap if not installed

Problem: OLED found but ATECC608B not found (scan returns [60] only)
  → Recheck ATECC608B pin orientation — pin 1 dot/notch matters
  → Try a different ATECC608B chip from your order

Problem: OLED not found (scan returns [96] only)
  → Some OLED modules use 0x3D instead of 0x3C
  → Change OLED_ADDR = 0x3D in main.py

Problem: Device responds to ping but sign returns ERR
  → Need to provision first: run provision command
  → Key slot 0 must be configured before signing

Problem: /dev/ttyACM0 permission denied
  → sudo usermod -aG dialout $USER   (then log out/in)
  → or: sudo chmod a+rw /dev/ttyACM0  (temporary fix)

Problem: Pico not appearing as ACM device
  → Make sure you have MicroPython installed (not just the UF2 bootloader)
  → dmesg | tail -20 to see what Linux sees when you plug it in


## WHAT'S NEXT (STM32 migration path)

The STM32F072 in your order has native USB HID support, which means
the final ZKnot Witness can appear as a USB HID device (like a
security key) rather than a serial port. The firmware architecture
is the same — ATECC608B I2C interface, signing flow, button — but
the USB layer changes from serial to HID. We'll tackle that once
the breadboard prototype is confirmed working.
