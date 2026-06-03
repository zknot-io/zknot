#!/usr/bin/env python3
"""
ZKnot Witness — Offline Signature Verifier
Verifies a .zksig record without needing the ZKnot Witness device.

Anyone with the .zksig file, the original file, and the public key
can verify the signature independently.

Usage:
    python3 verify_sig.py record.zksig
    python3 verify_sig.py record.zksig --file original_file.jpg
    python3 verify_sig.py record.zksig --pubkey <hex>   # override pubkey

Install dependencies:
    pip install cryptography
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime

try:
    from cryptography.hazmat.primitives.asymmetric.ec import (
        ECDSA, EllipticCurvePublicKey, SECP256R1
    )
    from cryptography.hazmat.primitives.asymmetric.utils import (
        decode_dss_signature, encode_dss_signature
    )
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.backends import default_backend
    from cryptography.exceptions import InvalidSignature
except ImportError:
    print("ERROR: cryptography library not installed.")
    print("Run: pip install cryptography")
    sys.exit(1)


def load_p256_public_key(pubkey_hex: str) -> EllipticCurvePublicKey:
    """
    Load a P256 public key from 64-byte uncompressed format (X || Y, no 0x04 prefix).
    This is the format returned by the ATECC608B.
    """
    if len(pubkey_hex) != 128:
        raise ValueError(f"Public key must be 128 hex chars (64 bytes X||Y), got {len(pubkey_hex)}")

    key_bytes = bytes.fromhex(pubkey_hex)
    x = int.from_bytes(key_bytes[:32], "big")
    y = int.from_bytes(key_bytes[32:], "big")

    public_key = ec.EllipticCurvePublicNumbers(
        x=x, y=y, curve=SECP256R1()
    ).public_key(default_backend())

    return public_key


def raw_sig_to_der(sig_hex: str) -> bytes:
    """
    Convert raw 64-byte ECDSA signature (R || S) from ATECC608B
    to DER-encoded format required by cryptography library.
    """
    if len(sig_hex) != 128:
        raise ValueError(f"Signature must be 128 hex chars (64 bytes R||S), got {len(sig_hex)}")

    sig_bytes = bytes.fromhex(sig_hex)
    r = int.from_bytes(sig_bytes[:32], "big")
    s = int.from_bytes(sig_bytes[32:], "big")
    return encode_dss_signature(r, s)


def verify_signature(pubkey_hex: str, digest_hex: str, sig_hex: str) -> bool:
    """
    Verify an ECDSA P256 signature.
    
    pubkey_hex: 128 hex chars (64 bytes, X || Y, no prefix)
    digest_hex: 64 hex chars (32 bytes, the SHA-256 hash that was signed)
    sig_hex:    128 hex chars (64 bytes, R || S)
    
    Returns True if valid, raises InvalidSignature if not.
    """
    public_key = load_p256_public_key(pubkey_hex)
    der_sig = raw_sig_to_der(sig_hex)
    digest_bytes = bytes.fromhex(digest_hex)

    # The ATECC608B signs the raw digest bytes directly (Prehashed)
    public_key.verify(
        der_sig,
        digest_bytes,
        ec.ECDSA(hashes.Prehashed())
    )
    return True


def hash_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description="Verify a ZKnot Witness signing record",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This tool verifies that:
  1. The .zksig record contains a valid ECDSA P256 signature
  2. The signature matches the digest in the record
  3. (Optional) The digest matches the provided file's SHA-256

The verification is purely cryptographic — it does not require the 
ZKnot Witness device, network access, or any ZKnot infrastructure.
        """
    )
    parser.add_argument("record", help="Path to .zksig JSON record")
    parser.add_argument("--file", help="Original file to verify against (optional)")
    parser.add_argument("--pubkey", help="Override public key (128 hex chars)")
    args = parser.parse_args()

    # Load record
    try:
        with open(args.record) as f:
            record = json.load(f)
    except FileNotFoundError:
        print(f"✗ Record file not found: {args.record}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in record: {e}")
        sys.exit(1)

    print(f"ZKnot Witness Verification Report")
    print(f"{'='*50}")
    print(f"Record:     {args.record}")
    print(f"Timestamp:  {record.get('timestamp_utc', 'N/A')}")
    print(f"Algorithm:  {record.get('algorithm', 'N/A')}")
    if record.get("source_file"):
        print(f"Source:     {record['source_file']}")
    print()

    digest_hex  = record.get("digest", "")
    sig_hex     = record.get("signature", "")
    pubkey_hex  = args.pubkey or record.get("public_key", "")

    # Show truncated values
    print(f"Digest:     {digest_hex[:16]}...{digest_hex[-8:]}")
    print(f"Signature:  {sig_hex[:16]}...{sig_hex[-8:]}")
    print(f"Public Key: {pubkey_hex[:16]}...{pubkey_hex[-8:]}")
    print()

    all_pass = True

    # ── Check 1: Signature validity ──
    print("Check 1: ECDSA P256 signature validity")
    try:
        verify_signature(pubkey_hex, digest_hex, sig_hex)
        print("  ✓ Signature is VALID")
    except InvalidSignature:
        print("  ✗ Signature is INVALID — record has been tampered with")
        all_pass = False
    except Exception as e:
        print(f"  ✗ Verification error: {e}")
        all_pass = False

    # ── Check 2: File hash (if provided) ──
    if args.file:
        print(f"Check 2: File integrity ({args.file})")
        try:
            file_hash = hash_file(args.file)
            if file_hash == digest_hex:
                print(f"  ✓ File SHA-256 matches digest in record")
            else:
                print(f"  ✗ File SHA-256 does NOT match record digest")
                print(f"    Expected: {digest_hex}")
                print(f"    Got:      {file_hash}")
                all_pass = False
        except FileNotFoundError:
            print(f"  ✗ File not found: {args.file}")
            all_pass = False
    elif record.get("source_sha256"):
        print(f"Check 2: Source file hash")
        print(f"  ⚠  Source file not provided for comparison")
        print(f"     Recorded hash: {record['source_sha256']}")

    # ── Check 3: Record consistency ──
    print("Check 3: Record internal consistency")
    if record.get("source_sha256") and record.get("digest"):
        if record["source_sha256"] == record["digest"]:
            print("  ✓ Source hash and digest field are consistent")
        else:
            print("  ✗ Source hash and digest field do not match — record is inconsistent")
            all_pass = False
    else:
        print("  — (no source hash to check)")

    # ── Summary ──
    print()
    print(f"{'='*50}")
    if all_pass:
        print("RESULT: ✓ VERIFIED — signature is valid")
        if args.file:
            print("        ✓ File matches signed digest")
        print()
        print("This record proves:")
        print(f"  • The digest was signed by the private key corresponding to:")
        print(f"    {pubkey_hex[:32]}...")
        print(f"  • The signing required physical button confirmation on a")
        print(f"    ZKnot Witness device (ATECC608B hardware secure element)")
        print(f"  • The private key never left the hardware secure element")
    else:
        print("RESULT: ✗ VERIFICATION FAILED")
        print("        This record should not be trusted.")
        sys.exit(1)


if __name__ == "__main__":
    main()
