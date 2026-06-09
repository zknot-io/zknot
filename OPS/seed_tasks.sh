#!/bin/bash
# ZKNOT Task Seed — extracted from 7 handoff documents, April 24 2026
# Safe to re-run: task add creates duplicates, so only run once or prune after.

set -e

echo "Seeding Taskwarrior with tasks mined from handoffs..."
echo "This will add ~60 tasks across all workstreams."
echo ""

# ============================================================
# PV-REV1 SHIP-IT (Powerverify Rev 1 — already partially seeded)
# New tasks extend the existing chain + catch things the first
# seed pass missed.
# ============================================================

# ---- Hardware: PCB gerber + order (1,2,3 already exist) ----
task add project:pv-rev1 workstream:hw priority:H \
  "Run DRC in KiCad on PV-THT-V2-CANONICAL — zero errors before gerber export"

task add project:pv-rev1 workstream:hw priority:H \
  "Fill GND pour on B.Cu layer (press B in PCB editor)"

task add project:pv-rev1 workstream:hw priority:H \
  "Route 0.8mm VBUS power nets: WH1 → D3.A → D3.K → FB1 → D1 → WH7 chain"

task add project:pv-rev1 workstream:hw priority:H \
  "Route 0.4mm LED power tap traces (R1/R2 to LED1/LED2, R12 to LED7)"

task add project:pv-rev1 workstream:hw priority:H \
  "Route 0.25mm signal traces (U1 PG, FLAG20, CC1, CC2, CFG1-3, R8-R11 to LEDs 3-6)"

task add project:pv-rev1 workstream:hw priority:H \
  "Verify D3 routed as TVS clamp: anode to VBUS, cathode short stub to GND only"

# ---- Tamper evidence + labeling (from Labeling/Potting handoff) ----
task add project:pv-rev1 workstream:hw priority:H \
  "Order Zebra ZT230 used printer" cost:350

task add project:pv-rev1 workstream:hw priority:H \
  "Order thermal transfer ribbon (wax-resin)" cost:15

task add project:pv-rev1 workstream:hw priority:H \
  "Order Uline S-19197 VOID polyester labels 2x1" cost:45

task add project:pv-rev1 workstream:hw priority:H \
  "Order gloss polyester labels 2x3 for ESD bags" cost:25

task add project:pv-rev1 workstream:hw priority:H \
  "Order direct thermal labels 4x6 for shipping" cost:30

task add project:pv-rev1 workstream:hw priority:M \
  "Order small gloss polyester labels for under-pot Data Matrix" cost:20

# ---- Potting experiment (from Labeling/Potting handoff) ----
task add project:pv-rev1 workstream:hw priority:H \
  "Order MG Chemicals 832HD clear potting epoxy" cost:30

task add project:pv-rev1 workstream:hw priority:M \
  "Order holographic glitter fine grade for optical PUF" cost:6

task add project:pv-rev1 workstream:hw priority:M \
  "Order thermochromic pigment/stickers for tamper indication" cost:12

task add project:pv-rev1 workstream:hw priority:M \
  "Order silicone mold release spray" cost:8

task add project:pv-rev1 workstream:hw priority:H \
  "Order small vacuum degassing chamber (production epoxy prep)" cost:80

# ---- Enclosure / pour mold (from Labeling/Potting handoff) ----
task add project:pv-rev1 workstream:hw priority:H \
  "DECIDE: Path A (generate study tray STL now) vs Path B (wait for board measurements) for enclosure mold"

task add project:pv-rev1 workstream:hw priority:M \
  "Measure tallest component height on PCB"

task add project:pv-rev1 workstream:hw priority:M \
  "Document USB-C connector exact dimensions + location (both ends?)"

task add project:pv-rev1 workstream:hw priority:M \
  "Mark mounting hole locations on PCB"

task add project:pv-rev1 workstream:hw priority:M \
  "Confirm single- vs double-sided component population"

task add project:pv-rev1 workstream:hw priority:M \
  "Document external access features: LEDs, buttons, additional connectors"

# ---- Lightning Labels A002 (batch production) ----
task add project:pv-rev1 workstream:hw priority:M \
  "Send Lightning Labels quote email with TS-A001 preview PNGs attached" cost:450

