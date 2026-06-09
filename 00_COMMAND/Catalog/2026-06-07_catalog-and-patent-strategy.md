---
date: 2026-06-07
topic: catalog-and-patent-strategy
tags: [patents, catalog, shopify, platform, sdvosb, gap-003]
workstream: [biz, ip, hw]
status: complete
---

# TL;DR

Reconciled the full product catalog against the authoritative patent tracker (DOC-001). Outcome: the entire catalog is already backed by filed provisionals — list freely, no defensive filing needed before public listing. Corrected the portfolio count to **18 filed (not 19)**. Drafted a new provisional for the one real gap (multi-party witness / GAP-003), ready to file. Locked storefront build order and dispositions. Surfaced the governing strategic fact: everything is one **30×90 core module + carriers**, so the flagship build funds every later build.

# Decisions

- **Portfolio count is 18 filed provisionals, 0 unfiled, 1 TM pending.** Use 18 on all federal/marketing artifacts. (PAT-014 folded into PAT-015; PAT-017 never existed — skipped number.)
- **Catalog is fully patent-covered → list everything freely.** Only a genuinely new SKU or an unclaimed gap-turned-product requires "file a provisional first" (on-sale bar).
- **GAP-003 (multi-party witness) → file it.** Provisional drafted broad (M-of-N + unanimous, simultaneous + sequential, co-located + distributed; two-person-integrity anchor). Pending: assign internal number (020 or reuse 017), confirm contact block, eyeball SB/15A boilerplate.
- **GAP-001 (verification protocol)** = attorney call. **GAP-002 (CC-line)** = treat as absorbed by PAT-018; close.
- **Build order locked:** 1) ZKKey Connect, 2) TrustSeal, 3) ZKKey Air, 4) PowerVerify Attested. Drone after ZKKey, internal.
- **TrustSeal is #2 because it's off the PCB critical path** — a seal, not a module — so it banks recurring revenue in parallel with the platform work.
- **SelfKnot → zknot.org only, benched** until ZKKey Connect + Air ship. Field builds/self-attests follow; meaningless without a paying product first.
- **Drone (PAT-012/013) stays internal.** Not listed publicly. Built as a carrier of the ZKKey core.
- **Storefront uses price + lead time** (proposed anchors set; PV-C $39 confirmed, rest to finalize).
- **Add an SDVOSB Teaming/Capabilities surface** signaling willingness to partner/merge — for primes needing an SDVOSB and for acquirers (12-month acquisition-readiness target).
- **Services are a confirmed development priority** (provisioning-as-a-service, verification authority/HashStamp, consulting, licensing).

# Durable facts to promote (→ systems docs)

- **30×90 core-module-and-carriers architecture.** ZKKey Connect = the core module; ZKKey Air, PV-Attested, and the drone build are carrier variants reusing it. → create `3_OPS/km/systems/hardware-platform.md`.
- **EvidenceProtocol (63/961,116)** is a filed patent that was missing from the DOC-003 summary; it strengthens the OfflineEvidence kit + verification service. → reflect in patent systems notes.

# Open items / next actions

- [ ] File GAP-003 provisional (assign number, confirm contact block + SB/15A).
- [ ] Confirm EvidenceProtocol (63/961,116) SB/15A / micro-entity status in TSDR — single-submission risk; strongest *protocol* claim could lapse if defective.
- [ ] Finalize proposed prices on ZKKey Connect / Air / PV-A / TrustSeal.
- [ ] Stand up the Teaming & Capabilities surface (SDVOSB + 18 patents + single core platform).
- [ ] Build `hardware-platform.md` systems doc for the 30×90 core module.
- [ ] Commit catalog docs + this entry deliberately — vault git mid-reorg; do NOT run `git clean -fd`.

# Artifacts produced

- `5_PLANS/` PLAN-CATALOG-001 — product catalog from patents
- `01_PATENTS/` STR-003 — catalog ↔ tracker reconciliation
- catalog status addendum (FINAL)
- `ZKNOT_PAT-XXX_MultiPartyWitness_provisional_spec_20260607.docx` — GAP-003, ready to file
