# Field-Verifiable Optical Physical Unclonable Functions Bound to Cryptographically Attested Hardware Ledgers

**A Technical Disclosure for Defensive Publication**

**Author:** William Shane Wilkinson
**Affiliation:** ZKNOT, INC.
**Date:** April 24, 2026
**Publication Venue:** GitHub (public repository) + zknot.io / verifyknot.io (future mirror)
**License:** CC-BY 4.0 — free to use, attribution appreciated
**Document Purpose:** This document constitutes a defensive publication. Its purpose is to establish prior art for the concepts described herein, preventing subsequent patent claims by other parties over the same subject matter. It does not waive ZKNOT, INC.'s rights to file its own patent applications on improvements, embodiments, or related inventions.

Page 1 of 6

---

## Abstract

This disclosure describes a method for binding an optical Physical Unclonable Function (PUF) — produced by random particle distribution in a transparent potting compound applied to an electronic device — to a cryptographically attested, vendor-irrevocable, offline-verifiable ledger entry, such that any end user with a consumer camera can confirm device integrity in the field without specialized hardware and without network connectivity. The potting compound simultaneously serves as both the optical PUF substrate and the physical tamper barrier, creating a dual-function material layer where defeating either function necessarily damages the other.

## 1. Background

Optical PUFs based on random particle distribution in transparent matrices have been known since at least Pappu et al., "Physical One-Way Functions" (Science, 2002). Cryptographic binding of device identifiers to distributed ledgers is commonplace. The combination of these elements, however, has been pursued predominantly in contexts requiring network-connected verification against a central database, using specialized PUF readers, and without integration into a device's core tamper-evidence strategy.

This disclosure addresses three limitations of prior approaches:

- Dependence on network-reachable verification infrastructure
- Requirement for specialized PUF capture hardware
- Treatment of the PUF substrate as a separate layer from the physical tamper barrier

## 2. The Disclosed System

### 2.1 Physical Layer

An electronic device with exposed internal components is potted using a transparent two-part epoxy resin loaded with randomly distributed optically distinctive particles. Suitable particles include but are not limited to: holographic microflakes (approximately 30–80 μm), metallic flakes, phosphorescent granules, or fluorescent fibers. The particles are distributed throughout the resin volume by brief agitation during pouring, with no attempt to control placement — randomness is the cryptographically valuable property.

After curing, the cured potting layer performs two functions simultaneously:

- **Function A (tamper barrier):** Physically impedes access to the underlying electronics. Removal destroys the layer visibly; re-pouring produces a different particle pattern.
- **Function B (optical PUF):** The specific three-dimensional arrangement of particles in the cured volume constitutes a physically unclonable fingerprint for that unit.

### 2.2 Manufacturing-Time Registration

At manufacture, after the potting layer has cured:

1. The device is photographed under controlled lighting from a fixed reference geometry.
2. The captured image is processed to extract one or more stable feature representations — for example, a perceptual hash, a set of SIFT/ORB keypoints, or a neural feature embedding.
3. The feature representation is combined with the device's cryptographic identity (derived from a secure element bound to the device during manufacture).
4. The combined record is signed by two cryptographically separated secure elements: one representing device identity, the other representing the manufacturing authority. Neither signature alone is sufficient.
5. The dual-signed record is committed to an append-only ledger whose integrity properties include vendor-irrevocability — that is, the manufacturer, post-commit, cannot alter the record.
6. The reference image and ledger entry identifier are packaged with the device (e.g., included in shipping documentation, available via QR code lookup, or cached in a field verification application).

Page 2 of 6

### 2.3 Field Verification

A user in the field, wishing to confirm device integrity before use:

1. Scans a device-identifying code (QR, serial, or similar) to retrieve the reference image and ledger record.
2. Captures a current image of the device using a consumer camera (phone) approximating the reference geometry.
3. Computes the same feature representation on the current image.
4. Compares the current representation against the reference.
5. If the representations match within a defined tolerance: device is confirmed original and untampered.
6. If they diverge beyond tolerance: device has been tampered with, damaged, or replaced.

Crucially, this verification requires no network connection once the reference image is cached locally, and requires no specialized hardware beyond a phone camera.

### 2.4 Compositional Security Property

