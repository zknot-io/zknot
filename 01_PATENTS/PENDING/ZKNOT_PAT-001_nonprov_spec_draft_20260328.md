# PATENT APPLICATION DRAFT
## PAT-001: User-Actuated Cryptographic Attestation Device
### Non-Provisional Patent Application — Pro Se Draft for Attorney Review
### Priority: US Provisional App. No. 63/960,933 (Filed January 15, 2026)

---

## TITLE OF INVENTION

**USER-ACTUATED CRYPTOGRAPHIC ATTESTATION DEVICE WITH POST-NONCE PHYSICAL ENFORCEMENT**

---

## CROSS-REFERENCE TO RELATED APPLICATIONS

This application claims priority to and the benefit of U.S. Provisional Patent Application No. 63/960,933, filed January 15, 2026, entitled "ZKey — User-Actuated Cryptographic Attestation Device," the contents of which are incorporated herein by reference in their entirety.

This application is related to co-pending applications [PAT-002, PAT-004, PAT-007, PAT-008, PAT-009, PAT-010] filed by the same inventor.

---

## STATEMENT REGARDING FEDERALLY SPONSORED RESEARCH

Not applicable.

---

## BACKGROUND OF THE INVENTION

### Field of the Invention

The present invention relates to cryptographic signing devices, and more particularly to hardware signing devices that enforce physical human actuation as a prerequisite to digital signature generation, where the user views and approves the specific content to be signed before the signing operation occurs.

### Description of Related Art

Digital signatures using hardware security modules (HSMs) and hardware token devices are widely deployed in authentication and transaction authorization systems. Existing hardware token systems, including FIDO2-compliant security keys, provide user presence verification through capacitive touch sensors that confirm a human is physically present when a signing operation occurs. However, such systems suffer from a fundamental limitation: the signing operation is initiated and controlled by software running on the host system, and user presence confirmation (touch) occurs independently of the content being signed.

This architecture creates a critical gap in evidence attestation contexts: a user touching a hardware token confirms that a human hand was present at a computer, but does not confirm that the human reviewed and specifically approved the content of the signing challenge. Moreover, in compromised host environments, software may generate and submit challenges to the hardware token without the user's knowledge, and the touch confirmation merely indicates physical proximity to the device at an arbitrary moment in time.

Existing hardware signing devices also lack a mechanism for displaying the cryptographic hash of the specific challenge to the user before signing occurs. The result is that a user pressing a hardware token button cannot confirm that the document, evidence record, or transaction they intended to sign is in fact what the hardware signed. This is particularly problematic in forensic evidence attestation, where the signed artifact may later be examined in legal proceedings.

Furthermore, existing solutions rely on software-initiated signing sequences, meaning that an attacker with control of the host software can forge or alter the challenge before it reaches the hardware device, or trigger a signing operation remotely without any physical human interaction.

What is needed is a hardware attestation device that enforces the following sequence as a physical constraint rather than a software policy: (1) a challenge is received and its cryptographic hash is displayed to the user; (2) the user physically actuates a dedicated hardware input element specifically to confirm the displayed hash; and (3) the hardware secure element signs the challenge only upon completion of step (2), with the hardware being physically incapable of signing absent that actuation.

---

## SUMMARY OF THE INVENTION

The present invention provides a user-actuated cryptographic attestation device and methods of operation that enforce post-nonce physical human confirmation as a prerequisite to digital signature generation. The device comprises a hardware secure element for key storage and signature generation, an integrated display for presenting a cryptographic challenge hash to the user, and a dedicated physical actuation element whose actuation gates the signing operation.

In one aspect, the invention provides a method comprising: receiving a cryptographic challenge; displaying a hash of the challenge on an integrated display; detecting physical actuation of a dedicated hardware input element; and generating a digital signature only upon detection of said actuation, wherein the hardware secure element is physically incapable of generating the signature absent the physical actuation.

