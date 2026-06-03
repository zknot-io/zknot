ZKNOT_BIZ — Master File Repository
=====================================
Version: 20260407
Owner: William Shane Wilkinson, CEO — ZKNOT, Inc.

NAMING CONVENTION (CANONICAL):
  ZKNOT_[TYPE]-[NNN]_[ShortName]_[descriptor_snake_case]_[YYYYMMDD].[ext]

TYPE CODES:
  PAT       Provisional patent specs
  PAT-NP    Non-provisional patent drafts/filings
  TM        Trademark filings
  DOC       General documents / patent tracker
  CORP      Corporate formation & equity
  FED       Federal registrations (SAM, CAGE, VetCert)
  CAP       Capability statement
  LGL       Legal agreements and templates
  CFO       Financial documents
  BOM       Bills of materials
  PCB       PCB design files
  HW        Hardware master documents
  FW        Firmware binaries
  SW        Software repo snapshots
  ACQ       Acquisition / M&A outreach
  MKT       Marketing materials
  TMPL      Blank templates
  CEO/COO/CFO/OPS  Leadership operating documents

FOLDER STRUCTURE:
  00_COMMAND/         Master operating docs (CEO, COO, CFO, OPS, LGL, ACQ)
  01_PATENTS/         All patent docs (FILED / PENDING / NON_PROVISIONAL / SUPPORTING_DOCS / ASSIGNMENTS)
  02_CORPORATE/       Articles, bylaws, EIN, stock certs, cap table
  03_FEDERAL/         SAM.gov, CAGE, VetCert, capability statement
  04_LEGAL/           NDAs, contractor agreements, IP assignments
  05_FINANCIAL/       Financial model, bookkeeping, receipts, SBIR
  06_HARDWARE/        PCB, Gerbers, BOM, HW docs
  07_FIRMWARE/        Compiled firmware binaries
  08_SOFTWARE/        Software repo snapshots
  09_ACQUISITION/     M&A outreach and data room
  10_MARKETING/       Demo scripts, brand, capability statement
  99_ARCHIVE/         Legacy and superseded files — do not reference

SOURCE OF TRUTH: 01_PATENTS/SUPPORTING_DOCS/DOC-SP_specs/ZKNOT_DOC-001_patent_tracker_[DATE].xlsx

OPEN ACTION ITEMS:
  [ ] Add PAT-019 SystemUmbrella to patent tracker (filed 20260403)
  [ ] Verify PAT-014 — gap in tracker, confirm if real or skipped
  [ ] Upload DD-214 to VetCert portal
  [ ] Upload VA disability rating letter to VetCert portal
