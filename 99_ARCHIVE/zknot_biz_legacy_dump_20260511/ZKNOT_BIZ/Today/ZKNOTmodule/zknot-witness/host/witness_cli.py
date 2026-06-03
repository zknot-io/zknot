#!/usr/bin/env python3
"""
ZKnot Witness — Host CLI
Communicates with the ZKnot Witness device over USB serial.

Usage:
    python3 witness_cli.py --port /dev/ttyACM0 ping
    python3 witness_cli.py --port /dev/ttyACM0 info
    python3 witness_cli.py --port /dev/ttyACM0 pubkey
    python3 witness_cli.py --port /dev/ttyACM0 provision
    python3 witness_cli.py --port /dev/ttyACM0 sign <file>
    python3 witness_cli.py --port /dev/ttyACM0 sign-digest <hex32>

Install dependency:
    pip install pyserial

The Pico appears as /dev/ttyACM0 (or ACM1) on Linux.
Find it with: ls /dev/ttyACM*  or  dmesg | tail -20
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import serial
except ImportError:
    print("ERROR: pyserial not installed. Run: pip install pyserial")
    sys.exit(1)


# ─── Device communication ─────────────────────────────────────────────────────

class WitnessDevice:
    def __init__(self, port: str, baud: int = 115200, timeout: float = 5.0):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self._ser = None

    def __enter__(self):
        self._ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
        time.sleep(0.5)  # let Pico reset after DTR toggle
        self._ser.reset_input_buffer()
        # Read the ready message
        ready = self._readline(timeout=8.0)
        if not ready.startswith("OK|READY"):
            raise RuntimeError(f"Device did not send READY, got: {ready!r}")
        return self

    def __exit__(self, *_):
        if self._ser:
            self._ser.close()

    def _readline(self, timeout: float = None) -> str:
        if timeout:
            self._ser.timeout = timeout
        line = self._ser.readline()
        self._ser.timeout = self.timeout
        return line.decode("utf-8", errors="replace").strip()

    def _send(self, line: str):
        self._ser.write((line + "\n").encode("utf-8"))
        self._ser.flush()

    def ping(self) -> dict:
        self._send("PING")
        resp = self._readline()
        return self._parse(resp)

    def info(self) -> dict:
        self._send("INFO")
        resp = self._readline()
        return self._parse(resp)

    def pubkey(self) -> dict:
        self._send("PUBKEY")
        resp = self._readline()
        return self._parse(resp)

    def provision(self) -> dict:
        """Generate new key pair. Waits for button press on device."""
        print("Device is waiting for button confirmation to generate key...")
        self._send("PROVISION")
        # Wait up to 35 seconds for button press
        resp = self._readline(timeout=35.0)
        return self._parse(resp)

    def sign(self, digest_hex: str) -> dict:
        """
        Sign a 32-byte digest. Waits for device to show WAITING,
        then waits for user to press the physical button.
        """
        if len(digest_hex) != 64:
            raise ValueError(f"Digest must be 64 hex chars, got {len(digest_hex)}")

        self._send(f"SIGN|{digest_hex}")

        # First response should be WAITING
        first = self._readline(timeout=5.0)
        if first == "WAITING":
            print("→ Device is showing digest on screen.")
            print("→ Press the button on the device to sign.")
            print("→ You have 30 seconds...")
            # Now wait for button press response (up to 35 seconds)
            resp = self._readline(timeout=35.0)
        elif first.startswith("ERR"):
            return self._parse(first)
        else:
            resp = first

        return self._parse(resp)

    def _parse(self, line: str) -> dict:
        """Parse 'STATUS|payload' or 'STATUS' response into a dict."""
        if not line:
            return {"status": "ERR", "error": "Empty response from device"}

        parts = line.split("|", 1)
        status = parts[0]
        payload = parts[1] if len(parts) > 1 else ""

        result = {"status": status, "raw": line}

        if status == "OK":
            # Parse key=value pairs
            if "," in payload or "=" in payload:
                for pair in payload.split(","):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        result[k.strip().lower()] = v.strip()
            else:
                result["value"] = payload
        elif status in ("CANCELLED", "WAITING"):
            result["message"] = status
        else:
            result["error"] = payload

        return result


# ─── Signing record ───────────────────────────────────────────────────────────

def build_signing_record(
    digest_hex: str,
    sig_hex: str,
    pubkey_hex: str,
    source_file: str = None,
    source_hash: str = None,
) -> dict:
    """
    Build a ZKnot Witness signing record — the on-disk artifact
    that proves a file was signed by this device at this time.
    """
    return {
        "zknot_version": "1.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "digest": digest_hex,
        "signature": sig_hex,
        "public_key": pubkey_hex,
        "algorithm": "ECDSA-P256",
        "hash_function": "SHA-256",
        "source_file": source_file,
        "source_sha256": source_hash,
        "device": "ZKnot-Witness-v1",
        "note": "Signed with physical button confirmation on ZKnot Witness device"
    }


def hash_file(path: str) -> tuple[str, str]:
    """Return (sha256_hex, digest_hex) of a file. They are the same thing."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    hex_digest = h.hexdigest()
    return hex_digest, hex_digest


