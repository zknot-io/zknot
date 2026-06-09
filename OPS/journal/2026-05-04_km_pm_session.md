# Session Journal — KM/PM System Buildout & Cleanup

**Date:** 2026-05-04 (covers work from 2026-04-24 through 2026-05-04)
**Topic:** Knowledge management + project tracking system selection, filesystem cleanup, task seeding, journal/memory conventions, zknot.org strategic question.

---

## Why this session happened

Started as "I'm going 1000 different directions, I need a proper KM solution and
a project tracker that handles dependencies." Ended up also covering filesystem
cleanup, disk reclamation, dev environment audit, password manager consolidation
notes, and a strategic question about zknot.org. This entry captures all of it
so the originating conversation can be deleted.

---

## DECISION: Taskwarrior + Timewarrior as the KM/PM system

**Chosen tool:** Taskwarrior 2.6.2 + Timewarrior 1.7.1, plus a markdown notes
vault. CLI-native, scriptable, Linux-first, real dependency tracking, free,
open-source, no SaaS, no vendor lock-in.

**Why not alternatives:** Notion (weak deps, SaaS, GUI), Linear (weak as KM),
Obsidian/Logseq (notes good, tasks need plugin stacks), Roam (was used before,
didn't stick), custom SQLite (would become its own project).

**The deciding factor:** dependency tracking. "Boards must arrive before
assembly, firmware must flash before test" — this is the capability that made
Taskwarrior the right call. Any future tool review should re-test this first.

### Configuration

- Config: `~/.taskrc`
- Data: `~/.task/` (git-tracked, commit after changes)
- Custom UDAs: workstream (hw/fw/sw/ip/biz/ops), involvement
  (solo/liz/lawyer/contractor/vendor), cost (numeric), estimate (duration)
- Custom reports: `task next`, `task ready`, `task blocked`, `task stream`
- Urgency tuning: dependencies dominate (blocking +10, blocked -10), due dates
  strong (+12), priority moderate, age slow drift
- bulk=3, confirmation=yes

### Daily usage (the only loop that matters)

```
task                  # what's ready, by urgency — your "what next" view
task N start          # + timew start "..." to track time
# do the work
task N done           # dependents auto-unblock
```

### Reference card

Two-page laminate-quality PDF at
`~/ZKNOT/3_OPS/journal/ZKNOT_Taskwarrior_Cheatsheet.pdf`

---

## CONVENTIONS established this session

### Folder structure (v2 S-shop, per KM-001)

```
~/ZKNOT/
├── 00_COMMAND/   CEO/COO/CFO/CCO/CTO subdirs, session handoffs, resume
├── 01_PATENTS/   IP filings (untouched, already well-organized)
├── 1_PERS/       Personnel (placeholder)
├── 2_INTEL/      Intelligence/research (placeholder)
├── 3_OPS/        km/ (notes vault) + journal/ (dated entries + cheat sheet)
├── 4_LOG/        Logistics (placeholder)
├── 5_PLANS/      Acquisition, strategy
├── 6_SIG/        hardware/ firmware/ software/
├── 7_ENG/        Marketing, engagements
├── 8_FIN/        Finance
├── 9_GOV/        Federal, SAM
├── JAG/          CORPORATE/ + CONTRACTS/
├── 99_ARCHIVE/   Cold storage
└── scripts/      Automation (leftover, needs a home)
```

### Journal entries
- Path: `~/ZKNOT/3_OPS/journal/YYYY-MM-DD_topic.md`
- Style: prose with sections, not bullet-dumps
- Commit: `cd ~/ZKNOT && git add 3_OPS/journal/ && git commit`
- Use journal for state-change records (what was true, what is now, what
  conventions to follow). Use Taskwarrior for actionable to-dos with due dates.

### Notes vault
- Path: `~/ZKNOT/3_OPS/km/` (markdown + git, no Obsidian/Notion)
- Link tasks to notes via `task N annotate "see km/file.md"`

### Both saved to Claude permanent memory
So future conversations know the paths and patterns without re-explaining.

---

## CLEANUP performed (~32 GB reclaimed)

- 13 "Books & Study Materials" zips in Downloads (~26 GB) — already extracted
  to ~/LIBRARY
- 3 pre-migration ZKNOT_BIZ snapshots (~600 MB) — superseded by git
- Patent zip dupe, files*.zip mystery zips, duplicate docx/KiCad files
- CUDA keyring deb, 2 HTB VPN configs, T55xx RFID lab dumps
- `.cache/` (~4.7 GB)
- Offensive security stack: Metasploit + .msf4 + .ZAP + hashcat + john (~1.4 GB)
  — cybersecurity masters coursework artifacts, not ZKNOT tooling. Kept nmap +
  Wireshark (legit hardware dev use).
- 46 cybersecurity course notes from ~/org/roam/ — tarred to 99_ARCHIVE first
  as 24-hr safety net, then deleted
- An inert zero-byte file whose NAME was a PowerShell reverse-shell payload
  (self-inflicted CTF artifact, not malware) — deleted

Separately, a v2 filesystem reorg dropped the ZKNOT tree from 808M to 113M.

---

## TASK SEEDING

71 tasks extracted from 7 prior session handoffs. Pruning pass closed ~26 as
already-done. Then added 13 more across two new chains (ZKKey Connect Pico +
PowerVerify final assembly) and the zknot.org tasks.

### Active project state at session end

- **PV-Rev1:** Ordered, awaiting boards. Final assembly chain wired:
  boards arrive → reflow bake → solder pigtails → pot → ZK-LocalChain record →
  verifyknot.io verify. Parallel label/potting shopping list still to order.
- **ZKKey Connect Pico (NEAR-TERM PRIORITY):** ATECC provisioning is #1.
  Chain: provision ATECC → finish backend sign/verify (Linux+Windows) →
  finalize KiCad → order PCB from JLCPCB → 3D print case → tamper evidence →
  marketing video.
- **ZKKey Air:** Parked. Unpark condition: "after ZKKey Connect prototype
  validates the attestation flow." It's the patent crown jewel (PAT-009,
  true air-gap, QR-only) but comes after Connect proves the model.
