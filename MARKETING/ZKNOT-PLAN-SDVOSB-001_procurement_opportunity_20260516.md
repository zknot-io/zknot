# ZKNOT SDVOSB Procurement & Opportunity Reference

**Document ID:** ZKNOT-PLAN-SDVOSB-001
**Author:** William Shane Wilkinson
**Created:** 2026-05-16
**Workstream:** ops / gov
**Status:** Active reference doc
**Review trigger:** Monthly or on major opportunity (SBIR window, surplus listing, certification change)
**Related docs:**
- ZKNOT-PLAN-INFRA-001 (infrastructure buildout, references SDVOSB surplus channels)
**Page 1 of 7**

---

## Executive summary

ZKNOT, INC. holds active SDVOSB certification through SBA VetCert (early May 2026).
This certification opens federal procurement, surplus, and set-aside opportunities
that are not available to non-certified small businesses. This doc tracks:

1. **Active certifications and registrations** (and their renewal dates)
2. **Procurement channels** (set-aside contracts, GSA paths, agency direct)
3. **Surplus equipment channels** (free/cheap infrastructure)
4. **Outreach and relationship targets**
5. **Compliance maintenance** (registrations that lapse will silently kill opportunity)

**Operating principle:** SDVOSB certification is a force multiplier, not a free
pass. Federal customers buy from SDVOSBs who can deliver. ZKNOT must continue
shipping PV1 and building the capability story in parallel with procurement work.

---

## Section 1 — Active certifications and registrations

