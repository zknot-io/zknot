# code.py  --  ZKNOT Attestor : Seeed XIAO RP2040 signing firmware (CircuitPython)
# =============================================================================
# Press button -> ATECC608 signs a challenge with slot-0 -> signature out over USB.
# 4 LEDs show state: READY / ARMED / BUSY / DONE.
#
# Tier-0 self-assertion. Presence-actuation only (button = "sign now").
# NOT display-then-confirm. Stays on the giveaway side of the PAT-001 line.
#
# PORTED from the Pico firmware. Crypto path UNCHANGED (verifies against
# verify_unit.py). Board layer changed:
#   (1) PINS dict  -- locked from Attestor-seed-r1-netlist.net
#   (2) button pull -- external R7 pull-up + C3 debounce, so internal pull off.
# LED drive is active-high (cathode->GND), unchanged.
#
# Pin map (Attestor-seed-r1 PCB, U1 = XIAO RP2040; from netlist):
#   /SDA   D4  board.SDA  GP6   (R1 pull-up, ATECC U3.5)
#   /SCL   D5  board.SCL  GP7   (R2 pull-up, ATECC U3.6)
#   /BTN   D0  board.D0   GP26  (R7 ext pull-up + C3 debounce)
#   /LED_G READY  D1  board.D1  GP27  (green)
#   /LED_B ARMED  D3  board.D3  GP29  (blue)
#   /LED_Y BUSY   D2  board.D2  GP28  (yellow)
#   /LED_R DONE   D6  board.D6  GP0   (red)
#
# Output over USB serial:
#   BOOT serial=<18hex> selftest=PASS|FAIL
#   SIG <serial> <challenge:64hex> <signature:128hex>   (one per button press)

import board, busio, digitalio, time, os, sys, supervisor
from adafruit_atecc.adafruit_atecc import ATECC

SLOT = 0
PINS = dict(SDA=board.SDA, SCL=board.SCL,
            READY=board.D1, ARMED=board.D3, BUSY=board.D2, DONE=board.D6,
            BTN=board.D0)

def _out(pin):
    d = digitalio.DigitalInOut(pin); d.direction = digitalio.Direction.OUTPUT
    d.value = False; return d

ready, armed, busy, done = (_out(PINS[k]) for k in ("READY", "ARMED", "BUSY", "DONE"))
btn = digitalio.DigitalInOut(PINS["BTN"]); btn.direction = digitalio.Direction.INPUT
btn.pull = None   # external pull-up (R7) on this board; pressed = LOW

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
    serial = atecc.serial_number
except Exception as e:           # noqa: BLE001
    print("INIT_FAIL", repr(e)); error_blink()
    raise SystemExit

try:
    sig = bytes(atecc.ecdsa_sign(SLOT, bytearray(os.urandom(32))))
    selftest = "PASS" if len(sig) == 64 else "FAIL"
except Exception as e:           # noqa: BLE001
    print("BOOT serial=%s selftest=FAIL err=%r" % (serial, e)); error_blink()
    raise SystemExit

print("BOOT serial=%s selftest=%s" % (serial, selftest))
if selftest != "PASS":
    error_blink(); raise SystemExit
ready.value = True

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

pending = None
prev = True
armed.value = True
while True:
    line = poll_line()
    if line and is_hex64(line):
        pending = unhex(line)

    cur = btn.value
    if prev and not cur:
        time.sleep(0.02)
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
            while not btn.value:
                time.sleep(0.01)
    prev = cur
    time.sleep(0.005)
