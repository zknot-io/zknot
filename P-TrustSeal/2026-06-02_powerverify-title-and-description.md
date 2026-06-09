# PowerVerify AirGap — Title + Listing Description (honest draft, v2)

> 2026-06-02 · for shop.zknot.io · reflects "things have changed": product is now
> a ~90mm power-only USB-C **pigtail cable**, not the dongle.
> ⚠️ Every `[VERIFY: …]` block is a claim I could NOT confirm or that conflicts with
> ground truth. Do not publish a bracketed line until you've resolved it.
> Honest-copy test on every line: "is this physically true of the unit in hand TODAY?"

---

## TITLE OPTIONS (pick one)

1. **PowerVerify AirGap — Power-Only USB-C Cable You Can See Through**
2. **PowerVerify AirGap — Verifiable Power-Only USB-C Cable (No Data Lines)**
3. **PowerVerify AirGap — Power-Only USB-C Charging Cable, Data Lines Physically Absent**

(#1 leads with the differentiator — the transparency. #2/#3 are more SEO-literal.)

---

## DESCRIPTION DRAFT

**Lead:**

> You shouldn't have to trust your charger.

Public USB ports *can* be used to move data, not just power — it's why the FBI,
FCC, and TSA have all warned travelers about "juice jacking."
`[VERIFY framing: keep this on the "possible/has been warned about" side — recent
reporting notes real-world juice-jacking is rare. "Has warned about" is true and
defensible; "will steal your data" invites fact-checking. Safer as written.]`
Every cheap data blocker asks you to *trust* it. PowerVerify lets you *verify* it.

Look through the clear epoxy. You can see there are no data lines.

**What you're buying**

A short power-only USB-C cable, approximately 90mm long, with the working board
visible through clear epoxy. The data pins (D+/D−) are physically absent — you
can see there are no data traces.
`[VERIFY: the exact pin-count claim. USB-C is 24 pins. If CC pins are present (required
for any PD profile above 5V), do NOT say "6 pins / no data pins" loosely — say "the
data pins (D+/D−) are absent." State the true count once you've confirmed it on a unit,
because you're inviting buyers to count.]`

**Specifications**

- USB-C receptacle (charger side) + USB-C plug (device side, on pigtail)
- `[VERIFY POWER: 60W max (20V / 3A) per your GCT 3A part — NOT 100W. If the board
  truly does 100W/5A, your 3A rating is wrong; reconcile before publishing.]`
- Surge protection (TVS diode)  `[confirm present]`
- EMI filter (ferrite bead)  `[confirm present]`
- Reverse-polarity protection (Schottky diode)  `[confirm present]`
- `[VERIFY LEDs: "green = power" is fine if passive/Vbus-driven. "blue = PD negotiated"
  requires a circuit that senses PD — which contradicts "no chips." Either reframe
  honestly (e.g. "blue = high-voltage charging active") or drop it. Tell me the real
  circuit.]`
- Clear epoxy enclosure, no screws — visual verification
- Serial number + QR verification at verifyknot.io
  `[HONEST FRAMING: the record is a manufacturing/lifecycle entry that resolves — it is
  NOT third-party-verifiable provenance today (units are software-signed). Describe it
  as a "registered manufacturing record," never as cryptographic proof.]`
- `[VERIFY PATENT: you pasted App 63/961,118; my record of PAT-001 is 63/960,933.
  Confirm the actual USPTO receipt for the provisional covering PowerVerify before
  printing any number. Do not guess.]`
- Designed in Utah. Hand-assembled by a veteran-owned business (SDVOSB). Made in USA.

**What it does NOT have**

- No data lines. The D+/D− data pins are absent; no data wires in the pigtail; no
  data traces on the board.
- `[CONDITIONAL: "No firmware. No hidden chips." — TRUE only if there is NO integrated
  circuit on the board. If a PD-sense IC or PUF exists, this claim must go. Confirm:
  is there ANY IC on the board?]`
- No cloud dependency. The cable works offline.
- `[REMOVE unless Rev 1 + ceremony has landed: "PUF tamper evident." The live record
  says PUF is deferred; PUF also contradicts "no chips." Not true of the unit today.]`

**Who this is for**

Travelers charging in airports, hotels, and cafés; journalists and researchers
handling sensitive devices; lawyers handling digital evidence; anyone who read an
FBI/FCC/TSA warning about public USB ports and wanted a better answer than "carry
your own brick."

**Who this is not for**

If you just need a charge-only cable for home, a $5 blocker is fine. This is for
people who want to verify, not just trust.

---

## PRICING / FULFILLMENT  `[BLOCKED on the Rev 0-now vs Rev 1-preorder decision]`

> The whole block below depends on which strategy you choose. Two honest versions:

**If shipping Rev 0 NOW (per primer):**
- Price: $39
- Made to order — usually ships in 2–3 business days
- Rev 0 pilot unit; free swap to hardware-attested Rev 1 when it ships
- No "pre-order," no "June 30," no "50-unit batch," no PUF/provenance claims

**If PRE-ORDERING Rev 1 (per your pasted copy):**
- Price: $39 pre-order (regular $49 after launch)  `[confirm $49 is the real planned price]`
- Ships: June 30, 2026  `[only if you can actually build + run the ceremony by then]`
- Limited to first 50 orders (Rev 1 pilot batch)
- Full refund any time before shipping
- Each unit registered at verifyknot.io
- ⚠️ Every Rev 1 claim (PUF, attestation) must be TRUE BY SHIP DATE — if the ceremony
  slips, the listing becomes false. Don't pre-sell a claim you can't guarantee landing.

---

## CONTACT
Email ops@zknot.io or reply to your order confirmation.
ZKNOT, Inc. · verifyknot.io · Veteran-owned · Made in USA
`[patent-pending line: add only after the number is verified]`

---

## DECISIONS THAT UNBLOCK FINAL COPY
1. Rev 0-now or Rev 1-preorder? (unblocks the whole pricing/fulfillment block)
2. Is there ANY integrated circuit on the board? (unblocks the no-chips/PD/PUF lines)
3. Real power rating — 60W or 100W? (one of your numbers is wrong)
4. True pin count, confirmed on a unit
5. Verified patent application number from the USPTO receipt
6. What the LEDs actually indicate
