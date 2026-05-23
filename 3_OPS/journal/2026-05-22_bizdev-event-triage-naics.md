# 2026-05-22 — BizDev Event Triage & NAICS Selection

**Context:** Calendar/event triage chat. Reviewed Utah APEX, DoD MICC, GSA, VA, and assorted vendor/job-seeker events against ZKNOT fit (PUF authentication, SDVOSB, pre-revenue cryptographic auth). Also covered NAICS sector selection during an event registration form.

---

## Event Triage

### HIGH VALUE — worth the time

**[APEX] Intro to GSA — May 27, 9:30–11:30 AM, Layton UT (Hybrid)**
- GSA Schedule likely path once ZKNOT has a sellable product/vehicle. SDVOSB + GSA is a strong combo.
- In-person at LSI Corporate Office, 1530 N. Layton Hills Pkwy (~45 min from SLC). Networking value with Laurie Pless (LSI, lpless@lsiwins.com, 801-678-9331) and Chuck Spence (Utah APEX, cspence@utah.gov, 801-538-8655). Recommend in-person.
- Registration: https://utahapex.ecenterdirect.com/events/3465
- **Goals:**
  1. Determine if GSA MAS is appropriate now or post-pilot.
  2. Identify which Schedule/SIN aligns with PUF auth (likely IT Cat 54151S or Highly Adaptive Cybersecurity Services / HACS).
  3. Get on Chuck Spence's radar as SDVOSB cryptographic authentication.
- **Questions to ask:**
  - For a pre-revenue SDVOSB with no past performance, is GSA MAS premature, or can the process start now?
  - Which SIN best fits cryptographic authenticity verification hardware + SaaS?
  - Typical timeline from offer submission to first task order?
  - Can SDVOSB set-asides be applied to GSA orders, and how mechanically?

**[DoD] MICC APBI — May 18–22 (Virtual, MS Teams)**
- MICC handles installation contracting across Army bases. PUF auth applies directly to supply chain integrity, parts authentication, counter-counterfeit — MICC pain points. 418th (Fort Hood) and 419th (Fort Bragg) cover large footprints.
- Day 1 briefing (May 18, 7:30–10 AM MDT / 8:30–11 AM CDT) is the keeper — forecasted opportunities + small business presentation from Luis Trinidad (MICC OSBP Director).
- One-on-one sessions Days 2–5; request a slot if still open. SDVOSB + cryptographic auth is a differentiated pitch.
- NOTE: Event window overlaps today (5/22). Likely mostly passed — capture for next year's cycle and for POC follow-up regardless.
- Key personnel from agenda: Mr. Luis O. Trinidad (MICC OSBP Director), BG Freddy L. Adams II (CG), COL Kizzy M. Danser (418th CSB Cdr), Mr. Percy D. Jones Jr. (419th CSB Deputy), Dr. Latosha V. McCoy (FDO Fort Eustis), COL Randy J. Garcia (FDO Fort Sam Houston).
- **Goals:**
  1. Identify forecasted MICC requirements touching supply chain integrity, anti-counterfeit parts, asset authentication.
  2. Get Luis Trinidad aware of ZKNOT.
  3. Capture POCs at 418th/419th CSBs for follow-up.
- **Questions:**
  - Does MICC have forecasted requirements around counterfeit parts detection or supply chain provenance?
  - Preferred entry path for an SDVOSB with novel cryptographic tech but no Army past performance?
  - Are there SBIR Phase III on-ramps MICC participates in?

### MODERATE — attend if low effort

**[GSA] OCAS Updates and Pipeline Review — May 28, 11 AM MDT (Virtual)**
- Pair with May 27 Intro to GSA — primed to understand OCAS. Pipeline review = forecasted opportunities. 1 hr virtual.
- Goal: identify any OCAS opportunities involving authentication, identity, or supply chain.

**[VA OSDBU] ICF Virtual Business Opportunity Session — May 28, 3:30 PM MDT**
- ICF is a major fed contractor actively seeking SDVOSB subs. "Digital Modernization" track could fit ZKNOT as a sub on VA work (credential/document authentication plausible for VA).
- Goal: get ZKNOT into ICF's SDVOSB vendor database for teaming.
- Skip if not ready to pitch subcontractor teaming. Otherwise low-cost 1 hr.

### SKIP — not aligned

- [GSA] Navigating GSA MAS – IT Category (May 14) — passed; May 27 in-person covers similar ground better.
- Hiring Our Heroes events — job-seeker events for transitioning service members. Founder, not job seeker. Revisit only if hiring vets later.
- Yubico webinars — adjacent (auth) but vendor marketing, not opportunity.
- STMicroelectronics events — component vendor marketing. Revisit only if sourcing specific MCUs for a PUF reader.
- ERDCWERX TEMPO (medium-voltage power) — out of domain.
- ERDCWERX Autonomous Dredging — out of domain.
- Schneider Electric OT resilience — out of domain.
- Govology webinars (subcontracting limits; IBAS/OTAs) — IBAS/OTA one (May 20) borderline interesting for DoD pathway awareness but not urgent; subcontracting compliance only matters once subs exist.
- HIPE / Veteran Business Conference / FLC — already passed (early May).

### Recommended action sequence (as of 5/22)
1. Register MICC APBI Day 1 + request 1:1 if slots remain (likely passed — verify / note for next cycle).
2. Register May 27 Intro to GSA — in-person at LSI Layton.
3. Optional: May 28 OCAS pipeline review + ICF session.

---

## NAICS Selection (event registration form)

Form had NAICS sector radio buttons; had selected **51 - Information**. Assessment for ZKNOT:

- **54 - Professional, Scientific, and Technical Services** = strongest fit. Where most cryptographic/cybersecurity/auth companies land and where DoD/MICC COs look for novel work. Pairs best with SDVOSB + R&D narrative.
  - 541512 Computer Systems Design Services
  - 541519 Other Computer Related Services (cybersecurity/auth)
  - 541715 R&D in Physical, Engineering, Life Sciences ← strong for PUF/novel crypto, esp. pre-revenue
- **31-33 - Manufacturing** = if ZKNOT produces/sells PUF hardware tags:
  - 334290 Other Communications Equipment Manufacturing
  - 334413 Semiconductor and Related Device Manufacturing (if PUF substrate qualifies)
- **51 - Information** = defensible but under-sells the crypto R&D + hardware story:
  - 518210 Computing Infrastructure Providers / Data Processing (fits api.zknot.io SaaS side)
  - 513210 Software Publishers (fits verification software)

**Recommendation:** If one pick → **54**. If multi-select → 54, 51, 33 (that order).

**OPEN ITEM:** Confirm NAICS codes currently on SAM.gov registration. Primary NAICS on SAM should drive event-form picks for consistency across SAM/GSA/registrations (matters for searchability). TODO: decide ZKNOT primary + secondary NAICS and align everywhere.

---

## Open follow-ups
- [ ] Verify MICC APBI 1:1 availability / capture for next year's cycle.
- [ ] Register May 27 Intro to GSA (in-person, LSI Layton).
- [ ] Confirm/align ZKNOT NAICS codes on SAM.gov (primary + secondary).
- [ ] Decide on OCAS + ICF May 28 attendance.
