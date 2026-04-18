# PATENT APPLICATION DRAFT
## PAT-004: ZK-LocalChain — Offline Hardware-Attested Hash-Chained Evidence Ledger
### Non-Provisional Patent Application — Pro Se Draft for Attorney Review
### Priority: US Provisional App. No. 63/961,442 (Filed January 15, 2026)

---

## TITLE OF INVENTION

**OFFLINE HARDWARE-ATTESTED APPEND-ONLY HASH-CHAINED EVIDENCE LEDGER WITH INDEPENDENT VERIFICATION**

---

## CROSS-REFERENCE TO RELATED APPLICATIONS

This application claims priority to U.S. Provisional Patent Application No. 63/961,442, filed January 15, 2026, entitled "ZK-LocalChain — Offline Hardware-Attested Chain-of-Custody Ledger," incorporated herein by reference.

Related applications: PAT-001 (ZKKey), PAT-002 (PowerVerify), PAT-007 (CombinedSession), PAT-010 (ShortCode).

---

## BACKGROUND OF THE INVENTION

### Field of the Invention

The present invention relates to cryptographic evidence ledgers, and more particularly to offline-capable append-only hash-chained ledgers that record hardware-attested attestation artifacts and are independently verifiable by any party without network access, central authority, or vendor involvement.

### Description of Related Art

Digital chain-of-custody systems have evolved from paper forms toward electronic records, and more recently toward blockchain-based distributed ledgers. Existing approaches each suffer from fundamental limitations in field-deployable evidence custody applications.

**Paper-based chain of custody** is procedurally challengeable, requires witnesses, and provides no cryptographic proof of content integrity. A paper chain of custody can be backdated, altered, or forged with sufficient access to the physical documentation.

**Centralized database audit logs** (e.g., those used by digital forensics tools such as EnCase, FTK, and Cellebrite UFED) record events in a database controlled by the forensics software vendor or the investigating agency. These records are mutable by parties with database administrator access. Authentication of such records in court requires the software vendor to testify to the system's integrity and configuration, creating a vendor dependency that can be exploited by opposing counsel.

**Blockchain-based chain-of-custody systems** (such as those described in academic literature including Fromm et al. 2020, "Chronological independently verifiable electronic chain of custody ledger using blockchain technology") require network access to record entries and to verify the chain's integrity via a distributed consensus mechanism. This architecture is incompatible with field operations in rural areas, restricted facilities (jails, military installations, Faraday-shielded rooms), or international deployments where reliable connectivity is not available. Furthermore, blockchain-based systems require the verifying party to access a blockchain network, creating an ongoing infrastructure dependency.

**Hardware Security Module (HSM) signing** can attest individual artifacts but does not provide a chain structure: each signed artifact is independent, and there is no cryptographic linkage that proves the artifacts were produced in a specific sequence without gaps or insertions.

What is needed is a chain-of-custody ledger that: (1) operates entirely without network connectivity, enabling field deployment in any environment; (2) records entries produced by hardware-attested signing devices, ensuring that entries cannot be fabricated without physical hardware; (3) links entries cryptographically in a hash chain, such that any insertion, deletion, or modification of entries is detectable; and (4) is independently verifiable by any party with access to an exported copy of the ledger, without requiring network access, vendor systems, or central authority.

---

## SUMMARY OF THE INVENTION

The present invention provides an offline-capable append-only hash-chained evidence ledger (the "Ledger") that records hardware-attested attestation artifacts. Each entry in the Ledger includes the cryptographic hash of the preceding entry, creating a chain in which any modification to any entry is detectable by recomputing and comparing chain hashes. The Ledger operates without network connectivity, storing entries in local persistent storage. The complete Ledger is independently verifiable by any party with access to an exported version, without requiring access to vendor systems, network services, or the original signing hardware.

In one aspect, the invention provides a method comprising: receiving a hardware-attested attestation artifact comprising a digital signature from a hardware secure element; computing a chain entry hash comprising the SHA-256 hash of the attestation artifact concatenated with the hash of the preceding chain entry; appending the chain entry to an append-only local data store; and producing an independently verifiable exported ledger file.

In another aspect, the invention provides a system comprising a local ledger data store, a chain entry computation module, a hardware attestation interface, and a verification module operable without network connectivity.

---

