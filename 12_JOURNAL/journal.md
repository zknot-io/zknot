# ZKNOT Operations Journal

## Format
[DATE] | Focus: ... | Done: ... | Blockers: ... | Next: ...

---

## 2026-04-18
Focus: File structure organization — extracted ZKNOT_BIZ zip, organized into ~/ZKNOT/, purged old cybersec environment
Done: Full file sort complete, 99_SENSITIVE isolated, ~600MB+ junk removed
Blockers: None
Next: Deploy verifyknot.io frontend to Cloudflare Pages, continue Saleae/MCP I2C integration


## 2026-04-18 — Full System Setup Session
Focus: File org, security hardening, GitHub setup, stack verification
Done:
- Extracted ZKNOT_BIZ zip, organized entire business file structure into ~/ZKNOT/
- Purged all HTB/cybersec environment (~600MB+ removed)
- Generated ed25519 SSH key (id_ed25519_zknot) for zknot-io GitHub org
- Generated 4096-bit GPG key (943C48B0FC7404D2, expires 2028-04-17)
- Registered YubiKey 4/5 FIDO2 resident SSH key
- Fixed multi-account SSH conflict (github-zknot host alias)
- Committed patents, firmware source, KM docs, journal to zknot-io/zknot
- Smoke tested full stack: health ✅  verify ✅  fake code error ✅  frontend ✅
- Generated and saved developer handoff doc to 10_KM/
Blockers: 99_SENSITIVE not encrypted yet — plaintext on disk
Next: Encrypt 99_SENSITIVE, continue Saleae/MCP I2C work, attorney for PAT-001/PAT-002
