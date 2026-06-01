<!--
ROOT PRIMER — how to use this file
- This is the FIRST thing you open after a trip/gap, and the FIRST thing you paste to any AI.
- It is an INDEX + TRIAGE, not a summary of everything. One line per project. Pointers, not detail.
- Detail lives in each project's own primer (00_COMMAND/primers/<project>.md) and in km/systems/ + journal/.
- MAINTENANCE RULE: update the relevant line here as the LAST step of any work session. A stale primer lies.
- Fields marked >>FILL<< are my guesses or blanks — correct them; don't trust them as-is.
- "Last verified" date at the bottom tells you (and any AI) how much to trust this file.
-->

# ZKNOT — ROOT CONTEXT PRIMER

**Operator:** William Shane Wilkinson — founder/operator, ZKNOT, INC. (Salt Lake City, UT)
**What ZKNOT does (2 sentences):** >>FILL: one or two plain sentences — the thing you'd tell a stranger. e.g. "ZKNOT builds hardware-rooted, human-gated cryptographic attestation devices that prove a real person performed an action at a real time. Products: PowerVerify, ZKKey Connect/Air."<<
**Federal status:** SDVOSB-certified (SBA VetCert, ~May 2026). Active SAM.gov (UEI C4SKW13JPEL5, CAGE 1AHZ4, renewal 2027-03-17). SBIR is NOT an active path.

---

## 🔥 ON FIRE / TIME-SENSITIVE (what bites if ignored)

- >>FILL: the 1–3 things with real deadlines or decay. Candidate from records: 6 provisional patents → non-provisional conversions due 2027-03-01 (long fuse but expensive to miss).<<
- >>FILL<<

## ⛔ BLOCKED ON ME (won't move until I act)

- >>FILL: things waiting on a decision/action only you can make.<<

## 🆕 SINCE LAST SESSION (rolling — clear when stale)

- 2026-06-01: Centralized storage live — `~/ZKNOT` vault is now an SMB share, mounted `Z:` on Windows via `\\mt\share`. `99_SENSITIVE` + `01_PATENTS` veto'd off the network. NAS deferred (build-as-income). See journal 2026-06-01.

---

## ACTIVE PROJECTS (one line each — status: 🔥hot / 🟡warm / 🅿️parked)

> Rule: a project earns its own primer ONLY while active. Parked = one line here, no primer.

| Project | Status | One-line state | Next action | Primer |
|---|---|---|---|---|
| **Patents** | >>?<< | 6 provisionals; conversions due 2027-03-01 | >>FILL<< | `primers/patents.md` |
| **NAS / infra** | 🟡 | Storage live; NAS deferred, parts-as-income; INFRA-002 pending forks | Stand up offsite backup; pick INFRA-002 forks | `primers/infra.md` |
| **HW provisioning** | >>?<< | Pivoted ATECC → FT260 USB-I2C bridge for bare TrustCUSTOM (TFLXTLS) | >>FILL<< | `primers/hw-provisioning.md` |
| **API / verifyknot** | >>?<< | FastAPI on Railway (api.zknot.io); verifyknot.io was ready for final Cloudflare deploy | >>FILL: is verifyknot deployed yet?<< | `primers/backend.md` |
| **PV1 manufacturing** | >>?<< | >>FILL: current unit/cure/ship state<< | >>FILL<< | `primers/pv1.md` |
| **Federal / SDVOSB / gov** | >>?<< | SDVOSB certified; surplus monitoring; >>FILL: APEX/outreach state<< | >>FILL<< | `primers/gov.md` |
| >>add/remove rows so this list = your REAL 4–5 active + any parked<< | | | | |

---

## STABLE FACTS (rarely change — pointers, not detail)

- **Legal name (all filings/signatures):** William Shane Wilkinson (not "Shane Wilkinson")
- **Federal account email:** shane.systems@gmail.com
- **Registered address:** 1884 W Sir Charles Dr, Salt Lake City, UT 84116-4652
- **Vault:** `~/ZKNOT/` (00_COMMAND → 99_ARCHIVE), git-tracked. Repos: `~/zknot-api`, `~/verifyknot-site`. GitHub org: zknot-io.
- **Storage:** `~/ZKNOT` = SMB share, Windows `Z:` via `\\mt\share`. How-it-works → `km/systems/network-storage.md` (>>to be written<<)
- **Backup status:** ⚠️ INTERIM — manual upload to ops@zknot.io + shane.systems@gmail.com Google Drives every ~2 days. restic→SSD+B2 deferred to NAS arrival. **Vault is otherwise single-copy on one disk.**
- **Patent backup:** `01_PATENTS/` excluded from git, "backed up off-repo" — >>VERIFY this is real and restorable<<
- **Dev env:** Debian Trixie 13, zsh, Taskwarrior+Timewarrior. Reports: `task next/ready/blocked/stream`.

---

## HOW TO BRIEF AN AI WITH THIS

1. Paste this file first.
2. Then paste the relevant project primer (`primers/<project>.md`).
3. Only then point at vault detail if the task needs it.
> Goal: max signal, min tokens. This file + one project primer should orient any model in 2 reads.

---

**Last verified:** 2026-06-01 (by Shane, partial — >>FILL<< fields still open)
**Maintenance:** update the changed project's row + 🆕 section as the last step of each work session.

Page 1 of 1
