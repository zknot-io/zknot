# ZKNOT Prior Art Search & Hybrid Pro Se Patent Plan
## Document: ZKNOT_PAT-001_prior_art_and_plan_20260328
### Prepared: March 28, 2026 | William Shane Wilkinson | ZKNOT, Inc.

---

## PART I: PRIOR ART SEARCH RESULTS

### Search Methodology
- Google Patents full-text search
- USPTO Patent Full-Text Database
- Academic literature (ScienceDirect, PMC)
- Cross-referenced against all 10 provisional claim sets

**Search terms used across four patent families:**
- PAT-001: "user actuated" "cryptographic signing" "physical button" "secure element" "post-nonce" "display hash" "user confirmation"
- PAT-002: "data path elimination" "data conductors absent" USB "chain of custody" "write blocker" forensic hardware
- PAT-004: "hash chained" "append-only ledger" "chain of custody" "offline" "independent verification" evidence integrity
- PAT-003/PAT-007: "tamper evident seal" "cryptographic" "chain entry" physical digital binding "combined session"

---

## PAT-001: ZKKey — User-Actuated Cryptographic Attestation Device
### Post-Nonce Human-Gated Signing

#### Prior Art Found — Analyzed

**1. US9509686B2 — Secure Element Authentication (Microsoft)**
- Filed: ~2013
- What it does: Stores credentials in a secure element after physical identity verification at a bank branch. Signs challenges using the SE.
- **Why it does NOT anticipate PAT-001:** The signing is software-triggered; there is no requirement for the user to physically view the specific hash being signed and physically confirm it BEFORE the SE signs. The challenge is "communicated to the SE, which processes it" — no user display/confirmation of the specific content intervenes. The human verification step is identity provisioning (one-time), not per-signing actuation.
- **Distinguishing claim language:** "wherein the user physically actuates a dedicated hardware button only after viewing the SHA-256 hash of the specific challenge on an integrated display, and wherein the secure element does not sign until said actuation occurs"

**2. DE10059066A1 — Device for Digitally Signing Information (Germany, 2000)**
- What it does: Smartcard-form device with input unit and display for signing. Hardware-coded signature program in ROM.
- **Why it does NOT anticipate PAT-001:** The display shows information, but the signing flow does not require the user to view the *hash of the specific content* before signing. More importantly, the claim is about a general signature device, not post-nonce enforcement on a challenge-response where the user approves the specific challenge hash. No state machine enforcing IDLE→ARMED→SIGNING→OUTPUT sequence gated on physical button press at the hash-display stage.
- **Distinguishing:** The FSM (FirmwareFSM, PAT-008) is a separate claim but the behavioral distinction — user sees the exact hash they're approving, device will not sign without that specific actuation — is not present in DE10059066A1.

**3. US11057215 — Automated Hash Validation (Oracle, 2021)**
- What it does: Server receives a hash and data ID, retrieves data, validates hash matches, sends to cryptographic device for signing.
- **Why it does NOT anticipate PAT-001:** This is server-side validation — there is no human in the loop at signing time. The cryptographic device signs when the server tells it to. This is precisely the problem PAT-001 solves. No physical button, no human viewing the hash, no post-nonce enforcement.
- **Distinguishing:** This is the closest software analog but operates on the opposite architecture — software commands hardware. PAT-001 requires hardware to refuse software commands.

**4. YubiKey / FIDO2 / WebAuthn Standards (Prior Art Background)**
- What they do: Hardware token signs challenge when software or OS triggers it. User presence confirmed by capacitive touch.
- **Why it does NOT anticipate PAT-001:** (a) Touch confirms "user is present" not "user approved THIS specific content." (b) The challenge hash is not displayed to the user before signing. (c) Remote/automated signing is possible if the host is compromised. (d) No post-nonce enforcement — the token doesn't know whether the challenge was generated before or after the user's intended action.
- **This is the key patentable distinction:** YubiKey-class devices prove presence. ZKKey proves *informed consent to specific content*.

**5. US4529870A — Cryptographic Identification Device (DigiCash, Chaum, 1985)**
- Historical device for identification/financial transactions. Cryptographic hardware with key storage.
- **Does not anticipate:** Pre-dates secure elements, no hash display, no challenge-response with user hash approval.

#### PAT-001 Prior Art Conclusion: PATENTABLE
**The specific combination of:**
1. Hardware secure element (ATECC608B class)
2. OLED/display showing the SHA-256 hash of the specific challenge
3. Dedicated physical button whose actuation gates signing
4. State machine that CANNOT sign without (2) having been displayed and (3) having been pressed
5. In the context of evidence attestation (not financial transactions)

