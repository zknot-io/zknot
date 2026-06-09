# PowerVerify Attested — Cryptographically Signed Power-Only USB-C Interface (Preorder)

**Preorder — $[set price] · In development**

> *Now in development. Reserve below to register interest and lock early pricing. We'll only ask for payment terms once a ship window is confirmed — and we'll tell you exactly where the build stands.*

## Core lets you *see* there's no data path. Attested lets you *prove* it.

PowerVerify Core makes the data lines physically absent — and lets you verify that with your own eyes. PowerVerify **Attested** adds the next thing a forensic, legal, or procurement context needs: a way to prove, to someone who wasn't in the room, that a specific session happened on a specific device with no data path — without trusting ZKNOT, the host, or the operator.

Every power session is signed by a secure element on the device itself. The result is a record any third party can re-check against a published key, offline, with no central authority to trust.

## What Attested adds over Core

- **A hardware secure element (ATECC608B).** Generates its key pair on-device; the private key never leaves the chip and can't be extracted in software.
- **Signed power-session records.** Each session is signed in hardware: device identity, start/end timestamps, measured voltage and current, and an attestation that no data path was active. The signature covers all of it — change any field and verification fails.
- **Measured, not assumed.** An onboard current/voltage monitor (INA219) records the real power profile of the session, not a nominal label.
- **Third-party verifiable, offline.** Anyone with the device's public key can verify a session record without contacting ZKNOT, without the device present, and without network access. Trust comes from the math, not from us.
- **Tamper-evident history.** Session records are hash-chained — each links to the one before it — so deletion or alteration of a past record is detectable.
- **Anti-replay.** A monotonic counter advances with every session, so records can't be reused or backdated.
- **Pairs with ZKey (roadmap).** Designed to share a session identifier with the ZKey human-presence signer, so a single verifiable record can prove *both* that power was delivered with no data path *and* that a human authorized the event in the same session.

## The honest boundary — what a signed session does and doesn't prove

This is the upgrade over Core: Attested signs **on the device, in the field**, not just at our bench. So a verified session record is real cryptographic proof that *this identified device recorded a power session with these measured parameters and no active data path.*

What it does **not** claim: it isn't proof of what a charged device did internally beyond drawing power, and we don't market it as a legal guarantee of anything. It's designed for evidentiary and chain-of-custody workflows; how a given record is used in a proceeding is for the people running that proceeding to decide. We'll always tell you exactly what a claim is and what it isn't.

## How verification works

1. A session ends; the secure element signs the session record.
2. The signed record is retrieved from the device.
3. A verifier checks the signature against the device's published public key and confirms the hash chain and counter.
4. The result is independently re-checkable — by you, by a recipient, by an auditor — without trusting the website, the host, or us.

## Intended specifications (in development — subject to change)

- USB-C power-only path: D+/D− and SuperSpeed pairs physically absent; VBUS/GND pass through; CC pins for power negotiation
- 5–20V DC USB-C Power Delivery pass-through
- STM32G0B1 microcontroller · ATECC608B secure element · INA219 current/voltage monitor
- ECDSA P-256 signatures; on-device key generation, private key never exported
- Hash-chained, monotonic-counter session records
- Solid clear-resin potting with unique optical fingerprint, photographed and recorded at manufacture
- Serialized; records verifiable at verifyknot.io and from the published public key
- Patent Pending — U.S. Application No. 63/961,118 (additional applications pending)
- Designed in Utah · veteran-owned (SDVOSB) · Made in USA

## Who it's for

People who must prove something to *others*, not just protect themselves: digital-evidence and chain-of-custody work · investigators and attorneys · journalists and researchers in adversarial settings · labs and secure facilities · procurement teams that need verifiable device provenance and session integrity.

If you only need to protect your own device while charging, **PowerVerify Core** is the right product and it's available now. Attested is for when a third party has to believe you.

## Reserve a unit

Register your interest below. Reserving costs nothing now — it tells us how many to build, locks early pricing, and gets you the build-status updates. We'll confirm a ship window and terms before anything else.
