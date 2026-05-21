# 2026-05-21 — ATECC bridge pivot to FT260 (real breakthrough)

## What we found
- MCP2221A path is genuinely broken for ATECC chips — independently verified
  by rounin's EEVblog thread (2024). Stop-pulse glitches + fixed 333kHz baud
  + can't generate proper wake pulse for ATECC sleep recovery.
- Trust&GO chips at Mouser: all variants "Factory Special Order" — structurally
  unavailable, not just temporarily out.
- FT260 USB-I2C bridge works for ATECC per rounin's verified bench experience.
- UMFT260EV1A eval board in stock at DigiKey (52 units), $14.21.

## What we did
- Ordered N x UMFT260EV1A from DigiKey
- Plan: drop in for MCP2221A on existing breadboard, no rewiring
- Provision bare ATECC608B chips using TFLXTLS slot config from
  cryptoauthlib repo

## Why this matters
- Two months of provisioning frustration was the BRIDGE, not the chip
- Avoids 9-12 week DM320118 lead time entirely
- Validates the Pico-as-kit-protocol-bridge plan as a real product opportunity
  (bare USB-I2C bridge chips have well-documented compatibility gaps)
- Strengthens federal SDVOSB pitch: "ZKNOT builds its own bridge fixture
  because off-the-shelf solutions have documented supply chain compatibility
  issues"

## References
- rounin EEVblog thread: https://www.eevblog.com/forum/projects/atecc608b-usb-breakout/
- FT260 datasheet
- FT260 out-of-tree Linux driver: https://github.com/MichaelZaidman/hid-ft260
- cryptoauthlib TFLXTLS XML: cryptoauthlib GitHub repo

## Next steps
- Wait for FT260 delivery (2-3 days)
- Drop in for MCP2221A
- Verify cryptoauthlib serial-read works
- Provision sacrificial ATECC608B
- Sign challenge, demo
