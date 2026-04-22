# ZKNOT-BIZ File Structure — Full Audit & Naming Convention Upgrade
**Generated: April 6, 2026 | Based on: ZKNOT_DOC-001_patent_tracker_20260328.xlsx**

---

## NAMING CONVENTION (Canonical — From Patent Tracker)

```
ZKNOT_[TYPE]-[NNN]_[ShortName]_[descriptor_snake_case]_[YYYYMMDD].[ext]
```

| Field | Pattern | Example |
|-------|---------|---------|
| PREFIX | Always ZKNOT | ZKNOT |
| TYPE | PAT, PAT-NP, TM, PCB, FW, BOM, DOC, ACQ, CEO, COO, CFO, OPS, LGL, HW, SW, CORP, FED, LGL | PAT |
| NNN | Zero-padded 3-digit per type | 001 |
| ShortName | CamelCase, no spaces | ZKKey |
| descriptor | snake_case, brief | provisional_spec |
| DATE | YYYYMMDD | 20260115 |
| ext | Always lowercase | .docx |

---

## STRUCTURE SCORECARD

| Area | Grade | Notes |
|------|-------|-------|
| Patent folder hierarchy | ✅ A | FILED / PENDING / NON_PROVISIONAL is clean |
| Patent file naming | ✅ A | Tracker convention fully defined + examples |
| Supporting docs index | ✅ A | DOC-ME-xxx, DOC-RX-xxx, DOC-SP-xxx system is excellent |
| 01_PATENTS top-level | ⚠️ B | tracker.xlsx sitting loose — should be DOC-001 subfolder |
| 00_COMMAND naming | ⚠️ B | Files use CEO/COO/CFO prefixes — not aligned to TYPE system |
| 02_CORPORATE | ⚠️ B | Files lack ZKNOT_ prefix + date suffix |
| 03_FEDERAL | ⚠️ B | Same — no convention applied |
| 04_LEGAL | ⚠️ B | Same — templates OK, signed files unnamed |
| 05_FINANCIAL | ⚠️ B | ZKNOT_CFO convention partially applied |
| 06_HARDWARE | ✅ B+ | BOM follows convention; KiCad/Gerbers raw |
| 07_FIRMWARE | ⚠️ C | No files named yet — structure only |
| 08_SOFTWARE | ⚠️ C | No convention applied — code repos |
| 09_ACQUISITION | ⚠️ B | ACQ type defined but outreach log unnamed |
| 10_MARKETING | ⚠️ C | No convention applied |
| 99_ARCHIVE | ✅ A | Correct use — legacy docs quarantined |

---

## WHAT'S PERFECT ✅

1. **Patent tracker is the single source of truth** — Every provisional has App#, Conf#, fees, transaction IDs. This is exactly right.
2. **DOC-ME / DOC-RX / DOC-SP sub-ID system** — Micro entity certs, receipts, and specs each have their own namespace. Scales cleanly.
3. **FILED / PENDING / NON_PROVISIONAL split** — Legal status is immediately obvious from folder location.
4. **Priority date clusters visible** — Jan 15, Jan 20, Feb 9, Mar 3, Mar 17 batches map perfectly to folders.
5. **99_ARCHIVE quarantine** — Pre-CEO001 docs are isolated. Nothing bleeds into live structure.
6. **Conversion timeline sheet** — Deadlines, costs, and strategy in one place.
7. **ZKM-P prefix in tracker** — Links hardware device identity to patent identity.
8. **PAT-019_SystemUmbrella** — Filed Apr 3; already in FILED folder. Tracker needs update (not in DOC-001 yet).

---

## WHAT TO FIX ⚠️

### FIX 1 — 00_COMMAND: Apply TYPE codes
Current names use functional titles (CEO, COO, CFO) but TYPE field should drive the prefix.

| Current Filename | Correct Filename |
|-----------------|-----------------|
| ZKNOT_CEO-001_master_operating_document.docx | ZKNOT_DOC-001_CEO_master_operating_doc_20260126.docx |
| ZKNOT_COO-001_master_operating_document.docx | ZKNOT_DOC-002_COO_master_operating_doc_20260126.docx |
| ZKNOT_CFO-001_master_operating_document.docx | ZKNOT_DOC-003_CFO_master_operating_doc_20260126.docx |
| ZKNOT_OPS-001_master_ops_calendar.docx | ZKNOT_DOC-004_OPS_master_ops_calendar_20260126.docx |
| ZKNOT_LGL-001_legal_ip_master.docx | ZKNOT_DOC-005_LGL_legal_ip_master_20260126.docx |
| ZKNOT_ACQ-004_acquirer_outreach_master.docx | ZKNOT_ACQ-004_acquirer_outreach_master_20260301.docx ✅ |

