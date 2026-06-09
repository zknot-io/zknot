---
title: ZKKey Software & Firmware Capability Requirements
doc_id: SIG-REQ-ZKKEY-001
status: DRAFT for hardware-selection input
author: William Shane Wilkinson (ZKNOT, INC.)
date: 2026-06-08
scope: Capability requirements ONLY. Hardware selection deliberately out of scope.
sources_of_truth:
  - PAT-001 ZKKey provisional (App 63/960,933) + Supplemental "Attestation Communication Interfaces"
  - PAT-004 ZK-LocalChain (App 63/961,098)
  - PAT-005 VendorAttest (App 63/964,169)
  - PAT-007 CombinedSession (App 63/995,728)
  - PAT-008 FirmwareFSM (App 63/995,736)
  - PAT-009 OpticalChallenge (App 63/995,740)
  - PAT-010 HumanReadableAttest (App 63/995,747)
  - PAT-011 DualSE (App 64/007,907)
  - PAT-018 PowerVerifyPlus (App 64/007,940)
classification: ZKNOT INTERNAL — patent-sensitive (see Part VI)
---

# ZKKey Software & Firmware Capability Requirements

## 0. Purpose and how to read this

This document answers two questions, and **only** these two:

1. **Core ceremony** — What must a ZKKey be able to do to *receive a challenge and relay a signature*? (Part I + Part II)
2. **Forward compatibility** — What must we *build into the architecture now* so future ZKKey versions don't require a redesign? (Part III)

It then collapses all of that into a **chip-agnostic capability checklist** (Part IV) you take into hardware selection, the **decisions to resolve before you buy silicon** (Part V), and the **patent-sensitivity / sequencing flags** (Part VI).

This document does **not** name chips, MCUs, secure-element part numbers, or boards. The filed patents list examples (e.g. "RP2040 or equivalent," "ATECC608A or equivalent," "STM32 or equivalent") — those are illustrative in the filings and are intentionally excluded here so the requirement set stays clean and the hardware choice stays yours.

**Requirement IDs**
- `C-##` — Core ceremony requirement
- `R-##` — Canonical record-format requirement
- `F-##` — Forward-compatibility (build-in-now) requirement
- `CAP-##` — Abstract hardware capability the chosen parts must satisfy

**Force of words** — MUST = required for a conforming ZKKey; SHOULD = strongly recommended, omit only with a recorded reason; MAY = optional / version-dependent.

**Naming note** — The filed spec text calls the device "ZKey." The product/taxonomy term is **ZKKey** (device-id prefixes `ZK-K` Connect / `ZK-A` Air). This document uses ZKKey for the product and treats the two as the same invention.

---

## 1. Canonical terms (glossary)

| Term | Meaning in this document |
|------|--------------------------|
| **Challenge** | The value the host wants signed: a nonce, hash, or structured event record. Arrives from outside the device. |
| **Actuation** | A deliberate physical human interaction (press-and-release, sustained touch) that gates signing. |
| **Armed** | State where a valid challenge is held and the device is waiting for actuation. |
| **Attestation artifact / signed record** | The structured output: signature + identity + counter + metadata. The unit a third party verifies. |
| **Short code** | A deterministic, human-readable code derived from the artifact (e.g. `A3F7-K2M9-PX4R` or a word sequence). |
| **Single-use consumption** | Once a challenge is signed it cannot be signed again; replay of a prior challenge is rejected. |
| **Post-nonce ordering** | The actuation must occur *after* the challenge is received. This is temporal ordering, not extra entropy. |
| **Transport** | The physical channel a challenge arrives on / an artifact leaves on (electrical, optical, etc.). The crypto is transport-independent. |
| **Identity assertion** | A signed claim "this specific device is present," provable against a CA. Distinct from an event signature. |
| **Event signature** | A human-gated signature over event data. Distinct from identity assertion. |

---

## Part I — Core ceremony: receive a challenge, relay a signature

The spine is the firmware state machine (PAT-008). Everything in Part I hangs off it. The lifecycle is:

```
IDLE → CHALLENGE_RECEIVED → ARMED → SIGNING → OUTPUT → IDLE
  └─────────────────────────── ERROR ──────────────────┘
```

### 1.1 The lifecycle (PAT-008)

