---
title: ZKKey Software Capability Specification — v5 (Canonical, HW+SW reconciled)
doc_id: SIG-SPEC-ZKKEY-005
status: CANONICAL for the v1 build window — single source of truth
supersedes: SIG-SPEC-ZKKEY-004; folds in & supersedes SIG-SPEC-ZKKEY-002-ADD-001 (hardware decision record)
author: William Shane Wilkinson (ZKNOT, INC.)
date: 2026-06-08
companions: PAT-001-ADD-001 (gate-enforcement addendum); PAT-020 provisional (strong-form gate, 2026-06-08)
governing_constraint: Cost is not a gate. Design the maximum into the board; population per build run
  (potting permanent). Population gated by firmware maturity / feature need, not cost.
headline: Flagship = strong-form gate, mechanism B (secure-MCU enclave), SPLIT-DOMAIN POPULATED (v1).
  Silicon spine LOCKED: STM32U585 enclave + Infineon OPTIGA Trust M (EAL6+) identity SE.
  Record declares binding via TWO explicit fields (presence + content), not one ordinal.
device_name: PLACEHOLDER "ZKKey" — rename open (compound-name lane; patent is brand-agnostic).
classification: ZKNOT INTERNAL — patent-sensitive
sources_of_truth: filed ZKNOT provisionals incl. PAT-011, PAT-020; SIG-SPEC-002-ADD-001 (hardware,
  ST primary sources verified 2026-06-08: AN5347/AN5600 GTZC; STM32U585 PSA-L3/SESIP3); Infineon
  OPTIGA Trust M cert listing (re-confirm before federal-facing custody claim — §9)
---

# ZKKey Software Capability Specification — v5 (HW + SW reconciled)

## 0. What changed in v5 (read first)

v5 reconciles the software spec (v4) with the hardware decision record (SIG-SPEC-002-ADD-001) into one canonical doc. The two were already in full agreement on mechanism, domain model, and silicon; v5 adopts the three places the hardware record was sharper and keeps the one place software was more careful.

1. **Record schema — binding is declared by TWO explicit fields, not one ordinal.** The single `assurance_profile` (0–5) conflated two orthogonal properties. It is **replaced** by `presence_binding_type` (R-13) and `content_binding_type` (R-14). A verifier reasons about each independently; the PAT-020 Profile 0–5 taxonomy survives only as patent vocabulary / an optional *derived* human label — not the authoritative stored field (§5).
2. **Honest-claim wording locked (verbatim).** Mechanism B is **immutable-firmware-enforced, not pure-silicon "incapable."** State it as *"no host command and no substitutable firmware can sign absent the actuation"* — never as a silicon impossibility (§2.3).
3. **A′ interlock = optional later board flex, explicitly NOT v1-critical.** B already binds presence and content at the secure-domain level; routing the sign-enable through a hardware interlock is a belt-and-suspenders option, not a v1 requirement (§2.4).
4. **Signing-key assurance residual carried identically in both halves (the careful point).** B-split anchors *identity* at EAL6+ and gives forge-needs-both + the procurement checkbox; it does **not** lab-harden the *signing* key (PSA-L3 in the enclave). That seizure question stays open (§11) and must not be implied closed (§9).

Everything else (mechanism B, split-domain populated, U585 + OPTIGA, content-binding firmware MUST) carries from v4 / the hardware record unchanged.

---

## 1. Locked v1 build parameters

