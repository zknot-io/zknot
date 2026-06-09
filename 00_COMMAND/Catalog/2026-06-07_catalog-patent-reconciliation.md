---
title: Catalog ↔ Patent Tracker Reconciliation — Coverage & Gaps to Claim
doc_id: STR-003 (suggested) — ZKNOT_STR-003_catalog_patent_reconciliation_20260607.md
author: William Shane Wilkinson
created: 2026-06-07
authoritative_source: ZKNOT_DOC-001_patent_tracker_UPDATED_20260604.xlsx (read in full, all 6 sheets, 2026-06-07)
companion: PLAN-CATALOG-001 (2026-06-07_product-catalog-from-patents.md)
scope: Internal IP/planning. NOT legal advice. Confirm filing decisions with registered patent attorney.
backup_status: NEW FILE — not committed. Vault git mid-reorg (~337 files showing deleted; do NOT run `git clean -fd`). Commit deliberately.
---

# TL;DR

- The tracker is the authority: **18 provisionals filed, 0 unfiled, 1 trademark pending.**
- **Nearly the entire proposed catalog is already covered by a filed provisional** — see coverage table. You can list most SKUs publicly today.
- **Defensible count is 18, not 19.** Internal IDs reach PAT-019, but PAT-014 and PAT-017 are holes (explained below). Fix any "19 patents" claim.
- **Bonus:** EvidenceProtocol (63/961,116) is filed and was missing from the DOC-003 summary; it strengthens the kit + verification-service claims. Confirm its SB15A status in TSDR.
- **Real gaps to claim:** GAP-003 multi-party witness (realest); GAP-001 verification protocol (maybe); GAP-002 CC-line (likely already absorbed by PAT-018). Plus two optional decisions.
- **Disclosure rule:** file a $65 provisional before any *unclaimed* invention is publicly listed/offered for sale. Covered items are safe to list now.

# Decisions captured

1. Use **18 filed provisionals** as the official number on all external/federal artifacts.
2. Treat **EvidenceProtocol (63/961,116)** as live backing for OfflineEvidence kit + verification service; verify its micro-entity cert.
3. **GAP-003 (multi-party witness)** is the strongest candidate for a new $65 provisional. Raise GAP-001/GAP-002 with attorney.
4. **No public storefront listing of any SKU not mapped to a filed App# below until a provisional is on file.**

---

# 1. Numbering reconciliation (clears prior confusion)

| Internal ID | Status | Explanation |
|---|---|---|
| PAT-014 (DataGapTester) | **Not filed** | Consolidated into PAT-015 (DataGapUSBDetect). Spec exists as draft only. |
| PAT-017 | **Never existed** | Was a *candidate slot* for PowerVerify Plus. PowerVerify Plus filed as **PAT-018** (64/007,940). Number simply skipped. |

**Correction to companion memo (PLAN-CATALOG-001):** that doc flagged "PAT-017 missing — confirm it exists." Resolved — it never existed; no action. The earlier "verify count of 19" note is superseded: the count is **18 filed**.

---

# 2. Coverage table — every catalog item → filed App# (ground truth: DOC-001)

Internal PAT-ID and ZKM-ID differ in the tracker; App# is the anchor.

| Catalog item | Backing patent (short) | App # | Filed? |
|---|---|---|---|
| PowerVerify Core | PAT-002 PowerVerify | 63/961,118 | ✓ |
| PowerVerify Attested | PAT-002 + PAT-018 | 63/961,118 + 64/007,940 | ✓ |
| PowerVerify Plus (tamper/sealed/CC) | PAT-018 PowerVerifyPlus | 64/007,940 | ✓ |
| ZKKey Connect | PAT-001 + PAT-008 + PAT-010 | 63/960,933 + 63/995,736 + 63/995,747 | ✓ |
| ZKKey Air | PAT-009 OpticalChallenge | 63/995,740 | ✓ |
| ZKKey Ultra (dual-SE) | PAT-011 DualSE | 64/007,907 | ✓ |
| TrustSeal (consumable) | PAT-003 TrustSeal | 63/961,112 | ✓ |
| DataGap USB Witness | PAT-015 DataGapUSBDetect | 64/007,931 | ✓ |
| TrustMeter | PAT-016 TrustMeter | 64/007,934 | ✓ |
| CombinedSession kit | PAT-007 CombinedSession | 63/995,728 | ✓ |
| OfflineEvidence field kit | PAT-006 OfflineEvidence **+ EvidenceProtocol** | 63/978,480 **+ 63/961,116** | ✓ |
| Drone CBRNE module | PAT-012 SiliconToSample | 64/007,917 | ✓ |
| Drone anti-capture (aerial) | PAT-013 HeartbeatErasure | 64/007,923 | ✓ |
| Provisioning-as-a-service | PAT-005 VendorAttest | 63/964,169 | ✓ |
| Verification authority / SDK / SaaS | PAT-004 ZK-LocalChain + PAT-019 Umbrella + EvidenceProtocol | 63/961,098 + 64/038,840 + 63/961,116 | ✓ |
| Human-readable verify codes | PAT-010 HumanReadableAttest | 63/995,747 | ✓ |
| Expert / chain-of-custody consulting | (service — no patent required) | — | n/a |

