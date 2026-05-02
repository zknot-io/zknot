# PAT-019 — Pending Decision: Optical PUF + Ledger Integration

**Internal ID:** PAT-019
**ZKM ID:** (unassigned — pending filing)
**Short Name:** OpticalPUF
**Proposed Title:** Field-Verifiable Optical Physical Unclonable Function With Cryptographic Ledger Binding for Hardware Attestation Devices
**Category:** Hardware / Software Integration
**Status:** NOT FILED — decision pending experiment results
**Date Opened:** April 24, 2026
**Decision Deadline:** Re-evaluate by July 31, 2026 (or upon experiment completion, whichever first)

Page 1 of 3

---

## Core Claim Concept

A method and system for binding a physical optical fingerprint of a device (produced by random particle distribution in a transparent potting compound) to a cryptographically attested, vendor-irrevocable, offline-verifiable ledger entry, such that field verification of device integrity requires only visual comparison against a ledger-resolved reference image, and such that the potting compound simultaneously serves as both the optical PUF substrate and the physical tamper barrier.

## Why This Might Be Novel

The Physical Unclonable Function concept is well-established (Pappu et al. 2002; dozens of patents). What is **potentially** novel here is the specific combination:

1. **Dual-SE signed PUF record** (per PAT-011 architecture) — not just any signature, but the ZKNOT two-SE separation model
2. **Offline verifiability** (per PAT-006) — reference image cached or shipped with device, no network required for verification
3. **Vendor-irrevocable binding** (per PAT-005) — manufacturer cannot retroactively alter the PUF record
4. **Dual-function potting** — single material layer serves as PUF substrate AND tamper barrier (PAT-018 multi-layer)
5. **Field verification via consumer device** (phone camera) — not specialized PUF reader hardware

The longer this combination is maintained as a required element set, the stronger the claim's survivability. Any one or two elements alone is prior-art-reachable.

## Why It Is Deferred

Filed provisionals sit at 16. Conversion costs already committed exceed $18K over the next 12 months. Core product revenue (PowerVerify, ZKey) is not yet generating. A peripheral integration patent at this stage dilutes attention without strengthening the acquirer story meaningfully.

Experimental validity is also unproven — §5 below lists the gating test.

---

## Gating Condition for Filing

**Experiment must pass all four criteria in ZKNOT_DOC-003_PAT-019_optical_puf_experiment_20260424.md §2.**

If experiment passes: proceed to provisional ($65) within 30 days.
If experiment fails any criterion: abandon or substantially redesign concept. Do not file.
If experiment not run by July 31, 2026: defensive-publish only (see §7).

Page 2 of 3

---

## Position in Portfolio

```
PAT-002 PowerVerify ──┐
PAT-018 PowerVerifyPlus ──┼─── PAT-019 cites as base
PAT-003 TrustSeal ──┤
PAT-004 ZK-LocalChain ──┤
PAT-011 DualSE ──┘
```

PAT-019 is an integration patent, not a standalone hardware claim. It depends on the supporting architecture being valid. This is a strength (harder to invalidate without invalidating four other patents) and a weakness (worthless as a standalone asset).

---

## Paths Forward

### Path A: Provisional after experiment passes
- Cost: $65 immediate + ~$3,000 conversion in 12 months
- Pro: Priority date, future non-prov optionality, asset in acquisition deal
- Con: Another conversion obligation on top of 16 existing

### Path B: Defensive publication only
- Cost: $0
- Pro: Prevents competitor patenting, zero ongoing commitment
- Con: No offensive claim available to ZKNOT
- **Current default recommendation** absent acquirer signal

### Path C: Wait and watch
- Cost: $0 now, risk of losing priority to competitor filing
- Pro: Cleaner spec possible after more engineering data
- Con: Priority race risk, no defensive coverage in interim

---

## Trigger Events That Change the Decision

File a provisional immediately if any of these occur before experiment completion:

- Named acquirer (Axon, defense prime, L3Harris, etc.) expresses specific interest in physical tamper-evidence integration
- Competitor files or publishes anything in optical-PUF + blockchain/ledger space
- PowerVerifyPlus commercial sale signed with a customer who requires this feature
- External investor or strategic partner asks for optical-PUF coverage in due diligence

Defensive-publish immediately (regardless of experiment status) if:

- Any third party is observed researching optical PUFs for passthrough security devices
- 90 days elapse from this document's creation with no experiment run

---

## Next Actions (Owner: Shane)

- [ ] Complete experiment per DOC-003 protocol
- [ ] Log experiment results in this folder
- [ ] Draft defensive publication (see ZKNOT_PAT-019_OpticalPUF_defensive_publication_20260424.md)
- [ ] Decide Path A / B / C based on experiment results
- [ ] If Path A: add PAT-019 to patent tracker, draft provisional spec, file via USPTO

---

## History Log

| Date | Event | Notes |
|---|---|---|
| 2026-04-24 | Concept documented | PAT-019 placeholder created; experiment protocol drafted; defensive publication drafted |
| _pending_ | Experiment completed | _log results here_ |
| _pending_ | Path decision | _A / B / C + rationale_ |

Page 3 of 3
