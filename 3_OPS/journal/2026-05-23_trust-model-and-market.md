# Trust Model & Market — Use Cases, Privacy Fork, Anchoring, and the Regulatory Pressure-Test

**Date:** 2026-05-23
**Author:** William Shane Wilkinson
**Context:** Pre-SBIR (Phase I deadline June 3) thinking session. Worked through what the human-actuated + independently-verifiable signing architecture is *for*, where the market actually is, and where the central market assumption is weak. This entry is the spine of the commercialization / impact narrative.

---

## 1. Core distinctive property

A signature that **cannot be produced without a live human physically actuating at the moment of signing**, with that action **bound to the specific thing being signed** (FSM-gated human-actuation-while-displaying-hash). Plus **independent verifiability** — a third party confirms genuineness without trusting the signer, ZKNOT, or any central authority.

This rules out a class of attacks normal signing keys can't: remote automation, key exfiltration, "malware signed it while you slept."

## 2. Use-case landscape

- **Proof-of-human-presence / anti-automation.** High-value financial authorizations; defeating bot/agentic abuse; consent, voting, regulatory attestation. As AI agents proliferate, "a human actually did this" becomes scarce and valuable.
- **Supply chain & physical provenance** (PUF + actuation together). PUF binds to the object, actuation binds to the human moment. Chain-of-custody for evidence, pharma, defense components, luxury goods.
- **Legal & compliance.** Non-repudiable consent; tamper-evident human-authorized audit trails (ZK-LocalChain).
- **Defense / federal** (SDVOSB/SBIR lane). Two-person integrity, positive human control, attestation that a human — not a spoofed/automated process — authorized a release/command.

Independent verifiability is what separates this from a YubiKey: verify after the fact without phoning home to an issuer.

## 3. The surveillance / privacy fork (shadow side)

Nothing in the core architecture *prevents* a coercive deployment: issue everyone a ZKKey, mandate it per decision, log every ZK number against an identity. Non-repudiation and surveillance are the same coin — "the signer can't deny it" is a feature for consent and a weapon for a coercive employer.

Two mitigations / honest limits:
- **ZK can prove a predicate, not an identity.** If verification proves *authorized / present / consenting* (group membership) rather than *which person*, the spreadsheet-of-everyone's-decisions attack weakens — there's no identity to log. **Open design question: does our current verification reveal individual identity or just authorization?** This answer determines the privacy stance. RESOLVE THIS.
- **Actuation is a coercion surface.** "A human did this" ≠ "a human consented." Can't fully engineer away; be honest rather than oversell.

## 4. The GRC / audit-acceleration use case (the grounded one)

Reframe of the above as a *good* use case: a document carrying a ZK number that resolves to a verifiable attestation (this hash, this timestamp, authorized actuation) collapses the auditor's job from *reconstructing* evidence to *checking* it.

- **Control testing** becomes binary and fast — valid attestation or not, no judgment on whether a screenshot is doctored.
- **Evidence integrity** for SOC 2 / ISO 27001 / FedRAMP — "this is the approved version, unaltered" becomes provable, not asserted.
- **Continuous / automated audit** — the bigger play. Machine-verifiable attestations move the industry from point-in-time to continuous assurance.

Crucially, GRC needs only a **predicate** (authorized + timestamped + unaltered), *not* identity. So the most commercially attractive use case is also the privacy-respecting one. Nice alignment. The verification must be genuinely independent (auditor checks it without calling us) — which is the property already built.

## 5. Anchoring stack — three separable trust properties

| Layer | Mechanism | Property it provides | Limit |
|---|---|---|---|
| Actuation binding | FSM-gated human action + PUF | *Who/what at creation* | Doesn't secure ordering or later tampering |
| ZK-LocalChain | Hash-linked records (genesis ZK-6GUA-7DV @ pos 0) | *Internal ordering & tamper-evidence* | It's *our* chain — tamper-evident vs outsiders, not tamper-proof vs operator |
| External anchor | Merkle root → public blockchain **or** RFC 3161 timestamp authority | *Operator-independent proof-of-existence by a time* | Proves existence/integrity, NOT correctness |

