# ZKNOT, Inc. — Patent Attorney Engagement Brief
## Document: ZKNOT_ATT-BRIEF-001_20260328
## Prepared by: William Shane Wilkinson, Founder & Inventor
## Contact: ops@zknot.io | UEI: C4SKW13JPEL5 | CAGE: 1AHZ4

---

## WHO WE ARE

ZKNOT, Inc. is a Utah-based Service-Disabled Veteran-Owned Small Business (SDVOSB) building hardware attestation and chain-of-custody products for government, law enforcement, election auditing, forensic journalism, and pharmaceutical supply chain. SAM.gov registration is ACTIVE.

**Core doctrine:** Physics enforces. Math proves. You verify.

**Founder background:** William Shane Wilkinson, U.S. Army veteran (CBRNe), 80% VA rating, embedded systems engineer, sole inventor on all applications.

**Working system live at:** zknot.io | api.zknot.io | verifyknot.io

---

## WHAT WE NEED FROM YOU

We need a registered patent attorney with electrical engineering or cryptography technical background to:

1. Review and refine the enclosed non-provisional specification drafts (4 patents)
2. File the non-provisional applications with USPTO in priority order
3. Prosecute through examination with us providing technical guidance

**We do NOT need you to draft the specifications from scratch.** We have produced complete pro se draft specifications with claims, drawings descriptions, IDS, and claim architecture notes. Your role is to review for legal sufficiency, refine claim language for optimal scope and defensibility, and file.

**Budget estimate:** $3,500–$4,500 per non-provisional (flat fee preferred). Total 4 non-provisionals: ~$12,000–$15,000.

**Micro-entity status:** Inventor qualifies as micro-entity. All government fees at 80% reduction.

---

## FILING PRIORITY AND DEADLINES

| # | Patent | Priority App. | Non-Prov Deadline | Est. Fee | Priority |
|---|---|---|---|---|---|
| 1 | PAT-001 ZKKey | 63/960,933 (Jan 15 2026) | **Jun 30, 2026** | $3,500–4,500 | CRITICAL |
| 2 | PAT-007 CombinedSession | 63/962,071 (Jan 15 2026) | **Jul 31, 2026** | $2,500–3,500 | HIGH |
| 3 | PAT-002 PowerVerify | 63/961,118 (Jan 15 2026) | **Jul 31, 2026** | $2,500–3,500 | HIGH |
| 4 | PAT-004 ZK-LocalChain | 63/961,442 (Jan 15 2026) | **Oct 31, 2026** | $2,500–3,500 | MEDIUM |

We need PAT-001 filed by **May 31, 2026** to allow sufficient buffer before the June 30 deadline.

---

## TECHNICAL SUMMARY — FOUR INVENTIONS

### PAT-001: ZKKey — Post-Nonce Physical Enforcement

**What it is:** A handheld USB device (the "ZKKey") containing an ATECC608B hardware secure element, an STM32 microcontroller, a 128×64 OLED display, and a tactile push-button. The device receives a cryptographic challenge (SHA-256 hash of evidence data), displays the hash on the OLED, and will NOT generate an ECDSA signature until the user physically presses the button while viewing the hash.

**The invention:** The state machine architecture that makes the HSE physically incapable of signing without button actuation. Not just policy-prevented — the code path to issue a signing command to the ATECC608B is only reachable via the SIGNING FSM state, which is only reachable via button actuation from the DISPLAY state. No software command, USB packet, or network message can reach the signing code path.

**Why it's patentable:** YubiKey/FIDO2 devices confirm user PRESENCE (touch), not user APPROVAL of specific content. The challenge hash is never shown to the user. Remote signing is possible if the host is compromised. PAT-001's post-nonce hash-display-then-physical-actuation sequence is novel.

**Key claim language:** "wherein the hardware secure element does not generate the digital signature absent detection of the physical actuation" — NOT "is prevented from" or "is configured to refuse" — "does not," meaning the code path to signing does not exist without the actuation event.

