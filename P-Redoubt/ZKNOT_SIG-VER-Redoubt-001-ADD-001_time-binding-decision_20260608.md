---
title: Time-Binding & Log-Anchoring Decision (resolves SIG-VER-001 §7)
doc_id: SIG-VER-ZKKEY-001-ADD-001
status: DECISION — to be folded into SIG-VER-ZKKEY-001 v0.2 and SIG-SPEC-ZKKEY-005 v6
parent: SIG-VER-ZKKEY-001 (verifyknot verifier spec)
author: William Shane Wilkinson (ZKNOT, INC.)
date: 2026-06-08
classification: ZKNOT INTERNAL — patent-sensitive
---

# Time-Binding & Log-Anchoring Decision

## 1. Decision

The trusted "when" for an attestation — needed for Redoubt's signing-key validity-window and revocation checks (VER-18) — is established by an **externally-anchored LocalChain transparency log whose checkpoints are timestamped by RFC-3161 Timestamp Authorities (TSAs)**. Three tiers, strongest to weakest, with the verifier always declaring which it used (VER-30):

| Tier | Anchor | Time bound | Needs |
|------|--------|------------|-------|
| **Upgrade** | RFC-3161 TST bound into the record **at signing** (Lever A) | "signed ≤ T_tst" | connectivity at signing |
| **Primary** | Event logged into the **TSA-anchored transparency log** | "logged ≤ T_checkpoint" | connectivity at registry only |
| **Degraded** | Device-asserted time only (no external anchor) | none — **Redoubt protection NOT asserted** | — |

Rationale: once the signing key is extracted, every field that key signs (including any timestamp) is attacker-controlled, so the anchor must be external. The primary tier needs connectivity only at *the registry* (which ZKNOT always has), not at the field device (which the journalist/evidentiary buyer often lacks) — and it reuses ZK-LocalChain, which is already in production. RFC-3161 is the pragmatic, standard, low-ops anchor; a public-chain anchor remains available as a later neutrality upgrade.

## 2. What to build — LocalChain → TSA-anchored transparency log

Evolve ZK-LocalChain (already append-only, hash-chained) into a transparency log:

