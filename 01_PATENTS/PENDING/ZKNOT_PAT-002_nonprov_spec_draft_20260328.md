# PATENT APPLICATION DRAFT
## PAT-002: PowerVerify — Physical Data-Path Elimination Device
### Non-Provisional Patent Application — Pro Se Draft for Attorney Review
### Priority: US Provisional App. No. 63/961,118 (Filed January 15, 2026)

---

## TITLE OF INVENTION

**POWER DELIVERY DEVICE WITH PHYSICALLY ABSENT DATA CONDUCTORS FOR HARDWARE-ATTESTED DATA-TRANSFER ELIMINATION**

---

## CROSS-REFERENCE TO RELATED APPLICATIONS

This application claims priority to U.S. Provisional Patent Application No. 63/961,118, filed January 15, 2026, entitled "PowerVerify — Physical Data-Path Elimination," incorporated herein by reference.

Related applications: PAT-001 (ZKKey), PAT-004 (ZK-LocalChain), PAT-007 (CombinedSession).

---

## BACKGROUND OF THE INVENTION

### Field of the Invention

The present invention relates to USB power delivery devices and evidence attestation systems, and more particularly to inline USB devices in which data conductors are physically absent, thereby providing a hardware-verifiable attestation that no data transfer occurred between a power source and a powered device.

### Description of Related Art

In digital forensics, law enforcement, election auditing, pharmaceutical supply chain, and other regulated industries, the ability to prove that a device was powered without any data exchange is a recurring evidentiary requirement. Current approaches rely on software-based write-blocking, hardware write-blocker devices, procedural documentation, and witness attestation. These approaches suffer from fundamental limitations:

**Software write-blockers** rely on operating system drivers and policy enforcement. They can be bypassed by operating system exploits, driver vulnerabilities, or deliberate misconfiguration. They provide no hardware-verifiable proof that data was blocked.

**Hardware write-blocker devices** (such as those described in US6813682) operate by intercepting and blocking write commands at the hardware level. However, they contain data conductors and active firmware that process USB traffic. The presence of data conductors means that a data-capable connection exists between the source and target devices, and independent verification requires expert testimony about the firmware's correct operation.

**Procedural documentation** (chain-of-custody forms, witness signatures, numbered seals) provides a social and procedural record that is inherently contestable in legal proceedings. A skilled attorney can challenge the integrity of a paper chain of custody by questioning the witnesses, the completeness of documentation, or the possibility of undetected tampering.

What is needed is a USB inline device in which the absence of data conductors makes data transfer physically impossible by construction rather than by policy, software control, or active blocking — and where this absence is independently verifiable by any party using standard electrical measurement equipment without requiring expert knowledge of firmware or software.

---

## SUMMARY OF THE INVENTION

The present invention provides an inline USB power delivery device in which the data signaling conductors (D+ and D-) are physically absent from the device, making data transfer between the upstream power source and the downstream powered device physically impossible by construction. The device optionally generates a power session attestation record suitable for recording in a hardware-attested chain-of-custody ledger.

In one aspect, the invention provides a USB inline device comprising: a USB upstream connector for connection to a power source; a USB downstream connector for connection to a device to be powered; a VBUS power conductor connecting the upstream connector to the downstream connector; a GND conductor connecting the upstream connector to the downstream connector; wherein the device does not comprise D+ or D- data signaling conductors, and wherein the absence of said conductors renders data transfer between the upstream connection and the downstream connection physically impossible.

In another aspect, the invention provides a method for attesting data-transfer absence comprising: supplying electrical power through an inline USB device lacking data conductors; generating a power session attestation record comprising a session identifier, device identifier, and timestamp; and recording the attestation record in an append-only hash-chained ledger.

---

## DETAILED DESCRIPTION OF THE INVENTION

### 1. Overview

The PowerVerify device is an inline USB device positioned between a USB power source (e.g., a wall adapter, computer USB port, or power bank) and a USB-powered device (e.g., a laptop, tablet, mobile phone, or evidence collection device). The device provides the electrical continuity of VBUS and GND, enabling the downstream device to receive power. The device does not provide D+ or D- conductors, and no equivalent data signaling path exists within the device.