- **Patents:** PAT-019 optical PUF disclosure draft started (active).
  PAT-009, PAT-002, attorney check-in queued.
- **Verifyknot:** Deployed to Cloudflare Pages. CORS check + endpoint test
  remain.
- **Biz:** Acquirer outreach template, Liz handoff doc, Instagram, Reddit
  karma — all pending, none blocking.

### Strategic note: two ZKKey Connect chains exist
- Older "RevA" path (build guide → fix script → gerber → PCB → firmware)
- Newer "Pico" path (ATECC → backend → KiCad → PCB → 3D print → tamper → video)
- TODO with fresh eyes: decide if RevA tasks are stale and should be deleted,
  or if they merge into the Pico path. Likely RevA is superseded.

---

## zknot.org — STRATEGIC QUESTION (deferred, captured here)

### The idea (Shane's words)
Spin up zknot.org with Gumroad. Sell SOPs not-for-profit to get people's ideas
protected, or give ZKNOT-specific GRC advice, or serve dissidents/whistleblowers
and training purposes. Self-described concern: "might be too self-serving, but
the org helps me separate the business from the legitimately important task of
protecting ideas that aren't for profit."

### Assessment (from this session)
**Not self-serving — it's a coherent extension of the patent stance.** A year
and ~$18K spent protecting ideas; making idea-protection accessible to
non-commercial creators is consistent with that. ZK-LocalChain attestation works
for "I conceived this on this date" as well as "this hardware is genuine."

**But a .org selling SOPs on Gumroad is a confused product.** Three distinct
options, pick ONE:

1. **Free public-good attestation** — anyone timestamps+signs an idea on
   ZK-LocalChain via verifyknot.io, no charge, no Gumroad. The
   dissident/whistleblower mission tool. ZKNOT, INC. (.io) sells the hardware
   that makes it tamper-evident. **(Strongest option — makes the .org a mission
   statement that strengthens the .io commercial story.)**
2. **Paid SOPs at cost** — Gumroad fits if SOPs are the product, but then it's
   a low-margin info-product, not really a non-profit move.
3. **GRC advisory** — real consulting offer, but advisory liability is real
   (needs professional liability insurance, separate brand, separate risk).

Mixing all three muddles the message and gives acquirers reason to ask
uncomfortable scope questions.

### Tasks created (in Taskwarrior, project:zknot-org)
- STRATEGIC (priority M): Define zknot.org scope — pick one of the three above
- Prep tasks (priority L, parked): domain registration, mission statement,
  hosting decision, attorney UPL check if scope #1, liability insurance
  research if scope #3
- All prep tasks should depend on the strategic decision before they unblock

### Timing
zknot.org is a Q3 conversation, not this-week. The strategic task is priority:M
so it stays in peripheral vision; execution is all priority:L. Do NOT let it
compete with ATECC provisioning, ZKKey Connect, or PowerVerify shipping.

---

## PASSWORD MANAGER CONSOLIDATION (separate journal entry exists)

Consolidated to Bitwarden on 2026-05-04. Full detail in
`3_OPS/journal/2026-05-04_password_consolidation.md`. Open follow-up: delete
LastPass account ~2026-05-11 (Taskwarrior task 60).

---

## OPEN LOOPS carried forward (not done this session)

- README.md for the ZKNOT monorepo
- Encrypt `~/ZKNOT/99_SENSITIVE/` (flagged repeatedly, still unresolved — note:
  v2 reorg may have moved this; there's also a ~/ZKNOT_VAULT age-encrypted
  archive that is the disaster-recovery copy)
- GitHub push: earlier push rejected ("remote contains work you don't have") —
  origin/main has commits local doesn't. Investigate with `git fetch origin`
  then compare `git log main ^origin/main`. Decide merge vs force-with-lease
  with fresh eyes.
- Taskwarrior context setup: `task context define rev1 project:pv-rev1` was
  suggested, never executed
- Read-only Taskwarrior → org-agenda bridge (org tree still at ~/org/)
- Decide RevA vs Pico ZKKey Connect chains (likely delete RevA)
- PV-Rev1 enclosure mold: Path A (study STL now) vs Path B (wait for board
  measurements)
- Lightning Labels quote email
- 5 PCB measurements needed before final mold STL
- Two deferred personal threads with full handoffs written (NOT in this repo,
  belong in a separate personal conversation):
  - Personal git-based file organization (chezmoi, git-crypt, restic to B2)
  - Off-Google migration for personal accounts (deferred to Q3)

---

## PATTERNS worth keeping

1. Brain-dump beats organization — add fast, prune later
2. Verify before destroy — `du`/`ls` check before every deletion
3. Tar before delete for anything uncertain — cheap 24-hr safety nets
4. One conversation, one outcome — don't let sessions sprawl across all tracks
5. Dependencies are the point — the whole reason for the tool

---

## REPRODUCIBILITY

If everything is lost, the setup rebuilds from:
- `~/.taskrc` (config)
- `~/.task/` (data, git-tracked)
- `~/ZKNOT/3_OPS/journal/ZKNOT_Taskwarrior_Cheatsheet.pdf` (reference)
- `~/ZKNOT/00_COMMAND/ZKNOT_Organization_Handoff_20260427.md` (the org handoff)
- This journal entry
- `apt install taskwarrior timewarrior`

---

*This entry exists so the originating Claude conversation can be safely deleted.*