| State | What happens | Exit |
|-------|--------------|------|
| **IDLE** | Powered, no challenge held. Signing requests rejected. Actuations ignored. | Valid challenge → CHALLENGE_RECEIVED; bad challenge → ERROR |
| **CHALLENGE_RECEIVED** | Challenge validated for format/canonical correctness, stored in buffer. | Immediately → ARMED |
| **ARMED** | Holds challenge; monitors actuation input; presents readiness (and, future, the hash to confirm). | Actuation → SIGNING; timeout/cancel → IDLE; second challenge → ERROR |
| **SIGNING** | Signing element signs the held challenge. Transient. | Success → OUTPUT; SE failure/timeout → ERROR |
| **OUTPUT** | Artifact assembled and emitted. Challenge buffer invalidated, counter incremented. | → IDLE |
| **ERROR** | Bad challenge / rejected actuation / SE fault. Buffers cleared. | → IDLE |

Any transition not listed above MUST be rejected.

### 1.2 Core requirements

| ID | Requirement | Force | Source |
|----|-------------|-------|--------|
| **C-01** | The device MUST accept a challenge from outside itself over at least one input transport. | MUST | PAT-001 §4,6 |
| **C-02** | The device MUST validate the challenge (length bounds, format/canonical check) **before** arming; a failing challenge MUST route to ERROR and never arm. | MUST | PAT-008 §4.4; PAT-001 §7 |
| **C-03** | The device MUST hold exactly one validated challenge in a buffer while armed. A second challenge arriving while ARMED MUST clear the pending challenge and go to ERROR. | MUST | PAT-008 §4.2 |
| **C-04** | The device MUST present a human-perceptible readiness indication when ARMED. | MUST | PAT-008 §4.1 |
| **C-05** | The device MUST require a deliberate physical actuation to sign. The actuation MUST be debounced and distinguishable from electrical transients/noise. | MUST | PAT-001 §5; PAT-008 §4.5 |
| **C-06** | The actuation MUST occur **after** challenge receipt (post-nonce ordering). One actuation MUST permit **at most one** signing operation. | MUST | PAT-001 §5,6; PAT-008 §4.2 |
| **C-07** | Actuations received in IDLE or CHALLENGE_RECEIVED MUST be ignored (no effect). | MUST | PAT-008 §4.2 |
| **C-08** | Signing MUST be performed inside a secure element using a private key that is generated on-device, never exported, and never exposed to the host or main processor. | MUST | PAT-001 §4; PAT-011 §1.2 |
| **C-09** | A monotonic counter MUST increment on each transition into OUTPUT and MUST be included in the artifact. | MUST | PAT-008 §4.6; PAT-001 Supplemental |
| **C-10** | On entering OUTPUT the device MUST invalidate/consume the signed challenge. The device SHOULD retain a rolling log of recently consumed challenges and reject any incoming challenge matching a consumed value (replay rejection). | MUST / SHOULD | PAT-008 §4.3; PAT-009 §4.2 |
| **C-11** | The device MUST return to a safe IDLE state after every OUTPUT and every ERROR, clearing all challenge buffers. | MUST | PAT-008 §4.1,4.2 |
| **C-12** | ARMED MUST support a configurable timeout and an explicit cancel, both returning to IDLE without signing. | MUST | PAT-008 §4.2 |
| **C-13** | The device MUST emit the artifact over at least one output transport. | MUST | PAT-001 §6, Supplemental |
| **C-14** | Signing element failure, secure-element comms failure, or timeout MUST surface as ERROR, not as a silent or partial signature. | MUST | PAT-008 §4.2 |

### 1.3 What "minimum viable" needs, in plain terms

To do *just* C-01…C-14, a ZKKey needs, as **capabilities** (not parts):

- A **processing element** that runs the FSM, does canonical validation, drives the transport(s), manages the counter and the consumed-challenge log, and talks to the signing element.
- A **secure signing element** that: generates a keypair on-device, never exports the key, signs internally, and exposes a **hardware monotonic counter**.
- A **human-actuation input** with debounce + deliberate-press detection.
- A **readiness indicator** (at minimum, a single status light).
- **At least one I/O channel** for challenge-in and artifact-out.
- **Non-volatile storage** for the consumed-challenge log and the device's own identity/cert.

That is the floor. Part III is about not painting yourself into it.

---

## Part II — The canonical signed-record format (the keystone)

This is the single most leveraged decision in the whole program. If the **output is a structured, versioned, crypto-agile record** instead of a bare signature, then *every* future version becomes "populate another field" rather than "redesign the device." Almost all of Part III depends on Part II being right on day one.

### 2.1 Record-format requirements