The physical absence of data conductors is the core inventive concept. This is distinct from:

- **Write-blocking:** A write-blocker has data conductors but intercepts write commands in the data stream. Data can flow; only write commands are blocked.
- **Data conductor disconnection:** A switch that opens D+ and D- has the conductors physically present but electrically disconnected. Reconnection is possible.
- **Signal termination:** Terminating D+ and D- to ground or to a defined voltage state still involves conductors being present.

In the PowerVerify device, D+ and D- conductors are not present in the device at all. There is no mechanism by which a software command, electrical condition, or physical intervention can cause data to flow through the device because there is no data pathway.

### 2. Physical Construction

**2.1 Upstream Connector**

In a preferred embodiment, the upstream connector is a USB-C receptacle (e.g., GCT USB4216-03-A or compatible) providing VBUS and GND connections. The USB-C connector has 24 pins in its full specification, including CC1, CC2, VBUS, GND, and multiple data pairs (TX1+/TX1-, RX1+/RX1-, TX2+/TX2-, RX2+/RX2-, D+/D-). In the PowerVerify device, only VBUS and GND pins are connected to internal conductors. All data-carrying pins (D+, D-, CC1, CC2, and SuperSpeed data pairs) are unconnected within the device.

**2.2 Downstream Connector**

In a preferred embodiment, the downstream connector is a USB-A plug, USB-C plug, or USB Micro-B plug depending on the target device. As with the upstream connector, only VBUS and GND pins are connected within the device. All data pins of the downstream connector are unconnected.

**2.3 Internal PCB**

The printed circuit board (PCB) of the PowerVerify device comprises:
- A VBUS trace connecting upstream VBUS pins to downstream VBUS pins
- A GND trace connecting upstream GND pins to downstream GND pins
- Optional: passive current-limiting or protection components in the VBUS path
- Optional: a hardware secure element and microcontroller for power session attestation (described below)

The PCB does not comprise D+ traces, D- traces, or any conductor connecting any data-capable pin of the upstream connector to any data-capable pin of the downstream connector.

**2.4 Verification by Continuity Testing**

The absence of data conductors is independently verifiable by any party using a standard electrical continuity tester (multimeter in continuity mode) without firmware, software, or specialized equipment. To verify:

1. Set multimeter to continuity mode.
2. Place probes on D+ of upstream connector and D+ of downstream connector.
3. Absence of continuity tone/reading confirms no D+ conductor is present.
4. Repeat for D-.
5. Optionally verify VBUS and GND continuity to confirm the device is functional for power delivery.

This verification procedure requires no expert knowledge, no specialized software, no access to firmware or configuration data, and no access to ZKNOT's systems. The result — data conductors absent — is an objective physical fact determinable by any party in possession of a $15 multimeter.

This creates a unique evidentiary property: the proof of data-transfer impossibility is available to any fact-finder without vendor involvement. In a legal proceeding, a non-expert witness can perform the continuity test and testify to the result.

### 3. Power Session Attestation

In an enhanced embodiment, the PowerVerify device includes an optional hardware secure element and microcontroller that generate a power session attestation record when the device is connected.

**3.1 Components**

- Hardware secure element (e.g., ATECC608B-class) storing a device private key
- Microcontroller (e.g., STM32-class) for session management
- Power-on detection circuit to trigger attestation upon USB power connection

**3.2 Attestation Record Generation**

Upon detecting power delivery (VBUS rising edge), the microcontroller:
1. Generates a session UUID (session_id)
2. Records a timestamp via internal RTC or by requesting time from the host via a side channel
3. Generates a power session attestation record comprising:
   - `artifact_type`: POWER_SESSION
   - `device_id`: hardware serial number from the HSE
   - `session_id`: UUID for this power session
   - `challenge_hash`: hash of session parameters
   - `signature`: ECDSA signature from the HSE over the session parameters
   - `signed_at`: timestamp
4. Transmits the attestation record via a side channel to the evidence management system

**3.3 Session Identifier**