**Prior art closest:** US9509686 (secure element auth) — distinguished because signing is software-triggered, no hash display, no post-nonce enforcement. DE10059066 (display + signing) — distinguished because no state machine gating, no post-nonce behavioral constraint. US11057215 (automated hash validation) — OPPOSITE architecture, software commands hardware.

**FTO:** Clear. No blocking patents identified.

---

### PAT-002: PowerVerify — Physical Conductor Absence

**What it is:** An inline USB device (USB-C upstream, USB-A downstream) with ONLY VBUS and GND traces. D+ and D- pins on both connectors are physically unconnected — no traces on the PCB connecting them. The device is inserted between a power source and a device under attestation to prove the device received power without any data connection.

**The invention:** The claim covers ABSENCE of conductors, not disconnection, blocking, or filtering. Any party can verify with a $15 multimeter continuity test — no expert required. This is continuity-testable proof of data impossibility.

**Why it's patentable:** All existing write-blockers (Tableau, WiebeTech, US6813682) work by intercepting commands in the data stream — data conductors are present, commands are blocked. PowerVerify has no data conductors. This is a physically different architecture with different verification properties.

**Closest prior art:** US12111961 (2024, unidirectional USB dongle) — DISTINGUISHED. That device DOES transfer data (unidirectionally); it has firmware and a data capture side. PowerVerify transfers NO data. The claim is physical absence of conductors, not unidirectionality.

**Key claim language:** "wherein the inline USB device does not comprise a D+ conductor connecting any D+ pin of the first USB connector to any D+ pin of the second USB connector" — "does not comprise" is the critical phrase. Not "does not allow," not "blocks," not "disconnects."

**FTO:** Clear. US12111961 covers a different mechanism. Passive variant has no FTO concerns.

---

### PAT-004: ZK-LocalChain — Offline Hash-Chained Hardware-Attested Ledger

**What it is:** An append-only hash-chained ledger stored in local persistent storage (SQLite, PostgreSQL, or file system) that records hardware-attested attestation artifacts. Each entry contains the SHA-256 hash of the preceding entry, creating a tamper-evident chain. Operates entirely without network connectivity. Any party with an exported file can independently verify the chain by recomputing hashes.

**The invention:** The COMBINATION of (1) offline-first operation, (2) hardware-attested entries from a physical HSE device, (3) no central authority or network required for verification, and (4) independently exportable and verifiable without vendor involvement. Hash-chaining is prior art (Bitcoin, 2008). The novel combination is the specific application to offline hardware-attested field evidence custody.

**Closest prior art:** Fromm et al. 2020 (blockchain-based CoC) — DISTINGUISHED by requiring network/blockchain for recording and verification. US11410233 (blockchain settlements) — DISTINGUISHED by requiring distributed consensus network. SQL Server Ledger (2022) — DISTINGUISHED by requiring Microsoft SQL Server infrastructure.

**Key claim language:** "wherein the appending does not require network connectivity" and "independently verifiable by any party having access to an exported version of the local data store... without network access, vendor systems, or access to the physical signing device."

---

### PAT-007: CombinedSession — Bound Power+Human Attestation

**What it is:** A single chain entry in the ZK-LocalChain ledger that binds a PowerVerify power attestation record AND a ZKKey signing attestation record into one entry using a shared `session_id`. This creates a single cryptographic artifact proving BOTH (1) a device was powered without data exchange AND (2) a human approved a specific evidence hash, within the same custody session.

**The invention:** The integration claim binding PAT-001 and PAT-002 outputs. Novel because: no prior art was found for binding a physical conductor-absence attestation with a user-actuated hardware signing event in a single cryptographically linked chain entry with a shared session identifier.

**Closest prior art:** None directly. The component inventions (PAT-001, PAT-002) are the closest, but neither individually nor in prior combinations do they produce the bound single-entry proof.

