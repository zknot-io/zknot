"""
ZKnot Witness Air-Gap — Main Firmware
Raspberry Pi Pico (RP2040)

Hardware:
    ATECC608B  — I2C0, GP4 (SDA), GP5 (SCL)
    SSD1306    — I2C0, GP4 (SDA), GP5 (SCL), addr 0x3C
    GM65       — UART0, GP0 (TX), GP1 (RX), GP2 (TRIG)
    Button     — GP15, active LOW, internal pull-up
    LED        — GP25 (onboard)

Power:
    USB power bank → Pico VBUS (pin 40)
    NO data lines used. Device is completely air-gapped.

Signing flow:
    1. Idle screen shown
    2. User presses button → scanner activates
    3. Device reads challenge QR from screen
    4. Parses challenge: mode (nonce|hash) + 32-byte value
    5. OLED shows "Sign? [digest preview] Press to confirm"
    6. User presses button → ATECC608B signs
    7. OLED shows QR1 of signature (first 32 bytes / 64 hex chars)
    8. User presses button → OLED shows QR2 (last 32 bytes / 64 hex chars)
    9. User presses button → back to idle

Provisional Patent Application No. 63/961,098
"""

import time
import ubinascii
from machine import I2C, Pin, freq

# Boost CPU to 133MHz for QR generation (default 125MHz, fine either way)
freq(133_000_000)

from atecc608b import ATECC608B, ATECC608BError
from ssd1306 import SSD1306_I2C
from gm65 import GM65Scanner, parse_challenge
from qrcode import make_qr


# ─── Pin config ───────────────────────────────────────────────────────────────
I2C_SDA       = 4
I2C_SCL       = 5
OLED_ADDR     = 0x3C
ATECC_ADDR    = 0x60
BUTTON_PIN    = 15
LED_PIN       = 25

UART_TX       = 0
UART_RX       = 1
SCANNER_TRIG  = 2

OLED_W        = 128
OLED_H        = 64
KEY_SLOT      = 0


# ─── Hardware init ────────────────────────────────────────────────────────────

def init():
    i2c = I2C(0, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=100_000)
    oled = SSD1306_I2C(OLED_W, OLED_H, i2c, addr=OLED_ADDR)
    chip = ATECC608B(i2c, address=ATECC_ADDR)
    scanner = GM65Scanner(uart_id=0, tx_pin=UART_TX, rx_pin=UART_RX, trig_pin=SCANNER_TRIG)
    button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
    led = Pin(LED_PIN, Pin.OUT)
    return oled, chip, scanner, button, led


# ─── OLED helpers ─────────────────────────────────────────────────────────────

def oled_clear(oled):
    oled.fill(0)
    oled.show()

def oled_splash(oled):
    oled.fill(0)
    oled.text("ZKnot Witness", 8, 0, 1)
    oled.hline(0, 11, 128, 1)
    oled.text("Air-Gap v1", 24, 18, 1)
    oled.text("Press button", 16, 34, 1)
    oled.text("to scan", 36, 46, 1)
    oled.show()

def oled_scanning(oled, dot_state):
    oled.fill(0)
    oled.text("Scanning QR", 20, 10, 1)
    oled.text("Point camera at", 4, 26, 1)
    oled.text("challenge screen", 0, 38, 1)
    dots = "." * (dot_state % 4)
    oled.text(dots, 56, 52, 1)
    oled.show()

def oled_confirm(oled, mode, val_hex):
    oled.fill(0)
    mode_label = "NONCE" if mode == "nonce" else "HASH"
    oled.text(f"Sign {mode_label}?", 20, 0, 1)
    oled.hline(0, 11, 128, 1)
    # Show first 8 and last 4 chars of value
    short = val_hex[:8] + ".." + val_hex[-4:]
    oled.text(short, 8, 18, 1)
    oled.hline(0, 30, 128, 1)
    oled.text("Press = SIGN", 16, 38, 1)
    oled.text("Wait  = CANCEL", 4, 52, 1)
    oled.show()

def oled_signing(oled):
    oled.fill(0)
    oled.text("Signing...", 24, 24, 1)
    oled.show()