## DETAILED DESCRIPTION OF THE INVENTION

### 1. Overview

The ZK-LocalChain ledger is an append-only data structure stored in local persistent storage (such as a relational database, file system, or structured data store) that maintains a cryptographically linked sequence of hardware-attested attestation artifacts. The Ledger is designed for field deployment without network connectivity and is independently verifiable by export.

### 2. Chain Structure

**2.1 Genesis Entry**

The first entry in the Ledger is the genesis entry. The genesis entry has a `prev_hash` field set to a known constant (e.g., the all-zeros string, or the SHA-256 hash of the empty string). All subsequent entries reference the genesis entry either directly (entry 1) or transitively (entries 2+).

**2.2 Chain Entry Format**

Each entry in the Ledger comprises the following fields:

```json
{
  "id": "<UUID>",
  "artifact_id": "<UUID matching the hardware artifact>",
  "artifact_type": "<enumerated: POWER_SESSION | ZKEY_SIGN | TRUST_SEAL | COMBINED_SESSION>",
  "device_id": "<hardware device serial number>",
  "session_id": "<optional UUID linking concurrent artifacts>",
  "challenge_hash": "<SHA-256 hash of the signed challenge>",
  "signature": "<ECDSA signature from hardware secure element>",
  "public_key": "<device public key for signature verification>",
  "signed_at": "<ISO 8601 timestamp>",
  "short_code": "<human-readable code derived from signature>",
  "prev_hash": "<SHA-256 hash of the preceding chain entry>",
  "entry_hash": "<SHA-256 hash of this entry's fields>",
  "chain_position": "<integer sequence number>",
  "metadata": "<optional structured field>"
}
```

**2.3 Entry Hash Computation**

The `entry_hash` for each entry is computed as:

```
entry_hash = SHA-256(
  artifact_id || artifact_type || device_id || session_id ||
  challenge_hash || signature || public_key || signed_at ||
  short_code || prev_hash || chain_position
)
```

Where `||` denotes concatenation of canonically serialized field values.

**2.4 Chain Linkage**

Each entry's `prev_hash` field contains the `entry_hash` of the immediately preceding entry. For the genesis entry, `prev_hash` is a known constant. This structure creates a hash chain in which any modification to any entry — including its content, its `prev_hash`, or its position — causes a mismatch between the computed `entry_hash` and the `prev_hash` recorded in the subsequent entry.

### 3. Hardware Attestation Requirement

A distinguishing feature of the Ledger is that each entry originates from a hardware-attested attestation artifact: a structured record produced by a hardware secure element (HSE) within a physical signing device (PAT-001 ZKKey) or power verification device (PAT-002 PowerVerify). The `signature` field of each entry is an ECDSA signature generated by the HSE using a device private key stored in tamper-resistant hardware.

This hardware attestation requirement means that fabricating a chain entry requires physical possession of the signing device. An attacker who compromises the software layer of the evidence management system cannot fabricate valid chain entries without the physical hardware device.

### 4. Offline Operation

The Ledger operates entirely without network connectivity. All operations — appending entries, computing hashes, and verifying the chain — are performed locally:

- **Appending entries:** The chain computation and data store write require only local compute and storage. No network call is made during entry creation.
- **Verification:** The hash chain can be verified by iterating through all entries in sequence, recomputing each `entry_hash`, and confirming that each entry's `prev_hash` matches the `entry_hash` of the preceding entry. This computation requires only the exported ledger file and a SHA-256 implementation.
- **Synchronization (optional):** Upon restoration of network connectivity, the local Ledger may optionally synchronize with a remote ledger by transmitting entries that have not yet been synchronized. The remote ledger validates each entry's hardware attestation and chain linkage before accepting it.

### 5. Independent Verification

The Ledger is designed so that any party with access to an exported version of the Ledger can independently verify its integrity without vendor involvement:

**5.1 Export Format**

The Ledger can be exported as a JSON Lines file, a CSV file, or a signed PDF report. The export includes all chain entries in sequence order.

**5.2 Verification Procedure**

A verifying party performs the following steps, which require only standard computing tools and a SHA-256 implementation:

