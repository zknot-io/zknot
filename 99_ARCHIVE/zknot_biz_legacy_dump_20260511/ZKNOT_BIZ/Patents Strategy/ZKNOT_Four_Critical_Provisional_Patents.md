# ZKNOT.IO — Four Critical Gap Provisional Patent Applications
**Inventor:** William Wilkinson | ops@zknot.io | March 2026

> File each of these as a separate provisional patent application with the USPTO.
> USPTO micro-entity fee: ~$320 per filing if you qualify (small business, under 3 prior patent applications).
> These are written in provisional style — broad, descriptive, no formal claims required.
> Have a patent attorney review GAP 4 (Combined Session Record) before filing if at all possible.

---
---

# PROVISIONAL PATENT APPLICATION 1 OF 4

**Title:** Optical Challenge Ingestion for Human-Gated Cryptographic Attestation Devices

**Inventor:** William Wilkinson

**Related Applications:** This application is related to prior provisional application titled "User-Actuated Cryptographic Attestation Device for Physically Verified Digital Events" filed by the same inventor.

---

## 1. Technical Field

This invention relates to cryptographic attestation devices, secure elements, and air-gapped digital evidence systems. More specifically, it relates to a hardware attestation device that receives a cryptographic challenge by optically reading a machine-readable visual code displayed on an external host device, without any electrical data connection between the host and the attestation device.

---

## 2. Background

Human-gated cryptographic attestation devices receive a challenge or nonce from a host system, sign that challenge using a hardware-protected private key only upon physical human actuation, and return a verifiable signature as proof that a human authorized a specific digital event at a specific time.

Existing implementations of such devices receive the challenge over an electrical data interface such as USB. While effective, electrical interfaces create a data path between the host system and the attestation device. In certain high-security, forensic, or adversarial contexts, any electrical data path between the host and the signing device is undesirable, as it creates a potential vector for host-side influence, data injection, or covert communication.

There exists a need for a human-gated cryptographic attestation device that can receive a challenge from a host without any electrical data connection — specifically by optically reading a machine-readable code displayed on the host screen.

---

## 3. Summary of the Invention

The invention is a hardware attestation device that receives a cryptographic challenge by optically scanning a machine-readable visual code displayed on an external host device. The device signs the received challenge only upon physical human actuation, using a hardware-protected private key stored in a secure element. No electrical data connection between the host and the attestation device is required or used during the challenge ingestion process.

The device comprises at minimum:
- An optical sensor or camera module capable of capturing and decoding machine-readable visual codes
- A microcontroller for processing the decoded challenge
- A secure element storing a hardware-protected private key
- A physical user-actuated control
- An output interface for presenting the resulting attestation artifact

---

## 4. Detailed Description

### 4.1 Challenge Ingestion via Optical Scanning

In the invention, a host system generates a cryptographic challenge or nonce and encodes it as a machine-readable visual code. The visual code may be a two-dimensional barcode, a QR code, a Data Matrix code, an Aztec code, or any other optically decodable format. The host displays this visual code on a screen, printed medium, or any other visible surface.

The attestation device is equipped with an optical sensor or camera module directed toward the displayed visual code. The device captures an image or video stream of the visual code and decodes it to extract the underlying challenge or nonce data.

The decoded challenge is passed to the microcontroller for validation. In some embodiments, the microcontroller verifies that the challenge conforms to an expected format, length, or canonical structure before proceeding. Challenges that do not conform may be rejected without entering the armed state.

### 4.2 Single-Use Challenge Consumption

In some embodiments, each challenge received via optical ingestion is treated as a single-use value. Once a challenge has been received and the device has entered an armed state, the same challenge value cannot be used to produce a second signature. This prevents replay attacks in which a prior challenge is re-displayed and re-scanned.

In some embodiments, the device maintains a record of recently consumed challenge values and rejects any challenge matching a previously consumed value.

### 4.3 Air-Gap Preservation

