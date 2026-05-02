"""
TrustSeal ZPL Print Driver
ZKNOT, INC. — PAT-003 App# 63/961,112

Generates ZPL (Zebra Programming Language) for Zebra ZT-series thermal
transfer printers. Tested against ZT230, ZT410, ZT610.

Label spec: 50mm × 25mm, 300 DPI (12 dpmm)
Stock:      Tamper-evident VOID thermal transfer, 2" × 1" roll

Usage:
    # Print one seal by serial
    python3 trustseal_print.py --serial TS-A001-00001-T

    # Print a range
    python3 trustseal_print.py --batch A001 --from 1 --to 10

    # Generate and print for a new device provisioning event
    python3 trustseal_print.py --provision --device-id ZKC-A1B2C3D4

    # Preview to PNG (no printer required)
    python3 trustseal_print.py --serial TS-A001-00001-T --preview

    # Write ZPL to file (send manually or via lpr)
    python3 trustseal_print.py --serial TS-A001-00001-T --zpl-out label.zpl

Printer connection:
    USB:      printer appears as /dev/usb/lp0 on Linux, COM3 on Windows
    Network:  Zebra default port 9100 (raw TCP)
    Serial:   /dev/ttyUSB0 at 9600 baud

Dependencies:
    pip install zpl qrcode[pil] pillow --break-system-packages
"""

import argparse
import json
import os
import socket
import sys
from datetime import date, datetime
from pathlib import Path

import qrcode
import zpl
from PIL import Image

# ── Constants ─────────────────────────────────────────────────────────────────
LABEL_W_MM   = 50       # label width mm
LABEL_H_MM   = 25       # label height mm
DPMM         = 12       # dots per mm (300 DPI = 11.811 dpmm → use 12)
BASE_URL     = "https://verifyknot.io/seal/"
REGISTRY_DIR = Path(__file__).parent.parent  # /home/claude/TrustSeal/
CHARSET      = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

# ── Serial utilities ───────────────────────────────────────────────────────────
def check_char(serial_body: str) -> str:
    val = sum(ord(c) * (i + 1) for i, c in enumerate(serial_body))
    return CHARSET[val % len(CHARSET)]

def make_serial(batch: str, seq: int) -> str:
    body = f"TS-{batch}-{seq:05d}"
    return f"{body}-{check_char(body)}"

def validate_serial(serial: str) -> bool:
    """Returns True if check character is correct."""
    parts = serial.split("-")
    if len(parts) != 4 or parts[0] != "TS":
        return False
    body     = "-".join(parts[:3])
    expected = check_char(body)
    return parts[3] == expected

def next_serial_in_batch(batch: str) -> str:
    """Find next unused seq in batch from registry JSON."""
    reg_file = REGISTRY_DIR / f"ZKNOT_TS-{batch}_serial_registry_*.json"
    import glob
    matches = glob.glob(str(reg_file))
    if not matches:
        # No registry yet — start at 1
        return make_serial(batch, 1)
    with open(sorted(matches)[-1]) as f:
        reg = json.load(f)
    max_seq = max(s["seq"] for s in reg["seals"])
    return make_serial(batch, max_seq + 1)