1. Load the exported Ledger entries in sequence order.
2. For the genesis entry, confirm `prev_hash` equals the known constant.
3. For each entry N, recompute `entry_hash_N` from the entry's fields.
4. Confirm that `entry_hash_N` equals the `prev_hash` field of entry N+1.
5. For each entry with an ECDSA signature, optionally verify the signature against the device public key using standard ECDSA verification.
6. If all checks pass, the ledger is intact; no entries have been inserted, deleted, or modified.

**5.3 Short Code Resolution**

Each chain entry contains a `short_code` derived deterministically from the ECDSA signature (PAT-010). A verifying party may also resolve the short code at a public verification service (e.g., verifyknot.io/{short_code}) to retrieve the chain entry display without accessing the raw ledger file. This provides a second, human-accessible verification path requiring only a web browser.

### 6. Combined Session Entry

In a preferred embodiment for evidence custody, the Ledger supports a `COMBINED_SESSION` entry type that binds a power attestation record (PAT-002) and a signing attestation record (PAT-001) into a single chain entry. This combined entry, described in detail in co-pending PAT-007, provides cryptographic proof that a specific device was powered without data exchange and a specific human approved a specific evidence hash within the same custody session.

### 7. Synchronization Architecture

While the Ledger operates offline, it supports an optional synchronization model for deployments with intermittent connectivity:

- **Local-first:** All entries are written to local storage first. Network availability is never a prerequisite for chain entry creation.
- **Sync-on-connect:** When connectivity is restored, the local client transmits unsynchronized entries to a remote ledger service.
- **Remote validation:** The remote service validates each entry's hardware attestation (ECDSA signature against known device public key) and chain linkage before accepting.
- **Conflict resolution:** If two local clients created entries during the same offline period, the remote service accepts both chains and creates a merge record. Chain integrity is maintained for each local sub-chain.

### 8. Deployment Contexts

**8.1 Election Auditing**

A ZK-LocalChain instance running on a field tablet is carried by an election observer. The observer uses a ZKKey device to attest ballot custody events throughout election day. All attestation artifacts are recorded in the local Ledger without network connectivity. At the end of the day, the Ledger is exported and transmitted to the county election office, which verifies the chain integrity and individual hardware attestations independently.

**8.2 Forensic Evidence Collection**

A law enforcement officer uses a ZKKey and PowerVerify in the field to attest evidence collection events. All events are recorded in a local Ledger on a ruggedized tablet. The Ledger is exported at end of shift and appended to the case file. The prosecutor independently verifies the chain before trial without contacting the vendor.

**8.3 Pharmaceutical Custody**

A pharmaceutical courier uses a TrustSeal device to attest seal application events at each custody handoff. Attestation artifacts are recorded in the local Ledger. At delivery, the recipient exports and verifies the Ledger to confirm all custody events are intact and hardware-attested.

---

## CLAIMS

**Claim 1.** A method for maintaining a hardware-attested chain-of-custody ledger comprising:
receiving, at a local data store, a hardware-attested attestation artifact comprising a digital signature generated by a hardware secure element of a physical signing device;
computing a chain entry hash by applying a hash function to a combination of fields of the attestation artifact and a hash of a preceding entry in the local data store;
appending a chain entry comprising the attestation artifact fields and the chain entry hash to the local data store in an append-only manner;
wherein the appending does not require network connectivity; and
wherein the chain entry is independently verifiable by any party having access to an exported version of the local data store by recomputing the chain entry hash from the chain entry fields and comparing to the chain entry hash stored in the subsequent entry.

**Claim 2.** The method of claim 1, wherein the hash function is SHA-256.

**Claim 3.** The method of claim 1, wherein a first entry in the local data store is a genesis entry having a preceding entry hash field set to a predefined constant.

**Claim 4.** The method of claim 1, further comprising exporting the local data store as a self-contained file comprising all chain entries in sequence order, wherein the exported file is independently verifiable without network access, vendor systems, or access to the physical signing device.

**Claim 5.** The method of claim 1, further comprising generating a human-readable short code derived deterministically from the digital signature of the attestation artifact, wherein the short code is stored in the chain entry and is resolvable at a public verification service to display the chain entry.

**Claim 6.** The method of claim 1, wherein the hardware-attested attestation artifact is generated by a user-actuated signing device that displays a cryptographic hash of a challenge to a user and requires physical actuation of a hardware input element before the hardware secure element generates the digital signature.