Because the challenge is received optically rather than electrically, no data path exists between the host system and the attestation device during challenge ingestion. The host cannot inject data, issue commands, or influence the signing process through any electrical means. The optical channel is inherently unidirectional from host to device — the host cannot receive data from the device through the optical ingestion channel.

This air-gap property provides a verifiable guarantee that the host system did not influence or participate in the signing operation beyond displaying the challenge.

### 4.4 Physical Human Actuation Requirement

After the challenge is received and validated, the device enters an armed state. The device will not produce a cryptographic signature until a human physically actuates a control on the device. The control may be a mechanical button, capacitive touch sensor, pressure sensor, or any physical mechanism requiring deliberate human interaction.

Each physical actuation permits at most one signing operation. The actuation must occur after the challenge has been received. This ensures that the resulting signature is contemporaneous with a deliberate human decision.

### 4.5 Secure Element Signing

Upon physical actuation, the microcontroller instructs the secure element to sign the challenge. The secure element stores the device's private key internally and performs the signing operation internally. The private key is never exposed to the microcontroller or any external interface.

The resulting signature, combined with the device's public key or identifier and optionally a monotonic counter value, constitutes the attestation artifact.

### 4.6 Output of Attestation Artifact

The attestation artifact may be output through one or more interfaces including:
- An electrical data interface (USB or equivalent) to a host system
- A visual display showing the full or truncated attestation artifact
- A visual display encoding the attestation artifact as a machine-readable visual code for capture by a second optical device
- Any combination of the above

In embodiments where the output is also optical, the device operates in a fully air-gapped mode — challenge received optically, signature output optically, with no electrical data connection to any host at any stage.

### 4.7 Example Embodiment

In one embodiment, a journalist in the field uses an attestation device equipped with a front-facing camera. The journalist's smartphone displays a QR code encoding a cryptographic challenge generated by an evidence collection application. The journalist points the attestation device's camera at the QR code. The device decodes the challenge, enters an armed state, and displays a confirmation prompt. The journalist presses the physical button. The secure element signs the challenge. The device displays the attestation artifact as a QR code on its OLED screen. The journalist's smartphone captures the QR code using its camera, completing a fully air-gapped attestation exchange.

---

## 5. Variations

The invention covers any hardware attestation device that:
- Receives a cryptographic challenge by optically reading a machine-readable visual code
- Signs the challenge using a hardware-protected private key
- Requires physical human actuation before signing
- Without requiring an electrical data connection to the challenge source

Optical sensor types, visual code formats, secure element models, microcontroller types, and output methods may vary without departing from the invention.

---

## 6. Diagram

```
[Host Screen: QR Challenge] 
         ↓ (optical, no electrical connection)
[Camera Module] → [MCU: Decode + Validate] → [Armed State]
                                                    ↑
                                             [Physical Button]
                                                    ↓
                                        [Secure Element: Sign]
                                                    ↓
                                    [Output: Display / QR / USB]
```

---
---

# PROVISIONAL PATENT APPLICATION 2 OF 4

**Title:** Human-Readable Short Attestation Code Derived from Cryptographic Signatures for Hardware Attestation Devices

**Inventor:** William Wilkinson

**Related Applications:** This application is related to prior provisional applications titled "User-Actuated Cryptographic Attestation Device for Physically Verified Digital Events" and the supplemental specification "Attestation Communication Interfaces — Transport-Agnostic Attestation Output" filed by the same inventor.

---

## 1. Technical Field

This invention relates to cryptographic attestation devices, human-computer interaction, and evidence verification systems. More specifically, it relates to methods and systems for generating a short, human-readable or human-transmittable attestation code derived from a full cryptographic signature or attestation artifact, enabling verification by observers who cannot process or transmit full cryptographic data.

---

## 2. Background

Cryptographic attestation devices produce digital signatures as proof that a human authorized a specific digital event. Full cryptographic signatures — typically 64 bytes or longer — are not practical for human reading, manual transcription, verbal communication, or visual comparison by non-technical users.

In many real-world evidence contexts — journalism, election observation, legal proceedings, field investigations — the person using the attestation device is not a cryptographer. They may need to:
- Read an attestation code aloud to a colleague
- Write it on a physical evidence log
- Verbally confirm it matches a previously recorded value
- Photograph it as part of a paper record

