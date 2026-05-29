---
title: "Federal BD & Post-SBIR Funding Strategy"
date: 2026-05-27
workstream: biz
status: active
tags: [federal, bd, funding, ota, diu, nstxl, s2marts, tradewinds, sbir, capability-statement, champion]
related:
  - "event: 2026-05-28 GSA OCAS Pipeline Review (11:00 MST)"
  - "event: 2026-05-28 ICF / VA OSDBU Business Opportunity Session (15:30 MST)"
  - "km/systems/federal-funding-vehicles.md (durable mechanics)"
---

# Federal BD & Post-SBIR Funding Strategy

> Note: front-matter fields above are my best reconstruction of the daily-journal template
> (front-matter + TL;DR + Decisions). Reconcile against
> ~/ZKNOT/3_OPS/km/templates/daily-journal.md before committing if fields differ.

## TL;DR

SBIR dead-ended, so I surveyed the alternatives I'd named — OTAs, prime IRAD interest,
and AFWERX/DIU non-SBIR pathways. The blunt result:

- **Two of the named alternatives are NOT alternatives.** AFWERX STRATFI/TACFI and AFWERX
  SBIR Open Topic share SBIR's exact root blocker — STRATFI/TACFI are gated on having an
  active/recent SBIR Phase II (I have none), and AFWERX can't issue *any* new SBIR/STTR
  awards until Congress reauthorizes the program. Same wall, different door.
- **IRAD was a misread on my part.** IRAD is a prime's own overhead R&D money — you don't
  apply for it, you get a prime to spend it on you. It's a relationship outcome, not a
  funding application.
- **Three vehicles are actually live and fit ZKNOT**, ranked: NSTXL consortium → S2MARTS
  (best thematic fit, cheap, but gated by a CMMC L2 self-assessment due Nov 10 2026);
  DIU Commercial Solutions Opening (fastest real money, 60–90 day awards, but competitive
  and needs a real military-need match); Tradewinds Solutions Marketplace (free, 30-day
  assessment, but scoped to AI/ML — a framing stretch for crypto/hardware).
- **The meta-unlock:** the actual bottleneck for almost every fast vehicle is a named
  government or prime **champion**, not a form. DIU is transformed by an end-user; STRATFI
  literally can't be submitted without a government POC; IRAD is a relationship by
  definition; consortium OTA awards trace back to a sponsoring program office. I don't have
  a funding-application problem. I have a sponsor problem.
- The two May 28 BD meetings are therefore reframed from "teaming" to **champion-hunting** —
  they're the front door to the thing gating everything else.
- **Gating artifact across all of it:** a one-page capability statement. Every path
  (webinar follow-ups, ICF teaming, DIU brief, cold outreach) needs something to attach.

## Decisions

1. **Stop spending cycles on SBIR, STRATFI/TACFI, and AFWERX SBIR Open Topic** until either
   a Phase II exists or the program is reauthorized. These are valley-of-death *bridges* and
   I'm not yet on the near bank.
2. **Build the one-page capability statement first** as the gating artifact, ahead of any
   funding submission. Do it myself in Word/Docs (AI-generated cap statements read as such to
   federal BD; format is standardized; content must be in my voice).
3. **Do NOT pay NSTXL dues on spec.** Wait until after the May 28 meetings — if a specific
   program office points me to a consortium and an Area of Interest, I join with a target
   instead of blind. Engagement, not membership, is the variable that pays.
4. **Reframe OCAS/ICF (May 28) as sponsor reconnaissance.** The real question across both
   rooms: who inside a prime or program office would spend their own credibility to sponsor
   a ZKNOT prototype?
5. **Promote funding-vehicle mechanics to km/systems/federal-funding-vehicles.md** — durable
   "how X works" facts don't live in the journal.

---

## Context

This entry closes out a working arc that started with two SDVOSB-relevant webinar invites
and expanded into a full post-SBIR funding-landscape review after the SBIR topic that fit
ZKNOT lapsed. Deleting the source thread, so this is the permanent record. The durable
vehicle mechanics live in the companion systems note; this journal holds the decisions,
the meeting prep, and the strategic read.

## The two meetings (May 28)

