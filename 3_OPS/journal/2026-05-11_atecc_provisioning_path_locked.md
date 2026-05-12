# 2026-05-11 — ATECC608B Provisioning Path Finally Locked

**Status:** Provisioning path identified and validated as next-session ready
**Workstream:** sig / firmware
**Outcome:** Stop chasing CircuitPython + Adafruit dead ends. Move to Pi 5 + Microchip CryptoAuthLib + Saleae verification.

## What was confirmed this session

1. **Adafruit `adafruit_atecc` library is the blocker, not the chip.** Diagnostic ran on virgin chip `012330E6EA45F9CCEE` (Pico breadboard, currently plugged in). Short ops (read serial, check lock state) work fine. 64-byte response ops (`gen_key`, `ecdsa_sign`) fail with `RuntimeError: CRC Mismatch` regardless of I2C clock speed. Tested at both 400 kHz (default) and 100 kHz. Clock stretching is NOT the cause. The library cannot read 64-byte responses correctly on RP2350.

2. **Demo Unit #1 brick was caused by `atecc.lock_all_zones()`** (Adafruit high-level helper). The slot 0 config it produces rejects external-mode Sign with status `0x0F`. Silicon serial `0123B77FB2B77F92EE`. Sacred demo only, never to be modified.

3. **Hardware inventory:**
   - Demo Unit #1: locked, bricked for signing. `0123B77FB2B77F92EE`.
   - Demo Unit #2: virgin, currently-plugged-in Pico. `012330E6EA45F9CCEE`.
   - 5 additional virgin Pico Connect breadboards on bench.

## Why the path was wrong

I let DOC-HW-002 (Rev A, 2026-04-27) drive the conversation. That guide documents the Adafruit CircuitPython approach because that was the working prototype path. Appendix A.4 of the guide already flagged the CRC issue and listed three potential fixes — including "switch to Microchip CryptoAuthLib" and "raw I2C bypass." I missed that for hours.

Also missed for hours: the February 2026 firmware `~/ZKNOT/6_SIG/firmware/zkauth_firmware.ino`, which uses Microchip CryptoAuthLib directly and shows the correct provisioning sequence (`atcab_genkey(0, pubkey)` then `atcab_lock_data_zone()`). That's a working reference for the right approach.

## The actual path forward

Provisioning is a one-time-per-chip operation that does NOT need to run on the deployment host. Standard pattern: provisioning fixture (Pi 5 + I2C) is separate from runtime device (Pico). Provision the chip on the Pi, then mount it on the Pico for normal operation. The Pico's `ecdsa_sign` calls on a properly-provisioned chip should work (or if Adafruit's `ecdsa_sign` has the same CRC bug, the fallback is replacing just that one call with raw wire protocol — much smaller scope than reimplementing provisioning).

Tools selected:
- **Pi 5** as provisioning host (direct GPIO I2C, clean debugging)
- **Microchip `cryptoauthlib` from PyPI** (official library, Linux I2C HAL, same library used in production for millions of ATECC608Bs)
- **Saleae Logic 16 Pro** taps SDA/SCL during all I2C transactions — ground-truth verification of wire-level behavior

## Decisions locked

- Curve: P-256 (forced by ATECC608B silicon)
- Key lifecycle: one key per device, generated in-chip, never rotates, no recovery
- Registry: self-hosted CSV at `~/ZKNOT/3_OPS/km/registry/zknot_devices.csv`, designed to evolve to public registry then manufacturer attestation
- Short_code: first 8 hex chars of SHA-256(pubkey)
- Provisioning fixture: Pi 5, NOT the deployment Pico
- First provisioning target: one of the 5 untouched virgin units (NOT Demo Unit #2 — keep that as virgin reference until at least one custom-provisioned unit exists)

## What to do tomorrow morning

1. Power down breadboard, unwire ATECC from Pico (keep wire pattern photo for reattach later). Move just the 4 wires (VIN, GND, SDA, SCL) to Pi 5 GPIO:
   - Pi pin 1 (3.3V) to ATECC VIN
   - Pi pin 6 (GND) to ATECC GND
   - Pi pin 3 (GPIO 2 / SDA) to ATECC SDA
   - Pi pin 5 (GPIO 3 / SCL) to ATECC SCL
2. Tap Saleae channels 0 and 1 on SDA and SCL. Saleae GND to Pi GND.
3. On the Pi 5:
   - sudo raspi-config nonint do_i2c 0
   - sudo apt install -y i2c-tools python3-pip python3-venv
   - mkdir -p ~/zknot-provision && cd ~/zknot-provision
   - python3 -m venv .venv && source .venv/bin/activate
   - pip install cryptoauthlib
   - i2cdetect -y 1 (should show 0x60)
4. Run the read-only inspection script (TBD next session) — confirms the chip responds correctly via cryptoauthlib. Saleae capture verifies wire traffic.
5. STOP. No writes, no locks, no provisioning. Confirm the path works end to end before committing to any irreversible operation.

Session-after-next: design slot 0 config bytes explicitly, dry-run, review, commit on one virgin unit, read back the pubkey, register in CSV.

## Open items dropped today

- Brief document was drafted (`CONTEXT_BRIEF_atecc_provisioning.md`) but never saved. Marking as DO NOT SAVE — the brief codified the "other chat" CRC investigation as if it were canonical, when really the actionable path is the cryptoauthlib direction documented here. This journal entry is the canonical record.