| Decision | v1 value |
|----------|----------|
| **Gate mechanism (D-2)** | **B — secure-MCU enclave.** Secure domain owns button + display + signing key. Strong-form, mandatory. |
| **Domain model (D-1)** | **Split-domain, populated.** U585 enclave (signing, PSA-L3) + OPTIGA Trust M EAL6+ (identity); identity certifies signing key under YubiHSM root. |
| **Silicon — MCU** | **STM32U585** (PSA L3 / SESIP3; TrustZone + GTZC/TZSC; USB FS; HW crypto; secure boot; anti-rollback; perturbation secret-erase). Pin the certified part number. |
| **Silicon — Identity SE** | **Infineon OPTIGA Trust M, EAL6+**, USON-10 (~3×3 mm), bottom-side. |
| **Binding declaration** | **Two fields:** `presence_binding_type` + `content_binding_type` (R-13/R-14). No single ordinal. |
| **Display (D-3)** | OLED owned by the **secure partition** (GTZC-secured bus + pins). Connect = short-code **text, no QR**; **QR = Air only**. LED-first bring-up. |
| **Replay (D-4)** | Stateful rolling consumed-challenge log, depth **1024**, on the monotonic-counter floor + staleness check. |
| **Manufacturing ledger (D-5)** | Reserve storage + genesis self-sign in v1; receipt/lifecycle flow on a federal trigger. |
| **Challenge input** | **32-byte hash AND structured records** (canonical-validated). |
| **Air** | **Separate variant** — optical challenge-in / QR-out, no electrical data path. |
| **Form factor** | **30 × 90 mm, potted**, double-sided → population per build run, permanent at cast. |
| **Root** | Two-tier: **YubiHSM civilian root** issues the device cert into the OPTIGA; SEs are field identities under it. v1 = civilian, **non-FIPS**. |

---

## 2. The strong-form gate (mechanism B, locked)

### 2.1 Definition (cannot silently degrade)

The signing operation cannot be caused by host or ordinary firmware alone unless the physical actuation has occurred. All of:
- **C-G1 (MUST)** Signature only in response to a deliberate actuation **after** a valid challenge (post-nonce).
- **C-G2 (MUST)** Enforced below replaceable firmware — secure boot + immutable measured firmware + debug lock; no non-secure path signs.
- **C-G3 (MUST)** The actuation's physical state is a precondition of the signing path; the button is a **secure-world-owned GPIO** (GTZC).
- **C-G4 (MUST)** **Secure-domain display & actuation ownership.** The display interface (driver + framebuffer) and the actuation input MUST be owned by the secure domain. The domain that renders the artifact to the human MUST be the domain that signs it. *Without this, B silently degrades to A′'s show-X-sign-Y hole.* Realizable on U585: GTZC binds the display bus and GPIO to the secure world (AN5347/AN5600, verified). This makes secure-domain display ownership a **hard MCU-selection filter** and a firmware requirement.

### 2.2 Content-binding is the moat

Mechanism B was chosen over A′ because content-binding (the human saw and approved the exact signed artifact) is the differentiator, and only a secure domain that owns *both* the display and the key can guarantee it. A′ (series hardware interlock) gives the strongest *presence*-binding but the weakest *content*-binding — a compromised MCU can show X, harvest the press, and sign Y. Presence-binding and content-binding are **orthogonal properties, not a ladder.**

### 2.3 Honest-claim wording (locked, verbatim)

B is **immutable-firmware-enforced, not pure-silicon "incapable."** Permitted: *"no host command and no substitutable firmware can sign absent the actuation."* **Prohibited:** stating or implying silicon-level physical impossibility for mechanism B. Best mode = the as-built B + split-domain + secure-display (PAT-020 Embodiment 3/5) → no new matter.

### 2.4 A′ interlock — optional later flex, NOT v1

Routing the enclave sign-enable through a hardware actuation interlock (A′) would add an electrical presence guarantee on top of B. PAT-020 covers it. It is an **optional board flex for a later run, not a v1 requirement** — B already binds presence and content at the secure-domain level.

### 2.5 Assurance division (state plainly; do not over-claim)

| Key | Where | Assurance | Extraction impact |
|-----|-------|-----------|-------------------|
| **Event-signing key** | U585 enclave | **PSA L3** ("basic physical resistance") | Catastrophic — forges presence attestations. **Not EAL6+.** |
| **Device-identity key** | OPTIGA Trust M | **EAL6+** | Serious but revocable/re-issuable under the HSM root. |

