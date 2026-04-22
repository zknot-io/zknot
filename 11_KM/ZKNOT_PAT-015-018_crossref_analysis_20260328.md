# PAT-015 / PAT-018 Cross-Reference Analysis vs. PAT-002
## Document: ZKNOT_PAT-015-018_crossref_20260328
### Prepared: March 28, 2026 | For Attorney Review

---

## PURPOSE

PAT-015 and PAT-018 are the two newest patents in the portfolio (March 16, 2026 filing). Both relate to USB data-path verification and expand the PowerVerify concept (PAT-002, Jan 15, 2026). This document maps the claim boundaries to prevent overlap, identify distinct novel elements, and guide non-provisional drafting strategy for each.

---

## PAT-002 RECAP — CORE CLAIM BOUNDARY

PAT-002 (PowerVerify, Jan 15 2026) covers:
- An inline USB device in which D+ and D- conductors are **physically absent**
- Only VBUS and GND pass through
- Absence is continuity-testable by any party with a multimeter
- Optional: hardware secure element generates a power session attestation record
- Optional: passive variant with no electronics whatsoever

**PAT-002 claims:** Physical absence of data conductors + continuity-testability as proof + optional attestation record generation

**PAT-002 does NOT claim:**
- Monitoring of existing connections for data activity
- Detection of whether data signaling is actually occurring on conductors that ARE present
- Electrical behavior anomaly detection (current draw, impedance profiles)
- Multi-layer physical tamper evidence integrated into the device casing
- CC-line negotiation monitoring
- SuperSpeed pair elimination (USB 3.x) — mentioned but not the primary claim

---

## PAT-018 — PowerVerifyPlus Analysis

### What PAT-018 Adds Over PAT-002

PAT-018 is explicitly an EXTENSION of PAT-002 (it cross-references App. No. 63/961,118 by number). The additional inventive elements are:

**1. Full Data-Path Elimination (not just D+/D-)**
PAT-002's primary claim covers D+ and D-. PAT-018 extends to ALL USB data-capable conductors:
- D+, D- (USB 2.0 data — covered by PAT-002)
- TX1+, TX1-, TX2+, TX2-, RX1+, RX1-, RX2+, RX2- (SuperSpeed differential pairs — USB 3.x)
- SBU1, SBU2 (Sideband Use lines — USB-C alternate mode signaling)

**Distinct claim:** "Physical elimination of all data-capable conductors including SuperSpeed differential pairs and SBU lines" — PAT-002 could read on a device that only eliminates D+/D- but retains SuperSpeed pairs. PAT-018's claim is broader and explicitly covers USB 3.x capable devices.

**2. Multi-Layer Tamper Evidence**
PAT-018 specifies at least three INDEPENDENT physical tamper detection mechanisms whose collective state is incorporated into the signed session record. The session record attests not just to power delivery but to whether the device housing was tampered with. This is a distinct claim element not in PAT-002.

Examples from spec: optical void tape, mesh tamper grid, holographic overlay, frangible enclosure elements, potted epoxy cavity — multiple independent mechanisms.

**Distinct claim:** "A session record that incorporates the collective tamper-detection state of at least three independent physical tamper mechanisms."

**3. Sealed Secondary Verification Interface**
A second physical interface (e.g., NFC, QR window, secondary USB port) that is physically isolated from BOTH the primary power conductors AND the primary data conductor pads. The session record is accessible via this interface without exposing the primary circuit to any connection.

**Distinct claim:** "A secondary interface physically isolated from both the primary VBUS conductor and the primary data conductor pads, through which session records are accessible without connecting to the primary power path."

**4. Power Delivery Parameter Logging**
The session record captures voltage and current measurements over time throughout the session — not just a binary "power delivered" attestation. This creates a power delivery profile that can be compared to expected profiles for specific device types.

**Distinct claim:** "A session record comprising power delivery parameters sampled at configurable intervals during the session duration."

