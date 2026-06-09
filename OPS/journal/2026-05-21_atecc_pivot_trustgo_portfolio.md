# 2026-05-21 — ATECC provisioning pivot to Trust&GO + portfolio strategy

## What happened
- Spent the day trying to provision bare ATECC608B chips via real Adafruit MCP2221A breakouts
- Three independent cryptoauthlib paths returned -16 (no response)
- Diagnosed root cause: kernel mcp2221 driver's I2C HAL doesn't handle ATECC clock-stretching reliably
- DT100104 daughter-board confirmed useless without DM320118 host (9-12 week lead time everywhere)

## What we decided
Three-track portfolio:
1. Trust&GO ATECC608B-TNGTLSS for immediate demo on existing Pico hardware
2. Pico-as-kit-protocol-bridge as long-term provisioning fixture product
3. SBIR Phase I submission on DoW supply chain hardening topics by June 3

## Why
- Patent (PAT-001) is chip-agnostic. Trust&GO satisfies all claims.
- Federal opportunity window is real: 89 topics open, June 3 deadline, SDVOSB advantages
- Pico-bridge becomes a sellable product, not just an internal tool

## Next steps
- Tomorrow: order ATECC608B-TNGTLSS-G x5 from DigiKey (~$10)
- Tomorrow morning: CircuitPython sign-only script
- Friday: real signed challenge demo
- Next week: start Pico-bridge firmware
- May 26: survey open DoW SBIR topics
- June 3: SBIR Phase I proposal submission

## Lessons
- The pain is the opportunity: provisioning friction is a federal SDVOSB market
- Verify hardware stock AND form factor before recommending purchases
- Read patent claims literally — preferred embodiments don't restrict claims
