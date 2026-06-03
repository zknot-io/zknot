"""
ZKnot Witness — Main Firmware
Raspberry Pi Pico (RP2040) + ATECC608B + SSD1306 OLED + Tactile Button

USB Serial Protocol:
    Host → Device:  CMD|PAYLOAD\n
    Device → Host:  STATUS|PAYLOAD\n

Commands:
    INFO              → returns device serial + public key
    SIGN|<hex32>      → sign a 32-byte digest (after button press)
    PUBKEY            → return current public key
    PROVISION         → generate new key pair (first-time setup only)
    PING              → health check

Responses:
    OK|<hex_payload>
    ERR|<message>
    WAITING           → displayed on OLED, waiting for button
    CANCELLED         → user did not press button within timeout

Provisional Patent Application No. 63/961,098
"""

import sys
import time
import select
import hashlib
import ubinascii
from machine import I2C, Pin, Timer

from atecc608b import ATECC608B, ATECC608BError
from ssd1306 import SSD1306_I2C


# ─── Pin assignments ──────────────────────────────────────────────────────────
# I2C bus 0 — shared by ATECC608B and OLED
# ATECC608B: SDA=GP4, SCL=GP5 (address 0x60)
# OLED:      SDA=GP4, SCL=GP5 (address 0x3C)
I2C_SDA_PIN    = 4
I2C_SCL_PIN    = 5
I2C_FREQ       = 100_000   # 100kHz — ATECC608B max is 1MHz but 100k is safe for breadboard

BUTTON_PIN     = 15   # GP15 — active LOW, pull-up enabled
LED_PIN        = 25   # onboard LED (GP25 on Pico)

# ─── Display config ───────────────────────────────────────────────────────────
OLED_WIDTH     = 128
OLED_HEIGHT    = 64   # change to 32 if using the 0.91" modules
OLED_ADDR      = 0x3C

# ─── Signing config ───────────────────────────────────────────────────────────
KEY_SLOT           = 0
BUTTON_TIMEOUT_MS  = 30_000   # 30 seconds to press button before cancel
SIGN_COOLDOWN_MS   = 500      # minimum ms between sign operations


# ─── Hardware init ────────────────────────────────────────────────────────────

def init_hardware():
    """Initialize I2C bus, OLED, ATECC608B, button, and LED."""
    i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=I2C_FREQ)

    # Scan I2C bus on startup to confirm devices are present
    devices = i2c.scan()
    expected = {OLED_ADDR, 0x60}  # OLED and ATECC608B
    for addr in expected:
        if addr not in devices:
            # Don't crash — report via USB and try to continue
            usb_send("ERR", f"I2C device 0x{addr:02X} not found. Found: {[hex(d) for d in devices]}")

    oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=OLED_ADDR)
    chip = ATECC608B(i2c, address=0x60)
    button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
    led = Pin(LED_PIN, Pin.OUT)

    return i2c, oled, chip, button, led


# ─── USB serial helpers ───────────────────────────────────────────────────────

def usb_send(status: str, payload: str = ""):
    """Send a response line over USB serial."""
    if payload:
        print(f"{status}|{payload}")
    else:
        print(status)


def usb_readline_nonblocking() -> str | None:
    """
    Read a line from stdin without blocking.
    Returns the line (stripped) or None if nothing available.
    """
    if select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        return line.strip() if line else None
    return None


# ─── OLED display helpers ─────────────────────────────────────────────────────

def oled_clear(oled):
    oled.fill(0)
    oled.show()


def oled_splash(oled):
    """Boot screen."""
    oled.fill(0)
    oled.text("ZKnot Witness", 8, 0, 1)
    oled.hline(0, 10, 128, 1)
    oled.text("v1.0", 48, 16, 1)
    oled.text("Ready", 44, 32, 1)
    oled.text("ZKNOT Systems", 8, 52, 1)
    oled.show()


