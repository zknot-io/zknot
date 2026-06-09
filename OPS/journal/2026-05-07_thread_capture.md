# 2026-05-07 — Thread Capture: Mold Design, SDVOSB, Production, ZKKey Provisioning

**Purpose:** Full capture of a long working thread before deletion. Covers four
distinct workstreams that came up in sequence. Each section is self-contained
so future-you can act without re-reading the original conversation.

---

# PART 1 — PowerVerify Mold Design (v1 → v4 history)

## Context
Heat shrink encapsulation was rejected (photos showed edges don't seal, pocket
gunk would accumulate). Pivoted to potted Rev 1 for all units. Designed a 3D
printed open-cast mold (like a Jell-O mold — one piece, open top, pour resin,
cure 24h, flex to demold). PCB silkscreen-back becomes the exterior face.

## PCB physical specs (confirmed)
- PCB: 90 × 30 × 1.6mm
- USB-C female (GCT USB4135 or equiv): boss 3.4mm above PCB top → connector
  top at 5.0mm from PCB bottom
- Pigtail strain relief / zip tie: 6.4mm below board → 8mm total at that point
- Cable OD: ~4mm
- Connector overhang past PCB edge: ~7.5mm

## Mold iteration history
- **v1**: Over-engineered. Centered PCB on 4 locating posts, side connector
  window, closed cable slot. Cavity 12.6mm deep, ~36mL resin/unit. PROBLEMS
  found at fit-check: posts printed badly (too small for PLA at 2.5mm dia),
  cable can't thread through closed slot (already attached), connector sits
  flush so no window needed.
- **v2**: PCB on floor (silkscreen exposed as exterior), no posts, open-top
  cable channel, no connector window, top_resin_cap 0.2mm. Cavity 5.2mm deep,
  ~13mL resin/unit.
- **v3**: PCB lifted 2mm on thin side rails, male USB-C plug bump on connector
  wall (dams connector + positions it), cable channel 7mm wide. Cavity 8.5mm.
- **v4**: User wanted rails removed, pour gate notches removed, plug bump
  smaller + rounded for easier demold. Geometry conflict surfaced (see below).

## v4 geometry conflict (the thing that stalled it)
User said "PCB should sit on the USB-C lip and cable" (dual anchor). But:
- Plug bump position puts PCB top at z=3.6mm, bottom at z=2.0mm
- Cable channel position puts cable top at z=4.6mm
- For PCB to rest on cable, cable_top must equal pcb_bottom — they don't align
- The two anchors want the PCB at different heights → unresolved

## v5 + cable shim (designed in SEPARATE session, already on disk)
After this thread, a v5 mold + cable shim was designed elsewhere and committed:
- Files: `~/ZKNOT/6_SIG/hw/PowerVerify_Mold_v5.{scad,stl}` and
  `~/ZKNOT/6_SIG/hw/PowerVerify_Cable_Shim.{scad,stl}`
- Journal: `~/ZKNOT/3_OPS/journal/2026-05-07_powerverify_mold_v5.md`
- v5 uses an EXTERNAL sacrificial USB-C plug locating strategy (a real cheap
  USB-C cable end plugs into the female connector, holds it positioned during
  pour, then is broken or razor-cut off after demold)
- This SUPERSEDES the v4 work above. v1-v4 are history; v5 is the live design.