| ID | Requirement | Force | Why it matters / unlocks |
|----|-------------|-------|--------------------------|
| **R-01** | The signed output MUST be a structured record, not a bare signature blob. | MUST | Precondition for everything below |
| **R-02** | The record MUST include a `record_version`. | MUST | Lets verifiers handle format evolution |
| **R-03** | The record MUST include an `algorithm_id` naming the signature scheme. | MUST | Post-quantum / curve migration without breaking old verifiers (PAT-006 §9.3, §11.1) |
| **R-04** | The record MUST include a `device_serial` / device public-key reference. | MUST | Device identity, auditability (PAT-001 §8) |
| **R-05** | The record MUST include the `event_hash` (the value actually signed). | MUST | The substance of the attestation |
| **R-06** | The record MUST include the `monotonic_counter`. | MUST | Anti-replay/backdating; distinct codes for identical data (PAT-008 §4.6; PAT-010 §4.2) |
| **R-07** | The record SHOULD include a `timestamp`. | SHOULD | "Optional timestamp" in PAT-001 §6 |
| **R-08** | The record MUST include a `session_id` field (may be empty in standalone use). | MUST | Combined power+presence sessions (PAT-007 §4.1; PAT-018 §4.4.1) |
| **R-09** | The record MUST include a `prior_record_hash` field (may be null for first record). | MUST | ZK-LocalChain compatibility; on-device hash chaining (PAT-004 §4; PAT-018 §4.4.2) |
| **R-10** | The record format MUST be able to carry **two distinct signature components** — an identity assertion and an event signature — plus a cross-reference linking them. | MUST | Single-SE today, dual-SE Ultra later, *same record shape* (PAT-011 §1.5) |
| **R-11** | The record SHOULD reserve a `firmware_hash` field. | SHOULD | Firmware-integrity attestation (PAT-018 §4.4.1) |
| **R-12** | The record MUST be deterministically reducible to a short human-readable code. | MUST | Transcription/verbal verification (PAT-010) |

### 2.2 Reference shape (illustrative field set, not wire format)

```
{
  record_version,            # R-02
  algorithm_id,              # R-03
  device_serial,             # R-04
  identity_assertion {       # R-10  (Field 1 — may be signed by same SE on v1)
     device_serial, timestamp, nonce, signature
  },
  event_signature {          # R-10  (Field 2 — the human-gated signature)
     event_hash,             # R-05
     session_id,             # R-08
     monotonic_counter,      # R-06
     timestamp,              # R-07
     prior_record_hash,      # R-09
     firmware_hash,          # R-11
     signature
  },
  cross_reference_hash       # R-10  (Field 3 — binds Field 1 & Field 2 to one session)
}
```

> On a single-secure-element v1, Field 1 and Field 2 are both produced by the one SE and Field 3 is computed by the processor. On a dual-SE Ultra, Field 1 comes from the Identity SE and Field 2 from the Signing SE. **The verifier sees the same record either way** — that is the whole point of R-10.

---

## Part III — Forward compatibility: what to build in now

Five architectural principles carry all the known future versions. Build these, and the future is feature-flags and hardware swaps, not rewrites.

### 3.1 The five principles

| ID | Principle | Build-in-now requirement | Force |
|----|-----------|--------------------------|-------|
| **F-01** | **Transport abstraction** | The FSM core MUST consume *validated challenge bytes* and emit *artifact bytes* through an internal interface that is agnostic to how they arrived/leave. Each physical channel is a swappable adapter. | MUST |
| **F-02** | **Structured, versioned, crypto-agile record** | Implement the Part II record format in full now, including the fields that v1 leaves empty. | MUST |
| **F-03** | **Role separation in firmware** | Treat *identity assertion* and *event signing* as separate logical roles / separate key slots even on a single SE, with a domain router that forbids one role from doing the other's work. | MUST |
| **F-04** | **FSM extension hooks** | The FSM MUST expose a "present challenge representation" hook in ARMED (for display-then-confirm and short-code display) and keep timeout/cancel + genesis-attestation as first-class transitions. | MUST |
| **F-05** | **Reserved headroom** | Reserve, in the architecture (not necessarily populated in v1): an optical input path, a display-capable output path, ledger storage, and firmware-hash measurement. | SHOULD |

### 3.2 Future versions mapped to build-in-now requirements

