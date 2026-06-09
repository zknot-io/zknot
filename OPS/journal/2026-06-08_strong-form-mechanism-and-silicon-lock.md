---
title: Strong-form mechanism & v1 silicon lock; PAT-020 fileable; rename explored
date: 2026-06-08
author: William Shane Wilkinson (ZKNOT, INC.)
type: daily journal
classification: ZKNOT INTERNAL — patent-sensitive
related:
  - SIG-SPEC-ZKKEY-004 (now canonical)
  - SIG-SPEC-ZKKEY-002-ADD-001 (decision record — now absorbed into v4; mark superseded)
  - PAT-020 strong-form provisional (drafted, filing-ready, NOT yet filed)
  - DOC-001 patent tracker (PAT-020 row added)
  - ZKKey rename naming brief
tags: [zkkey, hardware, patent, pat-020, silicon, stm32u585, optiga, naming]
---

# 2026-06-08 — Strong-form mechanism & v1 silicon lock

## TL;DR

Closed the central hardware question for the flagship: mechanism = **B (secure-MCU enclave)**,
domain model = **split-domain populated (AP-4)**, v1 silicon spine = **STM32U585 + OPTIGA Trust M
(EAL6+)**. Folded into a clean canonical spec, **SIG-SPEC-ZKKEY-004**. Drafted a filing-ready
strong-form provisional (**PAT-020**) with figures and added it to the tracker. Explored renaming
"ZKKey" — no winner yet; the **"-mark" lane (Witnessmark / PersonMark)** survives, naming still open.
Surfaced the real residual: the **signing key stays at PSA-L3** even in B-split — content-binding and
EAL6+ signing-custody are in genuine tension, logged as the open seizure residual.

## Decisions (durable)

- **Mechanism = B (collapsed secure-MCU enclave).** The secure domain owns the signing key + display
  + button. Chosen over A′ (hardware interlock) because only B gives **content-binding** (proof the
  human approved *this exact* artifact), which is the moat. A′ proves presence but not content.
- **Domain model = split-domain, populated in v1 (AP-4).** Discrete EAL6+ identity SE certifies the
  enclave's signing key under the YubiHSM root; forging a complete attestation needs **both** domains.
- **v1 silicon spine LOCKED:** **STM32U585** secure MCU (enclave) + **Infineon OPTIGA Trust M (EAL6+)**
  identity SE, under the two-tier YubiHSM root. v1 = civilian, **non-FIPS**.
- **C-G4 (firmware MUST):** secure partition owns the OLED interface (GTZC-secured bus + pins);
  value shown == value signed. (Verified realizable on U585 via GTZC/TZSC against ST app notes.)
- **Assurance division is honest and explicit:** signing key = PSA-L3 (enclave); identity key =
  EAL6+ (OPTIGA). Do **not** imply the signing key is EAL6+/tamper-proof.
- **Canonical spec advanced to SIG-SPEC-ZKKEY-004** (supersedes the v2/v3 chain).
- **PAT-020** assigned in the tracker (ZKM-P020, short name "StrongFormGate"), provisional drafted
  and filing-ready. *Not yet filed.*
- **Product rename: NOT decided.** Leading territory is compound "-mark" names (Witnessmark,
  PersonMark). Ruled out: Knotary, Vouchsafe, Signet, Avow, Countersign, TrueSign, the reality/meta/key
  lanes.

## What happened (arc)

Started from the PAT-001 enablement finding (firmware-mediated gate can't deliver "physically
impossible"). Built the strong-form provisional as a clean filing (PAT-020), verified the USPTO
mechanics, updated the tracker. Detoured into renaming the flagship for the professional market —
learned the identity/attestation namespace is heavily owned, so the winnable path is a distinctive
compound, not a dictionary word. Then ran the hardware decision chain: B-split vs B-pure → B-split;
A/A′/B → B (on the presence-vs-content-binding reframe); custody → split-domain populated with an
EAL6+ identity SE; MCU → U585 (verified GTZC can put the display + button in the secure world, PSA-L3
in production, USB, incumbent toolchain). Wrote the decision record; folded it (and more) into v4.
v4 then caught the sharpest point of the day — see residual #1.

## Open items / residuals

1. **Signing-enclave assurance (the real seizure residual, SIG-SPEC-004 §11.1).** B-split anchors
   *identity* at EAL6+ but the catastrophic *signing* key stays at PSA-L3. Content-binding forces the
   signing key into the display-owning enclave; EAL6+ custody needs a discrete SE that can't own the
   display — **no current chip gives both.** Decision pending: is lab-grade signing-key extraction in
   v1's threat model? If yes, the levers (which preserve content-binding) are **rotating/short-lived
   signing keys + HSM-root revocation** and **tamper-responsive potting → secret-erase (PAT-018)** —
   *not* a different MCU. This feeds gate #3.
2. **Device naming** — run a Class 9 + 42 trademark knockout + domain/handle check on the chosen
   "-mark" candidate before adopting. v4 still carries "ZKKey" as a placeholder.
3. **Verify-before-claim:** pin the exact **STM32U585** part for the cert; confirm package USB at BOM;
   confirm OPTIGA Trust M EAL6+ + on-die keygen vs Infineon datasheet; confirm STSAFE-A EAL level.
4. **Record schema:** ordinal `assurance_profile` (R-13) still reads as a ladder; decide the verifier
   keys off the typed fields (R-14/R-15) and consider a typed `content_binding_type`.
5. **Best-mode citations:** pin exact PAT-020 embodiment refs (Third Embodiment §5 / Example C §15 =
   secure-MCU; Fourth Embodiment §6 / Example D §16 = split-domain) before the non-provisional.

## Backup / version-control status (action needed)

Everything created today lives **only in the outputs folder** — not yet in the vault or git:
- PAT-020 provisional PDF → `01_PATENTS/FILED/PAT-020/`
- Updated tracker (DOC-001) → wherever DOC-001 lives
- Decision record SIG-SPEC-002-ADD-001 + the naming brief → `6_SIG/` and `7_ENG/` respectively
- This journal → `3_OPS/journal/`
Commit these under git. Vault reorg is mid-flight — add paths explicitly; **no destructive `git clean`
until the reorg commits.** When PAT-020 is filed, archive the **USPTO receipt** (the priority-date
proof) in `01_PATENTS/FILED/PAT-020/` first. Also: mark **SIG-SPEC-002-ADD-001 as superseded/absorbed
by v4** and add a pointer in any lingering v2 reference.

## Promote to systems/ (durable facts — keep out of the journal)

- Silicon facts (U585 GTZC secure-peripheral behavior, PSA-L3 scope, USB; OPTIGA EAL6+) already have
  their canonical home in **SIG-SPEC-ZKKEY-004** — reference it, don't re-document.
- The **USPTO provisional filing checklist** ($65 micro; cover sheet PTO/SB/16; micro-entity cert
  PTO/SB/15A; Patent Center; no DOCX surcharge on provisionals) is reusable across filings — worth a
  `km/systems/uspto-provisional-filing.md` so the next filing doesn't re-derive it.

## Next session

- **Gate #3 — secure-config / firmware-enforcement spec:** secure boot chain, debug-lock provisioning,
  anti-rollback, GTZC config for OLED + button, key injection + OPTIGA cross-cert under the HSM root,
  measured-firmware → device cert. This is where residual #1's mitigations (rotation, secret-erase,
  tamper response) get specified, and where B's real schedule risk lives.
- **File PAT-020** (SB/16 + SB/15A + $65 via Patent Center); archive the receipt.