There exists a need for a method of deriving a short, human-usable attestation code from a full cryptographic signature while preserving sufficient entropy to serve as a practically unique identifier for the attestation event, and while allowing the full signature to be independently verified by a technical party.

---

## 3. Summary of the Invention

The invention is a method and system for generating a short attestation code from a full cryptographic attestation artifact. The short code is derived deterministically from the full artifact so that it is unique to that specific attestation event, human-readable, and sufficient for practical verification purposes. The full cryptographic artifact is preserved and may be independently verified by any party with access to the device's public key.

---

## 4. Detailed Description

### 4.1 Short Code Generation

After a cryptographic attestation artifact is generated — comprising at minimum a digital signature and a device identifier — the device applies a deterministic derivation function to produce a short attestation code.

The derivation may include one or more of the following steps:
- Applying a cryptographic hash function to the full attestation artifact
- Selecting a subset of bytes from the hash output
- Encoding the selected bytes in a human-friendly character set (alphanumeric, excluding visually ambiguous characters such as O/0, I/l/1)
- Optionally formatting the result with separators for readability (e.g., groups of 4 characters: XXXX-XXXX-XXXX)

The resulting short code is typically 6 to 16 characters in length, balancing uniqueness against human usability. The character set and length may be configurable.

### 4.2 Entropy and Collision Resistance

The short code is not a replacement for the full cryptographic signature. It is a human-scale identifier derived from the full artifact. The short code has sufficient entropy that accidental collision between two distinct attestation events is practically negligible for the expected volume of attestation events per device.

In some embodiments, the short code incorporates a monotonic counter value from the device's secure element, ensuring that even two attestations of identical data by the same device produce distinct short codes.

### 4.3 Display and Presentation

The short code is displayed on the device's output interface — typically an OLED or e-ink display. The display may show:
- The short code in large, readable characters
- A visual separator format for easier transcription
- A phonetic encoding or word-based representation for verbal communication
- A machine-readable encoding (QR code) of the full attestation artifact alongside the short code

### 4.4 Verification Relationship

The short code is deterministically derivable from the full attestation artifact. Any party who subsequently obtains the full artifact may independently derive the expected short code and compare it to the recorded value. A match confirms the recorded short code corresponds to the full artifact.

A mismatch indicates that either the short code was recorded incorrectly, or that the full artifact presented for verification does not correspond to the original attestation event.

### 4.5 Use in Chain-of-Custody Records

In some embodiments, the short code is entered into a physical evidence log, a digital form, or a chain-of-custody system at the time of attestation. The full cryptographic artifact is separately stored or transmitted. The short code serves as a human-scale reference linking the physical record to the cryptographic record.

### 4.6 Example Embodiment

In one embodiment, a field investigator uses an attestation device to sign the hash of a photograph. The device generates a 64-byte cryptographic signature. The device applies a SHA-256 hash to the full attestation artifact, takes the first 8 bytes, and encodes them as a 12-character alphanumeric code formatted as XXXX-XXXX-XXXX. This code is displayed on the OLED screen. The investigator reads the code aloud to a colleague who records it in the paper evidence log. Later, a forensic analyst retrieves the full attestation artifact from the digital system, applies the same derivation, and confirms the short code matches the paper log entry, establishing continuity.

### 4.7 Word-Based Encoding Variant

In some embodiments, the short code is expressed as a sequence of common English words selected from a fixed dictionary (analogous to BIP-39 mnemonic encoding). This form is easier to read aloud, verbally transmit, and remember. For example: "RIVER-TABLE-CLOCK" may encode the same 3-word attestation identifier as a numeric short code.

---

## 5. Variations

The invention covers any system in which:
- A full cryptographic attestation artifact is produced by a hardware attestation device
- A short human-usable code is deterministically derived from that artifact
- The short code is displayed or transmitted to a human operator
- The short code can later be verified against the full artifact