In another aspect, the invention provides an apparatus comprising: a housing; a hardware secure element within the housing storing a device private key; an integrated display on the housing for displaying cryptographic hashes; a dedicated physical input element on the housing; and a microcontroller executing a state machine that transitions through defined states and generates a signature request to the hardware secure element only when the physical input element has been actuated after the hash has been displayed.

In a further aspect, the invention provides a system for evidence attestation comprising the apparatus described above, an append-only hash-chained ledger, and a public verification service accessible without account or credential requirements.

---

## BRIEF DESCRIPTION OF DRAWINGS

**FIG. 1** is a perspective view of the user-actuated cryptographic attestation device according to an embodiment of the invention.

**FIG. 2** is a block diagram of the internal components of the device, showing the hardware secure element, microcontroller, display, and physical input element.

**FIG. 3** is a state machine diagram showing the operational states of the device: IDLE, ARMED, DISPLAY, AWAITING_ACTUATION, SIGNING, and OUTPUT.

**FIG. 4** is a flowchart of the signing method enforced by the device state machine.

**FIG. 5** is a diagram of the attestation artifact produced by the device, showing fields including signature, device identifier, challenge hash, timestamp, and human-readable short code.

**FIG. 6** is a system diagram showing the device operating in an evidence attestation workflow with a hash-chained ledger and public verification service.

**FIG. 7** is a diagram of the ZKKey Air variant using optical challenge ingestion via QR code camera.

---

## DETAILED DESCRIPTION OF THE INVENTION

### 1. Overview

The user-actuated cryptographic attestation device (hereinafter "the Device") of the present invention enforces a physical constraint on digital signature generation: a hardware secure element within the Device cannot generate a signature until a user has (a) viewed the cryptographic hash of the challenge to be signed on an integrated display and (b) physically actuated a dedicated hardware input element in response to viewing that hash.

This enforcement is structural rather than behavioral. The Device's microcontroller executes a finite state machine (FSM) that does not issue a signing command to the hardware secure element until the FSM has transitioned through the DISPLAY state (wherein the hash is shown) and has subsequently detected an actuation event from the dedicated physical input element. There is no software pathway, network interface, or protocol command that causes the hardware secure element to sign without this sequence having been completed.

### 2. Hardware Architecture

**2.1 Housing**

The Device is housed in a compact, tamper-evident enclosure sized for handheld operation. In a preferred embodiment, the housing is approximately 60mm × 30mm × 12mm and is constructed of a rigid polymer or metal alloy.

**2.2 Hardware Secure Element (HSE)**

The Device comprises a hardware secure element (HSE) for cryptographic key storage and signature generation. In a preferred embodiment, the HSE is an ATECC608B-class device from Microchip Technology Inc., operating on the I2C interface. The HSE stores the device's private key in a tamper-resistant hardware zone from which the key cannot be extracted by software. The HSE generates ECDSA signatures using the P-256 elliptic curve (NIST P-256) upon receiving a signing command from the microcontroller.

A critical feature of the Device's architecture is that the HSE receives signing commands only from the microcontroller, and the microcontroller issues signing commands only when the FSM is in the SIGNING state, which can only be reached after the sequence described in Section 4 below.

**2.3 Microcontroller**

The Device comprises a microcontroller (MCU) for device orchestration and FSM execution. In a preferred embodiment, the MCU is an STM32F103-class or STM32F411-class device from STMicroelectronics. The MCU interfaces with the HSE via I2C, with the display via SPI or I2C, and with the physical input element via a GPIO input pin. The MCU does not store signing keys and cannot sign independently of the HSE.

**2.4 Integrated Display**

The Device comprises an integrated visual display for presenting information to the user. In a preferred embodiment, the display is a 128×64 pixel OLED display (SSD1306 or compatible controller). The display is integral to the device housing such that the user can view the display while interacting with the device.

