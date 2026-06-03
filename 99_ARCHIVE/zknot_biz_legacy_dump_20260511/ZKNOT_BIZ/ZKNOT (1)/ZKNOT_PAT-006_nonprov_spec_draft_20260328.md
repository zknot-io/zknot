# PATENT APPLICATION DRAFT
## PAT-006: EvidenceProtocol — Cryptographically Verified Evidence Integrity Protocol
### Non-Provisional Patent Application — Pro Se Draft for Attorney Review
### Priority: US Provisional App. No. 63/960,412 (Filed January 3, 2026)

---

## TITLE OF INVENTION

**CRYPTOGRAPHICALLY VERIFIED EVIDENCE INTEGRITY PROTOCOL FOR HUMAN-WITNESSED DIGITAL AND PHYSICAL EVENTS**

---

## CROSS-REFERENCE TO RELATED APPLICATIONS

This application claims priority to U.S. Provisional Patent Application No. 63/960,412, filed January 3, 2026, incorporated herein by reference.

This application is the SYSTEM CLAIM that integrates the following co-pending applications:
- PAT-001: ZKKey — User-Actuated Cryptographic Attestation Device
- PAT-002: PowerVerify — Physical Data-Path Elimination Device
- PAT-003: TrustSeal — Tamper-Evident Physical Seal with Cryptographic Binding
- PAT-004: ZK-LocalChain — Offline Hash-Chained Evidence Ledger
- PAT-007: CombinedSession — Bound Power and Human-Gated Attestation Record

---

## BACKGROUND OF THE INVENTION

### Field of the Invention

The present invention relates to evidence collection, forensic documentation, and cryptographic verification. More particularly, the invention provides a unified protocol that binds human physical presence, device power state, physical seal integrity, and digital record authenticity into a single, independently verifiable cryptographic chain of custody — applicable to journalism, election auditing, law enforcement, pharmaceutical custody, and any regulated industry where evidence integrity is subject to legal scrutiny.

### Description of Related Art

Evidence workflows in forensic, legal, and regulatory contexts currently rely on multiple independent systems for different aspects of evidence integrity:

Physical chain of custody is documented procedurally (numbered seals, witness signatures, paper forms) — providing social assurance but no cryptographic proof. Digital evidence integrity is documented by hash values recorded in forensic tool logs — but those logs are mutable by tool administrators and require vendor testimony for court authentication. Human presence is documented by witness declarations — but witnesses can be impeached, forget, or be absent.

No existing unified protocol provides a single cryptographic artifact that simultaneously and independently proves: (1) the device collecting evidence received power without data interference; (2) a specific human was physically present and approved the specific evidence hash; (3) a physical seal was applied to the evidence at a specific moment; and (4) all of these events are linked in an append-only hash chain that is verifiable by any third party without vendor involvement.

### The Integration Gap

Prior art covers individual components: hardware signing devices (YubiKey, FIDO2), write-blockers (Tableau), tamper seals (3M, Brady), blockchain evidence tracking (Chainlink, IBM Food Trust). None specifies a PROTOCOL — a defined workflow sequence — that combines hardware power attestation, human-gated signing, physical seal binding, and offline hash-chained ledger into a unified end-to-end evidence integrity system where each step's output cryptographically binds to the next.

The patent claim is not the individual components (each covered by co-pending applications) but the **protocol itself** — the defined sequence of steps and the cryptographic bindings between them — as a single claimable system.

---

## SUMMARY OF THE INVENTION

The present invention provides the EvidenceProtocol: a defined sequence of hardware-verified steps that produces a complete, independently verifiable cryptographic chain of custody for any physical or digital evidence event. The protocol comprises the following ordered steps: (1) power attestation via a data-path-eliminated device; (2) evidence capture; (3) physical seal application with cryptographic binding; (4) human-gated signing of the evidence hash and seal identifier; and (5) recording of all events in an offline hash-chained ledger. Each step produces a cryptographic artifact, and the artifacts are bound together by a shared session identifier and recorded as linked entries in the ledger.

---

## DETAILED DESCRIPTION OF THE INVENTION

### 1. Protocol Overview

The EvidenceProtocol defines five ordered steps. The protocol may be executed in whole or in subsets depending on the deployment context. The complete protocol provides the strongest evidence integrity assurance; partial protocol execution provides a subset of proofs appropriate for specific use cases.