def oled_error(oled, msg):
    oled.fill(0)
    oled.text("ERROR", 44, 0, 1)
    oled.hline(0, 11, 128, 1)
    oled.text(msg[:16], 0, 20, 1)
    if len(msg) > 16:
        oled.text(msg[16:32], 0, 34, 1)
    oled.text("Press to retry", 4, 52, 1)
    oled.show()

def oled_show_qr(oled, matrix, label):
    """
    Render a QR matrix onto the 128x64 OLED.
    
    Strategy: center the QR on the display with a quiet zone.
    QR version 3 = 29x29 modules.
    At 2px per module: 58x58 pixels, centered in 128x64.
    Left margin: (128-58)//2 = 35px
    Top margin: (64-58)//2 = 3px
    
    We also add a 1-module quiet zone (2px) around the QR.
    Final: 31x31 modules * 2 = 62x62px
    Left: (128-62)//2 = 33px, Top: (64-62)//2 = 1px
    """
    oled.fill(1)  # white background (inverted for QR — dark on light)
    
    size = len(matrix)
    scale = 2
    # With quiet zone
    total_px = (size + 2) * scale
    x_off = (OLED_W - total_px) // 2
    y_off = (OLED_H - total_px) // 2

    # QR is dark-on-light: fill background white, draw dark modules
    oled.fill_rect(x_off, y_off, total_px, total_px, 0)  # white background

    for row in range(size):
        for col in range(size):
            if matrix[row][col]:  # dark module
                x = x_off + (col + 1) * scale  # +1 for quiet zone
                y = y_off + (row + 1) * scale
                oled.fill_rect(x, y, scale, scale, 1)

    # Label at bottom if there's room (there isn't much — skip for QR clarity)
    # oled.text(label, 0, 58, 0)  # would overlap QR
    oled.show()

def oled_qr_prompt(oled, part, total):
    """Show between QR codes — tell user to scan then press button."""
    oled.fill(0)
    oled.text(f"Sig part {part}/{total}", 16, 4, 1)
    oled.hline(0, 16, 128, 1)
    oled.text("Scan this QR", 16, 24, 1)
    oled.text("with your phone", 4, 36, 1)
    oled.text("Press to advance", 0, 52, 1)
    oled.show()

def oled_done(oled):
    oled.fill(0)
    oled.text("Signature sent", 8, 12, 1)
    oled.text("via QR codes.", 12, 28, 1)
    oled.text("Press to restart", 0, 50, 1)
    oled.show()


# ─── Button helpers ───────────────────────────────────────────────────────────

def wait_button_press(button, timeout_ms=30000):
    """
    Block until button is pressed (active LOW) or timeout.
    Returns True if pressed, False if timeout.
    """
    start = time.ticks_ms()
    while button.value() == 1:
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            return False
        time.sleep_ms(20)
    # Debounce
    time.sleep_ms(30)
    # Wait for release
    while button.value() == 0:
        time.sleep_ms(10)
    return True


def led_blink(led, n=1, on_ms=80, off_ms=80):
    for _ in range(n):
        led.on()
        time.sleep_ms(on_ms)
        led.off()
        time.sleep_ms(off_ms)


# ─── Main signing flow ────────────────────────────────────────────────────────