> **Verdict:** ACQ-004 is already correct. CEO/COO/CFO/OPS/LGL should either adopt DOC-NNN or formalize CEO/COO/CFO/OPS/LGL as official TYPE codes in the tracker's File Naming Convention tab. **Recommend formalizing as TYPE codes** — they're functionally different enough to warrant their own namespace.

---

### FIX 2 — 02_CORPORATE: Add prefix + dates
| Current | Correct |
|---------|---------|
| Articles_of_Incorporation_20260126.pdf | ZKNOT_CORP-001_articles_of_incorporation_20260126.pdf |
| Bylaws_ZKNOT_Inc.docx | ZKNOT_CORP-002_bylaws_20260126.docx |
| EIN_Assignment_Letter.pdf | ZKNOT_CORP-003_ein_assignment_letter_20260126.pdf |
| Stock_Certificate_001_Wilkinson.pdf | ZKNOT_CORP-004_stock_certificate_001_wilkinson_20260126.pdf |
| Cap_Table_ZKNOT_Inc.docx | ZKNOT_CORP-005_cap_table_20260126.docx |
| Annual_Meeting_Minutes_2026.docx | ZKNOT_CORP-006_annual_meeting_minutes_20260401.docx |
| Utah_Annual_Report_2026.pdf | ZKNOT_CORP-007_utah_annual_report_20260401.pdf |

---

### FIX 3 — 03_FEDERAL: Add prefix
| Current | Correct |
|---------|---------|
| SAM_Registration_Certificate.pdf | ZKNOT_FED-001_sam_registration_cert_20260317.pdf |
| SAM_Renewal_Due_20270317.txt | ZKNOT_FED-002_sam_renewal_reminder_20270317.txt |
| VetCert_Application_Submitted.pdf | ZKNOT_FED-003_vetcert_application_submitted_20260101.pdf |
| CAGE_Code_1AHZ4_Letter.pdf | ZKNOT_FED-004_cage_code_1AHZ4_letter_20260101.pdf |
| ZKNOT_CAP-001_capability_statement.docx | ZKNOT_CAP-001_capability_statement_20260301.docx ✅ (add date) |

---

### FIX 4 — 04_LEGAL: Add prefix + dates
| Current | Correct |
|---------|---------|
| ZKNOT_NDA_template_mutual.docx | ZKNOT_LGL-001_nda_template_mutual_20260201.docx |
| ZKNOT_Contractor_Agreement_template.docx | ZKNOT_LGL-002_contractor_agreement_template_20260201.docx |
| Founder_IP_Assignment_Wilkinson_to_ZKNOT.docx | ZKNOT_LGL-003_ip_assignment_founder_wilkinson_20260126.docx |
| ZKNOT_Trade_Secret_Register.docx | ZKNOT_LGL-004_trade_secret_register_20260201.docx |

---

### FIX 5 — 05_FINANCIAL: Add prefix where missing
| Current | Correct |
|---------|---------|
| ZKNOT_CFO_Financial_Model_3Scenario.xlsx | ZKNOT_CFO-001_financial_model_3scenario_20260201.xlsx ✅ (add ID + date) |
| QSBS_Section1202_Analysis_Memo.docx | ZKNOT_CFO-002_qsbs_section1202_memo_20260201.docx |

---

### FIX 6 — 06_HARDWARE: Standardize PCB and HW docs
| Current | Correct |
|---------|---------|
| ZKNOT_BOM-001_ZKM001_AssemblyKit.xlsx | ZKNOT_BOM-001_ZKM001_assembly_kit_20260301.xlsx ✅ (add date) |
| ZKNOT_HW-001_hardware_firmware_master.docx | ZKNOT_HW-001_ZKM001_hardware_firmware_master_20260301.docx |
| Device_ID_Registry.xlsx | ZKNOT_DOC-010_device_id_registry_20260301.xlsx |

---

### FIX 7 — 09_ACQUISITION
| Current | Correct |
|---------|---------|
| ZKNOT_ACQ_Outreach_Log.xlsx | ZKNOT_ACQ-001_outreach_log_20260301.xlsx |

---

