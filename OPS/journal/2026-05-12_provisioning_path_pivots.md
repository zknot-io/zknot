# 2026-05-12 — Provisioning Path Pivots and Honest Reset

**Status:** Hardware on order. Real work resumes when MCP2221A arrives Wednesday.
**Workstream:** sig / firmware / business strategy
**Outcome:** Multiple pivots today; landed on a coherent plan + a parallel business deep-dive.

## What happened today

Morning started with intent to provision the ATECC608B via the Pi 5 + cryptoauthlib path agreed in last night's journal. Pi 5 install spiraled through old image / Pi 4 device-tree issues / Flatpak Imager permissions / Ethernet driver setup, consuming ~3 hours without producing a working provisioning host.

Pivoted to: use the existing Debian box + USB-to-I2C adapter (MCP2221A). cryptoauthlib already installed in `~/zknot-provision/.venv`. Adafruit 4471 out of stock; ordered an Amazon clone (GODIYMODULES MCP2221A breakout) for next-day delivery as the primary path, with a DigiKey order held in reserve depending on whether the Amazon part works.

## Engineering decisions locked

- **Method:** Microchip cryptoauthlib (official library) on Debian, talking to ATECC608B via MCP2221A HID HAL. No more CircuitPython / Adafruit library for provisioning.
- **Hardware path:** MCP2221A USB-I2C adapter on Debian box → SparkFun SOIC-to-DIP adapter (with chip soldered, has pullups) → ATECC608B chip. Saleae Logic Pro 16 taps SDA/SCL for verification.
- **Pi 5 is shelved:** not the right tool for now. May revisit later as a dedicated production fixture once the core flow is proven.
- **No raw I2C bypass:** the Adafruit library CRC bug is real but worked around by getting off Adafruit entirely. Using real cryptoauthlib eliminates the bug class.

## Business decision

Drafted a handoff document on secure-element provisioning as a federal/SDVOSB business opportunity. Saved at `~/ZKNOT/5_PLANS/HANDOFF_secure_element_provisioning_business_opportunity.md`. To be deep-dived in a separate AI thread; not to distract from the immediate engineering goal of one provisioned chip.

## What's NOT happening

- Not buying a Pi 5 dev kit
- Not buying the DM320118 / DM320119 (DM320119 is a different product, not a newer DM320118)
- Not implementing Kit Protocol on the Pico
- Not writing raw ATECC I2C wire protocol from scratch
- Not deep-diving the business case until at least one chip is provisioned

## What IS happening

- Amazon MCP2221A clone arrives Wednesday
- If it works: cryptoauthlib provisioning, dry-run, then commit one virgin chip Wednesday/Thursday
- If it's DOA: DigiKey order Wednesday for Friday-Saturday arrival, then same flow

## Honest notes for next session

- Be skeptical of any plan that requires more than 30 minutes of yak-shaving before producing observable progress
- When AI proposes a new tool/path, ask "what's already on the bench" first
- One provisioned chip with one real signature is the only deliverable that matters this week
- Bankruptcy timeline is real — keep that in the visible field
