# SBIR 2026 Topic Scan — Decision and Strategic Conclusion

**Date:** 2026-05-24
**Author:** William Shane Wilkinson
**Context:** Evaluated 6 DoW SBIR 2026 topics against ZKNOT's core IP (human-actuated, independently verifiable, non-repudiable attestation) ahead of the June 3 deadline. This entry records the per-topic verdicts so they aren't re-evaluated, and the strategic conclusion the scan produced.

---

## The decision in one line

Submit the **ITV white paper (ARM26BX01-NV001)** for June 3 as the only executable fit; treat **RMF Pre-Adjudication (NV006)** as the top watch-and-team target; stop scanning. ZKNOT's federal home is human-attestation / non-repudiation / accountability topics — they are emerging, and teaming is the fastest path to clearing the maturity bar to win them.

## The core insight: executable-fit vs thesis-fit

The scan surfaced two different kinds of "fit," and conflating them is the trap:
- **Executable fit** = a topic ZKNOT can credibly *win now* (eligible, right maturity, right deadline). Only ITV qualifies, and only imperfectly (integrity-layer contribution, not the core ask).
- **Thesis fit** = a topic that demands exactly what ZKNOT is *built for*. NV006 is the standout — it demands "human attestation" by name — but ZKNOT can't execute it this cycle (the buy is an AI analysis engine ZKNOT lacks; maturity/eligibility too high; closes June 24).

The strategic prize is the thesis-fit topic, not the executable one. ITV is what we can submit; NV006 is what we're built for. The job over the next 6–12 months is to close the gap between the two.

## Per-topic verdicts (do not re-evaluate)