The session_id is shared with a concurrent ZKKey signing session (PAT-001) via an out-of-band mechanism, enabling the two attestation records to be bound into a CombinedSession entry in the hash-chained ledger (PAT-007). This creates a single chain entry proving both (a) a device was powered without data exchange and (b) a human-gated signing event occurred within the same custody session.

### 4. Passive Variant

In the simplest embodiment, the PowerVerify device is entirely passive: VBUS and GND conductors only, no electronics whatsoever. This variant:
- Has no firmware and no attack surface via software
- Has no power consumption
- Has no failure mode attributable to software
- Is continuity-testable as described above
- Can be manufactured at minimal cost

The passive variant does not generate an attestation record but provides a physical continuity-testable proof of data conductor absence that may be combined with procedural documentation, photographic evidence, and witness attestation in lieu of an electronic attestation record.

### 5. PCB Design Notes

The PCB is designed to maximize visual inspectability of the absence of data conductors. In a preferred embodiment:
- D+ and D- PCB pads on both connectors are present as physical pads but have no copper traces connecting them
- A silkscreen label marks the unpopulated data pads
- The VBUS and GND traces are clearly routed between upstream and downstream connectors

This design enables visual PCB inspection as an additional verification method beyond electrical continuity testing.

### 6. Applications

**6.1 Election Integrity**

A PowerVerify device may be inserted between a power supply and a ballot tabulation machine to attest that the machine received power without any data connection to external devices. The power session attestation record is timestamped and signed by the device's hardware secure element, creating a cryptographic record of the power event that does not depend on witness testimony.

**6.2 Forensic Device Charging**

A PowerVerify device may be used to charge a mobile device or computer seized for forensic examination, with the power session attestation record demonstrating that no data was extracted from or written to the device during charging.

**6.3 Pharmaceutical Supply Chain**

A PowerVerify device may attest that a storage unit (e.g., a refrigerated medication transport container) was powered during transit without any data connection to external networks, demonstrating that the temperature log was not tampered with via a connected device.

---

## CLAIMS

**Claim 1.** An inline USB device comprising:
a first USB connector configured for connection to a USB power source;
a second USB connector configured for connection to a USB-powered device;
a VBUS conductor electrically connecting a VBUS pin of the first USB connector to a VBUS pin of the second USB connector; and
a GND conductor electrically connecting a GND pin of the first USB connector to a GND pin of the second USB connector;
wherein the inline USB device does not comprise a D+ conductor connecting any D+ pin of the first USB connector to any D+ pin of the second USB connector; and
wherein the inline USB device does not comprise a D- conductor connecting any D- pin of the first USB connector to any D- pin of the second USB connector;
whereby data transfer between the USB power source and the USB-powered device through the inline USB device is physically impossible.

**Claim 2.** The inline USB device of claim 1, wherein the absence of the D+ conductor and the D- conductor is verifiable by electrical continuity testing of the inline USB device using a standard electrical continuity testing instrument.

**Claim 3.** The inline USB device of claim 1, further comprising:
a hardware secure element storing a device private key; and
a microcontroller configured to generate a power session attestation record upon detection of VBUS power delivery, the power session attestation record comprising a device identifier, a session identifier, a timestamp, and a digital signature generated by the hardware secure element.

**Claim 4.** The inline USB device of claim 3, wherein the power session attestation record is configured to be recorded in an append-only hash-chained ledger.

**Claim 5.** The inline USB device of claim 3, wherein the session identifier is configured to be shared with an attestation record generated by a user-actuated cryptographic attestation device such that the two attestation records may be bound into a combined custody record.

**Claim 6.** The inline USB device of claim 1, wherein the inline USB device comprises no programmable logic, firmware, or active electronic components, consisting solely of passive conductors.

**Claim 7.** The inline USB device of claim 1, wherein the first USB connector is a USB-C receptacle and the second USB connector is selected from the group consisting of USB-A, USB-C, and USB Micro-B plugs.