**...has no direct prior art.** The closest art (YubiKey, FIDO2, DE10059066) addresses one or two elements but not the post-nonce enforcement combination. The distinguishing claim is not the hardware components individually but the *behavioral constraint enforced by the state machine*.

**Claim drafting note:** Lead with the METHOD claim (the sequence), not just the apparatus. Method claims are harder to design around and survive IPR more reliably.

---

## PAT-002: PowerVerify — Physical Data-Path Elimination

#### Prior Art Found — Analyzed

**1. US12111961 — Secure Data Extraction via Unidirectional Communication (2024)**
- **⚠️ IMPORTANT — Closest prior art found**
- What it does: Micro-DCU device powered by USB that allows data collection and transfer between two USB ports WITHOUT allowing data to flow back. Used for forensic data extraction in IIoT environments.
- **Analysis:** This patent covers *unidirectional data flow* which superficially resembles PowerVerify. However, critical distinctions:
  - The micro-DCU DOES transfer data — it's a unidirectional communication device. PowerVerify transfers NO data at all in either direction.
  - The micro-DCU has firmware and a data capture side. PowerVerify has ZERO firmware.
  - The micro-DCU's claim is about preventing cross-contamination during forensic extraction. PowerVerify's claim is about proving a device was POWERED without any data exchange.
  - The specific claim — physical ABSENCE of D+/D- conductors (not disconnection, not blocking, not unidirectional flow) — is not covered.
- **Key distinguishing language:** "wherein the data signaling conductors are physically absent from the device, such that data transfer is impossible by construction rather than by policy, software control, or unidirectional gating"

**2. US6813682 — Hardware Write-Blocker (Menz & Bress, 2004)**
- What it does: Forensic disk controller that intercepts and blocks write commands at hardware level.
- **Does not anticipate:** Write-blocker intercepts commands via firmware/controller logic. PowerVerify has no data path to block — the conductors don't exist. Also covers disk storage, not USB power delivery specifically.

**3. General USB Write-Blocker Prior Art (Tableau, WiebeTech, etc.)**
- All existing USB write-blockers work by blocking or filtering commands via firmware or controller logic.
- **None have the claim:** Physical conductor absence. All existing blockers use firmware, hardware switches, or signal termination — all of which involve conductors being present.

**4. Standard USB Spec Knowledge (Public Domain)**
- USB pins: VBUS (power), GND, D+, D- (data), ID (OTG)
- The innovation is removing D+ and D- from a device that still carries VBUS and GND.
- This creates a verifiable, continuity-testable proof of data impossibility.

#### PAT-002 Prior Art Conclusion: STRONG PATENTABLE POSITION
**The specific claim — physical absence of D+/D- conductors as a means of attesting that no data exchange occurred — has no direct prior art.** US12111961 is the closest but is fundamentally different in mechanism and purpose.

**Attorney note:** The claim scope should be broad: "a USB device wherein the data conductors are absent from the device body, wherein the device is capable of conducting electrical continuity testing to verify data conductor absence, and wherein said absence constitutes cryptographic proof of data non-transfer when combined with a power-session attestation record."

**Avoid claiming:** "write blocking" or "unidirectional" — these have prior art. Claim: "conductor absence" and "continuity-testable attestation."

---

## PAT-004: ZK-LocalChain — Offline Hash-Chained Event Ledger

#### Prior Art Found — Analyzed

**1. US11410233B2 — Blockchain Technology to Settle Transactions (2016)**
- Append-only immutable ledger with hash-linked blocks, cryptographic signatures. Financial settlements.
- **Does not anticipate:** Requires network/distributed consensus. Not offline-capable. Not designed for evidence chain-of-custody. No hardware attestation integration. No independent third-party verification without the ledger network.

**2. US10163080B2 — Document Tracking on Distributed Ledger**
- Hash value of document transmitted to distributed ledger for tracking.
- **Does not anticipate:** Distributed/networked architecture required. Centralized verification dependency.

**3. US11418322B2 — Information Management in Decentralized Database (Hyperledger Fabric)**
- Hash-linked blocks, append-only, tamper-resistant.
- **Does not anticipate:** Requires peer network. Not offline-capable in the field. Requires consensus mechanism. Not hardware-attested.

