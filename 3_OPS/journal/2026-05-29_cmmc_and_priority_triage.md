---
date: 2026-05-29
topic: cmmc_overview_and_priority_triage
workstreams: [biz, ops]
status: complete
tags: [cmmc, compliance, sbir, triage, federal]
---

# CMMC Overview & Priority Triage

## TL;DR

Asked Claude what CMMC is — got the basics, captured below. Then asked what to actually finish right now per this thread's context. Claude pointed at SBIR Phase I June 3, but this conflicts with a recent memory update saying SBIR is dead for now. The recommendation may be built on a stale "top of mind" signal. Need to reconcile SBIR status before treating either path as a real action item. CMMC is not a current gate — park as awareness, promote durable facts to a systems note.

## Decisions

- **No action on CMMC yet.** Not a gate for current work. Becomes relevant if/when ZKNOT pursues DoD contracts touching CUI.
- **Reconcile SBIR status before next working session.** Memory has contradictory signals — top-of-mind says June 3 deadline, recent_updates says SBIR is dead. Claude's "do this right now" recommendation rested on the wrong signal. Confirm which is true and update memory accordingly.
- **Promote CMMC facts to `~/ZKNOT/3_OPS/km/systems/cmmc.md`.** Durable reference knowledge belongs there, not in a journal.
- **Do not propagate CMMC details into any federal filing without primary-source verification.** Claude's facts are general knowledge, not verified against DFARS, the Federal Register, or the DoD CIO CMMC site.

## CMMC — what it is

The Cybersecurity Maturity Model Certification. DoD's framework for verifying that defense contractors adequately protect sensitive government information. Phasing into DoD contracts as a *condition of award* — no cert at the required level, no eligibility for that contract.

CMMC 2.0 rule was finalized in late 2024 and is rolling into DoD solicitations on a multi-year ramp. (Verify current phase-in dates against primary source before citing in any filing — rollout has shifted before.)

### Data types that drive scope

- **FCI** — Federal Contract Information. Non-public info provided to a contractor under contract.
- **CUI** — Controlled Unclassified Information. Broader, more sensitive category requiring stronger controls.

### Three levels

| Level | Scope | Control basis | Assessment |
|-------|-------|---------------|------------|
| 1 | FCI safeguarding | 15 controls from FAR 52.204-21 | Annual self-assessment |
| 2 | CUI protection | 110 controls from NIST SP 800-171 | Self- or C3PAO-assessed depending on contract |
| 3 | Most sensitive programs | Adds NIST SP 800-172 controls | Assessed by DIBCAC (government) |

### Supporting artifacts a Level 2 shop carries

- **SSP** — System Security Plan
- **POA&M** — Plan of Action & Milestones
- **C3PAO audit evidence** when third-party assessment is required

## Relevance to ZKNOT

- SBIR Phase I awards typically don't handle CUI — CMMC is usually not a gate at Phase I.
- Phase II / Phase III and follow-on DoD work very plausibly will require Level 2.
- A cryptographic authenticity vendor is the kind of company that ends up touching CUI eventually.
- **Architectural decision worth making early:** do we ever want to *hold* CUI, or design the stack to stay clear of it? Cheaper to decide before infrastructure ossifies than to retrofit later.
- This is the federal-compliance-moat angle on the personal monopoly — defense-adjacent cryptographic authenticity is precisely where CMMC-readiness becomes a competitive advantage rather than overhead.

## Priority triage (this thread)

Asked Claude what to actually finish right now. Claude pointed at SBIR Phase I, 6 days out.

**Caveat:** memory's `recent_updates` says SBIR is dead unless ZKNOT changes course completely. The recommendation may be based on stale top-of-mind data. Do not act on the SBIR triage list below until I confirm SBIR status.

### Action items Claude proposed (parked pending SBIR-status confirmation)

1. List proposal sections by state: done / drafted / not started.
2. Identify blockers per unfinished section.
3. Confirm DSIP submission flow — dry-run the portal mechanics, not just content.
4. Confirm the FT260 + bare TrustCUSTOM (TFLXTLS) hardware pivot is reflected in the proposal narrative, not the old Trust&GO plan.

If SBIR is in fact dead, the real triage question is different: **what *is* the next funded milestone, and what's the critical path to it?** That's the question to sit with before anything else.

## Open questions

- Is SBIR actually dead, or is the June 3 deadline still live? Memory is contradictory.
- If dead: what replaces it as the near-term forcing function?
- Does verifyknot.io deployment have an external deadline, or is it self-imposed?
- Where should CMMC awareness live — passive (read DFARS once a quarter) or active (design system boundaries around CUI now)?

## Followups

- [ ] Reconcile SBIR status; update memory if "top of mind" is stale.
- [ ] Create `~/ZKNOT/3_OPS/km/systems/cmmc.md` with facts verified against DoD primary sources (DoD CIO CMMC page, DFARS 252.204-7021, current Federal Register entry).
- [ ] If SBIR is dead, write a fresh "what's the next forcing function" journal entry.
- [ ] Commit this journal entry to git.

## Concepts to track

- [ ] CMMC 2.0 — three-level structure and what triggers each level
- [ ] FCI vs CUI — the distinction that drives scope
- [ ] NIST SP 800-171 — the 110-control baseline behind Level 2
- [ ] NIST SP 800-172 — additional Level 3 controls
- [ ] C3PAO — Certified Third-Party Assessor Organization
- [ ] DIBCAC — Defense Industrial Base Cybersecurity Assessment Center
- [ ] DFARS clause family — 252.204-7012, 7019, 7020, 7021
- [ ] SSP / POA&M — the two living documents every Level 2 shop maintains
- [ ] Federal compliance moat — how CMMC-readiness becomes a competitive advantage for a cryptographic authenticity company rather than overhead