**Claim 7.** The method of claim 1, wherein the hardware-attested attestation artifact is generated by a power verification device comprising VBUS and GND conductors and physically absent D+ and D- data conductors.

**Claim 8.** The method of claim 1, further comprising appending a combined chain entry comprising a first attestation artifact generated by a power verification device and a second attestation artifact generated by a user-actuated signing device, the first and second attestation artifacts sharing a session identifier.

**Claim 9.** The method of claim 1, further comprising, upon restoration of network connectivity, synchronizing the local data store with a remote ledger service by transmitting chain entries that have not been previously synchronized.

**Claim 10.** A system for offline hardware-attested evidence custody comprising:
a local data store configured to store chain entries in an append-only manner without network connectivity;
a chain entry computation module configured to compute a chain entry hash for each incoming attestation artifact using a hash function applied to the attestation artifact fields and the hash of the preceding chain entry; and
a verification module configured to verify the integrity of the local data store by iterating through chain entries in sequence, recomputing each chain entry hash, and confirming that each chain entry hash matches the preceding hash field of the subsequent entry;
wherein the verification module operates without network connectivity.

**Claim 11.** The system of claim 10, further comprising a hardware attestation interface configured to receive attestation artifacts from one or more hardware signing devices, each attestation artifact comprising a digital signature generated by a hardware secure element of the respective hardware signing device.

**Claim 12.** The system of claim 10, further comprising a public verification service configured to resolve a human-readable short code to a chain entry display, wherein the public verification service is accessible without account credentials.

**Claim 13.** The system of claim 10, wherein the local data store is hosted on a field-deployable computing device and the chain entry computation module operates without any network dependency.

**Claim 14.** A chain-of-custody ledger comprising:
a sequence of chain entries stored in an append-only local data store;
wherein each chain entry comprises:
  a hardware-attested attestation artifact comprising a digital signature generated by a hardware secure element;
  a preceding entry hash field containing the hash of the immediately preceding chain entry; and
  an entry hash field containing a hash computed from the chain entry's fields including the preceding entry hash field;
wherein the integrity of the ledger is independently verifiable by any party with access to an exported version of the ledger by recomputing each entry hash and confirming sequential hash linkage; and
wherein the ledger is operational without network connectivity.

**Claim 15.** The chain-of-custody ledger of claim 14, wherein the ledger supports a combined entry type comprising a power attestation record from a power verification device and a signing attestation record from a user-actuated signing device, the two records sharing a session identifier.

**Claim 16.** The chain-of-custody ledger of claim 14, wherein each chain entry further comprises a human-readable short code derived deterministically from the digital signature of the attestation artifact.

---

## ABSTRACT

An offline-capable append-only hash-chained evidence ledger records hardware-attested attestation artifacts from physical signing and power verification devices. Each ledger entry includes the cryptographic hash of the preceding entry, creating a tamper-evident chain in which any modification to any entry is detectable by hash recomputation. The ledger operates without network connectivity, enabling field deployment in rural, restricted, or disconnected environments. Any party with access to an exported version of the ledger can independently verify its integrity by iterating through entries and recomputing hash linkages, without requiring network access, vendor systems, or central authority involvement. Entries are produced exclusively by hardware secure elements, preventing fabrication of chain entries without physical possession of the signing hardware.

---

## IDS — Prior Art to Disclose

1. Fromm et al., "Chronological independently verifiable electronic chain of custody ledger using blockchain technology," ScienceDirect/Forensic Science International: Digital Investigation, 2020
2. US11410233B2 — Blockchain technology to settle transactions (append-only ledger), 2022
3. US10163080B2 — Document tracking on a distributed ledger, 2019
4. US11418322B2 — Information management in decentralized database (Hyperledger), 2022
5. Nakamoto, S., "Bitcoin: A Peer-to-Peer Electronic Cash System," 2008 (hash-chaining prior art)
6. US9774578B1 — Distributed key secret for rewritable blockchain, 2017
7. Microsoft SQL Server 2022 Ledger documentation (append-only ledger tables), 2022
8. National Institute of Standards and Technology, "Blockchain Technology Overview," NISTIR 8202, 2018

---

*DRAFT — For attorney review. Not yet filed. Priority date: January 15, 2026.*
*Inventor: William Shane Wilkinson | ZKNOT, Inc. | ops@zknot.io*
