# ZKNOT.IO — Patent Portfolio Evaluation & 6-Month Acquisition Roadmap
**Inventor:** William Wilkinson | ops@zknot.io | March 2026

> ⚠️ Not legal advice. Consult a registered patent attorney for all filing decisions.

---

## 1. Portfolio Overview

Seven provisional applications covering a vertically integrated cryptographic evidence stack.

| Patent | Core Claim | Status |
|---|---|---|
| PowerVerify | Inline USB device physically blocking data paths while delivering power | Provisional |
| ZKey | Hardware signing device gated by physical human actuation | Provisional |
| TrustSeal | Physical seal cryptographically bound to digital ledger | Provisional |
| ZK-LocalChain | Device-signed cryptographically chained event ledger | Provisional |
| EvidenceProtocol | End-to-end evidence integrity workflow | Provisional |
| Vendor Attestation | Manufacturer-irrevocable lifecycle attestation | Provisional |
| Supplemental Spec | Transport-agnostic attestation output (USB, QR, air-gap) | Supplement |

---

## 2. Portfolio Strengths

**2.1 Vertical Integration Is the Core Moat.** Most competitors patent individual components. Your portfolio patents the entire stack from power delivery to chain of custody. An acquirer must license the whole system to reproduce your workflow.

**2.2 The Human-Gating Claim Is Genuinely Novel.** FIDO2 and YubiKey prove presence to the HOST. ZKey proves presence to an independent OBSERVER. These are different claims. The one-actuation-one-signature rule with the post-challenge actuation requirement is a strong non-obvious combination.

**2.3 Vendor-Hostile Threat Modeling Is Commercially Valuable.** The Vendor Attestation patent models the manufacturer as a potential future adversary — rare in patent literature. Significant standalone licensing potential in consumer electronics, medical devices, automotive, and warranty enforcement.

**2.4 Transport-Agnostic Supplemental Spec Is Well-Drafted.** Covers USB output, QR output, and air-gapped optical output as interchangeable embodiments. Prevents competitors from arguing their device is different because it uses a different output method.

---

## 3. Gap Analysis

### 3.1 CRITICAL — File Immediately

**GAP 1: ZKKey Air Camera Input Is Unpatented.**
ZKey covers OUTPUT via QR but not INPUT via QR — receiving a challenge by optically reading a QR code on a host screen. A competitor can build a camera-input signing device without infringing. ZKKey Air's entire differentiator is unprotected. **Risk: HIGH**

**GAP 2: Short Code Output Method Is Unpatented.**
The supplemental spec mentions "truncated hash" but does not claim the method of deriving a human-readable short attestation code from a full cryptographic signature. This is the feature that makes the product usable by non-technical users. **Risk: MEDIUM-HIGH**

**GAP 3: Firmware State Machine Is Unpatented.**
The patents cover hardware but not the firmware: the armed state after challenge receipt, single-use nonce consumption, canonical hash verification before signing. These method claims block competitors who copy your hardware but rewrite firmware. **Risk: HIGH**

**GAP 4: Combined Session Record Is Unpatented.**
EvidenceProtocol covers the workflow but not the cryptographic data structure binding a PowerVerify session certificate AND a ZKey human-presence signature into a single verifiable record. This is your highest-value unique feature and is currently unprotected. **Risk: HIGH**

### 3.2 MODERATE — File Within 90 Days

**GAP 5: Verification Protocol Is Unpatented.** The steps a third party takes to independently verify a ZK-LocalChain event without manufacturer cooperation are patentable method claims.

**GAP 6: Multi-Party Witness Attestation Is Unaddressed.** Two or more ZKey devices from different users signing the same event — natural extension with major value in elections and legal evidence.

**GAP 7: External Timestamp Anchoring Is Unaddressed.** Anchoring local chain events to RFC 3161 or a public ledger substantially increases evidentiary weight and is a commercially important extension.

**GAP 8: USB-C CC-Line Claims Are Thin.** PowerVerify covers USB-C generally but not the specific CC-line interaction enabling PD negotiation while blocking data paths.

### 3.3 STRATEGIC — File Within 6 Months

**GAP 9: Mobile / Smartphone Integration.** No claims address smartphones as ZKey hosts — NFC, camera scan, or Bluetooth attestation receipt. Major adjacent market.

**GAP 10: Manufacturing Attestation + TrustSeal Binding.** The combination of a device whose manufacturing event is bound to the seal applied at manufacture — supply chain and pharma value.

**GAP 11: Revocation and Key Rotation.** Signed revocation events and key rotation are patentable and essential for enterprise sales.

