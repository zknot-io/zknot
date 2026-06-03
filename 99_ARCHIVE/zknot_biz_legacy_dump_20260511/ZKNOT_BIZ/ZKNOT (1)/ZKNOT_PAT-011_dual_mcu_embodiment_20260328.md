# PAT-011 DualSE — Additional Embodiment: Dual MCU Architecture
## For inclusion in PAT-011 Non-Provisional Specification
## Drafted: March 28, 2026

---

## ADDITIONAL EMBODIMENT: DUAL MICROCONTROLLER ARCHITECTURE WITH PHYSICALLY SEPARATED PROCESSING DOMAINS

### Overview

The primary embodiment of the invention employs two physically distinct secure elements managed by a single host microcontroller acting as a domain router. While this architecture provides hardware-level key separation between identity and signing domains, the single host microcontroller represents a shared processing substrate: firmware running on one processor has physical access to both I2C buses and could theoretically be exploited to misroute requests between domains.

The present embodiment eliminates this residual shared-substrate vulnerability by providing a dedicated microcontroller for each secure element, creating two fully independent processing domains with no shared firmware, no shared bus, and no shared execution context.

### Architecture Description

**MCU1 — Identity Domain Controller**

MCU1 is dedicated exclusively to device identity operations. It has:
- One I2C interface connected exclusively to the Identity SE (SE1)
- No electrical connection to the Signing SE (SE2)
- No I2C bus segment shared with MCU2
- Firmware containing only identity domain code: certificate operations, device identity assertion, nonce signing for device presence verification
- No event record format definitions in firmware
- No button GPIO input
- One unidirectional output interface to MCU2 (described below)
- One external USB or UART interface for identity assertion output to host systems

MCU1 physically cannot route a signing request to SE2 because MCU1 has no electrical path to SE2 and no firmware code path for event signing. This is not a software policy — it is a hardware constraint enforced by PCB routing.

**MCU2 — Signing Domain Controller**

MCU2 is dedicated exclusively to human-gated event signing operations. It has:
- One I2C interface connected exclusively to the Signing SE (SE2)
- No electrical connection to the Identity SE (SE1)
- No I2C bus segment shared with MCU1
- Firmware containing only signing domain code: challenge receipt, hash display, button gate enforcement, ECDSA signing, monotonic counter management, attestation artifact assembly
- No CA certificate, no device identity key reference, no identity assertion code
- Button GPIO connected directly to MCU2 and to SE2 authorization input — not connected to MCU1
- One unidirectional output interface to MCU1 (described below)
- One external USB or UART interface for signed artifact output to host systems

MCU2 physically cannot produce identity attestations because MCU2 has no electrical path to SE1 and no CA certificate or identity key in its firmware. This is a hardware constraint, not a software policy.

**Unidirectional Inter-MCU Communication Channel**

MCU1 and MCU2 communicate through a narrow, unidirectional channel designed to pass only the minimum data required to assemble a combined attestation record, without creating a path for domain cross-contamination.

In a preferred embodiment, the inter-MCU channel is a unidirectional UART:
- MCU2 UART TX → MCU1 UART RX
- No return path: MCU1 has no UART TX line to MCU2
- MCU1 cannot transmit to MCU2; MCU2 cannot receive from MCU1

The channel carries only:
- `session_id`: UUID for the current custody session
- `signing_artifact_hash`: SHA-256 hash of the signed artifact produced by MCU2/SE2
- `signing_timestamp`: timestamp of the signing event
- `monotonic_counter`: current counter value from SE2

MCU1 receives these fields and incorporates them into the combined attestation record alongside the identity assertion from SE1. MCU1 never learns the signing private key, the full event record content, or any other signing domain data. MCU2 never learns the identity private key, the CA certificate, or any identity domain data.

The unidirectional nature of the channel means MCU1 cannot send commands to MCU2. MCU2 initiates transmission only after a successful button-gated signing event. MCU1 cannot trigger or simulate a signing event by transmitting on the channel because no such path exists.