Derivation functions, character sets, lengths, display formats, and encoding schemes may vary without departing from the invention.

---

## 6. Diagram

```
[Secure Element: Full Signature (64+ bytes)]
              ↓
[MCU: Hash → Truncate → Encode → Format]
              ↓
[OLED Display: "A3F7-K2M9-PX4R"]
              ↓
[Human: reads aloud / writes in evidence log]
              ↓
[Later: Full artifact retrieved → same derivation → code matches → verified]
```

---
---

# PROVISIONAL PATENT APPLICATION 3 OF 4

**Title:** Firmware State Machine for Single-Actuation Human-Gated Cryptographic Signing Devices

**Inventor:** William Wilkinson

**Related Applications:** This application is related to prior provisional applications titled "User-Actuated Cryptographic Attestation Device for Physically Verified Digital Events" filed by the same inventor.

---

## 1. Technical Field

This invention relates to firmware architecture, cryptographic signing devices, and secure element integration. More specifically, it relates to a firmware state machine for a hardware cryptographic signing device that enforces single-use challenge consumption, post-challenge actuation requirements, and canonical input validation, preventing automated, replay, or remote signing while guaranteeing that each signature is contemporaneous with a deliberate human physical action.

---

## 2. Background

Human-gated cryptographic signing devices rely on firmware to enforce the physical presence guarantee. The firmware must ensure that:
- Signing is impossible without a challenge having been received
- Signing is impossible without physical human actuation after challenge receipt
- Each challenge can only be signed once regardless of subsequent actuations
- The device returns to a safe idle state after each signing operation

Without a formally enforced state machine, firmware implementations may inadvertently allow corner cases such as signing without a challenge, replaying a prior challenge after an actuation, or producing multiple signatures from a single actuation event. Such vulnerabilities would undermine the physical presence guarantee that is the device's primary security property.

There exists a need for a formally defined firmware state machine that enforces single-actuation human-gated signing with well-defined state transitions and rejection behaviors.

---

## 3. Summary of the Invention

The invention is a firmware state machine for a cryptographic signing device comprising a defined set of states and transitions that enforce: reception of a valid challenge before arming, physical human actuation after challenge receipt, single-use challenge consumption, and return to idle after each signing operation. The state machine provides a formal software architecture that makes the physical presence guarantee resistant to replay, automation, and race conditions.

---

## 4. Detailed Description

### 4.1 States

The firmware state machine comprises at minimum the following states:

**IDLE:** The device is powered but no challenge has been received. No signing is possible in this state. Physical actuations in this state are ignored or produce an error indication. The device actively rejects any signing request received in the IDLE state.

**CHALLENGE_RECEIVED:** A challenge or nonce has been received via an input interface (electrical or optical). The challenge has been validated for format and canonical correctness. The device has not yet been armed for signing. The challenge value is stored in a temporary buffer.

**ARMED:** The device has received a valid challenge and is awaiting physical human actuation. In this state, the device monitors the physical control for an actuation event. The device may display a visual prompt indicating it is ready for actuation.

**SIGNING:** The device has detected a valid physical actuation event while in the ARMED state. The microcontroller instructs the secure element to sign the stored challenge. This state is transient — the device enters and exits this state in a single operation.

**OUTPUT:** The signing operation is complete. The attestation artifact is available for output via the device's output interface(s). The challenge buffer is invalidated. The device presents the output and then transitions to IDLE.

**ERROR:** The device has encountered an invalid challenge, a rejected actuation, a secure element communication failure, or other fault condition. The device rejects the current operation, clears all buffers, and returns to IDLE.

### 4.2 State Transitions

Valid state transitions are:

- IDLE → CHALLENGE_RECEIVED: on receipt of a valid, canonical challenge via input interface
- IDLE → ERROR: on receipt of a malformed, non-canonical, or replay challenge
- CHALLENGE_RECEIVED → ARMED: immediately upon successful challenge validation
- ARMED → SIGNING: on detection of a valid physical actuation event
- ARMED → IDLE: on timeout (if configured) or explicit cancel command
- SIGNING → OUTPUT: on successful completion of secure element signing operation
- SIGNING → ERROR: on secure element failure or timeout
- OUTPUT → IDLE: on completion of output presentation
- ERROR → IDLE: after error display and buffer clearing