| Future version / capability | Source | What must already be true in the architecture |
|------------------------------|--------|-----------------------------------------------|
| **ZKKey Air** — optical, air-gapped challenge in / QR out, no electrical data path | PAT-009 | F-01 transport abstraction; an *optical-in* adapter (image capture + 2D-code decode) and an *optical-out* adapter (render a 2D code) can be added without touching the FSM core. **F-06**: challenge ingestion MUST NOT assume an electrical data channel. |
| **Display-then-confirm** (Tier-2 moat) — show the hash/short code, human confirms what they're signing | PAT-001 Supplemental; FSM hook | F-04 present-representation hook; a display-capable output path (F-05). **F-07**: ARMED MUST be able to present a representation of the held challenge before accepting actuation. *See Part VI — patent-sensitive.* |
| **Human-readable short code / word encoding** | PAT-010 | R-12 + the derivation function in firmware (truncate hash → ambiguity-free charset → group format; optional dictionary-word variant). **F-08**: derivation MAY fold in `monotonic_counter` so identical data yields distinct codes. |
| **Combined power+presence session** (bind to PowerVerify under one session) | PAT-007; PAT-018 §4.7 | R-08 `session_id` present from day one. **F-09**: the device MUST be able to accept an externally supplied `session_id` *or* derive one from the challenge, and embed it in the event signature. |
| **Dual-SE "Ultra"** — Identity SE + Signing SE, bidirectional separation | PAT-011 | F-03 role separation; R-10 two-component record. **F-10**: the human-actuation gate SHOULD be wired so the Signing role's authorization depends on a physical line, not a pure software assertion (see Part V tradeoff). Moving identity to a second SE later becomes a hardware swap, not a protocol change. |
| **Vendor-irrevocable manufacturing ledger** | PAT-005 | **F-11**: the SE MUST be able to emit a **genesis self-signature at key generation** (proves on-device key origin). **F-12**: reserve non-volatile storage for a device-resident, hash-chained ledger and the ability to append customer-receipt + lifecycle entries. |
| **ZK-LocalChain event output** | PAT-004 | R-09 `prior_record_hash` present; the device's record is already a valid chain event. |
| **Firmware-integrity attestation** | PAT-018 §4.4.1 | R-11 reserved field + ability to measure/report a firmware hash (F-05). |
| **Post-quantum / curve migration** | PAT-006 §9.3, §11.1 | R-03 `algorithm_id` + a signing abstraction so the scheme/SE can change without changing the record contract. |

---

## Part IV — Chip-agnostic capability checklist (take this to hardware selection)

Each item is a **capability the chosen parts must satisfy**, phrased without naming any part. Use this as the column headers when you evaluate silicon.

### Signing element
- **CAP-01** On-device keypair generation; private key non-extractable; signing performed internally. *(C-08)*
- **CAP-02** Hardware **monotonic counter** readable/incrementable per signing. *(C-09, R-06)*
- **CAP-03** Ability to produce a **genesis self-signature** at provisioning. *(F-11)*
- **CAP-04** Support for **at least two independent key slots / roles** (identity vs signing) with per-slot usage restriction. *(F-03, R-10)*
- **CAP-05** A **hardware authorization input** to the signing operation that the main processor cannot assert in software. *(F-10 — decision in Part V)*
- **CAP-06** Signature scheme is **not hard-wired into the record contract** (algorithm-agility at the system level). *(R-03)*

### Processing element
- **CAP-07** Runs the full FSM with strict transition rejection. *(Part I)*
- **CAP-08** Performs canonical challenge validation. *(C-02)*
- **CAP-09** Drives a **transport-abstracted** challenge-in / artifact-out interface. *(F-01)*
- **CAP-10** Maintains the consumed-challenge log and replay rejection. *(C-10)*
- **CAP-11** Computes the short-code derivation and the cross-reference hash. *(R-12, R-10)*
- **CAP-12** Can measure/report a firmware hash. *(R-11, F-05)*

### Human interface
- **CAP-13** A debounced deliberate-actuation input distinguishable from transients. *(C-05)*
- **CAP-14** A readiness indicator (floor: status light). *(C-04)*
- **CAP-15** *Reserved:* a display capable of rendering a legible hash/short code and a 2D code. *(F-05, F-07)*

### I/O transports
- **CAP-16** At least one challenge-in + artifact-out channel. *(C-01, C-13)*
- **CAP-17** *Reserved:* an **optical-in** capability (image capture + 2D-code decode) with no electrical data path. *(F-06)*
- **CAP-18** *Reserved:* an **optical-out** capability (render 2D code). *(PAT-009)*

### Storage
- **CAP-19** Non-volatile storage for device identity/cert + consumed-challenge log. *(C-08, C-10)*
- **CAP-20** *Reserved:* headroom for a device-resident hash-chained ledger. *(F-12)*

### Time / entropy
- **CAP-21** A monotonic ordering source (the counter is the floor; a real clock is the upgrade). *(C-09, R-07)*
- **CAP-22** Entropy source sufficient for any locally generated nonces/session-ids. *(F-09)*

---

## Part V — Decisions to resolve before you buy silicon (both sides shown)

These are genuine forks. I'm giving you the tension on each, not a verdict.