### FIX 8 — Missing PAT-019 in Tracker
PAT-019_SystemUmbrella was filed April 3, 2026. It appears in the folder tree but is NOT in the patent tracker. This is a gap — add row to Patent Portfolio sheet.

**Suggested tracker entry:**
- ZKM ID: ZKM-P019
- Internal ID: PAT-019
- Short Name: SystemUmbrella
- Filed: 04/03/2026
- Priority Date: 04/03/2026
- Expiry (12-mo): 04/03/2027

---

## COMPLETE FLAT FILE INDEX (All Files — Convention Applied)

> This is the "giant folder" view — every file in the system with its canonical name. Files are unique by name even without folder context.

### 00_COMMAND
```
ZKNOT_CEO-001_master_operating_doc_[DATE].docx
ZKNOT_COO-001_master_operating_doc_[DATE].docx
ZKNOT_CFO-001_master_operating_doc_[DATE].docx
ZKNOT_OPS-001_master_ops_calendar_[DATE].docx
ZKNOT_LGL-001_legal_ip_master_[DATE].docx
ZKNOT_ACQ-004_acquirer_outreach_master_[DATE].docx
```

### 01_PATENTS — Specs (DOC-SP)
```
ZKNOT_PAT-001_ZKKey_provisional_spec_20260115.docx
ZKNOT_PAT-001_ZKKey_supplemental_spec_attestation_comms_20260122.docx
ZKNOT_PAT-001_ZKKey_provisional_template_ref.docx
ZKNOT_PAT-002_PowerVerify_provisional_spec_v1_20260115.docx
ZKNOT_PAT-002_PowerVerify_provisional_spec_v2_plus_20260311.docx
ZKNOT_PAT-003_TrustSeal_provisional_spec_20260115.docx
ZKNOT_PAT-004_ZKLocalChain_provisional_spec_20260115.docx
ZKNOT_PAT-005_VendorAttest_provisional_spec_v1_20260120.docx
ZKNOT_PAT-005_VendorAttest_provisional_spec_v2_20260303.docx
ZKNOT_PAT-006_EvidenceProtocol_provisional_spec_20260103.docx
ZKNOT_PAT-007_CombinedSession_provisional_spec_x_20260303.docx
ZKNOT_PAT-008_FirmwareFSM_provisional_spec_x_20260303.docx
ZKNOT_PAT-009_OpticalChallenge_provisional_spec_x_20260303.docx
ZKNOT_PAT-010_HumanReadableAttest_provisional_spec_x_20260303.docx
ZKNOT_PAT-011_DualSE_provisional_spec_v1_20260303.docx
ZKNOT_PAT-011_DualSE_provisional_spec_v2_20260303.docx
ZKNOT_PAT-011_DualSE_provisional_spec_v3_final_20260303.docx
ZKNOT_PAT-012_SiliconToSample_provisional_spec_v1_20260303.docx
ZKNOT_PAT-012_SiliconToSample_provisional_spec_v3_final_20260317.docx
ZKNOT_PAT-013_HeartbeatErasure_provisional_spec_20260317.docx
ZKNOT_PAT-014_[name]_provisional_spec_20260317.docx
ZKNOT_PAT-015_DataGapUSBDetect_provisional_spec_20260317.docx
ZKNOT_PAT-016_TrustMeter_provisional_spec_20260317.docx
ZKNOT_PAT-017_TrustMeterPlus_provisional_spec_20260317.docx
ZKNOT_PAT-018_PowerVerifyPlus_provisional_spec_20260317.docx
ZKNOT_PAT-019_SystemUmbrella_provisional_spec_20260403.docx
ZKNOT_DOC-002_TrustKnot_early_platform_draft_ref.docx
```

### 01_PATENTS — Non-Provisional Drafts (PAT-NP)
```
ZKNOT_PAT-NP-001_ZKKey_nonprov_draft_20260328.docx
ZKNOT_PAT-NP-002_PowerVerify_nonprov_draft_20260328.docx
ZKNOT_PAT-NP-004_ZKLocalChain_nonprov_draft_20260328.docx
ZKNOT_PAT-NP-005_VendorAttest_nonprov_draft_20260328.docx
ZKNOT_PAT-NP-006_EvidenceProtocol_nonprov_draft_20260328.docx
ZKNOT_PAT-NP-007_CombinedSession_nonprov_draft_20260328.docx
```

