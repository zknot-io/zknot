---
title: ZKNOT Product Catalog — Defensible SKUs Mapped to Filed Patents
doc_id: PLAN-CATALOG-001
author: William Shane Wilkinson
created: 2026-06-07
status: working draft
source_of_truth: ZKNOT_DOC-003_ALL_patents_summary_20260604.docx (read in full 2026-06-07)
scope: Internal planning + Shopify roadmap. NOT a federal filing — see "Verification flags" before any gov-facing use.
backup_status: NEW FILE — not yet committed. Vault git is mid-reorg (~337 files showing deleted; do NOT run `git clean -fd`). Commit this deliberately so the reorg does not swallow it.
---

# TL;DR

You can legitimately defend **~12 hardware SKUs across 4 product families** plus a **services/licensing layer** with the currently filed portfolio. But the catalog question and the energy question have different answers:

- **Catalog (what you can list):** 4 families → 12 hardware SKUs + 4 kits/bundles + ~6 services.
- **Energy (what to build next, after ZKKey):** TrustSeal → PowerVerify Attested → CombinedSession kit → OfflineEvidence kit → ZKKey Ultra. Everything else is list-as-roadmap, license, or research-track.
- **Do NOT put on Shopify:** the drone verticals (PAT-012, PAT-013). They are licensing / defense-integration plays and listing them next to a $39 cable costs credibility with both consumer and gov buyers.

# Decisions captured here

1. **List in a Now / Next / Research structure**, not flat. Catches buyers without promising vaporware.
2. **TrustSeal is the highest ROI-to-effort catalog add after ZKKey** — cheap serialized consumable, recurring revenue, pairs with every other product.
3. **Bundles (CombinedSession, OfflineEvidence) are near-zero new build** — they package things you already have or will have. Treat as SKUs, not R&D.
4. **Drone patents → licensing/SBIR track, never a storefront SKU.**
5. **Services are the moat** — provisioning-as-a-service + verification authority deepen the personal monopoly more than any single new device.

---

# 1. Patent → product map (grounded in the filed specs)

Defensibility = how directly a filed claim covers the product. Build effort = realistic solo effort given your existing ATECC/YubiHSM/signing stack.

| Family | SKU | Backing patent(s) | Status of build | Defensibility | Build effort |
|---|---|---|---|---|---|
| **PowerVerify** | PV Core (PV-C, passive) | PAT-002 | **Shipping** | Direct | Done |
| PowerVerify | PV Attested (PV-A, MCU+SE logging/signing) | PAT-002 §8, PAT-018 | Rev after first 50 | Direct | Low–med (reuses ATECC stack) |
| PowerVerify | PV Plus (tamper-evident, sealed secondary verify iface) | PAT-018 | Later | Direct | Med |
| **ZKKey** | ZKKey Connect (ZK-K, USB) | PAT-001, PAT-008, PAT-010 | **Priority build** | Direct (foundational) | Med |
| ZKKey | ZKKey Air (ZK-A, optical, air-gapped) | PAT-009, PAT-001, PAT-008 | Priority+1 | Direct | Med |
| ZKKey | ZKKey Ultra (dual-SE) | PAT-011, PAT-001, PAT-008 | High-assurance / fed | Direct | High (two SEs, bidirectional separation) |
| **TrustSeal** | TrustSeal serialized consumable | PAT-003 | Easy add | Direct | **Very low** (serialize + bind to ledger you run) |
| **USB forensic** | DataGap USB Witness (data-path presence/absence) | PAT-015 (consol. PAT-014) | Niche | Direct on data-path claim | Med (USB2 easy; SuperSpeed tap is the hard part) |
| USB forensic | TrustMeter (current/voltage/impedance anomaly) | PAT-016 | Niche | Direct | High (impedance forensics is the hard, field-flaky part) |
| **DIY / community** | SelfKnot Mini / SelfKnot kit | PAT-001, PAT-008 (with carve-outs) | Community track | Partial — see constraint | Low (kit) |
| **Drone vertical** | CBRNE silicon-to-sample module | PAT-012 | **License/SBIR — not Shopify** | Direct | N/A solo |
| Drone vertical | Anti-capture heartbeat erasure module | PAT-013 | **License/SBIR — not Shopify** | Direct | N/A solo |

**Kits / bundles (not new silicon):**

| Kit | What's in it | Backing patent | Build effort |
|---|---|---|---|
| CombinedSession kit | PV-A + ZKKey under one session ID | PAT-007 | Packaging/SKU only — you have a live COMBINED_SESSION verify record |
| OfflineEvidence field kit | ZKKey + PV + TrustSeals + offline verify tool | PAT-006 (strongest system claim) | Integration/packaging |

**SelfKnot constraint (carry forward):** the display-then-confirm step must not appear in free SelfKnot builds or free public content before the non-provisional filing. A SelfKnot *kit* SKU is fine; the gated-confirm UX is the ZKKey (Tier 2) moat and stays out of the free line.

---

# 2. Services & licensing layer (you asked to include services)

This is where the SDVOSB / federal story and the durable margin live.