**Step 1 — Power Attestation (PowerVerify)**
The device from which evidence will be collected or on which evidence will be stored is connected to power through a PowerVerify inline device (PAT-002). The PowerVerify device has no D+/D- data conductors, making data transfer physically impossible by construction. The PowerVerify device generates a power session attestation record (POWER_SESSION artifact) containing: device identifier, session identifier, timestamp, and ECDSA signature from the PowerVerify hardware secure element.

Proof established by Step 1: The evidence device received electrical power and no data was transferred via the power connection during the session.

**Step 2 — Evidence Capture**
The evidence is captured, collected, or transferred — a photograph taken, a file copied to a storage medium, a ballot sealed in a container. The evidence data is hashed using SHA-256 to produce the evidence hash. This step is not instrumented by the protocol hardware but is the event to which all subsequent attestations are bound.

**Step 3 — Physical Seal Application (TrustSeal)**
A TrustSeal tamper-evident seal (PAT-003) is applied to the evidence storage medium or container. The seal's unique identifier (printed barcode or NFC/RFID identifier) is scanned and recorded. The seal application event generates a TRUST_SEAL artifact containing: seal identifier, application timestamp, evidence hash (linked from Step 2), session identifier (linked from Step 1), and optionally a hardware secure element signature.

Proof established by Step 3: A specific physical seal was applied to the specific evidence at a specific moment, and the seal identifier is cryptographically linked to the evidence hash.

**Step 4 — Human-Gated Signing (ZKKey)**
The evidence hash (from Step 2) and the seal identifier (from Step 3) are combined into a signing challenge. The challenge is presented to a ZKKey device (PAT-001). The ZKKey displays the SHA-256 hash of the challenge on its OLED display. The evidence collector physically actuates the ZKKey button, confirming they viewed the displayed hash. The ZKKey hardware secure element generates a ZKEY_SIGN attestation artifact containing: challenge hash (binding the evidence and seal), session identifier (linking to Steps 1 and 3), timestamp, device identifier, and ECDSA signature.

Proof established by Step 4: A specific human, in possession of the specific ZKKey device, physically viewed and approved the hash of the specific evidence and the specific seal identifier.

**Step 5 — Ledger Recording (ZK-LocalChain)**
All artifacts produced in Steps 1, 3, and 4 are recorded in the ZK-LocalChain append-only hash-chained ledger (PAT-004). The session's power artifact, seal artifact, and signing artifact may be recorded as individual sequential chain entries or as a single combined COMBINED_SESSION entry (PAT-007) linked by the shared session identifier. Each entry contains the hash of the preceding entry, creating a tamper-evident chain.

Proof established by Step 5: All artifacts are linked in a tamper-evident sequence; any insertion, deletion, or modification of any artifact is detectable by hash chain recomputation.

### 2. Session Identifier — The Binding Mechanism

The session identifier (session_id) is a UUID generated at the start of each protocol execution and included in every artifact produced during that execution. The session_id binds the power attestation, seal attestation, and signing attestation into a provably related set — they are not merely temporally proximate events but cryptographically linked events that the protocol enforces belong to the same custody session.

An opposing party cannot argue that a power attestation from one session was retroactively associated with a signing event from a different session, because the session_id in both artifacts is the same UUID and both artifacts are signed by hardware devices that cannot produce matching session_ids without receiving the same session_id as input.

### 3. Independent Verification

Any third party — opposing counsel, a judge, an auditor, a journalist — can independently verify the complete protocol execution by:

1. Obtaining the exported ZK-LocalChain ledger file (no network required)
2. Recomputing the hash chain to verify no entries were added, deleted, or modified
3. Verifying the ECDSA signature on each hardware artifact against the respective device's registered public key
4. Confirming the session_id matches across all artifacts in the session
5. Confirming the evidence hash in the ZKEY_SIGN artifact matches the SHA-256 of the evidence in question
6. Verifying the seal identifier in the signing challenge matches the physical seal on the evidence container

Alternatively, a human-readable short code derived from the signing artifact can be entered at verifyknot.io to retrieve a structured display of all six verification elements above.

### 4. Protocol Subsets

The full five-step protocol is not required for all use cases. Defined subsets include:

**Power+Sign subset (PAT-007 CombinedSession):** Steps 1, 2, 4, 5 — proof of powered device and human-gated signing without physical seal. Appropriate for digital-only evidence without physical media.