**5. CC-Line Interaction Attestation**
USB-C CC lines are used for Power Delivery negotiation. PAT-018 monitors CC-line activity to attest that no data-capable negotiation occurred — confirming that only power negotiation (PD protocol) was executed, not alternate mode negotiation (which could establish data channels).

**Distinct claim:** "Attestation that CC-line activity did not include data-capable protocol exchanges during the session."

### Claim Boundary Recommendations for PAT-018

**DO claim (distinct from PAT-002):**
- Elimination of SuperSpeed pairs AND SBU lines in addition to D+/D-
- Multi-layer physical tamper evidence integrated into session records
- Sealed secondary verification interface physically isolated from primary circuit
- Power delivery parameter sampling and logging over session duration
- CC-line negotiation monitoring and attestation

**DO NOT claim (PAT-002 territory — reference instead):**
- Physical absence of D+/D- conductors (cite PAT-002)
- Basic power session attestation record with session_id and ECDSA signature (cite PAT-002)
- Continuity-testability of data conductor absence (cite PAT-002)

**Risk:** PAT-018 Claim 1 cannot be identical to PAT-002 Claim 1. The broadest independent claim in PAT-018 must distinguish by at least one of: SuperSpeed elimination, tamper evidence integration, secondary interface, or power parameter logging. Recommend: distinguish by SuperSpeed/SBU elimination as the primary scope expansion.

---

## PAT-015 — DataGapUSBDetect Analysis

### What PAT-015 Is — Completely Distinct from PAT-002

PAT-015 is NOT an extension of PAT-002. It is an INVERSE and COMPLEMENTARY device:

- **PAT-002 (PowerVerify):** Eliminates data conductors from YOUR device. Proves YOUR connection has no data path.
- **PAT-015 (DataGapUSBDetect):** Monitors an EXISTING third-party connection to determine whether data IS flowing. Proves whether someone ELSE'S connection is carrying data.

These are orthogonal claims with no overlap risk.

### PAT-015 Core Claim Elements

**1. Passive High-Impedance Data-Path Monitoring**
The device taps D+, D-, and SuperSpeed pairs via a high-impedance circuit that does NOT disturb the monitored connection — it does not inject signal, draw current from data lines, or enumerate as a USB device. It observes passively.

**Distinct claim:** "A passive high-impedance tap on USB data conductors that monitors for signaling activity without disturbing the monitored connection, injecting signal, or enumerating as a USB device."

**2. Electrical Behavior Measurement and Classification**
The device measures: current draw profiles (magnitude, timing, transient characteristics); VBUS voltage characteristics; impedance of data conductors; and compares to reference profiles for known-good device categories and known anomalous signatures.

**Distinct claim:** "Comparison of measured electrical behavior against reference profiles for known device categories to classify the connected hardware as conforming or anomalous."

**3. Cryptographically Signed Witnessing Record**
The detection result — whether data signaling occurred, whether electrical behavior is anomalous — is produced as a cryptographically signed, hash-chained attestation artifact. A non-technical user can generate a court-admissible witnessing record of USB connection behavior without laboratory equipment or technical expertise.

**Distinct claim:** "A cryptographically signed attestation record certifying whether USB data-path signaling activity was detected during a specified time-bounded connection event, the record being independently verifiable by any party with the device's public key."

**4. No Prior Art Found for Cryptographic USB Witnessing**
Existing USB monitoring tools (oscilloscopes, protocol analyzers, USB sniffers) produce output that: requires technical expertise to interpret; is not cryptographically authenticated; cannot serve as independently verifiable evidence in legal proceedings; and requires laboratory equipment inaccessible to field users.

The specific combination of passive monitoring + electrical behavior classification + cryptographic signing producing a court-ready witnessing artifact appears to have no direct prior art.

### Claim Boundary Recommendations for PAT-015

**DO claim:**
- Passive high-impedance monitoring without signal injection or device enumeration
- Combined detection of data-path activity AND electrical behavior anomalies in a single device
- Cryptographically signed tamper-evident record of USB connection behavior
- Classification of connected device as conforming or anomalous based on electrical signature comparison
- Non-technical user accessibility — LED/display output without requiring oscilloscope interpretation