### 01_PATENTS — Supporting Docs (DOC-ME = Micro Entity, DOC-RX = Receipts)
```
ZKNOT_PAT-001_ZKKey_sb15a_micro_entity_cert_20260115.pdf
ZKNOT_PAT-002_PowerVerify_sb15a_micro_entity_cert_20260115.pdf
ZKNOT_PAT-003_TrustSeal_sb15a_micro_entity_cert_20260115.pdf
ZKNOT_PAT-004_ZKLocalChain_sb15a_micro_entity_cert_20260115.pdf
ZKNOT_PAT-005_VendorAttest_sb15a_micro_entity_cert_20260120.pdf
ZKNOT_PAT-006_EvidenceProtocol_sb15a_micro_entity_cert_20260103.pdf
ZKNOT_PAT-007_CombinedSession_sb15a_micro_entity_cert_20260303.pdf
ZKNOT_PAT-008_FirmwareFSM_sb15a_micro_entity_cert_20260303.pdf
ZKNOT_PAT-009_OpticalChallenge_sb15a_micro_entity_cert_20260303.pdf
ZKNOT_PAT-010_HumanReadableAttest_sb15a_micro_entity_cert_20260303.pdf
ZKNOT_TMPL-001_sb15a_micro_entity_cert_blank.pdf
ZKNOT_PAT-001_ZKKey_uspto_payment_receipt_20260115.pdf
ZKNOT_PAT-002_PowerVerify_uspto_payment_receipt_20260115.pdf
ZKNOT_PAT-003_TrustSeal_uspto_ack_receipt_20260303.pdf
ZKNOT_PAT-004_ZKLocalChain_uspto_ack_receipt_20260303.pdf
ZKNOT_PAT-005_VendorAttest_uspto_ack_receipt_20260303.pdf
ZKNOT_PAT-006_EvidenceProtocol_uspto_ack_receipt_20260303.pdf
ZKNOT_PAT-007_CombinedSession_uspto_payment_receipt_20260303.pdf
ZKNOT_PAT-008_FirmwareFSM_uspto_payment_receipt_20260303.pdf
ZKNOT_PAT-009_OpticalChallenge_uspto_payment_receipt_20260303.pdf
ZKNOT_PAT-010_HumanReadableAttest_uspto_payment_receipt_20260303.pdf
ZKNOT_PAT-001_ZKKey_uspto_ack_supplemental_spec_20260122.pdf
ZKNOT_PAT-001_ZKKey_uspto_ack_sb15a_20260303.pdf
ZKNOT_TM-001_ZKNOTmark_uspto_tm_receipt_20260115.pdf
ZKNOT_DOC-001_patent_tracker_20260328.xlsx
```

### 01_PATENTS — Assignments
```
ZKNOT_PAT-001_ZKKey_uspto_assignment_record.pdf
ZKNOT_PAT-002_PowerVerify_uspto_assignment_record.pdf
[... one per application]
```

### 02_CORPORATE
```
ZKNOT_CORP-001_articles_of_incorporation_20260126.pdf
ZKNOT_CORP-002_bylaws_20260126.docx
ZKNOT_CORP-003_ein_assignment_letter_20260126.pdf
ZKNOT_CORP-004_stock_certificate_001_wilkinson_20260126.pdf
ZKNOT_CORP-005_cap_table_20260126.docx
ZKNOT_CORP-006_annual_meeting_minutes_20260401.docx
ZKNOT_CORP-007_utah_annual_report_2026_20260401.pdf
```

### 03_FEDERAL
```
ZKNOT_FED-001_sam_registration_cert_20260317.pdf
ZKNOT_FED-002_sam_renewal_reminder_20270317.txt
ZKNOT_FED-003_vetcert_application_submitted_20260101.pdf
ZKNOT_FED-004_cage_code_1AHZ4_letter_20260101.pdf
ZKNOT_CAP-001_capability_statement_20260301.docx
```

### 04_LEGAL
```
ZKNOT_LGL-001_nda_template_mutual_20260201.docx
ZKNOT_LGL-002_contractor_agreement_template_20260201.docx
ZKNOT_LGL-003_ip_assignment_founder_wilkinson_20260126.docx
ZKNOT_LGL-004_trade_secret_register_20260201.docx
ZKNOT_LGL-NDA-[NNN]_nda_signed_[counterparty]_[DATE].pdf
ZKNOT_LGL-CTR-[NNN]_contractor_agreement_signed_[name]_[DATE].pdf
ZKNOT_LGL-IPC-[NNN]_ip_conception_[patshortname]_[DATE].docx
```

