# ZKNOT SOP Library — Dependency-Ordered Backlog

**Created:** 2026-05-18
**Author:** Shane Wilkinson
**Status:** Parked behind hardware product completion
**Trigger to start executing:** ZKKey Connect and ZKKey Air both in sellable format (prototype validated, JLCPCB orders received, case design complete, listing ready)

---

## Why this is parked

The SOP library is one of the highest-leverage marketing moves available to ZKNOT, but it has a hard prerequisite: **the hardware products it references must be real and orderable.** Publishing "Mobile Device Seizure SOP" with PowerVerify in the tool-options table when PowerVerify is the only ZKNOT product live is fine; publishing "Election Equipment Power Attestation" with both PowerVerify and a "ZKKey for sign-offs" reference when ZKKey isn't shippable yet creates a credibility gap. A procurement officer who reads the SOP and tries to buy ZKKey gets a "coming soon" page. That's worse than not publishing.

So: finish the hardware. Then ship SOPs.

The current state of hardware roadmap (per journal `2026-05-08_strategy_pivot_pico_first.md`):
- **PowerVerify AirGap** — live, selling at $39
- **ZKKey Connect** — Pico-based prototype in progress, KiCad → JLCPCB → firmware
- **ZKKey Air** — also Pico-based (pivoted from STM32), more complex (camera, battery), follows Connect
- **ZK-LocalChain** — backend live at api.zknot.io, no consumer product surface yet
- **TrustSeal** — referenced on zknot.io, productization status unclear

The SOP backlog assumes ZKKey Connect AND ZKKey Air are both buyable before the substantial publishing push begins.

---

## How to use this document

When you return to this work, do not try to do all of it. The document is structured so that:

1. **Phase 0** is what to do *now* (before hardware ships) to keep momentum without overcommitting.
2. **Phase 1-3** are the actual publishing sequence, ordered by dependency, not by topic interest.
3. **Phase 4** is "expansion mode" — only enter if Phases 1-3 produce measurable signal.

Each SOP has:
- **Trigger condition** — what must be true before this gets written
- **Estimated effort** — rough order of magnitude
- **Prerequisites** — what must be done first
- **Strategic value** — why this one and not others

---

## Phase 0 — Pre-Hardware Tasks (do these in parallel with KiCad work)

These are tasks that *don't* require ZKKey Connect or Air to be shippable. Many of them are content-only, audience-research, or infrastructure that takes time but doesn't block hardware.

### P0.1 — Talk to one real customer before writing anything

**Trigger:** Anytime
**Effort:** 2-3 conversations, 30 min each
**Prerequisites:** None

The biggest risk in this whole backlog is writing SOPs Claude and I think are valuable that actual buyers find irrelevant. Before writing any SOP, have at least one conversation with someone in each target audience.

For SOP authors, ask:
- *"You currently have to write/maintain SOPs for [domain]. What does the existing landscape get wrong?"*
- *"If a free, vendor-neutral SOP existed for [topic], where would you expect to find it?"*
- *"What would make you cite an SOP in a real audit binder vs. ignore it?"*