The display presents the cryptographic hash of the challenge to the user in human-readable hexadecimal format. In a preferred embodiment, the display shows at minimum the first 16 hexadecimal characters of the SHA-256 challenge hash, with scrolling or pagination for the full 64-character representation.

**2.5 Physical Input Element**

The Device comprises a dedicated physical input element whose actuation gates the signing operation. In a preferred embodiment, the physical input element is a tactile push-button switch (PTS645SM43-2 LFS or compatible) with a minimum actuation force of 2.0N. The button is positioned on the device housing such that it is clearly associated with the display and distinct from any USB interface connectors.

The button is electrically connected to a GPIO input pin of the MCU configured with an internal pull-up resistor. Button actuation creates a measurable electrical event detectable by the MCU.

**2.6 Communication Interface**

The Device communicates with the host system via a USB interface in a preferred embodiment. The USB interface is used to receive challenge data from the host and to transmit the signed attestation artifact to the host. In the ZKKey Air variant (described in Section 7), no electrical interface to the host is used; challenge ingestion occurs via optical scanning of a QR code.

### 3. Software Architecture

**3.1 Firmware**

The Device's MCU executes firmware implementing the FSM described in Section 4. The firmware is loaded at manufacture and stored in non-volatile flash memory. The firmware does not accept over-the-air updates via the USB interface during normal operation.

**3.2 Challenge Processing**

Upon receiving a challenge via the communication interface, the firmware:
- Validates the challenge format
- Computes the SHA-256 hash of the challenge
- Stores the challenge and hash in volatile MCU memory for the duration of the signing session
- Transitions the FSM to the DISPLAY state

**3.3 Attestation Artifact**

Upon successful completion of the signing sequence, the firmware generates an attestation artifact comprising:
- `artifact_id`: UUID for unique identification
- `artifact_type`: enumerated type (ZKEY_SIGN in the primary embodiment)
- `device_id`: hardware serial number burned into the HSE during manufacture
- `session_id`: optional UUID linking this artifact to a concurrent power attestation (PAT-007)
- `challenge_hash`: SHA-256 hash of the challenge signed
- `signature`: ECDSA signature generated by the HSE
- `public_key`: device public key for independent signature verification
- `signed_at`: timestamp in ISO 8601 / RFC 3339 format
- `short_code`: human-readable code derived deterministically from the signature (described in co-pending PAT-010)
- `metadata`: optional structured field for case identifier, operator, and location

The attestation artifact is serialized in JSON format for transmission to the host and subsequent recording in the append-only hash-chained ledger (PAT-004).

### 4. State Machine — The Core Enforcement Mechanism

The critical inventive contribution of the Device is the FSM that enforces post-nonce physical actuation as a hardware constraint. The FSM operates as follows:

**State IDLE:** The device awaits a challenge. No signing operations are possible. The display may show device status or be inactive.

**State ARMED:** A valid challenge has been received and validated. The challenge hash has been computed. The device transitions from IDLE to ARMED upon challenge receipt.

**State DISPLAY:** The MCU drives the display to show the SHA-256 hash of the received challenge. The device transitions from ARMED to DISPLAY automatically. The device remains in DISPLAY until button actuation is detected.

**State AWAITING_ACTUATION:** (In some embodiments, DISPLAY and AWAITING_ACTUATION are combined.) The device monitors the physical input element GPIO pin for an actuation event while displaying the hash.

**State SIGNING:** Triggered exclusively by detection of button actuation while in the DISPLAY state. The MCU issues a signing command to the HSE, passing the challenge hash. The HSE generates the ECDSA signature. The device cannot enter SIGNING from any state other than DISPLAY/AWAITING_ACTUATION via button actuation. No software command, network packet, USB command, or timeout can cause the device to enter the SIGNING state.

**State OUTPUT:** The signed attestation artifact is assembled and transmitted to the host. The device transitions from SIGNING to OUTPUT, then returns to IDLE.

