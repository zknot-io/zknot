# ZKNOT Organization & Filesystem Handoff

**Date:** April 27, 2026
**From:** KM/PM setup session
**To:** Next Claude conversation, or future-Shane reviewing in 6 months

---

## Why this document exists

This session was supposed to be about picking a knowledge management and project
tracking system. It ended up also being a filesystem cleanup, dev environment
audit, and disk space reclamation. None of that belonged in the KM conversation
proper, but the decisions made are worth preserving so they don't get re-litigated.

---

## Filesystem layout decisions (current state)

### Canonical paths
```
~/ZKNOT/                  Linux primary working tree (also C:\ZKNOT\ on Windows)
├── 00_COMMAND/           Top-level operating docs, this kind of handoff
├── 01_PATENTS/           IP filings, drafts, attorney correspondence
├── 02_CORPORATE/         Legal entity, SAM.gov, EIN docs
├── 03_FEDERAL/           Government procurement, federal contracting
├── 04_LEGAL/             Contracts, NDAs, advisor agreements
├── 05_FINANCIAL/         Bookkeeping, banking, expense records
├── 06_HARDWARE/          KiCad projects, BOMs, datasheets
├── 07_FIRMWARE/          STM32 source, build artifacts
├── 08_SOFTWARE/          Backend (Railway), frontend (Cloudflare), ZK-LocalChain
├── 09_ACQUISITION/       Acquirer outreach, due diligence prep
├── 10_MARKETING/         Social, web copy, press kits
├── 11_KM/                Knowledge management vault — markdown notes
├── 12_JOURNAL/           Working journal, reference docs (cheat sheets, etc.)
├── 99_ARCHIVE/           Cold storage — old session backups, retired projects
├── 99_SENSITIVE/         Encrypted secrets (TODO: actually encrypt this)
└── scripts/              Shell scripts, automation
```

### Reference docs go to 12_JOURNAL
The Taskwarrior cheat sheet PDF lives in `~/ZKNOT/12_JOURNAL/`, symlinked
from `~/ZKNOT/11_KM/` for convenience. Pattern: durable reference material
that's read repeatedly belongs in 12_JOURNAL; live thinking and project
notes go in 11_KM.

### Notes vault is plain markdown + git
`~/ZKNOT/11_KM/` is just `git init`ed and contains markdown files. No Obsidian,
no Logseq, no Roam. Tasks reference notes by filename
(e.g. `task 7 annotate "see notes/pv-rev1-potting.md"`). Notes reference
task IDs by inline text. `grep -r` is the search tool.

---

## What got removed this session

### Disk space reclaimed: ~32 GB total
- 13 "Books & Study Materials" zips in Downloads (~26 GB) — already extracted to ~/LIBRARY
- 3 pre-migration ZKNOT_BIZ snapshots (~600 MB) — superseded by git
- Patent zip duplicate, files*.zip mystery zips, duplicate docx, duplicate KiCad files
- CUDA keyring deb (one-time installer, useless after install)
- Two HTB VPN configs (cybersecurity masters coursework, complete)
- T55xx RFID lab dumps
- `.cache/` folder (~4.7 GB browser/OS cache)

### Software removed
- Metasploit framework + ~/.msf4 + ~/.ZAP (~1.4 GB)
- hashcat + hashcat-data
- john (John the Ripper) + john-data

These were cybersecurity masters coursework artifacts, not ZKNOT tooling.
Easy to reinstall via apt if needed for security testing. Keeping nmap and
Wireshark since those are legitimately useful for hardware development.

### Notes archived then removed
46 cybersecurity course notes from `~/org/roam/` covering Payloads, Meterpreter,
Reverse Shells, Hashcat, MSFvenom, Wordlists, XSS, etc. Tarred to
`~/ZKNOT/99_ARCHIVE/cyber_masters_notes_backup_20260427.tar.gz` as a 24-hour
safety net before deletion. **If you're reading this more than 24 hours after
April 27, 2026, that tar is safe to delete (or already gone).**

### Inert reverse-shell filename
A zero-byte file with a PowerShell reverse-shell payload as its filename was
sitting in `~/`. Self-inflicted from a CTF/lab exercise. Deleted. Not malware,
just a filename artifact.

---

## What stays

- **org-mode tree at `~/org/`** — has agenda, journal, projects, attachments,
  observational notes. Keep it. The Roam subfolder lost its security notes
  but the rest is intact. Eventually consider a read-only bridge so org-agenda
  can see Taskwarrior tasks without dual-writing — Taskwarrior remains the
  source of truth.
- **`~/LIBRARY/`** — 26 GB of books and study materials, extracted and intact
- **`~/ZKNOT_STAGING/`** — old OneDrive snapshot, scheduled for deletion in
  ~8 days per the dev env migration plan (2-week passive backup window)
- **`~/Downloads/ZKNOT_BIZ/`** — same as above, also scheduled for deletion
  May 8, 2026

---

## Dev environment status