# ── QR code → ZPL graphic ─────────────────────────────────────────────────────
def qr_to_zpl_graphic(url: str, size_mm: float, dpmm: int) -> tuple[str, int, int]:
    """
    Generate a QR code and convert to ZPL ^GF (Graphic Field) format.
    Returns (zpl_gf_command, width_dots, height_dots).

    ZPL ^GF format:
        ^GFa,b,c,d,data
        a = format (A=ASCII hex, B=binary, C=compressed)
        b = total bytes
        c = bytes per row
        d = dots per row (width in dots)
        data = hex-encoded bitmap rows
    """
    size_dots = int(size_mm * dpmm)

    # Generate QR
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=2,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("1")
    img = img.resize((size_dots, size_dots), Image.LANCZOS)

    # Convert PIL 1-bit image to ZPL hex bitmap
    width_dots  = img.width
    height_dots = img.height

    # ZPL bitmap: each row is ceil(width/8) bytes, MSB first
    bytes_per_row = (width_dots + 7) // 8
    total_bytes   = bytes_per_row * height_dots

    hex_rows = []
    pixels = img.load()
    for y in range(height_dots):
        row_bytes = bytearray(bytes_per_row)
        for x in range(width_dots):
            # PIL "1" mode: 0=black, 255=white
            # ZPL: bit=1 means black dot
            if pixels[x, y] == 0:  # black pixel
                byte_idx = x // 8
                bit_idx  = 7 - (x % 8)
                row_bytes[byte_idx] |= (1 << bit_idx)
        hex_rows.append(row_bytes.hex().upper())

    hex_data = "".join(hex_rows)

    zpl_gf = (
        f"^GFA,{total_bytes},{total_bytes},{bytes_per_row},"
        f"{hex_data}"
    )

    return zpl_gf, width_dots, height_dots

