# ZKKey Connect Pico — 100 kHz I2C diagnostic
# Tests whether the Adafruit CRC mismatch bug is a clock-stretch timing issue.
# NO WRITES. NO LOCKS. Pure read-test.

import board, busio, time
import displayio, i2cdisplaybus, terminalio
from adafruit_display_text import label

# --- Force 100 kHz I2C instead of STEMMA_I2C's 400 kHz default ---
displayio.release_displays()
i2c = busio.I2C(board.GP5, board.GP4, frequency=100_000)

# OLED setup (try SSD1306 first, fall back to SH1106)
try:
    from adafruit_displayio_ssd1306 import SSD1306
    display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
    display = SSD1306(display_bus, width=128, height=64)
    oled_driver = "SSD1306"
except Exception:
    from adafruit_displayio_sh1106 import SH1106
    display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
    display = SH1106(display_bus, width=128, height=64, colstart=2)
    oled_driver = "SH1106"

g = displayio.Group(); display.root_group = g
l1 = label.Label(terminalio.FONT, text="100kHz DIAG", color=0xFFFFFF, x=4, y=10)
l2 = label.Label(terminalio.FONT, text=f"OLED:{oled_driver}", color=0xFFFFFF, x=4, y=26)
l3 = label.Label(terminalio.FONT, text="Testing...", color=0xFFFFFF, x=4, y=42)
l4 = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=4, y=58)
g.append(l1); g.append(l2); g.append(l3); g.append(l4)

print("\n" + "=" * 60)
print("100 kHz I2C DIAGNOSTIC — no writes, no locks")
print("=" * 60)

from adafruit_atecc.adafruit_atecc import ATECC
atecc = ATECC(i2c)

# Baseline: confirm short ops still work at 100 kHz
print("\n[1] Reading serial number (short op, should always work)...")
try:
    serial = atecc.serial_number
    print(f"    OK: {serial}")
except Exception as e:
    print(f"    FAIL: {type(e).__name__}: {e}")

print("\n[2] Reading lock state...")
try:
    locked = atecc.locked
    print(f"    OK: config locked = {locked}")
except Exception as e:
    print(f"    FAIL: {type(e).__name__}: {e}")
    locked = None

# The actual test: try the 64-byte-response operations
print("\n[3] Attempting gen_key (the operation that was failing)...")
print("    Expected on virgin chip: 'zone not locked' error (config zone not locked yet)")
print("    Expected if CRC bug remains: 'CRC Mismatch' error")
try:
    pubkey = bytearray(64)
    atecc.gen_key(pubkey, 0, private_key=False)  # public-only read attempt
    print(f"    UNEXPECTED OK: got 64 bytes back: {bytes(pubkey).hex()[:32]}...")
except Exception as e:
    err_type = type(e).__name__
    err_msg = str(e)
    print(f"    Error: {err_type}: {err_msg}")
    if "CRC" in err_msg or "crc" in err_msg:
        print("    -> CRC bug still present at 100 kHz. Clock speed is NOT the cause.")
        l3.text = "CRC: STILL BAD"
    elif "lock" in err_msg.lower() or "zone" in err_msg.lower():
        print("    -> Got a sensible error. CRC bug appears fixed at 100 kHz!")
        l3.text = "CRC: FIXED?"
    else:
        print(f"    -> Different error. Need to interpret: {err_msg}")
        l3.text = "ATECC: OTHER"

l4.text = "See REPL"
print("\n" + "=" * 60)
print("Done. Check the [3] result above to decide next step.")
print("=" * 60)

while True:
    time.sleep(60)