The dev-env migration handoff is complete:
- ZKNOT_BIZ moved off OneDrive to `~/ZKNOT/`
- `gh repo create zknot/zknot --private --source=. --push` done
- KiCad ZKNOT_LIB paths configured on both Linux and Windows
- `.gitignore` and `.gitattributes` written and committed
- Backend repos (`software/backend/`, `software/verifyknot-frontend/`) remain
  separate from the monorepo because they have their own deploy hooks

Open items from that handoff that remain:
- README.md for the monorepo
- Unlink OneDrive Desktop/Documents redirects on Windows (currently still
  active, low risk but should be done)
- Establish weekly `git clone --mirror` to USB SSD habit

---

## Knowledge management system (the actual ask)

**Tool:** Taskwarrior 2.6.2 + Timewarrior 1.7.1, plus markdown vault at
`~/ZKNOT/11_KM/`. Selected because:

- CLI-native, scriptable, Linux-first
- Real dependency tracking (the killer feature for the boards-must-arrive-
  before-assembly workflow)
- Custom UDAs for cost, involvement, workstream
- No SaaS, no vendor, free, open-source
- Spreadsheet escape hatch via `task export | jq` to CSV
- All data in `~/.task/`, git-tracked

**Why not the alternatives that came up:**
- Notion — flexible but weak dependency tracking, SaaS, GUI-only
- Linear — strong on tasks but weak as KM, SaaS
- Obsidian — good notes but task layer requires plugin combinations
- Logseq — same as Obsidian
- Roam — Shane was deep in this previously, didn't stick
- Custom SQLite + scripts — would become a project of its own

**Configuration choices:**
- 6 workstream values: hw, fw, sw, ip, biz, ops
- 5 involvement values: solo, liz, lawyer, contractor, vendor
- Custom reports: `task next`, `task ready`, `task blocked`, `task stream`
- Urgency tuning: dependencies dominate (blocking +10, blocked -10),
  due dates strong (+12), priority moderate, age slow drift
- bulk=3 (confirms above 3 tasks), confirmation=yes

**Reference card:** Two-page laminate-quality PDF at
`~/ZKNOT/12_JOURNAL/ZKNOT_Taskwarrior_Cheatsheet.pdf`

---

## Task seed outcome

71 tasks were extracted from 7 prior session handoffs (PV-Rev1 ship-it,
labeling/potting, dev env migration, Logic 2 MCP, ZKKey Connect build guide,
execution pack, PV-THT routing, ZKKey Air, email triage). After a pruning
pass, 26 tasks were closed as already-done, leaving 59 active.

Active state at end of session:
- PV-Rev1: ordered, awaiting boards. Parallel-path label/potting shopping
  remains.
- ZKKey Connect: bumped to High priority, near-term deliverable, chain wired.
- ZKKey Air: parked with explicit unpark condition ("after ZKKey Connect
  prototype validates the attestation flow").
- Patents: PAT-019 disclosure draft started (active).
- Verifyknot: deployed; CORS check and endpoint test remain.
- Biz: acquirer outreach template, Liz handoff doc, Instagram setup, Reddit
  karma all pending.

Total cost captured in tasks: $19,601 (mostly the $18K patent conversion
budget, plus ~$1,100 in Rev1 labeling/potting supplies).

---

## What didn't get done in this session (open loops)

- README.md for the ZKNOT monorepo (task in queue)
- Encrypting `~/ZKNOT/99_SENSITIVE/` — flagged in dev env handoff, never
  resolved. Should use age, gpg, or a per-file approach.
- The actual Taskwarrior context setup (`task context define rev1
  project:pv-rev1`) was suggested but not executed
- A read-only Taskwarrior → org-agenda bridge for those moments when org-mode
  is the right view
- Decision on Path A vs Path B for the PV-Rev1 enclosure mold STL
- The Lightning Labels quote email
- The 5 PCB measurements needed before final mold STL generation

---

## Patterns worth preserving

1. **Brain-dump beats organization.** Adding tasks fast and pruning later
   produced a better list than trying to curate as we went.

2. **Verify before destroy.** Every deletion in this session was preceded by
   a `du -sh` or `ls` check. The "show what would be deleted, ask y/n, then
   delete" pattern caught nothing dangerous but reinforces the right habit.

3. **Tar before delete for anything mildly uncertain.** The cybersecurity
   notes got tarred to 99_ARCHIVE before deletion. 24-hour safety nets are
   cheap.

4. **One conversation, one outcome.** This session almost sprawled into
   five tracks. Pulling back to "pick a KM tool, set it up" and parking the
   rest produced a working system. The hardware/firmware/biz tracks each
   need their own conversations.

5. **Dependencies are the point.** The "boards must arrive before assembly"
   pattern is what made Taskwarrior the right answer. Any future tool review
   should re-test this requirement first.

---

## If this all gets lost

The setup is reproducible from:
- `~/.taskrc` (the config)
- `~/.task/` (the data, git-tracked)
- `~/ZKNOT/12_JOURNAL/ZKNOT_Taskwarrior_Cheatsheet.pdf` (the reference)
- This document

Plus `apt install taskwarrior timewarrior` on any Debian-family system.

---

*Page 1 of 1*