# ── Label builder ─────────────────────────────────────────────────────────────
def build_label_zpl(serial: str) -> str:
    """
    Build complete ZPL string for one TrustSeal label.

    Layout (50mm × 25mm, landscape):
    ┌────────────────────────────────────────────────────────┐
    │ ┌──────────┐  ZKNOT                                    │
    │ │          │  TrustSeal                                │
    │ │  QR CODE │  ────────────────                         │
    │ │  18×18mm │  TS-A001                                  │
    │ │          │  00001-T                                  │
    │ │          │  verifyknot.io                            │
    │ └──────────┘                                           │
    │              PAT. PEND. — App# 63/961,112              │
    └────────────────────────────────────────────────────────┘

    ZPL coordinate system: origin top-left, units = dots (1 dot = 1/dpmm mm)
    At 12 dpmm (300 DPI): 1mm = 12 dots
    """
    url = BASE_URL + serial

    # Parse serial for two-line display
    parts   = serial.split("-")
    line1   = f"{parts[0]}-{parts[1]}"   # TS-A001
    line2   = f"{parts[2]}-{parts[3]}"   # 00001-T

    # Dimensions in dots
    W = LABEL_W_MM * DPMM   # 600 dots
    H = LABEL_H_MM * DPMM   # 300 dots

    # QR zone: 18mm × 18mm, starts at x=2mm, centered vertically
    QR_SIZE_MM  = 18
    QR_X_MM     = 2.5
    QR_Y_MM     = (LABEL_H_MM - QR_SIZE_MM) / 2   # 3.5mm top margin

    # Text zone: starts after QR + gap
    TXT_X_MM    = QR_X_MM + QR_SIZE_MM + 2.5      # 23mm from left
    TXT_W_MM    = LABEL_W_MM - TXT_X_MM - 2       # remaining width - right margin

    # Generate QR graphic
    qr_gf, qr_w_dots, qr_h_dots = qr_to_zpl_graphic(url, QR_SIZE_MM, DPMM)

    # Convert mm to dots
    def mm(x): return int(x * DPMM)

    zpl_lines = []

    # ── ZPL header ────────────────────────────────────────────────────────────
    zpl_lines += [
        "^XA",                              # Start label
        f"^PW{mm(LABEL_W_MM)}",            # Print width in dots
        f"^LL{mm(LABEL_H_MM)}",            # Label length in dots
        "^LH0,0",                           # Label home (origin)
        "^CI28",                            # UTF-8 encoding
        "^MD10",                            # Darkness 10 (range 0-30, 10 = medium)
        "^MNY",                             # Media type: non-continuous (die-cut)
        "^MMT",                             # Print mode: tear-off
    ]

    # ── Outer border ──────────────────────────────────────────────────────────
    zpl_lines += [
        f"^FO{mm(0.5)},{mm(0.5)}",         # Field origin: 0.5mm inset
        f"^GB{mm(LABEL_W_MM-1)},{mm(LABEL_H_MM-1)},2,B,0",  # Box
        "^FS",
    ]

    # ── QR code graphic ───────────────────────────────────────────────────────
    zpl_lines += [
        f"^FO{mm(QR_X_MM)},{mm(QR_Y_MM)}",
        qr_gf,
        "^FS",
    ]

    # ── ZKNOT wordmark ────────────────────────────────────────────────────────
    # Font 0 = default scalable font. Height and width in dots.
    # Character height ~4mm = 48 dots, width ~0 = auto
    zpl_lines += [
        f"^FO{mm(TXT_X_MM)},{mm(2.5)}",
        f"^A0N,{mm(4.2)},{mm(3.2)}",       # Font 0, H=4.2mm, W=3.2mm
        "^FD ZKNOT^FS",
    ]

    # ── TrustSeal product name ────────────────────────────────────────────────
    zpl_lines += [
        f"^FO{mm(TXT_X_MM)},{mm(7.2)}",
        f"^A0N,{mm(3.0)},{mm(2.5)}",       # Slightly smaller
        "^FDTrustSeal^FS",
    ]

    # ── Separator rule ────────────────────────────────────────────────────────
    zpl_lines += [
        f"^FO{mm(TXT_X_MM)},{mm(11.2)}",
        f"^GB{mm(TXT_W_MM)},1,1,B,0",
        "^FS",
    ]

    # ── Serial line 1 (TS-A001) ───────────────────────────────────────────────
    zpl_lines += [
        f"^FO{mm(TXT_X_MM)},{mm(12.2)}",
        f"^A0N,{mm(3.0)},{mm(2.8)}",
        f"^FD{line1}^FS",
    ]

    # ── Serial line 2 (00001-T) ───────────────────────────────────────────────
    zpl_lines += [
        f"^FO{mm(TXT_X_MM)},{mm(15.8)}",
        f"^A0N,{mm(3.0)},{mm(2.8)}",
        f"^FD{line2}^FS",
    ]

    # ── verifyknot.io URL ─────────────────────────────────────────────────────
    zpl_lines += [
        f"^FO{mm(TXT_X_MM)},{mm(19.8)}",
        f"^A0N,{mm(2.2)},{mm(1.8)}",
        "^FDverifyknot.io^FS",
    ]

    # ── Patent pending — bottom, centered across full label ───────────────────
    PAT_TEXT = "PAT. PEND.  63/961,112"
    zpl_lines += [
        f"^FO{mm(2)},{mm(22.5)}",
        f"^A0N,{mm(1.6)},{mm(1.4)}",
        f"^FD{PAT_TEXT}^FS",
    ]

    # ── End label ─────────────────────────────────────────────────────────────
    zpl_lines += [
        "^XZ",   # End label
    ]

    return "\n".join(zpl_lines)


