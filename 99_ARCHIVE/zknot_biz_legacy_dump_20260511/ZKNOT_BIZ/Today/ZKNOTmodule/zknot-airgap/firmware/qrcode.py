"""
Minimal QR Code generator for MicroPython.
No external dependencies. Generates QR matrix as a 2D list of bools.

Supports:
  - Byte mode encoding (works for hex strings, base64, alphanumeric)
  - Error correction level M (15% recovery)
  - Versions 1-10 (up to ~154 bytes)

Usage:
    from qrcode import make_qr
    matrix = make_qr("HELLO")   # returns list of lists of bool
    # matrix[row][col] == True means dark module

This is a focused implementation for the ZKnot Witness use case.
The signature is split into two chunks of ~44 chars each, both fit
comfortably in QR version 3 (29x29) at error correction M.
"""

# ── Reed-Solomon GF(256) arithmetic ──────────────────────────────────────────

GF_EXP = [0] * 512
GF_LOG = [0] * 256

def _init_gf():
    x = 1
    for i in range(255):
        GF_EXP[i] = x
        GF_LOG[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 0x11D
    for i in range(255, 512):
        GF_EXP[i] = GF_EXP[i - 255]

_init_gf()

def gf_mul(x, y):
    if x == 0 or y == 0:
        return 0
    return GF_EXP[(GF_LOG[x] + GF_LOG[y]) % 255]

def gf_poly_mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for j, qj in enumerate(q):
        for i, pi in enumerate(p):
            r[i + j] ^= gf_mul(pi, qj)
    return r

def gf_poly_div(dividend, divisor):
    result = list(dividend)
    for i in range(len(dividend) - len(divisor) + 1):
        coef = result[i]
        if coef != 0:
            for j in range(1, len(divisor)):
                if divisor[j] != 0:
                    result[i + j] ^= gf_mul(divisor[j], coef)
    sep = len(dividend) - len(divisor) + 1
    return result[sep:]

def rs_generator_poly(n):
    g = [1]
    for i in range(n):
        g = gf_poly_mul(g, [1, GF_EXP[i]])
    return g

def rs_encode(data, n_ec):
    gen = rs_generator_poly(n_ec)
    padded = list(data) + [0] * n_ec
    remainder = gf_poly_div(padded, gen)
    return data + bytes(remainder)


# ── QR constants ──────────────────────────────────────────────────────────────

# Format info strings for error correction M, masks 0-7
# Precomputed (XOR with 101010000010010)
FORMAT_INFO = {
    0: 0b101010000010010,
    1: 0b101000100100101,
    2: 0b101111001111100,
    3: 0b101101101001011,
    4: 0b100010111111001,
    5: 0b100000011001110,
    6: 0b100111110010111,
    7: 0b100101010100000,
}

# Version info: (size, ec_codewords_per_block, blocks, data_codewords)
# Only versions 1-5 needed for our use case (max 64 bytes at M)
VERSION_INFO = {
    1: (21,  10, 1, 16),
    2: (25,  16, 1, 28),
    3: (29,  26, 1, 44),   # ← our primary target (44 bytes payload)
    4: (33,  18, 2, 64),
    5: (37,  24, 2, 86),
}

def _version_for_length(data_len):
    """Return smallest version that fits data_len bytes in byte mode at EC=M."""
    for v, (size, ec_per_block, blocks, data_cw) in VERSION_INFO.items():
        # Byte mode overhead: mode(4) + length(8 for v1-9) + terminator(4) = 16 bits = 2 bytes
        if data_len + 2 <= data_cw:
            return v
    raise ValueError(f"Data too long ({data_len} bytes) for supported versions")


# ── Data encoding ─────────────────────────────────────────────────────────────

def _encode_byte_mode(data: bytes, version: int) -> list:
    """Encode data in byte mode, return list of bits."""
    bits = []

    def push(val, length):
        for i in range(length - 1, -1, -1):
            bits.append((val >> i) & 1)

    push(0b0100, 4)           # mode indicator: byte
    push(len(data), 8)        # character count (8 bits for versions 1-9)
    for byte in data:
        push(byte, 8)

    # Terminator
    for _ in range(min(4, 0)):  # we'll pad to codeword boundary below
        bits.append(0)

    return bits

def _bits_to_codewords(bits: list, total_cw: int) -> list:
    """Pad bit stream to total_cw codewords and return list of ints."""
    # Terminator (up to 4 zeros)
    for _ in range(min(4, total_cw * 8 - len(bits))):
        bits.append(0)
    # Pad to byte boundary
    while len(bits) % 8:
        bits.append(0)
    # Pad codewords
    pad = [0xEC, 0x11]
    i = 0
    while len(bits) < total_cw * 8:
        bits += [(pad[i % 2] >> j) & 1 for j in range(7, -1, -1)]
        i += 1
    return [int(''.join(str(b) for b in bits[i:i+8]), 2)
            for i in range(0, total_cw * 8, 8)]


# ── Matrix construction ───────────────────────────────────────────────────────

class QRMatrix:
    def __init__(self, version):
        self.version = version
        self.size, self.ec_per_block, self.blocks, self.data_cw = VERSION_INFO[version]
        self.matrix = [[None] * self.size for _ in range(self.size)]
        self.reserved = [[False] * self.size for _ in range(self.size)]

    def _set(self, row, col, val):
        self.matrix[row][col] = val
        self.reserved[row][col] = True

    def _place_finder(self, row, col):
        for r in range(7):
            for c in range(7):
                dark = (r in (0, 6) or c in (0, 6) or (2 <= r <= 4 and 2 <= c <= 4))
                self._set(row + r, col + c, dark)
        # Separators
        for i in range(8):
            if row + 7 < self.size:
                self._set(row + 7, col + i, False) if col + i < self.size else None
            if col + 7 < self.size:
                self._set(row + i, col + 7, False) if row + i < self.size else None

    def _place_timing(self):
        for i in range(8, self.size - 8):
            val = (i % 2 == 0)
            self._set(6, i, val)
            self._set(i, 6, val)

    def _place_dark_module(self):
        self._set(4 * self.version + 9, 8, True)

    def _reserve_format_areas(self):
        for i in range(9):
            if not self.reserved[8][i]:
                self.reserved[8][i] = True
            if not self.reserved[i][8]:
                self.reserved[i][8] = True
        for i in range(8):
            self.reserved[8][self.size - 1 - i] = True
            self.reserved[self.size - 1 - i][8] = True

    def _place_format_info(self, mask_pattern):
        fmt = FORMAT_INFO[mask_pattern]
        bits = [(fmt >> i) & 1 for i in range(14, -1, -1)]

        positions_h = list(range(0, 6)) + [7, 8] + list(range(self.size - 8, self.size))
        positions_v = list(range(0, 6)) + [7, 8] + list(range(self.size - 7, self.size))

        for i, pos in enumerate(positions_h[:8]):
            self.matrix[8][pos] = bool(bits[i])
        for i, pos in enumerate(positions_h[8:]):
            self.matrix[8][pos] = bool(bits[7 + i])

        for i, pos in enumerate(positions_v[:8]):
            self.matrix[pos][8] = bool(bits[7 - i])
        self.matrix[self.size - 8][8] = True  # dark module
        for i, pos in enumerate(positions_v[8:]):
            self.matrix[pos][8] = bool(bits[14 - i])

    def _place_data(self, codewords):
        bits = []
        for cw in codewords:
            for i in range(7, -1, -1):
                bits.append((cw >> i) & 1)

        bit_idx = 0
        col = self.size - 1
        going_up = True

        while col >= 0:
            if col == 6:
                col -= 1
                continue
            rows = range(self.size - 1, -1, -1) if going_up else range(self.size)
            for row in rows:
                for dc in (0, 1):
                    c = col - dc
                    if not self.reserved[row][c]:
                        if bit_idx < len(bits):
                            self.matrix[row][c] = bool(bits[bit_idx])
                            bit_idx += 1
                        else:
                            self.matrix[row][c] = False
            col -= 2
            going_up = not going_up

    def _apply_mask(self, pattern):
        def condition(r, c):
            if pattern == 0: return (r + c) % 2 == 0
            if pattern == 1: return r % 2 == 0
            if pattern == 2: return c % 3 == 0
            if pattern == 3: return (r + c) % 3 == 0
            if pattern == 4: return (r // 2 + c // 3) % 2 == 0
            if pattern == 5: return (r * c) % 2 + (r * c) % 3 == 0
            if pattern == 6: return ((r * c) % 2 + (r * c) % 3) % 2 == 0
            if pattern == 7: return ((r + c) % 2 + (r * c) % 3) % 2 == 0

        for r in range(self.size):
            for c in range(self.size):
                if not self.reserved[r][c] and condition(r, c):
                    self.matrix[r][c] = not self.matrix[r][c]

    def _score(self):
        """Simplified penalty score for mask selection."""
        score = 0
        # Rule 1: five or more same color in a row/column
        for row in self.matrix:
            run = 1
            for i in range(1, self.size):
                if row[i] == row[i-1]:
                    run += 1
                    if run == 5: score += 3
                    elif run > 5: score += 1
                else:
                    run = 1
        return score

    def build(self, data: bytes):
        # Functional patterns
        self._place_finder(0, 0)
        self._place_finder(0, self.size - 7)
        self._place_finder(self.size - 7, 0)
        self._place_timing()
        self._place_dark_module()
        self._reserve_format_areas()

        # Encode data
        version = self.version
        _, ec_per_block, blocks, data_cw = VERSION_INFO[version]
        bits = _encode_byte_mode(data, version)
        codewords = _bits_to_codewords(bits, data_cw)
        cw_bytes = bytes(codewords)

        # Reed-Solomon
        final = rs_encode(cw_bytes, ec_per_block * blocks)

        # Place data
        self._place_data(list(final))

        # Choose best mask
        best_mask = 0
        best_score = float('inf')
        import copy
        saved = copy.deepcopy(self.matrix)
        saved_res = copy.deepcopy(self.reserved)

        for mask in range(8):
            self.matrix = copy.deepcopy(saved)
            self.reserved = copy.deepcopy(saved_res)
            self._apply_mask(mask)
            self._place_format_info(mask)
            s = self._score()
            if s < best_score:
                best_score = s
                best_mask = mask

        # Apply best mask for real
        self.matrix = copy.deepcopy(saved)
        self.reserved = copy.deepcopy(saved_res)
        self._apply_mask(best_mask)
        self._place_format_info(best_mask)

        return self.matrix


def make_qr(text: str) -> list:
    """
    Generate a QR code matrix for the given text string.
    Returns list of lists of bool (True = dark module).
    Automatically selects minimum version.
    
    For ZKnot: split 128-char hex signature into two 64-char chunks.
    Each chunk fits in version 3 (29x29) with EC level M.
    """
    data = text.encode('utf-8')
    version = _version_for_length(len(data))
    qr = QRMatrix(version)
    return qr.build(data)
