# Full Session Capture — SAM Renewal, Master Docs v1.1, Downloads Cleanup

**Date:** 2026-05-11
**Workstream:** ops / federal-compliance / km
**Status:** Session complete; two open loops noted at bottom

This journal captures an entire long working session so the source chat can be deleted.

## 1. NDA Template Set (COMPLETED)

Produced 4 NDA documents, customized to Utah / Salt Lake County, saved to
~/ZKNOT/JAG/CONTRACTS/NDA/templates/:
- ZKNOT_NDA_Unilateral_v1.0.pdf (6 pages)
- ZKNOT_NDA_Mutual_v1.0.pdf (7 pages)
- ZKNOT_NDA_Demo_v1.0.docx (2 pages, in-person trade show use)
- ZKNOT_NDA_CheatSheet_v1.0.docx (internal reference)

Key decisions:
- Utah governing law, Salt Lake County venue, JAMS arbitration default
- Founder & CEO title, operating address as registered address
- Broad AI/LLM clause (covers any third-party processing)
- Residual knowledge clause omitted (flagged as negotiation lever)
- Terms: 2yr disclosure / 5yr confidentiality / perpetual trade secrets
- Mutual NDA keeps Sections 3, 6, 9, 10 asymmetric (protect ZKNOT only);
  counter-offer is separate addendum if counterparty has comparable hardware
- Section 3 names ATECC slot configs, PUF substrate, manufacturer attestation
  private key custody as perpetual trade secrets
- Section 10 export control (EAR/ITAR) acknowledgment

PENDING: fill bracketed placeholders per engagement ([DESCRIBE PURPOSE],
counterparty fields, [Effective Date], [NOTICE EMAIL]); route all 4 to a
small-business IP attorney for review (budget $300-500), focusing on 15 starred
decision items (arbitration enforceability, asymmetric mutual clauses, AI clause,
trade secret carve-out).

## 2. Email Signature (COMPLETED)

