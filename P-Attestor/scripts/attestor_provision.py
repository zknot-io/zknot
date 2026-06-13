#!/usr/bin/env python3
"""
attestor_provision.py  --  ZKNOT Rev2 Attestor  ATECC608 Tier-0 provisioning  (v2)
==================================================================================
Self-assertive signing provisioning over the FT260 kernel-i2c path.
Recipe: config-lock -> GenKey slot0 -> host-verify -> data-lock, one guarded CLI.

Scope: Tier-0 self-assertion. NOT a ZKKey, NOT the YubiHSM root of trust.
Boundary: device-bound / presence-style signing only. No display-then-confirm.

v2 changes:
  - AUTO-DETECTS the FT260 i2c bus (no more hardcoded /dev/i2c-6 drift).
  - `record` is FAIL-CLOSED: refuses to write a row unless BOTH zones are locked
    AND a fresh test signature verifies. No more PASS-row-with-WARN.
  - `record` writes rows in the REAL ledger schema:
      n | serial | addr | sign_slot | pubkey | cfg_lock | keygen | data_lock | testsig | notes

Usage (run each step deliberately):
    python3 attestor_provision.py read
    python3 attestor_provision.py lock-config <SERIAL>     # IRREVERSIBLE
    python3 attestor_provision.py genkey      <SERIAL>
    python3 attestor_provision.py verify      <SERIAL>
    python3 attestor_provision.py lock-data   <SERIAL>     # IRREVERSIBLE (re-verifies first)
    python3 attestor_provision.py record      <SERIAL>

Run inside the venv (no sudo needed once you're in the i2c group):
    source ~/ZKNOT/P-Attestor/.venv/bin/activate
"""

import os
import sys
import glob
import datetime

from cryptoauthlib import (
    load_cryptoauthlib, cfg_ateccx08a_i2c_default, AtcaReference,
    atcab_init, atcab_release, atcab_read_serial_number,
    atcab_is_locked,
    atcab_read_config_zone, atcab_lock_config_zone, atcab_lock_data_zone,
    atcab_genkey, atcab_get_pubkey, atcab_sign,
)

ATCA_SUCCESS = 0x00

# --- BENCH CONSTANTS --------------------------------------------------------------
I2C_BUS_OVERRIDE = None   # None = auto-detect FT260. Set an int to force a bus.
I2C_ADDR = 0xC0           # 8-bit form of 7-bit 0x60 (preconfigured parts)
LEDGER_ADDR = "0x60"      # how addr is recorded in the ledger (7-bit, matches existing rows)
EXPECT_SLOT0_SLOTCONFIG = 0x2083
EXPECT_SLOT0_KEYCONFIG  = 0x0033
LEDGER = os.path.expanduser("~/ZKNOT/P-ZKKEY/atecc-provisioning-ledger.psv")
PRODUCT_NOTE = "Rev2-Attestor"
SIGN_SLOT = 0
LOCK_ZONE_CONFIG = 0x00
LOCK_ZONE_DATA = 0x01
# ---------------------------------------------------------------------------------


def find_ft260_bus():
    """Derive the FT260's i2c bus from sysfs adapter names (drift-proof)."""
    for name_path in sorted(glob.glob("/sys/class/i2c-dev/i2c-*/name")):
        try:
            if "ft260" in open(name_path).read().strip().lower():
                base = os.path.basename(os.path.dirname(name_path))  # 'i2c-6'
                return int(base.split("-")[1])
        except (OSError, ValueError, IndexError):
            continue
    return None


def connect():
    load_cryptoauthlib()
    bus = I2C_BUS_OVERRIDE if I2C_BUS_OVERRIDE is not None else find_ft260_bus()
    if bus is None:
        sys.exit("[FATAL] no FT260 i2c adapter found.\n"
                 "  lsusb | grep -i 0403           # is the FT260 enumerated?\n"
                 "  sudo modprobe i2c-dev hid-ft260 # nodes need i2c-dev\n"
                 "  i2cdetect -l | grep -i ft260    # confirm the bus exists")
    print(f"  FT260 on /dev/i2c-{bus}")
    cfg = cfg_ateccx08a_i2c_default()
    cfg.cfg.atcai2c.bus = bus
    cfg.cfg.atcai2c.address = I2C_ADDR
    if atcab_init(cfg) != ATCA_SUCCESS:
        sys.exit("[FATAL] atcab_init failed on a found bus. Check seating, pull-ups, 3.3V.")


def seated_serial():
    sn = bytearray(9)
    if atcab_read_serial_number(sn) != ATCA_SUCCESS:
        sys.exit("[FATAL] could not read serial. A blank read = sleeping/absent part.")
    return sn.hex().upper()