**Sign+Chain subset:** Steps 2, 4, 5 — human-gated signing and ledger recording without power attestation. Appropriate when the device is not USB-powered or power attestation is handled by other means.

**Seal+Sign subset:** Steps 2, 3, 4, 5 — physical seal with human-gated signing. Appropriate for physical evidence without a powered device.

**Full protocol:** Steps 1–5. Maximum evidentiary coverage.

### 5. Vertical Applications

**5.1 Election Auditing**
A county election observer uses the full protocol during ballot transfer. A voting machine is powered through PowerVerify (Step 1). Ballots are sealed in a transfer bag with a TrustSeal (Step 3). The hash of the ballot manifest and seal ID is signed via ZKKey (Step 4). The observer's tablet records all artifacts in ZK-LocalChain (Step 5). The county election office and any independent auditor can verify the complete protocol execution without contacting the observer.

**5.2 Forensic Journalism**
A photojournalist covers a conflict zone. Their camera is powered via PowerVerify (Step 1). A photograph is captured (Step 2). A TrustSeal is applied to the memory card (Step 3). The photographer signs the image hash and seal ID via ZKKey (Step 4). The artifact chain is recorded locally (Step 5). Any newspaper, fact-checker, or court can independently verify that the journalist was physically present when this specific image was captured and sealed, without trusting the publication.

**5.3 Pharmaceutical Custody (DSCSA)**
A pharmaceutical courier uses Seal+Sign subset. Each drug unit or batch receives a TrustSeal (Step 3). The courier signs the drug identifier hash and seal ID (Step 4). The event is recorded in the ledger (Step 5). At destination, the receiving pharmacist independently verifies the full seal and signing chain without contacting the courier company.

### 6. Claim of Protocol Novelty

The novelty of PAT-006 is not in any individual hardware component (each is covered by separate applications) but in:

(a) The defined protocol SEQUENCE — the specific ordered workflow in which each step's output is the input for the next step's binding;

(b) The SESSION IDENTIFIER as the binding mechanism across hardware artifacts produced by physically separate devices;

(c) The claim that the COMPLETE PROTOCOL produces a single independently verifiable chain that simultaneously proves power state, human presence, physical seal integrity, and digital evidence authenticity — no prior art produces all four proofs in a single independently verifiable chain.

---

## CLAIMS

**Claim 1.** A method for cryptographically verified evidence integrity comprising:
generating a power attestation record by a power verification device that delivers electrical power to an evidence device without data conductor connectivity, the power attestation record comprising a session identifier and a first digital signature;
hashing evidence data to produce an evidence hash;
applying a tamper-evident physical seal to evidence media or container and recording a seal identifier;
presenting a signing challenge comprising the evidence hash and the seal identifier to a human-gated signing device, the signing device displaying the challenge hash to a user and generating a signing attestation record comprising the session identifier and a second digital signature only upon physical actuation of a hardware input element by the user;
recording the power attestation record, a seal application record, and the signing attestation record in an append-only hash-chained ledger;
wherein the session identifier binds the power attestation record and the signing attestation record as part of the same evidence custody session.

**Claim 2.** The method of claim 1, wherein the power verification device does not comprise D+ or D- data signaling conductors, and wherein the absence of data conductors is verifiable by electrical continuity testing.

**Claim 3.** The method of claim 1, wherein the human-gated signing device generates the second digital signature using a hardware secure element only upon physical actuation of a dedicated hardware button after displaying the challenge hash on an integrated display.

**Claim 4.** The method of claim 1, wherein the append-only hash-chained ledger operates without network connectivity, such that all five steps may be executed in a field environment without network access.

**Claim 5.** The method of claim 1, wherein the power attestation record, the seal application record, and the signing attestation record are recorded as a single combined chain entry in the append-only hash-chained ledger.

**Claim 6.** The method of claim 1, wherein any third party may independently verify the complete method execution by: verifying the first and second digital signatures against registered device public keys; confirming the session identifier matches across the power attestation record and the signing attestation record; confirming the evidence hash in the signing attestation record matches the SHA-256 hash of the evidence data; and verifying hash chain continuity of the append-only ledger; without network access, vendor involvement, or access to the power verification device or signing device.

