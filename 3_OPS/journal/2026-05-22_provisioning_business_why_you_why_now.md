# SE Provisioning Business — "Why You, Why Now" Deep-Dive

**Date:** 2026-05-22
**Author:** William Shane Wilkinson
**Source:** Deep-dive thread off HANDOFF_secure_element_provisioning_business_opportunity.md (2026-05-12)
**Status:** Working notes. Thread deleted after capture. Pick up at "Next actions."

---

## Purpose of this entry

Captured the full reasoning from a thread that stress-tested the provisioning-fixture
business thesis, focused on sharpening the "why you, why now" narrative for investors
and SBA. The handoff doc itself is unchanged; this is the analysis layer on top of it.

---

## Key finding #1: The handoff doc does NOT yet have a defensible "why you, why now"

Part 9 of the handoff reads like a *competency* claim ("I've felt the pain") rather than
an *unfair-advantage* claim ("I can capture this in a way others can't"). Investors and
SBA loan officers hear the difference immediately. Three specific failure modes:

- **Pain experience != unfair advantage.** Having struggled with every provisioning
  method shows competence, not a moat. A funded engineer catches up in ~90 days.
- **SDVOSB is a license, not a moat.** ~13,000 SDVOSBs in SAM. It gets you in the room
  for set-asides; it doesn't keep other SDVOSBs out. Wrong question is "why does SDVOSB
  matter" — right question is "why am I the right SDVOSB for THIS opportunity."
- **Adjacent product lines are listed but not connected.** PowerVerify / ZKKey /
  verifyknot.io / patent are bullets in Part 9, mentioned once in Part 4, never tied to
  *why they make winning provisioning more likely.* That connection is the real wedge and
  it's currently buried.

## Key finding #2: The biggest unexamined assumption is in the Part 3 gap table

The gap table conflates TWO different gaps into one product:

- **Gap A** — small/mid commercial hardware cos who want better than Method 1/2 but can't
  afford Method 6. Real, but price-sensitive and don't need SDVOSB sourcing.
- **Gap B** — federal procurement that wants Method 6 assurance but needs SDVOSB sourcing
  + faster delivery. Real, but small buyer count, and "FIPS-pathway-not-certified" may not
  clear the bar.

These are different products: different price points, different sales motions, probably
different fixtures. Part 4 implicitly assumes one product serves both. **This is the
assumption to put the most pressure on.** It recurs in Part 7 risk #2 (TAM ambiguity) and
Part 8 Q6 (first customer).

---

## The "why now" — CONFIRMED via web research (this is the strong version)

Not the generic EO 14028 / NDAA 848 tailwind everyone cites. The specific dated cliff:

- **CMMC 2.0 48 CFR rule became legally enforceable Nov 10, 2025** — DFARS clause
  252.204-7021 now inserted into DoD solicitations. As of this writing (May 2026), buyers
  are *currently* receiving clauses they have no off-the-shelf answer for.
- **Phase 2 cliff: Nov 10, 2026** — requires third-party (C3PAO) CMMC Level 2
  certification for most contractors handling CUI. ~6 months out from now.
- **Mandatory flowdown** — primes must flow CMMC down to all subcontractors/suppliers that
  process/store/transmit FCI or CUI on their own systems. This is the mechanism that pushes
  the pain from primes (who have compliance teams) down to small hardware suppliers (who
  don't). COTS items excluded from flowdown — worth noting as a possible scoping gap.

**One-sentence why-now:** CMMC 2.0 became enforceable Nov 10 2025; the Phase 2 cert cliff
hits Nov 10 2026; small/mid hardware suppliers are getting flowdown clauses right now with
no SDVOSB vendor selling them a solution. 6–18 month window.

---

## The rebuilt "why you" narrative — three layers (hardest to copy last)

1. **Customer gravity, not customer acquisition.** ZKNOT already ships verification
   products into the evidentiary attestation space — adjacent to the federal
   hardware-identity buyer. The fixture closes the trust loop on devices ZKNOT already
   sells. A fresh competitor starts at customer zero; ZKNOT starts at customer *current.*
   THIS NEEDS TO MOVE TO THE FRONT and get 3 paragraphs, not 1 bullet.
   **CAVEAT (see open risks): this claim only holds if PowerVerify/ZKKey are actually in
   customer hands. If pre-revenue prototypes, this weakens hard.**

2. **Protocol-depth credibility, not feature-list credibility.** Documented the specific
   failure modes that defeat existing methods: Adafruit CryptoAuthLib CRC failure on
   64-byte responses; irreversible lock_all_zones() that bricked Demo Unit #1
   (0123B77FB2B77F92EE); TPDS prototype-tier limits. 6+ months of expensive engineering for
   a competitor to reproduce, and most won't (they'll buy the vendor story). Tied to
   provisional App # 63/960,933.

