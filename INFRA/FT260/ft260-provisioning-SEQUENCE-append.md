# FT260 → ATECC608 — Proven Provisioning Sequence (append to ft260-provisioning.md)

> Add this section to `~/ZKNOT/3_OPS/km/systems/ft260-provisioning.md`. It captures the
> end-to-end recipe proven and replicated on 5 parts on 2026-06-01.

## Proven provisioning sequence (Tier 0 self-assertion)

Verified working on 5 ATECC608B parts over the FT260 kernel-i2c path (`/dev/i2c-6`,
addr 8-bit 0xC0). Each step is its own script with the part's serial hardcoded as a guard.

1. **Read seated part** (read-only): confirm serial is new + both zones unlocked
   (LockConfig byte 87 = 0x55, LockValue byte 86 = 0x55).
2. **Lock config zone** — `atcab_lock_config_zone()`. IRREVERSIBLE. Freezes slot policy.
   Confirm byte 87 → 0x00.
3. **GenKey slot 0** — `atcab_genkey(0, pub)`. Device generates P256 keypair on-chip;
   private key non-extractable; returns 64-byte pubkey (X||Y). Reversible until data lock.
4. **Host-side verify** — chip signs a random 32-byte digest with `atcab_sign(0,...)`;
   verify the signature in host software (python `cryptography`, SECP256R1, Prehashed
   SHA256) against the GenKey pubkey. Must print valid=True before locking.
5. **Lock data zone** — `atcab_lock_data_zone()`. IRREVERSIBLE. Freezes slot-0 key forever.
   Confirm byte 86 → 0x00.
6. **Record** in ledger (serial, full 128-char pubkey, dates, PASS) + git commit + push.

## Why host-side verify, not chip-side
`atcab_verify_extern` runs the verify ON the chip → another FT260 bus round-trip → can
return `ATCA_COMM_FAIL` (a comm-layer glitch, NOT a bad signature). Host-side verify takes
the chip out of the verify path and is also the path a real verifier uses (they hold the
public key, not the chip). Sign succeeding + chip-verify COMM_FAIL is a bus issue, not crypto.

## Slot semantics (this TFLXTLS-family config)
- Slots 0,1,2: P256 ECC private, ExtSign enabled, Lockable (SlotConfig 0x2083/87/8f,
  KeyConfig 0x0033). Slot 0 = primary signing key by convention.
- Slots 3-15: data/SHA slots, not signing keys.
- I2C address byte (offset 16) = 0xC0 (7-bit 0x60), non-default — parts were preconfigured.

## Lock byte reference (config zone)
- Byte 87 = LockConfig: 0x55 unlocked, 0x00 locked.
- Byte 86 = LockValue (data zone): 0x55 unlocked, 0x00 locked.

## Operational hygiene proven useful
- **Serial guard** in every lock script (`EXPECT = "<serial>"`; abort if seated != EXPECT)
  — prevents locking the wrong/duplicate part.
- **Step-by-step over batch loop** for irreversible ops — human confirms each serial.
- **Ledger integrity check:** `awk -F'|' '/^[0-9]/{gsub(/ /,"",$5); print $1, length($5)}'`
  — every data row's pubkey must be 128 chars. Catches truncation/typos batch-wide.
- **Never abbreviate the pubkey** in the ledger — it's the only record and the private key
  is gone; a truncated pubkey verifies nothing.
