"""
ATECC608B driver for MicroPython (Raspberry Pi Pico)
Handles I2C wake/sleep, key slot configuration, and ECDSA P256 signing.

ZKnot Witness — secure element interface layer
Provisional Patent Application No. 63/961,098
"""

import time
from machine import I2C


# ─── ATECC608B constants ───────────────────────────────────────────────────────
ATECC_ADDR        = 0x60   # default I2C address (SSHDA variant = 0x60)
WORD_ADDR_COMMAND = 0x03
WORD_ADDR_RESET   = 0x00

# Opcodes
OP_INFO      = 0x30
OP_RANDOM    = 0x1B
OP_GENKEY    = 0x40
OP_SIGN      = 0x41
OP_VERIFY    = 0x45
OP_LOCK      = 0x17
OP_READ      = 0x02
OP_WRITE     = 0x12
OP_NONCE     = 0x16
OP_SHA       = 0x47

# Key slot to use for ZKnot signing key (slot 0 is standard for P256 private key)
SIGNING_KEY_SLOT = 0

# Timing constants (microseconds) from datasheet
WAKE_DELAY_US  = 1500   # SDA low pulse duration for wake
WAKE_RESP_US   = 2500   # time after wake before first command
EXEC_GENKEY_MS = 115    # GenKey execution time
EXEC_SIGN_MS   = 70     # Sign execution time
EXEC_RANDOM_MS = 23     # Random execution time
EXEC_INFO_MS   = 1      # Info execution time


def _crc16(data: bytes) -> bytes:
    """CRC-16 as specified by ATECC608B datasheet (polynomial 0x8005)."""
    crc = 0x0000
    for byte in data:
        for _ in range(8):
            if (crc ^ (byte << 8)) & 0x8000:
                crc = (crc << 1) ^ 0x8005
            else:
                crc = crc << 1
            byte <<= 1
            crc &= 0xFFFF
    return bytes([crc & 0xFF, (crc >> 8) & 0xFF])


class ATECC608BError(Exception):
    pass