Plain text + HTML versions produced with full federal credentials.
Gold accent (#C2B280). Includes UEI C4SKW13JPEL5, CAGE 1AHZ4, EIN 36-5165991,
SDVOSB Certified (SBA VetCert), VOSB, Small Business, NAICS + PSC lists,
"SAM.gov Active — Cryptographic Authenticity Verification". Explicit "(SBA VetCert)"
qualifier added because self-certified SDVOSB no longer counts for set-asides
post-2024.

## 3. SAM.gov Full Entity Renewal (SUBMITTED — AWAITING VALIDATION)

Stepped through entire SAM.gov full entity renewal, submitted 2026-05-11 with
SDVOSB attestation. Validation window 24-72 hrs typical, up to 10 business days
for IRS/CAGE re-verification.

Critical values submitted:
- Entity Structure: Corporate Entity, Not Tax Exempt (For Profit) — resolves
  prior LLC ambiguity
- Socio-Economic: Veteran-Owned + Service-Disabled Veteran-Owned both checked
- Small Disadvantaged Business: No (SDB differs from SDVOSB)
- NAICS expanded 3 to 8: PRIMARY 334418 (Printed Circuit Assembly Mfg), plus
  334290, 334419, 541512, and full 541715 family with all 4 exceptions
  (covers DARPA/AFWERX/IC R&D incl aerospace/missiles/space)
- PSC: 5999, 5810 (COMSEC), 7A20, AC11 (DoD Basic Research), AC12 (DoD Applied
  Research), DA10 (IT SaaS)
- Annual Receipts: $1 (SAM rejects $0)
- Employees Worldwide: 1
- Most Recent Tax Return Year: 2025 (PLACEHOLDER — incorporated 2026-01-26, no
  actual return filed; ACKNOWLEDGED RISK may flag during IRS validation; fix at
  validation failure if it happens)
- Disaster Response Registry: Yes
- All 3 mandatory POCs: William Shane Wilkinson, CEO, ops@zknot.io, (385) 234-7555
- Past Performance optional POC: REMOVED (was contaminated with personal gmail/
  (801) and no past contracts to reference)
- DFARS: GAAP-compliant statements Yes (founder accounting degree); all others No
- FAR Offer-Level: Limited Rights Data declared "ZKNOTmodule firmware and
  attestation software" under FAR 52.227-15; Service Contract Labor Standards
  exemption Yes; Covered Telecom No; Buy American No (pre-production)
- Banking: Bank of America NW N.A.-Idaho on file

## 4. Master Operating Docs v1.1 (COMPLETED — committed 65c7bdc)

Converted 3 master docs from .docx to markdown and updated to post-cert state:

- ~/ZKNOT/00_COMMAND/ZKNOT_COO-001_v1.1_20260511.md (378 lines) — complete rewrite.
  SDVOSB PENDING to CERTIFIED. Stale "single-member LLC" fixed to "Utah for-profit
  corporation, single shareholder." NAICS 3 to 8, PSC 2 to 6. Section 2 pivoted to
  post-cert maintenance + exploitation playbook. Section 6 ladder: Steps 1-3 DONE,
  new Step 5 (VA VIP) marked CRITICAL NEXT. New Section 11 (Pre-Exit Cleanup).
- ~/ZKNOT/9_GOV/ZKNOT_DOC-011_v1.1_20260511.md (259 lines) — SDVOSB strategy
  reframed from execution plan to value-extraction playbook. Timeline collapsed
  forward to start with VA VIP registration. Valuation premium realized at row 3
  ($8-12M with SDVOSB), row 4 ($12-16M) as next target via first contract.
- ~/ZKNOT/00_COMMAND/ZKNOT_CFO-001_v1.1_20260511.md (361 lines) — Section 7 Data
  Room: SDVOSB Certificate PENDING to DONE. Section 8.2 added GAAP compliance notes.
  Section 6.1 SDVOSB premium "now realized, not projected." Section 9 first-tax-return
  paragraph added. QSBS Section 1202 noted (C-Corp confirmed; up to $10M tax-free
  on exit; verify with CPA).

Originals archived to ~/ZKNOT/99_ARCHIVE/superseded_20260511/.
Going forward: master docs are markdown + git, not .docx.

## 5. Taskwarrior Tasks Created (COMPLETED)

- 80: Check DISS/DCSA for past clearance status (zknot.gov, M)
- 81: Research clearance reinstatement options post-SBIR (zknot.gov, L)
- 82: Resolve POC founder-dependency before going to market (zknot.acquisition,
  ops, M, due 2027-01-01, +preexit)
- 83: Research federal & state surplus property program access (zknot.gov, M,
  due 2026-07-01, +postsam)
- 84: Build ZKNOT capital equipment wishlist with target sources (zknot.gov, L,
  +postsam)
- 85: Register at GSAXcess.gov as SDVOSB-eligible recipient (depends 83, +postsam)
- 86: Register Utah State Surplus Property eligibility (depends 83, +postsam)
- 87: Sort ZKNOT_BIZ legacy dump into KM-001 structure (zknot.ops, ops, M,
  due 2026-06-30)

## 6. Surplus Property Program Notes (for tasks 83-86)

Federal: GSAXcess.gov (SDVOSB access via SBA programs); DLA Disposition Services
(free transfer via State Agency for Surplus Property); GovDeals/GovPlanet (auction).
Utah: Utah State Surplus Property Program (Division of Purchasing, SLC-based).
Wishlist priorities: 3D printers, reflow soldering, oscilloscopes, soldering/rework
stations, inspection microscopes (all high surplus availability). Consumables
(filament, solder paste, components) and licensed software NOT surplus territory —
buy retail. DLA disposal cycle peaks Q4 fiscal year (Aug-Sep); be registered by
Jul/Aug 2026 to hit prime window. University surplus (U of U, BYU, Utah State)
also worth checking. Watch for end-use/no-resale restrictions on transfers.

## 7. Downloads Folder Cleanup (COMPLETED)

Downloads is now empty. Sorted:
- Federal letters to 9_GOV/federal/: zknot-inc_ucp_approval_letter.pdf +
  _vet_cert_supp.pdf (SDVOSB approval letters — data room headliners; consider
  renaming to SDVOSB_VetCert_approval_2026-05.pdf)
- NDA set to JAG/CONTRACTS/NDA/templates/
- Journals/scripts to 3_OPS/ and 3_OPS/journal/
- KM docs to 3_OPS/km/
- Hardware handoffs to 6_SIG/hw/
- SW-001 to NEW 6_SIG/software/ (was a file-collision; sw wasn't a directory)
- PUF guide + social presence to 7_ENG/
- Photos to ~/Pictures/from_downloads/
- Deleted: Bitwarden.AppImage, Logic AppImage, CUDA keyring, Pi Pico uf2,
  files*.zip, duplicate .py source (identical to ~/zknot-api/ repo), zknot-api-pr
  (identical to repo), duplicate NDA/journal files
- 01_PATENTS: merged Feb 2026 Google Drive export (rsync --ignore-existing) then
  removed Downloads copy

## 8. ZKNOT_BIZ Legacy Dump (ARCHIVED — needs future sort, task 87)

585MB / 3737 files pre-KM-001 dump moved INTACT to
~/ZKNOT/99_ARCHIVE/zknot_biz_legacy_dump_20260511/. Contains UNIQUE,
NON-REPRODUCIBLE docs not in current KM structure, including:
- ZKNOT_CORP-004_stock_certificate_001_wilkinson (stock certificate)
- ZKNOT_CORP-008_utah_incorporation_filing_receipt
- ZKNOT_DOC-005 Utah Articles of Incorporation (stamped)
- ZKNOT_DOC-010 signed stock cert (10M shares, signed 03172026)
- ZKNOT_Stock_Ledger.docx + .pdf
- ZKNOT_DOC-003_SpendTracker.xlsx
- ZKNOT_CORP-010_logins_credentials_ref
- Receipts/, legal/, USPTO export folders
- Many TrustKnot/DataGap/TrustMeter/TrustSeal HW specs (HW-003 through HW-011)
- PAT spec drafts (PAT-001/002/004/007/011), attorney brief, prior art search
DO NOT DELETE. Task 87 (due 2026-06-30) to sort into KM-001 properly.

## 9. lizhoke.com Moved Out of ZKNOT (COMPLETED — committed 0bc9a7d)

lizhoke.com is a personal project (girlfriend's photography portfolio site,
mostly done, awaiting better photos to go live). Moved from ~/ZKNOT/7_ENG/lizhoke.com
to ~/personal/lizhoke.com to keep personal project out of business/acquisition
vault. Git tracking removed (5 files deleted from repo going forward). Old git
history in dae3578 still contains the files but that's harmless — not scrubbing.
old-scaffold was earlier lizhoke.com scaffolding, lives in ~/personal/lizhoke.com.

## 10. Memory Edits Added This Session

- Full legal name is William Shane Wilkinson; use on all official docs/signatures/
  certifications/federal filings (not "Shane Wilkinson" alone)
- ZKNOT SDVOSB certified through SBA VetCert, approved early May 2026. SAM record:
  ZKNOT INC, UEI C4SKW13JPEL5, CAGE 1AHZ4, 1884 W Sir Charles Dr SLC UT 84116-4652,
  expiration 2027-03-17. Account email shane.systems@gmail.com.

## OPEN LOOPS (carry forward — do NOT lose these)

1. SAM VALIDATION: Monitor email + sam.gov public search for certified SDVOSB tag.
   Once it appears: register VA VIP (vetbiz.va.gov) WITHIN 5 DAYS — gateway to
   Vets First, $6.2B/yr SDVOSB market, single highest-value action open.

2. GIT ERROR (5-min fix): The "Downloads cleanup completion" commit FAILED with:
   "99_ARCHIVE/zknot_biz_legacy_dump_20260511/ZKKEY-HW-G1-USB-A-REV-A/ does not
   have a commit checked out". That subfolder inside ZKNOT_BIZ is a nested git repo
   (its own .git), which blocks the parent git add. Untracked-but-uncommitted right
   now: 01_PATENTS additions + the whole zknot_biz_legacy_dump. Files are physically
   safe; just not committed. Fix tomorrow: either delete the nested .git
   (rm -rf the nested .git dir to flatten it) OR add as submodule. Then re-run
   git add -A && git commit.

3. CAP-001 capability statement: needs "SDVOSB Certified (SBA VetCert)" added to
   header; distribute to VA OSDBU + 5 DoD/DHS small biz offices after SAM validates.

4. SDVOSB recertification (3-year): set calendar alert for 2029-02-01 (90 days early).

5. Other master docs (CEO-001, ACQ-003/004, HW-001, LGL-001, OPS-001) likely need
   minor SDVOSB-status updates + markdown conversion — future sessions.

6. NDA attorney review: route 4 NDA docs to IP attorney ($300-500).

7. Save SDVOSB cert PDF to ~/ZKNOT/9_GOV/federal/SDVOSB_cert_2026-05.pdf + offsite.