Both Thursday, both on the calendar with 15-min reminders. **Registration links were not in
the invites — must register from the original emails; the calendar event is useless without
registration.** SBIR-adjacent deadline pressure is gone, so attending is lower-cost than it
felt, but the ICF session is the higher-value of the two.

### GSA OCAS Pipeline Review — 11:00–12:00 MST
- OCAS = operational arm of the EO to consolidate federal procurement into "one federal
  wallet." Brand-new office (stood up late 2025); already absorbed contracting for OPM, SBA,
  HUD; manages NASA SEWP and NIH CIO-SP3/CIO-SP4; tasked with piloting AI/automation in
  procurement.
- Scope is **"common goods and services"** — cryptographic authenticity hardware is NOT that.
- **Play here is listening, not pitching.** Learn pipeline cadence and which agencies they're
  absorbing next, so later VA/DoD/DHS targeting understands the plumbing.
- Questions that earn a follow-up:
  - "As OCAS absorbs more agency contracting, will small-business set-aside goals be evaluated
    at the OCAS portfolio level or stay at the originating agency level?"
  - "What's the cadence for these pipeline reviews going forward — quarterly?"
- Inbound contact for industry: **industrygsaocas@gsa.gov**. Join the OCAS Interact community
  (buy.gsa.gov/interact) for future pipeline events.

### ICF / VA OSDBU Business Opportunity Session — 15:30–16:30 MST
- ICF = publicly-traded (~$2B+) federal consulting prime; subs heavily because VA/HHS push
  small-business goals down through FAR-required subcontracting plans (>$750K contracts).
- **Leverage point:** VA's Veterans First Contracting Program (38 U.S.C. 8127) gives SDVOSBs
  statutory priority over all other set-aside types. ICF *wants* SDVOSB subs on VA work — that's
  why this session exists. This is also the closest live IRAD shot (nobody will say "IRAD").
- Their four focus areas → ICF practice lines. "Digital Modernization & Experience" = cloud,
  identity, FedRAMP, CX, app modernization. Device attestation isn't a line item, but
  **supply-chain integrity for VA-procured devices** is real and growing (post-SolarWinds,
  post-Volt Typhoon).

### The 45-second framing (use at ICF; adapt for any prime)
> "We're an SDVOSB doing cryptographic authenticity verification — hardware-rooted device
> attestation, so a VA endpoint or supplied device can prove it is what it claims to be, with
> a zero-knowledge audit trail. We're built for supply-chain integrity use cases, and we're
> looking for primes interested in SDVOSB teaming on digital modernization or supply-chain
> assurance scopes."

**Do NOT say in the room:** "FSM-gated post-nonce human-actuation architecture," "PUF
verification," ZK-LocalChain internals, or "pre-revenue" (true, but unforced).

### Questions for ICF
- "For your VA digital-modernization portfolio, what's your typical SDVOSB subcontracting goal
  range, and where in the capture cycle do you bring subs in?" (tells me pre-RFP vs post-award)
- "Are there specific NAICS codes or capability gaps where you're actively looking for SDVOSB
  partners right now?"

## The capability statement (gating artifact)

One page, PDF, finished before the meetings. Everything downstream attaches to it. Send within
~30 min of each meeting ending → ahead of 90% of attendees.

Required sections: tagline; core competencies (3–5 bullets); differentiators (2–3 — the
human-actuation novelty in *plain English* here); current work (active R&D, patent app —
pre-revenue is fine, don't hide it); company data block (UEI C4SKW13JPEL5, CAGE 1AHZ4,
EIN 36-5165991, SDVOSB cert, SAM active since 2026-03-27); contact (William Shane Wilkinson,
support@zknot.io, verifyknot.io); NAICS codes.

**Before writing it:** look up ICF's active VA prime contracts on USASpending.gov (search ICF
as recipient, filter to VA) and mirror their NAICS codes. Candidate codes: 541512, 541330,
541715, 334290, 334418 — verify against what ICF actually uses.

If I can't write the differentiator bullets without jargon, that's the signal the category
still isn't named — and naming it is the real work hiding inside this task.

## Funding landscape — summary only (mechanics → systems note)