**Claim 7.** The method of claim 1, wherein a human-readable short code derived deterministically from the second digital signature is generated and is resolvable at a public verification service to a structured display of all verification elements.

**Claim 8.** A system for cryptographically verified evidence integrity comprising:
a power verification device configured to deliver electrical power without data transfer and generate a power attestation record comprising a session identifier;
a tamper-evident seal having a unique identifier; and a seal recording mechanism configured to record the seal identifier and evidence hash;
a human-gated signing device configured to display a challenge hash comprising the evidence hash and seal identifier and to generate a signing attestation record comprising the session identifier only upon physical actuation by a user who has viewed the challenge hash;
an append-only hash-chained ledger configured to record the power attestation record, seal application record, and signing attestation record;
wherein the session identifier binds all records to a single verifiable custody session.

**Claim 9.** The system of claim 8, further comprising a public verification service configured to resolve a human-readable short code to a display of all custody session records without account credentials.

**Claim 10.** The system of claim 8, wherein the append-only hash-chained ledger operates without network connectivity.

**Claim 11.** A protocol for evidence custody comprising an ordered sequence of hardware-verified steps: a power step in which an evidence device receives power through a data-path-eliminated interface generating a session-identified power attestation; a capture step in which evidence data is hashed; a seal step in which a tamper-evident physical seal is applied and its identifier is recorded; a signing step in which a human physically actuates a hardware signing device after viewing a challenge hash combining the evidence hash and seal identifier, generating a session-identified signing attestation; and a recording step in which all attestations are appended to an offline hash-chained ledger; wherein each step's output is cryptographically bound to the next step's input via the shared session identifier.

**Claim 12.** The protocol of claim 11, wherein the protocol is executable as a subset comprising the power step, capture step, signing step, and recording step without the seal step, producing a combined power-and-signing attestation record.

**Claim 13.** The protocol of claim 11, wherein independent verification of the complete protocol execution requires only an exported ledger file and standard ECDSA verification tools, without network connectivity or vendor involvement.

---

## ABSTRACT

A cryptographically verified evidence integrity protocol defines a workflow sequence for collecting and documenting evidence with hardware-verified steps. The protocol comprises: power attestation via a physical data-path-eliminated device; evidence capture and hashing; tamper-evident seal application with cryptographic identifier binding; human-gated signing in which a user physically actuates a hardware signing device after viewing the evidence hash; and offline hash-chained ledger recording. A shared session identifier binds all hardware-produced attestation records to a single verifiable custody session. The complete protocol provides independent verifiable proof — by any third party without vendor involvement — that a specific device received power without data transfer, a specific human approved a specific evidence hash and seal identifier, and a physical seal was applied during the same custody session. All proofs are linked in an offline-capable append-only hash-chained ledger independently verifiable by hash recomputation.

---

## IDS — Prior Art to Disclose

1. PAT-001 (ZKKey) — co-pending, same inventor
2. PAT-002 (PowerVerify) — co-pending, same inventor
3. PAT-003 (TrustSeal) — co-pending, same inventor
4. PAT-004 (ZK-LocalChain) — co-pending, same inventor
5. PAT-007 (CombinedSession) — co-pending, same inventor
6. C2PA Coalition for Content Provenance and Authenticity specification (content provenance prior art)
7. US7644138B2 — Forensics tool for electronic discovery (forensic chain of custody prior art)
8. NIST SP 800-86 — Guide to Integrating Forensic Techniques (procedural protocol prior art)
9. Fromm et al. 2020 — blockchain-based CoC (distinguished: no hardware signing, no power attestation, no physical seal binding)
10. ISO/IEC 27037 — Guidelines for identification, collection, acquisition and preservation of digital evidence

---

*DRAFT — For attorney review. Not yet filed. Priority date: January 3, 2026.*
*Inventor: William Shane Wilkinson | ZKNOT, Inc. | ops@zknot.io*

**ATTORNEY NOTE — Strategic Value of PAT-006:**
PAT-006 is the hardest patent to design around in the entire portfolio. It is a SYSTEM CLAIM and PROTOCOL CLAIM, not a device claim. A competitor cannot avoid PAT-006 by designing a different hardware device — they must avoid the specific protocol sequence with session-identifier binding. Any competitor who builds a combined power+signing+seal+ledger system using session binding will need a license. This is the "umbrella" patent that covers any implementation of the ZKNOT doctrine regardless of specific hardware choices.