**4. Chronological Independently Verifiable Electronic Chain of Custody Ledger (ScienceDirect, 2020)**
- **⚠️ IMPORTANT — Academic prior art**
- Authors propose a blockchain-based CoC ledger for digital evidence. Hash-chained, independently verifiable, uses public blockchain to prove integrity.
- **Analysis:** This is the closest academic prior art to PAT-004. It proposes:
  - Hash-chaining of evidence events
  - Public blockchain anchoring for independent verification
  - Application to forensic chain of custody
- **Critical distinctions from PAT-004:**
  - Requires network access (public blockchain anchoring)
  - No hardware attestation integration (no secure element)
  - No offline-first architecture (field deployment without connectivity)
  - No physical hardware device producing the chain entries
  - No short code derivation for human-readable public verification
  - Published 2020 — post-dates our priority (Jan 15, 2026) but is prior art if the concept predates our filing. **However:** the offline-first capability and hardware integration are novel.
- **Distinguishing:** "wherein the ledger operates entirely offline without network connectivity requirements, wherein each entry is produced by a hardware-attested signing device, and wherein the chain is independently verifiable by any party with access to the exported file without requiring network access to a consensus mechanism or central authority"

**5. US9774578B1 — Distributed Key Secret for Rewritable Blockchain**
- Allows rewriting blockchain with key secret.
- **Does not anticipate:** Our claim is specifically that the chain is NOT rewritable. This patent's existence strengthens our append-only claim by showing the art went in the rewritable direction.

**6. SQL Server 2022 Ledger**
- Microsoft's append-only ledger table implementation.
- **Does not anticipate:** Server-dependent, requires Microsoft infrastructure, not field-deployable, not hardware-attested, not independently verifiable offline.

#### PAT-004 Prior Art Conclusion: PATENTABLE WITH NARROW CLAIM FOCUS
**The combination of (1) offline-first operation, (2) hardware-attested entries, (3) no central authority or network required for verification, and (4) independent exportable verification is not anticipated by prior art.** Hash-chaining itself is well-known (Bitcoin, 2008). The claim must focus on the specific combination for field-deployable hardware-attested evidence custody.

**Key claim language:** Focus on the COMBINATION — offline + hardware-attested + independently verifiable without vendor. Avoid claiming hash-chaining generally.

---

## PAT-003 / PAT-007: TrustSeal & CombinedSession

#### PAT-003 — TrustSeal Physical-Digital Binding

**Prior Art:**
- Tamper-evident seals: Widely known (FDA, DEA, DOJ). Void patterns, holographic labels, etc.
- RFID-tagged seals: Known. NFC seals with serial numbers: Known.
- Hash-to-seal binding: Some supply chain prior art exists.

**Key prior art found:**
- US10664797B2 — Distributed Ledger Certification (includes concept of certification being recorded on ledger when physical item certified)
- Supply chain blockchain: IBM Food Trust, Walmart food tracking — bind physical events to blockchain records.

**Distinction for PAT-003:** The specific claim is binding the cryptographic chain entry creation to the moment of physical seal application — not after the fact, not at manufacture, but at the custody transfer event. The short code is printed ON the seal itself. This creates a provable physical-digital unity event that isn't present in supply chain art (which records events, not binds a printed identifier to a ledger entry at creation moment).

**PAT-003 claim strength: MODERATE.** The concept of physical-digital binding is known in supply chain. The strength is in the specific evidence-custody application and the real-time binding at the moment of seal application (not retroactive).

#### PAT-007 — CombinedSession: Bound Power+Human Attestation Record

**Prior Art search result: NO DIRECT PRIOR ART FOUND.**

This claim covers a single chain entry that simultaneously proves:
1. A specific device was powered (PowerVerify session certificate)
2. A specific human approved a specific action (ZKKey signature)
3. Both are cryptographically bound by a shared session identifier

The concept of binding multiple evidence events into a single record is not novel (multi-part records, compound evidence). However, the specific binding of a PHYSICAL POWER ATTESTATION (PAT-002) with a HUMAN-GATED SIGNING EVENT (PAT-001) into a single independently verifiable chain entry — specifically for evidence custody purposes — appears novel.

**No prior art found in:** Google Patents, USPTO, academic literature on this specific combination.

**PAT-007 claim strength: STRONG.** This is an integration claim covering the novel combination of PAT-001 and PAT-002 outputs, not an attempt to patent either independently.

---

## PART II: HYBRID PRO SE PATENT PLAN