3. **SDVOSB + USA assembly + TAA-eligible silicon.** The procurement license. Lower
   set-aside competition, sole-source up to $4M/agency, VA Vets First. State briefly,
   do NOT lead with it.

**Why defensible / exit story (most pitches skip this):** Acquisition logic isn't "we got
big." It's "a prime or hardware-security incumbent buys us because we're the
SDVOSB-certified door into a procurement channel they can't enter directly." Primes pay
premiums for SDVOSBs with shipping product + patent posture. Known exit pattern (SDVOSB
cyber acquisition wave 2022–2024 — VERIFY comparables before citing).

---

## Pushback to expect (and current weak answers)

- **SBA loan officer:** "Repayment plan if federal procurement doesn't materialize in 12mo?"
  Need a commercial fallback (bodycam/drone vendors, Part 4) with >=1 named conversation in
  progress. Not a sale — a conversation.
- **Angel:** "Why doesn't Microchip collapse this in 18mo with a production-grade TPDS?"
  Answer: (a) 5 years and haven't; (b) incentive is to keep customers on high-margin
  Trust&GO/TrustFLEX, not enable 3rd-party provisioning; (c) even if they ship it, they're
  not SDVOSB and never will be. Defensible but NOT in current doc.
- **Sophisticated investor:** "Provisional from 2025 — what's the actual defensible claim?"
  Must answer without flinching. If it's a defensive filing w/o strong novelty, SAY SO.
  Patents are not the moat — customer gravity is.
- **Honest stress-test:** strongest "why you" = "shipping product in the adjacent space."
  If PowerVerify/ZKKey are pre-revenue prototypes, characterize them accurately. Investors
  will dig.

---

## Tasks I can offload to real life (don't burn AI tokens on these)

- **SBIR pipeline (Part 8 Q2):** sbir.gov, ~15 min. Search "secure element provisioning,"
  "hardware root of trust," "device attestation," "secure boot provisioning." Filter Phase I
  awards 2023–2026. Gives DoD topic numbers + awardees + amounts.
- **SDVOSB competitor scan (Part 8 Q3):** SAM.gov dynamic search, NAICS 541512 / 541330 /
  334413, filter SDVOSB. Definitive list vs. my partial one.
- **Customer discovery:** the 10-vs-10,000 TAM question (Part 7 risk #2) only resolves via
  5–10 PM conversations at bodycam/drone/sensor vendors. Can't be researched.

## Where AI is actually useful next

- One-page "why you / why now" section to replace Part 9 (cheap once claims verified)
- Tighter 3-paragraph investor cold-outreach version
- SBA-loan-officer version emphasizing commercial fallback + cash flow
- FIPS 140-3 pathway + cost map (~$200K–500K, 12–18mo per handoff Part 7)
- SBIR Phase I pitch structure against a real solicitation

---

## Next actions (in order)

1. **VERIFY the load-bearing claims before any drafting:**
   - Actual commercial/shipping status of PowerVerify Rev 1 and ZKKey (units in hands? or
     prototypes?). The whole "customer gravity" wedge rests on this.
   - What App # 63/960,933 actually claims (strong novelty vs. defensive filing).
2. Run the two real-life searches above (SBIR + SDVOSB scan) before next AI session.
3. Line up >=1 commercial-fallback customer conversation (bodycam/drone/sensor PM).
4. THEN draft the Part 9 replacement + investor/SBA versions.
5. Resolve the Gap A vs Gap B product split — decide which is the actual v1 product.

## Open question to carry forward

Is provisioning a *standalone* product or the *trust anchor* that unifies the existing
ZKNOT line (PowerVerify, ZKKey, verifyknot.io)? Handoff Part 8 Q7 raised it; thread didn't
resolve it. The answer probably determines whether this is a new business or a feature of
the existing one — and that changes the entire pitch.
