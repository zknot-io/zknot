---
title: ZKKey Strong-Form Mechanism & v1 Silicon — Decision Record (Addendum to SIG-SPEC-ZKKEY-002)
doc_id: SIG-SPEC-ZKKEY-002-ADD-001
status: CANONICAL for the v1 build window
type: Decision record (ADR) — resolves the single open item in SIG-SPEC-ZKKEY-002
resolves: SIG-SPEC-ZKKEY-002 §2.3 (mechanism), §2.4 (D-1 realization), §10 (open item)
supersedes: none  # v1 decisions (SIG-DEC-ZKKEY-001) were already superseded by SIG-SPEC-ZKKEY-002
companion: SIG-SPEC-ZKKEY-002 (canonical spec); PAT-001-ADD-001 (gate-enforcement finding);
  PAT-020 strong-form provisional (ready to file)
author: William Shane Wilkinson (ZKNOT, INC.)
date: 2026-06-08
governing_constraint: Cost is not a gate. Design the maximum into the board; population is per
  build run (potting is permanent). Population gated by firmware maturity / feature need, not cost.
classification: ZKNOT INTERNAL — patent-sensitive
sources_of_truth: SIG-SPEC-ZKKEY-002; PAT-001-ADD-001; filed ZKNOT provisionals (esp. PAT-011 dual-SE);
  ST primary sources verified 2026-06-08 (AN5347/AN5600 GTZC peripheral+GPIO security; STM32U585
  PSA Certified Level-3 / SESIP3 announcement & security guidance); Infineon OPTIGA Trust M datasheet
  (to be re-confirmed before any federal-facing custody claim — see §8)
fold_into: SIG-SPEC-ZKKEY-003 (edit list in §9)
---

# ZKKey Strong-Form Mechanism & v1 Silicon — Decision Record

## 0. What this resolves (read first)

SIG-SPEC-ZKKEY-002 locked the flagship as **strong-form gate only** and left exactly one open
decision: **which strong-form mechanism** (§2.3, options A / A′ / B), which in turn resolves the
key-domain realization (§2.4) and completes the silicon shortlist (§8/§10). This record closes that
item and, for the first time in the SIG family, **binds part numbers** (the spec deliberately
excluded them). Its determinations are to be folded into the next spec revision, **SIG-SPEC-ZKKEY-003**
(edit list in §9). It does **not** supersede the v1 decisions doc — that was already done by
SIG-SPEC-ZKKEY-002.

Two reframes drive the determination and are recorded so they cannot be lost:

- **Presence-binding ≠ content-binding.** *Presence-binding* proves a live human physically actuated
  at signing time. *Content-binding* proves the human saw and approved **the exact artifact that got
  signed** (display-then-confirm). These are **orthogonal properties, not a ladder** — a higher
  "assurance profile" number is not strictly better. The moat is **content-binding**.
- **Why this kills A′ as the primary mechanism.** A series hardware interlock (A′) gives the
  *strongest presence-binding* (electrical, no firmware in the gate path) but the **weakest
  content-binding**: the MCU still drives the display and feeds the buffer to the signer, so a
  compromised MCU can show hash X, harvest the legitimate press, and sign hash Y. The interlock
  proves "a human pressed," not "the human approved *this*." For evidentiary/journalistic use,
  content-binding is the whole point.

---

## 1. Determinations at a glance