**State TIMEOUT/ERROR:** If a configurable timeout elapses in the DISPLAY state without actuation, the device clears the challenge from memory and returns to IDLE. This prevents a pre-loaded challenge from being signed at an arbitrary future time.

The physical impossibility of signing without button actuation derives from the architecture: the MCU code that issues the HSE signing command is only reachable via the SIGNING state, which is only reachable via the button actuation transition from DISPLAY. There is no code path, interrupt handler, or exception handler that sends a signing command to the HSE outside of this sequence.

### 5. Security Properties

**5.1 Post-Nonce Enforcement**

The Device enforces what is herein termed "post-nonce enforcement": the challenge (nonce) is received BEFORE the user is consulted, and the user's physical actuation is the gate that allows signing to proceed. This is distinct from:

- Pre-authentication systems (user authenticates before receiving any challenge)
- Concurrent presence systems (YubiKey-class: touch confirms presence at signing time but does not confirm challenge content)
- Software-gated systems (software prompts user, but the hardware signs regardless of user response)

**5.2 Remote Attack Resistance**

Because the signing operation requires physical button actuation, a remote attacker who has compromised the host system cannot cause the Device to sign. The attacker can deliver a challenge to the Device, but the Device will display the challenge hash and wait for physical human actuation. If the human does not actuate (because the challenge displayed is not what they expected to sign), the signing does not occur.

**5.3 Impersonation Resistance**

The device private key is stored in the HSE hardware zone and cannot be extracted by software. A clone of the device's software or firmware cannot sign with the device's private key. Physical possession of the device is required.

**5.4 Informed Consent**

By displaying the challenge hash before signing, the Device enables the user to verify that the hash they are approving matches the hash of the document or evidence they intended to sign. A user who signs document X can verify that the hash displayed matches the known hash of document X before actuating the button.

### 6. Evidence Attestation Workflow

In a preferred embodiment for evidence attestation applications, the Device operates as follows:

1. An evidence collection system hashes the evidence data to produce an evidence hash.
2. The evidence hash is sent to the Device as the challenge.
3. The Device displays the evidence hash on its integrated display.
4. The evidence collector views the displayed hash and confirms it matches the hash of the evidence they intend to attest.
5. The evidence collector actuates the physical button.
6. The Device generates a signed attestation artifact.
7. The attestation artifact is recorded in an append-only hash-chained ledger (PAT-004).
8. A human-readable short code derived from the signature is generated and associated with the chain entry (PAT-010).
9. The short code may be printed, transmitted, or affixed to the evidence for subsequent public verification at a verification service (no account required).

### 7. ZKKey Air Variant — Optical Challenge Ingestion

In an alternative embodiment termed "ZKKey Air," the Device operates without any electrical data connection to the host system. The Device is fully air-gapped.

Challenge ingestion occurs via an integrated QR code camera. The host system displays a QR code encoding the challenge. The Device scans the QR code, decodes the challenge, computes and displays the hash, and operates the FSM as described above.

The signed attestation artifact is presented by the Device as a QR code on its display, which the host system scans to receive the artifact. No data is exchanged via electrical connector.

This embodiment is covered separately in co-pending provisional application PAT-009 (OpticalChallenge) but is disclosed here as an embodiment of the present invention.

### 8. System Integration

The Device is designed to operate within a broader hardware attestation system comprising:

- The Device (this invention)
- A PowerVerify inline power attestation device (co-pending PAT-002)
- An append-only hash-chained ledger (co-pending PAT-004)
- A combined session attestation mechanism binding the above (co-pending PAT-007)
- A public verification service at which any party may verify an attestation artifact using a short code

In this system, the Device provides the human-gated signing component: proof that a specific human approved a specific content hash at a specific time using a specific hardware device whose private key is bound to a known public key.

### 9. Manufacturing and Provisioning

