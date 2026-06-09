---
title: ZKKey Firmware & Secure-Configuration Enforcement Specification (Gate #3)
doc_id: SIG-FW-ZKKEY-001
status: DRAFT — firmware enforcement layer under the canonical capability spec
parent: SIG-SPEC-ZKKEY-005 (canonical capability spec, HW+SW reconciled)
author: William Shane Wilkinson (ZKNOT, INC.)
date: 2026-06-08
silicon: STM32U585 secure MCU (enclave) + Infineon OPTIGA Trust M (EAL6+) identity SE
classification: ZKNOT INTERNAL — patent-sensitive (feeds PAT-020 best-mode)
primary_sources_verified_2026-06-08:
  - ST AN5447 (Secure Boot & Secure Firmware Update on TrustZone STM32 / TF-M)
  - ST wiki Security:Secure_Boot_for_STM32H5 + Security features (HDPL model, BOOT_LOCK, HDP) — same iRoT/uRoT model applies to U5 via AN5447
  - ST community: U585 has full HW crypto + TF-M/MCUboot SBSFU in STM32Cube_FW_U5; HDP/RDP2 for key protection
  - Infineon OPTIGA Trust M Solution Reference Manual + KBA235163/235406 + personalize-optiga-trust (EAL6+, on-die GenKeyPair, ECDSA, cert slots, re-personalization)
verify_before_build: see §9 (exact RM0456 RDP/option-byte mapping; OPTIGA personalization SKU/path; Secure Manager availability on U585)
---
update: SIG-FW-ZKKEY-001 → v0.2 (close its §9): FW-S-05 → decide OEMiRoT (note STiRoT tamper-restrictiveness for Redoubt); FW-L-01 → RDP2 + HSM-custodied OEM2 password, set at pogo jig pre-pot; FW-P-02/03 → OPTIGA std-V3 DIY field-perso, pin identity curve (P-256 to match signing); add a Redoubt section: device SHOULD bind a signing-time TST when online, else emit log-ready records (already does via prior_event_hash); add rotating-key provisioning hook (R-19).
# ZKKey Firmware & Secure-Configuration Enforcement Specification (Gate #3)

## 0. Purpose, scope, boundary

This spec turns the canonical capability requirements (SIG-SPEC-005 §2 C-G1–C-G4, the AP-4 split-domain model, the two-field binding R-13/R-14, and R-10/R-11/R-16) into **firmware and secure-configuration requirements** for the STM32U585 enclave and the OPTIGA Trust M identity SE. It is where content-binding stops being a requirement and becomes the actual secure design.

**In scope:** the secure/non-secure partition map; secure boot chain; runtime isolation (GTZC); debug-lock / lifecycle / anti-rollback; the in-enclave signing ceremony (incl. the content-binding invariant); the key + identity provisioning and cross-certification ceremony under the YubiHSM root; measured-firmware → device-certificate binding.

**Out of scope (separate gates):** the host/application wire protocol; the verifier (verifyknot) logic; the Air optical variant's capture/decode firmware; the manufacturing-line runbook (gate #4 candidate).

**The governing rule:** *anything that touches presence-binding or content-binding lives in the Secure world.* If non-secure code can influence what is shown or what is signed, the moat is gone.

Requirement IDs: `FW-S-##` secure boot · `FW-I-##` isolation · `FW-L-##` lifecycle/lock · `FW-C-##` signing ceremony · `FW-P-##` provisioning/cross-cert. Force: MUST / SHOULD / MAY.

---

## 1. Trust architecture — what lives where

The U585 runs Arm TrustZone-M (Cortex-M33). Two partitions:

| Secure partition (S) — the enclave | Non-secure partition (NS) |
|------------------------------------|---------------------------|
| Signing private key (generated on-die, non-exportable) | USB device stack / transport |
| Signing FSM + challenge canonicalization | Host-comms relay (passes challenge bytes in, artifact bytes out) |
| OLED display driver + framebuffer (content-binding) | Optional non-secure UI chrome (status text only) |
| Button GPIO ownership (presence-binding) | Housekeeping, power management (non-security) |
| Monotonic counter; 1024-deep consumed-challenge log | |
| OPTIGA I²C interface + cross-cert logic | |
| HW crypto (PKA/SAES/hash/RNG), secure flash regions | |

- **FW-A-01 (MUST)** Every asset in the Secure column above MUST reside in the secure partition; NS code MUST reach the enclave only through a minimal, audited set of non-secure-callable (NSC) veneers (§5.1).
- **FW-A-02 (MUST)** The NSC surface MUST NOT include any call that signs, drives the display, reads/asserts the button, or mutates the counter/log directly. NS may only *submit a challenge* and *collect a completed artifact*.

---

## 2. Secure boot chain (FW-S)

U585 secure boot follows the ST TF-M / MCUboot model (AN5447): an **immutable Root of Trust** (OEMiRoT in user flash, or STiRoT in system flash) at hide-protection level HDPL1, an optional updatable RoT (uRoT) at HDPL2, then the secure user app at HDPL3, with the non-secure app alongside. `BOOT_LOCK` fixes the boot entry to the secure RoT address.

- **FW-S-01 (MUST)** Only OEM-signed, authenticated firmware images run. The RoT MUST verify each stage's signature against the OEM public key before transferring control. (TF-M/MCUboot image signing; OEMiRoT or STiRoT.)
- **FW-S-02 (MUST)** `TZEN=1` (TrustZone enabled) and `BOOT_LOCK` set so the device's unique boot entry is the unmodifiable secure RoT address — no alternate/system-bootloader entry on production units.
- **FW-S-03 (MUST)** The signing key, signing FSM, and content-binding code execute only in the HDPL3 secure app, reached only after the RoT chain validates.
- **FW-S-04 (MUST)** The OEM RoT public key / hash MUST be stored immutably (HDP-locked / write-protected per §3, §4), so it cannot be replaced to authenticate attacker firmware.
- **FW-S-05 (SHOULD)** Prefer **OEMiRoT** (OEM-controlled keys) over STiRoT unless the ST-managed RoT's constraints are acceptable; decide at §9. If STM32 **Secure Manager** is adopted instead of raw TF-M, re-map FW-S-01..04 onto its model (verify availability/version — §9).
- **FW-S-06 (MUST)** A measurement of the running secure firmware (image hash / TF-M measured boot value) MUST be retrievable by the secure app for inclusion in the record (R-11) and the device cert (§7).

---

## 3. Runtime isolation — GTZC binds the moat to the Secure world (FW-I)

This is the firmware realization of **C-G4** (secure-domain display + button ownership). On U585, GPIOs are secure by default under TrustZone, and GTZC/TZSC assigns peripherals to the Secure world; a peripheral configured secure cannot have non-secure I/O (verified against ST GTZC app notes in the hardware record).

- **FW-I-01 (MUST)** The **OLED bus** (SPI or I²C) and its GPIO pins MUST be assigned to the Secure world via GTZC/TZSC + GPIO secure config. The display driver and framebuffer live in S. NS code cannot render to or read the panel.
- **FW-I-02 (MUST)** The **button GPIO** (+ its EXTI/interrupt path) MUST be Secure-owned. NS code can neither read a forged "pressed" state into the signing path nor assert the line.
- **FW-I-03 (MUST)** The **OPTIGA I²C** interface MUST be Secure-owned (cross-cert and identity operations never traverse NS).
- **FW-I-04 (MUST)** HW crypto (PKA/SAES/hash), RNG, the monotonic-counter peripheral/store, the consumed-challenge log store, and the secure-key flash region MUST be Secure-only via GTZC (TZSC for securable peripherals; MPCBB for SRAM blocks; MPCWM/watermark for flash regions).
- **FW-I-05 (MUST)** A GTZC illegal-access event (NS touching a secure resource) MUST be trapped and routed to a safe ERROR/reset, never ignored.

---

## 4. Debug lock, lifecycle, anti-rollback (FW-L)

- **FW-L-01 (MUST)** Production units ship **debug-closed**: readout protection at the level that disables debug access to secure memory, set irreversibly for production. (U5 RDP / product-state model + HDP; pin the exact RDP level + option bytes against RM0456 — §9.) Open/Provisioning states are used only on the line, never shipped.
- **FW-L-02 (MUST)** Hide-protection (HDP) MUST cover the iRoT and secure assets so they are not readable/modifiable after boot progresses past their level.
- **FW-L-03 (MUST)** **Anti-rollback:** secure firmware carries a monotonic version counter; the RoT MUST refuse to boot/install an image with a lower version, preventing downgrade to a weaker/vulnerable build. (TF-M anti-rollback / NV counters.)
- **FW-L-04 (MUST)** The current `lifecycle_state` and `debug_lock_state` MUST be readable by the secure app for inclusion in the record (R-16) and the device cert (§7), so a verifier can confirm the unit was in a locked production state.
- **FW-L-05 (MUST)** No NSC veneer, test hook, or debug command may exist on production firmware that bypasses the signing ceremony. CI MUST assert the NSC surface matches the audited allowlist (FW-A-02).

---

## 5. The in-enclave signing ceremony (FW-C) — content-binding made real

### 5.1 The NSC boundary (minimal)
- **FW-C-01 (MUST)** Exactly two NSC entry points: `submit_challenge(bytes)` and `collect_artifact()`. Both copy data across the boundary by value into/out of secure RAM; no shared mutable buffer the NS side can alter mid-ceremony.

### 5.2 The ceremony (all steps in S)
- **FW-C-02 (MUST)** On `submit_challenge`, the secure app canonicalizes and validates the challenge (32-byte hash or structured record) into a **secure-RAM buffer `B`**; invalid → ERROR, no arm. (C-02)
- **FW-C-03 (MUST)** Derive the display representation (short code / displayed_hash) **from `B`** and render it via the Secure-owned display (FW-I-01). The rendered value MUST be derived from the exact bytes that will be signed.
- **FW-C-04 (MUST)** Enter ARMED; await a debounced press on the Secure-owned button (FW-I-02) occurring **after** display. Timeout/cancel → IDLE. (C-G1, C-06, C-12)
- **FW-C-05 (MUST — the content-binding invariant)** The buffer signed MUST be **the same secure-RAM buffer `B`** that was displayed. The firmware MUST NOT re-read, re-fetch, or accept any challenge value from NS between display and signing. *This single invariant is what makes the device show-X-sign-X, not show-X-sign-Y.*
- **FW-C-06 (MUST)** On valid press: increment the monotonic counter (C-09); check `B`'s identity against the 1024-deep consumed-challenge log and reject replays (C-10); sign `B` (+ assembled record fields) with the enclave key (C-08).
- **FW-C-07 (MUST)** Assemble the record (SIG-SPEC-005 §4): event signature + identity-domain attestation (R-10, §6), firmware measurement (R-11), `presence_binding_type=secure-domain` (R-13), `content_binding_type=secure-domain-display` (R-14), `signing_domain_type` (R-15), lifecycle/debug state (R-16), counter, prior hash, etc.
- **FW-C-08 (MUST)** Append `B` to the consumed-challenge log (power-loss-safe write), clear the armed state and `B`, return to IDLE. `collect_artifact()` then returns the assembled record to NS. (C-10, C-11)
- **FW-C-09 (MUST)** Any enclave/OPTIGA/crypto failure or timeout → ERROR with buffers cleared; never a partial or silent signature. (C-14)

---

## 6. Key + identity provisioning and cross-certification (FW-P) — under the YubiHSM root

This realizes the **split-domain AP-4** binding and the **R-10** identity-domain attestation. Two on-die keys in two packages, bound under your two-tier civilian root.

### 6.1 Enclave signing key (U585)
- **FW-P-01 (MUST)** Generate the signing keypair **inside the U585 secure key store**, non-extractable; export only the public key. Private key never leaves the enclave. (CAP-01; PSA-L3 custody — not EAL6+, §8.)

### 6.2 Identity key (OPTIGA Trust M)
- **FW-P-02 (MUST)** The device-identity key is an **on-die OPTIGA key** (GenKeyPair, non-extractable; EAL6+ hardware custody). The OPTIGA ships pre-provisioned with a unique keypair + Infineon-CA-chained X.509 cert; ZKNOT MUST establish a device-identity cert **chained to the YubiHSM civilian root** (re-personalize a cert slot, or layer a ZKNOT cert) so trust roots at ZKNOT, not Infineon. (Infineon cert MAY be retained as supply-chain provenance.)
- **FW-P-03 (SHOULD)** Use a P-256 identity key to match the device signing curve unless the OPTIGA's default P-384 device cert is preferred for the root chain — pin curve at §9.

### 6.3 Cross-certification (the dual-domain bind)
- **FW-P-04 (MUST)** During provisioning, the **OPTIGA identity key signs an attestation** over `{enclave_signing_pubkey, device_serial, firmware_measurement, lifecycle_state}` — i.e., the identity domain certifies the signing domain. This attestation (or a derived cert) is the **R-10 identity-domain signature** carried in every event record. (OPTIGA ECDSA-signs arbitrary digests — verified.)
- **FW-P-05 (MUST)** The YubiHSM **civilian** root issues/anchors the OPTIGA device-identity cert; the verifier's chain is `event sig ← enclave key`, `enclave key ← OPTIGA attestation`, `OPTIGA cert ← YubiHSM root`. **Forging a complete attestation requires compromising both the enclave and the OPTIGA.** Civilian and federal roots are never bridged.
- **FW-P-06 (MUST)** Emit a signed **genesis record** at provisioning (the AP-5 / fixture-interlocked profile if a sealed provisioning fixture is used — PAT-020 Embodiment 5) capturing serial, both public keys, firmware measurement, lifecycle/debug state, and enforcement types. This is the first entry in the device's LocalChain / vendor ledger (D-5 reserved).

### 6.4 Provisioning environment
- **FW-P-07 (MUST)** Provisioning runs only in the Open/Provisioning lifecycle state, behind §4's locks, after which the device is irreversibly closed (FW-L-01). A sealed fixture/interlock MAY gate the provisioning signing op (PAT-020 Embodiment 5).
- **FW-P-08 (MUST — honesty)** EAL6+ may be claimed for the **OPTIGA hardware key custody**. The **personalization-environment** EAL6+ applies to Infineon's facility; if ZKNOT writes certs in-house, do **not** claim ZKNOT's personalization step is EAL6+ (§8, §9).

---

## 7. Measured-firmware → device certificate (R-11 / R-16)

- **FW-7-01 (MUST)** The secure firmware measurement (FW-S-06), the secure-boot policy/RoT identity, and the lifecycle/debug-lock state MUST be bound into the provisioning/device certificate (or the genesis record), so a verifier can confirm the signature was produced by a unit provisioned under the approved signing policy and locked state — not a debug/open unit. (PAT-020 §5,§11; SIG-SPEC-005 R-11/R-16.)
- **FW-7-02 (SHOULD)** Include the `presence_binding_type` and `content_binding_type` values the firmware enforces in the device cert as well, so the binding declaration is anchored at provisioning, not just asserted per-event.

---

## 8. Honesty & claim constraints (carried from SIG-SPEC-005 §9)

- The gate is **immutable-firmware-enforced** (secure boot + debug lock + GTZC isolation), **not pure-silicon "incapable."** State as "no host command and no substitutable firmware can sign absent the actuation."
- **Signing key = PSA-L3** in the enclave; **identity key = EAL6+** in the OPTIGA. Do not imply the signing key is EAL6+/tamper-proof. The signing-enclave assurance residual (SIG-SPEC-005 §11) is unchanged by this gate.
- EAL6+ personalization-environment claim = Infineon's facility only; ZKNOT in-house cert-writing is not EAL6+.
- No FIPS claims without live NIST CMVP verification.

---

## 9. Verify-before-build (primary-source items — feed best-mode & BOM)

1. **RDP / product-state / option-byte mapping** for U585 — pin exact level that closes secure debug irreversibly for production, plus HDP and WRP settings, against **RM0456** and the U5 security app notes. (Confirmed at concept level: RDP2 + HDP usable; exact bytes unverified here.)
2. **OEMiRoT vs STiRoT vs STM32 Secure Manager** on U585 — confirm Secure Manager availability/version for U5 and decide RoT path; if Secure Manager, re-map §2. (TF-M/MCUboot/OEMiRoT confirmed for U585.)
3. **OPTIGA personalization path** — confirm the SKU/tooling (Express/MTR provisioning, CIRRENT Cloud ID, or a provisioning server) that lets ZKNOT inject a device-identity cert chained to the YubiHSM root; confirm cert-slot size (~1.3–1.7 KB) holds your chain; pin identity curve (P-256 vs P-384).
4. **OPTIGA ECDSA attestation format** for FW-P-04 (digest construction over the enclave pubkey bundle) against the OPTIGA Solution Reference Manual.
5. **U585 USB** package/class (OTG_FS) at BOM.
6. **EAL6+ scope** wording (hardware vs personalization environment) before any government-facing claim.

Do not propagate any of the above into a federal-facing artifact without checking the cited ST/Infineon primary source.

---

## 10. Patent best-mode note

This firmware architecture — secure-domain ownership of display + button (FW-I-01/02), the content-binding invariant (FW-C-05), secure boot + debug lock, and the OPTIGA cross-cert bind (FW-P-04/05) — **is the enabling detail** for PAT-020 Embodiment 3 (secure-MCU signing domain) and Embodiment 4 (split-domain). As-built MUST equal as-disclosed: the non-provisional should describe this secure-config enforcement (especially FW-C-05, the show-X-sign-X invariant) as the mechanism that makes content-binding real. No new matter relative to PAT-020.

---

## 11. Open items / next gate

1. Resolve the §9 verify-before-build items (RoT path, RDP bytes, OPTIGA personalization) — these gate firmware bring-up and the BOM.
2. **Gate #4 candidate:** the **provisioning/manufacturing runbook** (the line procedure that executes §6 under the fixture and locks the device), and/or the **verifier spec** (how verifyknot checks the §6 chain + the two binding fields). Pick one to do next.
3. Carry-forward residual (unchanged): signing-enclave assurance is PSA-L3; not closed by this gate.

---

## 12. Changelog

| Version | Date | Change |
|---------|------|--------|
| SIG-FW-001 v0.1 | 2026-06-08 | Initial firmware/secure-config enforcement spec (gate #3): partition map, TF-M secure boot, GTZC isolation, debug-lock/anti-rollback, in-enclave signing ceremony with content-binding invariant (FW-C-05), OPTIGA cross-cert under YubiHSM root, measured-firmware→cert. Verified against ST AN5447 / OPTIGA reference manual; verify-before-build items in §9. |

*Child of SIG-SPEC-ZKKEY-005. Provenance: enforcement requirements trace to the canonical spec and PAT-020; STM32U585 and OPTIGA mechanisms verified against ST/Infineon primary sources on 2026-06-08, with residual items flagged in §9. Honest-claim constraints (PSA-L3 signing vs EAL6+ identity; immutable-firmware-enforced, not silicon-impossible) carried from the parent spec.*
