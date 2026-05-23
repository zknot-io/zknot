# 2026-05-22 — KiCad Install, HW Folder Structure, and Project Intake

**Status:** In progress — several items need finishing (see OPEN THREADS at bottom)
**Workstream:** hw
**Author:** William Shane Wilkinson

---

## Summary

Installed KiCad 10 on Debian Trixie, built out the `7_ENG/hw/` folder structure for
the full ZKNOT product family, created a reusable title-block worksheet template,
imported the PowerVerify pigtail library parts, and began intaking the GRAIP /
PowerVerify Rev 1 KiCad project from a zip. The GRAIP intake is **not finished** —
it's in a broken half-renamed state that must be fixed inside KiCad before committing.

---

## 1. KiCad 10 install (DONE)

Chose KiCad 10 via Flatpak (latest; avoids dependency drama on Trixie). Decided
against 9.0.8-backports and 9.0.2-stable.

```bash
sudo apt install flatpak
flatpak remote-add --if-not-exists --user flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub org.kicad.KiCad
flatpak run org.kicad.KiCad
```

### CLI alias so `kicad` = v10 (DONE)
Added to `~/.zshrc`:
```bash
alias kicad='flatpak run org.kicad.KiCad'
alias pcbnew='flatpak run --command=pcbnew org.kicad.KiCad'
alias eeschema='flatpak run --command=eeschema org.kicad.KiCad'
alias pl_editor='flatpak run --command=pl_editor org.kicad.KiCad'
alias gerbview='flatpak run --command=gerbview org.kicad.KiCad'
```

### Notes / gotchas learned
- KiCad 10 **does NOT** have a "Working directory" setting in Preferences → Common
  (that was older KiCad). New projects just default to wherever you last saved one.
- Flatpak sandbox sees `$HOME` by default, so `~/ZKNOT/` works with no override.
  Only need `flatpak override --user org.kicad.KiCad --filesystem=/mnt/...` if
  storing projects outside $HOME.
- Text editor in Prefs is set to `nvim` — won't pop open since KiCad spawns it with
  no terminal. If external-edit is wanted, change to `kitty -e nvim` or similar.
  (Left as-is for now.)

---

## 2. Folder structure (DONE)

Decided on `7_ENG/hw/` (NOT flat `7_ENG/`) to leave room for non-KiCad hardware
artifacts. Reconciled an earlier proposed structure against the already-configured
path variables.

Final layout:
```
~/ZKNOT/7_ENG/hw/
├── README.md
├── kicad-libs/{symbols,footprints,3dmodels}/   # shared, global libs
├── kicad-templates/zknot-default/              # worksheet template lives here
├── design-rules/                               # .kicad_dru per fab (JLC 2L/4L)
├── datasheets/
├── fab-output/
├── zkkey-connect/{rev0-breadboard,rev1-pico-carrier}/
├── powerverify/rev0-shipped/                   # forensic tool
├── zkkey-air/
├── graip/                                      # NEW — consumer product (see §5)
└── tooling/atecc-provisioning-jig/rev1/
```

Per-product and per-rev README.md stubs were created with status fields
(in-design / sent-to-fab / received / validated / shipped).

`kicad-projects/` subdir was made redundant by per-product top-level dirs — can
rmdir or keep as scratch sandbox.

### KiCad path variables (configured in Preferences → Configure Paths)
KiCad does NOT expand `~`, so use absolute paths:
```
ZKNOT_SYMBOLS    = /home/mt/ZKNOT/7_ENG/hw/kicad-libs/symbols
ZKNOT_FOOTPRINTS = /home/mt/ZKNOT/7_ENG/hw/kicad-libs/footprints
ZKNOT_3DMODELS   = /home/mt/ZKNOT/7_ENG/hw/kicad-libs/3dmodels
```

### .gitignore block added to ~/ZKNOT/.gitignore
```
# KiCad — autosave/backup/local-state (regenerable cruft)
7_ENG/hw/**/*-backups/
7_ENG/hw/**/*.bak
7_ENG/hw/**/*.kicad_pcb-bak
7_ENG/hw/**/*.kicad_sch-bak
7_ENG/hw/**/*.kicad_prl
7_ENG/hw/**/_autosave-*
7_ENG/hw/**/fp-info-cache
7_ENG/hw/**/*.lck
7_ENG/hw/**/~*
# KiCad — manufacturing outputs (regenerable, can be large)
7_ENG/hw/**/manufacturing/gerbers/
7_ENG/hw/**/manufacturing/drill/
7_ENG/hw/**/manufacturing/pos/
7_ENG/hw/**/fab-output/
7_ENG/hw/**/*.zip
```
Tracked: .kicad_pro, .kicad_sch, .kicad_pcb, .kicad_sym, .kicad_mod, .pretty/,
.kicad_dru, .kicad_wks, READMEs, BOMs.