**This unidirectional inter-MCU channel is itself a distinct patentable element:** a hardware-enforced one-way data path between processing domains that passes only cross-reference hashes, preventing either domain from learning the operational details of the other while enabling assembly of a combined attestation record.

### PCB Layout Considerations

The dual-MCU architecture has specific PCB layout requirements that reinforce the domain separation:

- SE1 and MCU1 are placed in one physical quadrant of the PCB
- SE2 and MCU2 are placed in a separate physical quadrant
- No shared I2C traces cross between quadrants
- The button GPIO trace routes exclusively to MCU2 and SE2, with no branch to MCU1
- The inter-MCU UART trace is the only electrical connection crossing between quadrants
- A ground plane segment between quadrants reduces electromagnetic coupling
- Independent power domain filter networks for each MCU/SE pair reduce shared-power-rail attack surface

### Security Properties of Dual-MCU Architecture

**Property 1: Firmware Compromise Isolation**
In the single-MCU design, a firmware exploit on the host processor potentially gives an attacker control over both I2C buses. In the dual-MCU design, a firmware exploit on MCU2 gives an attacker control over only the signing domain — SE1 is physically unreachable from MCU2's bus. A firmware exploit on MCU1 gives control over only the identity domain — SE2 is physically unreachable from MCU1's bus. Neither compromise alone produces a complete forgery.

**Property 2: Button GPIO Isolation**
In the single-MCU design, the button GPIO connects to the host MCU, which could theoretically assert it programmatically (though hardware design mitigates this). In the dual-MCU design, the button GPIO connects to MCU2 only — MCU1 has no electrical access to the button line and cannot observe or influence button state. MCU1 cannot simulate or suppress a button press.

**Property 3: Signing Cannot Be Triggered Remotely**
Because MCU1 has no transmit path to MCU2, an attacker who compromises MCU1 (the identity domain) cannot send commands to MCU2 to trigger signing. The signing domain is triggered only by: (a) a host system request arriving on MCU2's external interface, followed by (b) physical button actuation. Neither step can be satisfied by MCU1.

**Property 4: Combined Record Integrity Without Shared Trust**
The combined attestation record is assembled by MCU1, which receives only the cross-reference hash from MCU2. MCU1 wraps this with the identity assertion from SE1 to produce the final record. Neither MCU has the complete combined record in a form it could independently modify — MCU2 never sees the identity assertion, MCU1 never sees the full signing artifact.

**Property 5: Physical Attack Scope**
A physical attack targeting SE1 requires physical access to MCU1's I2C bus. A physical attack targeting SE2 requires physical access to MCU2's I2C bus. These are in separate PCB quadrants. A complete forgery requires simultaneous physical attacks on two separate IC packages in two separate PCB regions — a significantly higher bar than the single-MCU design.

### Combined Attestation Record — Dual MCU Variant

The combined attestation record produced by the dual-MCU architecture contains:

```
Field 1: Identity Assertion (from MCU1 / SE1)
  - device_serial: hardware serial from SE1
  - identity_timestamp: time of identity assertion
  - session_nonce: nonce from verifier
  - identity_signature: ECDSA signature from SE1 over above fields
  - identity_cert: CA-signed certificate for SE1 public key

Field 2: Signing Cross-Reference (received by MCU1 from MCU2 via unidirectional UART)
  - session_id: shared UUID
  - signing_artifact_hash: SHA-256 of the full signing artifact
  - signing_timestamp: time of signing event
  - monotonic_counter: SE2 counter value at signing

Field 3: Combined Record Hash (computed by MCU1)
  - SHA-256(Field 1 fields || Field 2 fields)
  - Signed by SE1 over the combined hash
  - Proves both fields were assembled by the identity domain in the same session

Field 4: Full Signing Artifact (from MCU2 / SE2, transmitted separately)
  - challenge_hash: SHA-256 of the evidence data signed
  - event_record: structured event data
  - signing_signature: ECDSA signature from SE2
  - monotonic_counter: matches Field 2
  - session_id: matches Field 2
```