### What "Hybrid Pro Se" Means for ZKNOT
Pro se = you file and prosecute yourself.
Hybrid = you do the strategic drafting and prosecution, but engage a registered patent attorney for:
1. Non-provisional claim drafting (the legally operative claims)
2. USPTO filing and docketing of non-provisionals
3. Response to any Office Actions on priority patents

**Why hybrid vs. full attorney:** Full prosecution of 10 patents would cost $80,000–$150,000. Hybrid approach for 4 priority non-provisionals runs $12,000–$18,000 in attorney fees while you control the strategy, narrative, and claim architecture.

---

### ATTORNEY ENGAGEMENT PRIORITY (Ranked)

| Priority | Patent | Deadline | Est. Attorney Cost | Rationale |
|---|---|---|---|---|
| 1 — CRITICAL | PAT-001 ZKKey | Jun 30, 2026 | $3,500–$4,500 | Highest value, broadest claims, most defensible |
| 2 — HIGH | PAT-007 CombinedSession | Jul 31, 2026 | $2,500–$3,500 | Novel integration claim, Axon acquisition differentiator |
| 3 — HIGH | PAT-002 PowerVerify | Jul 31, 2026 | $2,500–$3,500 | Physical absence claim, hardest to design around |
| 4 — MEDIUM | PAT-004 ZK-LocalChain | Oct 31, 2026 | $2,500–$3,500 | Offline-first combination claim |
| Refile | PAT-003, PAT-006, PAT-008, PAT-010 | Jan 2027 | $65 each (pro se) | Lower priority, refile provisionals yourself |

**Total attorney budget estimate: $11,000–$15,000 for Priorities 1–4**

---

### PRO SE REFILE STRATEGY (You Do These)

For patents where you're refiling provisionals at $65 each rather than converting to non-provisionals immediately, the process is:

1. Log into USPTO Patent Center (patentcenter.uspto.gov)
2. File → Provisional Patent Application
3. Upload the existing provisional spec (you already have these)
4. Pay $65 micro-entity fee (you qualify as micro-entity — individual inventor, income threshold)
5. Get new application number and priority date

**Micro-entity qualification:** You qualify if:
- You have not filed more than 4 previous patent applications (check your count)
- Gross income is below ~$239,000 (2026 threshold)
- You are not obligated to assign to an entity that does not qualify

**Refile candidates (Jan 2027, before provisionals expire):**
- PAT-003 TrustSeal (filed Jan 15, 2026 → expires Jan 15, 2027)
- PAT-006 OfflineEvidence (filed Feb 9, 2026 → expires Feb 9, 2027)
- PAT-008 FirmwareFSM (filed Mar 3, 2026 → expires Mar 3, 2027)
- PAT-010 ShortCode (filed Mar 3, 2026 → expires Mar 3, 2027)

---

### PRO SE CLAIM DRAFTING FRAMEWORK

Even when using an attorney for filing, you control the narrative. Give your attorney:
1. The prior art analysis (Part I of this document)
2. The claim architecture below
3. The specific distinguishing language
4. A clear hierarchy of independent claims → dependent claims

#### Claim Architecture Template (Use for All Four Priority Patents)

**Structure every non-provisional with:**
- 3 independent claims (method, apparatus, system)
- 15–17 dependent claims narrowing each independent
- 1 abstract
- Detailed description with drawings
- At least one working example (you have the live system)

**Independent Claim Types:**
```
Claim 1 (Method): A method comprising...
Claim 8 (Apparatus): An apparatus comprising...
Claim 15 (System): A system comprising...
```

---

### PAT-001 CLAIM ARCHITECTURE (ZKKey)

**Independent Claim 1 — Method:**
```
A method for hardware-attested evidence signing comprising:
  receiving, by a hardware attestation device, a cryptographic challenge
    comprising a hash of evidence data;
  displaying, on an integrated visual output of the hardware attestation
    device, the cryptographic challenge hash;
  detecting a physical actuation of a dedicated hardware input element
    of the hardware attestation device;
  generating, by a hardware secure element of the hardware attestation
    device, a digital signature of the cryptographic challenge hash
    only upon detection of said physical actuation; and
  producing an attestation artifact comprising the digital signature,
    a device identifier, and a timestamp;
  wherein the hardware secure element is physically incapable of
    generating the digital signature absent the physical actuation.
```

