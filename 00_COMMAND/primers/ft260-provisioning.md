<!--
PROJECT PRIMER — ft260-provisioning
- Paste the ROOT primer (CONTEXT.md) first, THEN this, to brief any AI.
- STATUS CHANGED 2026-06-01: bring-up SOLVED. Recipe proven on part #1. Remaining work = batch replay (9 parts).
- >>FILL<< = needs your input.
-->

# PRIMER — FT260 ATECC Provisioning  (✅ RECIPE PROVEN — now a batch task)

## Why this matters (1 line)
Unblocks SelfKnot builds AND the commercial HSM2 ceremony. As of 2026-06-01 the bring-up is DONE — this is no longer the blocker, it's a mechanical replay.

## Status: SOLVED on part #1 (2026-06-01)
- First Tier-0 self-assertion device fully provisioned end-to-end and signature-verified.
- `lock_data_zone -> ATCA_SUCCESS`, data zone `LockValue 0x00 -> LOCKED`. Slot-0 P256 key permanent + non-extractable.
- Recipe validated; the other 9 known-good parts are a mechanical replay (see "Batch replay" below).

## The architecture that worked (the non-obvious part)
- **Transport: the mainline `hid_ft260` kernel driver** — NOT hidraw, NOT a cryptoauthlib HID/kit shim.
  `hid_ft260` binds the FT260's HID interface (USB `0403:6030`) and exposes a real Linux **`/dev/i2c-N` adapter**.
- That means the ATECC becomes a standard kernel I2C device, and cryptoauthlib's **stock `/dev/i2c` HAL** talks to it directly. No HID bridging needed. This sidesteps the whole transport problem most FT260+ATECC attempts get stuck on.
- Working config in cryptoauthlib: `cfg_ateccx08a_i2c_default()`, `cfg.atcai2c.bus = 6` (the FT260 adapter number — verify yours via `i2cdetect -l`), `cfg.atcai2c.address = 0xC0` (8-bit form; chip enumerated at 7-bit `0x60` on the bus scan).
- >>FILL: confirm your adapter number is stable across replug, or note how to re-find it.<<

## The PROVEN provisioning sequence (config-lock → GenKey → host-verify → data-lock)
1. `atcab_init` against `/dev/i2c-N` at the chip address; `atcab_read_serial_number` — confirm seated serial.
2. `atcab_read_config_zone` — verify config BEFORE locking. (read-verify-then-lock discipline)
3. Lock CONFIG zone (irreversible gate #1).
4. `GenKey` on slot 0 — keypair born on-chip, private key non-extractable by design. Record the 64B (X||Y) pubkey.
5. **Host-side verify** the test signature (see gotcha below) — sign on chip, verify on host against the GenKey pubkey.
6. Lock DATA zone (irreversible gate #2) — freezes slot-0 key forever. Do this LAST, behind a serial guard + 5s abort window.

## ⚠️ Key gotcha — chip-verify vs host-verify
- On-chip `verify_extern` returned **ATCA_COMM_FAIL** — but that's a COMM error, NOT a crypto failure. Don't read it as "signature invalid."
- **Host-side verify** (verify the chip's signature on the host against the recorded pubkey) PASSED: `signature valid? -> True`.
- This is the correct test anyway: a real verifier checks the signature host-side against the recorded pubkey, which is exactly what the ledger exists to enable. >>Worth understanding WHY chip-verify glitched — that understanding is the moat, not the command.<<

## Safety patterns that worked (keep for the batch)
- **Serial guard:** script aborts if the seated serial != expected `EXPECT` value — refuses to lock the wrong part.
- **Precondition check:** aborts if the zone is already locked (reads lock byte before acting).
- **5-second Ctrl-C window** before each irreversible lock, with the serial printed.
- **Test-article discipline:** full recipe proven on ONE sacrificial part before batching.

## The ledger — sole serial↔pubkey record
- File: `3_OPS/km/systems/atecc-provisioning-ledger.psv` (pipe-delimited, one row per chip).
- Tier 0 = SelfKnot/DIY, self-asserted, NOT official ZK# / NOT PUF-tracked. NO secrets in the file (pubkey only; private key is on-chip).
- ⚠️ This is the ONLY off-chip record mapping a permanently-locked chip to its pubkey. A truncated/abbreviated pubkey can't verify a signature — store the FULL 128-char (X||Y) value.
- Part #1: serial `012337d1a9f0eb45ee`, addr `0x60`, slot 0, cfg_lock + keygen + data_lock 2026-06-01, testsig PASS.
- ⚠️ BACKUP: vault is single-copy on ~2-day manual Drive upload. After each provisioning session, upload the ledger to ops@zknot.io + shane.systems@gmail.com SAME session — these records exist nowhere else and the chip can never be re-keyed.

## Batch replay (the remaining 9 — fresh-energy task, not end-of-session)
- 9 known-good parts left. Each is the same gated sequence; the recipe is fixed.
- Per part: set new `EXPECT` serial in the lock script(s), fresh `read_config_zone` to confirm what's seated, run the gated sequence, add a ledger row with the FULL pubkey, commit, back up.
- Failure mode to respect: fat-fingered serial guard or mis-seated part locked to the wrong ledger row. Clear-headed task — don't batch tired.

## Done = (this project's exit criteria)
- [x] One part fully provisioned + signature-verified (2026-06-01)
- [x] Recipe written down repeatably (this file)
- [ ] >>Batch the remaining 9 (or however many you want now)<<
- [ ] Ledger backed up off-box after the latest session

## What this unblocks (back to ROOT critical path)
- SelfKnot builds + content — the FT260-as-kernel-i2c trick + proven lock sequence IS the "protect your ideas" guide material.
- Commercial provisioning — this Tier-0 recipe is the rehearsal for the HSM2 ceremony + ZK#/PUF tracking.

**Last verified:** 2026-06-01 (recipe proven on part #1; >>FILL<< fields are config/understanding notes)
Page 1 of 1