What B-split buys: **dual-domain forgery resistance (forge-needs-both) + EAL6+ identity custody + the procurement checkbox.** What it does **not** buy: lab-grade protection of the signing key (§11).

---

## 3. Core ceremony requirements

FSM (PAT-008 / PAT-020): `IDLE → CHALLENGE_RECEIVED → ARMED → DISPLAY(secure) → SIGNING → OUTPUT → IDLE`, with `ERROR`. Unlisted transitions rejected.

| ID | Requirement | Force |
|----|-------------|-------|
| C-01 | Accept a challenge over ≥1 transport; accept 32-byte hash and structured records. | MUST |
| C-02 | Canonical-validate before arming; failures → ERROR. | MUST |
| C-03 | Hold one validated challenge; second while ARMED clears it → ERROR. | MUST |
| C-04 | Present readiness when ARMED (LED floor; OLED present). | MUST |
| C-05 | Deliberate, debounced actuation on a **secure-world GPIO** (§2.1). | MUST |
| C-06 | Actuation after challenge; one actuation → at most one signature. | MUST |
| C-07 | Actuations in IDLE / CHALLENGE_RECEIVED ignored. | MUST |
| C-08 | Signing inside the enclave; key on-device, non-exportable. | MUST |
| C-09 | Monotonic counter increments per OUTPUT; in the artifact. | MUST |
| C-10 | On OUTPUT consume the challenge; retain last **1024** + reject replays; + staleness. | MUST |
| C-11 | Return to safe IDLE after OUTPUT and ERROR, clearing buffers. | MUST |
| C-12 | ARMED timeout + explicit cancel → IDLE without signing. | MUST |
| C-13 | Emit artifact over ≥1 transport. | MUST |
| C-14 | Enclave/SE failure or timeout → ERROR, never silent/partial. | MUST |
| C-15 | DISPLAY shows the same buffer that will be signed (content-binding, C-G4). | MUST |

---

## 4. Canonical signed-record format (two-field binding)

Structured, versioned, crypto-agile; compact enough for Air QR rendering.

| ID | Field | Force | Notes |
|----|-------|-------|-------|
| R-01 | structured record | MUST | precondition |
| R-02 | `event_version` | MUST | |
| R-03 | `signature_algorithm` | MUST | PQ/curve agility |
| R-04 | `device_identifier`, `device_public_key`, `device_certificate_reference` | MUST | |
| R-05 | `challenge`, `event_hash` | MUST | |
| R-06 | `monotonic_counter` | MUST | |
| R-07 | `timestamp` / monotonic time | SHOULD | |
| R-08 | `session_identifier` | MUST | combined sessions (PAT-007) |
| R-09 | `prior_event_hash` | MUST | LocalChain (PAT-004) |
| R-10 | event signature **+ identity-domain signature** + cross-reference | MUST | **populated v1** (split-domain); identity SE certifies signing key (PAT-011) |
| R-11 | `firmware_hash` / secure-domain measurement | MUST | proves signing policy active |
| R-12 | `displayed_hash` / `short_code` | MUST | content-binding evidence + verbal verify |
| **R-13** | **`presence_binding_type`** | **MUST** | how presence was enforced; v1 = `secure-domain`. *(replaces `assurance_profile`)* |
| **R-14** | **`content_binding_type`** | **MUST** | whether signed artifact was bound to what was shown; v1 = `secure-domain-display`. |
| R-15 | `signing_domain_type` | MUST | v1 = `secure-MCU-enclave (PSA-L3) + discrete-identity-SE (EAL6+)` |
| R-16 | `debug_lock_state` / `lifecycle_state` | SHOULD | enclave integrity context |
| R-17 | `physical_actuation_time` / `actuation_sequence_number` | SHOULD | |

Keep R-13/R-14 as compact enum tokens — the Air QR size ceiling still applies.

---

## 5. Binding declaration (replaces the ordinal profile)