# ─── CLI commands ─────────────────────────────────────────────────────────────

def cmd_ping(device, args):
    result = device.ping()
    if result["status"] == "OK":
        print("✓ Device responded: PONG")
    else:
        print(f"✗ Error: {result.get('error', 'unknown')}")
        sys.exit(1)


def cmd_info(device, args):
    result = device.info()
    if result["status"] == "OK":
        print(f"Serial:     {result.get('serial', 'N/A')}")
        pubkey = result.get("pubkey", "")
        print(f"Public Key: {pubkey[:64]}")
        if len(pubkey) > 64:
            print(f"            {pubkey[64:]}")
    else:
        print(f"✗ Error: {result.get('error', 'unknown')}")
        sys.exit(1)


def cmd_pubkey(device, args):
    result = device.pubkey()
    if result["status"] == "OK":
        pk = result.get("value", "")
        print(f"Public Key (uncompressed P256, X||Y, 64 bytes):")
        print(f"  X: {pk[:64]}")
        print(f"  Y: {pk[64:]}")
    else:
        print(f"✗ Error: {result.get('error', 'unknown')}")
        sys.exit(1)


def cmd_provision(device, args):
    print("⚠  PROVISION will generate a NEW key pair.")
    print("   This OVERWRITES the existing private key permanently.")
    confirm = input("   Type YES to continue: ").strip()
    if confirm != "YES":
        print("Cancelled.")
        return

    result = device.provision()
    if result["status"] == "OK":
        pk = result.get("pubkey", "")
        print(f"✓ New key pair generated.")
        print(f"  Public Key:")
        print(f"    X: {pk[:64]}")
        print(f"    Y: {pk[64:]}")
        print(f"\n  Save this public key — you need it to verify signatures.")
        # Save to file
        out_path = "zknot_pubkey.txt"
        with open(out_path, "w") as f:
            f.write(f"# ZKnot Witness Public Key\n")
            f.write(f"# Generated: {datetime.now(timezone.utc).isoformat()}\n")
            f.write(f"# Algorithm: ECDSA P256\n")
            f.write(f"PUBKEY={pk}\n")
        print(f"  Saved to: {out_path}")
    elif result["status"] == "CANCELLED":
        print("Cancelled — button not pressed within timeout.")
    else:
        print(f"✗ Error: {result.get('error', 'unknown')}")
        sys.exit(1)