| # | Item | Determination |
|---|------|---------------|
| **D-2 (resolved)** | Strong-form mechanism (§2.3) | **Option B — collapsed secure-MCU enclave.** Secure execution domain owns the signing key **and** the display/indication path **and** the actuation input. Binds presence **and** content. |
| **C-G4 (new MUST)** | Secure-domain display ownership | The path that renders the challenge and the actuation input MUST be owned by the secure domain (securable peripheral + secure GPIO). Without this, B degrades to A′'s show-X-sign-Y hole. |
| **D-1 (resolved)** | Key-domain realization (§2.4) | **Split-domain, populated in v1.** Secure-MCU signing domain (event-signing key) **+** discrete high-assurance **Identity SE** (device-identity key), cross-certified. Forging a complete attestation requires breaking **both**. |
| **Silicon — MCU** | Secure microcontroller | **STM32U585** (PSA Certified Level-3 / SESIP3; Arm TrustZone + GTZC; USB; crypto accel; secure boot; anti-tamper secret-erase). |
| **Silicon — Identity SE** | Discrete identity element | **Infineon OPTIGA Trust M (CC EAL6+)** — lead. ST **STSAFE-A** is an in-ecosystem alternative (verify exact EAL level, §8). |
| **Root model** | Trust anchor | Two-tier: **YubiHSM (civilian root)** issues the device cert into the Identity SE; device SEs are field identities under it. v1 = civilian, **non-FIPS**. |
| **Record schema** | Enforcement representation | Encode **presence_binding_type** and **content_binding_type** as **two separate fields**, not one ordinal `assurance_profile` (§7, proposed R-13/R-14). |

Assurance v1 ships at: **content-binding = secure-domain (B)**; **presence-binding = secure-domain
enforced**; **identity custody = EAL6+ discrete SE**.

---

## 2. D-2 (resolved) — Mechanism = Option B (collapsed secure-MCU enclave)

**Status:** Canonical · resolves SIG-SPEC-ZKKEY-002 §2.3

**Context.** The spec defined the strong-form gate (C-G1/2/3) and left the *mechanism* open between
A (presence-gating SE), A′ (series hardware-enable), and B (collapsed secure-MCU). The deciding
property is content-binding (see §0).

**Determination.** **Option B.** The signing key and the challenge-display/indication path live in
one secure execution domain whose gate is enforced by attested, secure-boot-locked, debug-locked,
anti-rollback firmware. The domain shows X, waits for a deliberate actuation on a secure-owned input,
and signs the **same buffer X**. A compromised non-secure relay can offer a different challenge — but
the human sees it on a secure-owned display and declines; it **cannot show-X-sign-Y**.

**Rationale.**
- Only B makes display-then-confirm *trustworthy* (content-binding), which is the moat.
- B is compact for the 30×90 potted envelope and its firmware is evolvable post-launch.
- Honest claim wording (carry from SIG-SPEC-ZKKEY-002 §2.3): B is **immutable-firmware-enforced**,
  not pure-silicon "incapable." State it as *"no host command and no substitutable firmware can
  sign absent the actuation,"* never as a silicon impossibility.
- A′'s electrical presence guarantee may be layered on later as a **belt-and-suspenders** option
  (route the secure-MCU sign-enable through a hardware actuation interlock); PAT-020 covers it. This
  is an **optional board flex, not v1-critical**, because B already binds both at the secure-domain level.

**Consequences.** The real cost of B is **secure-MCU lifecycle firmware** — secure boot chain,
debug-lock provisioning, anti-rollback, key injection + cross-certification under the HSM root. That
is where schedule risk now lives (carried into the firmware/secure-config pass). It also imposes the
new content-binding requirement, §3.

**Revisit trigger.** Only a finding that secure-domain display ownership (C-G4) is unachievable on
the selected MCU — escalate, do not silently revert to A′ (which forfeits content-binding).

---

## 3. C-G4 (new MUST) — Secure-domain display & actuation ownership

**Status:** Canonical · refines SIG-SPEC-ZKKEY-002 §2.1

**C-G4 (MUST).** The challenge-rendering/indication path (display interface and framebuffer logic)
**and** the actuation input MUST be owned by the **secure execution domain**. The domain that renders
the artifact representation to the human MUST be the same domain that produces the signature over
that artifact. Non-secure firmware MUST NOT be able to drive the display or assert the actuation.

