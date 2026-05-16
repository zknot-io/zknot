# 2026-05-16 — Finishing Workstation Buildout + Graip Strategy + Coatings

## Summary

Decided finishing workstation setup for potted PV1 units. Selected Griot's G8
Mini Random Orbital Polisher (3" / 2") as the primary tool. Explored Graip
consumer line as offshoot brand for visible-trust consumer hardware.
Identified zknot.org as future educational/public-interest layer. Investigated
protective coatings for finished units; settled on ceramic-coat approach
once volume justifies it.

## Finishing Workstation — Final Spec

**Decision:** Griot's G8 Mini Random Orbital + manual wet-sand stages.

Considered and rejected:
  - DeWalt 20V cordless polisher (DCM848 5") — too large for PV1 form factor
    despite battery ecosystem fit. DeWalt has no <5" 20V polisher.
  - Pneumatic 3" tools — would have required compressor purchase, more
    setup complexity for marginal benefit
  - Dremel + flex shaft — saved for later if parts shrink (Graip line, etc.)
  - Griot's G9 / GR3 rotary — wrong size/type for clear epoxy

**Tools/consumables ordered (~$327):**
  - Griot's G8 Polisher (model 10908) — $145
  - Griot's BOSS 2" Conversion Kit — $45
  - Lake Country 3.5" HDO 3-pack (cut/polish/finish) — $31
  - Lake Country 3.5" SDO 3-pack (gentler set) — $21
  - 3M Trizact P3000 foam discs 3" (15ct) — $37
  - BAISDY 45-pc sandpaper assortment (400-3000 grit) — $9
  - Novus #1 Plastic Clean & Shine — $11
  - Novus #2 Fine Scratch Remover — $12
  - Menzerna SF3800 Final Polish — $16

**Workflow per unit (target 5 min):**
  1. Wet-sand by hand: 400 -> 600 -> 800 -> 1000 -> 1500 -> 2000 -> 3000
     (distilled water + dish soap as lubricant)
  2. G8 with cutting pad + Novus #2 (speed 2-3, 20 sec/face)
  3. G8 with finishing pad + Menzerna SF3800 (speed 2-3, 20 sec/face)
  4. Hand wipe with Novus #1 on microfiber

**Critical operating constraint:** Never exceed G8 speed 4. Cured epoxy
softens around 140F. Heat = haze = ruined unit. If part warms to touch,
stop, cool, continue.

## Protective Coatings Research

Investigated post-polish coatings for in-field durability. Three categories:

1. **Ceramic coating (SiO2-based, e.g. Cerakote, CG HydroSlick):**
   - 1-3 micron transparent hydrophobic film
   - Preserves visual inspectability (no patent/tamper-evidence concern)
   - Lasts 1-3 years, repairable by re-application
   - Adds one 12-24 hr cure step
   - **DECISION: Plan to adopt for production once volume warrants.**
     Skip for first 10-20 units to gather real-world wear data first.

2. **Flood coat (second thin pour of casting epoxy):**
   - REJECTED. Creates layered structure that weakens tamper-evidence
     claim. Attacker could dissolve outer layer, manipulate internals,
     re-pour. Conflicts with monolithic-encapsulation patent claim.

3. **Hard polyurethane clear (2K automotive clear coat):**
   - REJECTED. Same tamper-evidence concern as flood coat. Plus
     application is harder, smelly, can yellow over time.

## Graip / Consumer Line — Strategic Notes

Discussed possibility of consumer-facing "Graip" / "drip" line as a
viral-aesthetic offshoot. Key strategic points captured for later:

**Three-layer brand architecture (potential):**
  - ZKNOT Inc. — enterprise, patents, attestation (current)
  - Graip — consumer culture, drip line, viral (new exploration)
  - zknot.org — educational bridge, trust literacy (planned)

**Graip line product concept:**
  - Fruit-themed translucent potting variants
    (Kiwi green, Strawberry, Grape purple, Mango, Glacier blue)
  - Controlled limited drops, not infinite customization
  - Serialized within each batch
  - Optional internal LED (status only, no implied real-time monitoring)
  - Premium boutique-electronics aesthetic, NOT toy/vape-shop look

**Marketing positioning principles:**
  - "Visibly trustworthy object" framing
  - "Understand power vs data" educational hook
  - AVOID: fear marketing, "impossible to hack," "no one can spy on you"
  - AVOID: marketing-to-minors framing without legal review
  - SAFE: "Reduces data exposure risk from unknown USB ports"
  - SAFE: "Physically inspectable power-only architecture"

**Legal flags identified:**
  - Marketing to teens/college kids needs lawyer review before launch
    (privacy framing, parental implications, COPPA if any data collection)
  - Every marketing claim must pass the strict-language filter
    ("reduces" not "prevents", "designed to" not "guaranteed to")
  - LED status indication is fine for "power flowing" but cannot imply
    real-time threat detection the hardware doesn't actually do

## Patent / Tamper-Evidence Reinforced

The decision tree on protective coatings reinforced the importance of the
monolithic-cast structure as a core patent + trust claim:
  - Single-pour epoxy cannot be opened and re-closed without visible damage
  - Any multi-layer approach (flood coats, removable shells) weakens this
  - Ceramic coatings work BECAUSE they're cosmetic, not structural

This is worth documenting in the patent file as a design decision rationale.

## Open Questions

  1. At what unit volume does ceramic coating become production-default?
     Probably ~50/month threshold.
  2. Should there be a "PowerVerify Renewal" service where users mail
     units back for re-polish + ceramic? Could be a recurring revenue
     stream and trust-touchpoint.
  3. Graip line: should it use the same PV1 PCB or a smaller dedicated
     board? Affects whether it's truly an offshoot or a separate product
     line with its own BOM.
  4. zknot.org: register domain now (hold), but defer content build
     until enterprise side has more bandwidth.

## Next Concrete Actions

  - Ship Amazon cart ($327)
  - Practice workflow on the failed-USB-C unit from last pour batch
  - Photograph polish-progression before/after for marketing assets
  - Register zknot.org (defer build)
  - Sketch one Graip prototype: Kiwi green translucent epoxy, single PV1
    PCB, see if aesthetic reads as "premium boutique" vs "AliExpress toy"