def cmd_sign(device, args):
    """Hash a file and sign it with the ZKnot Witness device."""
    file_path = args.file
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        sys.exit(1)

    file_size = os.path.getsize(file_path)
    print(f"File:    {file_path}")
    print(f"Size:    {file_size:,} bytes")

    print("Hashing file...")
    file_hash, digest_hex = hash_file(file_path)
    print(f"SHA-256: {file_hash}")
    print()

    result = device.sign(digest_hex)

    if result["status"] == "OK":
        sig_hex = result.get("sig", "")
        pubkey_hex = result.get("pubkey", "")

        record = build_signing_record(
            digest_hex=digest_hex,
            sig_hex=sig_hex,
            pubkey_hex=pubkey_hex,
            source_file=os.path.basename(file_path),
            source_hash=file_hash,
        )

        # Save signing record
        record_path = file_path + ".zksig"
        with open(record_path, "w") as f:
            json.dump(record, f, indent=2)

        print(f"\n✓ Signed successfully.")
        print(f"  Signature: {sig_hex[:32]}...")
        print(f"  Record:    {record_path}")

    elif result["status"] == "CANCELLED":
        print("\n✗ Signing cancelled — button not pressed within timeout.")
        sys.exit(1)
    else:
        print(f"\n✗ Error: {result.get('error', 'unknown')}")
        sys.exit(1)


def cmd_sign_digest(device, args):
    """Sign a raw 32-byte digest (provided as 64 hex chars)."""
    digest_hex = args.hex_digest.strip().lower()
    if len(digest_hex) != 64:
        print(f"✗ Digest must be 64 hex chars (32 bytes), got {len(digest_hex)}")
        sys.exit(1)

    print(f"Digest: {digest_hex}")
    print()

    result = device.sign(digest_hex)

    if result["status"] == "OK":
        sig_hex = result.get("sig", "")
        pubkey_hex = result.get("pubkey", "")
        print(f"✓ Signed.")
        print(f"  Signature:  {sig_hex}")
        print(f"  Public Key: {pubkey_hex}")

        record = build_signing_record(
            digest_hex=digest_hex,
            sig_hex=sig_hex,
            pubkey_hex=pubkey_hex,
        )
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        out_path = f"zksig_{ts}.json"
        with open(out_path, "w") as f:
            json.dump(record, f, indent=2)
        print(f"  Record:     {out_path}")

    elif result["status"] == "CANCELLED":
        print("✗ Cancelled — button not pressed.")
        sys.exit(1)
    else:
        print(f"✗ Error: {result.get('error', 'unknown')}")
        sys.exit(1)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ZKnot Witness host CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 witness_cli.py --port /dev/ttyACM0 ping
  python3 witness_cli.py --port /dev/ttyACM0 info
  python3 witness_cli.py --port /dev/ttyACM0 provision
  python3 witness_cli.py --port /dev/ttyACM0 sign photo_evidence.jpg
  python3 witness_cli.py --port /dev/ttyACM0 sign-digest a3f1...64hex
        """
    )
    parser.add_argument(
        "--port", default="/dev/ttyACM0",
        help="USB serial port (default: /dev/ttyACM0)"
    )
    parser.add_argument(
        "--baud", type=int, default=115200,
        help="Baud rate (default: 115200)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ping", help="Check device is responding")
    subparsers.add_parser("info", help="Show device serial and public key")
    subparsers.add_parser("pubkey", help="Show public key only")
    subparsers.add_parser("provision", help="Generate new key pair (DESTRUCTIVE)")

    sign_p = subparsers.add_parser("sign", help="Hash a file and sign it")
    sign_p.add_argument("file", help="File to hash and sign")

    sign_d = subparsers.add_parser("sign-digest", help="Sign a raw 32-byte hex digest")
    sign_d.add_argument("hex_digest", help="64 hex chars (32 bytes)")

    args = parser.parse_args()

    try:
        with WitnessDevice(args.port, args.baud) as device:
            if args.command == "ping":
                cmd_ping(device, args)
            elif args.command == "info":
                cmd_info(device, args)
            elif args.command == "pubkey":
                cmd_pubkey(device, args)
            elif args.command == "provision":
                cmd_provision(device, args)
            elif args.command == "sign":
                cmd_sign(device, args)
            elif args.command == "sign-digest":
                cmd_sign_digest(device, args)
    except serial.SerialException as e:
        print(f"✗ Serial port error: {e}")
        print(f"  Check that the device is connected and try: ls /dev/ttyACM*")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)


if __name__ == "__main__":
    main()
