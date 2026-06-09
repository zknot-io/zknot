# 2026-05-16 — MCP2221A Amazon Clones DOA, Pico Setup Restored

**Status:** Back to known-good Pico inspection state. No silicon harmed.
**Workstream:** sig / hardware
**Outcome:** Amazon MCP2221A clones (GODIYMODULES brand) both DOA. Path forward decided tomorrow with rested head.

## What happened

Plan from yesterday's journal was: MCP2221A arrives, plug into Debian box,
run cryptoauthlib, read ATECC serial via real Microchip library. Confirms
the path before designing slot config.

Amazon order arrived. Two MCP2221A boards in the package.

Board 1: enumerated cleanly (idVendor=04d8, idProduct=00dd, Manufacturer
"Microchip Technology Inc."). Kernel `mcp2221` driver auto-loaded. Created
`/dev/i2c-6`. Multiple `i2cdetect -y 6` runs returned empty grid. Repeatedly
USB-disconnected over a span of minutes (devices 28 → 29 → 30 → 31 → 32, each
dropping within 1-58 seconds).

Board 2: same DOA pattern.

Reddit thread (r/embedded, "What's your actual production ATECC608B
provisioning setup") had warned about this exact failure mode for cheap
Amazon clones — solder bridges on the USB-C connector causing intermittent
brownouts under load. 25% DOA rate in user reviews. Confirmed.

## What we learned

1. Cheap Amazon MCP2221A clones are unreliable. Two dead in one order is
   enough data — don't reorder same brand.
2. The kernel `mcp2221` driver works fine when given working hardware
   (we saw it load both times). Issue is hardware, not driver.
3. cryptoauthlib path is still correct — just needs real hardware.
4. The Pico setup remains the known-good baseline. Read-only inspection
   script confirms virgin chip (serial-of-currently-plugged-unit) is
   healthy after all the wire-shuffling.

## What changed about the plan

- Don't buy more Amazon clones. Order legitimate Adafruit 4471 (Adafruit
  direct or DigiKey) when in stock, or take the Reddit advice and use
  the Pico itself as the USB-I2C bridge to cryptoauthlib (no new hardware
  needed, ~4-8 hours of firmware work).
- The DigiKey trimmed cart (~$50) is the easy answer if budget allows.
- The Pico-as-bridge is the zero-cost answer that aligns with the
  Reddit responder's "production path" recommendation.
- Decision deferred to tomorrow with a rested head.

## What's NOT changed

- Curve P-256 (forced by ATECC608B)
- One key per device, in-chip generation, no rotation
- Registry CSV schema design
- Reddit-thread engineering decisions: canonical config from cryptoauthlib
  TrustFLEX example, GenKey returns 64-byte pubkey directly, sacrificial
  unit policy for first locks
- Three-tier cert chain design (manufacturer / factory / device) for v2

## Wiring state at end of day

Pico breadboard restored. OLED at 0x3c, ATECC at 0x60. Inspection script
confirms virgin chip. Photo of working wiring should be taken before any
further changes.

MCP2221A boards: in drawer. Treat as scrap until/unless we want to try
reflowing the USB-C connectors per Amazon reviewer's recovery method.