# ---- Copy / shop fixes (from Rev1 overwhelm handoff) ----
task add project:pv-rev1 workstream:sw priority:H \
  "Audit shop.zknot.io copy: fix 100W→60W claim, CC passthrough language"

# ============================================================
# VERIFYKNOT — frontend deploy (#10 exists, these are support tasks)
# ============================================================
task add project:verifyknot workstream:sw priority:H \
  "Upload verifyknot.io public/ folder to Cloudflare Pages" estimate:10min depends:10

task add project:verifyknot workstream:sw priority:H \
  "Set custom domain verifyknot.io in Cloudflare Pages" estimate:5min depends:10

task add project:verifyknot workstream:sw priority:H \
  "Test /v1/attest and /v1/verify endpoints from deployed frontend"

task add project:verifyknot workstream:sw priority:M \
  "Verify CORS on api.zknot.io accepts verifyknot.io origin (add allow-list if needed)"

# ============================================================
# ZKKEY CONNECT REVA — build guide + PCB
# ============================================================
task add project:zkkey-connect workstream:hw priority:M \
  "Finish generating ZKKey Connect RevA build guide docx (run build_guide.js)"

task add project:zkkey-connect workstream:hw priority:M \
  "Run KiCad 10 fix script against ZKKey Connect RevA project files"

task add project:zkkey-connect workstream:hw priority:M \
  "Export Gerbers for ZKKey Connect RevA"

task add project:zkkey-connect workstream:hw priority:M \
  "Order ZKKey Connect RevA PCBs from JLCPCB" cost:50

task add project:zkkey-connect workstream:fw priority:M \
  "Write state machine for ZKKey Connect RevA firmware (STM32F072 + ATECC608A)"

task add project:zkkey-connect workstream:fw priority:M \
  "Set up CryptoAuthLib I2C integration for ATECC608A on PB6/PB7"

# ============================================================
# ZKKEY AIR REVA — fully air-gapped signing device (PAT-009)
# ============================================================
task add project:zkkey-air workstream:hw priority:M \
  "Complete ZKKey Air RevA PCB (STM32F072 + ATECC608 + GM65-S QR + ST7789 display)"

task add project:zkkey-air workstream:hw priority:M \
  "DRC + Gerber export for ZKKey Air RevA"

task add project:zkkey-air workstream:fw priority:M \
  "Design ZKKey Air firmware state machine: idle → scan → verify → sign → display"

task add project:zkkey-air workstream:fw priority:M \
  "Integrate GM65-S QR scanner UART on PA9/PA10 with PA8 trigger"

task add project:zkkey-air workstream:fw priority:M \
  "Integrate ST7789 240x240 SPI display driver"

# ============================================================
# LOGIC 2 / MCP / hardware debug infrastructure
# ============================================================
task add project:tooling workstream:ops priority:M \
  "Edit claude_desktop_config.json: add logic2 MCP entry at 127.0.0.1:10530"

task add project:tooling workstream:ops priority:M \
  "Restart Claude Code with Logic 2 open, verify MCP connection"

task add project:tooling workstream:ops priority:M \
  "Document Saleae Logic 2 MCP natural language capture workflow"

# ============================================================
# DEV ENV MIGRATION (from dev-env handoff)
# ============================================================
task add project:devenv workstream:ops priority:H \
  "Migrate ZKNOT_BIZ off OneDrive to ~/ZKNOT/ on Linux (45 min procedure)" estimate:45min

task add project:devenv workstream:ops priority:H \
  "Create canonical .gitignore for ZKNOT monorepo (KiCad + firmware + Python + OS)"

task add project:devenv workstream:ops priority:H \
  "Create .gitattributes forcing LF + marking KiCad binaries"

task add project:devenv workstream:ops priority:M \
  "Draft README.md for ZKNOT monorepo"

task add project:devenv workstream:ops priority:H \
  "gh repo create zknot/zknot --private --source=. --push"

task add project:devenv workstream:ops priority:H \
  "Configure KiCad ZKNOT_LIB path on Linux (Preferences → Configure Paths)"

task add project:devenv workstream:ops priority:H \
  "Configure KiCad ZKNOT_LIB path on Windows after git clone"

