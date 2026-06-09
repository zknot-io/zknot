# 2026-05-02 — KM Migration & v2 Folder Reorg

## Outcome
Full ZKNOT file structure migration completed. Tree 808M → 113M (86% reduction).
Three commits on local `main`, 3 ahead of `origin/main` — NOT pushed yet.

## Commits
- bb91853  Pre-migration baseline
- c5bad04  Migration: merge fresh Drive export, quarantine superseded designs (296 files)
- 8ed1ccd  v2 reorg: apply S-shop folder structure per KM-001 strategy

## Old → New folder mapping (CRITICAL — other threads reference old paths)
| Old | New |
|---|---|
| 02_CORPORATE | JAG/CORPORATE |
| 03_FEDERAL | 9_GOV |
| 04_LEGAL | JAG/CONTRACTS |
| 05_FINANCIAL | 8_FIN |
| 06_HARDWARE | 6_SIG/hardware |
| 07_FIRMWARE | 6_SIG/firmware |
| 08_SOFTWARE | 6_SIG/software |
| 09_ACQUISITION | 5_PLANS |
| 10_MARKETING | 7_ENG |
| 11_KM | 3_OPS/km |
| 12_JOURNAL | 3_OPS/journal |
| 00_COMMAND | 00_COMMAND (+ CEO/COO/CFO/CCO/CTO subfolders) |
| 01_PATENTS | 01_PATENTS (unchanged) |
| 99_ARCHIVE | 99_ARCHIVE (unchanged) |

## Sensitive vault
- ~/ZKNOT_VAULT/sensitive_v3_20260502.tar.gz.age (age -p passphrase, in password mgr)
- 4,916,372 bytes, mode 600, byte-verified via SHA-256
- Contents: bank PINs (BofA, Capital One), DD-214s, VA letter, identity docs,
  Stripe + Shopify recovery codes, credentials reference
- Passphrase stored in password manager

## Quarantine / deletions
- ~/ZKNOT_QUARANTINE/{kicad_backups,kicad_designs_superseded,llm_drafts,zknotmodule_superseded,residual}/
- ~/ZKNOT_REFERENCE_LIB/usb_specs/ (39 USB-IF public specs)
- DELETED: 06_HARDWARE/tools/ (567MB STM32 vendor toolchains)
- DELETED: 06_HARDWARE/firmware/ (67MB Eclipse workspace dupe; real fw preserved at 6_SIG/firmware)
- KiCad: ONLY PowerVerify-Rev1 kept active; all other designs (ZKKey, Goldfinger, zkmodule, PV variants) quarantined
- Personal/medical files shredded (all confirmed in Google Drive backup first)

## Decisions made (don't relitigate)
- Hybrid git model: git tracks structure/text/code; binaries (.docx/.pdf/.png) gitignored, stay on disk
- Aggressive quarantine over indecision
- PowerVerify-Rev1 is the only active KiCad design (hardware direction changed)
- Migration on branch, not pushed — gives rollback room

## Backend API location note
api.zknot.io (FastAPI/Railway) backend code is likely a SEPARATE repo, NOT in ~/ZKNOT.
Check ~/ for sibling repos (zknot-api). The ~/ZKNOT tree is docs/design-heavy.

## OPEN LOOPS (pick up after trip)
1. PUSH: origin/main rejected earlier ("remote contains work you don't have").
   Investigate with: git fetch origin; git log origin/main --oneline -5; compare to local.
   Decide merge-down vs force-with-lease WITH FRESH EYES.
2. Move ~/ZKNOT_STAGING/ and ~/Downloads/ZKNOT_BIZ/ → ~/ZKNOT_FROZEN_SNAPSHOTS/
3. Rotate Stripe + Shopify recovery codes (old ones in vault become invalid after)
4. 19 doubled-extension files (.docx.docx, .pdf.pdf) in canonical — cosmetic, fix later
5. Sort 00_COMMAND/*.docx into role subfolders (CEO/COO/CFO/CCO/CTO) — needs domain knowledge
6. Empty placeholder folders: 1_PERS, 2_INTEL, 4_LOG — fill as work happens
7. scripts/ folder at top level — leftover, decide where it belongs
8. git-crypt + MANIFEST.md session (~2hr, separate, per KM-002)
9. Bitwarden install (AppImage from bitwarden.com — apt/snap both failed)

## Handoffs drafted (ready to paste into new threads)
- KM-002 scope note (ZKNOT company files only; personal + off-Google out of scope)
- Thread B: Personal Git-Based File Org (chezmoi/git-crypt/restic-B2/Codeberg mirror)
  - WATCH: don't migrate existing age vault into git-crypt; keep age as DR copy
  - ADD: B2 account/bucket as step 0; personal git identity email decision

## NOT in this thread (flagged, unresolved)
- ATECC608 provisioning brief (Demo Unit serials, CRC spec, 0x0F finding, Demo Unit #2 role)
  came from a DIFFERENT thread — findings NOT in this conversation.
  Source: search past chats for "ATECC608 provisioning" / check ~/ZKNOT/3_OPS/km/ /
  Curves of Trust drafts / Microchip datasheet.