def signing_cycle(oled, chip, scanner, button, led):
    """
    One complete sign-and-display cycle.
    Returns True on success, False on cancel/error.
    """

    # ── Step 1: Scan the challenge QR ────────────────────────────────────────
    dot_state = 0
    raw = None

    def on_waiting():
        nonlocal dot_state
        oled_scanning(oled, dot_state)
        dot_state += 1

    raw = scanner.scan_blocking(
        timeout_ms=20000,
        on_waiting=on_waiting,
    )

    if raw is None:
        oled_error(oled, "No QR found")
        time.sleep_ms(2000)
        return False

    # ── Step 2: Parse challenge ───────────────────────────────────────────────
    parsed = parse_challenge(raw)
    if parsed is None:
        oled_error(oled, "Bad challenge")
        time.sleep_ms(2000)
        return False

    mode, val_hex = parsed

    # ── Step 3: Show confirmation, wait for button ────────────────────────────
    oled_confirm(oled, mode, val_hex)

    pressed = wait_button_press(button, timeout_ms=30000)
    if not pressed:
        oled_error(oled, "Timeout")
        time.sleep_ms(1500)
        return False

    # ── Step 4: Sign with ATECC608B ───────────────────────────────────────────
    oled_signing(oled)
    led.on()

    try:
        digest_bytes = bytes.fromhex(val_hex)
        signature = chip.sign(digest_bytes, KEY_SLOT)
        pubkey = chip.get_public_key(KEY_SLOT)
        led.off()
        led_blink(led, 2, on_ms=100)
    except ATECC608BError as e:
        led.off()
        oled_error(oled, str(e)[:32])
        time.sleep_ms(3000)
        return False
    except Exception as e:
        led.off()
        oled_error(oled, "Sign failed")
        time.sleep_ms(3000)
        return False

    # ── Step 5: Encode signature as two QR codes ──────────────────────────────
    sig_hex = ubinascii.hexlify(signature).decode()
    pub_hex = ubinascii.hexlify(pubkey).decode()

    # Split signature: R (first 32 bytes = 64 hex) and S (last 32 bytes = 64 hex)
    sig_r = sig_hex[:64]   # 64 chars — fits in QR version 3
    sig_s = sig_hex[64:]   # 64 chars — fits in QR version 3

    # QR1 payload: "1|<mode>|<val_hex[:8]>|<sig_r>"
    # QR2 payload: "2|<sig_s>|<pub_hex[:32]>"  (first half of pubkey)
    # This gives the browser everything it needs to reconstruct and verify.
    qr1_data = f"1|{mode}|{val_hex[:8]}|{sig_r}"   # ~80 chars → version 4
    qr2_data = f"2|{sig_s}|{pub_hex}"               # ~2+64+128 = too long

    # Revised: keep it minimal
    # QR1: sig R component
    # QR2: sig S component  
    # Public key is stored/known by the browser from provisioning
    qr1_data = f"ZKNOT1|{sig_r}"   # 71 chars → version 3/4
    qr2_data = f"ZKNOT2|{sig_s}"   # 71 chars → version 3/4

    # Generate QR matrices
    try:
        oled.fill(0)
        oled.text("Generating QR...", 0, 28, 1)
        oled.show()

        qr1_matrix = make_qr(qr1_data)
        qr2_matrix = make_qr(qr2_data)
    except Exception as e:
        oled_error(oled, "QR gen failed")
        time.sleep_ms(3000)
        return False

    # ── Step 6: Show QR1 ─────────────────────────────────────────────────────
    oled_qr_prompt(oled, 1, 2)
    time.sleep_ms(1200)

    oled_show_qr(oled, qr1_matrix, "1/2")

    pressed = wait_button_press(button, timeout_ms=60000)
    if not pressed:
        # Timeout — redisplay and wait again (user might be scanning)
        oled_show_qr(oled, qr1_matrix, "1/2")
        wait_button_press(button, timeout_ms=60000)

    # ── Step 7: Show QR2 ─────────────────────────────────────────────────────
    oled_qr_prompt(oled, 2, 2)
    time.sleep_ms(1200)

    oled_show_qr(oled, qr2_matrix, "2/2")

    wait_button_press(button, timeout_ms=60000)

    # ── Done ─────────────────────────────────────────────────────────────────
    oled_done(oled)
    led_blink(led, 3, on_ms=150)

    wait_button_press(button, timeout_ms=60000)

    return True


# ─── Main loop ────────────────────────────────────────────────────────────────

def main():
    oled, chip, scanner, button, led = init()

    led_blink(led, 3, on_ms=60, off_ms=60)

    # Verify ATECC608B
    try:
        chip.info()
    except ATECC608BError:
        oled_error(oled, "ATECC not found!")
        # Don't halt — show error and let user try

    oled_splash(oled)

    while True:
        # Wait for button press to start a scan cycle
        if not wait_button_press(button, timeout_ms=None if True else 0):
            continue

        led_blink(led, 1)
        signing_cycle(oled, chip, scanner, button, led)

        # Return to splash
        oled_splash(oled)


if __name__ == "__main__":
    main()