Any state transition not listed above is explicitly rejected by the firmware. In particular:
- Actuation events received in IDLE or CHALLENGE_RECEIVED states are ignored
- Signing requests received outside of the SIGNING state are rejected
- A second challenge received while in ARMED state causes transition to ERROR and clears the pending challenge

### 4.3 Single-Use Challenge Enforcement

Upon entering the OUTPUT state, the device invalidates the challenge buffer. The challenge value used in the signing operation is marked as consumed. In some embodiments, the device maintains a rolling log of recently consumed challenge values and rejects any incoming challenge matching a prior consumed value, preventing replay attacks.

### 4.4 Canonical Challenge Validation

Upon receipt of a challenge, the device applies a canonical validation function before transitioning to CHALLENGE_RECEIVED. The canonical validation may include:
- Verifying the challenge is within an expected byte length range
- Verifying the challenge contains no disallowed byte patterns
- Verifying the challenge passes a format check (e.g., is a valid hash, nonce, or structured event record)
- Optionally verifying a challenge timestamp or sequence number if provided

Challenges failing canonical validation cause a transition to ERROR.

### 4.5 Actuation Validity

In some embodiments, a physical actuation is considered valid only if it meets the following conditions:
- The actuation occurs while the state machine is in ARMED state
- The actuation is a complete, deliberate physical interaction (press and release, sustained contact, etc.) rather than an electrical transient or noise event
- The actuation occurs within a configurable timeout period after entering ARMED state

### 4.6 Monotonic Counter Integration

In some embodiments, each transition from SIGNING to OUTPUT increments a monotonic counter stored in the secure element. The counter value is included in the attestation artifact, providing a tamper-evident sequence number that allows auditors to detect if the device was used more times than recorded.

### 4.7 Example Embodiment

In one embodiment, an attestation device powers on and enters IDLE. A host transmits a 32-byte challenge over USB. The firmware validates the challenge format, stores it in the challenge buffer, and transitions to ARMED. The OLED displays "READY — PRESS TO SIGN." The user presses the button. The firmware transitions to SIGNING, calls the secure element signing API, and receives the resulting signature. The firmware transitions to OUTPUT, displays the short attestation code, outputs the full artifact over USB, invalidates the challenge buffer, and returns to IDLE. If the user presses the button again without a new challenge, the device remains in IDLE and no signing occurs.

---

## 5. Variations

The invention covers any firmware state machine for a cryptographic signing device that:
- Requires challenge receipt before arming
- Requires physical human actuation after challenge receipt for signing
- Enforces single-use challenge consumption
- Returns to a safe idle state after each operation
- Rejects actuations received outside the armed state

The number of states, specific transition conditions, timeout durations, canonical validation rules, and output methods may vary without departing from the invention.

---

## 6. Diagram

```
          ┌─────────────────────────────────────────────────────┐
          ↓                                                     │
        IDLE ──[valid challenge]──→ CHALLENGE_RECEIVED ──→ ARMED
          ↑                              │                    │
          │                             │ [invalid]          │ [actuation]
          │                             ↓                    ↓
          │                           ERROR ←────────── SIGNING
          │                             │                    │
          └─────────────────────────────┘                    ↓
                                                           OUTPUT
                                                             │
                                                             └──→ IDLE
```

---
---

# PROVISIONAL PATENT APPLICATION 4 OF 4

**Title:** Cryptographically Bound Combined Power-Session and Human-Presence Attestation Record

**Inventor:** William Wilkinson

**Related Applications:** This application is related to prior provisional applications titled "User-Actuated Cryptographic Attestation Device for Physically Verified Digital Events," "Power-Delivery Interface With Physical Data-Path Elimination and Verified Power-Only Operation," and "Cryptographically Verified Evidence Integrity Protocol for Human-Witnessed Digital and Physical Events" filed by the same inventor.

---