**No overlap with PAT-002** because:
- PAT-002: Device IN the connection, eliminates data paths
- PAT-015: Device ADJACENT to connection, monitors passively
- Different physical architecture, different claim structure, different use case

**Potential overlap area to watch:** Both PAT-002 and PAT-015 generate ECDSA-signed attestation records. The record FORMAT is similar. Ensure PAT-015 claims the specific content of the witnessing record (detection result, measurement data) rather than the general format (which PAT-002 also covers).

---

## COMBINED PORTFOLIO MAP — PAT-002 FAMILY

```
PAT-002 PowerVerify (Jan 15, 2026)
    └── Core claim: Physical absence of D+/D- in inline device
    └── Priority date: EARLIEST in family
    └── Non-prov deadline: Jul 31, 2026

PAT-018 PowerVerifyPlus (Mar 16, 2026)
    └── Extends PAT-002 to: SuperSpeed pairs, SBU lines, tamper evidence, secondary interface
    └── Priority date: Mar 16, 2026 (6 weeks after PAT-002)
    └── Non-prov deadline: Mar 16, 2027 (1 year from filing)
    └── IMPORTANT: Does not claim what PAT-002 already claimed

PAT-015 DataGapUSBDetect (Mar 16, 2026)
    └── Orthogonal to PAT-002 family: monitoring, not elimination
    └── Complementary product: verifies that a third-party connection is clean
    └── Priority date: Mar 16, 2026
    └── Non-prov deadline: Mar 16, 2027
    └── NO overlap with PAT-002
```

---

## NON-PROVISIONAL DRAFTING RECOMMENDATIONS

### PAT-018 Non-Provisional Strategy

**File as continuation-in-part (CIP) of PAT-002** — this preserves PAT-002's Jan 15, 2026 priority date for the D+/D- elimination claims that are shared, while establishing Mar 16, 2026 priority date for the new matter (SuperSpeed elimination, tamper evidence, secondary interface).

**Independent Claim 1:** Should distinguish from PAT-002 Claim 1 by including at least SuperSpeed differential pair elimination (not just D+/D-).

**Suggested Claim 1 structure:**
"An inline USB power delivery device comprising: VBUS and GND conductors connecting upstream and downstream connectors; wherein the device does not comprise D+, D-, TX1+, TX1-, TX2+, TX2-, RX1+, RX1-, RX2+, RX2-, SBU1, or SBU2 conductors; and at least [one tamper evidence element / a secondary verification interface / power parameter logging] ..."

### PAT-015 Non-Provisional Strategy

**File as standalone application** — no CIP relationship to PAT-002. Separate invention.

**Independent Claim 1:** Lead with the passive high-impedance monitoring claim — this is the most defensible and broadest element.

**Suggested Claim 1 structure:**
"A device for witnessing USB connection behavior comprising: a passive high-impedance electrical interface configured to monitor USB data conductors for signaling activity without injecting signal, drawing current from monitored data conductors, or enumerating as a USB device; a measurement subsystem configured to measure electrical characteristics of the monitored connection; a hardware secure element configured to generate a cryptographically signed attestation record certifying whether data-path signaling activity was detected during a defined connection period; wherein the attestation record is independently verifiable by any party having the device's public key."

---

## DEADLINE SUMMARY FOR ALL NEW PATENTS

| Patent | Filed | Non-Prov Deadline | Strategy |
|---|---|---|---|
| PAT-002 | Jan 15, 2026 | **Jul 31, 2026** | Standard conversion |
| PAT-018 | Mar 16, 2026 | Mar 16, 2027 | CIP of PAT-002 |
| PAT-015 | Mar 16, 2026 | Mar 16, 2027 | Standalone |
| PAT-005 | Jan 20, 2026 | Jan 20, 2027 | Standard conversion |
| PAT-006 | Jan 3, 2026 | Jan 3, 2027 | Standard conversion |

---

*Document prepared for internal use and attorney review. Not legal advice.*
*ZKNOT, Inc. | ops@zknot.io | UEI: C4SKW13JPEL5*
