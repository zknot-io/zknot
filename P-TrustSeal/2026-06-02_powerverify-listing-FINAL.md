# PowerVerify AirGap — Final Listing Copy (verified)

> 2026-06-02 · shop.zknot.io · every claim verified against the physical unit
> (PV1-00053), the PAT-002 filing doc, and FBI/FCC sources.
> Product: power-only USB-C pigtail cable, clear-potted, 60W max, no data pins, no ICs.
> ONLY open item: pricing model (§ PRICING — pick one). Rest is paste-ready.

---

## TITLE (pick one)

1. **PowerVerify AirGap — Power-Only USB-C Cable You Can See Through**
2. **PowerVerify AirGap — Verifiable Power-Only USB-C Charging Cable (No Data Lines)**

---

## DESCRIPTION

**You shouldn't have to trust your charger.**

Public USB ports and unknown cables can carry data, not just power — which is why
the FBI and FCC have both warned travelers about "juice jacking." The FCC's own
advice: use a charging-only cable from a trusted supplier. Most data blockers ask
you to *trust* that they work. PowerVerify lets you *see* it.

Look through the clear epoxy. The data lines aren't switched off in software —
they're not there. The board says so itself: **DATA LINES PHYSICALLY ABSENT.**
Power flows over VBUS and GND, your charger and device negotiate over the CC pins,
and the D+/D− data pins simply don't exist in the connector. *Your charger can't
spy through this* — not because the path is disabled, but because it's absent.

### What you're getting
A short power-only USB-C cable (~90 mm pigtail) with the working board fully
visible through clear, tamper-evident epoxy. The USB-C source connector is
power-only 6-pin — no D+/D− data pins. You can read every component through the
pot: input surge protection, a VBUS filter, output surge protection — and nothing
else. No data traces. No chips. No firmware.

### Specifications
- USB-C power-only input (6-pin, no D+/D− pins) → USB-C plug to your device (pigtail)
- 5–20V DC, **60W max** — passes your charger's USB-C Power Delivery straight through
- Input + output surge protection (TVS diodes)
- VBUS filtering capacitor + ferrite EMI suppression
- Clear, tamper-evident epoxy potting — no screws, full visual verification
- Serial number + QR code, registered at verifyknot.io
- **Patent Pending — U.S. Application No. 63/961,118**
- Designed in Utah · hand-assembled, veteran-owned (SDVOSB) · Made in USA

### What it does NOT have
- **No data lines.** The D+/D− pins are physically absent from the connector and
  there are no data traces on the board — no USB enumeration is possible.
- **No chips. No firmware. No software.** It's a passive cable. Nothing to update,
  exploit, or phone home.
- **No cloud dependency.** It works offline, the same way, forever.

### How to verify it yourself
1. Hold it to the light — you can see there are no data lines.
2. Look at the connector — power-only, no D+/D− data pins.
3. Scan the QR or enter the code at **verifyknot.io** to look up the unit's
   registered manufacturing record by serial number.

*(That record confirms the unit's identity and build history — it's an honesty
trail you can check, not a third-party cryptographic proof. We'll always tell you
exactly what a claim is and isn't.)*

### Who it's for
Travelers charging in airports, hotels, and cafés · journalists and researchers
handling sensitive devices · attorneys handling digital evidence · anyone who saw
an FBI or FCC warning about public USB ports and wanted a real answer.

### Who it's not for
If you just need a charge-only cable at home, a $5 blocker is fine. This is for
people who want to verify, not trust.

---

> *When physics is policy, trust is optional.* — printed on every board.

---

## PRICING / FULFILLMENT — PICK ONE

> You have real, potted R1 units in hand (e.g. PV1-00053). That makes "ship now"
> genuinely available — which is the deciding fact between these two.

**OPTION A — Ship now (recommended if you have ≥3 sale-grade units ready):**
- Price: $39
- In stock — made to order, usually ships in **2–3 business days**
- Honest, present-tense, dollar-in-the-door this week. No date you can miss.

**OPTION B — Pre-order batch (per your pasted copy):**
- Price: $39 pre-order ($49 regular after launch)  *(confirm $49 is the real plan)*
- Ships June 30, 2026 · limited to first 50 · full refund any time before shipping
- ⚠️ Only choose this if you genuinely can't ship the units you already have, AND
  every claim stays true by ship date. You hold potted units now — a pre-order that
  *delays* shippable stock is a harder sell than "in stock, ships this week."

*(Tradeoff in one line: A converts a buyer into a shipped unit and a real funnel
signal now; B builds a bigger waitlist story but promises a date and sits on stock
you already have. With units in hand, A is the lower-risk path to the 30-day
revenue signal.)*

---

## PHOTO PLAN
- **HERO (image #1):** the component-side shot — "PowerVerify / DATA ABSENT / Your
  charger can't spy through this," diodes and filter visible through the pot. This
  IS the pitch. *(Reshoot tip: lose the warm window-glare at the bottom-right; shoot
  on a plain neutral surface, even, diffuse light. The current one is usable but a
  clean version will convert better as the thumbnail everywhere.)*
- **Image #2:** the label side — serial, QR, "Patent Pending," "When physics is
  policy, trust is optional." Legitimacy + verification story.
- Add the marketing video as media once shot.

---

## CLAIM-VERIFICATION LOG (so you can defend every line)
- 60W: silkscreened "5–20V DC POWER, 60W MAX" on the board ✓
- No data pins: board labels D+/D− as NC; "DATA LINES PHYSICALLY ABSENT" ✓
- No chips/firmware: only passive parts visible (TVS×2, cap, ferrite) ✓
- PD works: CC pins present and passed through; cable is passive ✓
- Patent No. 63/961,118: confirmed in PAT-002 doc, filed 2026-01-15 ✓
- FBI + FCC warnings: confirmed (FBI Denver 2023; FCC advisory since 2019) ✓
- Dropped: "100W" (false), "PUF tamper evident" (no PUF on board), "blue PD LED"
  (no LEDs on board), "TSA" (unverified)