The potting layer cannot be removed to access internals without destroying the optical pattern, because the pattern exists throughout the three-dimensional volume of the resin. Repouring produces a new random pattern that will not match the ledger-attested reference. Therefore:

- An attacker who defeats the tamper barrier necessarily fails the optical verification.
- An attacker who somehow preserves the optical pattern has not defeated the tamper barrier.
- An attacker who replaces the device entirely fails because the new device's PUF was never registered to the original ledger entry.

The security of the system reduces to: the cryptographic strength of the ledger and signatures, the entropy of the particle distribution, and the stability of the imaging/feature-extraction pipeline.

---

## 3. Implementation Considerations

### 3.1 Particle Selection

Particle size, shape, reflectivity, and loading density affect both uniqueness and stability. Finer particles yield higher spatial entropy but may require higher-resolution imaging. Reflective (holographic) particles produce viewpoint-dependent patterns, which can either enhance uniqueness (if captured from a fixed geometry) or harm stability (if geometry is not controlled). Fluorescent or phosphorescent particles allow capture under controlled excitation wavelengths, reducing ambient-lighting sensitivity.

### 3.2 Capture Geometry

Reference and field captures must use approximately the same geometry — distance, angle, focal length, lighting direction. A simple mechanical alignment aid (a printed frame, a QR-code-indexed focus target, a phone case-integrated standoff) can enforce this without user training.

### 3.3 Feature Representation

Perceptual hashing alone is often insufficient; combining pHash with keypoint-based matching (ORB, SIFT) or a small neural embedding improves robustness to minor geometric variation. The feature representation committed to the ledger should be the one used at verification — not the raw image — to bound the comparison operation and allow efficient offline verification.

### 3.4 Tolerance Setting

The verification threshold must balance two errors: false reject (legitimate device flagged as tampered) and false accept (tampered device passes verification). Threshold is set empirically based on measured intra-device stability and inter-device uniqueness distributions. A threshold at least 3× the observed maximum intra-device distance, and at most 1/3 the observed minimum inter-device distance, provides acceptable margins.

Page 3 of 6

### 3.5 Ledger Properties

The ledger used must support: append-only semantics, cryptographic chain integrity, multi-signature commitment, and offline-resolvable queries (a cached ledger snapshot must be usable for verification without live network access). The ledger must further support vendor-irrevocability — the manufacturer cannot retroactively alter or redact committed entries.

---

## 4. Threat Model

The disclosed system is designed to defeat the following attack vectors:

**Supply chain interdiction.** An adversary intercepts a device in transit, opens the potted enclosure to insert a hardware implant, and re-pots to restore appearance. The attacker's re-potted unit produces a different optical pattern than the reference. Verification fails.

**Counterfeit substitution.** An adversary produces a visually similar device and substitutes it for the original. The counterfeit was never registered to the ledger; lookup fails or returns a record that does not match the counterfeit's features. Verification fails.

**Manufacturer compromise.** An adversary compromises the manufacturer and attempts to alter existing ledger records to match a substituted device. Vendor-irrevocability prevents this; the record is append-only and dually signed. Verification against the original ledger state still fails.

**Partial tampering.** An adversary drills into the potting to access a specific component without removing the full layer. The drilled region disturbs the particle distribution locally; feature-based verification detects the localized change.

**Replay / image substitution.** An adversary captures the reference image and attempts to substitute it for their own device's capture. Defeated by requiring fresh capture of the current device at verification time, bound to the verifier's session through a challenge-response extension.

### 4.1 Known Limitations

The system does not defeat:

- Attacks on the secure element identity directly (outside scope — addressed by separate architecture)
- Attacks that preserve the exact particle distribution while modifying underlying electronics (considered practically infeasible due to 3D entropy of the volume, but not cryptographically precluded)
- Coercion of legitimate users into accepting tampered devices (social engineering, outside scope)
- Degradation of the potting material over time (addressable via periodic re-verification and ledger-recorded aging tolerance)

---

## 5. Novel Contributions (For Prior Art Purposes)

The following combinations are disclosed as prior art with respect to future patent filings by third parties:

