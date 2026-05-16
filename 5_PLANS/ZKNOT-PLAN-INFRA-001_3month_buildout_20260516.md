# ZKNOT Infrastructure Buildout — 3-Month Reference

**Document ID:** ZKNOT-PLAN-INFRA-001
**Author:** William Shane Wilkinson
**Created:** 2026-05-16
**Workstream:** ops
**Status:** Active reference doc
**Review trigger:** Monthly or on funding/surplus event
**Page 1 of 8**

---

## Executive summary

ZKNOT's infrastructure spend over the next 3 months is **subordinate to PV1
manufacturing and shipping velocity**. The current Debian workstation (i9-11900K,
64GB DDR4, RTX 3080 Ti) is adequate for all engineering work through Q3. No
new compute is needed in Phase 1.

**Total new infrastructure spend, Phase 1 (Month 1):** ~$240
**Total new infrastructure spend, Phase 2 (Month 2):** ~$100–250 (backup, optional)
**Total new infrastructure spend, Phase 3 (Month 3):** $0–1,500 (NAS, only if revenue or surplus)

The plan defers all NAS / dedicated app server work until either (a) PV1 revenue
materializes, (b) SDVOSB surplus delivers usable hardware, or (c) an SBIR award
funds infrastructure as an allowable expense.

---

## Current state snapshot (as of 2026-05-16)

### Compute on hand and working

| System | CPU | RAM | GPU | Storage | OS | Role |
|---|---|---|---|---|---|---|
| Linux workstation (`mt`) | i9-11900K (8c/16t) | 64GB DDR4-3200 | RTX 3080 Ti 12GB | 1TB NVMe + 500GB + 250GB | Debian Trixie 13 | Primary dev + ZKNOT vault |
| Windows gaming rig | i9-12900KF (16c) | 64GB DDR5-4800 | RTX 4080 16GB | 2.75TB | Win 11 25H2 | Personal, gaming, untouched |
| Pi 5 (8GB) | ARM Cortex-A76 | 8GB | — | TBD | TBD | Currently ATECC bench duty |
| Pi 4 | ARM Cortex-A72 | TBD | — | TBD | TBD | Available |
| Pi Zero | ARM | 512MB | — | TBD | TBD | Available |
| Jetson Nano | — | — | NVIDIA | TBD | TBD | Available |

### Network gear on hand

- **Protectli VP2420** (Celeron J6412, 16GB, 480GB) — earmarked for OPNsense
- **TP-Link TL-SG2008P** — 8-port managed PoE switch, Omada-capable
- **Dualcomm ETAP-2003** — passive network TAP

### Critical gap

- **No UPS on the Debian workstation.** 3 days uptime, ZFS not present
  (ext4 root), but any brownout corrupts active writes including
  Taskwarrior data, git index, and ZKNOT vault working changes.
- **No off-machine backup.** ZKNOT vault is 727MB / 6,593 files in
  `~/ZKNOT`. Lives on one disk. Git remotes are the only redundancy.
- **`enp7s0` is DOWN.** 2.5GbE Realtek port on the Z590 motherboard
  is unused — currently on Wi-Fi only.

### Engineering work in flight (NOT infra — context for prioritization)

- **PV1 manufacturing:** PV1-00042/43/44 in 48hr epoxy cure, check due 2026-05-17
- **ATECC608B provisioning:** Pico bench restored, Amazon MCP2221A clones DOA,
  decision pending on Adafruit 4471 vs Pico-as-USB-I2C-bridge path