---

## 3. Worksheet title-block template (DONE)

Created `kicad-templates/zknot-default/zknot-title.kicad_wks` — a reusable drawing
sheet with ZKNOT branding baked in.

### KEY LESSON: KiCad's .kicad_wks parser does NOT accept `;;` line comments.
First version failed to load ("Unexpected ;; ... line 14, offset 2"). Fixed by
stripping all `;;` comments. Only the file-format-native `(comment "...")` tokens
inside item definitions are legal.

### Auto-filling fields in the template
- `${TITLE}`, `${REVISION}`, `${ISSUE_DATE}`, `${PAPER}` — from Page Settings
- `${#}` = current page, `${##}` = total pages → renders "Page X of Y"
  (matches ZKNOT pagination standard)
- `${FILENAME}` — auto traceability stamp
- `${COMMENT1}` — optional, shows on pages 2+ only

### Hardcoded in template
- "ZKNOT, INC." company name
- Tagline "Cryptographic Authenticity Verification"
- "Designer: William Shane Wilkinson" (legal name per filing standard)
- "CONFIDENTIAL — ZKNOT, INC. PROPRIETARY" stamp

### Usage per project
File → Page Settings → Drawing sheet file → Browse → select the .kicad_wks.
Preview in pl_editor:
`flatpak run --command=pl_editor org.kicad.KiCad <path>/zknot-title.kicad_wks`

NOTE: The .kicad_wks layout was never visually verified after the comment fix.
Open in pl_editor and confirm geometry doesn't overlap/run off-page; the title
block uses bottom-right corner anchoring.

---

## 4. PowerVerify pigtail library parts (DONE)

Imported two custom parts (uploaded as files):
- `PowerVerify_Pigtail.kicad_sym` → renamed to `PowerVerify.kicad_sym`
- `Pigtail_USB-C_4wire_6pad_ZKNOT_THT_Arc.kicad_mod`

Placement:
```
kicad-libs/symbols/PowerVerify.kicad_sym
kicad-libs/footprints/PowerVerify.pretty/Pigtail_USB-C_4wire_6pad_ZKNOT_THT_Arc.kicad_mod
```

Rationale: one `.kicad_sym` = one library (can hold many symbols). Named library
`PowerVerify` because the symbol's footprint property references the nickname
`PowerVerify:Pigtail_USB-C_4wire_6pad_ZKNOT_THT_Arc`.

### Library registration (Preferences → Manage Symbol/Footprint Libraries → GLOBAL tab)
```
Symbol:    Nickname=PowerVerify  Path=${ZKNOT_SYMBOLS}/PowerVerify.kicad_sym
Footprint: Nickname=PowerVerify  Path=${ZKNOT_FOOTPRINTS}/PowerVerify.pretty
```
MUST use GLOBAL tables (not project-local) so all products share the lib.
The nickname `PowerVerify` MUST match the symbol's baked-in footprint prefix.

### Gotchas
- Footprint was saved by KiCad 9 (`generator_version "9.0"`). KiCad 10 opens it
  fine and auto-upgrades on save.
- IP NOTE: pigtail symbol/footprint reference PAT-002 / PAT-018. These are now
  IP-relevant artifacts in version control. **Do NOT open-source the PowerVerify
  lib** if kicad-libs/ is ever made public.

---

## 5. GRAIP / PowerVerify Rev 1 project intake (NOT FINISHED — NEEDS WORK)

Source zip: `PowerVerify-GRAIP-Rev1-20260522T030138Z-3-001.zip`
Extracted to: `~/Downloads/_inspect-graip/PowerVerify-GRAIP-Rev1/`

### PRODUCT CLARIFICATION (important)
- **GRAIP** = small CONSUMER-market product, goes in a little graip-shaped container.
- **PowerVerify** = the FORENSIC tool.
These are TWO DIFFERENT PRODUCTS that got tangled into one KiCad folder.

### THE PROBLEM: project is in a broken half-renamed state
The project was renamed `PowerVerify-Rev1` → `GraipPowerVerify-Rev1` mid-design,
but the rename was incomplete:

```
GraipPowerVerify-Rev1.kicad_pcb   140145   May 21 19:54   ← newest PCB
GraipPowerVerify-Rev1.kicad_pro    16676   May 21 19:59   ← newest project
GraipPowerVerify-Rev1.kicad_dru
GraipPowerVerify-Rev1.kicad_prl
PowerVerify-Rev1.kicad_pcb        139147   Apr 24 09:38   ← OLD pcb
PowerVerify-Rev1.kicad_pro         16675   May 20 15:58   ← OLD project
PowerVerify-Rev1.kicad_sch         44992   May 20 15:58   ← THE ONLY SCHEMATIC
PowerVerify-Rev1.kicad_dru
```