**Key dependent claims to add:**
- Wherein the hardware secure element is an ATECC608B-class device
- Wherein the visual output is an OLED display
- Wherein the attestation artifact is recorded in an append-only hash-chained ledger
- Wherein the physical actuation is a dedicated tactile button separate from any data interface
- Wherein the method further comprises transmitting the attestation artifact to a public verification service
- Wherein the challenge hash is derived from evidence data received via an optically scanned QR code (covers ZKKey Air, PAT-009)
- Wherein no network connection is required during signing (offline capability)
- Wherein the device executes a finite state machine transitioning through IDLE, ARMED, SIGNING, and OUTPUT states
- Wherein the attestation artifact further comprises a human-readable short code derived deterministically from the digital signature

---

### PAT-002 CLAIM ARCHITECTURE (PowerVerify)

**Independent Claim 1 — Method:**
```
A method for attesting the absence of data transfer comprising:
  providing an inline USB device positioned between a power source
    and a powered device, wherein the inline USB device comprises
    a VBUS conductor and a GND conductor and wherein the inline USB
    device does not comprise data signaling conductors;
  supplying electrical power from the power source to the powered
    device through the inline USB device;
  generating a power session attestation record comprising a session
    identifier, a timestamp, and a device identifier;
  wherein the absence of data signaling conductors is verifiable by
    continuity testing of the inline USB device.
```

**Key dependent claims:**
- Wherein the data signaling conductors that are absent include at minimum the D+ conductor and D- conductor of the USB specification
- Wherein the inline USB device operates without firmware or programmable logic
- Wherein the power session attestation record is generated by a hardware secure element
- Wherein the power session attestation record is recorded in an append-only hash-chained ledger
- Wherein the power session attestation record shares a session identifier with a human-gated signing attestation (covers PAT-007 integration)
- Wherein the absence of data conductors makes data transfer impossible by physical construction rather than by software policy

---

### PAT-004 CLAIM ARCHITECTURE (ZK-LocalChain)

**Independent Claim 1 — Method:**
```
A method for maintaining a hardware-attested chain-of-custody ledger
comprising:
  receiving a hardware-attested attestation artifact from a hardware
    signing device, wherein the attestation artifact comprises a
    digital signature generated by a hardware secure element;
  computing a chain entry hash comprising a hash function applied to
    the attestation artifact and a hash of a preceding chain entry;
  appending the chain entry to an append-only ledger stored in
    local storage without requiring network connectivity;
  wherein the ledger is independently verifiable by any party having
    access to an exported version of the ledger without requiring
    access to a central authority, network service, or the original
    hardware device.
```

**Key dependent claims:**
- Wherein the hash function is SHA-256
- Wherein a first entry in the ledger comprises a genesis entry with a null preceding hash
- Wherein the ledger is exportable as a self-contained file
- Wherein verification of the ledger comprises recomputing each chain entry hash and confirming sequential linkage
- Wherein the ledger supports synchronization with a remote ledger upon restoration of network connectivity
- Wherein each attestation artifact further comprises a human-readable short code derived from the digital signature
- Wherein the ledger records a combined session entry binding a power attestation record and a signing attestation record sharing a session identifier

---

### PAT-007 CLAIM ARCHITECTURE (CombinedSession)

**Independent Claim 1 — Method:**
```
A method for generating a bound hardware-attested evidence record comprising:
  generating a power attestation record by a power verification device
    wherein the power verification device does not comprise data
    signaling conductors, the power attestation record comprising
    a first session identifier;
  generating a signing attestation record by a human-gated signing device
    wherein a user physically actuates a hardware input element after
    viewing a challenge hash on an integrated display, the signing
    attestation record comprising the first session identifier;
  producing a combined attestation entry in an append-only hash-chained
    ledger, the combined attestation entry comprising both the power
    attestation record and the signing attestation record bound by the
    shared first session identifier;
  wherein the combined attestation entry provides independent cryptographic
    proof that a specific device was powered and a specific human
    authorized a specific action during the same custody event.
```

---

### PART III: DOCUMENT PRODUCTION PLAN

#### Documents to Produce This Weekend (Pro Se Drafts for Attorney Review)

**Priority 1: PAT-001 Non-Provisional Draft**
- Full specification (~8,000–12,000 words)
- 20 claims (3 independent, 17 dependent)
- 6–8 drawings (state machine diagram, device diagram, system diagram, flow charts)
- Abstract

**Priority 2: PAT-002 Non-Provisional Draft**
- Full specification (~6,000–8,000 words)
- 20 claims
- 4–6 drawings (device cross-section, USB pin diagram, continuity test diagram, system diagram)