## 1. Technical Field

This invention relates to cryptographic evidence systems, power delivery verification, and chain-of-custody records. More specifically, it relates to a combined attestation record that cryptographically binds, within a single verifiable data structure, a power-session certificate produced by a data-blocking power delivery device and a human-presence signature produced by a human-gated cryptographic signing device, where both records share a common session identifier establishing that the two events occurred in the same operational session.

---

## 2. Background

In forensic, journalistic, legal, and investigative contexts, establishing a complete chain of custody for a digital device or piece of evidence requires demonstrating two independent facts simultaneously:

1. That the device was powered from a clean source with no data communication — proved by a power-only delivery device
2. That a human was physically present and authorized the evidence collection event — proved by a human-gated signing device

Existing systems address these two requirements independently. A power-only USB device may produce a log of power delivery parameters. A cryptographic signing device may produce a signature on an event hash. However, no existing system cryptographically binds these two records into a single verifiable artifact that proves both facts occurred together in the same operational session.

Without this binding, an adversary could potentially substitute a legitimate power-session certificate from one session with a human-presence signature from a different session, undermining the integrity of the combined record.

There exists a need for a combined attestation record that cryptographically proves both clean power delivery and human-authorized signing occurred in the same session, verifiable by any third party without access to either device.

---

## 3. Summary of the Invention

The invention is a combined attestation record comprising a power-session certificate and a human-presence signature that are cryptographically bound to a common session identifier. The power-session certificate is produced by a data-blocking power delivery device. The human-presence signature is produced by a human-gated cryptographic signing device. A session identifier is established prior to or during the session and is incorporated into both records, such that the binding between the two records is verifiable by any party with access to the public keys of both devices.

---

## 4. Detailed Description

### 4.1 Session Identifier

Before or at the beginning of an operational session, a session identifier is established. The session identifier may be:
- A random nonce generated by a host system or evidence collection application
- A hash of the current timestamp, device identifiers, and a random value
- A value derived from the challenge that will be signed by the human-gated device
- Any unique value that both the power delivery device and the signing device can incorporate into their respective records

The session identifier links the power-session certificate and the human-presence signature as records of the same operational session.

### 4.2 Power-Session Certificate

The power delivery device produces a power-session certificate comprising at minimum:
- The session identifier
- The device's unique identifier or public key reference
- Power delivery parameters recorded during the session (voltage, current, duration, or equivalents)
- A cryptographic signature over the above fields produced by the power delivery device's secure element

The power-session certificate constitutes proof that a power delivery session with the recorded parameters occurred, associated with the given session identifier, as attested by the power delivery device.

### 4.3 Human-Presence Signature

The human-gated signing device produces a human-presence signature comprising at minimum:
- The session identifier (or a value from which the session identifier is derivable)
- The device's unique identifier or public key reference
- A cryptographic hash of the event data being attested (e.g., a file hash, evidence record hash, or event description hash)
- A cryptographic signature over the above fields produced by the signing device's secure element, generated only upon physical human actuation

The human-presence signature constitutes proof that a human physically authorized the signing of the identified event data in a session associated with the given session identifier.

### 4.4 Combined Attestation Record

The combined attestation record comprises:
- The power-session certificate
- The human-presence signature
- The session identifier (if not already embedded in both constituent records)
- Optionally, a binding signature or hash over the combined record produced by a host system or third party

Any verifier may independently verify:
- The power-session certificate signature using the power delivery device's public key
- The human-presence signature using the signing device's public key
- That both records reference the same session identifier, establishing they occurred in the same session
- The integrity of the combined record as a whole

### 4.5 Session Identifier Binding Variants

In some embodiments, the session identifier is derived from the challenge that the human-gated signing device will sign. Because the power delivery device incorporates the same challenge value into its certificate, and the signing device signs that same challenge, the two records are bound without requiring a separately generated session identifier.

In other embodiments, the session identifier is generated by the host system before either device begins its operation, and is transmitted to both devices before the session begins.

In further embodiments, the session identifier is derived from a hash of the combined state of both devices at session initiation, incorporating both devices' public keys and a timestamp.