## Potting workflow (still valid regardless of mold version)
Full doc was generated: `POTTING_WORKFLOW.md` covering print settings,
materials, mold release, resin mix (EpoxAcast 690, 100A:30B by weight),
glitter dosing for PUF (~1/8-1/4 tsp holographic fine 0.008" hex per unit),
pour technique, 24h cure, demold, trim connector cap, sand, PUF photo, QC.

Key points:
- Top of resin (open mold top) cures glassy against air — that's the nice face
- Sides/bottom take mold texture — use XTC-3D coating or sand+polish for finish
- USB-C dummy plugs prevent resin wicking into connector during pour
- Vacuum/pressure chamber removes bubbles (build/buy by Friday — Day 5 commit)

## Surface finish options (user asked about smoothness)
1. Print at 0.08-0.16mm layer (slower, smoother walls)
2. Sand mold interior 400→800→1200 grit before use
3. Polish mold interior with Meguiar's PlastX
4. **XTC-3D coating on mold interior (~$30, best result, recommended)**
5. Buff each cured unit individually (most labor)

---

# PART 2 — SDVOSB + VOSB Certification (granted today)

## The milestone
ZKNOT, INC. certified by SBA as both:
- **SDVOSB** (Service-Disabled Veteran-Owned Small Business)
- **VOSB** (Veteran-Owned Small Business)
- Entrance date: 2026-05-07
- Renewal date: 2029-05-06
- Source: SBA VetCert

## Why it matters (current as of 2026)
- Federal goal is now 5% of all contract dollars to SDVOSB (up from 3% per
  FY2024 NDAA)
- FY2025: $28.6B awarded to SDVOSBs across ~52,000 contract actions
- Certification mandatory since Dec 22, 2024 (self-cert is dead)
- Sole-source authority up to $5M for SDVOSB (services + manufacturing)
- Agencies missing 5% goal must file corrective action reports → pull demand

## Full federal stack now complete
- SAM.gov: active, UEI C4SKW13JPEL5, CAGE 1AHZ4, renewal 2027-03-17
- EIN: 36-5165991
- SDVOSB + VOSB: certified
- This is the complete entry-level federal contracting stack

## Strategic guide highlights (full doc: SDVOSB_STRATEGIC_GUIDE.md)
Phase 1 (this week):
- Verify/expand NAICS codes in SAM.gov (likely: 334418 PCB assembly primary,
  plus 334417, 334419, 541512, 541330, 541715, 561621)
- Build 1-page capability statement (UEI, CAGE, certs, NAICS, contact)
- Update DSBS profile at sbs.sba.gov (keywords are how COs find you)
- Add "SDVOSB | VOSB" to email signature + Shopify

Phase 2 (this month) — targeting:
- Tier 1: DoD, DIU, DARPA, AFWERX, DHS/CISA, DOE, IC
- SBIR/STTR is the BEST fit (no past performance needed, $50-275K Phase I,
  SDVOSB preference points). Browse sbir.gov for hardware supply chain /
  anti-counterfeit / hardware root of trust topics.
- GSA Schedule is year-2 (needs ~$100K+ commercial sales history first)
- Mentor-Protégé Program is year-2 (JV exemption from affiliation — major lever)

Phase 3 (this quarter) — outreach:
- OSDBU calls (DoD, DHS, GSA) — free government employees paid to help you win
- NVSBE (National Veterans Small Business Engagement) — biggest matchmaking event
- Capability statement send to OSDBUs + COs of expiring contracts in your NAICS

Risk: equity dilution. Must preserve 51%+ veteran ownership AND control through
any fundraise. Investor veto rights over operations can violate "control" even
if ownership stays >51%. Get federal contracting attorney review of every term
sheet (~$1-2K each).

## ZKNOT-specific opportunity flags
DoD DMSMS (supply chain provenance), CHIPS Act follow-on (supply chain
integrity), Sec 889 enforcement (verifiable supply chain alternatives), DARPA
SHIELD legacy (hardware root of trust), NIST PQC migration.

---

# PART 3 — Production Transition (PowerVerify first units)

## State
"The pot is done" — crossed from design into production.

## First 5 units (all provisioned, on chain)
| SN | Short code | Chain pos | Artifact ID |
|---|---|---|---|
| PV1-00001 | ZK-HFZZ-PKZ | 5 | (from Day 4) |
| PV1-00002 | ZK-KAMY-T4B | 6 | 8399ef67... |
| PV1-00003 | ZK-9CXC-SN9 | 7 | 55a1784f-7021-4253-924f-fd65549c910a |
| PV1-00004 | ZK-SU3W-9ZQ | 8 | ec930953-e21c-47a4-8710-aed5436a7340 |
| PV1-00005 | ZK-3M83-NHZ | 9 | 734228ef-26b9-4b73-a6f6-dd218ce3abc8 |

Sidecar JSONs: `~/zknot-api/labels/PV1-0000{1..5}_unit.json`
Insert cards: printed for all 5
Under-shrink labels: working (after sed fix — label_size "62red", red=True)

## Three tracks to finish first batch
1. **Pour cycle**: mix EpoxAcast 690 + glitter, pour each unit, 24h cure,
   demold, trim sacrificial plug, sand, PUF photo + enroll
2. **Supplies**: zip ties, padded mailers, anti-static bags, tamper seals,
   sacrificial USB-C cables (1/pour), USPS Priority labels
3. **Ship**: decide recipients (5 names+addresses), QC scan QR, continuity
   test, package with insert cards + tamper seals, ship

## Taskwarrior state (tasks 72-79 added today for v5 workflow)
- 72: Slice and print mold v5 (H)
- 73: Print 3x cable shim spares (M)
- 74: Dry-fit PCB in v5 + shim (H, depends 72,73)
- 75: Water test seal before pour (H, depends 74)
- 76: First epoxy pour PV1-00001 (H, depends 75 + should add 79)
- 77: Test sacrificial plug release method (M, depends 76)
- 78: Decide PCB orientation in pot (M)
- 79: Source sacrificial USB-C cables (M, zknot.ops, cost 20)

NOTE: earlier dependency command tried `depends:81` but 81 doesn't exist.
Should be `task 76 modify depends:75,79`.

Incremental tasks generated this thread (supplies, pours 2-5, recipients,
QC, ship, Shopify updates) — in `incremental_production_tasks.sh` if saved,
otherwise re-derive from the three-tracks list above.

## Loose ends
- Shopify still says "ships June 30" — update after first ship
- Shopify says "100W max" — should be "60W max" (GCT 3A rating)
- verifyknot.io custom domain Cloudflare config pending
- Recipient list for first 5 units — NOT decided yet

## Recipient strategy (when deciding)
Mix: 1-2 technical reviewers (will report bugs), 1 with reach (journalist/
infosec personality), 1 investor (premium impression), 1 personal connection.
Frame all as "Rev 1 pilot, please send feedback."

---

# PART 4 — ZKKey Connect Pico Provisioning (in progress, paused for trip)

## Hardware decisions (locked, from May 11 session)
- Plain Pico (RP2040, no wireless — minimize attack surface on signing device)
- SSD1306 0.96" OLED (I2C, shares bus with ATECC at 0x3C; ATECC at 0x60)
- ATECC608B (NOT 608A — current production silicon, matches SW-001 schema)
- CircuitPython shipping firmware for v1
- Form factor: bare ATECC608B SOIC-8 on perfboard (hidden in sealed case =
  the actual security story; breakout with labeled pins tells attacker where
  to probe)

## Wiring (to verify before provisioning)
- VCC → 3V3
- GND → GND
- SDA → GP4
- SCL → GP5
- Pullups: Pico has internal weak pullups; ATECC has internal. External 4.7k
  to 3V3 recommended for reliability but test without first.

## Provisioning flow (the 9 phases — NOT YET EXECUTED)
1. I2C scan, verify ATECC608B at 0x60 (zero risk)
2. Read-only inspection — serial number, config zone state, slot configs (zero risk)
3. Slot configuration design:
   - Slot 0: Primary ECC P256 signing key (private, never leaves chip)
   - Slot 8: Backup signing key (optional)
   - Slot 10-12: Trust anchor public keys
   - Slot 14-15: Counter/diversification
4. Write config zone (reversible until locked)
5. ⚠️ LOCK CONFIG ZONE (IRREVERSIBLE) — pause + confirm before executing
6. Generate ECC P256 keypair in slot 0 (chip rolls own private key)
7. ⚠️ LOCK DATA ZONE (IRREVERSIBLE) — pause + confirm before executing
8. Export public key + register with api.zknot.io device enrollment
9. Sign test challenge, verify with public key (proves end-to-end)

~45 min total. Two irreversible LockBytes operations — no factory reset exists.

## Critical safety notes for when resuming
- If multiple ATECC608B chips available: provision a SACRIFICIAL bench chip
  FIRST, walk the whole flow, THEN provision production chip
- If only one chip: go slow, confirm twice before each lock
- Use RAW I2C via busio + helper functions, NOT adafruit_atecc library
  (Adafruit lib defaults to their slot config which doesn't match ZKNOT
  schema; raw I2C is auditable for patent-defensibility)
- Plan: write minimal `zknot_atecc.py` CircuitPython module (~400 lines, no
  unauditable dependencies)

## Where this was paused
Was about to confirm: Pico firmware state, USB connection, wiring pinout —
then write the provisioning module and walk through phases 1-2 (zero-risk
inspection) before any writes. Trip interrupted before execution.

## Related task
Task 60: "Provision ATECC608 chips on ZKKey Connect Pico" (urgency ~17.8,
project zkkey-connect, workstream fw)

---

# RESUME CHECKLIST (after trip)

PowerVerify production:
- [ ] Print mold v5 + 3x cable shims (tasks 72, 73)
- [ ] Source sacrificial USB-C cables (task 79)
- [ ] Fix dependency: `task 76 modify depends:75,79`
- [ ] Buy zip ties, mailers, anti-static bags, tamper seals
- [ ] Decide 5 pilot recipients
- [ ] Dry-fit → water test → pour PV1-00001 → cure → demold → PUF → ship

SDVOSB (highest leverage):
- [ ] Verify NAICS codes in SAM.gov (10 min, free)
- [ ] Build capability statement (1-page PDF)
- [ ] Update DSBS profile
- [ ] Schedule OSDBU calls (DoD, DHS, GSA)
- [ ] Identify 5 SBIR Phase I topics

ZKKey provisioning:
- [ ] Confirm Pico CircuitPython + wiring
- [ ] Write zknot_atecc.py raw-I2C module
- [ ] Phases 1-2 inspection (zero risk)
- [ ] Sacrificial chip dry run if available
- [ ] Production provision with double-confirm on locks

---

**Tags:** capture, mold, sdvosb, production, zkkey, provisioning
**Related journals:** 2026-05-07_powerverify_mold_v5.md,
2026-05-07_sdvosb_vosb_certified.md, 2026-05-06_rev2_observations.md,
2026-05-06_mold_handoff.md

*Physics enforces. Math proves. You verify.*