- **Patents:** 6 provisionals to convert to non-provisionals by 2027-03-01
- **Acquisition outreach:** 8 named targets, follow-up due 2026-10-24
- **Verifyknot.io:** Deployed, CORS verification still pending (T#29)

---

**Page 2 of 8**

## Architecture target (defer most of this until Phase 3+)

```
                          Internet
                              |
                       [Protectli VP2420]
                       [OPNsense + WireGuard]
                              |
                       [TL-SG2008P switch]
                       /      |       \
                      /       |        \
              [VLAN 10]   [VLAN 20]  [VLAN 30]
                Trust       Mfg       Mgmt
                  |          |          |
            [Workstation]  [Pi 5]   [PiKVM]
            [Future NAS]   [bench]
            [Pi 4 — bkp]
```

**VLAN allocation:**
- **VLAN 10 (Trust, 10.10.10.0/24):** Workstation, NAS, Pi 4 (backup/monitor), trusted devices
- **VLAN 20 (Mfg, 10.10.20.0/24):** Pi 5 bench, ATECC fixtures, label printers, camera rigs, 3D printer
- **VLAN 30 (Mgmt, 10.10.30.0/24):** PiKVM, switch management, OPNsense management
- **VLAN 40 (Guest, 10.10.40.0/24):** Future — IoT, untrusted

**Trust rules:**
- Mfg → Trust API endpoints only (no shell, no SMB)
- Trust → Mfg full access (for debugging)
- Mgmt isolated, accessible only from Trust via jump host
- Guest → Internet only

**This is the target. Building toward it incrementally. Not all in 3 months.**

---

**Page 3 of 8**

## Phase 1 — Month 1 (May 16 – June 15): Stabilize what exists

**Goal:** Don't lose work. Don't lose data. Don't slow PV1 shipping.

### Required actions

| # | Action | Cost | Rationale |
|---|---|---|---|
| 1.1 | Buy CyberPower CP1500PFCLCD UPS | $240 | Workstation runs 24/7. One brownout = corrupted Taskwarrior DB + git index + active KiCad project. |
| 1.2 | Plug `enp7s0` into TP-Link TL-SG2008P | $0–10 (cable) | 2.5GbE wired beats Wi-Fi for git push, large file ops, future NAS access. |
| 1.3 | Configure TP-Link with single default VLAN | $0 | Get the switch on the network with Omada controller (container later). Don't VLAN yet. |
| 1.4 | Run weekly `git clone --mirror` of ZKNOT vault to existing 500GB NVMe | $0 | T#43 already in Taskwarrior. Just execute it. |
| 1.5 | Audit `~/ZKNOT/99_SENSITIVE/` for actual plaintext exposure | $0 | Journal 2026-04-18 flagged this as a known blocker. |

### Phase 1 budget: **$240–250**

### Phase 1 deliverables

- [ ] UPS protecting workstation
- [ ] Wired 2.5GbE up (`enp7s0` shows UP, IP assigned)
- [ ] Weekly cron job mirroring ZKNOT to second NVMe
- [ ] 99_SENSITIVE audit complete (encrypted or moved off-disk)
- [ ] Taskwarrior tasks added (see appendix)

### What's explicitly NOT in Phase 1

- No NAS purchase
- No additional compute
- No OPNsense deploy
- No Pi reassignment (Pi 5 stays on ATECC bench duty until ZKKey Connect is provisioning real units)
- No managed switch VLAN work

---

**Page 4 of 8**

## Phase 2 — Month 2 (June 15 – July 15): Real backup, opportunistic surplus

**Goal:** Survive disk failure. Start watching surplus channels actively.

### Required actions

| # | Action | Cost | Rationale |
|---|---|---|---|
| 2.1 | Buy 2TB external USB SSD (Crucial X9 Pro or Samsung T7 Shield) | $100–150 | Restic snapshot target. Air-gapped backup, lives in different physical location than workstation. |
| 2.2 | Set up restic to external SSD + Backblaze B2 | $0 setup + ~$1/mo storage | Two-target backup. B2 for offsite, USB SSD for fast restore. |
| 2.3 | Register for GovPlanet, GSA Auctions, Utah State Surplus | $0 | T#85 + T#86 marked done in Taskwarrior — verify access works and set saved searches. |
| 2.4 | Set saved search alerts for: APC SmartUPS 1500/3000, Dell PowerVault, rackmount UPS | $0 | When surplus hardware shows up, you have hours, not weeks. Email alerts critical. |
| 2.5 | Document target hardware wishlist (T#84 already exists, M priority) | $0 | Convert wishlist to specific make/model targets with budget caps. |

### Phase 2 budget: **$100–150** (plus $1/mo ongoing for B2)

### Phase 2 deliverables

- [ ] Restic snapshots running nightly, 30-day retention, verified restorable
- [ ] External SSD lives in a different room than workstation (fire/theft separation)
- [ ] Backblaze B2 bucket configured, encryption keys backed up (NOT in same place as snapshots)
- [ ] Surplus alerts active on 3+ channels
- [ ] Hardware wishlist doc committed to `~/ZKNOT/5_PLANS/`

### Phase 2 trigger to advance to Phase 3

Phase 3 (NAS build) only begins if **one** of these happens:

1. PV1 revenue ≥ $5,000 cumulative (covers full NAS spend, leaves runway)
2. SBIR Phase 1 awarded (infrastructure is an allowable expense)
3. Acceptable enterprise surplus hardware available (APC SmartUPS + a rackmount server or NAS chassis)
4. SDVOSB-specific procurement opportunity opens

**If none of the above happens by Month 3, stay in Phase 2 indefinitely.** The workstation is enough.

---

**Page 5 of 8**

## Phase 3 — Month 3 (July 15 – Aug 15): NAS build, only if triggered

**Goal:** Add proper storage tier with redundancy, replication, and growth path. Only if Phase 2 trigger fires.

### Three sub-paths depending on what's available

### Path A — Full new build (only if revenue/SBIR funds)

Parts list (Memorial Day pricing should already be banked):

| Item | Source | Cost |
|---|---|---|
| Jonsbo N3 case (8-bay mITX) | Amazon | $160 |
| ASRock B760M Pro RS | Amazon | $110 |
| Intel i3-14100 | Newegg/Amazon | $130 |
| Thermalright Peerless Assassin 120 SE | Amazon | $35 |
| Corsair RM650e PSU | Amazon | $105 |
| 32GB DDR5 SODIMM kit (Crucial) | Newegg | $85 |
| 256GB boot NVMe (any) | Amazon | $30 |
| 2× 500GB NVMe (special vdev mirror) | Amazon | $80 |
| 4× WD Red Pro 12TB | Newegg + B&H (split) | $1,000–1,200 |
| **Total Path A** | | **$1,735–1,935** |

### Path B — Hybrid (G.SKILL DDR4 leveraged, B660/H670 board)

If the G.SKILL DDR4-3200 32GB kit from Trident Z5 inventory can be allocated to NAS:

| Item | Cost |
|---|---|
| Jonsbo N3 | $160 |
| Used B660/H670 mITX motherboard (DDR4) | $80–120 |
| Intel i3-12100 (Memorial Day target $120) | $120 |
| Cooler, PSU, NVMes, drives as Path A | $1,250 |
| **Total Path B** | **~$1,650** |

### Path C — Surplus-driven (only if right hardware appears)

If SDVOSB surplus delivers a usable chassis (Dell PowerVault, HPE D3600, Synology RS-series):

| Item | Cost |
|---|---|
| Surplus chassis | $0–200 |
| Surplus or new drives (drives never come with surplus) | $1,000–1,200 |
| Misc cables, caddies, brackets | $50–100 |
| **Total Path C** | **~$1,050–1,500** |

### TrueNAS Scale dataset layout (any path)

```
tank/
├── zknot-vault          # mirror of ~/ZKNOT, snapshotted every 6hr, kept 90d
├── zknot-repos          # Gitea data + mirrors, snapshotted daily, kept 30d
├── zknot-photos         # PUF images, no snapshots (immutable, append-only)
├── zknot-3dmodels       # STL/3MF/STEP archive, snapshotted weekly
├── zknot-docs           # contracts, signed PDFs, federal paperwork
├── zknot-backups        # restic repo target from workstation
├── containers           # Docker/Podman persistent state
└── archive              # cold storage, no snapshots
```

### Phase 3 deliverables

- [ ] NAS hardware acquired (one of A/B/C)
- [ ] TrueNAS Scale installed, pool created (RAID-Z2 if ≥4 drives)
- [ ] Dataset structure created per above
- [ ] Restic from workstation now targets NAS + B2 (3-target backup)
- [ ] ZKNOT vault mirrored to NAS dataset
- [ ] First container service moved (Gitea or Radicale)

---

**Page 6 of 8**

## Budget tiers, three scenarios

### Tier 0 — Strict bootstrap (zero or near-zero new spend)

If funds are critically tight:

- Skip the UPS. Buy a $30 surge protector instead, accept the brownout risk.
- Defer external SSD. Use git remotes (GitHub + Codeberg) as 2-target redundancy.
- Plug in ethernet, configure restic to B2 only (~$1/mo).
- **Total: $0–30**

This is survivable but exposed. **Recommended only if literally out of cash.**

### Tier 1 — Recommended bootstrap (Phase 1 + Phase 2 only)

- UPS, external SSD, restic to 2 targets.
- Workstation stays primary, no NAS.
- **Total: $340–400, plus $1/mo ongoing**

This is the actual recommendation given current state.

### Tier 2 — Revenue-funded full buildout (Phase 1 + 2 + 3 Path A)

- Everything in Tier 1 plus a full new NAS build.
- **Total: ~$2,100, plus $1/mo ongoing**

Only if PV1 sells ≥10 units at ≥$300 net margin each, or SBIR awards.

### Tier 3 — SBIR / contract-funded enterprise (Phase 1 + 2 + 3 Path A + extras)

- Tier 2 plus: enterprise UPS, secondary backup target (rsync.net), full VLAN deployment, PiKVM, Zeek monitoring on Pi 5 when free.
- **Total: ~$2,500–3,000**

Only on funding event.

### Decision triggers — what shifts you between tiers

| Event | Action |
|---|---|
| PV1 generates $0–500 by Aug 15 | Stay Tier 1 |
| PV1 generates $500–3000 by Aug 15 | Stay Tier 1, but bank funds for Tier 2 |
| PV1 generates $3000+ by Aug 15 | Begin Tier 2 (Path A or B) |
| SBIR Phase 1 awarded | Jump to Tier 3 |
| Acquisition LOI received | Pause infra entirely, focus on diligence |
| SDVOSB surplus delivers UPS | Apply that savings to drives, advance toward Tier 2 Path C |

---

**Page 7 of 8**

## Taskwarrior add commands

Paste these into your terminal. They follow the existing workstream:ops convention.

```bash
# === PHASE 1 TASKS ===
task add "Buy CyberPower CP1500PFCLCD UPS for workstation" \
  project:zknot.ops workstream:ops priority:H due:2026-05-23 \
  +infra

task add "Plug enp7s0 into TP-Link TL-SG2008P, verify 2.5GbE link" \
  project:zknot.ops workstream:ops priority:H due:2026-05-20 \
  +infra

task add "Configure Omada controller (Docker container on workstation), adopt switch" \
  project:zknot.ops workstream:ops priority:M due:2026-05-30 \
  +infra

task add "Audit ~/ZKNOT/99_SENSITIVE/ for plaintext exposure, encrypt or move" \
  project:zknot.ops workstream:ops priority:H due:2026-05-25 \
  +infra +security

task add "Set up weekly cron: git clone --mirror ~/ZKNOT to /mnt/backup-nvme/zknot-mirror" \
  project:zknot.ops workstream:ops priority:M due:2026-05-30 \
  +infra +backup

# === PHASE 2 TASKS ===
task add "Buy 2TB external USB SSD (Crucial X9 Pro or Samsung T7 Shield)" \
  project:zknot.ops workstream:ops priority:M due:2026-06-20 \
  +infra +backup

task add "Configure restic: workstation -> external SSD + Backblaze B2" \
  project:zknot.ops workstream:ops priority:H due:2026-06-25 \
  +infra +backup

task add "Verify restic restore works (restore one file from B2 to /tmp)" \
  project:zknot.ops workstream:ops priority:H due:2026-06-26 \
  +infra +backup

task add "Set GovPlanet saved search: APC SmartUPS 1500/3000/5000 in Utah/CO/NV/AZ" \
  project:zknot.gov workstream:ops priority:M due:2026-06-25 \
  +infra +surplus

task add "Set GovPlanet saved search: Dell PowerVault, HPE D3600, NAS chassis" \
  project:zknot.gov workstream:ops priority:M due:2026-06-25 \
  +infra +surplus

task add "Set Utah State Surplus alert (manual check weekly) for IT equipment" \
  project:zknot.gov workstream:ops priority:L due:2026-06-30 \
  +infra +surplus

task add "Document target hardware wishlist in 5_PLANS with specific models + budget caps" \
  project:zknot.ops workstream:ops priority:M due:2026-07-01 \
  +infra +surplus

# === PHASE 3 GATE TASKS ===
task add "DECISION POINT: review PV1 revenue, SBIR status, surplus availability" \
  project:zknot.ops workstream:ops priority:H due:2026-07-15 \
  +infra +gate

task add "If gate passed: select NAS path A/B/C, place orders" \
  project:zknot.ops workstream:ops priority:M due:2026-07-20 \
  +infra

task add "If gate passed: build NAS, install TrueNAS Scale, create RAID-Z2 pool" \
  project:zknot.ops workstream:ops priority:M due:2026-08-01 \
  +infra

task add "If gate passed: configure dataset structure, set up first replication" \
  project:zknot.ops workstream:ops priority:M due:2026-08-10 \
  +infra

# === MONTHLY REVIEW ===
task add "Monthly infra review: revisit ZKNOT-PLAN-INFRA-001, adjust tier" \
  project:zknot.ops workstream:ops priority:L due:2026-06-15 recur:monthly \
  +infra +review
```

---

**Page 8 of 8**

## Appendix A — SDVOSB surplus monitoring sources

| Source | URL | Notes |
|---|---|---|
| GovPlanet | govplanet.com | DLA Disposition Services. Auctions. SDVOSB doesn't get priority but prices low. |
| GSA Auctions | gsaauctions.gov | Civilian agency surplus. |
| GSAXcess | gsaxcess.gov | Federal property to eligible recipients (SDVOSB qualifies for some). T#85 marked done. |
| Utah State Surplus | surplus.utah.gov | State + local agency surplus. T#86 marked done. |
| VA OSDBU | osdbu.va.gov | VA-specific small business outreach. ICF session scheduled May 28. |
| DLA Disposition | dla.mil/dispositionservices | Direct surplus sales. |
| GSA Schedule (different) | gsa.gov/schedules | NOT surplus — for selling TO gov. Already in your APEX track. |

## Appendix B — What never to skimp on

1. **The UPS.** Cheaper to buy a $240 UPS once than to recover one corrupted day of work.
2. **Drive diversity.** Mix WD Red Pro and Seagate IronWolf Pro across retailers. Same-batch failure is real.
3. **Backup verification.** A backup that hasn't been test-restored is not a backup.
4. **Off-site copy.** Same room, same building, same city — none of those count for fire/theft.

## Appendix C — What's safe to skimp on

1. **NAS CPU.** i3-14100 or even i3-12100 is plenty for 4-6 drives + a few containers.
2. **NAS RAM brand.** Crucial, Kingston, Corsair — all fine. Just match speed.
3. **NAS PSU wattage.** 650W is overkill for 4-bay NAS. Don't pay for 750W+.
4. **Switch enterprise upgrade.** Your TP-Link Omada is genuinely good. Don't replace.

## Appendix D — Out-of-scope for this doc (handled elsewhere)

- ATECC608B / Pico / cryptoauthlib decisions — separate thread
- PV1 manufacturing process — in `pv-rev1` project
- PUF protocol design — in `6_SIG/` and patents
- Federal acquisition strategy — in `9_GOV/` and `zknot.gov` workstream
- ZKKey Connect / Air firmware — in `zkkey-connect` / `zkkey-air` projects

## Appendix E — Reference: existing related artifacts in vault

- `~/ZKNOT/5_PLANS/` — strategic planning home (this doc belongs here)
- `~/ZKNOT/3_OPS/journal/` — daily journals, infrastructure decisions get entries
- `~/ZKNOT/3_OPS/km/` — knowledge management, lasting reference
- `~/ZKNOT/4_LOG/` — operational logs
- `~/ZKNOT/99_SENSITIVE/` — sensitive material (audit pending per Phase 1)

## Revision log

| Date | Author | Change |
|---|---|---|
| 2026-05-16 | William Wilkinson | Initial creation |

---

**End of document. Page 8 of 8.**