### 4.6 Verification Without Device Access

Once the combined attestation record is produced, it may be verified by any third party with access only to the public keys of the two devices. Neither device needs to be present, connected, or cooperative for verification. The manufacturer of neither device needs to be contacted. The verification is fully offline and self-contained.

### 4.7 Integration with Cryptographic Event Ledger

In some embodiments, the combined attestation record is inserted as a single event into a cryptographically chained event ledger. The ledger event contains both the power-session certificate and the human-presence signature, along with the session identifier and any additional metadata (timestamp, location, operator identifier). The ledger event is signed by the human-gated signing device, establishing that the human authorized the insertion of the complete record.

### 4.8 Example Embodiment

In one embodiment, an election observer prepares to document the state of a voting machine. A host application generates a session identifier. The observer connects the voting machine's power supply through a data-blocking power delivery device. The power delivery device records the session parameters and produces a power-session certificate incorporating the session identifier, signed by its secure element. The host application then generates a challenge incorporating the session identifier and a hash of the observer's field notes. The observer's human-gated signing device receives the challenge, enters an armed state, and the observer presses the button to sign. The signing device produces a human-presence signature incorporating the same session identifier. The host application combines both records into a single combined attestation record. Any subsequent verifier can confirm that the machine was powered from a data-clean source AND that a human observer was present and authorized the documentation event, in the same session, by independently verifying both signatures.

---

## 5. Variations

The invention covers any system in which:
- A power delivery device produces a cryptographically signed record of a power session
- A human-gated signing device produces a cryptographically signed record of human-authorized signing
- Both records incorporate a common session identifier establishing they occurred in the same session
- The combined record is verifiable by any third party without access to either device

Specific session identifier derivation methods, record formats, binding mechanisms, ledger integration methods, and device implementations may vary without departing from the invention.

---

## 6. Diagram

```
[Host: generates SESSION_ID]
         │                    │
         ↓                    ↓
[PowerVerify Device]    [ZKey Device]
[records power params]  [receives challenge]
[signs with SESSION_ID] [armed → human presses button]
[→ Power-Session Cert]  [signs with SESSION_ID]
         │              [→ Human-Presence Sig]
         └──────────────────┘
                  ↓
    [Combined Attestation Record]
    [Power-Session Cert + Human-Presence Sig]
    [Bound by SESSION_ID]
    [Verifiable by any party with both public keys]
                  ↓
    [Optional: inserted into ZK-LocalChain event]
```

---

# Filing Instructions

## What to Do With These Documents

1. **File each as a separate USPTO provisional patent application** at https://www.uspto.gov/patents/apply/patent-center
2. **Select "Provisional Application for Patent"** — no formal claims, no abstract required
3. **Include as the specification** the full text of each application above
4. **Include the diagram section** as a figure (can be ASCII art as shown, or a simple hand-drawn diagram scanned to PDF)
5. **Title each application** exactly as shown at the top of each section
6. **List inventor** as William Wilkinson with your address and contact information
7. **Pay the filing fee** — approximately $320 at micro-entity rate (verify current USPTO fee schedule)

## Priority

File in this order:
1. **Application 4 (Combined Session Record)** — highest commercial value, highest vulnerability
2. **Application 1 (Camera Input)** — ZKKey Air's entire differentiator
3. **Application 3 (Firmware State Machine)** — blocks firmware copy attacks
4. **Application 2 (Short Code)** — important UX protection

## Timeline

All four should be filed within 30 days. The provisional establishes your priority date. You then have 12 months from each filing date to convert to a non-provisional or file a PCT application.

## Cost Estimate

- 4 x ~$320 micro-entity fee = ~$1,280 total USPTO fees if filing yourself
- If using an attorney for Application 4 only: add ~$800–1,200
- Total bootstrapped cost: ~$1,280–2,480

---

*ZKNOT.IO — CONFIDENTIAL — All inventions patent pending — William Wilkinson*
*This document does not constitute legal advice. Consult a registered patent attorney.*
