# FT260 → ATECC608 Provisioning (open / educational tier)

> **Scope.** This is the open/educational provisioning path ("protect your ideas on
> any platform"). It is **NOT** the official ZKNOT root of trust. The official root
> lives on a YubiHSM 2 as a separate trust domain. Do not conflate the two.

> **Status of facts below:** everything in "Verified" was confirmed on the bench
> 2026-05-30 against the actual hardware and/or primary vendor docs. "Open / unverified"
> is explicitly flagged. Don't promote anything out of the open section into a
> government-facing artifact without re-verifying against a primary source.

---

## Verified mechanics (bench-confirmed 2026-05-30)

### The bridge enumerates as USB HID, not a serial port
- FT260 (FTDI VID `0403`, PID `6030`) enumerates as **two** USB HID interfaces:
  - `input0` → **I²C** host controller
  - `input1` → **UART** (driver logs "uart interface is not supported")
- It does **not** create a `/dev/ttyUSB*`. The relevant nodes are `/dev/hidraw*` (raw)
  and — because the in-tree kernel driver binds — a cooked `/dev/i2c-N`.

### The kernel driver gives us a standard I²C adapter (this is the whole game)
- Debian Trixie kernel `6.12.x` ships `hid_ft260.ko` in-tree (author: Michael Zaidman).
- On bind it exposes the FT260's I²C controller to the Linux i2c-core as a normal
  bus adapter. On this machine it came up as **`/dev/i2c-6`**.
- Confirm with: `i2cdetect -l | grep -i ft260` → shows `i2c-6  ... FT260 usb-i2c bridge`.
- **Consequence:** standard `i2c-tools` and cryptoauthlib's stock Linux I²C HAL work
  directly. No custom HAL, no libft260, no hidraw glue. (See HAL decision below.)

### HAL decision: Path A (stock kernel I²C) — CONFIRMED, Path B not needed
- **Path A** = `ATCA_HAL_I2C` + `ATCA_ATECC608_SUPPORT`, `cfg.atcai2c.bus = 6`.
  cryptoauthlib talks to `/dev/i2c-6` like any other I²C master.
- **Path B** = custom HAL over FTDI libft260 / raw hidraw. The thread originally
  assumed this would be required ("the known hard part"). It is **not** — Path A
  works end to end. Path B is only a fallback if kernel-adapter wake reliability
  ever fails, which it did not.

### Address math (the footgun that actually bit)
- cryptoauthlib wants the I²C address in **8-bit form**: `8bit = (7bit << 1)`.
- These parts ACK at **7-bit `0x60`** → write **`0xC0`** in `cfg.atcai2c.address`.
- A 7-bit `0x6A` (the factory default) would be `0xD4`; `0x36` → `0x6C`; etc.

### Bus-health tell: the board EEPROM at 0x50
- The UMFT260EV1A populates a config EEPROM that ACKs at 7-bit **`0x50`**.
- Seeing `0x50` on a scan proves the FT260 → board I²C path is good (bridge, kernel
  driver, pull-ups, SCL/SDA on the header) **even while the target chip is silent.**
- This isolates faults: `0x50` present + target absent = problem is downstream of a
  known-good bus (leads / seating / chip / wake), not the bridge.

### Why i2cdetect can't, by itself, wake an ATECC
- ATECC wake requires SDA held low for > tWLO with SCL ignored during the window.
- `i2cdetect` issues a quick read/write; it physically cannot produce that hold.
- Therefore a **blank scan is not proof of a dead part** — it's the expected state of
  a sleeping ATECC. cryptoauthlib's `atcab_init` performs the real wake token.

### Wiring (UMFT260EV1A JP6 header ↔ ATECC608B SOIC-8), verified against both datasheets
| Wire | ATECC608B SOIC-8 pin | FT260 board header | Notes |
|------|----------------------|--------------------|-------|
| VCC 3.3 V | pin 8 | JP6-1 (VOUT3V3) | use 3.3 V, not VBUS 5 V (pull-ups tie to VCCIO) |
| SDA | pin 5 | JP6-10 (DIO6) | on-board pull-up via JP4 (closed by default) |
| SCL | pin 6 | JP6-11 (DIO5) | on-board pull-up via JP3 (closed by default) |
| GND | pin 4 | JP6-12 | — |
- ATECC pins 1, 2, 3, 7 = No-Connect, leave floating.
- SOIC-8 numbering wraps: 1–4 down the left, 5–8 up the right; dot/notch = pin 1.
- Add a 100 nF decoupling cap pin 8 ↔ pin 4, close to the chip — helps clean wakes.

### Order-code decode (Microchip primary source)
- Format: `ATECC608B-<pkg><iface><pack>`.
  - Package: `SS` = SOIC-8 (gull-wing, hand-solderable), `MA` = UDFN (leadless, needs reflow).
  - Interface: **`D` = I²C**, **`C` = Single-Wire (SWI)**.
  - Packing: `-T` = tape/reel, `-B` = tube.
- **Use SSHDA** (SOIC, I²C). **SSHCZ is the trap** — the `C` = SWI, no SCL line, will
  never appear on an I²C scan no matter how good the solder.
- 608A vs 608B: config bit-fields are identical; `cfg_ateccx08a_i2c_default()` covers both.

### "It's alive" probe (read-only, locks nothing)
- `~/alive.py` checks every return code (no all-zeros false positives).
- A genuine serial is **9 bytes, starts `01 23`, ends `EE`**.
- Bus = 6, address = `0xC0` for these parts.

---

## Confirmed parts inventory (2026-05-30)

All read at 7-bit `0x60` / 8-bit `0xC0` on `/dev/i2c-6`. All returned `ATCA_SUCCESS`
with valid `0123…ee` serials. Six distinct serials = six independent genuine parts.

| # | Serial (hex) | Note |
|---|--------------|------|
| 1 | `01239cb0044cf5d6ee` | new |
| 2 | `01231c0a2fc647cbee` | new |
| 3 | `0123d49d18b8602eee` | original "first light" part |
| 4 | `01235d49dfdb8e93ee` | new |
| 5 | `01233571a3172157ee` | new |
| 6 | `0123f0982825efe9ee` | new |

> Serials are device identifiers, not secrets — safe to keep in version control.
> (Private keys / provisioned secrets are NOT — those go to `~/ZKNOT/99_SENSITIVE/`,
> mode 600, gitignored.)

---

## Open / unverified — resolve before provisioning

1. **Preconfigured address (provenance).** Factory default is 7-bit `0x6A`; these parts
   all answer at `0x60`. Six-for-six at a non-default address means they were written
   before they reached us — these are **not pristine factory parts**. Acceptable for
   this open tier; would matter a great deal for anything trust-critical. **Read the
   config zone before writing anything** to see their actual state.

2. **FT260 I²C clock.** AN_394: valid range 60K–3400K bps; unsupported requests **fall
   back to 100K**. cryptoauthlib's Linux path treats 100 kHz as the only supported
   cryptoauth clock (Linux has no baud switching). Wake succeeded at whatever the
   current rate is, so the clock was never the blocker — but the exact rate was not
   read back. The driver exposes a sysfs clock attribute (README documents a 400 kHz
   example) on the **input0** node if it ever needs forcing. **Unverified:** exact
   sysfs attribute filename on this kernel build (not yet dumped successfully — the
   earlier dump hit the input1/UART node by mistake).

3. **sysfs node suffix drifts.** The `0003:0403:6030.00XX` suffix **increments on every
   re-enumeration**. Never hardcode it; derive the node by matching `HID_PHYS=...input0`
   in the node's `uevent`.

---

## Next step (still fully reversible — no locks)
Read the config zone on a part to see its preconfigured state. Locking config/data
zones is **one-way and irreversible** — that step stops for an explicit go-ahead and
the slot-config recipe gets version-controlled (recipe only; never secrets) before any
lock is issued.
