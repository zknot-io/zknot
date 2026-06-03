"""
GM65 QR/Barcode Scanner Module — UART Driver for MicroPython
Raspberry Pi Pico

Wiring:
    GM65 VCC  → 3.3V (module is 3.3V-5V tolerant, 3.3V is fine)
    GM65 GND  → GND
    GM65 TX   → Pico GP1  (UART0 RX)
    GM65 RX   → Pico GP0  (UART0 TX)
    GM65 TRIG → Pico GP2  (optional: pull LOW to trigger scan)
                           (if not used, scanner runs in continuous mode)

Default baud rate: 9600
Default mode: continuous scanning (scans until it reads something)

The GM65 outputs the decoded data as ASCII terminated with CR+LF (\r\n).
For a QR code containing "HELLO", it outputs: b'HELLO\r\n'

For ZKnot, the challenge QR contains a JSON payload like:
    {"mode":"nonce","v":"a3f1...64hex","ts":1234567890}
or
    {"mode":"hash","v":"b4e2...64hex","ts":1234567890}
"""

import time
from machine import UART, Pin


class GM65Error(Exception):
    pass


class GM65Scanner:
    """
    Driver for GM65 barcode/QR scanner module.
    
    The GM65 operates in two modes:
    1. Continuous: scans automatically, outputs when it reads something
    2. Triggered: only scans when TRIG pin is pulled LOW
    
    We use triggered mode to save battery — scanner is off until
    the Pico tells it to scan.
    """

    def __init__(
        self,
        uart_id: int = 0,
        tx_pin: int = 0,
        rx_pin: int = 1,
        trig_pin: int = 2,
        baud: int = 9600,
    ):
        self.uart = UART(
            uart_id,
            baudrate=baud,
            tx=Pin(tx_pin),
            rx=Pin(rx_pin),
            bits=8,
            parity=None,
            stop=1,
            timeout=100,
        )
        # TRIG pin: pull HIGH = idle, pull LOW = trigger scan
        self.trig = Pin(trig_pin, Pin.OUT, value=1)
        self._buf = b''

    def trigger_scan(self):
        """Pulse the TRIG pin to start one scan cycle."""
        self.trig.value(0)
        time.sleep_ms(10)
        self.trig.value(1)

    def read_result(self, timeout_ms: int = 3000) -> str | None:
        """
        Wait for the scanner to output a decoded result.
        Returns the decoded string, or None if timeout.
        
        The GM65 outputs ASCII + CR + LF.
        """
        deadline = time.ticks_add(time.ticks_ms(), timeout_ms)
        buf = b''

        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            chunk = self.uart.read(64)
            if chunk:
                buf += chunk
                if b'\r\n' in buf or b'\n' in buf:
                    # Extract complete line
                    line = buf.split(b'\n')[0].replace(b'\r', b'')
                    return line.decode('utf-8', errors='replace').strip()
            time.sleep_ms(20)

        return None

    def scan_once(self, timeout_ms: int = 4000) -> str | None:
        """
        Trigger one scan and return the result.
        Returns decoded string or None on timeout.
        """
        # Flush any stale data
        self.uart.read()
        self.trigger_scan()
        return self.read_result(timeout_ms)

    def scan_blocking(
        self,
        timeout_ms: int = 30000,
        on_waiting: callable = None,
    ) -> str | None:
        """
        Keep scanning until a valid result is obtained or timeout.
        Calls on_waiting() periodically so the UI can update.
        
        Returns decoded string or None on timeout.
        """
        deadline = time.ticks_add(time.ticks_ms(), timeout_ms)
        buf = b''

        # Clear buffer
        self.uart.read()

        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            # Trigger scan pulse
            self.trig.value(0)
            time.sleep_ms(5)
            self.trig.value(1)

            # Read for up to 500ms
            scan_deadline = time.ticks_add(time.ticks_ms(), 500)
            while time.ticks_diff(scan_deadline, time.ticks_ms()) > 0:
                chunk = self.uart.read(64)
                if chunk:
                    buf += chunk
                    if b'\n' in buf:
                        line = buf.split(b'\n')[0].replace(b'\r', b'')
                        decoded = line.decode('utf-8', errors='replace').strip()
                        if decoded:
                            return decoded
                        buf = b''
                time.sleep_ms(20)

            if on_waiting:
                on_waiting()

        return None


def parse_challenge(raw: str) -> tuple[str, str] | None:
    """
    Parse a ZKnot challenge QR payload.
    
    Expected formats:
        {"mode":"nonce","v":"<64hex>","ts":<int>}
        {"mode":"hash","v":"<64hex>","ts":<int>}
    
    Returns (mode, value_hex) or None if invalid.
    
    We do a minimal parse without json module to save memory.
    """
    raw = raw.strip()

    # Extract mode
    mode = None
    if '"mode":"nonce"' in raw or "'mode':'nonce'" in raw:
        mode = "nonce"
    elif '"mode":"hash"' in raw or "'mode':'hash'" in raw:
        mode = "hash"
    else:
        return None

    # Extract value (v field) — find 64-char hex string
    v_start = raw.find('"v":"')
    if v_start == -1:
        v_start = raw.find("'v':'")
    if v_start == -1:
        return None

    v_start += 5  # skip '"v":"'
    v_end = raw.find('"', v_start)
    if v_end == -1:
        v_end = raw.find("'", v_start)
    if v_end == -1:
        return None

    value = raw[v_start:v_end]

    # Validate: must be exactly 64 hex chars
    if len(value) != 64:
        return None
    try:
        int(value, 16)
    except ValueError:
        return None

    return (mode, value)