def oled_waiting_for_button(oled, digest_hex: str):
    """
    Show the confirmation screen with truncated digest.
    The user sees what they're signing before pressing the button.
    """
    oled.fill(0)
    oled.text("SIGN REQUEST", 16, 0, 1)
    oled.hline(0, 10, 128, 1)
    oled.text("Digest:", 0, 14, 1)
    # Show first 8 and last 4 hex chars of digest (first 4 bytes + last 2)
    short = digest_hex[:8] + ".." + digest_hex[-4:]
    oled.text(short, 8, 24, 1)
    oled.hline(0, 36, 128, 1)
    oled.text("Press button", 16, 40, 1)
    oled.text("to sign", 36, 52, 1)
    oled.show()


def oled_signing(oled):
    oled.fill(0)
    oled.text("Signing...", 24, 24, 1)
    oled.show()


def oled_success(oled):
    oled.fill(0)
    oled.text("Signed!", 40, 20, 1)
    oled.text("OK", 56, 36, 1)
    oled.show()
    time.sleep_ms(1200)


def oled_cancelled(oled):
    oled.fill(0)
    oled.text("Cancelled", 28, 20, 1)
    oled.text("Timeout", 36, 36, 1)
    oled.show()
    time.sleep_ms(800)


def oled_error(oled, msg: str):
    oled.fill(0)
    oled.text("ERROR", 40, 8, 1)
    oled.hline(0, 18, 128, 1)
    # Truncate message to fit 16 chars per line
    oled.text(msg[:16], 0, 26, 1)
    if len(msg) > 16:
        oled.text(msg[16:32], 0, 38, 1)
    oled.show()


def oled_provisioned(oled, pubkey_hex: str):
    oled.fill(0)
    oled.text("Key Generated!", 8, 0, 1)
    oled.hline(0, 10, 128, 1)
    oled.text("PubKey (X):", 0, 14, 1)
    oled.text(pubkey_hex[:16], 0, 26, 1)
    oled.text(pubkey_hex[16:32], 0, 38, 1)
    oled.text("See USB output", 0, 52, 1)
    oled.show()


# ─── LED feedback ─────────────────────────────────────────────────────────────

def led_blink(led, times: int = 1, on_ms: int = 80, off_ms: int = 80):
    for _ in range(times):
        led.on()
        time.sleep_ms(on_ms)
        led.off()
        time.sleep_ms(off_ms)


# ─── Command handlers ─────────────────────────────────────────────────────────

def handle_ping(oled, chip, led):
    led_blink(led, 1)
    usb_send("OK", "PONG")


def handle_info(oled, chip, led):
    """Return device serial number and current public key."""
    try:
        serial = chip.serial_number()
        pubkey = chip.get_public_key(KEY_SLOT)
        serial_hex = ubinascii.hexlify(serial).decode()
        pubkey_hex = ubinascii.hexlify(pubkey).decode()
        usb_send("OK", f"SERIAL={serial_hex},PUBKEY={pubkey_hex}")
        led_blink(led, 2)
    except ATECC608BError as e:
        usb_send("ERR", str(e))
        oled_error(oled, str(e))


def handle_pubkey(oled, chip, led):
    """Return just the public key."""
    try:
        pubkey = chip.get_public_key(KEY_SLOT)
        pubkey_hex = ubinascii.hexlify(pubkey).decode()
        usb_send("OK", pubkey_hex)
    except ATECC608BError as e:
        usb_send("ERR", str(e))


def handle_provision(oled, chip, led):
    """
    Generate a new key pair in slot 0.
    This OVERWRITES the existing private key — only call during setup.
    The firmware asks for confirmation via button press before generating.
    """
    oled.fill(0)
    oled.text("PROVISION", 28, 0, 1)
    oled.hline(0, 10, 128, 1)
    oled.text("Generate new key?", 0, 16, 1)
    oled.text("THIS CANNOT BE", 0, 28, 1)
    oled.text("UNDONE", 36, 40, 1)
    oled.text("Press to confirm", 0, 52, 1)
    oled.show()

    # Wait for button confirmation
    button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
    start = time.ticks_ms()
    while button.value() == 1:  # waiting for press (active LOW)
        if time.ticks_diff(time.ticks_ms(), start) > BUTTON_TIMEOUT_MS:
            oled_cancelled(oled)
            usb_send("CANCELLED")
            return

    try:
        oled_signing(oled)
        pubkey = chip.gen_key(KEY_SLOT)
        pubkey_hex = ubinascii.hexlify(pubkey).decode()
        oled_provisioned(oled, pubkey_hex)
        usb_send("OK", f"PUBKEY={pubkey_hex}")
        led_blink(led, 3, on_ms=150)
    except ATECC608BError as e:
        usb_send("ERR", str(e))
        oled_error(oled, str(e))


