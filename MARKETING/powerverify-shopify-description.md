# PowerVerify — Verifiable Power-Only USB-C Charging Cable (No Data D+/D− Lines)

**$39.00**

## You shouldn't have to trust your charger. You should be able to prove it.

Public USB ports and unknown cables can move data, not just power — the reason the FBI and FCC have both warned travelers about "juice jacking," and why the FCC's guidance is to use a charging-only cable from a trusted supplier.

Here's the problem with most "data blockers": they ask you to *trust* that the data path is switched off. Software can be wrong. Switches can fail. You can't see any of it.

PowerVerify doesn't switch the data lines off. **They're not there.** As the device itself says: *When physics is policy, trust is optional.*

## Don't trust it. Verify it.

**See it.** Look straight through the clear, cast resin. No data traces, no chips, no firmware — just input surge protection, a VBUS filter, and output surge protection, with every pin labeled. The board states it plainly: *DATA LINES PHYSICALLY ABSENT — NO USB ENUMERATION.*

**Prove it won't talk.** Plug a computer into the input and your phone into the output. Your phone charges — and never appears as a USB device. It can't enumerate, because there's no data path to enumerate over.

**Confirm it's the real unit.** Every PowerVerify carries a one-of-a-kind optical fingerprint — the random scatter of particles suspended in its resin, which can't be reproduced. We photograph that fingerprint, front and back, and record it against the unit's serial at manufacture. Compare your unit to its registered photos at verifyknot.io to confirm it's the same physical object that left our bench.

Power flows over VBUS and GND. Your charger and device negotiate voltage over the CC pins. The D+/D− data pins simply don't exist in the connector. Your charger can't reach your device — not because the path is disabled, but because it was never built.

## Built as evidence, not as an accessory

Every PowerVerify is a serialized object with a build record, not an anonymous cable:

- It's sealed in a single solid pour of clear resin — no seams, no screws, no shell to pop open. To reach the board you'd have to destroy the unit, and its embedded serial label and unique fingerprint go with it.
- A serial and verification code link the unit to its registered manufacturing record at **verifyknot.io** — scan the QR or enter the code to confirm the unit's identity and build history.
- The optical fingerprint photos are signed at manufacture, so the registered record itself is tamper-evident.

*Straight talk about what that record is:* it's a provenance trail you can check — signed proof of how and when we built this specific unit, bound to its physical fingerprint. It is **not** a device-level cryptographic proof generated in the field; this passive unit carries no key and signs nothing on its own. (Our Attested tier does that — see below.) We'll always tell you exactly what a claim is and what it isn't.

## Specifications

- USB-C power-only input (6-pin, no D+/D− pins) → USB-C plug to your device (~50 mm pigtail)
- 5–20V DC, 60W max — passes your charger's USB-C Power Delivery straight through
- Input + output surge protection (TVS diodes)
- VBUS filtering capacitor + ferrite EMI suppression
- Solid clear-resin potting — no seams or screws, full visual verification; reinforced cable strain relief
- Unique optical fingerprint, photographed and signed at manufacture
- Serialized; manufacturing record registered at verifyknot.io
- Patent Pending — U.S. Application No. 63/961,118
- Designed in Utah · hand-assembled · veteran-owned (SDVOSB) · Made in USA

## What it deliberately does NOT have

- **No data lines.** D+/D− are physically absent from the connector and there are no data traces on the board. USB enumeration is impossible.
- **No chips. No firmware. No software.** It's a passive cable. Nothing to update, exploit, or phone home.
- **No cloud dependency.** It works offline, the same way, forever.

## Who it's for

Travelers charging in airports, hotels, and cafés · journalists and researchers handling sensitive devices · attorneys and investigators handling digital evidence · anyone who saw an FBI or FCC warning about public USB ports and wanted proof instead of a promise.

## Who it's not for

If you just need a charge-only cable at home, a $5 blocker is fine. PowerVerify is for people who need to *verify*, not trust — and to hand someone else the means to verify too.

## Need cryptographic proof, not just a build record?

A PowerVerify **Attested** version is in development — it adds a secure element that cryptographically signs each power session (device identity, timestamp, voltage/current, and proof no data path was active). If that's your requirement, get in touch.