def build_provisioning_label_zpl(serial: str, device_id: str,
                                  device_type: str = "ZKKey Connect") -> str:
    """
    Variant label for device provisioning seals.
    Applied over the SWD header after firmware flash — proves device
    has not been reprogrammed since provisioning.

    Same 50×25mm format but text zone shows device ID instead of
    'TrustSeal' generic text.
    """
    url    = BASE_URL + serial
    parts  = serial.split("-")
    line1  = f"{parts[0]}-{parts[1]}"
    line2  = f"{parts[2]}-{parts[3]}"

    def mm(x): return int(x * DPMM)

    QR_SIZE_MM = 18
    QR_X_MM    = 2.5
    QR_Y_MM    = (LABEL_H_MM - QR_SIZE_MM) / 2
    TXT_X_MM   = QR_X_MM + QR_SIZE_MM + 2.5
    TXT_W_MM   = LABEL_W_MM - TXT_X_MM - 2

    qr_gf, _, _ = qr_to_zpl_graphic(url, QR_SIZE_MM, DPMM)

    zpl_lines = [
        "^XA",
        f"^PW{mm(LABEL_W_MM)}",
        f"^LL{mm(LABEL_H_MM)}",
        "^LH0,0",
        "^CI28",
        "^MD10",
        "^MNY",
        "^MMT",
        # Border
        f"^FO{mm(0.5)},{mm(0.5)}^GB{mm(LABEL_W_MM-1)},{mm(LABEL_H_MM-1)},2,B,0^FS",
        # QR
        f"^FO{mm(QR_X_MM)},{mm(QR_Y_MM)}{qr_gf}^FS",
        # ZKNOT wordmark
        f"^FO{mm(TXT_X_MM)},{mm(2.5)}^A0N,{mm(4.2)},{mm(3.2)}^FD ZKNOT^FS",
        # Device type (smaller)
        f"^FO{mm(TXT_X_MM)},{mm(7.2)}^A0N,{mm(2.5)},{mm(2.0)}^FD{device_type}^FS",
        # Device ID (mono-spaced feel — use what's available)
        f"^FO{mm(TXT_X_MM)},{mm(10.5)}^A0N,{mm(2.2)},{mm(1.9)}^FD{device_id}^FS",
        # Separator
        f"^FO{mm(TXT_X_MM)},{mm(13.5)}^GB{mm(TXT_W_MM)},1,1,B,0^FS",
        # Serial line 1
        f"^FO{mm(TXT_X_MM)},{mm(14.5)}^A0N,{mm(2.8)},{mm(2.5)}^FD{line1}^FS",
        # Serial line 2
        f"^FO{mm(TXT_X_MM)},{mm(18.0)}^A0N,{mm(2.8)},{mm(2.5)}^FD{line2}^FS",
        # PROVISIONED stamp
        f"^FO{mm(TXT_X_MM)},{mm(21.5)}^A0N,{mm(1.8)},{mm(1.5)}^FDPROVISIONED^FS",
        # Patent bottom
        f"^FO{mm(2)},{mm(22.5)}^A0N,{mm(1.6)},{mm(1.4)}^FDPAT. PEND.  63/961,112^FS",
        "^XZ",
    ]

    return "\n".join(zpl_lines)


