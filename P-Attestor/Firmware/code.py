# code.py  --  ZKNOT Rev2 Attestor : Pico signing firmware (CircuitPython)
# =============================================================================
# Press button -> ATECC608 signs a challenge with slot-0 -> signature out over USB.
# 4 LEDs show state: READY / ARMED / BUSY / DONE.
#
# Tier-0 self-assertion. Presence-actuation only (button = "sign now").
# NOT display-then-confirm. Stays on the giveaway side of the PAT-001 line.
#
# Pin map (matches the breadboard wiring):
#   SDA=GP4  SCL=GP5   |  LEDs: READY=GP6 ARMED=GP7 BUSY=GP8 DONE=GP9  |  BTN=GP15
#
# Output over USB serial:
#   BOOT serial=<18hex> selftest=PASS|FAIL
#   SIG <serial> <challenge:64hex> <signature:128hex>   (one per button press)
#
# A host (verify_unit.py) or verifyknot.io/start reads SIG lines and verifies
# the signature against the slot-0 pubkey recorded for that serial in the ledger.
# Optionally, send a 64-hex-char line over serial to set the next challenge
# (then press the button to sign it) -> presence-gated challenge/response.

import board, busio, digitalio, time, os, sys, supervisor
from adafruit_atecc.adafruit_atecc import ATECC

SLOT = 0
PINS = dict(SDA=board.GP4, SCL=board.GP5,
            READY=board.GP6, ARMED=board.GP7, BUSY=board.GP8, DONE=board.GP9,
            BTN=board.GP15)

def _out(pin):
    d = digitalio.DigitalInOut(pin); d.direction = digitalio.Direction.OUTPUT
    d.value = False; return d

ready, armed, busy, done = (_out(PINS[k]) for k in ("READY", "ARMED", "BUSY", "DONE"))
btn = digitalio.DigitalInOut(PINS["BTN"]); btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP   # pressed = LOW

def all_off(): ready.value = armed.value = busy.value = done.value = False
def error_blink():
    for _ in range(6):
        for L in (ready, armed, busy, done): L.value = not L.value
        time.sleep(0.12)
    all_off()
def pulse(led, n=3):
    for _ in range(n):
        led.value = True;  time.sleep(0.1)
        led.value = False; time.sleep(0.1)

def hexs(b):  return "".join("%02x" % x for x in b)
def unhex(s): return bytes(int(s[i:i+2], 16) for i in range(0, len(s), 2))
def is_hex64(s): return len(s) == 64 and all(c in "0123456789abcdefABCDEF" for c in s)

# --- bring-up -----------------------------------------------------------------
i2c = busio.I2C(PINS["SCL"], PINS["SDA"], frequency=100000)
try:
    atecc = ATECC(i2c)
    serial = atecc.serial_number          # Adafruit lib already returns an uppercase hex string
except Exception as e:           # noqa: BLE001
    print("INIT_FAIL", repr(e)); error_blink()
    raise SystemExit

# boot self-test: prove the part actually signs before we trust the button loop
try:
    sig = bytes(atecc.ecdsa_sign(SLOT, bytearray(os.urandom(32))))
    selftest = "PASS" if len(sig) == 64 else "FAIL"
except Exception as e:           # noqa: BLE001
    print("BOOT serial=%s selftest=FAIL err=%r" % (serial, e)); error_blink()
    raise SystemExit

print("BOOT serial=%s selftest=%s" % (serial, selftest))
if selftest != "PASS":
    error_blink(); raise SystemExit
ready.value = True               # chip alive + signs

# --- main loop ----------------------------------------------------------------
_buf = ""
def poll_line():
    global _buf
    while supervisor.runtime.serial_bytes_available:
        c = sys.stdin.read(1)
        if c in ("\n", "\r"):
            line, _buf = _buf, ""
            return line.strip()
        _buf += c
    return None

pending = None        # optional externally-supplied challenge (32 bytes)
prev = True
armed.value = True
while True:
    line = poll_line()
    if line and is_hex64(line):
        pending = unhex(line)     # next press signs this challenge

    cur = btn.value
    if prev and not cur:          # falling edge = press
        time.sleep(0.02)          # debounce
        if not btn.value:
            armed.value = False; busy.value = True
            challenge = pending if pending else os.urandom(32)
            pending = None
            try:
                sig = bytes(atecc.ecdsa_sign(SLOT, bytearray(challenge)))
                busy.value = False
                print("SIG %s %s %s" % (serial, hexs(challenge), hexs(sig)))
                pulse(done)
            except Exception as e:    # noqa: BLE001
                busy.value = False
                print("SIGN_FAIL", repr(e)); error_blink()
            armed.value = True
            while not btn.value:      # wait for release
                time.sleep(0.01)
    prev = cur
    time.sleep(0.005)