**Claim 8.** A method for attesting the absence of data transfer between a USB power source and a USB-powered device comprising:
inserting an inline USB device between the USB power source and the USB-powered device, wherein the inline USB device provides VBUS and GND connectivity and does not provide D+ or D- data conductor connectivity;
supplying electrical power from the USB power source to the USB-powered device through the inline USB device; and
generating a power session attestation record comprising a timestamp and a device identifier certifying that power was supplied through the inline USB device during a defined time period;
wherein any party may independently verify the absence of data conductor connectivity in the inline USB device using standard electrical continuity testing equipment.

**Claim 9.** The method of claim 8, further comprising recording the power session attestation record in an append-only hash-chained ledger.

**Claim 10.** The method of claim 8, further comprising verifying the absence of data conductor connectivity by performing continuity testing on the D+ and D- pins of the inline USB device.

**Claim 11.** The method of claim 8, wherein the power session attestation record is signed by a hardware secure element within the inline USB device using a device private key stored in tamper-resistant hardware.

**Claim 12.** A system for hardware-attested evidence custody comprising:
an inline USB power delivery device comprising VBUS and GND conductors and physically absent D+ and D- conductors, the inline USB device configured to generate a power session attestation record;
a user-actuated cryptographic signing device configured to generate a signing attestation record only upon physical actuation of a hardware input element by a user who has viewed the challenge hash on an integrated display; and
an append-only hash-chained ledger configured to record a combined custody entry comprising both the power session attestation record and the signing attestation record, the combined entry establishing that a device was powered without data exchange and that a human approved a specific evidence hash during the same custody session.

**Claim 13.** The system of claim 12, wherein the power session attestation record and the signing attestation record share a session identifier, and wherein the combined custody entry is associated with the session identifier.

**Claim 14.** The system of claim 12, wherein the combined custody entry is publicly verifiable via a human-readable short code without requiring account credentials or access to the inline USB device or the signing device.

**Claim 15.** An inline USB device for forensic power delivery comprising:
a housing;
a first connector on the housing configured for upstream USB connection;
a second connector on the housing configured for downstream USB connection;
a first conductor within the housing providing VBUS continuity between the first connector and the second connector;
a second conductor within the housing providing GND continuity between the first connector and the second connector;
wherein no conductor within the housing provides D+ continuity between the first connector and the second connector; and
wherein no conductor within the housing provides D- continuity between the first connector and the second connector;
whereby a standard electrical continuity testing instrument applied to D+ pins of the first connector and the second connector produces no continuity indication, and applied to D- pins of the first connector and the second connector produces no continuity indication.

**Claim 16.** The inline USB device of claim 15, wherein PCB land patterns for D+ and D- pins are present on a printed circuit board within the device but are not connected by copper traces.

---

## ABSTRACT

An inline USB device for forensic power delivery in which the D+ and D- data signaling conductors are physically absent. The device provides VBUS and GND continuity between upstream and downstream USB connectors, enabling electrical power delivery while making data transfer between connected devices physically impossible by construction. The absence of data conductors is independently verifiable by any party using a standard electrical continuity testing instrument, without requiring firmware access, software, or expert knowledge. In an enhanced embodiment, the device includes a hardware secure element that generates a cryptographically signed power session attestation record upon power delivery, enabling the data-transfer-free power event to be recorded in a hardware-attested chain-of-custody ledger. The power session attestation record may be combined with a human-gated signing attestation record into a single combined custody entry that proves both physical data-transfer impossibility and human-authorized evidence attestation within a single custody event.

---

## IDS — Prior Art to Disclose

1. US12111961 — Secure data extraction from computing devices using unidirectional communication, 2024
2. US6813682 — Forensic disk controller (Menz & Bress), 2004
3. USB Implementers Forum, USB 2.0 Specification, 2000
4. USB Implementers Forum, USB Type-C Specification, 2014
5. Tableau (OpenText), hardware write-blocker product documentation
6. WiebeTech (CRU-DataPort), hardware write-blocker product documentation

---

*DRAFT — For attorney review. Not yet filed. Priority date: January 15, 2026.*
*Inventor: William Shane Wilkinson | ZKNOT, Inc. | ops@zknot.io*