class ATECC608B:
    """
    Driver for the Microchip ATECC608B cryptographic co-processor.
    
    Wiring (I2C):
        SDA → Pico GP4 (or any SDA pin)
        SCL → Pico GP5 (or any SCL pin)
        VCC → 3.3V
        GND → GND
        
    The ATECC608B-SSHDA-T has address 0x60 by default.
    """

    def __init__(self, i2c: I2C, address: int = ATECC_ADDR):
        self.i2c = i2c
        self.addr = address
        self._buf = bytearray(128)

    # ─── Wake / Sleep ──────────────────────────────────────────────────────────

    def wake(self) -> bool:
        """
        Wake the ATECC608B from sleep/idle.
        Send a 0x00 byte at a low I2C frequency to create the SDA wake pulse,
        then read the 4-byte wake response.
        """
        # Toggle SDA low by writing to address 0x00 at slow speed
        # On MicroPython we approximate by doing a zero-byte write
        try:
            self.i2c.writeto(0x00, b'\x00')
        except OSError:
            pass  # expected — no ACK at address 0x00
        time.sleep_us(WAKE_RESP_US)

        # Read wake response (should be 0x04 0x11 0x33 0x43)
        try:
            resp = self.i2c.readfrom(self.addr, 4)
        except OSError:
            raise ATECC608BError("No wake response — check wiring and address")

        if resp[1] != 0x11:
            raise ATECC608BError(f"Unexpected wake response: {resp.hex()}")
        return True

    def sleep(self):
        """Put the ATECC608B back to sleep."""
        try:
            self.i2c.writeto(self.addr, bytes([WORD_ADDR_RESET]))
        except OSError:
            pass

    def idle(self):
        """Put the ATECC608B into idle mode (faster to wake than sleep)."""
        try:
            self.i2c.writeto(self.addr, b'\x02')
        except OSError:
            pass

    # ─── Command layer ─────────────────────────────────────────────────────────

    def _send_command(self, opcode: int, param1: int, param2: int,
                      data: bytes = b'') -> None:
        """Build and transmit a command packet."""
        # Packet: word_addr | count | opcode | param1 | param2_lo | param2_hi | data | crc
        count = 1 + 1 + 1 + 2 + len(data) + 2  # count byte itself + opcode + params + data + crc
        packet = bytes([count, opcode, param1, param2 & 0xFF, (param2 >> 8) & 0xFF]) + data
        crc = _crc16(packet)
        full = bytes([WORD_ADDR_COMMAND]) + packet + crc
        self.i2c.writeto(self.addr, full)

    def _read_response(self, length: int, delay_ms: int) -> bytes:
        """Wait for command execution then read response."""
        time.sleep_ms(delay_ms)
        resp = self.i2c.readfrom(self.addr, length + 3)  # count + data + crc
        count = resp[0]
        if count < 4:
            raise ATECC608BError(f"Short response: {resp.hex()}")
        payload = resp[1:count - 2]
        expected_crc = _crc16(resp[:count - 2])
        actual_crc = resp[count - 2:count]
        if expected_crc != actual_crc:
            raise ATECC608BError("CRC mismatch in response")
        if len(payload) == 1 and payload[0] != 0x00:
            raise ATECC608BError(f"Command error code: 0x{payload[0]:02X}")
        return payload

    # ─── Public API ────────────────────────────────────────────────────────────

    def info(self) -> bytes:
        """Return 4-byte device info (revision number)."""
        self.wake()
        self._send_command(OP_INFO, 0x00, 0x00)
        result = self._read_response(4, EXEC_INFO_MS)
        self.idle()
        return result

    def random(self) -> bytes:
        """Return 32 bytes of hardware-generated random data."""
        self.wake()
        self._send_command(OP_RANDOM, 0x00, 0x00)
        result = self._read_response(32, EXEC_RANDOM_MS)
        self.idle()
        return result

    def gen_key(self, slot: int = SIGNING_KEY_SLOT) -> bytes:
        """
        Generate a new P256 ECC key pair in the specified slot.
        Returns the 64-byte uncompressed public key (X || Y).
        
        WARNING: This overwrites any existing key in the slot.
        Only call this during initial provisioning.
        """
        self.wake()
        # param1=0x04 = generate new key; param2 = slot number
        self._send_command(OP_GENKEY, 0x04, slot)
        result = self._read_response(64, EXEC_GENKEY_MS)
        self.idle()
        return result

    def get_public_key(self, slot: int = SIGNING_KEY_SLOT) -> bytes:
        """
        Read the public key from a slot without modifying the private key.
        Returns 64-byte uncompressed public key (X || Y).
        """
        self.wake()
        # param1=0x00 = read public key only
        self._send_command(OP_GENKEY, 0x00, slot)
        result = self._read_response(64, EXEC_GENKEY_MS)
        self.idle()
        return result

    def sign(self, digest: bytes, slot: int = SIGNING_KEY_SLOT) -> bytes:
        """
        Sign a 32-byte digest using the P256 private key in the specified slot.
        
        The digest must already be a SHA-256 hash — the ATECC608B signs
        the raw 32 bytes directly using ECDSA P256.
        
        Returns 64-byte signature (R || S).
        
        The private key never leaves the secure element.
        """
        if len(digest) != 32:
            raise ATECC608BError(f"Digest must be 32 bytes, got {len(digest)}")

        # First load the digest into the TempKey register via Nonce command
        self.wake()
        # Nonce with mode=0x03 loads external digest directly into TempKey
        self._send_command(OP_NONCE, 0x03, 0x00, digest)
        self._read_response(1, 7)  # expect 0x00 success

        # Now sign TempKey with the private key in the slot
        # param1=0x80 = sign using internal key (not external); param2 = slot
        self._send_command(OP_SIGN, 0x80, slot)
        result = self._read_response(64, EXEC_SIGN_MS)
        self.idle()
        return result

    def serial_number(self) -> bytes:
        """Return the 9-byte unique serial number of this device."""
        self.wake()
        # Config zone, word 0, 4 bytes starting at byte 0 (serial bytes 0-3)
        self._send_command(OP_READ, 0x80, 0x0000)
        part1 = self._read_response(4, 2)
        self._send_command(OP_READ, 0x80, 0x0002)
        part2 = self._read_response(4, 2)
        self._send_command(OP_READ, 0x80, 0x0003)
        part3 = self._read_response(4, 2)
        self.idle()
        # Serial = bytes 0,1,2,3,4 from part1+part2, bytes 8 from part3
        return part1[:4] + part2[:4] + part3[:1]