The record declares enforcement through **two orthogonal fields** (R-13, R-14). The verifier (verifyknot) MUST reason about each independently and MUST be able to require a minimum on each. It MUST NOT collapse them into a single rank, and MUST NOT treat firmware-trust content-binding as equal to secure-domain content-binding.

v1 flagship: `presence_binding_type = secure-domain`, `content_binding_type = secure-domain-display`.

The PAT-020 Profile 0–5 taxonomy is retained **only** as (a) patent vocabulary and (b) an optional *derived* human-readable label a UI MAY show — computed from R-13/R-14 + the signing-domain assurance. It is **not** an authoritative stored field. (For reference, the v1 flagship would derive to the former "Profile 4 / split-domain.")

---

## 6. Forward-compatibility (design-in; populate per run)

F-01 transport abstraction · F-02 full record format now · F-03 domain separation (**populated v1**) · F-04 FSM hooks incl. secure present-representation · F-05 reserved headroom (Air optics, ledger storage, firmware-hash, A′ interlock option).
Variants: Air (reserved optics, no data path) · display-then-confirm (secure-partition firmware, patent-gated for public/free builds) · combined power+presence (R-08) · vendor ledger (genesis self-sign CAP-03 + storage) · LocalChain (R-09) · PQ (R-03 + signer abstraction).

---

## 7. Silicon eligibility (§7-A) — LOCKED for v1