A verifier independently verifies:
1. Field 1 identity signature against SE1 public key (via CA chain from identity_cert)
2. Field 4 signing signature against SE2 public key (registered in device record)
3. Field 3 combined hash against the received Field 1 and Field 2 values
4. signing_artifact_hash in Field 2 matches SHA-256 of Field 4
5. session_id matches between Field 2 and Field 4
6. monotonic_counter matches between Field 2 and Field 4

A forger must compromise both SE1 and SE2 to produce a record that passes all six verifications. Compromising only MCU2's firmware allows forging Field 4 but not Fields 1 or 3. Compromising only MCU1's firmware allows altering Field 3 assembly but not Field 4 (which was signed by SE2 before transmission).

### Claim Language for Dual-MCU Embodiment

**Additional Apparatus Claim:**
"The apparatus of claim [8], further comprising a second microcontroller dedicated exclusively to device identity operations, wherein: a first microcontroller is coupled exclusively to the signing secure element via a first I2C bus and has no electrical connection to the identity secure element; the second microcontroller is coupled exclusively to the identity secure element via a second I2C bus and has no electrical connection to the signing secure element; and the first and second microcontrollers communicate via a unidirectional channel over which the second microcontroller can receive data from the first microcontroller but cannot transmit data to the first microcontroller."

**Additional Method Claim:**
"The method of claim [1], wherein routing identity requests to the identity secure element and routing signing requests to the signing secure element is enforced by physical PCB routing rather than software configuration, such that the dedicated host processor for each secure element has no electrical path to the secure element of the other domain."

**Unidirectional Channel Claim:**
"The apparatus of any preceding claim, wherein the first microcontroller and second microcontroller are coupled by a unidirectional serial interface over which the signing domain microcontroller transmits cross-reference data to the identity domain microcontroller following a successful signing event, and over which the identity domain microcontroller cannot transmit data to the signing domain microcontroller."

### Comparison: Single MCU vs. Dual MCU Embodiments

| Property | Single MCU (Primary Embodiment) | Dual MCU (This Embodiment) |
|---|---|---|
| Domain separation | Software-enforced routing on shared MCU | Hardware-enforced by separate MCUs |
| Button GPIO access | MCU has access to button line | Only signing MCU has button access |
| Firmware compromise scope | Full device (both buses accessible) | Single domain only |
| Inter-domain channel | Shared I2C bus with software multiplexing | Unidirectional UART (signing → identity only) |
| Cost/complexity | Lower | Higher (~$4–6 BOM addition) |
| Attack bar for complete forgery | Compromise single MCU firmware + two SE packages | Compromise two MCU firmwares + two SE packages |
| Recommended tier | ZKM-001 Basic, ZKM-002 Pro | ZKM-003 Ultra |

---

## INTEGRATION NOTES FOR PAT-011 NON-PROVISIONAL

Insert this section after Section 4 (Security Analysis) in the existing spec as "Section 5: Alternative Embodiment — Dual Microcontroller Architecture." Renumber existing Section 5 (Claims) to Section 6.

Add the three claim language blocks above as dependent claims following the existing exemplary claims. The unidirectional channel claim is the most novel element and should be drafted broadly — it applies to any dual-domain cryptographic device where domain outputs are passed one-way for record assembly without creating a reverse command channel.

**Attorney note:** The unidirectional inter-MCU channel is worth a dedicated independent claim in the non-provisional. It is architecturally elegant, clearly novel, and applicable beyond this specific device — any multi-domain cryptographic system that needs to assemble combined records without domain cross-contamination could use this pattern. Draft it broadly: "a unidirectional communication channel between a first processing domain and a second processing domain, wherein the channel carries attestation cross-reference data from the second domain to the first domain for combined record assembly, and wherein the channel does not provide a command path from the first domain to the second domain."

---

*Drafted March 28, 2026 | William Shane Wilkinson | ZKNOT, Inc.*
*For inclusion in PAT-011 DualSE non-provisional specification*