def lock_state():
    c, d = AtcaReference(0), AtcaReference(0)
    atcab_is_locked(LOCK_ZONE_CONFIG, c)
    atcab_is_locked(LOCK_ZONE_DATA, d)
    return bool(c.value), bool(d.value)


def slot0_config():
    cz = bytearray(128)
    if atcab_read_config_zone(cz) != ATCA_SUCCESS:
        return None, None
    return (cz[20] | (cz[21] << 8)), (cz[96] | (cz[97] << 8))


def get_pubkey():
    pub = bytearray(64)
    if atcab_get_pubkey(SIGN_SLOT, pub) != ATCA_SUCCESS:
        sys.exit("[FATAL] get_pubkey failed (no key in slot 0 yet? run genkey first).")
    return bytes(pub)


def host_verify(pub_xy, digest, sig_rs):
    from cryptography.hazmat.primitives.asymmetric import ec, utils
    from cryptography.hazmat.primitives import hashes
    from cryptography.exceptions import InvalidSignature
    x = int.from_bytes(pub_xy[:32], "big")
    y = int.from_bytes(pub_xy[32:], "big")
    pub = ec.EllipticCurvePublicNumbers(x, y, ec.SECP256R1()).public_key()
    der = utils.encode_dss_signature(int.from_bytes(sig_rs[:32], "big"),
                                     int.from_bytes(sig_rs[32:], "big"))
    try:
        pub.verify(der, digest, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        return True
    except InvalidSignature:
        return False


def _sign_and_verify():
    digest = os.urandom(32)
    sig = bytearray(64)
    if atcab_sign(SIGN_SLOT, digest, sig) != ATCA_SUCCESS:
        sys.exit("[FATAL] sign failed.")
    pub = get_pubkey()
    return host_verify(pub, digest, bytes(sig)), pub


def guard(expect):
    seated = seated_serial()
    if seated != expect.upper():
        sys.exit(f"[ABORT] seated {seated} != expected {expect.upper()}. Wrong part. Stop.")
    print(f"  seated part confirmed: {seated}")
    typed = input("  IRREVERSIBLE. Retype the serial to proceed (anything else aborts):\n  > ").strip().upper()
    if typed != expect.upper():
        sys.exit("[ABORT] serial not retyped correctly. Nothing changed.")


def next_n(path):
    mx = 0
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            first = line.split("|", 1)[0].strip()
            if first.isdigit():
                mx = max(mx, int(first))
    return mx + 1


# ----------------------------- commands --------------------------------------

def cmd_read(_=None):
    serial = seated_serial()
    cl, dl = lock_state()
    slotcfg, keycfg = slot0_config()
    shape_ok = serial.startswith("0123") and serial.endswith("EE") and len(serial) == 18
    print("=" * 58)
    print("ATTESTOR READ (read-only, locks nothing)")
    print("=" * 58)
    print(f"  serial          : {serial}   [{'valid 0123..EE' if shape_ok else 'UNEXPECTED SHAPE'}]")
    print(f"  config zone     : {'LOCKED' if cl else 'unlocked'}")
    print(f"  data zone       : {'LOCKED' if dl else 'unlocked'}")
    if slotcfg is not None:
        print(f"  slot0 SlotConfig: 0x{slotcfg:04X}  [{'ext-sign P256 lockable' if slotcfg==EXPECT_SLOT0_SLOTCONFIG else 'UNEXPECTED'}]")
        print(f"  slot0 KeyConfig : 0x{keycfg:04X}  [{'expected' if keycfg==EXPECT_SLOT0_KEYCONFIG else 'UNEXPECTED'}]")
    print("-" * 58)
    if not cl and not dl and shape_ok:
        print(f"  GO: fresh unlocked part. Next: lock-config {serial}")
    else:
        print("  NOT a fresh unlocked part. Do not provision this one.")
    print("=" * 58)


def cmd_lock_config(expect):
    cl, dl = lock_state()
    if cl:
        sys.exit("[ABORT] config zone already locked. Skip to genkey/verify.")
    slotcfg, keycfg = slot0_config()
    if slotcfg != EXPECT_SLOT0_SLOTCONFIG or keycfg != EXPECT_SLOT0_KEYCONFIG:
        print(f"[WARN] slot0 config (0x{slotcfg:04X}/0x{keycfg:04X}) != expected "
              f"(0x{EXPECT_SLOT0_SLOTCONFIG:04X}/0x{EXPECT_SLOT0_KEYCONFIG:04X}).")
        if input("  Proceed anyway? type YES: ").strip() != "YES":
            sys.exit("[ABORT] config mismatch, stopped.")
    guard(expect)
    if atcab_lock_config_zone() != ATCA_SUCCESS:
        sys.exit("[FATAL] lock_config_zone failed.")
    cl, _ = lock_state()
    print(f"[OK] config zone now {'LOCKED' if cl else 'STILL UNLOCKED (!)'}. Next: genkey {expect}")


def cmd_genkey(expect):
    cl, dl = lock_state()
    if not cl:
        sys.exit("[ABORT] config zone not locked. Run lock-config first.")
    if dl:
        sys.exit("[ABORT] data zone already locked. Key generation is closed.")
    if seated_serial() != expect.upper():
        sys.exit("[ABORT] seated part != expected.")
    pub = bytearray(64)
    if atcab_genkey(SIGN_SLOT, pub) != ATCA_SUCCESS:
        sys.exit("[FATAL] genkey failed.")
    print(f"[OK] slot {SIGN_SLOT} keypair born on-chip (private non-extractable).")
    print(f"  pubkey (128 hex): {bytes(pub).hex()}")
    print(f"  Next: verify {expect}")


def cmd_verify(expect):
    if seated_serial() != expect.upper():
        sys.exit("[ABORT] seated part != expected.")
    ok, pub = _sign_and_verify()
    print(f"[{'PASS' if ok else 'FAIL'}] host-side verify of slot-{SIGN_SLOT} signature.")
    print(f"  pubkey: {pub.hex()}")
    if not ok:
        sys.exit("  DO NOT lock data. Investigate before sealing.")
    print(f"  Next: lock-data {expect}")


def cmd_lock_data(expect):
    cl, dl = lock_state()
    if not cl:
        sys.exit("[ABORT] config not locked. Out of order.")
    if dl:
        sys.exit("[ABORT] data zone already locked.")
    ok, _ = _sign_and_verify()           # never seal a key that doesn't verify
    if not ok:
        sys.exit("[ABORT] pre-lock verify FAILED. Not sealing a bad key.")
    print("  pre-lock verify PASS.")
    guard(expect)
    if atcab_lock_data_zone() != ATCA_SUCCESS:
        sys.exit("[FATAL] lock_data_zone failed.")
    _, dl = lock_state()
    print(f"[OK] data zone now {'LOCKED' if dl else 'STILL UNLOCKED (!)'}. "
          f"Slot-{SIGN_SLOT} key is permanent. Next: record {expect}")


def cmd_record(expect):
    seated = seated_serial()
    if seated != expect.upper():
        sys.exit("[ABORT] seated part != expected.")
    cl, dl = lock_state()
    if not (cl and dl):
        sys.exit(f"[ABORT] part not sealed (config={'LOCKED' if cl else 'unlocked'}, "
                 f"data={'LOCKED' if dl else 'unlocked'}). "
                 f"Run lock-data {expect} first. Nothing written to the ledger.")
    pub = get_pubkey().hex()
    if len(pub) != 128:
        sys.exit(f"[ABORT] pubkey is {len(pub)} chars, not 128. Never record a truncated key.")
    testsig, _ = _sign_and_verify()
    if not testsig:
        sys.exit("[ABORT] test signature FAILED at record time. Not recording. Investigate.")
    n = next_n(LEDGER)
    d = datetime.date.today().isoformat()
    # schema: n | serial | addr | sign_slot | pubkey | cfg_lock | keygen | data_lock | testsig | notes
    row = (f"{n} | {seated.lower()} | {LEDGER_ADDR} | {SIGN_SLOT} | {pub} | "
           f"{d} | {d} | {d} | PASS | {PRODUCT_NOTE}\n")
    with open(LEDGER, "a") as f:
        f.write(row)
    print(f"[OK] appended row {n} to {LEDGER}")
    print("  Integrity check (every pubkey must be 128 chars):")
    print(f"    awk -F'|' '/^[0-9]/{{gsub(/ /,\"\",$5); print $1, length($5)}}' {LEDGER}")
    print("  Then: git add + commit + push.")


def main():
    cmds = {"read": cmd_read, "lock-config": cmd_lock_config, "genkey": cmd_genkey,
            "verify": cmd_verify, "lock-data": cmd_lock_data, "record": cmd_record}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd != "read" and len(sys.argv) < 3:
        sys.exit(f"[ABORT] '{cmd}' needs the expected serial. Run `read` first.")
    connect()
    try:
        cmds[cmd](sys.argv[2] if len(sys.argv) > 2 else None)
    finally:
        atcab_release()


if __name__ == "__main__":
    main()