**Secure MCU (enclave) — STM32U585:**
- **C-G4 secure-domain display + button** via GTZC/TZSC (GPIO secure-by-default under TrustZone; a secure peripheral cannot have non-secure I/O — AN5347/AN5600, verified). ✓ — the decisive filter.
- PSA L3 / SESIP3 in production (cert attaches to the specific part — pin **STM32U585**). ✓
- USB OTG_FS (confirm package at BOM); HW crypto; secure key storage; secure boot; anti-rollback; perturbation secret-erase; measured-boot capable (R-11). On incumbent STM32 toolchain.
- *Not selected:* H573 (MHz unneeded for FSM + one P-256 sign + OLED; Air is a separate board). SiLabs Secure Vault / NXP LPC55S (ecosystem switch for no gain — high-assurance custody is the identity SE's job).

**Identity SE — OPTIGA Trust M, EAL6+:** on-die P-256/P-384 keygen (non-extractable), monotonic counters, X.509 ingestion, genesis self-sign, USON-10. *STSAFE-A110 believed EAL5+, not 6+ — not an equivalent if EAL6+ is the bar; verify against ST's cert listing before substitution.*

**CAP list (unchanged):** CAP-01 non-exportable signing key · CAP-02 hardware monotonic counter · CAP-03 genesis self-sign · CAP-04 ≥2 key roles (physically separated) · CAP-05 strong-form gate = B + C-G4 · CAP-06 algorithm-agile · CAP-07–12 FSM/validation/1024-log/derivation/measurement · CAP-13 actuation · CAP-14 LED · CAP-15 display driven from **secure domain** (Connect text; Air QR) · CAP-16–22 transports/storage/time/entropy · CAP-23 emit R-13/R-14/R-15 · CAP-24 firmware measurement + lifecycle reporting.

---

## 8. Decision records (ADR)

- **D-0** Design the maximum into the PCB; populate per run (potting permanent). v1 **populates** the split-domain board (already budgeted).
- **D-2 (decided)** Mechanism **B**; secure-domain ownership of display + button is a firmware MUST (C-G4). **Revisit:** only if secure-display proves unmeetable on the chosen part (met on U585) — escalate, do not silently revert to A′.
- **D-1 (decided)** **Split-domain, populated.** Signing in U585 enclave (PSA-L3); identity in OPTIGA (EAL6+); identity certifies signing under HSM root. **Revisit:** if cost/schedule forces it, ship enclave-only (`presence=secure-domain`, no identity-domain signature) with the OPTIGA footprint unpopulated — record format unchanged — but only with an explicit, honest downgrade of the seized-device custody claim.
- **D-3 / D-4 / D-5** as in §1.

---

## 9. Honesty & claim constraints

- Advertise **dual-domain forgery resistance** and **EAL6+ identity** custody. **Do not** state or imply the **signing** key is EAL6+/tamper-proof — it is PSA-L3.
- Gate wording per §2.3 (no silicon-impossibility claim for B).
- No FIPS claims without live NIST CMVP verification (140-2 sunset 2026-05-02; 140-3 pending). Civilian/federal roots never bridged.
- Any government-facing artifact: re-verify primary sources — (1) PSA-L3/SESIP3 attaches to **STM32U585** specifically; (2) OPTIGA **EAL6+ + on-die keygen** against Infineon's listing; (3) STSAFE-A exact EAL level; (4) FIPS via CMVP; (5) naming/terminology — do not propagate from this doc.

---

## 10. Patent & sequencing flags

- Best mode = as-built B + split-domain + secure-display, on U585 + OPTIGA → **PAT-020 Embodiment 3/5**, no new matter. C-G4 (secure-domain display ownership) is the element that makes content-binding **enabling** — keep as-built and as-disclosed matched.
- PAT-020 ready to file; filing opens the strong-form priority chain. Attorney target 2026-07-01; PAT-001 non-prov deadline 2027-01-15; reconcile PAT-001 "physically impossible" → Profile-1 framing (PAT-001-ADD-001); double-patenting managed by attorney.
- Keep display-then-confirm firmware / public-free-build content out of circulation until the non-provisional is filed.

---

## 11. Open items

1. **Signing-enclave assurance (the real seizure residual).** B-split anchors *identity* at EAL6+ but leaves the *signing* key at PSA-L3. If v1's threat model later includes lab-grade extraction of the signing key, that is a separate, larger decision than the identity SE and is **not** closed by B-split. Track it.
2. **Verify-before-claim:** STSAFE EAL level vs OPTIGA; exact U585 part number for the cert; U585 package USB at BOM; OPTIGA EAL6+ + keygen against Infineon listing.
3. **Device naming** (compound-name lane; trademark knockout before adopting).
4. **Next gate (#3): firmware / secure-config enforcement spec** — secure boot chain, debug-lock provisioning, anti-rollback, GTZC config binding OLED + button to the secure world, secure-partition display driver + framebuffer, key injection + OPTIGA cross-certification under the HSM root, measured-firmware → device cert.

---

## 12. Changelog

| Version | Date | Change |
|---------|------|--------|
| v1 (REQ/DEC) | 2026-06-08 | Initial requirements + decisions |
| v2 (SPEC-002) | 2026-06-08 | Merged; strong-form mandatory; ATECC removed from flagship |
| SPEC-002-ADD-001 | 2026-06-08 | (Hardware) resolved mechanism = B, C-G4, split-domain populated, U585 + OPTIGA, proposed R-13/R-14 |
| v3 (SPEC-003) | 2026-06-08 | Integrated PAT-020; assurance profiles; expanded record; mechanism engineering-only |
| v4 (SPEC-004) | 2026-06-08 | Locked B + split-domain populated + U585/OPTIGA; content-binding firmware MUST; assurance-division line |
| **v5 (SPEC-005)** | 2026-06-08 | **HW+SW reconciled into one source of truth (folds in & supersedes SPEC-002-ADD-001). Record schema: replaced ordinal `assurance_profile` with two fields `presence_binding_type` (R-13) + `content_binding_type` (R-14); reconciled signing_domain_type (R-15). Locked honest-claim wording (B = immutable-firmware-enforced, not silicon-impossible). A′ interlock marked optional non-v1 flex. Signing-key assurance residual carried explicitly (§11) and constrained in claims (§9).** |

*Supersedes SIG-SPEC-ZKKEY-004 and folds in SIG-SPEC-ZKKEY-002-ADD-001. Provenance: determinations trace to filed provisionals (PAT-011, PAT-020) and the hardware record; silicon facts verified against ST primary sources (Infineon to re-confirm per §9). The OPTIGA protects identity, not the signing key — stated so claims stay honest.*
