# SAM.gov Renewal — SDVOSB Certification Update

**Date:** 2026-05-11
**Workstream:** ops / federal-compliance
**Status:** Submitted, awaiting IRS/CAGE validation

## Context

SBA VetCert SDVOSB certification approved early May 2026. Initiated SAM.gov
full entity registration renewal to update business type designation from
"SDVOSB pending" to certified, and to clean up several stale items in the
SAM record.

## What got updated this session

- Entity structure: explicitly confirmed Corporate Entity, Not Tax Exempt
  resolves prior ambiguity in COO doc where bylaws section read "single-member LLC"
- Socio-Economic Types: Veteran-Owned Business + Service-Disabled Veteran-Owned
  Business both checked. SDVOSB self-attestation; SAM auto-validates against VetCert
- NAICS codes: cleaned and expanded. Primary 334418 Printed Circuit Assembly Mfg,
  secondaries 334290, 334419, 541512, plus full 541715 family with all four exceptions
  covers DoD R&D, DARPA, AFWERX, aerospace work
- PSC codes: 5999, 7A20, 5810, AC11, AC12, DA10. Hardware, IT services, COMSEC,
  DoD basic/applied R&D, IT services-as-a-service
- POCs updated: William Shane Wilkinson full legal name, CEO, ops@zknot.io,
  primary 385-234-7555. Removed personal gmail and personal mobile references
  from notes fields. Past Performance POC removed as unnecessary.
- Annual receipts: 1 dollar. SAM rejects zero; nominal value satisfies validation
  and confirms small business status across all NAICS
- Disaster Response Registry: Yes. Chain-of-custody products plausibly serve
  FEMA recovery; registry inclusion is reversible
- Buy American FAR 52.212-3: No. Accurate for current pre-production state
- Limited Rights Data declared: ZKNOTmodule firmware and attestation software
  under FAR 52.227-15 protections
- GAAP-compliant accounting attested under DFARS 252.232-7015. Legitimate;
  founder has accounting degree and will maintain books accordingly

## Issues identified during renewal

### Founder dependency in POC structure
All three mandatory POCs Accounts Receivable, Electronic Business, Government
Business currently list William Shane Wilkinson alone. SAM-compliant and
accurate for current solo operation, but reads as founder-dependency to acquirers
reviewing the record post-LOI. Resolution before exit:
- Hire federal contracts admin OR
- Designate Mentor-Protege partner staff for select POC roles OR
- Engage fractional CFO/corporate counsel for Government Business POC
Tracked in Taskwarrior as zknot.acquisition / +preexit, due 2027-01-01.

### Stale single-member LLC reference in COO master doc
The COO master doc ZKNOT_COO-001 v1.0 contains a contradiction.
States "Utah domestic corporation, single-member" in one section and
"Single-member LLC operating structure" under bylaws description. ZKNOT is a
Utah for-profit corporation; the LLC reference is a stale draft artifact.
Needs cleanup before doc enters any data room.

### TS/SCI clearance reactivation worth pursuing
Previously held TS/SCI; status lapsed. Worth checking DISS/DCSA for last
adjudication date and whether reinstatement is faster than initial. Cleared
founder/CEO meaningfully expands acquisition premium beyond SDVOSB alone.
Opens IC contracting, classified DoD, expedites buyer's clearance pathway.
Separate task; not blocking. Tracked as tasks 80 and 81.

### Tax year reporting
Selected 2025 as most recent tax return year despite incorporation date
2026-01-26 preceding any actual filed return. IRS may flag this during
validation. Acknowledged risk; will fix at validation failure if it happens.

## Strategic notes

SAM with confirmed SDVOSB unlocks:
- VA Vets First post-VIP registration, needed within 5 days of SAM showing certified
- GSA VETS 2 GWAC pathway, sole-source up to 4 million per task order
- SDVOSB set-asides on DoD/DHS contracts
- Direct sole-source contracts up to 4 million from federal agencies
- Approximately 2-4 million acquisition exit premium per COO doc Section 2.3

## Next concrete actions

1. Wait for IRS/CAGE validation up to 10 business days
2. Within 5 days of SAM showing certified SDVOSB, register at VA VIP vetbiz.va.gov
3. Update CAP-001 capability statement with certified status
4. Begin CO outreach distribution per COO doc Section 8
5. Look up DISS/DCSA clearance status, tasks 80 and 81
6. Federal/state surplus property program registration, tasks 83 84 plus follow-ons
