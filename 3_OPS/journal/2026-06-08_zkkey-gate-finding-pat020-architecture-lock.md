---
date: 2026-06-08
topic: ZKKey gate finding, PAT-020, and v1 architecture lock (B-split / U585 / OPTIGA)
tags: [zkkey, sig, patents, pat-020, hardware-selection, decisions, b-split, stm32u585, optiga]
status: complete
related:
  - SIG-SPEC-ZKKEY-005 (canonical spec, HW+SW reconciled)
  - SIG-SPEC-ZKKEY-002-ADD-001 (hardware decision record, folded into v5)
  - PAT-001-ADD-001 (gate-enforcement finding & decision addendum)
  - PAT-020 (strong-form gate provisional, dated 2026-06-08)
  - PAT-001 (provisional 63/960,933 + non-prov draft + Master Guide Vol.1–2)
  - PAT-011 (dual-SE / split-domain)
superseded_docs: SIG-REQ-ZKKEY-001, SIG-DEC-ZKKEY-001, SIG-SPEC-ZKKEY-002, -003, -004, SPEC-002-ADD-001
---

# 2026-06-08 — ZKKey gate finding, PAT-020, and v1 architecture lock

## TL;DR

Started the day deriving ZKKey software requirements from the patents; ended it with the entire v1
architecture and silicon spine locked, a new provisional (PAT-020) covering the fix, and hardware +
software reconciled into one canonical spec. The pivotal event: discovered the PAT-001 non-provisional
overclaims — it calls the gate "physically impossible" while the disclosed architecture is
firmware-mediated on a blind ATECC, which is the exact weakness used to distinguish FIDO2. Fixed it by
moving the flagship to a real strong-form gate (secure-MCU enclave, mechanism B), filing PAT-020 to
cover all buildable strong-form mechanisms, and selecting STM32U585 + OPTIGA Trust M (EAL6+) as a
split-domain build. Naming still unresolved.

## Decisions (canonical — full detail in SIG-SPEC-ZKKEY-005)

- **Gate finding (the hinge):** PAT-001's "physically incapable / physically impossible" language is,
  on the disclosed button→MCU→I²C-Sign architecture, a firmware policy on a blind ATECC — not a
  hardware guarantee. Same software-fakeability it uses to distinguish FIDO2. §112 exposure + IPR
  gift. Captured in PAT-001-ADD-001 for the attorney.
- **Patent strategy = layered, not retreat:** keep the broad firmware-mediated claim (Jan-2026
  priority, reads on competitors); add a strong-form independent claim; scope "physically impossible"
  to the strong-form embodiment only. Product goes strong-form-only; the firmware-mediated mechanism
  stays in the patent as breadth. Do NOT surrender the broad claim.
- **PAT-020 filed (2026-06-08):** strong-form gate across all buildable mechanisms (interlock /
  secure-MCU / split-domain / fixture) + assurance taxonomy. This is new matter → its own June-2026
  priority. Confirmed from the uploaded provisional + supplemental that the strong-form gate is in
  neither → the later priority is correct.
- **Mechanism = B (collapsed secure-MCU enclave).** Chosen over A′ (hardware interlock) because the
  moat is *content-binding* (human approved THIS artifact), and only a secure domain owning both the
  display and the key can guarantee it. A′ gives stronger presence-binding but weakest content-binding.
- **Domain model = split-domain, populated v1.** Signing key in the enclave (PSA-L3); identity key in
  a discrete EAL6+ SE that certifies the signing key under the YubiHSM root. Forge-needs-both.
- **Silicon spine LOCKED:** STM32U585 enclave (owns signing key + OLED + button + USB; GTZC binds
  display + button to the secure world → content-binding is real) + Infineon OPTIGA Trust M (EAL6+)
  identity SE. U585 over H573 (MHz unneeded). Non-STM32 declined (ecosystem switch for no gain).
- **Record schema:** replaced the single ordinal `assurance_profile` with two explicit fields —
  `presence_binding_type` + `content_binding_type` — so a verifier reasons about each independently.
- **HW + SW reconciled** into SIG-SPEC-ZKKEY-005 (single source of truth); v4 and the hardware
  decision record (SPEC-002-ADD-001) superseded.

## Why these landed where they did (the reasoning, not the what)

- The decision that drove everything: **the asset is the claim, not the chip.** Dropping the ATECC
  cost nothing on the patent side (broad claim is chip-agnostic) and the ATECC was actively making the
  headline "software-unfakeable" claim false. Engineering instinct and patent strategy were the same
  decision.
- **Cost-is-not-a-gate (D-0)** reframed every hardware call from "include it?" to "design it into the
  board, populate per run." Potting makes population permanent per build run, not retrofittable per unit.
- **Presence-binding vs content-binding are orthogonal, not a ladder.** This is the single most
  load-bearing concept of the day — it's why B beat the higher-"profile" A′, and why the record now
  carries two fields instead of one number.
- **The honesty discipline held throughout:** B is immutable-firmware-enforced, not silicon-impossible;
  EAL6+ protects identity, not the signing key (which stays PSA-L3). Stated plainly so the claims and
  marketing can't drift past the parts.

## Open items / next steps

- **Signing-enclave assurance is the real seizure residual** — B-split anchors identity at EAL6+ but
  leaves the signing key at PSA-L3. NOT closed by B-split. Track it; it's a bigger decision than the
  identity SE if the threat model ever includes lab-grade signing-key extraction.
- **Verify-before-claim:** STSAFE EAL level vs OPTIGA; exact U585 part number for the PSA-L3 cert;
  U585 package USB at BOM; OPTIGA EAL6+ + on-die keygen against Infineon's listing.
- **Device naming unresolved** — "ZKKey/ZKey" out (.zkey collision, weak mark). Knockout-killed this
  session: Signet, Cachet, Proofmark, Vouch, Cairn, Bulla; Attestor too generic. Leaning toward a
  plain-English compound (RealSeal / PresenceSeal / LiveProof style) + a fixed descriptor doing the
  YubiKey contrast. Still thinking. Run knockout searches before adopting anything.
- **Next gate (#3): firmware / secure-config enforcement spec** — secure boot chain, debug-lock
  provisioning, anti-rollback, GTZC config binding OLED + button to the secure world, secure-partition
  display driver + framebuffer, key injection + OPTIGA cross-certification under the HSM root,
  measured-firmware → device cert.
- **Patent calendar:** attorney engagement target 2026-07-01; PAT-001 non-prov deadline 2027-01-15;
  reconcile PAT-001 language with PAT-020's Profile-1 framing before filing.

## Version-control status

NOT backed up until committed. To file/commit today's outputs:
- 01_PATENTS/ : ZKNOT_PAT-001-ADD-001 (addendum), PAT-020 provisional PDF, and the pre-filing source
  docs (non-prov draft + Master Guide Vol.1–2) — priority analysis depends on these being in the tree.
- 6_SIG/firmware/ : SIG-SPEC-ZKKEY-005 (canonical). Mark v2/v3/v4 and SPEC-002-ADD-001 superseded;
  add `superseded_by: SIG-SPEC-ZKKEY-005` to the hardware addendum front-matter.
- 3_OPS/journal/ : this entry.
- Vault reorg still mid-flight (~337 files appear deleted) — add paths explicitly; do NOT run
  git clean -fd until the reorg is committed.
- Outstanding authoritative pull: as-filed PAT-001 provisional 63/960,933 + Jan-22 supplemental and
  the PAT-020 filing receipt from USPTO Patent Center.
