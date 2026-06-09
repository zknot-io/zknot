# PowerVerify AirGap — Shopify Listing Copy (honest-copy v1)

> 2026-06-02 · paste-ready for **shop.zknot.io** · founder/ZKNOT, INC.
> Claim discipline per trust-model review (2026-05-29). Every line passes:
> "is this physically true of the unit in hand?"

---

## TITLE
PowerVerify AirGap — Power-Only USB Data Blocker

## TAGLINE / SUBTITLE
**Look through the clear pot. There are no data lines.**

## PRICE
$39

## AVAILABILITY
In stock. Ships within **[CONFIRM: 24–48h? 2 business days?]** of your order.
Built and potted in the USA, one at a time.

---

## SHORT DESCRIPTION (above-the-fold pitch)

A malicious cable or charging port can move data, not just power. PowerVerify
AirGap can't — the data lines aren't disabled in firmware, they're physically
not on the board. Look through the clear potting and see for yourself: power
pins, no data path. Charge from any port, kiosk, or borrowed cable without
opening a data channel to your device.

---

## FULL DESCRIPTION

Most "data blockers" ask you to trust a spec sheet. PowerVerify asks you to look.

The housing is clear on purpose. The data lines a malicious cable would use to
talk to your phone or laptop are physically absent from the board — and you can
confirm that with your own eyes through the pot. That's the whole idea:
**verify, don't trust.**

Use it anywhere you'd plug into power you don't control — public charging kiosks,
conference tables, hotel ports, a cable someone hands you. Power flows; data has
nowhere to go.

### What it does
- Passes USB power through to your device (60W max — 20V / 3A)
- Physically omits the data lines — no data path exists on the board
- Visible verification: the clear pot lets you confirm there are no data traces

### What it is, honestly
This is a **Rev 0 pilot unit**. It does one thing and does it *physically*: power
passthrough with no data path. It is **not** a cryptographic-provenance device
yet — early units carry a scannable record, but that record is not independently
third-party verifiable today, and we won't pretend otherwise.

Every Rev 0 buyer gets a **free swap to Rev 1** when the hardware-attested
version ships. You're an early pilot, and we'll treat you like one.

### Who makes it
ZKNOT, INC. — veteran-owned (SDVOSB), Salt Lake City, Utah. Designed, built, and
potted in the USA.

---

## SPECS
- **Power:** 60W max (20V / 3A)
- **Connector:** USB-C passthrough  *[CONFIRM connector type before publishing]*
- **Data lines:** physically absent
- **Housing:** clear potting (visible verification)
- **Origin:** Made in USA
- **Revision:** Rev 0 pilot — free Rev 1 upgrade included

---

## WHAT WAS DELIBERATELY LEFT OUT (and why)

Per the trust-model review (2026-05-29), this listing makes only claims that are
physically true of the unit in hand:

- **NO** "unforgeable," "court-grade," "forensic," or "cryptographically proves
  provenance." Units sign with server-side HMAC, which is not third-party
  verifiable — that's a Rev 1 / post-HSM-ceremony claim, a different thread.
- **"Reduces data-exposure risk," not "prevents hacking."**
- **"Designed to," not "guaranteed to."**
- The scannable record is mentioned only as *existing*, never as *proof*.

---

## BEFORE YOU PUBLISH — checklist
- [ ] Replace `[ship window]` with the real number you can hit (fulfillment check)
- [ ] Confirm connector type (USB-C assumed)
- [ ] Delete every instance of old "Pre-Order, ships June 30" and "100W max"
- [ ] Confirm which verify-link form resolves (curl check) before linking buyers
- [ ] Skim the live preview on mobile — most buyers land there