**Result: full catalog coverage.** No proposed SKU is unbacked.

---

# 3. Bonus filed patent (was absent from the summary doc)

**EvidenceProtocol — App# 63/961,116 (ZKM-P004 / tracker "PAT-006b")**
"Cryptographically Verified Evidence Integrity Protocol for Human-Witnessed Digital and Physical Events." System-level end-to-end chain-of-custody workflow. Filed 01/15/2026.

- **Why it matters:** stronger backing for the OfflineEvidence kit and the verification service than the device patents alone.
- **Action:** tracker flags **1 submission only — confirm SB15A (micro-entity) status in TSDR** so it isn't defective. (Dashboard "JUL 2026" action also calls this out.)

---

# 4. Gaps to claim (NOT filed per tracker)

Source: your own Dashboard "File P1 gap provisionals" (was scheduled May 2026, before attorney engagement). None appear as filed App#s.

| Gap | Current coverage read | Recommendation |
|---|---|---|
| **GAP-003 Multi-party witness** | PAT-007 binds two *devices* in one session; multiple independent *human* witnesses co-signing one event likely exceeds it. | **Strongest candidate. File $65 provisional.** |
| **GAP-001 Verification Protocol** | Partially covered by PAT-019 (verification output) + PAT-004 (ledger). Standalone third-party verification ceremony may still warrant its own claim. | Raise with attorney; cheap to file if in doubt. |
| **GAP-002 CC-Line specificity** | PAT-018 added CC-line negotiation attestation. | **Likely already absorbed.** Confirm, then close. |
| (Optional) Self-provisioned / self-asserted identity (SelfKnot) | Vendor-provisioned is PAT-005; self-asserted model not separately claimed. | Only file if you intend to *defend* it — conflicts with CC-licensed open posture. Decide deliberately. |
| (Optional) Non-aerial tamper-triggered key erasure | PAT-013 scoped to unmanned aerial/vehicle systems. | A stationary/portable evidence-box variant may be uncovered. File only if it becomes a product. |

---

# 5. The disclosure rule (why "not in tracker → claim it" is correct)

*Factual summary, not legal advice — this is the precise question for your attorney.*

- **US on-sale / public-disclosure bar (AIA §102):** publicly offering an invention for sale or disclosing it starts a **one-year clock** to file in the US; miss it and the invention is barred. A storefront listing with a price can constitute an offer for sale even before the unit physically exists.
- **Foreign (absolute-novelty) jurisdictions:** public disclosure *before* filing can destroy novelty **immediately** — foreign rights lost the moment you list.
- **Provisional filing** establishes priority and starts the 12-month conversion clock.

**Operational rule for the storefront:**
- Items mapped to a filed App# in §2 → **safe to list now** (priority already secured; mind conversion deadlines).
- Any **new** SKU, or a GAP item turned into a product → **file a $65 provisional before it goes on the site, even as "coming soon."**

---

# 6. Action checklist

- [ ] Update catalog/marketing/cap statement to say **18 filed provisionals**.
- [ ] Confirm **EvidenceProtocol (63/961,116)** SB15A status in TSDR.
- [ ] File **GAP-003 (multi-party witness)** provisional ($65) — or confirm a decision not to.
- [ ] Ask attorney: GAP-001 standalone vs. covered by PAT-019; confirm GAP-002 absorbed by PAT-018.
- [ ] Decide SelfKnot self-provisioning: defend (file) vs. keep open (don't).
- [ ] Before listing any SKU not in §2: file provisional first.

# 7. Backup / version-control

- **New, uncommitted.** Vault git mid-reorg — commit deliberately; **do not run `git clean -fd`** until reorg is committed.
- Suggested home: `~/ZKNOT/3_OPS/...` or `01_PATENTS/` per your File Naming Master (STR type lives in `01_PATENTS/`). Suggested name: `ZKNOT_STR-003_catalog_patent_reconciliation_20260607.md`.
- Markdown vault file → no "Page X of Y" footer. Want a formal PDF/docx (with footer + cover) for attorney handoff? Say so and I'll generate it.