**Why this is load-bearing.** B's content-binding holds *only* if the display is secure-owned. If
non-secure code drives the display, B silently degrades to A′'s show-X-sign-Y weakness (non-secure
code shows X; the secure domain signs whatever buffer it is handed). C-G4 makes secure-domain
display ownership a hard requirement and a **hard filter on MCU selection**.

**Realizability (verified, ST primary sources, 2026-06-08).** On STM32 TrustZone, GTZC/TZSC assigns a
peripheral as secure; ST states a secure peripheral's I/O cannot be configured non-secure ("it is not
possible to connect a secure peripheral to a non-secure I/O" — AN5600), and on STM32U5 all GPIO are
secure by default when TrustZone is enabled (AN5347). Therefore the display bus (SPI/I²C) and the
actuation GPIO can be bound to the secure world. **Firmware consequence:** the display driver +
framebuffer live in the secure partition — carried into the firmware/secure-config pass.

---

## 4. D-1 (resolved) — Key-domain realization = split-domain, populated v1

**Status:** Canonical · resolves SIG-SPEC-ZKKEY-002 §2.4 · realizes R-10 / F-03 / PAT-011

**Determination.** **Split-domain, populated in v1.** Two protected domains:
- **Signing domain** — the secure MCU's secure execution environment holds the **event-signing key**
  (on-device keygen, non-extractable; CAP-01/08), enforces the gate (C-05/§2.1) and content-binding
  (C-G4), maintains the monotonic counter (CAP-02/C-09) and the 1024 consumed-challenge log (D-4/C-10).
- **Identity domain** — a discrete **high-assurance secure element** holds the long-lived
  **device-identity key**, ingests the HSM-root-signed device certificate (CAP-04 / §7-F root model),
  emits the genesis self-signature at provisioning (CAP-03/D-5), and **certifies the signing domain's
  public key**. The record carries both components plus the cross-reference (R-10).

**Rationale — why populated now, and why a discrete EAL6+ part:**
- **Threat model for v1 is seized-device.** This product's buyers (hostile-environment journalists,
  chain-of-custody evidence, election/government) are precisely the population whose devices get
  physically captured. If a captured unit's identity key can be extracted, an adversary mints forged
  "genuine ZKNOT device" attestations and the "can't be faked" promise collapses against the exact
  adversary the market faces.
- **Assurance division (state plainly; do not conflate):** the secure-MCU enclave provides
  PSA Level-3 — "basic physical resistance" — adequate for the event-signing key against host/firmware
  and board-level attack, **but not** determined lab-grade key extraction. The **identity** key — the
  one whose extraction breaks the whole trust chain — is therefore held in a **CC EAL6+** discrete SE
  built to resist physical key extraction. The division *is* the point of split-domain.
- **Forge-needs-both / PAT-011.** One enclave compromise yields at most half a forgery; a complete
  attestation requires breaking both domains.

**Revisit trigger.** If the chosen mechanism ever makes two physical domains impractical, fall back to
logical separation within one secure domain (record format unchanged) — but only with an explicit,
honest downgrade of the seized-device custody claim.

---

## 5. v1 silicon determination

> The SIG family previously excluded part numbers by design; this addendum is the silicon-binding
> layer. Every part below is selected against the resolved requirements above and the spec's CAP-list.

### 5.1 Secure microcontroller — **STM32U585**

Selected because it satisfies every resolved requirement and is, in ST's own positioning, built for
this exact architecture:

- **Content-binding filter (C-G4):** TrustZone + GTZC → secure-owned display bus + secure GPIO. ✓ (verified)
- **Assurance baseline:** **PSA Certified Level-3 / SESIP3, in production** — passed logical, board,
  and basic-physical-resistance evaluation (ST, verified 2026-06-08). ✓
- **Fit:** ST markets the U585 to *consolidate* "keyboard, display, and USB connection" with secure
  functions in one secure MCU (PCI-PTS payment-terminal positioning) — i.e., ST's marketed use case
  *is* secure-MCU-owns-display+USB+signing. ✓
