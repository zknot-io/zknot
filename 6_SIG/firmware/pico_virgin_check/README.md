# Pico Virgin Check Script

CircuitPython script for checking ATECC608B virgin status via the Adafruit
library on a Raspberry Pi Pico.

## What it does

1. Initializes I²C at 100 kHz (slower than default 400 kHz; safer with mixed bus loads)
2. Auto-detects OLED driver (SSD1306 or SH1106)
3. Reads ATECC silicon serial number (always works)
4. Reads ATECC config zone lock state via `atecc.locked` (False = virgin)
5. Attempts `gen_key` (will fail with CRC mismatch on Adafruit lib — known bug)

## How to use

1. Copy this file to a Pico's CIRCUITPY drive as `code.py`
2. Wire ATECC608B to Pico:
   - VIN -> 3.3V
   - GND -> GND
   - SDA -> GP4
   - SCL -> GP5
3. (Optional) Wire SSD1306 OLED to same I²C bus at address 0x3C
4. Plug in Pico, watch REPL output (e.g., via `screen /dev/ttyACM0 115200`)
5. Output line `[2] Reading lock state... config locked = False` = virgin

## Known limitations

- CRC bug in adafruit_atecc means `gen_key` and other 64-byte response ops fail
- Provisioning (writes/locks) should use cryptoauthlib via MCP2221A, not this script
- This script is READ-ONLY — safe to run on any chip including bricked Demo Unit #1

## Recovered from

CIRCUITPY drive of Pico 2 (USB 2e8a:000b), 2026-05-16. Original session 2026-05-11.
See journal entry `2026-05-11_atecc_provisioning_path_locked.md`.