**There is NO `GraipPowerVerify-Rev1.kicad_sch`.** When you open the Graip project,
KiCad looks for a schematic matching the project name, doesn't find it → broken
schematic↔PCB link. MUST be fixed via KiCad "Save As" (which rewrites internal
cross-references), NOT a shell `mv`.

### Decisions made
- `.history/` nested git repo (VS Code Local History ext): EXCLUDE entirely.
- `Gerbers/`: DROP — regenerate when actually ordering.
- `*-backups/`, `*.kicad_prl`, `~*.lck`, `fp-info-cache`: exclude.
- GRAIP gets its own top-level product dir: `~/ZKNOT/7_ENG/hw/graip/`.

### UNRESOLVED (was waiting on user answers when thread ended)
1. Do GRAIP and forensic PowerVerify SHARE one schematic (differ only in PCB
   layout), or are they fully separate designs mixed by accident?
2. Final home/name for GRAIP board: `graip/rev1/` renamed to `graip-r1`, or keep
   `GraipPowerVerify-Rev1` name?

### Intake commands (Steps 1–2 safe to run; Step 3 must be done in KiCad GUI)
```bash
# Step 1 — copy clean files into graip slot (excludes all cruft)
mkdir -p ~/ZKNOT/7_ENG/hw/graip/rev1
rsync -av \
  --exclude='.history/' \
  --exclude='*-backups/' \
  --exclude='Gerbers/' \
  --exclude='*.kicad_prl' \
  --exclude='~*.lck' \
  --exclude='fp-info-cache' \
  ~/Downloads/_inspect-graip/PowerVerify-GRAIP-Rev1/ \
  ~/ZKNOT/7_ENG/hw/graip/rev1/

# Step 2 — verify what landed
find ~/ZKNOT/7_ENG/hw/graip/rev1 -type f | sort

# Step 3 — FIX RENAME IN KICAD (GUI, not shell!)
flatpak run org.kicad.KiCad ~/ZKNOT/7_ENG/hw/graip/rev1/GraipPowerVerify-Rev1.kicad_pro
# → File → Save As → rename project cleanly (e.g. graip-r1)
# → KiCad rewrites internal refs; then delete leftover old-named files
```

---

## 6. The procedures-zknot-org-site.zip (SEPARATE — not yet placed)

A different zip also in Downloads: `procedures-zknot-org-site.zip`. This is a
COMPLETE STATIC WEBSITE for zknot.org procedures (chain-of-custody, methodology,
colophon) with its own wrangler.toml (Cloudflare Pages). SEPARATE from verifyknot.io.

### Recommended home: `~/zknot-org-site/` (top-level repo sibling, its own git repo)

### KNOWN BUG in that zip: malformed brace-expansion dirs
Contains junk dirs from a failed `mkdir {a,b}` brace expansion:
```
public/{assets/
public/{assets/css,procedures/
public/{assets/css,procedures/digital-evidence-chain-of-custody}/
```
Remove after extract: `cd public && rm -rf '{assets'` (single-quote the brace).

NOTE: This site intake was started but set aside when user clarified they meant the
GRAIP zip instead. Pick up later if still needed.

---

## OPEN THREADS / TODO (priority order)

1. **[GRAIP intake] FINISH §5** — answer the 2 unresolved questions, run rsync
   Steps 1–2, then fix the rename in KiCad (Step 3), then commit. The half-renamed
   schematic link is a real risk: a board editing against a stale/blank schematic.
2. **[Verify] §3 worksheet** — open zknot-title.kicad_wks in pl_editor, confirm the
   title-block geometry renders correctly (never visually checked post-fix).
3. **[Register libs] §4** — confirm PowerVerify symbol+footprint libs added to GLOBAL
   tables and the pigtail resolves (place symbol, check footprint preview).
4. **[procedures site] §6** — if still wanted, extract to ~/zknot-org-site/, kill the
   brace-junk dirs, git init, check wrangler.toml target (zknot.org vs subdomain).
5. **[Priority decision] DEFERRED** — which board gets KiCad time next:
   - ATECC provisioning jig (unblocks hw-signed production for Connect + PowerVerify;
     but blocked on MCP2221 arrival)
   - PowerVerify Rev 1 formalization (stabilize shipping/revenue product)
   - ZKKey Connect Rev 1 (patent-embodiment validator)
   User to decide based on actual weekly blockers, not paper aesthetics.

## Taskwarrior follow-ups to create
```bash
task add project:zknot.hw.graip workstream:hw priority:H "fix GRAIP project rename in KiCad + commit"
task add project:zknot.hw workstream:hw "verify zknot-title.kicad_wks geometry in pl_editor"
task add project:zknot.hw workstream:hw "register PowerVerify symbol/footprint libs in KiCad global tables"
task add project:zknot.web workstream:sw "place procedures-zknot-org-site, fix brace-junk, check wrangler target"
```
