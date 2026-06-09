---
title: Catalog Status Addendum — Per-Item Storefront Disposition (FINAL)
doc_id: PLAN-CATALOG-001-ADDENDUM-A
parent: PLAN-CATALOG-001 (2026-06-07_product-catalog-from-patents.md)
author: William Shane Wilkinson
created: 2026-06-07
status: FINAL — decisions locked 2026-06-07
backup_status: NEW FILE — not committed. Vault git mid-reorg; do NOT run `git clean -fd`.
---

# Platform frame (read first — it governs everything below)

These are not 12 independent products. They are **one 30×90 mm core module + carriers**.
- ZKKey Connect establishes the core module (ZKKey base).
- ZKKey Air, PowerVerify Attested, and the internal drone build are **carrier variants** that reuse that same core.
- TrustSeal is the exception — a physical seal, not a PCB — which is precisely why it can ship in parallel without competing for module-design time.

**Consequence:** building #1 funds the foundation for all later carriers. Build order is sequenced to (a) establish the core, (b) bank cheap orthogonal revenue, (c) reuse the core outward.

# Status vocabulary

- **IN PRODUCTION** — shipping now, add-to-cart.
- **PRIORITY BUILD** — committed next build; not yet for sale.
- **BUILD NEXT** — roadmap, made-to-order; "Coming soon" + email capture.
- **EMAIL FOR INFO** — no cart; inquiry/quote/licensing.
- **RESEARCH** — real patent, hard/undecided build; "Contact us," no date.
- **NOT LISTED** — internal; not on any public surface.

# Build order (locked)

1. **ZKKey Connect** — core module (PRIORITY BUILD)
2. **TrustSeal** — orthogonal, off-platform, recurring revenue (BUILD NEXT)
3. **ZKKey Air** — first carrier reuse of the core (BUILD NEXT)
4. **PowerVerify Attested** — second carrier reuse (BUILD NEXT)
5. *(internal)* **Drone build** — carrier reuse, built after ZKKey, stays internal

---

# Per-item disposition (price + lead time)

> Prices marked **(proposed)** are starting anchors for you to set — only PV-C is confirmed. Unbuilt items show **target price** + pre-order availability.

| Item | Status | Price | Lead time / availability |
|---|---|---|---|
| **PowerVerify Core (PV-C)** | IN PRODUCTION | **$39** (confirmed) | Made-to-order, ships ~1–2 weeks |
| **ZKKey Connect** | PRIORITY BUILD (#1) | ~$149 (proposed) | Pre-order / notify — launch TBD |
| **TrustSeal** | BUILD NEXT (#2) | ~$24 / 10-pack (proposed) | Made-to-order; near-term |
| **ZKKey Air** | BUILD NEXT (#3) | ~$249 (proposed) | Pre-order / notify — after ZKKey Connect |
| **PowerVerify Attested (PV-A)** | BUILD NEXT (#4) | ~$99 (proposed) | Pre-order / notify — after first 50 PV-C |
| **PowerVerify Plus** | RESEARCH | Quote | Contact us — no date |
| **ZKKey Ultra (dual-SE)** | EMAIL FOR INFO | Quote (no public price) | Made-to-order, agency inquiry |
| **CombinedSession kit** | EMAIL FOR INFO → BUILD NEXT once PV-A + ZKKey exist | Quote | After components ship |
| **OfflineEvidence field kit** | EMAIL FOR INFO | Quote | Org / quote-based |
| **DataGap USB Witness** | RESEARCH | Quote | Contact us — no date |
| **TrustMeter** | RESEARCH | Quote | Contact us — no date |
| **Drone CBRNE module** | NOT LISTED (internal) | — | Built after ZKKey; carrier of core module |
| **Drone anti-capture** | NOT LISTED (internal) | — | Built after ZKKey; carrier of core module |
| **Multi-Party Witness (GAP-003)** | RESEARCH | Quote | Patent pending; future kit |

---

# Services (confirmed development priority)

You flagged these as the right direction and to be developed. They are the moat — they monetize the platform without new silicon.

| Service | Status | Note |
|---|---|---|
| Provisioning-as-a-service (VendorAttest) | EMAIL FOR INFO | B2B / federal. Strongest procurement hook. |
| Verification authority + HashStamp SaaS | BUILD NEXT (software) | verifyknot.io live; HashStamp = self-serve surface. |
| Expert / chain-of-custody consulting | EMAIL FOR INFO — available now | No build; veteran-owned positioning. Listable today. |
| Patent licensing (drone verticals) | EMAIL FOR INFO | Capabilities/licensing page only. |

---

# SDVOSB teaming / partnership / M&A signal

You want to signal willingness to partner or merge — especially for primes who need an SDVOSB. Add a dedicated **"Teaming & Capabilities"** surface (page or banner), distinct from the shop:

- Lead with **SDVOSB + the 18-patent portfolio + the single attested core platform**.
- Two audiences, one page: (a) **primes** needing an SDVOSB subcontractor/teaming partner for set-asides; (b) **acquirers** (ties to your 12-month acquisition-readiness target).
- Disposition: **EMAIL FOR INFO** — inquiry/NDA gate, no public detail on internal builds (drone stays dark here too).

---

# Off-storefront

- **SelfKnot** — lives on **zknot.org** only (open/DIY, CC BY-NC-SA). **Benched** until ZKKey Connect + Air ship. Field builds and self-attests follow, but carry no weight without a paying product first. Not in the commercial catalog.

# Promote to systems doc

The **30×90 core-module-and-carriers architecture** is a durable fact, not a planning note. Recommend a dedicated `3_OPS/km/systems/hardware-platform.md` capturing the core module spec and which carriers inherit it. (Offered separately.)