def handle_sign(oled, chip, button, led, digest_hex: str):
    """
    Main signing flow:
    1. Validate digest
    2. Show confirmation screen
    3. Wait for button press (with timeout)
    4. Send to ATECC608B for signing
    5. Return signature over USB
    """
    # Validate
    if len(digest_hex) != 64:
        usb_send("ERR", f"Digest must be 64 hex chars (32 bytes), got {len(digest_hex)}")
        return

    try:
        digest_bytes = ubinascii.unhexlify(digest_hex)
    except Exception:
        usb_send("ERR", "Invalid hex in digest")
        return

    # Show the confirmation screen
    oled_waiting_for_button(oled, digest_hex)
    usb_send("WAITING")

    # Wait for button press
    start = time.ticks_ms()
    pressed = False
    while True:
        if button.value() == 0:  # active LOW
            # Debounce
            time.sleep_ms(20)
            if button.value() == 0:
                pressed = True
                break
        elapsed = time.ticks_diff(time.ticks_ms(), start)
        if elapsed > BUTTON_TIMEOUT_MS:
            break

    if not pressed:
        oled_cancelled(oled)
        usb_send("CANCELLED")
        # Return to splash after a moment
        time.sleep_ms(1000)
        oled_splash(oled)
        return

    # User confirmed — sign
    oled_signing(oled)
    led.on()

    try:
        signature = chip.sign(digest_bytes, KEY_SLOT)
        sig_hex = ubinascii.hexlify(signature).decode()
        pubkey = chip.get_public_key(KEY_SLOT)
        pubkey_hex = ubinascii.hexlify(pubkey).decode()

        led.off()
        oled_success(oled)
        led_blink(led, 2, on_ms=100)

        # Return signature + public key so host can verify immediately
        usb_send("OK", f"SIG={sig_hex},PUBKEY={pubkey_hex}")

    except ATECC608BError as e:
        led.off()
        usb_send("ERR", str(e))
        oled_error(oled, str(e))

    # Return to splash
    oled_splash(oled)


# ─── Main loop ────────────────────────────────────────────────────────────────

def main():
    i2c, oled, chip, button, led = init_hardware()

    # Boot LED blink
    led_blink(led, 3, on_ms=60, off_ms=60)

    # Show splash
    oled_splash(oled)

    # Confirm ATECC608B is alive
    try:
        info = chip.info()
        # Info returns 4 bytes of revision data — just check it responds
    except ATECC608BError as e:
        oled_error(oled, "ATECC not found")
        usb_send("ERR", f"ATECC608B not responding: {e}")
        # Don't halt — continue so USB is usable for debugging

    usb_send("OK", "READY")

    # Main command loop
    while True:
        line = usb_readline_nonblocking()
        if line is None:
            time.sleep_ms(10)
            continue

        line = line.strip()
        if not line:
            continue

        parts = line.split("|", 1)
        cmd = parts[0].upper()
        payload = parts[1] if len(parts) > 1 else ""

        if cmd == "PING":
            handle_ping(oled, chip, led)

        elif cmd == "INFO":
            handle_info(oled, chip, led)

        elif cmd == "PUBKEY":
            handle_pubkey(oled, chip, led)

        elif cmd == "PROVISION":
            handle_provision(oled, chip, led)

        elif cmd == "SIGN":
            if not payload:
                usb_send("ERR", "SIGN requires a 64-char hex digest payload")
            else:
                handle_sign(oled, chip, button, led, payload.strip())

        else:
            usb_send("ERR", f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