task add project:devenv workstream:ops priority:M \
  "Unlink OneDrive Desktop/Documents redirects on Windows"

task add project:devenv workstream:ops priority:M \
  "Weekly: git clone --mirror ~/ZKNOT to USB SSD"

task add project:devenv workstream:ops priority:L \
  "Delete ~/Downloads/ZKNOT_BIZ/ (passive backup) in 8 days (after 2-week cooldown)" due:2026-05-08

# ============================================================
# IP / PATENTS
# ============================================================
task add project:patents workstream:ip priority:M \
  "Draft PAT-019 optical PUF one-page disclosure for attorney"

task add project:patents workstream:ip priority:M \
  "Draft PAT-009 air-gapped QR signing disclosure review (App# 63/995,740)"

task add project:patents workstream:ip priority:M \
  "Track patent prosecution next steps for PAT-002" involvement:lawyer

task add project:patents workstream:ip priority:M \
  "Patent attorney check-in: review 16 provisionals, confirm 6 non-provisional targets"

# ============================================================
# BUSINESS / ACQUISITION / SOCIAL
# ============================================================
task add project:acquisition workstream:biz priority:H \
  "Draft outreach email template for 8 named acquirers"

task add project:acquisition workstream:biz priority:M \
  "Prepare Liz handoff documentation: what she needs to manufacture independently"

task add project:social workstream:biz priority:M \
  "Set up Instagram account for ZKNOT (product photo story, clear-pot visuals)"

task add project:social workstream:biz priority:L \
  "Skip TikTok for Rev 1 (revisit if Rev 2 hits consumer price point)"

task add project:social workstream:biz priority:M \
  "Post LinkedIn launch post (draft in ZKNOT_Execution_Pack.docx)"

task add project:social workstream:biz priority:M \
  "Reddit: accumulate 150+ karma in r/embedded before Day 8 ATECC608 post"

task add project:social workstream:biz priority:L \
  "Schedule X thread (7 tweets on AirGap/USB data blocker) per Execution Pack playbook"

# ============================================================
# OPS / MISC
# ============================================================
task add project:ops workstream:ops priority:H \
  "Initialize git in ~/.task and commit initial Taskwarrior state" estimate:5min

task add project:ops workstream:ops priority:M \
  "Create ~/ZKNOT/11_KM/ as markdown notes vault, git init"

task add project:ops workstream:ops priority:M \
  "Copy Taskwarrior cheat sheet PDF to ~/ZKNOT/12_JOURNAL/"

task add project:ops workstream:ops priority:L \
  "Optional: try vit or taskwarrior-tui for TUI kanban view"

task add project:ops workstream:ops priority:L \
  "Delete ~/ZKNOT/99_ARCHIVE/cyber_masters_notes_backup_*.tar.gz in 24h if no regrets" due:tomorrow

# ============================================================
# DEFERRED / PARKED (Rev 2, next-gen, advanced features)
# Low priority so they sit in the tail of task list as reminders
# ============================================================
task add project:pv-rev2 workstream:hw priority:L \
  "PARKED: Rev 2 PUF architecture design — resume after Rev 1 has revenue"

task add project:nextgen workstream:hw priority:L \
  "PARKED: Next-gen USB condom product line planning"

task add project:zk-localchain workstream:sw priority:L \
  "PARKED: Advanced ZK-LocalChain features beyond serial binding"

# ============================================================
# DEPENDENCIES: wire up the obvious chains
# (You'll need to adjust task IDs — run "task" after seeding to see them)
# Leaving these as comments; add depends: manually after reviewing IDs
# ============================================================

echo ""
echo "Done. Run:"
echo "  task stream       # see everything grouped by workstream"
echo "  task project:pv-rev1   # focus on ship-it project"
echo "  task ready        # only unblocked tasks"
echo ""
echo "Next: adjust task IDs in dependency chains with:"
echo "  task <id> modify depends:<other-id>"
echo ""
echo "Total cost captured in tasks:"
task export | python3 -c "import json,sys; data=json.load(sys.stdin); total=sum(float(t.get('cost',0)) for t in data); print(f'\${total:,.0f}')"