**GAP 12: API / SDK Interface Claims.** No claims cover the host-side software interface. An API claim prevents commoditization of the hardware.

---

## 4. Acquirability Assessment

| Dimension | Now | Target | Primary Gap |
|---|---|---|---|
| Claim Breadth | 6/10 | 9/10 | Missing firmware, camera input, short code, API |
| Claim Defensibility | 7/10 | 9/10 | Needs continuations + prior art searches |
| Market Size Coverage | 5/10 | 8/10 | Missing mobile, supply chain, enterprise |
| Portfolio Coherence | 8/10 | 9/10 | Strong — vertical integration evident |
| **Overall Acquirability** | **6.5/10** | **9/10** | **12 gaps identified** |

### Most Likely Acquirer Categories

| Acquirer Type | Why They Want It | Lead Asset | Valuation Driver |
|---|---|---|---|
| Forensic / Legal Tech | Chain of custody unsolved at scale | EvidenceProtocol + ZKKey | SaaS + hardware |
| Election Security Vendor | Human-witnessed attestation at scale | ZKKey + TrustSeal | Gov contract moat |
| Cybersecurity Hardware Co. | USB blocking + attestation fills gap | PowerVerify + ZKKey | Enterprise endpoint |
| Journalism / Media Tech | Provenance crisis acute (C2PA, CAI) | Full ecosystem | Licensing + hardware |
| Supply Chain / IoT | Vendor-hostile attestation is novel | Vendor Attestation | Standalone license |

---

## 5. Six-Month Daily Acquisition Roadmap

### MONTH 1: Patent Hardening
*Close the four critical gaps before prior art searches find them.*

**Week 1 — GAP 1 + GAP 2: Camera Input + Short Code**
- Mon: Draft claims for optical QR challenge ingestion — camera, QR parsing, challenge extraction
- Tue: Draft single-use nonce consumption from camera input — new challenge vs replay prevention
- Wed: Draft short-code output claims — method of deriving 6–12 char code from full hash
- Thu: Cross-check both drafts against ZKey and Supplemental Spec for overlap
- Fri: Send to patent attorney for formal claim language conversion

**Week 2 — GAP 3: Firmware State Machine**
- Mon: Document full state machine: idle → challenge received → armed → actuated → signed → output → idle
- Tue: Identify novel transitions: single-actuation rule, post-challenge requirement, nonce invalidation
- Wed: Draft method claims for state machine as patentable sequence of steps
- Thu: Draft system claims for firmware architecture as a device component
- Fri: Send to attorney — file as continuation-in-part of ZKey provisional

**Week 3 — GAP 4: Combined Session Record**
- Mon: Design combined record structure — PowerVerify session cert + ZKey signature + shared session ID
- Tue: Draft claims on the record — cryptographic binding between power session and signing event
- Wed: Draft method claims on generating and verifying the combined record
- Thu: Review against EvidenceProtocol — file as continuation, not new patent
- Fri: Submit supplemental disclosure to attorney

**Week 4 — GAP 5: Verification Protocol + Start Prior Art**
- Mon: Document how a third party verifies a ZK-LocalChain event offline step-by-step
- Tue: Identify non-obvious steps — specifically the vendor-independent verification path
- Wed: Draft method claims for the verification algorithm
- Thu: Review against ZK-LocalChain patent — file as continuation
- Fri: Begin prior art search: USPTO + Google Patents ("USB data blocking", "hardware attestation human presence")

---

### MONTH 2: Prior Art Defense + Provisional Conversions
*Understand the landscape, differentiate claims, convert the strongest provisional.*

**Week 5 — Prior Art: PowerVerify**
- Mon: Search USPTO "USB data blocking power delivery" — document all relevant patents
- Tue: Search "juice jacking prevention hardware" — identify overlapping claims
- Wed: Compare found art against PowerVerify claims — flag any reading on prior art
- Thu: Draft amendments to differentiate — cryptographic session logging is the key differentiator
- Fri: Compile prior art matrix for attorney

**Week 6 — Prior Art: ZKey vs FIDO2**
- Mon: Search "hardware security key physical presence" — YubiKey, FIDO2, CTAP2 patents
- Tue: Document the key distinction: FIDO2 proves presence to HOST. ZKey proves presence to OBSERVER.
- Wed: Search "human-gated signing" and "physical actuation cryptographic"
- Thu: Draft prior art differentiation memo — 1 page per closest reference
- Fri: Share with attorney — this memo becomes the non-provisional claim argument