# ── Print transport ───────────────────────────────────────────────────────────
def print_network(zpl_str: str, host: str, port: int = 9100,
                  timeout: int = 10) -> bool:
    """Send ZPL to Zebra printer over TCP (raw port 9100)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            s.sendall(zpl_str.encode("utf-8"))
        print(f"  ✓ Sent to {host}:{port}")
        return True
    except Exception as e:
        print(f"  ✗ Network print failed: {e}")
        return False

def print_usb(zpl_str: str, device: str = "/dev/usb/lp0") -> bool:
    """Send ZPL directly to USB printer device file."""
    try:
        with open(device, "wb") as f:
            f.write(zpl_str.encode("utf-8"))
        print(f"  ✓ Sent to {device}")
        return True
    except PermissionError:
        print(f"  ✗ Permission denied: {device}")
        print(f"    Fix: sudo usermod -aG lp $USER && newgrp lp")
        return False
    except FileNotFoundError:
        print(f"  ✗ Device not found: {device}")
        print(f"    Check: ls /dev/usb/lp* or ls /dev/ttyUSB*")
        return False
    except Exception as e:
        print(f"  ✗ USB print failed: {e}")
        return False

def print_serial_port(zpl_str: str, port: str = "/dev/ttyUSB0",
                      baud: int = 9600) -> bool:
    """Send ZPL over serial (RS-232) connection."""
    try:
        import serial
        with serial.Serial(port, baud, timeout=5) as ser:
            ser.write(zpl_str.encode("utf-8"))
        print(f"  ✓ Sent to {port} @ {baud}")
        return True
    except ImportError:
        print("  ✗ pyserial not installed: pip install pyserial")
        return False
    except Exception as e:
        print(f"  ✗ Serial print failed: {e}")
        return False

def save_zpl(zpl_str: str, path: str) -> None:
    """Write ZPL to file. Send with: cat label.zpl > /dev/usb/lp0"""
    with open(path, "w") as f:
        f.write(zpl_str)
    print(f"  ✓ ZPL saved to {path}")
    print(f"    Print via USB:    cat {path} > /dev/usb/lp0")
    print(f"    Print via netcat: nc PRINTER_IP 9100 < {path}")

# ── Preview renderer (no printer needed) ─────────────────────────────────────
def preview_label(serial: str, out_path: str = None) -> str:
    """
    Render label to PNG using PIL (not ZPL).
    Uses the existing PNG generator logic for visual verification.
    Output saved to out_path or auto-named.
    """
    from generate_labels import render_label   # sibling module

    url   = BASE_URL + serial
    label = render_label(serial, url)

    if out_path is None:
        out_path = f"/tmp/{serial}_preview.png"

    label.save(out_path, dpi=(300, 300))
    print(f"  ✓ Preview saved: {out_path}")
    return out_path


# ── Registry updater ──────────────────────────────────────────────────────────
def mark_printed(serial: str, batch: str) -> None:
    """Mark a seal as PRINTED in the local registry JSON."""
    import glob
    pattern  = str(REGISTRY_DIR / f"ZKNOT_TS-{batch}_serial_registry_*.json")
    matches  = glob.glob(pattern)
    if not matches:
        print(f"  ⚠ Registry not found for batch {batch} — skipping mark")
        return
    reg_path = sorted(matches)[-1]
    with open(reg_path) as f:
        reg = json.load(f)
    for seal in reg["seals"]:
        if seal["serial"] == serial:
            seal["print_status"] = "PRINTED"
            seal["printed_at"]   = datetime.utcnow().isoformat() + "Z"
            break
    with open(reg_path, "w") as f:
        json.dump(reg, f, indent=2)


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(
        description="TrustSeal ZPL Print Driver — ZKNOT, INC.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview seal 1 (no printer needed)
  python3 trustseal_print.py --serial TS-A001-00001-T --preview

  # Print single seal to network printer
  python3 trustseal_print.py --serial TS-A001-00001-T --printer-ip 192.168.1.100

  # Print single seal to USB printer
  python3 trustseal_print.py --serial TS-A001-00001-T --usb /dev/usb/lp0

  # Print range to file (inspect ZPL before sending)
  python3 trustseal_print.py --batch A001 --from 1 --to 5 --zpl-out batch.zpl

  # Print device provisioning seal
  python3 trustseal_print.py --provision --device-id ZKC-A1B2C3D4 \\
      --device-type "ZKKey Connect" --batch A001

  # Validate a serial without printing
  python3 trustseal_print.py --validate TS-A001-00047-R
        """
    )

    # What to print
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--serial",    help="Print one seal by full serial (e.g. TS-A001-00001-T)")
    group.add_argument("--provision", action="store_true",
                       help="Print a device provisioning seal variant")
    group.add_argument("--validate",  help="Validate a serial check character without printing")

    # Range printing
    ap.add_argument("--batch",   default="A001", help="Batch ID (default: A001)")
    ap.add_argument("--from",    dest="seq_from", type=int, help="Start seq for range print")
    ap.add_argument("--to",      dest="seq_to",   type=int, help="End seq for range print")

    # Provisioning
    ap.add_argument("--device-id",   help="Device serial for provisioning seal")
    ap.add_argument("--device-type", default="ZKKey Connect",
                    help="Device type label (default: 'ZKKey Connect')")

    # Output
    ap.add_argument("--printer-ip",  help="Network printer IP address")
    ap.add_argument("--printer-port",type=int, default=9100, help="Printer TCP port (default: 9100)")
    ap.add_argument("--usb",         help="USB device path (e.g. /dev/usb/lp0)")
    ap.add_argument("--serial-port", help="Serial port path (e.g. /dev/ttyUSB0)")
    ap.add_argument("--zpl-out",     help="Save ZPL to file instead of printing")
    ap.add_argument("--preview",     action="store_true", help="Render PNG preview, no printer")
    ap.add_argument("--copies",      type=int, default=1, help="Number of copies (default: 1)")
    ap.add_argument("--quiet",       action="store_true", help="Suppress output")

    args = ap.parse_args()

    # ── Validate only ──────────────────────────────────────────────────────────
    if args.validate:
        serial = args.validate.upper().strip()
        ok     = validate_serial(serial)
        if ok:
            print(f"  ✓ {serial} — valid check character")
        else:
            parts = serial.split("-")
            if len(parts) == 4:
                body     = "-".join(parts[:3])
                expected = check_char(body)
                print(f"  ✗ {serial} — check char mismatch")
                print(f"    Expected: {expected}  Got: {parts[3]}")
            else:
                print(f"  ✗ {serial} — malformed serial")
        return

    # ── Build list of serials to print ────────────────────────────────────────
    serials = []

    if args.serial:
        s = args.serial.upper().strip()
        if not validate_serial(s):
            print(f"  ✗ Invalid serial: {s}")
            sys.exit(1)
        serials.append(s)

    elif args.provision:
        if not args.device_id:
            print("  ✗ --provision requires --device-id")
            sys.exit(1)
        # Auto-assign next serial in batch
        serial = next_serial_in_batch(args.batch)
        serials.append(("provision", serial, args.device_id, args.device_type))

    elif args.seq_from and args.seq_to:
        for seq in range(args.seq_from, args.seq_to + 1):
            serials.append(make_serial(args.batch, seq))

    else:
        ap.print_help()
        return

    # ── Print each serial ──────────────────────────────────────────────────────
    for item in serials:
        is_provision = isinstance(item, tuple)

        if is_provision:
            _, serial, device_id, device_type = item
            zpl_str = build_provisioning_label_zpl(serial, device_id, device_type)
            label_type = "provisioning"
        else:
            serial  = item
            zpl_str = build_label_zpl(serial)
            label_type = "standard"

        # Multiply copies
        if args.copies > 1:
            zpl_str = zpl_str.replace("^XZ", f"^PQ{args.copies}^XZ")

        if not args.quiet:
            print(f"\n→ {serial}  [{label_type}]")
            print(f"  URL: {BASE_URL}{serial}")

        # ── Output routing ────────────────────────────────────────────────────
        if args.preview:
            try:
                preview_label(serial, f"/tmp/{serial}_preview.png")
            except ImportError:
                # generate_labels not on path — write raw ZPL instead
                out = f"/tmp/{serial}.zpl"
                save_zpl(zpl_str, out)
                print(f"  (preview requires generate_labels.py in same dir)")

        elif args.zpl_out:
            # Append all serials to one file
            mode = "a" if serials.index(item) > 0 else "w"
            with open(args.zpl_out, mode) as f:
                f.write(zpl_str + "\n")
            if not args.quiet:
                print(f"  ✓ Appended to {args.zpl_out}")

        elif args.printer_ip:
            print_network(zpl_str, args.printer_ip, args.printer_port)
            mark_printed(serial, args.batch)

        elif args.usb:
            print_usb(zpl_str, args.usb)
            mark_printed(serial, args.batch)

        elif args.serial_port:
            print_serial_port(zpl_str, args.serial_port)
            mark_printed(serial, args.batch)

        else:
            # No output specified — dump ZPL to stdout
            if not args.quiet:
                print("  (no output target — dumping ZPL to stdout)")
                print("  Use --printer-ip, --usb, --zpl-out, or --preview")
                print()
            print(zpl_str)


if __name__ == "__main__":
    main()
