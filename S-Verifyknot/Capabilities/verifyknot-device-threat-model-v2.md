---
title: VerifyKnot — Device Class Threat Model & Trust Profile
system: verifyknot
version: v2 (supersedes v1 — see Corrections)
status: device taxonomy verified against HW-001 §3.4.2 + patent set; SelfKnot/DIY taxonomy UNVERIFIED (not in primary source)
owner: Shane
created: 2026-06-04
primary_sources: ZKNOT_HW-001 v2.0; ZKNOT_DOC-003 patents summary (PAT-001..019)
canonical_path: ~/ZKNOT/3_OPS/km/systems/verifyknot-device-threat-model.md
---

# VerifyKnot — Device Class Threat Model & Trust Profile (v2)

## Corrections vs v1 (read first)
v1 of this doc, built before reading HW-001 and the patent set, contained errors:
- Invented device classes "SelfKnot Connect Pico / Black Pill." These names appear in
  NEITHER primary-source doc. Canonical signing devices are ZK-K, ZK-A, PV-A (HW-001 §3.4.2).
- Mischaracterized ZKKey Air as wireless with a relay/pairing surface. ZK-A is
  air-gapped OPTICAL (PAT-009): QR challenge via camera, no electrical data path, no RF.
- Stated the post-nonce ceremony is constant across "every device." It is the constant
  across the human-presence tier (ZK-K, ZK-A) only. PowerVerify Attested signs
  autonomously with no human gate.
v1 is superseded. If v1 was committed to the vault, mark it superseded or remove it.

## What the verify page consumes
Per HW-001 §3.4.1: a user enters a SHORT CODE (event-level, e.g. ZK-6GUA-7DV). The
backend resolves it to an ARTIFACT / event record containing device_id, signature,
public key, chain linkage. Device class is read from the device_id prefix; provenance
is established by looking that device up in the ZKNOT registry.

## Two axes (keep separate)
1. Identity assurance — is device_id + signing public key registered in the ZKNOT
   device registry (HW-001 §6)? Registered -> ZKNOT-PROVISIONED. Not registered ->
   SELF-ASSERTED.
2. Device class — read from device_id prefix (HW-001 §3.4.2).

## Canonical device taxonomy (HW-001 §3.4.2)
| prefix | product | signs | MCU + SE | key custody | identity | challenge transport | post-nonce human gate | status |
|--------|---------|-------|----------|-------------|----------|---------------------|----------------------|--------|
| ZK-K | ZKKey Connect | human-presence signature | STM32F103CBT6 + ATECC608B (ZKM-001) | ATECC608B secure element | ZKNOT registry (unique keypair, pubkey in ZKNOT DB) | electrical USB-C | YES (PAT-001, PAT-008) | ACTIVE / assembly |
| ZK-A | ZKKey Air | human-presence signature | STM32 + ATECC608B + camera + e-ink/OLED + battery | ATECC608B secure element | ZKNOT registry | OPTICAL QR — no electrical data path (PAT-009) | YES | DEFINED / future |
| PV-A | PowerVerify Attested | power-session certificate | STM32G0B1 + ATECC608B (0x6A) + INA219 | ATECC608B secure element | ZKNOT registry | electrical USB-C (CC negotiation) | NO — autonomous power signing | IN DEV |
| PV-C | PowerVerify Core | nothing — passive, no MCU/SE | none | n/a | verified by multimeter (HW-001 §3.6) | n/a | n/a | ACTIVE — does NOT produce signed records |

Roadmap tiers (not shipping; HW-001 §5):
- ZKM-002 Pro: STM32F4 + ATECC608B + display + GPS + storage — premium ZKKey.
- ZKM-003 Ultra: dual SE (ATECC608B + SE050 + STM32H7), PAT-011 — identity SE and
  signing SE separated; no single compromise yields a complete forgery. Would need its
  own prefix / threat profile when it ships.

## DIY / SelfKnot — GAP (blocks the labels you asked for)
SelfKnot does not exist in HW-001 or the patents. There is no device_id prefix for a
self-built unit. To label DIY builds on the verify page you must first, against a
canonical source, decide:
- a prefix scheme for DIY builds (proposed, NOT canonical: SK-P Pico/RP2040,
  SK-B Black Pill/STM32F4),
