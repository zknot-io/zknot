# 2026-05-07 — Production Transition: Mold Done, First Pour Underway

**Status:** Crossed from design iteration into production
**Milestone:** First PowerVerify potted units in process

## What just changed

The mold is finalized and printed. After v1 (over-engineered), v2
(simplified, PCB on floor), v3 (rails + plug bump), v4 (geometry conflict
identified), the working mold is now in hand and the first pour is
happening. The 5-day mold iteration cycle is closed.

This is the transition from "designing the product" to "making the
product." Different work, different cadence, different blockers.

## Immediate execution path

Three parallel tracks to complete the first batch of PowerVerify units:

### Track 1: Resin pour cycle
- [ ] Mix the next pot of resin (EpoxAcast 690, 100A:30B by weight)
- [ ] Pour into mold around PV1-00001 (or next provisioned unit)
- [ ] Cure 24h at 73°F under dust cover
- [ ] Demold, trim connector cap, sand connector face
- [ ] PUF photograph and enroll
- [ ] Apply insert card label

### Track 2: Supplies acquisition
- [ ] More zip ties for pigtail strain relief (current stock running low)
- [ ] Shipping materials run:
  - Padded mailers or small boxes (sized for ~100x40x12mm potted unit + insert card)
  - Anti-static bags (or kraft paper for non-ESD-sensitive carry)
  - Tamper-evident packaging seals (Brady or generic VOID labels)
  - Shipping labels (USPS Priority preferred for tracking)
  - Return address stamps if shipping in volume

### Track 3: First units out the door
- [ ] PV1-00001 (ZK-HFZZ-PKZ, chain pos 5) — already provisioned
- [ ] PV1-00002 (ZK-KAMY-T4B, chain pos 6) — already provisioned
- [ ] PV1-00003 (ZK-9CXC-SN9, chain pos 7) — already provisioned
- [ ] PV1-00004 (ZK-SU3W-9ZQ, chain pos 8) — already provisioned
- [ ] PV1-00005 (ZK-3M83-NHZ, chain pos 9) — already provisioned

All five have chain entries minted, sidecar JSONs saved at
`~/zknot-api/labels/`, insert cards generated. Just need:
1. Potting (track 1)
2. Packaging (track 2)
3. Recipient confirmation (who specifically gets each one?)
4. Ship

## What this means for the broader plan

**Heat shrink path:** dead, retired. Photos from 2026-05-06 documented why.

**Conformal coat path:** held in reserve for Rev 2 or as backup if potting
yield is low.

**Potted Rev 1:** active, in production.

**PUF integration:** part of the standard pour going forward
(holographic glitter mixed into resin). Each unit gets unique sparkle
pattern photographed at QC.

## Recipient assignments (TBD — capture before shipping)

The first 5 PowerVerify units are pilot batch. Recipients should be:
- Chosen for good feedback potential (technical, will actually USE the
  device, will report issues)
- Mix of contexts (one investor, one tinkerer, one journalist/influencer,
  one peer security person, one personal friend)
- Get explicit "this is Rev 1, please send feedback" framing

Concrete decision needed: who gets PV1-00001 through PV1-00005?

## Notes on the production cycle now established

Per-unit time (active) post-dial-in:
- Provision + label: 3 min (already done for first 5)
- Mold prep: 5 min (mold release, masking)
- Mix resin: 8 min (weigh, double-cup mix, glitter)
- Pour: 5 min (place PCB, pour, vent bubbles)
- (Cure 24h passive)
- Demold, trim, sand, IPA wipe: 8 min
- PUF photo + enroll: 3 min
- Package: 5 min
- **Total active per unit: ~37 min**

With one mold: 1 unit/day throughput (cure-bound)
With 5 molds: 5 units/day (active-time bound)

For first 75-board batch at 5 units/day = 15 days of pour cycles.
For pre-order scaling, need 3-5 molds and probably a vacuum/pressure
chamber by Friday per Day 5 commitment.

## Loose ends in context

- Shopify listing still says "ships June 30" — must update once first
  units ship
- Shopify product description still says "100W max" — should be "60W max"
  per GCT 3A rating
- verifyknot.io HTML deployed but custom domain config pending Cloudflare
- Backend at api.zknot.io healthy, ZK-LocalChain at position 9
- SDVOSB and VOSB certifications active as of today (separate journal)

## What's next after first 5 ship

Per Day 5 plan:
1. Watch first-week feedback from recipients
2. Build vacuum chamber by Friday
3. Iterate workflow based on actual yield numbers
4. Scale to next 20 units in batch 2
5. Update Shopify listing and remove pre-order language
6. Reddit followup post with attribution to community contributors

Also (per today's certification milestone):
1. Verify NAICS codes in SAM.gov
2. Build capability statement
3. Schedule OSDBU calls (DoD, DHS, GSA)

---

**File commit**: `2026-05-07_production_transition.md`
**Related**: `2026-05-06_mold_handoff.md`, `2026-05-07_sdvosb_vosb_certified.md`
**Tags**: production, milestone, powerverify, rev1

*Physics enforces. Math proves. You verify.*