During manufacturing, the HSE is provisioned with a device-unique private key pair generated and stored in the HSE hardware zone. The corresponding public key is recorded in a device registry and published to enable independent signature verification. The device serial number is burned into the HSE configuration zone.

Firmware is flashed to the MCU at manufacture and write-protected to prevent post-manufacture modification via the USB interface.

---

## CLAIMS

### Independent Claims

**Claim 1.** A method for hardware-attested evidence signing comprising:
receiving, by a hardware attestation device, a cryptographic challenge comprising evidence data or a hash thereof;
computing, by the hardware attestation device, a cryptographic hash of the cryptographic challenge;
displaying, on an integrated visual output of the hardware attestation device, a representation of the computed cryptographic hash;
detecting, by the hardware attestation device, a physical actuation of a dedicated hardware input element of the hardware attestation device subsequent to the displaying;
generating, by a hardware secure element of the hardware attestation device, a digital signature of the cryptographic challenge upon and only upon detection of the physical actuation; and
producing an attestation artifact comprising the digital signature, a device identifier, and a timestamp;
wherein the hardware secure element does not generate the digital signature absent detection of the physical actuation.

**Claim 8.** A hardware attestation apparatus comprising:
a housing;
a hardware secure element within the housing, the hardware secure element storing a device private key in tamper-resistant hardware and configured to generate digital signatures using the device private key;
an integrated visual display on or accessible from the housing, the integrated visual display configured to display a cryptographic hash of a challenge received by the apparatus;
a dedicated physical input element on the housing; and
a microcontroller within the housing executing a finite state machine, the finite state machine configured to issue a signing command to the hardware secure element only upon detection of an actuation event from the dedicated physical input element while the integrated visual display is displaying the cryptographic hash of the challenge;
wherein the hardware secure element generates a digital signature of the challenge upon receipt of the signing command from the microcontroller.

**Claim 15.** A system for evidence custody attestation comprising:
a hardware attestation device comprising a hardware secure element, an integrated display, and a dedicated physical input element, the hardware attestation device configured to generate a digital signature of a challenge only upon physical actuation of the dedicated physical input element while the integrated display shows a cryptographic hash of the challenge;
an append-only hash-chained ledger configured to record attestation artifacts produced by the hardware attestation device; and
a public verification service configured to resolve a human-readable code to a corresponding attestation artifact without requiring account credentials.

### Dependent Claims

**Claim 2.** The method of claim 1, wherein the hardware secure element is an ATECC608B-class device operating on a two-wire serial interface.

**Claim 3.** The method of claim 1, wherein the cryptographic hash is computed using the SHA-256 algorithm.

**Claim 4.** The method of claim 1, wherein the integrated visual output is an OLED display integrated into the housing of the hardware attestation device.

**Claim 5.** The method of claim 1, further comprising: recording the attestation artifact in an append-only hash-chained ledger, wherein each entry in the ledger comprises a hash of the entry and a hash of a preceding entry.

**Claim 6.** The method of claim 5, further comprising: generating a human-readable short code derived deterministically from the digital signature, wherein the short code is associated with the attestation artifact in the ledger and is usable to retrieve the attestation artifact from a public verification service.

**Claim 7.** The method of claim 1, wherein the cryptographic challenge is received via an optically scanned two-dimensional barcode displayed by a host system, and wherein no electrical data connection between the hardware attestation device and the host system is required.

**Claim 9.** The apparatus of claim 8, wherein the finite state machine operates in at least the following states: an IDLE state awaiting challenge receipt; an ARMED state after challenge receipt and before hash display; a DISPLAY state wherein the integrated visual display shows the cryptographic hash; a SIGNING state reachable only via detection of the actuation event from the DISPLAY state; and an OUTPUT state wherein the attestation artifact is transmitted.

**Claim 10.** The apparatus of claim 8, wherein the dedicated physical input element is a tactile push-button switch requiring a minimum actuation force.