| Topic | Close | Verdict | Disqualifier |
|---|---|---|---|
| **ARM26BX01-NV001** In Transit Visibility Blockchain (ARMY) | Jun 3 | **SUBMIT** | Imperfect but real: integrity/provenance-layer contribution; white paper; eligible (CMMC L1). Draft complete. |
| **DAF26BZ01-NV008** Runtime Assured Autonomy (USAF) | Jun 3 | No | Premise is *no human in the loop* (autonomy fills the gap when human C2 can't). Contrary to human-actuation IP. ITAR, CMMC L2. |
| **OSW26BZ02-DV003** GenAI for Secure Workflow & Compliance (OSD) | Jun 24 | No | Direct-to-Phase-II gate: requires prior TS/SCI classified DoW performance + fine-tuned-LLM track record ZKNOT lacks. Wrong end of pipeline (generates docs; we prove integrity). |
| **DLA26BZ02-NV006** AI-Assisted RMF Pre-Adjudication (DLA) | Jun 24 | No now / **TOP WATCH-TEAM** | Best thesis fit — demands "explicit human attestation mechanism" by name; NIST 800-37/800-53 grounded. But the *buy* is an AI document-analysis engine ZKNOT doesn't have; Phase I expects a functional prototype in a gov sandbox; CMMC L2 + ITAR. |
| **DLA26BZ02-NV004** Enterprise Digital Thread / Decision Intelligence (DLA) | Jun 24 | No | Demands **TRL 6-9** (near-fielded) + FedRAMP High + integration of named enterprise stack (Celonis, ServiceNow, SAP S/4HANA, MuleSoft, Vertex AI). Enterprise-integration play for an embedded vendor. No attestation content. |
| **DON26BZ01-NV007** HUB Tester for Type 1 Encryptors (NAVY) | Jun 3 | No | "Encryption" is a false friend — it's a *battery-health test instrument* problem. Requires secret facility clearance (NISPOM), CMMC L2, ITAR. Zero attestation content. |

Remaining ~125 topics in the solicitation are sonar/lasers/propulsion/ceramics/materials/working-dog medicine/antennas — no conceivable connection to cryptographic attestation. Scan considered exhausted.

## The maturity bar these topics reveal

To win human-attestation topics *solo*, ZKNOT will need some combination of:
- **TRL 6+** (demonstrated prototype in a relevant environment) — NV004, NV006
- **FedRAMP** authorization (Moderate/High) — NV004
- **Prior classified DoW performance** + clearances (facility + personnel) — DV003, NV007
- **A fielded/maturing product**, not just an architecture

ZKNOT currently has: an attestation backend + tamper-evident chain in development, SDVOSB cert, active SAM.gov — but none of the above bar items. That gap is the real blocker, not topic availability.

## Strategic conclusion (the payoff of the whole exercise)

1. **DoD is now writing ZKNOT's thesis into solicitations.** NV006's "explicit human attestation mechanism … to prevent reliance on unreviewed AI outputs" is the AI-era, NIST-grounded accountability use case articulated in the 2026-05-23 trust-model journal — now a federal requirement. This is the empirical confirmation sought when pressure-testing "which contracts actually demand human-attestation." Answer: they're starting to.
2. **Teaming is the fastest path across the maturity bar.** On NV006, an AI/NLP firm owning the document-analysis engine needs exactly the human-attestation + source-traceability + NIST-defensible accountability layer ZKNOT has and most AI teams hand-wave. ZKNOT as the attestation sub-partner is a credible Phase II angle — possibly stronger than any solo bid.
3. **SBIR is one funnel, not the only one.** Other federal doors given SDVOSB status: AFWERX/SpaceWERX open topics + STRATFI/TACFI on-ramps; DIU; civilian-agency SBIR where the audit/compliance angle fits cleanly (DHS, GSA, Treasury/FinCEN-adjacent, HHS for pharma track-and-trace); SDVOSB set-aside on ordinary contract vehicles. And the commercial GRC/audit-acceleration market needs no federal door at all.

## Forward watch-list (for the next scan — start here, not from scratch)

Watch for topics that are:
- **Human-attestation / non-repudiation / chain-of-custody / evidence-integrity** in the requirement (not just "compliance" or "encryption" as keywords)
- **Phase I** (not Direct-to-Phase-II) — so prior performance isn't a gate
- **Not clearance-gated** at entry (clearance OK as a later-phase requirement)
- Ideally **CMMC L1**, civilian-agency, or SDVOSB set-aside
- Sources to monitor: DLA, OSD/SCO, AFWERX compliance/governance topics

## Action items
- [ ] **DECIDE ITV (yes/no) — today.** Hard June 3 clock. Draft exists.
- [ ] If yes on ITV: verify before submitting — (a) AFRL-interop section framed honestly as a Phase I research objective, not a solved problem; (b) "attestation backend + tamper-evident chain already in development" wording matches reality (federal submission under signature).
- [ ] **Start NV006 teaming outreach** to AI/NLP/compliance firms (before Jun 24 close) — position ZKNOT as the human-attestation + traceability + NIST-accountability sub-partner. Highest-leverage long game.
- [ ] Widen the funnel: pull current AFWERX/STRATFI + civilian-agency (DHS/GSA/HHS) openings for human-attestation/audit fit.
- [ ] Cross-link: this decision connects to 2026-05-23_trust-model-and-market.md (NV006 = the demand-side confirmation of that market thesis).

## CMMC timing & strategy note (added 2026-05-24)

**Rule status:** CMMC enforceable since Nov 10, 2025 (48 CFR / DFARS 252.204-7021). It is a condition of **award and performance**, NOT bid eligibility. Phased 4-year rollout; contracting-officer discretion on when the clause appears in a given award.

**Levels:** L1 (Federal Contract Information) = 15 practices, **self-assessment** posted to SPRS, doable in-house. L2 (Controlled Unclassified Information) = NIST SP 800-171 (110 controls), and during Phase 1 may require a **C3PAO third-party assessment**.

**Implications for ZKNOT:**
- ITV (NV001) is tagged **CMMC L1** — no cert needed to submit; if selected, complete an L1 self-assessment + SPRS posting before award. Lightweight.
- The four rejected topics + the human-attestation prize topics (NV006, etc.) were **CMMC L2**. So "path to CMMC L2" now joins **TRL 6-9** and **FedRAMP** on the maturity-bar list. Teaming with an already-certified prime is the near-term way to sidestep all three.
- NOT a lawyer; the authoritative requirement for any award is the clause in that specific solicitation. Read award terms if selected.

**Strategic build goal (founder, 2026-05-24):** Become the **SDVOSB + CMMC-certified** human-attestation company, and **dogfood ZKNOT** to meet/evidence the controls — i.e., ZKNOT's own attestation provides part of the audit evidence (esp. NIST 800-171 / 800-53 AU-10 non-repudiation, audit-trail integrity, access accountability). Founder holds an MS in cybersecurity → technical bar is reachable. SEE SEPARATE BUILD-PLAN ENTRY for the honest sequencing, scope-reduction strategy, and the three risks (CUI scope creep, FedRAMP ≠ CMMC, dogfooding covers only some control families).

## One-line throughline
Six topics confirmed empirically what the trust-model journal theorized: ZKNOT's IP shines exactly where a human *must be provably in the loop* — which autonomy topics reject, hardware topics don't ask for, and compliance/RMF topics are now starting to demand. ITV is this cycle's shot; NV006 is the signal of where the real traction lives; teaming is how to get there before solo eligibility catches up.