- **Capabilities:** USB; hardware crypto accelerators; on-device secure key storage; secure boot;
  secure firmware install/update; anti-tamper with perturbation-driven secret-erase; measured-boot
  capable (R-11 firmware_hash meaningful when enabled). ✓
- **Ecosystem:** incumbent STM32 toolchain — no ecosystem switch.
- **Pairing:** sits in ST's STM32Trust framework, whose reference pattern is secure-MCU **+ a
  CC-certified secure element** — i.e., B-split exactly.

**Part-number caution:** the PSA L3 / SESIP3 certification attaches specifically to **STM32U585**.
If a different U5 variant is chosen for pinout/memory, the security claim does **not** automatically
transfer — pick the certified part if the claim is to hold.

**U585 vs STM32H573 (the one hinge):** H573 offers more compute headroom (~250 MHz vs ~160 MHz) and
also has TrustZone/GTZC/PSA-L3. The v1 workload (FSM + one P-256 sign + OLED text) does not need the
MHz, Air is a *separate* board (no QR-decode load here), and U585's certification maturity + security
positioning + lower power win. **Flip to H573 only** if heavy on-device graphics or significant added
compute lands on this same board later.

**Non-STM32 considered:** SiLabs Secure Vault, NXP LPC55Sxx — declined. They would cost an ecosystem
switch for no gain, because the high-assurance custody is the discrete Identity SE's job, not the
MCU's; the MCU needs TrustZone + securable display + USB + PSA-L3 + secure boot, all of which U585 has.

### 5.2 Identity secure element — **OPTIGA Trust M (CC EAL6+)**

- Lead part: **Infineon OPTIGA Trust M**, CC EAL6+, on-die P-256/P-384 keygen (non-extractable),
  monotonic counters, X.509 / PKI cert ingestion, USON-10 3×3 mm (fits the potted bottom side).
  *(Re-confirm against Infineon datasheet/cert listing before any federal-facing custody claim — §8.)*
- In-ecosystem alternative: ST **STSAFE-A** (keeps everything ST/STM32Trust). **Verify exact EAL
  level before treating as equivalent** — believed EAL5+ for A110, i.e., below the OPTIGA; if EAL6+
  is the bar, OPTIGA leads.
- Eligibility line (resolved §7-A): the Identity SE MUST provide CC **EAL6+** (or stated-and-accepted
  lower with an honest custody claim), on-die non-extractable keygen, ≥1 monotonic counter,
  external CA-signed cert ingestion, and a genesis self-signature at provisioning (CAP-01/02/03/04).

### 5.3 Root / certification

- **Two-tier root:** YubiHSM holds the civilian root + attestation authority; it signs the device
  certificate into the Identity SE; device SEs are per-unit field identities under that root.
- **v1 = civilian, non-FIPS.** Do not pick parts that block a future FIPS sibling; **do not claim
  FIPS** anywhere without checking live NIST CMVP (the 140-2 path sunset 2026-05-02; 140-3 pending).
- Civilian and any future federal roots are **separate anchors, separately generated** — never bridged.

---

## 6. §7-A / CAP eligibility — resolved values

| Item (was open in SIG-SPEC-ZKKEY-002) | Resolved value |
|---|---|
| Strong-form gate realization (CAP-05) | Option B — secure-domain enclave; gate enforced below replaceable firmware; **+ C-G4 secure-domain display ownership**. |
| Signing element | Secure-MCU secure execution domain (STM32U585), P-256 device signing, `algorithm_id` reserves PQ (R-03). |
| Identity element eligibility | CC EAL6+ discrete SE (OPTIGA Trust M lead), on-die keygen, monotonic counter, X.509 ingestion, genesis self-sign. |
| Display (CAP-15) | Connect renders legible short-code/hash **text** (no QR), driven from the **secure domain** (C-G4). Air QR remains the separate Air board. |
| Boot | Secure + measured boot enabled; debug locked; anti-rollback (firmware/secure-config pass). |
| Transport | USB (Connect / ZK-K), full-speed sufficient for challenge-in / artifact-out. |