**Week 7 — Convert ZKey to Non-Provisional**
- Mon: Confirm ZKey as first conversion with attorney (most novel, most defensible)
- Tue–Wed: Work with attorney on independent and dependent claim drafting
- Thu: Review spec completeness — all embodiments including Air variant described
- Fri: File non-provisional ZKey application (watch your 12-month deadline from provisional)

**Week 8 — Competitive Intelligence**
- Mon: Research competitors: Yubico, Ledger, Archivist, Veritone, Witness, Authentica
- Tue: Map their patent portfolios on Google Patents — gaps in their coverage
- Wed: For each: where do you compete, where do you complement?
- Thu: Build competitor landscape: company / products / relevant patents / your advantage
- Fri: This becomes your acquirer pitch competitive moat section

---

### MONTH 3: Product + Patent Alignment
*Every key patent claim demonstrated by working hardware.*

**Week 9 — PowerVerify Rev C**
- Mon: Audit Rev B — identify any patent claim not demonstrated by current hardware
- Tue: Add ATECC608 session signing to Rev C if not present — this is the key differentiating claim
- Wed: Add session ID generation to firmware
- Thu: Order Rev C from JLCPCB — corrected Gerbers, no paste on fingers, correct mask openings
- Fri: Begin session parameter signing firmware

**Week 10 — ZKKey Connect Firmware**
- Mon: Implement formal state machine from Week 2 documentation
- Tue: Implement canonical hash verification before signing
- Wed: Implement nonce consumption flagging — each nonce marked used after signing
- Thu: Implement OLED short code display
- Fri: Full flow test: challenge → arm → actuate → sign → display

**Week 11 — ZKKey Air Camera Integration**
- Mon: Evaluate camera modules — OV2640 vs HM01B0 for QR decode performance on STM32
- Tue: Integrate QR decode library — test speed and reliability
- Wed: End-to-end test: laptop shows QR → ZKKey Air reads it → signs → displays short code
- Thu: Document camera input flow in detail for patent continuation
- Fri: Order ZKKey Air Rev A PCBs

**Week 12 — Evidence Chain Demo**
- Mon: Build full demo: PowerVerify charges device → ZKKey signs → TrustSeal applied → chain recorded
- Tue: Implement ZK-LocalChain MVP: event creation, chaining, offline verification
- Wed: Record demo video showing all products working together
- Thu: Write 1-page technical brief: "How ZKNOT.IO Creates a Verifiable Evidence Record"
- Fri: Finalize — demo video and brief are your primary acquisition pitch assets

---

### MONTH 4: Commercial Packaging
*Materials that make an acquirer confident enough to sign an NDA.*

**Week 13 — Patent Portfolio Summary Deck**
- Mon: 1 page per patent: claim, diagram, prior art differentiation, market application
- Tue: Portfolio map showing how all 7 patents interlock into the ecosystem
- Wed: Design-around difficulty analysis — how hard is it to work around each patent?
- Thu: Claim chart for top 3 target acquirers showing exactly which claims they need
- Fri: Attorney review for accuracy

**Week 14 — Market Size Documentation**
- Mon: Research forensic evidence tech TAM — analyst reports
- Tue: Research election security hardware market size
- Wed: Research USB security / endpoint protection market
- Thu: Research media authenticity / content provenance market (C2PA, Content Authenticity Initiative)
- Fri: Combined TAM slide — your patents address multiple billion-dollar markets

**Week 15 — Revenue Model**
- Mon: Hardware: unit cost, sell price, margin per product
- Tue: Licensing: per-device royalty, annual license, OEM integration
- Wed: SaaS: ZK-LocalChain as hosted verification service
- Thu: 3-year pro forma: path to $10M ARR under each model
- Fri: Stress-test assumptions — what must an acquirer believe for each model?

**Week 16 — Outreach Preparation**
- Mon: Identify 20 target acquirers across the 5 categories
- Tue: For each: find the right contact (VP Eng, Chief IP Counsel, Head of M&A)
- Wed: Write 3-sentence teaser email — lead with the problem solved, not patent count
- Thu: Prepare 1-page NDA-free overview: what products do, what patents cover, what you seek
- Fri: Attorney review of NDA-free overview for inadvertent disclosure

---

### MONTH 5: Acquirer Outreach
*Get a technical call. You are not selling yet — you are getting in the room.*

**Week 17 — Tier 1 Outreach (Top 5 Targets)**
- Mon: Send personalized teasers — reference the specific problem their product has that yours solves
- Tue: Connect on LinkedIn — brief note, no pitch
- Wed: Follow up Day 1 emails if no response
- Thu: Research whether any targets attend RSA, DEF CON, evidence, or journalism conferences
- Fri: Prepare for technical calls — know your claims cold, know the prior art cold