**Claim 11.** The apparatus of claim 8, wherein the microcontroller does not store the device private key and cannot generate digital signatures independently of the hardware secure element.

**Claim 12.** The apparatus of claim 8, wherein the finite state machine includes a timeout state that clears the challenge from memory and returns to the IDLE state if no actuation event is detected within a configurable duration.

**Claim 13.** The apparatus of claim 8, further comprising a USB interface configured to receive the challenge from a host system and to transmit the attestation artifact to the host system.

**Claim 14.** The apparatus of claim 8, further comprising an optical scanning element configured to decode a two-dimensional barcode encoding the challenge, wherein no electrical data interface to a host system is required.

**Claim 16.** The system of claim 15, wherein the append-only hash-chained ledger operates without network connectivity, such that attestation artifacts are recorded offline and the ledger is independently verifiable by any party having access to an exported version of the ledger.

**Claim 17.** The system of claim 15, further comprising a power attestation device configured to generate a power attestation record indicating that a device was electrically powered without any data transfer, wherein the power attestation record and an attestation artifact from the hardware attestation device share a session identifier, and wherein the append-only hash-chained ledger records a combined entry comprising both the power attestation record and the attestation artifact.

**Claim 18.** The method of claim 1, wherein the attestation artifact further comprises a session identifier shared with a power attestation record generated by a hardware power verification device, the power verification device being configured to supply electrical power to a device under test without transmitting data to or receiving data from the device under test.

**Claim 19.** The apparatus of claim 8, wherein the device identifier is a hardware serial number stored in a configuration zone of the hardware secure element during manufacture and is not modifiable by firmware.

**Claim 20.** The system of claim 15, wherein the public verification service is accessible via a domain name resolving the human-readable code directly to an attestation record display without requiring login, account creation, or communication with the hardware attestation device.

---

## ABSTRACT

A user-actuated cryptographic attestation device enforces post-nonce physical human confirmation as a hardware constraint on digital signature generation. The device comprises a hardware secure element for key storage and signing, an integrated display for presenting cryptographic challenge hashes to the user, and a dedicated physical input element whose actuation is a prerequisite for the hardware secure element to generate a signature. A finite state machine in the device's microcontroller ensures that the signing command is issued to the hardware secure element only when the actuation event is detected while the challenge hash is displayed. This architecture makes it physically impossible for software, network commands, or automated processes to trigger a signing operation without a human viewing and physically confirming the specific challenge hash. Attestation artifacts produced by the device, comprising the signature, device identifier, and timestamp, are recorded in an append-only hash-chained ledger and are publicly verifiable via a human-readable short code.

---

## INFORMATION DISCLOSURE STATEMENT (IDS) — Prior Art to Disclose

The following references are known to the inventor and are being disclosed pursuant to 37 CFR 1.56:

1. US9509686B2 — Microsoft Corporation, "Secure element authentication," issued 2016
2. DE10059066A1 — "Device for digitally signing information," published 2002
3. US11057215B2 — Oracle International, "Automated hash validation," issued 2021
4. FIDO Alliance, "FIDO2 WebAuthn Standard," public specification, various versions 2018–2025
5. FIDO Alliance, "FIDO U2F Security Key Specification," public specification, 2014
6. Yubico Inc., YubiKey product documentation and technical specifications, 2008–2025
7. Microchip Technology Inc., ATECC608B Datasheet and Application Notes, 2019–2025
8. US4529870A — DigiCash/Chaum, "Cryptographic identification, financial transaction, and credential device," issued 1985
9. Solana Foundation, "Durable Nonces," technical documentation, 2022
10. Fromm et al., "Chronological independently verifiable electronic chain of custody ledger using blockchain technology," ScienceDirect, 2020

---

*DRAFT — For attorney review. Not yet filed. Priority date: January 15, 2026.*
*Inventor: William Shane Wilkinson | ZKNOT, Inc. | ops@zknot.io*