---

## 7. Record-schema refinement (proposed R-13 / R-14)

The provisional's single ordinal `assurance_profile` (0–5) conflates two orthogonal properties
(§0). Replace/augment with **two explicit fields** so a verifier reasons about each:

- **R-13 — `presence_binding_type`** — how presence was enforced (e.g., secure-domain, hardware-interlock).
- **R-14 — `content_binding_type`** — whether the signed artifact was bound to what the human was
  shown (e.g., secure-domain display, none/firmware-trust).

Keep both compact (string/enum tokens) — the Air QR ceiling (§4 Air constraint) still applies. Folds
into the §4 record format at SIG-SPEC-ZKKEY-003.

---

## 8. Patent & federal flags

- **This is the structure the strong-form claim discloses.** Best mode for the non-provisional =
  the as-built Option B on **STM32U585 + OPTIGA Trust M**, with **secure-domain display ownership
  (C-G4)** as the element that makes content-binding **enabling**. Keep as-built and as-disclosed matched.
- **PAT-020** (strong-form provisional) is drafted and ready to file; filing opens the strong-form
  priority chain. Attorney engagement target 2026-07-01; PAT-001 non-provisional deadline 2027-01-15.
- **Patent-gated content:** keep display-then-confirm firmware and any public/free-build content or
  video narration out of circulation until the non-provisional is filed (carry from SIG-SPEC-002 §9).
- **Verify-before-claim (any federal-facing artifact — re-verify against primary sources):**
  1. PSA L3 / SESIP3 attaches to **STM32U585** specifically (not the whole U5 family).
  2. OPTIGA Trust M **EAL6+ and on-die keygen** — confirm against Infineon datasheet/cert listing.
  3. STSAFE-A exact **EAL level** before treating as an OPTIGA equivalent.
  4. **FIPS:** do not claim; check live NIST CMVP.
  5. Naming/terminology bound for a capability statement or proposal — verify; do not propagate from this doc.

---

## 9. Edits to fold into SIG-SPEC-ZKKEY-003

1. §2.3 — mark the open mechanism **resolved: Option B**; move the A/A′/B table to "considered."
2. §2.1 — add **C-G4** (secure-domain display & actuation ownership) as a MUST.
3. §2.4 / D-1 — record realization = **split-domain, populated v1** (secure-MCU signing + discrete EAL6+ Identity SE).
4. §1 locked-params — add a **silicon row** (U585 + OPTIGA Trust M) — first part numbers in the SIG family.
5. CAP-05 — realization = B + C-G4; CAP-15 — Connect display driven from secure domain.
6. §4 record format — add **R-13 `presence_binding_type`**, **R-14 `content_binding_type`**.
7. §10 — **close** the open item; next open decision = firmware/secure-config enforcement pass (#3).

---

## 10. Changelog

| Version | Date | Change |
|---------|------|--------|
| SIG-SPEC-002-ADD-001 | 2026-06-08 | Resolves SIG-SPEC-ZKKEY-002 §2.3/§2.4/§10. Mechanism = **B** (collapsed secure-MCU enclave); adds **C-G4** secure-domain display ownership; D-1 realization = **split-domain populated v1**; binds v1 silicon (**STM32U585 + OPTIGA Trust M EAL6+**) under the two-tier YubiHSM root; proposes record fields R-13/R-14. ST GTZC + U585 PSA-L3 facts verified against ST primary sources 2026-06-08. |

---

*Format note: this matches the SIG `.md` family (front-matter + ADR + changelog), which is unpaginated;
on export to PDF for any formal or federal-facing use, apply "Page X of Y" footer numbering per ZKNOT
document standard. Provenance: determinations trace to SIG-SPEC-ZKKEY-002, PAT-001-ADD-001, and filed
provisionals; silicon facts verified against ST primary sources (and Infineon, to be re-confirmed per §8).*