| Service | Backing | Buyer | Notes |
|---|---|---|---|
| Device provisioning-as-a-service (vendor-irrevocable manufacturing ledger) | PAT-005 VendorAttest | Gov / regulated enterprise | Strongest federal-procurement hook. You provision *their* fleet under your root. |
| Verification authority (verifyknot.io) | PAT-004, PAT-019 | Anyone holding your devices | Already live (`/v/{code}`). Can be a paid tier for orgs. |
| HashStamp SaaS (self-serve signing/verify) | PAT-004 | SMB / developers | hashstamp.io. Recurring. |
| Attestation SDK / integration | PAT-004, PAT-019 | Integrators | Licensable spine. |
| Patent licensing — drone verticals | PAT-012, PAT-013 | Defense primes / UAV makers | Better licensed than built solo. |
| Expert / chain-of-custody consulting | Portfolio | Legal / journalism / forensic | Veteran-owned positioning; high trust, low capex. |

---

# 3. Energy allocation — ranked, after ZKKey ships

Ranked by ROI-to-effort, given PowerVerify is shipping and ZKKey is your committed next build.

1. **TrustSeal (PAT-003).** Cheapest thing you can make, recurring revenue, pairs with every product, trivial on-demand. Binds to the ledger you already operate. *Build this right after ZKKey.*
2. **PowerVerify Attested (PAT-002/018).** You're already in PV production; adding MCU+SE logging unlocks PAT-018 and the CombinedSession story while reusing your ATECC signing pipeline.
3. **CombinedSession kit (PAT-007).** Not a build — a bundle + listing. High story value for legal/forensic buyers. You have the verify record already.
4. **OfflineEvidence field kit (PAT-006).** Bundle/system, your strongest system-level claim, sells to journalists/NGOs/forensic field teams.
5. **ZKKey Ultra / dual-SE (PAT-011).** The federal/high-assurance differentiator. Real build effort (two SEs) — schedule it, don't rush it.

Different track (do not let these compete for bench time):
- **DataGap / TrustMeter (PAT-015/016):** real and defensible, but the hard build and a slow market. List as "research / contact us," not with a ship date.
- **Drone modules (PAT-012/013):** license / SBIR / partner. Not a storefront item.

---

# 4. Shopify structure — Now / Next / Research

The fix for "traffic arrives, one product, missed buyer" is structure, not volume.

**NOW (in stock / made on demand):**
- PowerVerify Core — $39
- ZKKey Connect *(on launch)*

**NEXT (made-to-order, email capture, honest "in production" / "taking interest"):**
- TrustSeal (consumable, sold in packs)
- PowerVerify Attested
- CombinedSession kit
- OfflineEvidence field kit
- ZKKey Air
- ZKKey Ultra *(high-assurance / agency inquiries)*

**RESEARCH / CONTACT US (no cart, no date):**
- DataGap USB Witness
- TrustMeter
- Provisioning-as-a-service (VendorAttest)
- Expert / chain-of-custody consulting

**NEVER list as add-to-cart:** drone CBRNE module, anti-capture heartbeat module. These go on a separate "Capabilities / Licensing" page if anywhere — language framed for primes and program offices, not consumers.

### The tradeoff, both sides
- **For listing breadth:** catches buyers across the range, email capture feeds a pipeline, signals roadmap depth, fuels build-in-public.
- **Against:** a solo shop listing 12 products can read as *less* credible to conservative gov/forensic buyers; every unbuilt SKU is an owed expectation; support burden scales with list length.
- **Resolution:** Now/Next/Research caps the credibility risk while still catching the buyer. "Made to order" is literally true for you, so the "incoming" label carries no overpromise.

---

# 5. Verification flags (read before any gov-facing use)

- **This is an internal/planning doc.** Patent numbers, titles, and statuses here are transcribed from your own summary. Before any of this appears on a **capability statement, proposal, or government-facing artifact**, re-verify titles and application numbers against USPTO Patent Center as primary source — do not propagate from this doc.
- **PAT-014** is an **unfiled draft** consolidated into PAT-015. Do not represent it as filed.
- **PAT-017** does **not appear** in the summary document. Confirm whether it exists / what it covers before relying on a count of 19, or before any "19 patents" claim on a federal artifact.
- **PAT-013** title: use the as-filed "Authenticated Heartbeat Key Erasure for Unmanned Aerial Evidence Systems" — an earlier draft title was wrong.
- **Marketing language guardrails:** "reduces," "designed to prevent," "physically inspectable." Avoid absolute security claims and real-time-threat-detection language. PowerVerify honesty gate stands: 60W max, no PUF/LEDs on current boards.

# 6. Backup / version-control status

- This file is **new and not yet committed**. The vault git working tree is mid-reorg (~337 files appearing deleted). **Do not run `git clean -fd`** until the reorg is committed, or this could be lost.
- Suggested home: `~/ZKNOT/5_PLANS/` (strategy/planning). The pure patent→product map (§1) could alternatively be promoted to `~/ZKNOT/3_OPS/km/systems/product-portfolio.md` as a durable fact if you want it as reference rather than a plan.
- This is a markdown vault file, so no "Page X of Y" footer (that applies to formal docx/PDF filings). If you want a formal PDF/docx version to send externally, say so and I'll add the footer and a cover.