| Vehicle | Status for ZKNOT | Why |
|---|---|---|
| SBIR (topic that fit) | DEAD | Topic lapsed; no longer applies unless we change course |
| AFWERX SBIR Open Topic | BLOCKED | Program-wide freeze on new awards pending reauthorization |
| AFWERX STRATFI/TACFI | BLOCKED | Requires active/recent SBIR Phase II — same wall as SBIR |
| Prime IRAD | INDIRECT | Not an application; a prime relationship outcome. ICF = closest shot |
| **NSTXL → S2MARTS** | **LIVE — best fit** | Microelectronics/trusted-hardware focus; cheap dues; CMMC L2 gate by Nov 2026 |
| **DIU CSO** | **LIVE — fastest $** | 60–90 day awards, short brief to enter; competitive; needs real mil-need match |
| **Tradewinds TSM** | **LIVE — free/fast** | 5-min video, 30-day assessment; but AI/ML-scoped → framing stretch |

Full eligibility gates, costs, timelines, and primary sources are in
`km/systems/federal-funding-vehicles.md`. Verify any eligibility figure at its primary source
before acting on it.

## The champion insight (carry this forward)

The pattern across every fast vehicle: DIU is transformed by an end-user, STRATFI can't be
submitted without a government POC, IRAD is a prime relationship by definition, consortium OTA
awards trace to a sponsoring program office. **The bottleneck is a person who'll vouch, not a
form to fill out.** I've been hunting for a form. The May 28 meetings are champion reconnaissance.

## Next actions

**Sequenced (do first → last):**
1. Register for both webinars (precondition; ~5 min).
2. Pull ICF's VA prime contracts on USASpending.gov; pick NAICS codes (~15 min).
3. Draft + PDF the one-page capability statement, myself (~60–90 min).
4. Rehearse the 45-sec pitch out loud x3 with a timer (~10 min).
5. **After meetings:** debrief journals (who showed up + roles, which focus areas had real
   openings, whether the SDVOSB+attestation framing landed or drew blank stares — blank-stare
   data > head-nods).

**Strategic / this week (after meetings):**
- Verify the Tradewinds TSM collection window (recurring; current one closes ~May 31 — check
  SAM.gov / tradewindai.com for the next period before investing video effort).
- Register the NSTXL member portal + confirm dues tier (~30 min) — but hold on *paying* until a
  meeting points to a specific program office / AOI.
- Bookmark + RSS the DIU open-solicitations page (diu.mil/work-with-us/open-solicitations) so new
  AOIs hit the inbox.

## Open questions / TODO

- [ ] Did either meeting surface a named potential champion (prime BD lead or program POC)?
- [ ] Which existing buying category does ZKNOT's attestation belong inside — or is "microelectronics
      assurance, human-in-the-loop corner" a category I get to name?
- [ ] CMMC L2 self-assessment: scope the effort now (months-long if started cold) ahead of any NSTXL move.

## Concepts to internalize (captured here since the source thread is being deleted)

- OTA (Other Transaction Authority, 10 U.S.C. 4022) — legal basis to skip the FAR for prototypes
- CSO (Commercial Solutions Opening) — DIU's competitive front door to a prototype OT
- Prototype OT → Production OT follow-on — why the prototype is a sole-source "audition"
- Consortium-managed OTA — how NSTXL / S2MARTS / SpEC broker between buyers and small firms
- STRATFI / TACFI — SBIR-Phase-II-gated valley-of-death bridges, and *why* they're gated
- IRAD — prime overhead R&D; a relationship outcome, not an application
- CMMC Level 2 self-assessment / SPRS — the cybersecurity-maturity gate baked into NSTXL membership
- "Champion" / government sponsor — the actual unlock behind every fast vehicle
- Microelectronics assurance — the procurement category the hardware attestation most naturally lives in
- Veterans First Contracting Program (38 U.S.C. 8127) — SDVOSB statutory priority at VA

## Personal-monopoly thread

"Microelectronics assurance" is a named, funded DoD priority that almost nobody frames around
*human-actuated* attestation the way PAT-001 does. If the category is real and buyers fund it,
the question is whether I become the name on the human-in-the-loop corner of it — before someone
else names it first. The cap statement is the first forcing function for that naming.
