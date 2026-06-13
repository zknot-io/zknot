#!/usr/bin/env python3
"""
verify_unit.py  --  ZKNOT Attestor functional-test verifier (host side)
=======================================================================
Reads SIG lines from a running Attestor (Pico over USB serial) and verifies
each signature against the slot-0 public key recorded for that serial in the
provisioning ledger. This is the bench stand-in for verifyknot.io/start.

Pass = the physical unit produced a signature that verifies against its
enrolled identity. That is the test that actually means something.

Usage:
    source ~/ZKNOT/P-Attestor/.venv/bin/activate     # needs pyserial + cryptography
    pip install pyserial                              # if not already present
    python3 verify_unit.py                            # auto-detects /dev/ttyACM*
    python3 verify_unit.py /dev/ttyACM0               # or name the port

Send a challenge (optional, presence-gated): type 64 hex chars + Enter is done
on the device side via verifyknot.io/start; for a bench smoke test just press
the button and the device self-generates a random challenge.
"""
import sys, glob, os

LEDGER = os.path.expanduser("~/ZKNOT/P-ZKKEY/atecc-provisioning-ledger.psv")


def pubkey_for(serial):
    serial = serial.lower()
    with open(LEDGER) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5 and parts[1].lower() == serial:
                return parts[4]
    return None


def verify(pub_hex, challenge_hex, sig_hex):
    from cryptography.hazmat.primitives.asymmetric import ec, utils
    from cryptography.hazmat.primitives import hashes
    from cryptography.exceptions import InvalidSignature
    pub_xy = bytes.fromhex(pub_hex)
    pub = ec.EllipticCurvePublicNumbers(
        int.from_bytes(pub_xy[:32], "big"),
        int.from_bytes(pub_xy[32:], "big"), ec.SECP256R1()).public_key()
    sig = bytes.fromhex(sig_hex)
    der = utils.encode_dss_signature(int.from_bytes(sig[:32], "big"),
                                     int.from_bytes(sig[32:], "big"))
    try:
        pub.verify(der, bytes.fromhex(challenge_hex),
                   ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        return True
    except InvalidSignature:
        return False


def main():
    import serial   # pyserial
    port = sys.argv[1] if len(sys.argv) > 1 else None
    if not port:
        cands = sorted(glob.glob("/dev/ttyACM*") + glob.glob("/dev/ttyUSB*"))
        if not cands:
            sys.exit("[FATAL] no /dev/ttyACM* found. Plug in the Pico, or pass the port.")
        port = cands[0]
    print(f"listening on {port} (Ctrl-C to stop). Press the device button to test.")
    ser = serial.Serial(port, 115200, timeout=1)
    while True:
        raw = ser.readline().decode("utf-8", "replace").strip()
        if not raw:
            continue
        if raw.startswith("BOOT"):
            print(f"[boot] {raw}")
        elif raw.startswith("SIG "):
            try:
                _, serial_hex, challenge_hex, sig_hex = raw.split()
            except ValueError:
                print(f"[skip] malformed: {raw}"); continue
            pub = pubkey_for(serial_hex)
            if pub is None:
                print(f"[FAIL] serial {serial_hex} not in ledger — unenrolled unit."); continue
            ok = verify(pub, challenge_hex, sig_hex)
            print(f"[{'PASS' if ok else 'FAIL'}] {serial_hex}  challenge={challenge_hex[:12]}…")
        else:
            print(f"[dev] {raw}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nstopped.")