**Week 18 — Tier 2 Outreach + Licensing Track**
- Mon: Send to next 10 targets
- Tue: For any responses: schedule calls within 48 hours while interest is warm
- Wed: Prepare licensing term sheet template: field-of-use, per-unit royalty, exclusivity options
- Thu: Research patent brokers specializing in hardware/security IP
- Fri: Contact 2–3 brokers for valuation opinions — dual track sell vs license

**Week 19 — Technical Calls**
- Mon–Tue: Conduct scheduled calls — lead with demo, follow with patent discussion
- Wed: Post-call: send portfolio summary and specific claim chart for their use case
- Thu: Document objections raised — these reveal claim weaknesses
- Fri: Debrief with attorney on any technical questions about claim scope

**Week 20 — Non-Provisional Conversions: Round 2**
- Mon: Begin PowerVerify non-provisional with attorney
- Tue–Wed: Work on PowerVerify claims — session logging as the key differentiator
- Thu: Begin Vendor Attestation non-provisional — strong standalone licensing value
- Fri: File or schedule filings

---

### MONTH 6: Close or Fund
*Term sheet with an acquirer — or pivot to fundraising with portfolio as primary asset.*

**Week 21 — Valuation + Deal Structure**
- Mon: Get formal IP valuation from certified IP valuation firm — required for any serious deal
- Tue: Research comparable deals: hardware security patent portfolio acquisitions 2022–2025
- Wed: Define your deal spectrum: outright sale / license / acqui-hire / investment
- Thu: Model each structure's 3-year personal outcome
- Fri: Decide your walk-away position before entering any negotiation

**Week 22 — Due Diligence Preparation**
- Mon: Compile clean patent file: confirmations, serial numbers, key dates for all 7
- Tue: Compile hardware designs, Gerbers, BOMs in clean data room
- Wed: Compile firmware source code with comments — acquirers want to see it is real
- Thu: Compile customer evidence: LOIs, pilot discussions, production orders
- Fri: Attorney reviews data room — what not to disclose pre-NDA

**Week 23 — Parallel Fundraising Track**
- Mon: If no acquisition: pivot to seed round — patent portfolio is primary asset
- Tue: Identify 15 seed investors: deep tech, security hardware, evidence tech
- Wed: Adapt acquisition deck to investor deck — market opportunity replaces acquirer value
- Thu: Submit to HAX (hardware accelerator), Y Combinator, Bolt
- Fri: Apply to SBIR grants: DoD (forensics/evidence integrity) and DHS (election security)

**Week 24 — Review + Regroup**
- Mon: Review all outreach results — which categories responded, which did not
- Tue: If deal in progress: 100% focus on closing
- Wed: If no deal: identify what portfolio change unlocks the next conversation
- Thu: File any remaining gap patents from Section 3
- Fri: Update this document and the AI context document — record what worked, plan Month 7–12

---

## 6. Priority Action Summary

| Priority | Action | Deadline |
|---|---|---|
| P0 CRITICAL | File: ZKKey Air camera/optical input claim | Week 1 |
| P0 CRITICAL | File: Firmware state machine method claims | Week 2 |
| P0 CRITICAL | File: Combined session record (PowerVerify + ZKey) | Week 3 |
| P0 CRITICAL | File: Short code / truncated hash output method | Week 1 |
| P1 HIGH | Prior art search: PowerVerify vs juice jacking patents | Week 5 |
| P1 HIGH | Prior art search: ZKey vs FIDO2 / YubiKey / CTAP2 | Week 6 |
| P1 HIGH | Convert ZKey to non-provisional | Week 7 |
| P2 MEDIUM | File: Verification protocol method claims | Week 4 |
| P2 MEDIUM | File: Multi-party witness attestation | Month 3 |
| P2 MEDIUM | Convert PowerVerify to non-provisional | Month 5 |
| P2 MEDIUM | Convert Vendor Attestation to non-provisional | Month 5 |
| P3 STRATEGIC | File: Mobile / smartphone integration | Month 4 |
| P3 STRATEGIC | File: API / SDK interface claims | Month 4 |
| P3 STRATEGIC | Apply to SBIR grants (DoD, DHS) | Month 6 |

---

*ZKNOT.IO — CONFIDENTIAL — All inventions provisional patent pending — William Wilkinson*
*Not legal advice. Consult a registered patent attorney for all filing decisions.*
