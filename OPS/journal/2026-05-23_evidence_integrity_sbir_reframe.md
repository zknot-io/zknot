# 2026-05-23 — Evidence Integrity: SBIR reframe + open threads

**Author:** William Shane Wilkinson · ZKNOT, Inc.
**Context:** Worked through the evidence-integrity line as the acquisition narrative,
then untangled what the "SBIR Phase I, June 3" date actually means. Source brief:
`ZKNOT_evidence_integrity_thread_brief.md`.

---

## The headline takeaway

**The June 3 SBIR date should NOT be driving evidence-integrity priorities right now.**
A Phase I proposal is a response to a *specific open topic*. There is currently no open
topic that fits evidence integrity. With no topic, there is nothing to write against —
no evaluation criteria, no agency, no work-plan target. So the "deadline" is attached to
a solicitation that hasn't opened / doesn't fit / was speculative. This is good news:
not behind on anything. Don't manufacture urgency from a dateless deadline.

### Caveat to self
The June 3 date may belong to a *different* track (PUF / supply-chain / hardware pivot —
the FT260 + TrustCUSTOM SBIR work). If so, that deadline is real but is NOT the
evidence-integrity line. Keep these separate. Confirm which track June 3 actually
belongs to before treating it as live.

---

## Decisions made

1. **Evidence integrity = acquisition story, not near-term SaaS.** Confirmed framing
   from the brief. Strategic buyers (Axon archetype, defense govcons/primes) acquire
   capabilities or run procurement-heavy pilots — they don't sign up for a self-serve API.

2. **No-topic = no proposal-writing work right now.** The path forward is BD/outreach
   (procurement time) plus the build/spec work below — none of it gated by June 3.

3. **If a real topic later appears,** the existing brief is ~70% of the proposal's
   intellectual content. A Phase I is a *feasibility + work plan* deliverable, not a
   "show us a working system" deliverable — so the challenger build becomes a *proposed
   Phase I deliverable*, not a prerequisite. What a future proposal would still need:
   solicitation topic language mapped to PAT-007/008/009, a Phase I technical-objectives
   list, and the reliability-measurement plan written as proposed work.

---

## The dependency chain (holds regardless of any solicitation)

    challenger/verifier build → reliability data → one pilot → acquisition conversation

- Can't run a credible evidence pilot without the challenger side built.
- Can't prove reliability (false-accept / false-reject) without a pilot generating real numbers.
- This ordering should anchor the evidence-integrity roadmap.

**The challenger/verifier is the gating unbuilt piece.** It mints and optically presents
the nonce. It's the one item here that needs actual design work, not reframing. Next
substantive work session on this line should be the challenger/verifier spec.

---

## Sharper points worth keeping (the analysis, not just conclusions)

- **Axon corp-dev would need, in order:** (1) working continuity demo on real footage,
  (2) error-rate data, (3) patent prosecution status. Moat against "ignore" is the patent
  cluster being far enough along that building around it is expensive. → Argues for
  non-provisional conversion (PAT-007/008/009) *before* heavy outreach, not after. A
  provisional about to lapse is a weak negotiating position.

- **Body-cam continuity demo — what software alone can/can't prove:**
  - CAN prove today: structural continuity + tamper-evidence (chain is unbroken, ordered).
  - CAN'T prove with software alone: that the chain corresponds to a *continuous real-world
    recording* vs. a continuous chain of independently-signed-but-edited segments.
  - The heartbeat (PAT-013) closes that gap — periodic challenges prove the device was live
    *throughout*. Honest demo claim: "provable structural continuity" now → "provable
    temporal liveness continuity" once challenger exists. Do NOT blur these; an Axon
    engineer catches it instantly.

- **"Strengthens admissibility" discipline cuts both ways:** precise claiming isn't only
  defense against an opposing attorney — it's what makes the pitch credible to Axon's own
  legal team, who are the internal skeptics during any acquisition. Overclaiming
  ("court-protected") kills you twice. Brief's existing language on FRE 901/902 is correct;
  keep it.

---

## Open questions (carried forward)

- **Which track does June 3 actually belong to?** (evidence integrity vs. PUF/hardware) — resolve first.
- Has any open SBIR/BAA topic appeared that fits human-gated optical-challenge attestation
  or evidence continuity? (DoD SBIR cycles, DHS S&T, DOJ/NIJ are the plausible homes.)
  Could search SAM.gov / SBIR.gov / DoD SBIR to confirm fit when ready.
- Which evidence vertical has the most reachable first contact?
- Axon-specific: what would corp-dev / technical team need to see? (partial answer above)

---

## Next actions

- [ ] Confirm whether the June 3 deadline is evidence integrity or the PUF/hardware track.
- [ ] (When ready) Spec the challenger/verifier — the gating unbuilt piece.
- [ ] (Strategic) Sequence non-provisional conversion of PAT-007/008/009 ahead of heavy buyer outreach.
- [ ] (Optional) Search current open SBIR/BAA topics for evidence-integrity fit.

---

*Source brief retained context; safe to delete the working thread after this entry is committed.*