**D-1 · Single secure element vs dual secure element (now or later)**
- *Single SE:* cheaper, simpler firmware, fewer bus/isolation headaches; one compromise = full forgery. Fine for Connect/standard.
- *Dual SE:* compromise of one SE yields only half a forgery (identity *or* signing, not both); this is a *claimed* differentiator (PAT-011) and the Ultra story. Costs board area, a second bus/select, and firmware domain-routing.
- *Bridge:* if you build R-10 + F-03 now, you can ship single-SE v1 and move to dual-SE later **without changing the record or the verifier.** That's the cheap option that doesn't foreclose the expensive one.

**D-2 · Hardware-enforced human gate vs software-detected button**
- *Software-detected:* processor reads the button, includes its state in signed data. Simple. But a compromised processor can lie about the press.
- *Hardware-enforced (SE authorization line):* the actuation physically gates the SE; software cannot simulate it (PAT-011 §3.2 step 3 / §4.3). Materially stronger and aligned with the human-presence claim that is the entire point of the device.
- *Tension:* the hardware gate constrains which signing elements qualify (CAP-05). Decide D-2 before D-1, because it filters the SE shortlist.

**D-3 · LED-only vs display, in v1**
- *LED-only:* cheapest, smallest, and — importantly — keeps the display-then-confirm step *out* of the build entirely (patent-safe for free/Tier-1 builds; see Part VI). Matches the SelfKnot Tier-1 profile.
- *Display:* unlocks display-then-confirm (the moat) and short-code UX (PAT-010), but is the patent-sensitive surface and adds cost/power/firmware.
- *Bridge:* F-04/F-05 let you ship LED-only now and add the display path later. Reserve the hook; don't populate it in free builds.

**D-4 · Stateful replay log vs stateless device**
- *Stateful (consumed-challenge log):* real replay rejection on-device (C-10 SHOULD), needs durable storage and a wear story.
- *Stateless:* simpler, but leans entirely on host-supplied freshness + the monotonic counter for anti-replay.
- *Tension:* the counter (CAP-02) gives you backdating/duplication detection for free; the on-device log is the upgrade for true single-use enforcement without trusting the host.

**D-5 · Carry the manufacturing ledger on-device vs reference it externally**
- *On-device ledger (PAT-005):* strongest vendor-irrevocability and the federal-procurement story; needs CAP-20 storage + genesis self-sign (CAP-03).
- *External reference:* lighter device, but weaker "customer holds the proof" guarantee.
- *Tension:* this is more about the federal narrative than the core ceremony — you can defer it, but reserving CAP-20 + CAP-03 now keeps it cheap to add.

---

## Part VI — Patent-sensitivity and sequencing flags

These are flags, not blockers — but they affect what goes into *public* and *free* builds.

- **Display-then-confirm (F-07) and the dual-SE separation (PAT-011) are the moat.** The "display the hash → human confirms → sign" ceremony (PAT-001 + supplemental) must **not** appear in free builds or public-facing content (including video narration / DIY guides) before the non-provisional filing. Documenting it in *this internal engineering spec* is fine; exposing it publicly early is the risk.
- **Sequencing anchors on file:** non-provisional conversions are due **2027-03-01** for the January-filed core (PAT-001 = App 63/960,933, 12-month deadline **2027-01-15**). Public-exposure gating for the display-then-confirm feature should track the attorney-engagement and filing targets, not the hardware schedule.
- **Tiering:** the LED-only, button-gated, no-display profile (D-3 LED-only) is the part of this requirement set that is *safe to open*. The display + dual-SE features are the part to hold proprietary.
- **Federal-filing caution:** if any of this terminology flows into a capability statement, proposal, or government-facing artifact, re-verify names and application numbers against USPTO Patent Center primary records before use — do not propagate from this doc or chat.

---

## Part VII — Open items for you to decide

1. **D-2 first, then D-1** — pick the human-gate model (hardware-enforced vs software-detected); it filters the secure-element shortlist before anything else.
2. **Lock the Part II record format** — this is the keystone; once you and I agree the field set, the rest of the build is mechanical. Tell me if you want session_id/firmware_hash mandatory vs reserved.
3. **v1 personality** — LED-only Tier-1-style, or display-bearing Tier-2 from the start? (Affects D-3 and Part VI exposure.)
4. **Ledger now or later** — reserve CAP-20/CAP-03 only, or implement the on-device manufacturing ledger in v1?

When you've made these calls, the next document is the **v1 conformance subset** — the exact MUST list a first build has to hit — which then maps one-to-one onto candidate hardware.

---

*Provenance: every requirement in this document traces to a filed ZKNOT provisional listed in the front-matter. No capability here is invented beyond those claims. Hardware part numbers from the filings are intentionally excluded per the scope of this exercise.*