Three audiences are tractable to reach without warm intros:
- Police chief technology officers (LinkedIn cold outreach works; they're underserved)
- Compliance managers at small/mid defense contractors (CMMC anxiety is universal)
- Election integrity officials at the county level (often individuals named on public county pages)

**Output:** Three pages of notes. Drop them in `~/ZKNOT/3_OPS/journal/sop_customer_research.md`.

---

### P0.2 — Audit the existing $79 Gumroad Compliance Series

**Trigger:** Anytime
**Effort:** 2-3 hours
**Prerequisites:** None

Pull up the Compliance Series. Read it as if you were a free-SOP reader who landed on procedures.zknot.org. Answer:

- Which content is broad-spectrum (belongs in free SOPs)?
- Which content is deep-dive practitioner detail (stays on Gumroad)?
- Are there sections that could be free *and* paid simultaneously, with the paid version being a more detailed elaboration?

**Output:** A two-column mapping in `~/ZKNOT/3_OPS/journal/compliance_series_audit.md`. Left column: section of the Gumroad series. Right column: free / paid / both, with justification.

This is the prerequisite for any decision about whether the free SOP library cannibalizes Gumroad revenue. Spoiler: it almost certainly doesn't — free SOPs are a different product for a different buyer — but you should verify by actually reading the existing content.

---

### P0.3 — Write the standing references library

**Trigger:** Anytime
**Effort:** 4-6 hours
**Prerequisites:** None

Every SOP cites standards (NIST 800-86, ISO 27037, ACPO Guidelines, FRE 901, etc.). Build a single markdown file of standards that get cited across SOPs, with proper bibliographic detail. Format:

```
NIST SP 800-86 — Guide to Integrating Forensic Techniques into
Incident Response. National Institute of Standards and Technology,
2006. https://csrc.nist.gov/publications/detail/sp/800-86/final

  Used in: Mobile Device Seizure (P1.1), Digital Evidence
  Acquisition (P2.1), Bodycam COC (P1.2)
```

**Output:** `~/ZKNOT/3_OPS/journal/sop_standards_reference.md`. Reusable across every SOP. Writing this once saves you research time on every subsequent document.

---

### P0.4 — Establish `procedures@zknot.org` mailbox

**Trigger:** After Google Workspace verification completes for zknot.org
**Effort:** 30 minutes
**Prerequisites:** Workspace setup completion (already in progress per the ecosystem journal)

The methodology page and every SOP footer cite `procedures@zknot.org` as the corrections contact. Make sure mail actually flows. Test by sending yourself a correction from a different account.

---

### P0.5 — Decide on professional review partnerships

**Trigger:** Before publishing v1.0 of the first SOP
**Effort:** 2-3 weeks of email outreach
**Prerequisites:** None blocking — start when ready

The methodology page currently says *"We do not currently engage outside professional reviewers... When a procedure has been reviewed by a named outside professional, that fact is stated on the procedure's cover page."* The honest framing buys you time, but professional review eventually becomes a credibility multiplier.

Three categories to explore:
- **CMMC Registered Practitioner (RP)** for the CMMC-adjacent SOPs. Costs $500-2000 per document review. Worth it for the CMMC SOP specifically.
- **Cybersecurity attorney** for chain-of-custody SOPs that might appear in litigation. Look at people who already publish on this topic.
- **Subject matter expert per vertical** — a former police evidence custodian, a former election clerk, a former CFO who's handled SOX. Often willing to review for credit + small honorarium.

**Output:** A shortlist of 5-10 names by category in `~/ZKNOT/3_OPS/journal/sop_reviewers_shortlist.md`. Don't engage them until you have a real SOP draft ready.

---

## Phase 1 — Foundation SOPs (publish after both ZKKey products are sellable)

These three are the foundation. They establish the format, the editorial voice, the search-engine presence, and the basic credibility. **Each one must reference at least two ZKNOT products that are actually buyable.** That's why they're parked.

### P1.0 — Complete ZKNOT-SOP-001: Digital Evidence Chain of Custody

**Trigger:** ZKKey Connect orderable + Phase 0 tasks complete
**Effort:** 20-30 hours of writing
**Prerequisites:** P0.1 (customer conversations), P0.2 (Gumroad audit), P0.3 (references library), P0.5 (at least one reviewer engaged), ZKKey Connect listing live

This is the first real publication. The placeholder is already at `procedures.zknot.org/procedures/digital-evidence-chain-of-custody/`. Replace the draft content with v1.0.

**Why first:** It's the broadest-spectrum SOP, applicable across law enforcement, journalism, corporate forensics, and education. It establishes the format. Adapting from the existing Gumroad Compliance Series gives you content you already authored.

**What this SOP must include:**
- Scope section (who this is for, what it covers, what it doesn't)
- Numbered procedure sections: receiving custody, maintaining custody, transferring custody, producing for audit/court, disposing of evidence
- Tool-options tables at every step. Each step's table must include: ZK-LocalChain (audit log), ZKKey Connect (sign-offs), plus 2-3 named competitors per category
- Verification criteria — the audit questions an examiner asks
- References to NIST SP 800-86, ISO 27037, ACPO Guidelines, FRE 901
- Standing disclosure footer
- Document ID badge: ZKNOT-SOP-001

**The hard part:** Vendor-neutrality discipline. If you find yourself writing "ZK-LocalChain provides X better than competitors," delete the sentence. The procedure describes the *step*; the tools table lists the *options* alphabetically. ZKNOT's advantage is established by the reader noticing it, not by you asserting it.

---

### P1.1 — ZKNOT-SOP-002: Bodycam Footage Chain of Custody

**Trigger:** ZKNOT-SOP-001 v1.0 published and live for at least 30 days
**Effort:** 30-40 hours
**Prerequisites:** P1.0 complete, P0.1 conversations with law enforcement, ZKKey Connect + ZK-LocalChain both verifiably orderable

**Why second:** Most well-defined audience, clearest pain point, ZKNOT has real differentiation. Police procurement officers actively search for SOPs like this and the existing landscape is genuinely terrible — vendor whitepapers from Axon, outdated DOJ guidance, fragmented agency policies. There's a real hole to fill.

**Critical pre-write step:** Read the latest Bureau of Justice Statistics report on bodycam adoption (the audience for this SOP is bigger than most people realize — most U.S. police departments now use them) and at least three existing agency policies (these are public records, easy to find). Don't reinvent — improve on what exists.

**Caveat to plan for:** Bodycam is politically charged in some directions. Stay procedural. Don't editorialize on police use of force, recording policies, or release laws. The SOP is about *integrity of the recorded artifact*, not the policy debate.

**Tool-options tables must include:**
- Axon Evidence.com (the 800-pound gorilla)
- Veritone Redact
- Genetec Clearance
- ZK-LocalChain
- Generic hashing utilities

Each one listed alphabetically with no preferencing.

---

### P1.2 — ZKNOT-SOP-003: CMMC 2.0 / DFARS 252.204-7012 Evidence Retention

**Trigger:** ZKNOT-SOP-002 v1.0 published, at least one CMMC RP engaged for review
**Effort:** 40-50 hours (CMMC is dense)
**Prerequisites:** P1.1 complete, CMMC RP reviewer engaged, ZKKey Connect orderable, possibly a CMMC-specific PowerVerify use case documented

**Why third:** Your SDVOSB credentials make this the single most direct path to federal contracting conversations. Defense contractors are desperate for CMMC guidance and most of what's available is bloated sales-driven material from CMMC consultancies charging $50K+ for what should be a $200 document.

**Critical caveat:** CMMC 2.0 implementation timeline is still moving. The rule was finalized in late 2024 but contract-level enforcement phases differently across DoD components. **Do not publish without a current CMMC RP review.** Outdated CMMC content is worse than no content — it actively damages credibility.

**The right structural play:** This SOP is the public lead magnet for a future paid sop.zknot.io product (CMMC SOP customization). Make the free version genuinely useful but leave room for "you can buy a customized version of this here." The free version teaches the framework; the paid version applies it to a specific contractor's environment.

---

## Phase 2 — Vertical Expansion (after Phase 1 produces measurable signal)

Only enter Phase 2 if Phase 1 produces at least one of these signals:

- A procurement officer or compliance professional cites an SOP in public correspondence
- A journalist or academic links to an SOP in published work
- Inbound contact through `procedures@zknot.org` from someone in a target audience asking when more SOPs are coming
- Measurable organic search traffic (>100 unique visitors/month to a single SOP page)

If you publish Phase 1 and get *no* signal in 90 days, the strategy needs review. Don't keep writing into a void.

### P2.1 — ZKNOT-SOP-004: Election Equipment Power Attestation

**Trigger:** Phase 1 signal achieved AND election year timing favorable
**Effort:** 30-40 hours
**Prerequisites:** P1.0-1.2 complete, conversations with at least one county election official, careful political-tone review

**Why this one, why with care:** PowerVerify's positioning maps directly onto election equipment use cases. The audience exists (5,000+ U.S. election jurisdictions). The audience also includes people with strong political opinions, and an election-security SOP will be read partisan-tribally regardless of how technical you keep it.

**Mitigation:** Get review from someone with bipartisan election integrity credibility — the Brennan Center, CISA's election security division, a state-level election director. Don't publish without external eyes.

**Tool-options must include both major voting system vendors** (ES&S, Dominion) alongside ZKNOT products. If a partisan reader sees only ZKNOT alternatives to one vendor or the other, the document will be perceived as partisan.

---

### P2.2 — ZKNOT-SOP-005: Mobile Device Seizure & Power-State Preservation

**Trigger:** P2.1 published, law enforcement audience engaged
**Effort:** 20-25 hours
**Prerequisites:** P2.1 complete, the bodycam SOP (P1.1) producing some inbound, PowerVerify production volume capable of handling LE procurement

**Why later than you'd think:** It's a great fit for PowerVerify but the audience overlaps heavily with the bodycam SOP audience. Publishing both close together is fine if P1.1 has built authority; publishing this one without P1.1 first wastes the differentiation.

---

### P2.3 — ZKNOT-SOP-006: Field Reporting Evidence Capture (Journalism)

**Trigger:** Phase 1 signal achieved, ZKKey Air orderable (this is the SOP where ZKKey Air's positioning matters most)
**Effort:** 25-30 hours
**Prerequisites:** ZKKey Air sellable, at least one conversation with a working journalist or press freedom org

**Strategic note:** This SOP is where the editorial values of the .org get visibly tested. Journalists are some of the most skeptical readers in the world about vendor-published material. Getting cited by even one credible press freedom organization (Freedom of the Press Foundation, CPJ, RSF) is worth more than 50 federal contractor reads.

---

### P2.4 — Addendums (drop-in, low-effort, high-utility)

**Trigger:** Anytime after Phase 1
**Effort:** 5-10 hours each
**Prerequisites:** Phase 1 complete

The addendums are 2-3 page documents that drop into existing customer SOPs. They're often more useful than full standalone SOPs because they slot into workflows the customer already has.

Publish in this order:
1. **A-001: USB Power Isolation Addendum** — directly supports PowerVerify sales, very short, easy to write
2. **A-002: Hardware-Attested Sign-Off Addendum** — supports ZKKey Connect, short
3. **A-003: Append-Only Audit Logging Addendum** — supports ZK-LocalChain
4. **A-004: Physical Tamper-Evidence Addendum** — supports TrustSeal (only if TrustSeal becomes a real product)
5. **A-005: Cryptographic Receipt Generation Addendum** — supports the whole stack

Each one ~1500 words. Each one points back to a related full SOP. Each one is reusable across multiple full SOPs as a sub-reference.

---

## Phase 3 — Specialized Verticals (if Phase 2 succeeds)

Only enter Phase 3 if Phase 2 produces multi-vertical traction. Each of these is roughly 30-40 hours of writing and requires domain-specific reviewer engagement.

In rough priority order:
- **ZKNOT-SOP-007: HIPAA Audit Trail Requirements** (healthcare audience, narrow but well-funded)
- **ZKNOT-SOP-008: E-Discovery Production Integrity** (legal audience, very specific buyer)
- **ZKNOT-SOP-009: OT/ICS Maintenance Window Evidence Trail** (industrial audience, growing as ransomware concerns rise)
- **ZKNOT-SOP-010: Clinical Trial Data Integrity (FDA 21 CFR Part 11)** (pharma audience, high revenue per customer)

The remaining SOPs from the 47-doc taxonomy in the ecosystem journal can be considered Phase 4+ — write them only on direct customer request.

---

## Phase 4 — Pivot to sop.zknot.io (paid customization)

**Trigger:** procedures.zknot.org has 6+ published SOPs, demonstrated organic traffic, and at least one customer who has asked "can I get a customized version of this for my company?"

That last question is the green-light for sop.zknot.io v1. Until someone asks, the paid product is premature.

When you reach this trigger, the next thread starts by reading both the ecosystem journal and this backlog document, then executes the build plan documented in the `zknot_thread_handoff.md` under "Task B."

---

## What I won't add to this backlog

A few things were in the brainstorm but should *not* be in your active queue:

- **Whistleblower/dissident operational security SOPs.** These are public-interest valuable but the audience is wrong for ZKNOT's commercial trajectory and they create unmanaged legal/political risk. Write them later, when you have organizational maturity to support them properly.
- **Personal/individual SOPs (litigation timestamping, family estate).** Niche, fragmented audience, low strategic value. Skip unless someone specifically requests one.
- **Humanitarian aid, climate data, cultural heritage, refugee documentation.** All valuable, none commercially aligned for first-decade ZKNOT. These are charitable contributions to other organizations' missions, not ZKNOT publishing priorities.

---

## Daily-driver question when you return to this work

Whenever you sit down to work on the SOP library, ask one question first:

**"What signal have I gotten since the last SOP I wrote?"**

If the answer is "none," the next move is NOT writing another SOP. The next move is outreach, audience-building, or improving the published ones based on reader feedback. Writing more documents into a void is the failure mode this backlog is structured to prevent.

The discipline is: **one SOP, then signal, then next SOP.** Not: ship the backlog.

---

## Cross-references

- Ecosystem state: `~/ZKNOT/3_OPS/journal/2026-05-17_ecosystem_state.md`
- Thread handoff for future Claude sessions: `~/ZKNOT/3_OPS/journal/zknot_thread_handoff.md`
- Hardware pivot (Pico-first): `~/ZKNOT/3_OPS/journal/2026-05-08_strategy_pivot_pico_first.md`
- Procedures site source: `~/procedures-zknot-org-site/`

— End of backlog —