| Item | Status | Identifier | Renewal due |
|---|---|---|---|
| Legal entity | Active | ZKNOT, INC. | — |
| EIN | Issued | 36-5165991 | — |
| SAM.gov registration | Active | UEI: C4SKW13JPEL5, CAGE: 1AHZ4 | 2027-03-17 |
| SDVOSB (SBA VetCert) | Active | Certified early May 2026 | 3 years from cert date (~2029-05) |
| State of Utah business | Confirm | TBD | TBD — verify |
| GSAXcess.gov | Registered (T#85) | — | — |
| Utah State Surplus | Registered (T#86) | — | — |

### Critical renewal dates

- **SAM.gov: 2027-03-17.** Lapsing this kills all federal contracting. Set 60-day and 30-day warnings.
- **SDVOSB VetCert: ~2029-05.** 3-year cycle. Reverification required.

### Documents to keep current in `~/ZKNOT/9_GOV/federal/`

- SAM.gov registration certificate (PDF)
- SDVOSB certification letter
- DD-214 (proof of service for veteran status)
- VA service-connected disability rating documentation
- Business formation docs (articles, EIN letter)
- Capability statement (PDF, max 1 page, updated quarterly)
- Past performance summary (when PV1 customer ships)

---

**Page 2 of 7**

## Section 2 — Procurement channels (selling to government)

### 2.1 — SDVOSB-specific set-asides

**Federal Acquisition Regulation (FAR) 19.14 and VA 38 U.S.C. 8127:**
- VA must consider SDVOSB set-asides FIRST for purchases >$25K (the "Vets First" / Kingdomware rule)
- Other agencies may set aside contracts up to ~$5M for SDVOSBs
- Sole-source SDVOSB awards possible up to $5M for products, $7M for manufacturing

**Target NAICS codes for ZKNOT:**
- **541330** — Engineering Services (broad fallback)
- **541512** — Computer Systems Design Services
- **541715** — Research and Development in the Physical/Engineering Sciences
- **334290** — Other Communications Equipment Manufacturing
- **334418** — Printed Circuit Assembly Manufacturing
- **541380** — Testing Laboratories
- **541990** — Other Professional, Scientific, Technical Services

Verify in SAM.gov that all relevant NAICS are claimed. Each NAICS has a small-business
size standard; confirm ZKNOT qualifies on all claimed codes.

### 2.2 — GSA Schedule path

**GSA Multiple Award Schedule (MAS), IT Category** — long-term contract that lets
agencies buy from your catalog without competing the contract.

- **Pros:** Pre-negotiated, agencies prefer it for speed
- **Cons:** Application is ~6 months of paperwork, requires past performance
- **Recommendation:** Defer until 1-2 PV1 sales completed. Past performance is required.

**Active event:** Intro to GSA, May 27, Layton UT (in-person + virtual). Registered? Verify.

### 2.3 — SBIR / STTR (the most realistic near-term play)

**Small Business Innovation Research:**
- Phase 1: $50K–$300K, 6 months, feasibility
- Phase 2: $500K–$2M, 24 months, prototype/development
- Phase 3: commercialization, no specific funding cap

**Target agencies for ZKNOT:**
- **DoD (Army, Navy, Air Force, DARPA)** — supply chain authentication, anti-counterfeit
- **DHS S&T** — border, customs, port security authentication
- **DOE** — grid component authentication
- **NIH** — medical device anti-counterfeit
- **DoT** — vehicle parts authentication

**Open topics to watch:**
- DoD Phase 1 — quarterly open topics, search at https://www.dodsbirsttr.mil/
- DARPA Open BAA — continuous
- AFWERX — Air Force, fast-track topics

**Action:** Monthly check of open SBIR topics. Add as Taskwarrior recurring task.

### 2.4 — APEX Accelerator (Utah)

Already engaged with Sara Ortiz at Utah APEX. Provides:
- Free counseling on federal contracting
- Event notifications (already receiving)
- GSA training (May 27 event)
- Bid match service (saved searches for opportunities)

**Action:** Confirm bid match search profile is current. Targeted NAICS, set-asides, geographic scope.

### 2.5 — Direct agency outreach

- **VA OSDBU ICF Session** — May 28, 3:30–4:30 PM MT (already calendared)
- **MICC APBI** — May 18–22 (Army contracting overview)
- **Agency-specific Office of Small and Disadvantaged Business Utilization (OSDBU)** contacts

Each OSDBU office wants to meet with SDVOSBs. They're the gateway to programs.

---

**Page 3 of 7**

## Section 3 — Surplus equipment channels (acquiring infrastructure)

### 3.1 — GSAXcess.gov (federal property to eligible recipients)

**Status:** Registered (T#85 done).

**What's available:**
- Computers, monitors, networking equipment, furniture
- Vehicles (rarely useful for ZKNOT)
- Lab/test equipment

**How it works:**
- Agencies post excess property
- Eligible recipients (SDVOSB qualifies for some categories) request
- First-come, first-served within recipient priority

**Cost:** Property itself is free. Recipient pays shipping/pickup.

**Recommended targets:**
- Rackmount servers (Dell PowerEdge, HPE ProLiant)
- Rack-mount UPS (APC SmartUPS 1500/2200/3000)
- Network switches (Cisco/Juniper enterprise)
- NAS chassis (Dell PowerVault, NetApp shelves)
- Test equipment (oscilloscopes, multimeters, power supplies)

**Caveat:** Lots are usually large. May get 1 thing or 50 things. Coordinate pickup.

### 3.2 — GovPlanet / DLA Disposition Services (auction-based)

**Status:** Need to register and set saved searches (Phase 2 task in infra doc).

**What's available:**
- Same as GSAXcess but auction-priced
- More variety, including consumer-grade gear

**Pros:**
- No eligibility restriction beyond having a business
- Prices often very low (UPS $50–200, server $200–500)

**Cons:**
- Auction = uncertainty
- Often Eastern US locations, shipping costs add up
- Sold as-is, no warranty

**Recommended saved searches:**
1. "APC SmartUPS" — set max bid, alert on new listings
2. "Dell PowerVault" or "HP D3xxx" — NAS/JBOD chassis
3. "Rackmount server" with location filter (Utah/CO/NV/AZ)
4. "Network rack" — for future rack-mounted setup

### 3.3 — Utah State Surplus

**Status:** Registered (T#86 done).

**What's available:**
- State agency surplus (often education and DOT)
- Lower volume than federal, but Utah-local pickup

**Specific to Utah-based SDVOSB:**
- Veteran-owned small business sometimes gets priority
- Department of Veterans and Military Affairs may have direct programs

**Action:** Monthly visit to surplus.utah.gov, check listings.

### 3.4 — Local: SLC area government / school surplus

- Salt Lake County surplus auctions
- University of Utah surplus (chunks of lab equipment when grants close)
- Utah Tech / SLCC surplus
- LDS Hospital / Intermountain (occasionally)

**Action:** Set quarterly check, build relationships with surplus managers.

### 3.5 — DLA / Military base direct disposal

Hill Air Force Base in Utah is a major DoD installation with ongoing IT refresh:
- Direct contact with DLA Disposition Services at Hill AFB
- Possibility of preferred SDVOSB pickup arrangements

**Action:** Research contact path. APEX Accelerator can help broker introduction.

---

**Page 4 of 7**

## Section 4 — Outreach and relationship targets

### 4.1 — Active outreach (in flight)

From Taskwarrior T#8 and T#48: 8 named acquirer targets (project: acquisition).
This is separate from procurement outreach — these are acquisition/exit targets.

### 4.2 — Procurement outreach targets (new — to develop)

**VA OSDBU and VA medical centers (Salt Lake VA):**
- VA buys hardware authentication and supply chain verification
- SLC VA Medical Center is local
- Action: cold outreach via OSDBU, attend the May 28 ICF session

**DoD Small Business Program Offices:**
- Hill AFB SBPO (local)
- Army Contracting Command - Aberdeen
- Naval Information Warfare Center
- AFWERX

**Civilian agencies aligned with ZKNOT mission:**
- DHS Science and Technology Directorate
- NIST (especially for cryptographic standards alignment)
- USPTO (interesting — IP authentication)
- Food and Drug Administration (pharmaceutical anti-counterfeit)

**Federally Funded Research and Development Centers (FFRDCs):**
- MITRE Corp
- Aerospace Corp
- Sandia National Labs (closer to ZKNOT mission than most)

### 4.3 — Named individuals in pipeline

From userMemories: outreach campaign targeting individuals named Green, Schneier,
and Pfefferkorn. Not certain if these are procurement targets or technical/legal
contacts. **Action:** Clarify in Taskwarrior — are these procurement, advisory, or legal?

### 4.4 — Capability statement requirements

A 1-page capability statement is the universal currency of federal SDVOSB outreach.
Must include:

- Company name, UEI, CAGE, EIN
- SDVOSB certification info
- NAICS codes
- Core capabilities (3-5 bullets, specific not generic)
- Past performance (when available — PV1 deliveries become this)
- Differentiators (PUF authentication, cryptographic provenance)
- Contact info

**Action:** Draft v1 by end of June. Keep updated quarterly.

---

**Page 5 of 7**

## Section 5 — Compliance maintenance calendar

### Annual

- **SAM.gov renewal:** 2027-03-17 (set 60-day, 30-day, 7-day reminders)
- **Capability statement refresh** (quarterly is ideal, annually minimum)
- **NAICS code review** in SAM.gov — confirm all relevant codes claimed
- **Past performance record update** — add each shipped customer

### Triennial

- **SDVOSB reverification through SBA VetCert** (~2029-05)
- **Patent prosecution milestones** (separate from this doc, in zknot.patents)

### Monthly

- Check open SBIR topics across target agencies
- Check Utah State Surplus listings
- Review GovPlanet saved searches for new listings
- APEX Accelerator event review

### Weekly (or as alerts arrive)

- APEX bid match results
- GovPlanet auction alerts
- SAM.gov contract opportunities matching saved searches

### When something significant changes

- New employee hire (impacts size standard compliance)
- Revenue threshold change (impacts small business size standard)
- New NAICS code applicable to ZKNOT capability
- Address change (must update SAM.gov within 30 days)
- Ownership change (could affect SDVOSB status)

---

**Page 6 of 7**

## Section 6 — Risk and considerations

### 6.1 — SDVOSB certification risks

**What could revoke SDVOSB status:**
- Loss of veteran ownership (51% must remain veteran-owned)
- Loss of veteran control (day-to-day operations by non-veteran)
- Size standard exceeded for claimed NAICS codes
- Material misrepresentation in application

**Mitigation:** Annual self-review. Document ownership clearly in JAG/CORPORATE/.

### 6.2 — Federal contracting risks

**Cybersecurity Maturity Model Certification (CMMC) 2.0:**
- DoD contracts increasingly require CMMC Level 1 or 2
- Level 1: Basic safeguarding of Federal Contract Information (FCI)
- Level 2: Protection of Controlled Unclassified Information (CUI)
- ZKNOT will need at least Level 1 for most DoD work
- Self-assessment route exists for Level 1 (cheaper)
- **Action:** Plan CMMC Level 1 self-assessment by end of 2026

**Defense Federal Acquisition Regulation Supplement (DFARS) 252.204-7012:**
- Required for any DoD contract involving CUI
- Mandates NIST SP 800-171 compliance
- 110 security controls; partial overlap with CMMC

**Buy American Act / Trade Agreements Act:**
- Federal contracts often require US-made components
- ZKNOT must track country of origin for PCBs, components, assembly
- JLCPCB (China) is fine for prototypes, but production for federal may need US fab

### 6.3 — Past performance gap

ZKNOT has no federal past performance yet. This is the chicken-and-egg of federal
contracting. Mitigation paths:

1. **Subcontract under a prime** — get federal experience without being prime
2. **Small contracts first** — micropurchases ($10K) don't require past performance
3. **SBIR Phase 1** — designed for first-time federal awardees
4. **Commercial past performance** — PV1 customer letters count for some purposes

### 6.4 — Capacity and capability honesty

Federal contractors get burned by overpromising. As a one-person SDVOSB:
- Don't bid on contracts requiring >40 hours/week of delivery for >30 days
- Be honest about subcontracting — disclose what you'll do vs. partner do
- Don't claim "team" capability that doesn't exist

### 6.5 — Cash flow risk

Federal payment terms are typically Net 30 from invoice acceptance, which can
mean 60-90 days from work completion. SDVOSBs go under regularly due to cash
flow mismatch on federal work. Mitigation:

- Don't take on contracts that require >30 days of cash outlay before invoicing
- Use SBA's contract financing options (e.g., 7(a) for working capital)
- Build relationships with veteran-focused lenders (e.g., StreetShares for VOSBs)

---

**Page 7 of 7**

## Appendix A — Resource links

| Resource | URL |
|---|---|
| SAM.gov | sam.gov |
| SBA VetCert | veterans.certify.sba.gov |
| GSAXcess | gsaxcess.gov |
| GovPlanet | govplanet.com |
| GSA Auctions | gsaauctions.gov |
| Utah State Surplus | surplus.utah.gov |
| DoD SBIR/STTR | dodsbirsttr.mil |
| SBIR.gov | sbir.gov |
| DLA Disposition | dla.mil/dispositionservices |
| FedBizOpps (now SAM.gov contracts) | sam.gov/content/opportunities |
| APEX Accelerator Utah | utahapex.ecenterdirect.com |
| VA OSDBU | osdbu.va.gov |
| AFWERX | afwerx.com |
| DAU (Defense Acquisition University) | dau.edu |
| SBA Boots to Business | boots2business.org |

## Appendix B — Quick-reference: ZKNOT identifiers for any federal form

Copy-paste ready:

```
Legal name: ZKNOT, INC.
Owner (full legal name on official docs): William Shane Wilkinson
UEI: C4SKW13JPEL5
CAGE: 1AHZ4
EIN: 36-5165991
SDVOSB Certified: Yes (SBA VetCert, certified May 2026)
NAICS (primary): [confirm primary in SAM.gov]
State of incorporation: [confirm]
Address: [confirm registered business address]
```

**Action:** Verify and complete the blanks above, then commit this doc with the
filled values. The full legal name William Shane Wilkinson must appear on all
official documents per established convention.

## Appendix C — What this doc is NOT

- Not a sales/marketing plan (see future ZKNOT-PLAN-GTM-001)
- Not a federal compliance checklist (see future ZKNOT-PLAN-COMPLIANCE-001)
- Not a patent strategy (see existing patent docs in 01_PATENTS/)
- Not infrastructure (see ZKNOT-PLAN-INFRA-001)
- Not engineering roadmap (see project-specific docs)

## Appendix D — Cross-references to related Taskwarrior projects

- `zknot.gov` — primary project for this doc's tasks
- `zknot.ops` — when SDVOSB tasks become operational (compliance, renewals)
- `acquisition` — separate workstream for exit/M&A targets
- `patents` — IP work tracked separately
- `pv-rev1` / `zkkey-connect` — engineering, not procurement

## Revision log

| Date | Author | Change |
|---|---|---|
| 2026-05-16 | William Wilkinson | Initial creation |

---

**End of document. Page 7 of 7.**
