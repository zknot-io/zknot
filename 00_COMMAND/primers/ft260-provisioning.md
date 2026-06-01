<!--
PROJECT PRIMER — ft260-provisioning
- Paste the ROOT primer (CONTEXT.md) first, THEN this, to brief any AI.
- This is a BENCH + DEBUG file: technical state, what's tried, what's stuck. Keep it current as you debug.
- >>FILL<< = needs your input. The blanks are where I'd be guessing about your physical setup.
-->

# PRIMER — FT260 ATECC Provisioning  (🔥 THE UNBLOCKER)

## Why this matters (1 line)
This gates everything: SelfKnot builds AND the commercial HSM2 ceremony both wait on FT260 provisioning working.

## Goal
Provision bare TrustCUSTOM ATECC chips over USB using the **FT260 USB-I2C bridge** (UMFT260EV1A board), applying the **TFLXTLS slot configuration**, repeatably.

## Current state
- **Hardware:** wired up. Software bottleneck — no working script yet.
- **Why FT260 at all:** Trust&GO (pre-provisioned) ATECC chips unavailable at distributors -> pivoted to provisioning bare TrustCUSTOM chips ourselves. FT260 is the USB->I2C path that replaces the dead MCP2221A clones / Pico-bridge attempts.
- >>FILL: exact chip part number — ATECC608B TrustCUSTOM? confirm.<<
- >>FILL: FT260 mode in use — is the EV board strapped for I2C (not UART)? DCNF0/DCNF1 jumpers?<<
- >>FILL: wiring — SDA/SCL pins used, pull-up resistors present (value?), target I2C address (default 0x6A / 0xC0 8-bit for ATECC?), Vcc source.<<

## The actual blocker (what "no working script" means)
>>FILL: which is it?<<
- [ ] FT260 not enumerating / not seen by OS
- [ ] FT260 seen, but I2C scan finds no device (wiring / pull-ups / address)
- [ ] Device ACKs, but library/auth handshake fails
- [ ] Reads work, but applying TFLXTLS config / lock fails
- [ ] Other: >>describe<<

## Environment / toolchain
- Host: Debian Trixie 13 (zsh).
- >>FILL: library stack — cryptoauthlib (Python `cryptoauthlib` / `python -m ...`)? Does it have an FT260/HID transport, or are you driving FT260 via its own HID interface (ftd2xx / libft260 / hidapi)? This is the key architecture question — cryptoauthlib's stock HALs are I2C/SWI/Kit-protocol; FT260 needs a HID->I2C shim.<<
- >>FILL: how the OS exposes the FT260 — `/dev/hidraw*`? `lsusb` shows VID 0x0403 PID 0x6030? udev rule for non-root access?<<

## First-principles debug ladder (cheapest checks first)
1. `lsusb | grep -i future` — does the FT260 enumerate at all? (FTDI VID 0403)
2. `ls /dev/hidraw*` and permissions — can you read it without sudo? (udev rule may be needed)
3. I2C scan via the FT260's HID interface — does the ATECC ACK at its address? (proves wiring + pull-ups before any crypto)
4. Pull-up sanity: ATECC I2C needs pull-ups on SDA/SCL — confirm present (the EV board may or may not populate them).
5. Only after a clean ACK: attempt cryptoauthlib `atcab_init` with the FT260/HID transport, then read config zone (read before write — never lock until the config reads back correct).
6. Apply TFLXTLS config -> verify -> THEN lock. Locking is irreversible.

## ⚠️ Irreversibility flags (chips are cheap but not free)
- **Config/data zone lock is PERMANENT.** Read-verify-then-lock. Never lock on a guessed config.
- Burn through the cheapest bare chips first; keep known-good provisioned units aside as references.
- >>FILL: how many bare chips on hand to experiment with?<<

## Patent / IP note
PAT-001 is chip-agnostic ("hardware secure element" generically); FT260 vs other bridges is an implementation detail, not a claims issue. Provisioning method doesn't affect the FSM-gated human-actuation novelty.

## Done = (definition of "this is unblocked")
- [ ] One bare chip provisioned with TFLXTLS config via FT260, end to end
- [ ] Process written down repeatably (-> feeds the HSM2 ceremony design later)
- [ ] Known-good unit set aside as reference

## Pointers
- Hardware context, ZK/PUF concepts -> vault `6_SIG/`, `7_ENG/`
- Downstream that unblocks -> ROOT primer critical path (SelfKnot, commercial provisioning)

**Last verified:** 2026-06-01 (scaffold — >>FILL<< fields are hardware state only Shane can confirm)
Page 1 of 1