**Priority 3: Prior Art Statement (IDS)**
- Information Disclosure Statement listing all prior art found in this search
- Required to be filed with each non-provisional
- Disclose: US12111961, US9509686, DE10059066, US11057215, ScienceDirect 2020 CoC paper, US11410233, US10163080

**Priority 4: Patent Attorney Brief**
- 2-page brief per patent summarizing claim architecture, key prior art distinctions, and inventor's technical explanation
- Purpose: Get attorney up to speed in 1 hour instead of 4

---

### MICRO-ENTITY FEE SCHEDULE (2026)

| Filing | Micro-Entity Fee | Standard Fee |
|---|---|---|
| Provisional application | $65 | $320 |
| Non-provisional basic filing | $320 | $1,600 |
| Non-provisional search | $220 | $1,100 |
| Non-provisional examination | $200 | $1,000 |
| Non-provisional total (gov't fees only) | ~$740 | ~$3,700 |
| Issue fee (if granted) | $500 | $1,000 |

**Micro-entity status saves ~75% on government fees.** Confirm eligibility before each filing.

---

### PROSECUTION STRATEGY NOTES

**Things to disclose (mandatory — IDS):**
- All prior art found in this search
- The ScienceDirect 2020 CoC ledger paper
- US12111961 (unidirectional USB)
- Any academic publications you or your team have made about the technology

**Things to avoid in claim language:**
- "blockchain" — triggers prior art floods and examiner skepticism
- "write-blocker" — has specific prior art (Menz & Bress)
- "distributed ledger" — blockchain prior art
- "smart contract" — extensive prior art
- Functional language that reads on prior art software implementations

**Things to emphasize:**
- "physically absent" (not blocked, not filtered, not disabled)
- "hardware-attested" (not software-signed)
- "independently verifiable without network access" (not "decentralized")
- "physically incapable" (not "prevented by policy")
- "post-nonce" (not just "user confirmation")

---

### FREEDOM TO OPERATE (FTO) QUICK ANALYSIS

**Can you make and sell these products today?**

PAT-001 (ZKKey): No blocking patents found. YubiKey/FIDO2 patents do not cover the specific post-nonce hash-display-then-button-press sequence for evidence attestation. **FTO: YES**

PAT-002 (PowerVerify): US12111961 covers unidirectional data collection devices but explicitly requires data transfer capability. PowerVerify transfers no data. **FTO: YES** (confirm with attorney)

PAT-004 (ZK-LocalChain): Blockchain/ledger space has extensive patents but all cover distributed/networked implementations. Offline-first local implementation appears clear. **FTO: Likely YES, verify**

PAT-007 (CombinedSession): Novel combination — no FTO concerns identified. **FTO: YES**

**Note:** This is not legal advice. A registered patent attorney should conduct a formal FTO analysis before commercial launch.

---

### WEEKEND EXECUTION PLAN

**Saturday:**
- [ ] Generate PAT-001 full specification draft (this session)
- [ ] Generate PAT-002 full specification draft (this session)
- [ ] Generate attorney brief for PAT-001 and PAT-002

**Sunday:**
- [ ] Generate PAT-004 full specification draft
- [ ] Generate PAT-007 full specification draft
- [ ] Generate IDS (Information Disclosure Statement) listing all prior art

**Monday (after vacation):**
- [ ] Send attorney brief + prior art search + draft specs to 2–3 registered patent attorneys for engagement quotes
- [ ] Target engagement by May 1, 2026 for PAT-001 June 30 deadline

---

### ATTORNEY SELECTION CRITERIA

When engaging a patent attorney for ZKKey and PowerVerify:

1. **Technical background:** Electrical engineering, embedded systems, or cryptography. Not a generalist IP attorney.
2. **Experience with hardware patents:** Ask for examples of hardware attestation, security device, or IoT patents they've prosecuted.
3. **USPTO experience:** Ask for their allowance rate and average time to allowance for comparable cases.
4. **SDVOSB/small entity fees:** Confirm they handle micro-entity filings.
5. **Fixed fee vs. hourly:** Request fixed fee for non-provisional drafting. $3,500–$4,500 for PAT-001 is reasonable.

**Where to find:**
- USPTO Patent Attorney Directory (patft.uspto.gov)
- Registered Patent Attorney bar (look for attorneys with EE + CS technical backgrounds)
- Utah State Bar IP section (local preferred for in-person meetings before key decisions)

---

*Document prepared for internal use. Not legal advice. For reference by retained patent counsel.*

*ZKNOT, Inc. | ops@zknot.io | UEI: C4SKW13JPEL5 | CAGE: 1AHZ4*