### 05_FINANCIAL
```
ZKNOT_CFO-001_financial_model_3scenario_20260201.xlsx
ZKNOT_CFO-002_qsbs_section1202_memo_20260201.docx
ZKNOT_CFO-BK-[YYYYMM]_bookkeeping_ledger_[YYYYMM].xlsx
ZKNOT_CFO-RX-[YYYYMM]_receipts_[YYYYMM].pdf
ZKNOT_CFO-SBIR-[NNN]_sbir_draft_[agency]_[DATE].docx
ZKNOT_CFO-TX-001_tax_return_2026.pdf
ZKNOT_CFO-BNK-[YYYYMM]_bank_statement_[YYYYMM].pdf
```

### 06_HARDWARE
```
ZKNOT_BOM-001_ZKM001_assembly_kit_20260301.xlsx
ZKNOT_HW-001_ZKM001_hardware_firmware_master_20260301.docx
ZKNOT_PCB-001_ZKM001_kicad_project_20260301.zip
ZKNOT_PCB-001_ZKM001_gerbers_20260301.zip
ZKNOT_PCB-002_PowerVerify_RevE_kicad_project_20260301.zip
ZKNOT_PCB-002_PowerVerify_RevE_gerbers_20260301.zip
ZKNOT_BOM-002_PowerVerify_RevE_bom_20260301.xlsx
ZKNOT_DOC-010_device_id_registry_20260301.xlsx
ZKNOT_HW-002_ZKKeyConnect_build1_wiring_doc_20260301.docx
```

### 07_FIRMWARE
```
ZKNOT_FW-001_ZKKeyConnect_stm32_fw_v0-1_20260315.bin
ZKNOT_FW-002_ZKNOTmodule_fw_v0-1_20260315.bin
ZKNOT_FW-003_PowerVerify_fw_v0-1_20260315.bin
```

### 08_SOFTWARE
```
ZKNOT_SW-001_api_zknot_io_repo_[DATE].zip
ZKNOT_SW-002_zknot_io_site_repo_[DATE].zip
ZKNOT_SW-003_verifyknot_io_repo_[DATE].zip
ZKNOT_SW-004_zknot_python_lib_repo_[DATE].zip
ZKNOT_SW-005_ZK_LocalChain_repo_[DATE].zip
```

### 09_ACQUISITION
```
ZKNOT_ACQ-001_outreach_log_20260301.xlsx
ZKNOT_ACQ-002_data_room_index_20260301.docx
ZKNOT_ACQ-003_acquirer_profile_[name]_20260301.docx
ZKNOT_ACQ-004_acquirer_outreach_master_20260301.docx
```

### 10_MARKETING
```
ZKNOT_MKT-001_demo_script_2min_20260301.docx
ZKNOT_MKT-002_brand_colors_fonts_20260301.docx
ZKNOT_CAP-001_capability_statement_20260301.docx
```

---

## RECOMMENDED ADDITIONS TO FILE NAMING CONVENTION TAB

Add these TYPE codes to the tracker's "File Naming Convention" sheet:

| TYPE | Meaning |
|------|---------|
| CEO | CEO operating documents |
| COO | COO operating documents |
| CFO | Financial documents / CFO operating documents |
| OPS | Operations calendar and scheduling |
| CORP | Corporate formation and equity |
| FED | Federal registrations (SAM, CAGE, VetCert) |
| CAP | Capability statement |
| MKT | Marketing and demo materials |
| SW | Software repo snapshots |
| HW | Hardware master docs |
| TMPL | Blank templates |

---

## GAP: PAT-014 Missing from Tracker

The folder tree shows PAT-011 through PAT-018 in PENDING, but the tracker only has entries through PAT-013 then jumps to PAT-015. PAT-014 appears to have no tracker row. Verify whether PAT-014 was a placeholder that was skipped, or a real application that needs to be added.

---

## FLAT-FOLDER UNIQUENESS CONFIRMATION

Every file listed above is unique by its canonical name, even without folder context, because:
- TYPE code differentiates domain (PAT vs CORP vs FED vs CFO)
- Numeric ID differentiates within type
- ShortName disambiguates within patent series
- Descriptor differentiates document purpose
- Date differentiates versions

The only deliberate duplicates are intentional mirrors:
- `ZKNOT_CAP-001_capability_statement` appears in both 03_FEDERAL and 10_MARKETING (by design — mirrors)
- NDA signed copies mirror between 04_LEGAL and 09_ACQUISITION/NDAS (by design)