How public anchoring works: batch many local records, take a Merkle root, write that single hash to a public chain periodically. One transaction covers thousands of attestations. Altering any record changes the root, which won't match the chain. (Same model as Certificate Transparency / OpenTimestamps.)

**What's easy to miss (overclaim traps):**
1. Anchoring proves existence + integrity, **not correctness/truth**. "Blockchain-verified" only ever means "existed and unaltered."
2. **Oracle / input-integrity problem.** Anchoring secures everything *after* attestation. Garbage in → an immutable, verifiable record of a lie. Actuation defends the *front*; chain defends the *back*; neither covers the other.
3. **Metadata leak.** Anchor timing/frequency is public. Batch at fixed intervals, never per-event. (Don't reintroduce the surveillance leak through the anchoring layer.)
4. **Cost & permanence.** Per-tx cost; chain choice is a long-term dependency (Bitcoin/Ethereum = conservative). "Permanent" cuts both ways vs GDPR erasure — anchor only opaque hashes, never a personal-data fingerprint.
5. **May not need a public chain at all.** Federal/enterprise GRC may be satisfied by LocalChain + RFC 3161 TSA — cheaper, faster, privacy-preserving, already accepted. Public chain is the right answer *only* when zero trusted parties are permitted in the verification path. Match the tier to the customer's trust model; don't reach for "blockchain" reflexively.

**Framing:** actuation = who/what at creation; LocalChain = ordering; external anchor = operator-independent existence. Three distinct properties, three mechanisms. Strength of the pitch is honesty about which layer does which.

## 6. Market thesis — answering "most people trust the system enough, this is overkill"

The objection is **mostly right**, and conceding that is more credible than fighting it everywhere.

- **Truth:** for the vast majority of transactions, ambient trust is sufficient and cheaper. Most of the economy runs on good-enough trust — an efficient equilibrium, not a failure. "Verify everything" is a losing pitch.
- **Right question:** not "is trust usually enough" (yes) but "where does usually-enough trust fail *badly*, and is that failure expensive enough to pay to prevent?"

**Three forces eroding the equilibrium (why it's a *growing* market):**
1. **AI is destroying cheap trust signals.** Fabrication used to be expensive; now it's a prompt. "Looks legitimate" stops being evidence. Proof-of-human-actuation gains value precisely because "a human did this" becomes the scarce, expensive-to-fake signal. Tailwind that didn't exist 3 years ago — the part the objection hasn't priced in.
2. **Adversarial / high-coercion environments.** Defense, critical infra, evidence chains, high-value finance. Counterparty assumed hostile; "trust the system" not available by definition. (= our lane.)
3. **Regulatory mandate, not desire.** The buyer doesn't *want* verification — they're *required* to produce it for a third party (auditor, regulator, court) who won't take their word. Non-discretionary demand = cleanest market. (= GRC thread.)

**What the market actually is:** the intersection of *high consequence of failure* + *adversarial/untrusting verifier* + (*regulatory requirement* OR *irreversible outcome*). Beachhead = **regulated/compliance-driven attestation + defense/federal human-control assurance.** Small as a share of transactions, large in dollars, growing.

**Losing markets (be honest):** consumer-convenience; anywhere "good enough" works and fraud is rare and recoverable. Don't fight there.

**The line for the interviewer:** *"You're right that most trust is good enough — and we're not selling to most. We sell where good-enough trust is collapsing under AI-generated fraud, or was never permitted because a regulator or adversary is in the loop. That set is small as a share of transactions, large in dollars, and growing because fabrication is getting cheaper."* Concede the 90%, win the 10%.

## 7. The weak link — and the regulatory pressure-test

**Weakest assumption in the whole thesis:** will beachhead buyers pay for *our* mechanism vs a cheaper "good enough" option (plain hardware token, timestamp authority)? The actuation binding must be **load-bearing for a real requirement**, not just elegant.

**Finding from checking the two closest regs (verified 2026-05-23):**
- **NIST 800-53 AU-10 (Non-repudiation):** requires *irrefutable evidence that an individual performed an action* as a **property**, and explicitly names **digital signatures and digital message receipts** as acceptable mechanisms. Does NOT mandate human-presence proof. (See also AU-10(2) validate-binding-of-producer-identity via cryptographic checksums, AU-10(3) chain of custody.)
- **FDA 21 CFR Part 11 §11.200:** strictest mainstream signature rule. Requires *at least two distinct identification components (e.g., ID code + password)*, all components on first signing in a continuous session, re-auth (all components) for signings outside a single session. A username+password satisfies the "deliberate act." Does NOT mandate our actuation mechanism.

**Conclusion — brace for this:** it's a spectrum, not yes/no. *Almost no regulation names our exact mechanism; most name a property our mechanism satisfies; a few (Part 11 deliberate-act, nuclear two-person, AU-10 non-repudiation) come close enough to argue we're the best available way to meet them.* That is still a real business — "best evidence for a property regulators already require" — but it is a **different and harder sell** than "the only thing that satisfies an unmet mandate." Danger: believing the second when the truth is the first.

**Where to pressure-test (in order of likely hard-mandate):**
1. **Nuclear/defense two-person & positive human control** — DoD nuclear surety two-person concept; DoDD 3000.09 (human judgment in autonomous weapons). Likely demands presence *procedurally* but not as a *cryptographic artifact* — that's the gap we may fill (better evidence, not unmet mandate).
2. **FDA 21 CFR Part 11** — deepest signature-specific reg; pharma/biotech deep pockets. "Deliberate act" + re-auth is the closest mainstream concept. (Checked above.)
3. **eIDAS Qualified Electronic Signatures (EU)** — "sole control" ≈ actuation binding, but tech-neutral and satisfied by existing QSCDs. Property specified, mechanism not.

**Where requirements become operational (test here, not just the law text):**
- **Audit/certification criteria, not laws.** NIST 800-53A assessment procedures; AICPA Trust Services Criteria (SOC 2); read AU-10 verbatim. This is where "demanded vs benefits-from" gets decided in reality.
- **Actual federal solicitation language** (highest-leverage, privileged access via SAM.gov). Grep SAM.gov / beta.SAM / DSIP topics for: "positive human control," "non-repudiation," "human-in-the-loop," "two-person integrity," "proof of presence," "anti-spoofing." A *solicitation* using these as requirements >> a regulation that merely permits it.
- **People who fail audits.** GRC officers, pharma QA/regulatory-affairs, federal ISSOs. Cutting question: *"Have you ever been dinged by an auditor or lost a contract specifically because you couldn't prove a human authorized something?"* Recurring yes = mandate-driven market. "No, password e-sign passes fine" = benefit, not requirement — need to know NOW.

**Single highest-leverage immediate test (before June 3):** pull the exact text of the SBIR topic being responded to and grep it for human-control / non-repudiation / presence language. That document either demands what's built or it doesn't — decisive and immediately available.

---

## Action items
- [ ] **RESOLVE:** does current verification reveal individual identity or only authorization (predicate)? Determines privacy stance + GRC fit.
- [ ] **BEFORE JUNE 3:** grep the target SBIR topic text for human-control / non-repudiation / presence / two-person / anti-spoofing language.
- [ ] Decide anchoring tier for first customer (public chain vs RFC 3161 TSA) based on their trust model.
- [ ] Validation campaign (post-June 3): NIST 800-53A assessment procedures; SOC 2 TSC; interview GRC officers / pharma QA / federal ISSOs with the "have you ever been dinged" question.
- [ ] Pull SAM.gov / DSIP solicitations and grep for the requirement keywords.

## One-line throughline (for the proposal)
Actuation binding (who/what at creation) + LocalChain (ordering) + external anchor (operator-independent existence) = three separable trust properties; predicate verification keeps us privacy-side; the market is the small-but-growing intersection where AI-eroded trust or a regulator/adversary makes "good enough" unavailable — and we are the **best evidence for a property regulators already require**, not the only thing satisfying an unmet mandate.
