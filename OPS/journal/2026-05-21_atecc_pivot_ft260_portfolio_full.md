# 2026-05-21 — ATECC Provisioning Pivot: MCP2221A Dead, FT260 Path, Portfolio Strategy

**Workstream:** hw / fw / biz
**Session type:** Major strategic pivot + bench diagnosis
**Related docs:** HANDOFF_pico_as_kit_protocol_bridge.md, STRATEGY_federal_cryptographic_provisioning.md, ZKKEY_CONNECT_BOM_REV1.md, ZKKEY_AIR_BOM_REV1.md

---

## TL;DR (if you read nothing else)

The chips were never the problem. **Commodity USB-I2C bridge chips were the
problem.** MCP2221A is permanently ruled out for ATECC (verified by my own
bench + rounin's EEVblog thread). Ordered FT260 eval boards (UMFT260EV1A) as
the working bench bridge. Trust&GO chips turned out to be Factory Special
Order (unavailable). DM320118 host board is 9-12 weeks out everywhere.
Pivoted to a three-track portfolio: (1) FT260 bench provisioning of bare
chips, (2) Pico-as-kit-protocol-bridge as the real product, (3) SBIR Phase I
federal positioning by June 3. Bigger vision crystallized: "provision
anything anywhere with commonly-available parts" — a universal provisioning
knowledge base + fixture that serves the unserved global middle market.

---

## What happened this session

### The bench work (Problem: provisioning)

- Real Adafruit 4471 MCP2221A breakouts arrived (5 units, all genuine, USB-stable)
- Kernel mcp2221 driver loaded cleanly, /dev/i2c-6 exposed
- cryptoauthlib's Linux I2C HAL initialized successfully (Status 0)
- BUT every ATECC command beyond init returned **-16 (ATCA_RX_NO_RESPONSE)**
- Tested 3 variations: 8-bit addr (0xC0), 7-bit addr (0x60), 100kHz baud — all -16
- i2cdetect -y 6 returned empty grid even with proper external 4.7kΩ pullups
- Read-mode probe (-r) also empty; manual wake via i2cset to 0x00 also failed
- Tried cryptoauthlib HID HAL: kithid default expects VID 03EB/PID 2312
  (Microchip dev kit), returned -31 (ATCA_NO_DEVICES) on bare MCP2221A
- Confirmed: kernel mcp2221 driver claims the HID device and removes the
  hidraw node, so the HID HAL path can't see the MCP2221A raw interface anyway

### Root cause (externally verified)

rounin's EEVblog thread "ATECC608B USB breakout" (mid-2024) independently
documents the SAME failures from hands-on bench work:
- URL: https://www.eevblog.com/forum/projects/atecc608b-usb-breakout/
- CP2112 bridge: can't write to general-call address 0x00, can't wake ATECC
- MCP2221A bridge: stop-pulse glitches, bitrate fixed at 333kHz (too fast for
  ATECC wake), kernel driver can't change baud from userland, clock-stretch
  handling unreliable
- FT260 bridge: WORKS — properly generates wake pulse, out-of-tree Linux
  driver allows userland baud rate change via /sys/bus/hid/drivers/ft260
- FT260 driver: https://github.com/MichaelZaidman/hid-ft260

This was the breakthrough of the session: the failure was the bridge, not us.

### The hardware ID confusion (my errors)

I made multiple errors this week that cost a day, documented here so I don't
repeat them:
- Conflated DT100104 (mikroBUS daughter-board, no USB) with DM320118 (the
  USB host board). DT100104 alone is useless — needs DM320118 host.
- Recommended DM320118 as a fix; it's 9-12 weeks out at every distributor
  (DigiKey 0 stock, Microchip Direct ships 14-Aug-2026, Mouser 8/3/2026,
  Newark 9 weeks).
- Floated OPTIGA Trust M as a chip switch; its eval boards have the SAME
  supply pinch (OPTIGATRUSTADAPTERTOBO1 out, March-April 2026 dates).
- Gave malformed DigiKey part numbers for Trust&GO chips (added 150- prefix
  that doesn't exist for that variant).
- Trusted "ships today" web-search snippets that contradicted live DigiKey
  stock pages. Lesson: live product page is ground truth, snippets lie.

### The supply reality (verified on live pages)

- Trust&GO ATECC (all variants checked at Mouser): "Not Available" +
  "Factory Special Order" — structurally non-stocked, requires factory run
  - ATECC608B-TNGTLSU-G, ATECC608B-TNGTLSU-C, ATECC608C-TNGTLSS-B all FSO
  - ATECC608B-TNGTLSS-B at DigiKey: "unable to accept backorders"
- DM320118 host board: 9-12 weeks everywhere
- FT260 eval board (UMFT260EV1A): **In-Stock 52 units at DigiKey, $14.21,
  part 768-1280-ND.** This is the win.

---

## Decisions locked

### DECISION: MCP2221A permanently abandoned for ATECC
Verified non-functional by own bench + external confirmation. Do not retry.
The 5 Adafruit 4471 units stay as general-purpose I2C bench tools (not for
ATECC). 6 bare MCP2221A chips reserved for possible future non-ATECC fixtures.

### DECISION: FT260 is the bench bridge
Ordered 2-3x UMFT260EV1A from DigiKey (768-1280-ND, $14.21 ea). Drops in for
MCP2221A on existing breadboard, no rewiring. rounin verified it handles
ATECC wake + clock-stretch. Out-of-tree driver (MichaelZaidman/hid-ft260)
enables userland baud control.

### DECISION: Provision bare TrustCUSTOM chips ourselves
We have 10x bare ATECC608B-SSHCZ SOIC-8 (virgin, unlocked) + 10x UDFN from
the 2026-05-16 DigiKey order. These are the right chips for self-provisioning.
Use TFLXTLS slot config XML from cryptoauthlib repo as the canonical config
(do NOT design slot config from datasheet — produces 0x0F Sign failures).
Validate on 5+ sacrificial chips before touching Demo Unit #2.

### DECISION: Pico-as-kit-protocol-bridge is the production fixture
Long-term product. Port Microchip's cryptoauth-d21-host kit firmware to
RP2350 + Pico SDK (C/C++, NOT CircuitPython). FT260 serves as known-good
reference while building it. Full handoff doc written:
HANDOFF_pico_as_kit_protocol_bridge.md.

### DECISION: SBIR Phase I federal positioning, June 3 deadline
89 DoW topics open now, 44 more May 27. Target a "secure element provisioning
fixture for DoW supply chain hardening" fit. Full strategy doc written:
STRATEGY_federal_cryptographic_provisioning.md.

### DECISION: MCU choice clarified (runtime vs fixture)
- Runtime (ZKKey Connect/Air): any MCU talks to ATECC over I2C fine. Pico 2
  non-W stays the choice. STM32 fine alternative (patent §2.3 preferred
  embodiment). AVOID ESP32 (radio liability vs air-gap patent claim).
- Fixture (ZKNOT-FIXTURE-001): Pico-bridge escapes commodity-bridge problems
  by controlling I2C timing in firmware. STM32 also viable (kit firmware runs
  on SAMD21, similar class).

---

## The conceptual clarification that matters most

TWO SEPARATE PROBLEMS, do not conflate:

**Problem A — Provisioning (hard):** host computer + bridge + chip, done once.
The MCP2221A/FT260 saga is ENTIRELY about the bridge in this problem.

**Problem B — Runtime signing (easy):** embedded MCU talks DIRECTLY to ATECC
over plain I2C, no bridge, done forever in the product. This ALWAYS WORKED.
Millions of devices do it. Our own zkauth_firmware.ino (Feb 2026) proved it.

Why the Pico "appeared" to fail: (1) Adafruit CircuitPython library chokes on
64-byte responses (GenKey/sign) — a LIBRARY limit, not hardware; (2) we were
using Pico/MCP2221A for Problem A (hard) instead of just Problem B (easy).

One-sentence summary: the chips were never the problem; commodity USB-I2C
bridges were the problem; real MCUs (including Pico running custom bridge
firmware) don't have that problem.

---

## The bigger vision (crystallized this session)

"Provision anything anywhere with commonly-available parts." A universal,
low-cost, documented provisioning recipe set. Someone in Lagos/Nairobi/Dhaka
who can't get Microchip's $24-and-9-weeks dev kit, can't run TPDS-on-Windows,
has no corporate procurement — they should be able to provision a secure
element with whatever bridge they can actually get (Pi, Pico, FT260) using
ZKNOT's published recipes.

Why it matters:
1. Humanitarian/development angle — enabling trusted hardware in underserved
   regions. Maps to DoW partner-nation industrial base themes, State/USAID
   tech-capacity programs, "trusted microelectronics for partner nations."
2. Standards/authority play — publish the canonical guide, become the
   reference authority. Reputational capital feeding the whole business.
3. Natural product wrapper for Pico-bridge — open firmware, documented BOM,
   bridge options ranked by regional availability.

The two months of pain IS the intellectual property behind this vision. A
quiet working STM32 board would have given a board but no insight into the
failure landscape. The detour bought the understanding.

FUTURE TODO: draft a "Universal Secure Element Provisioning Guide" outline —
the publishable artifact. Decision tree by available-bridge, recipe per
bridge, verification steps. (Not started — planted for a future session.)

---

## On the STM32-on-JLCPCB path

NOT closed. Still fully available. STM32 talks to ATECC over I2C directly,
no bridge drama, patent's preferred embodiment. When ready to leave
breadboarding, the STM32 build on JLCPCB is a clean path and JLC will
assemble cheaply. This week opened that door wider (now understand
provisioning well enough to provision the chips that go on those boards),
didn't close it. The self-criticism ("should've stuck to STM32") is
misplaced — the detour was the education.

---

## Current bench inventory (as of session)

| Item | Status | Use |
|---|---|---|
| Demo Unit #1 (0123B77FB2B77F92EE) | BRICKED (lock_all_zones) | scrap/reference |
| Demo Unit #2 (012358E0A17F79D6EE) | Virgin reference | DO NOT TOUCH until process validated |
| Live Pico ATECC (012330E6EA45F9CCEE) | Virgin, healthy | runtime demo platform |
| ~4 virgin Pico 2 boards | Untouched | reserve 1 for bridge firmware dev |
| 10x bare ATECC608B SOIC-8 | Virgin TrustCUSTOM | sacrificial provisioning targets |
| 10x bare ATECC608B UDFN | Virgin | production builds (needs hot air) |
| 5x Adafruit 4471 MCP2221A | Works USB, useless for ATECC | general I2C bench tools |
| 6x bare MCP2221A chips | New | future non-ATECC fixtures |
| DT100104 daughter-board | Useless w/o DM320118 | hold for if DM320118 ever arrives |
| 2-3x UMFT260EV1A FT260 | ON ORDER (arriving 2-3 days) | the working bench bridge |
| Saleae Logic Pro 16 | Working | wire-level diagnosis (essential) |
| SparkFun SOIC-to-DIP adapter | Working, has pullups | chip mounting |
| Pi 5 + Pi Zero | Abandoned | drawer |

---

## Next steps (when FT260 arrives, ~2-3 days)

1. Drop FT260 in for MCP2221A on existing breadboard (same 4 wires)
2. Install FT260 driver if needed (MichaelZaidman/hid-ft260)
3. Run cryptoauthlib serial-read — expect SUCCESS this time
4. Provision a sacrificial bare ATECC608B using TFLXTLS slot config XML
5. Sequence: config_write → config_lock → data_write → gen_key → data_lock
6. Capture each step's wire traffic on Saleae for the provisioning runbook
7. ecdsa_sign(slot=0, hash) → verify 64-byte signature externally
8. Display hash on OLED via Pico (runtime path) — demo artifact

## Parallel tracks

- Pico-bridge firmware dev (1-2 weeks) — see handoff doc
- DoW SBIR topic survey by May 26, proposal draft, submit by June 3
- Eventually: Universal Provisioning Guide (the publishable vision artifact)
- Eventually: STM32-on-JLCPCB real PCB build

## Pending Claude deliverables (promised, not yet delivered)

- CircuitPython/cryptoauthlib sign-only script for when FT260 arrives
- TFLXTLS slot config translated to Python provisioning script
- Step-by-step provisioning runbook with expected outputs per step
- DoW SBIR topic survey (by May 26)

---

## Mistakes log (do not repeat)

1. Don't buy Amazon MCP2221A clones (25% DOA, established earlier)
2. Don't use Adafruit lock_all_zones() (bricked Demo Unit #1)
3. Don't derive slot config from datasheet — use cryptoauthlib TFLXTLS XML
4. Don't burn Demo Unit #2 until sacrificial chips validate the process
5. Don't try Pi 5 path again
6. Verify hardware stock AND form factor on LIVE pages before recommending
7. Don't conflate daughter-boards with host boards (DT100104 vs DM320118)
8. Don't add WiFi/BT ever (violates patent air-gap claim)
9. Web-search snippets lie about stock — live distributor page is truth
10. Don't recommend chip switches without verifying the alternative's eval
    board supply (OPTIGA had same pinch as ATECC)

---

## Founder note

Two months, ~$2000, demoralizing. But this session turned the corner: clear
diagnosis, a $14 in-stock fix, a defensible federal story, and a vision
("provision anywhere") bigger than the original problem. The pain is the
opportunity — and now there's a documented path that doesn't depend on
out-of-stock parts. All in.