- that DIY builds are always SELF-ASSERTED tier (never in ZKNOT registry),
- the SelfKnot brand name itself (USPTO TESS clearance still pending per prior context).
Until those are entered in HW-001 / naming doc, treat SelfKnot device names as
display-layer strings only, decoupled from any stored identifier, so a rename or a
dirty TESS result is a UI change, not a data migration.

## Threat-model deltas (grounded)
- ATECC608B secure element (all provisioned units + any DIY that added one): private
  key generated in-chip, never exported; hardware TRNG for nonces (HW-001 §6); monotonic
  sign_count increments per signing, cannot decrement — replay/backdate evidence
  (PAT-001, HW-001 §6).
- DIY software-key custody (Pico / Black Pill without SE): key in MCU flash,
  extractable via debug port unless locked. RP2040 has no secure boot. STM32F4 RDP is
  downgradable by documented glitch attacks. No registry entry -> device identity is a
  claim only.
- ZK-K (Connect): electrical USB data path exists; host can deliver a nonce. The FSM
  (PAT-008: IDLE -> CHALLENGE_RECEIVED -> ARMED -> SIGNING -> OUTPUT, single-use challenge,
  actuation must follow challenge) plus canonical validation plus the physical button
  gate the signature. Single SE = single point of compromise.
- ZK-A (Air): optical air-gap, no electrical data path; host cannot inject data or
  command the device electrically (PAT-009). Optical channel is unidirectional
  host->device. Residual: the operator must visually trust the QR source. Strongest
  host-isolation of the signing tier. Future.
- PV-A (PowerVerify Attested): attests a power session (voltage/current/duration +
  data-path-elimination + CC-line behavior), signed autonomously — NO human presence
  claim. Different attestation type, not a human-gated signature.
- COMBINED_SESSION (PAT-007): one record binds a PV-A power cert and a ZKKey
  human-presence signature under a shared session_id. Verify must render BOTH devices,
  BOTH roles, BOTH threat profiles. ZK-6GUA-7DV is this type.
- Dual-SE (ZKM-003 Ultra, future, PAT-011): identity SE cannot sign events, signing
  SE cannot assert identity; complete forgery requires compromising two packages.

## The constant (human-presence tier only)
Post-nonce, FSM-gated, human-actuation-after-challenge (PAT-001 + PAT-008) is the
critical element for ZK-K and ZK-A. It does NOT apply to PV-A. Surface the FSM/ceremony
result independently of the device badge, but only for human-presence devices.

## Badge / discriminator logic (derived)
    record = resolve(short_code)            # HW-001 §3.4.1
    for each device_id in record.devices:   # COMBINED_SESSION may have >1
        reg = zknot_registry.lookup(device_id, signing_pubkey)   # HW-001 §6
        if reg.found:
            product = prefix_to_product(device_id)   # ZK-K / ZK-A / PV-A
            badge   = "ZKNOT-PROVISIONED · {product} · identity verified vs ZKNOT registry"
            role    = human_presence if product in {ZK-K, ZK-A} else power_session
        else:
            product = artifact.claimed_type or "unknown"
            badge   = "SELF-ASSERTED (DIY) · {product}, as claimed · not verified vs registry"
            # key custody unknown unless artifact carries secure-element evidence
    render row per device with badge + role + threat profile
    if any role == human_presence: show post-nonce ceremony result

Note: registry "identity" for ZK-K as-built is a public-key registry match (HW-001 §6),
not confirmed to be a full X.509 CA chain. CA-cert chains and dual-SE identity are
described as patent embodiments (PAT-005, PAT-011), associated with higher tiers. Do not
claim "CA-attested" on the ZK-K verify badge unless the as-built provisioning SOP issues
a cert chain — flag for confirmation.

## Open items to confirm against primary source
- [ ] As-built ZK-K identity: registry pubkey match vs CA cert chain (provisioning SOP).
- [ ] DIY/SelfKnot prefix scheme + forced SELF-ASSERTED tier — enter in HW-001 §3.4.2.
- [ ] SelfKnot brand name (USPTO TESS).
- [ ] Whether PV-C (passive, no signature) ever needs a verify-page representation.

---
*Page 1 of 1*