**Acquirer value:** This is the most commercially significant patent for Axon Enterprise. They own every step of the evidence lifecycle except hardware-enforced chain-of-custody at the collection event. PAT-007 is that claim. One artifact that proves physics enforced AND math proved, in a single verifiable record.

---

## PRIOR ART SEARCH SUMMARY

Full prior art search documented in ZKNOT_PAT_PRIOR_ART_SEARCH_20260328.md. Key findings:

| Patent | Closest Prior Art | Distinguished By |
|---|---|---|
| PAT-001 | US9509686, DE10059066, FIDO2 | Post-nonce hash-display-then-actuation sequence; state machine enforcement |
| PAT-002 | US12111961 | Physical absence vs. unidirectional gating; no firmware; continuity-testable |
| PAT-004 | Fromm 2020, US11410233 | Offline-first; hardware-attested entries; no network for verification |
| PAT-007 | None directly | Novel integration claim; no prior combination found |

**IDS disclosures required (all four applications):**
- US12111961 (2024)
- US9509686B2 (2016)
- DE10059066A1 (2002)
- US11057215B2 (2021)
- Fromm et al. 2020 (ScienceDirect)
- US11410233B2 (2022)
- US10163080B2 (2019)
- FIDO2 WebAuthn Standard (2018–2025)
- YubiKey technical documentation
- Nakamoto 2008 (Bitcoin)

---

## CLAIM ARCHITECTURE GUIDANCE

**Claim strategy for all four patents:**
- 3 independent claims per application (Method, Apparatus, System)
- 15–17 dependent claims narrowing scope and adding fallback positions
- Prioritize Method claims — harder to design around, survive IPR better
- Avoid "blockchain," "distributed ledger," "write-blocker," "smart contract" — prior art magnets
- Use "physically absent," "hardware-attested," "physically incapable," "independently verifiable without network access"

**Broadest reasonable interpretation (BRI) targets:**
- PAT-001: Any device whose HSE cannot sign without physical user actuation of a dedicated element after displaying the challenge hash
- PAT-002: Any USB-family inline device lacking D+/D- (or equivalent protocol data) conductors as a class
- PAT-004: Any offline-capable append-only ledger recording hardware-attested artifacts with hash linkage
- PAT-007: Any single record binding a physical data-impossibility attestation with a human-gated signing event via session identifier

---

## WHAT WE PROVIDE TO YOU

1. ✅ Complete pro se draft specifications (4 documents, attached)
2. ✅ Prior art search with analysis of each reference (attached)
3. ✅ Claim architecture with independent and dependent claim drafts (within specifications)
4. ✅ IDS reference list (within each specification and consolidated above)
5. ✅ Working live system demonstrating all four inventions (verifyknot.io)
6. ✅ PCB design files (KiCad) and firmware (STM32CubeIDE) for PAT-001 and PAT-002 hardware
7. ✅ Technical drawings (to be produced as formal patent drawings in USPTO format)

**What we need from you:**
- Legal review and refinement of claim language
- Drawing preparation in USPTO format
- Non-provisional filing with USPTO
- Prosecution management (Office Action responses if required)

---

## ENGAGEMENT QUESTIONS TO ANSWER

Before engaging, please confirm:

1. Do you have technical background in embedded systems, cryptography, or hardware security?
2. Have you prosecuted hardware attestation, USB device, or cryptographic signing patents?
3. Can you provide a fixed fee quote for each non-provisional (flat fee, not hourly)?
4. Can you commit to filing PAT-001 by May 31, 2026?
5. Are you familiar with micro-entity status and the associated fee reductions?
6. Do you have experience with SDVOSB clients and any relevant IP strategy for federal contracting?

---

## CONTACT

William Shane Wilkinson
Founder & CEO, ZKNOT, Inc.
ops@zknot.io
UEI: C4SKW13JPEL5 | CAGE: 1AHZ4 | EIN: 36-5165991

*All documents attached. Please review specifications and prior art analysis before our call.*

---

*ZKNOT, Inc. | Utah-based SDVOSB | zknot.io | Physics enforces. Math proves. You verify.*