- **TL-01 (MUST)** Append-only, hash-chained entries (have it). Add a **Merkle tree** over entries so single events get compact inclusion proofs.
- **TL-02 (MUST)** Emit **checkpoints** (signed tree head) at a fixed cadence (per-N entries or per-T interval — §6).
- **TL-03 (MUST)** Each checkpoint root MUST be timestamped by **≥ 2 independent RFC-3161 TSAs**; store the resulting TSTs with the checkpoint. (≥2 so one TSA being unavailable or later distrusted doesn't sink the anchor, and for legal robustness.)
- **TL-04 (MUST)** Checkpoints + TSTs are signed under the **YubiHSM root** and **published** (fetchable / carryable), so verifiers obtain them without trusting ZKNOT's bare word — the TST is the neutral anchor; the HSM-root signature binds it to the chain.
- **TL-05 (MUST)** Provide **Merkle inclusion proofs** (audit paths) so an event proves its position between two checkpoints without the whole log.
- **TL-06 (MUST)** **Revocation is itself a logged, ordered entry** (revocation statement, HSM-root-signed), so its position in time is anchored the same way as events.
- **TL-07 (SHOULD)** Keep the RFC-3161 TSA list and checkpoint cadence as configuration, not hardcoded — they will change.

## 3. The verifier rule (concretizes VER-18 / VER-30)

For a Redoubt record, establish the event's **upper-bound log time** `T_ub` = the TSA time of the **first checkpoint that includes the event** (proven via inclusion proof). Then:

- **VER-18′ (MUST, fail-closed)** Accept the window/revocation check only if `T_ub ≤ signing_key_cert.notAfter` **AND** (`no revocation` **OR** `T_ub < revocation_time`). Otherwise reject. Using the *upper* bound makes it backdating-resistant: the attacker cannot make the inclusion-checkpoint's TSA time earlier than the real append time, so a post-expiry/post-revocation forgery cannot be made to look in-window.
- **VER-18″ (MUST)** If a **signing-time TST** (Lever A) is present, use `T_tst` as a stronger, signing-time bound in place of `T_ub`.
- **VER-30′ (MUST)** The verdict states the basis: `signing-time TSA token` / `log-anchored (checkpoint TSA, logged ≤ T_ub)` / `device-asserted only — Redoubt window & revocation NOT enforceable`. Never present a degraded-tier record as Redoubt-protected.

## 4. Offline bundle additions (extends VER-31)

A bundle for a log-anchored record MUST additionally carry: the event's **Merkle inclusion proof**, the **including checkpoint + its RFC-3161 TST(s)**, and the **revocation entry/snapshot**. The verifier reproduces `T_ub` and the VER-18′ test fully offline (it needs the TSA certs out-of-band, like the HSM root).

## 5. The guarantee, stated honestly

- Cert **expiry** bounds the blast radius even with no detection; **revocation** shortens it on detection; **log-time** supplies the un-backdatable "when."
- **Irreducible limit:** forgeries an attacker produces between key extraction and compromise detection, logged before the revocation entry and within the cert window, still pass — you cannot revoke before you detect. Short rotation windows bound this; the verifier must not pretend otherwise.
- **Offline-standalone** records (never logged, no signing-time TST) get only "cert not expired by the verifier's own clock + not in the held revocation snapshot" — weaker; the verifier says so.
- **Trust note:** the anchor is "as neutral as the TSAs." ≥2 independent TSAs reduce single-point trust; a public-chain / OpenTimestamps anchor can be layered on later for maximal neutrality without changing the model.

## 6. Deferred sub-decisions

1. **Which TSAs** (≥2 reputable; consider different jurisdictions for evidentiary robustness).
2. **Checkpoint cadence** (per-N entries vs per-T minutes) — trades proof freshness vs TSA call volume.
3. **Rotation cadence** (still open from the Redoubt decision: time / count / on-demand) — interacts with checkpoint cadence.
4. Whether to add a **public-chain anchor** later as a neutrality upgrade.

## 7. Ripple edits (carry-list)

- **SIG-VER-001 → v0.2:** fold §1–5 in; resolve §7; concretize VER-18/30; expand §8 bundle; close open item #1.
- **SIG-SPEC-005 → v6:** add optional `tsa_token` field (signing-time, Lever A) to the record; redefine LocalChain as the externally-anchored transparency log; reference inclusion-proof carriage. (Folds with the already-queued v6 edits: §11 residual + WitnessMark/Redoubt line shape.)
- **SIG-FW-001 (Redoubt section, when written):** device SHOULD bind a signing-time TST when connectivity exists; otherwise emit log-ready records (already does via `prior_event_hash`).
- **ZK-LocalChain backend (real work on api.zknot.io):** Merkle tree + checkpoints + ≥2 RFC-3161 TSA timestamping + publish + inclusion-proof API + revocation-as-logged-entry (TL-01..07).

## 8. Patent flag

The combination — human-presence-gated attestation events, ordered in an externally-TSA-anchored transparency log, with short-lived rotating keys for bounded-blast-radius revocation — may be novel in combination beyond PAT-004 (LocalChain) and PAT-006 (offline). **Flag for the attorney as a possible continuation / new provisional** (candidate "PAT-021"); keep the as-built method matched to whatever is disclosed. Do not publicly narrate the rotating-key + TSA-anchored-revocation method before that filing decision.

## 9. Changelog

| Version | Date | Change |
|---------|------|--------|
| ADD-001 | 2026-06-08 | Time basis decided: RFC-3161 TSA-anchored LocalChain transparency log (primary) + optional signing-time TST (upgrade) + honest degradation. Concretizes VER-18/30; defines TL-01..07; resolves SIG-VER-001 §7. |

*Resolves the open item in SIG-VER-ZKKEY-001 §7. To be folded into SIG-VER-001 v0.2 and SIG-SPEC-005 v6. Honest-translation discipline preserved: the verifier states its time basis and never claims more than the anchor supports.*