1. The combination of a transparent potted tamper barrier that also serves as an optical PUF substrate, where the two functions share a single material layer.
2. The binding of such a PUF's feature representation to a ledger entry signed by two cryptographically separated secure elements, one representing device identity and the other representing manufacturing authority.
3. The offline verification of such a PUF using a cached ledger snapshot and a consumer camera, without network connectivity at verification time.
4. The use of vendor-irrevocable ledger semantics (append-only, no retroactive alteration by the committing party) as the trust root for such PUF records.
5. The composition of the above with a cryptographically attested power-delivery-only passthrough device (i.e., a device whose data-path has been physically eliminated by design), producing a single attestation covering both physical tamper integrity and data-path integrity.

Page 4 of 6

---

## 6. Suggested Parameters (Non-Limiting)

Provided as implementation guidance, not as claim limitations:

- Particle loading: 1–5% by volume
- Particle size: 30–80 μm median, with broad distribution for entropy
- Capture resolution: ≥ 8 megapixel, macro-focus capable
- Feature representation: 256-bit composite (128-bit pHash + 128-bit ORB descriptor cluster hash)
- Tolerance margin: threshold at approximately the geometric mean of maximum intra-device distance and minimum inter-device distance
- Ledger commitment: dual ECDSA signatures over SHA-256 of (device_id || feature_vector || timestamp || manufacturer_id)
- Reference image retention: at manufacture and at each ledger-recorded maintenance event

---

## 7. Example Operational Scenarios

**Scenario A — Power-only passthrough device for forensic evidence protection.** A field investigator receives a device from inventory, scans its QR, retrieves the cached ledger record and reference image, compares visually using the verification app, confirms match, and proceeds to use the device to charge evidence without data exfiltration risk. Total verification time: under five seconds. No network required.

**Scenario B — Supply chain audit.** A procurement officer receiving a shipment of 100 devices batch-verifies each unit against ledger records. Any device that fails verification is quarantined. Failure analysis is simplified by the dual-signature record, which identifies which manufacturing authority signed the original commit.

**Scenario C — Post-incident integrity confirmation.** After a device has been out of custody for a period, the holder re-verifies it before returning to service. The ledger record may be augmented with maintenance-event entries, each dually signed and appended. A device passing verification against the latest record is confirmed not to have been tampered with since the most recent signed event.

---

## 8. Relationship to Existing ZKNOT Portfolio

This disclosure references and builds upon the following ZKNOT patent filings, any of which may be cited for additional context:

- **Power-Delivery Interface With Physical Data-Path Elimination** (U.S. Provisional 63/961,118, filed January 15, 2026)
- **Tamper-Evident Physical Seal With Cryptographic Binding to a Digital Evidence Ledger** (U.S. Provisional 63/961,112, filed January 15, 2026)
- **Cryptographically Chained Device-Signed Event Ledger for Verifiable Real-World Evidence** (U.S. Provisional 63/961,098, filed January 15, 2026)
- **Dual Secure Element Architecture** (U.S. Provisional 64/007,907, filed March 17, 2026)
- **Tamper-Evident, Cryptographically Verified Power-Only Delivery Interface With Multi-Layer Integrity Attestation** (U.S. Provisional 64/007,940, filed March 17, 2026)

This disclosure does not constitute an admission that any subject matter herein is outside the scope of the above filings.

Page 5 of 6

---

## 9. Citation

If you reference or build on this disclosure, please cite as:

> Wilkinson, W. S. (2026). *Field-Verifiable Optical Physical Unclonable Functions Bound to Cryptographically Attested Hardware Ledgers.* Technical Disclosure, ZKNOT, INC. Published April 24, 2026. CC-BY 4.0.

---

## 10. Contact

William Shane Wilkinson
ZKNOT, INC.
ops@zknot.io

---

## Disclaimer

This document is published as a defensive technical disclosure to establish prior art. Publication does not constitute a grant of any patent license, express or implied, from ZKNOT, INC. or its successors. ZKNOT, INC. reserves the right to file patent applications on specific embodiments, improvements, or related inventions not disclosed herein.

Nothing in this document should be construed as legal advice. Parties seeking to implement the disclosed methods should consult qualified counsel regarding applicable intellectual property, export control, and regulatory requirements in their jurisdiction.

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-24 | Initial publication |

Page 6 of 6
