---
date: 2026-06-01
topic: centralized-storage-and-nas-planning
author: William Shane Wilkinson
workstream: ops
tags: [infra, storage, samba, smb, nas, backup, git, security-audit]
related:
  - ZKNOT-PLAN-INFRA-001
  - (pending) ZKNOT-PLAN-INFRA-002
  - (pending) km/systems/network-storage.md
supersedes: 2026-06-01_centralized-storage-smb.md
status: complete
---

# 2026-06-01 — Centralized storage live + NAS plan reworked

## TL;DR

Stood up working centralized storage for $0 on hardware already on hand, then
reworked the NAS plan to "build the right system as income comes in" instead of
rushing a deadline build. The ZKNOT vault (`~/ZKNOT`) is now the SMB share itself
(Option A), mounted on Windows as a persistent `Z:` drive, with `99_SENSITIVE/`
and `01_PATENTS/` excluded from the network via Samba `veto files`. Mapping by
NetBIOS name (`\\mt\share`) solved the DHCP IP-churn problem permanently. Along
the way: hardened the `zknot-api` repo (removed tracked `.bak` files, added
secrets/scratch ignores — commit `cadbb18`), audited the 585 MB legacy biz dump
and confirmed it carries no live secrets (archive-tier, share-only, never git),
and corrected four hardware-spec errors in INFRA-001 that would have caused
failed orders. Backup remains the single highest-leverage open item.

---

## Context — what prompted this

Too many files accumulating on two machines (Debian workstation `mt`, Windows
`mtpc`); git is the wrong tool for general/binary file storage. Goal: one
centralized place both machines can read/write, as a bridge until the NAS exists.

Machines (same 10.0.0.0/24 subnet, route through router at 10.0.0.1):
- **Debian `mt`** — primary dev + ZKNOT vault host. On Wi-Fi (`wlo1`). 2.5GbE
  `enp7s0` still unused. DHCP-assigned, moved .162 -> .163 across a reboot today.
- **Windows `mtpc`** — i9-12900KF / 64 GB / RTX 4080, ~2.3 TB free, wired,
  10.0.0.148, user `shane`. Win 11 Insider Preview (build expires 2026-08-11).

---

## What was built (in sequence — verify before trusting each layer)

1. Confirmed both machines already talk on the existing network — no switch
   needed (a switch adds ports/speed/VLANs, not connectivity the router already
   provides). Ping Windows -> Debian succeeded.
2. Installed Samba on Debian, created Samba user `mt` (credential separate from
   Linux login), enabled `smbd`/`nmbd` to auto-start on boot.
3. Initial scoped share at `/srv/share` (deliberately NOT `$HOME`), mounted as
   `Z:` on Windows via `net use ... /persistent:yes`.
4. Verified the round trip: wrote `Z:\test.txt` from Windows, confirmed it
   appeared on the share. Write across the network proven.
5. Reboot test: `systemctl is-active smbd nmbd` -> `active / active`. Samba is
   reboot-proof; never needs manual restart.
6. **Promoted the share to the vault (Option A):** re-pointed `[share]` from
   `/srv/share` to `/home/mt/ZKNOT`. The existing 00-99 vault structure (already
   git-tracked, already `.gitignore`-governed) becomes the single source of
   truth, with zero copying/duplication.

### Final share configuration (decided)

```ini
[share]
   path = /home/mt/ZKNOT
   browseable = yes
   read only = no
   valid users = mt
   veto files = /99_SENSITIVE/01_PATENTS/
   delete veto files = no
```

- `veto files` makes Samba refuse to serve `99_SENSITIVE/` and `01_PATENTS/` over
  the network — they remain fully accessible locally on the Debian box, just not
  exposed on the LAN share.
- `delete veto files = no` prevents deletion-through-share of those paths.
- Rationale for excluding even though the rest of the vault is shared: the
  `99_SENSITIVE` plaintext audit (INFRA-001 Phase 1) is still OPEN, SMB serves
  cleartext over the wire by default, and the host is on Wi-Fi. Exposing keys /
  `api_secrets.env` / filed patents on the network before auditing them is the
  wrong order. Excluding costs nothing — local access is unchanged.

---

## The IP-churn problem and the fix (a logged tradeoff that came due)

Predicted earlier in the addressing discussion: `Z:` mapped by raw IP is brittle
because DHCP can reassign the Debian box's address. It did — `.162` -> `.163` on
reboot — which would have broken the mount.

**Fix: map by NetBIOS name, not IP.** `nmbd` broadcasts the name `mt`, so:

```
net use Z: /delete
net use Z: \\mt\share /user:mt /persistent:yes
```

`\\mt\share` resolves regardless of the underlying IP. `Z:` is now reboot-stable.
This makes a DHCP reservation / static IP optional rather than required — the name
mapping removes the dependency on the address entirely. (A reservation is still
worth doing eventually for general network hygiene, and will migrate to OPNsense
when that phase happens.)

---

## Git / share / secrets — the three-bucket split (decided + applied)

- **Git (version-controlled):** source (`.py`), markdown knowledge, configs whose
  history matters. The vault already tracks `.md` and ignores binaries/docs.
- **Share-only (archive/binary tier):** PDFs, docx/xlsx, images, STL/STEP/3MF,
  KiCad fab output, archives, the legacy biz dump. Big/regenerable/binary — never
  git (bloats history permanently).
- **Neither in plaintext (secrets):** `99_SENSITIVE/`, `api_secrets.env`, keys,
  `01_PATENTS/`. Stays off git AND off the network share (veto'd).

The vault `.gitignore` already encoded most of this (all PDFs/docx/images/archives
excluded, `99_SENSITIVE/` and `01_PATENTS/` excluded). Confirmed mature.

### zknot-api hygiene (commit cadbb18)

- Found 2 tracked backup snapshots (`attestation.py.bak-20260520`,
  `crypto.py.bak-20260520`) — untracked with `git rm --cached`.
- Hardened the minimal api `.gitignore` with secrets (`*.env`, `*.key`, `*.pem`,
  `secrets/`) and scratch (`*.bak*`, `*.tmp`, `*.swp`) patterns.
- Secret scan of tracked JSON/TXT (5 label JSONs + `requirements.txt`): clean,
  no matches.

---

## Legacy biz dump audit — `99_ARCHIVE/zknot_biz_legacy_dump_20260511/`

585 MB historical dump of the old `ZKNOT_BIZ` tree (KiCad/STEP/SCAD hardware,
firmware, Capstone project, website). Audited before letting it near the share:

- **Word-match grep** flagged 10 files — ALL crypto *subject matter*
  (`witness_cli.py`, `atecc608b.py`, Capstone docs, a folder literally named
  "holds a private key"). Not credentials.
- **Assignment-pattern grep** (looking for `key = "longvalue"`, `postgres://`,
  tokens): **zero hits.** No live secrets.
- **`.db` files:** all `project.db` under `Corne/crkbd` + `jlcpcb` paths —
  JLCPCB fab databases from the Corne keyboard side-project. Benign.
- **`.conf` files:** all OpenSCAD bundled font configs. Benign.
- **Nested `.git` dirs (10):** nine are VS Code Local History (`.history/.git`)
  artifacts; one (`ZKKEY-HW-G1-USB-A-REV-A/.git`) is a real project repo.

**Disposition:** archive-tier, share-only, NEVER `git add` (nested repos =
submodule chaos; size/binaries bloat history). Cleared of secrets.
**Deferred (low priority):** a clean working tree doesn't prove clean git
*history* — an old commit in the embedded repos could hold a deleted key. For a
private archive on an access-controlled private share, not worth chasing now.

---

## NAS architecture — deferred, build it right

Decided to defer the build and buy correct parts as income comes in, rather than
rush a deadline build. This overrides INFRA-001's July-15 Phase-3 gate — recorded
as a deliberate deviation, not silent drift.

**Platform direction:** ASRock Rack B650D4U family (AM5, DDR5 **ECC** UDIMM,
**IPMI**, current-gen socket). Philosophy: the box protects irreplaceable data
for years, so integrity + remote management + platform runway outrank raw specs.

**Verified this session:**
- B650D4U-2L2T/BCM = ECC + IPMI + dual 10GbE (leaning this variant; 10GbE-onboard
  beats the 2nd M.2 for a multi-year box, even though current switch is 1GbE).
- Jonsbo N3 = Mini-ITX/SFX/130mm-cooler only (rules out a microATX build).
- Jonsbo N4 = microATX, 6x3.5"+2x2.5", but 70mm cooler cap; Fractal Node 804 =
  roomier, ATX PSU, tower coolers, 8-10 bays (leaning 804 for thermals/expansion).
- NAS drive market: CMR only (SMR breaks ZFS rebuilds); enterprise (Exos/Ultrastar)
  often better $/TB than NAS-tier for home; ~16TB ~ $16-17/TB currently, volatile.

**Forks still OPEN (needed for INFRA-002):** board variant (2L2T/BCM vs plain),
case (Node 804 vs N4), CPU (Ryzen 7600 vs EPYC 4004 — verify ECC on the board QVL).

**Do NOT reuse the G.SKILL Trident Z5 DDR5-6000 kit:** it is non-ECC; the build
is ECC. Stays gaming inventory.

### INFRA-001 corrections logged (doc to be superseded by INFRA-002)

- "DDR4-3200" kit is actually DDR5-6000 U-DIMM (and non-ECC — wrong for NAS).
- Path A spec'd SODIMM (laptop RAM); desktop boards take full-size U-DIMM.
- Path A paired microATX board + ATX PSU + 155mm cooler with the Jonsbo N3
  (Mini-ITX/SFX/130mm only) — three parts wouldn't physically fit.
- Path B assumed reusing DDR4 on a DDR4 board — impossible with a DDR5 kit.

---

## Backup plan — DECIDED interim + FLAGGED risk

**Stated interim plan:** back the vault up to two separate Google Drives until the
NAS is installed.

**Flagged tradeoff (both sides, for the record):**
- *For Google Drive:* free-ish, already set up, zero learning, fine as an interim
  copy for the regenerable/binary/archive bucket. Better than nothing.
- *Against, for irreplaceables:* Google Drive *syncs* — a deletion or corruption
  on the source propagates to the cloud automatically (mirroring, not snapshots).
  Two Drives in the same Google account share a failure domain (not independent
  copies). No versioned restore, no client-side encryption guarantee.
- *Recommended (INFRA-001 Phase 2):* restic -> external SSD + Backblaze B2.
  Snapshots (restore prior state after a bad delete), encryption, verification.
  ~$120 SSD + ~$1-5/mo B2. Stand this up SOON, ahead of the NAS, for anything
  irreplaceable (patents, filed records).

**Net:** Google Drive acceptable as interim bulk copy; do NOT let it be the only
protection for irreplaceable items. Backup is the highest-leverage open item in
this whole arc — cheaper than the NAS, protects more.

---

## Decisions

1. **NAS deferred; build the correct ECC+IPMI system as income comes in.**
   Overrides INFRA-001 Phase-3 July-15 gate (deliberate, logged).
2. **Platform: ASRock Rack B650D4U-2L2T/BCM direction** (ECC, IPMI, 10GbE).
   Case/CPU forks open pending INFRA-002.
3. **Do not reuse the Trident Z5 kit** (non-ECC) in the NAS.
4. **Centralized storage = the ZKNOT vault itself** (Option A), shared via Samba
   at `/home/mt/ZKNOT`, mounted as `Z:` on Windows.
5. **`99_SENSITIVE/` and `01_PATENTS/` veto'd from the share** — local-only,
   never served over SMB. Secrets never cross to the share.
6. **Map by name (`\\mt\share`), not IP** — solves DHCP churn; reservation optional.
7. **No switch for connectivity** — deferred to the network phase, after NAS parts.
8. **Three-bucket file policy** — git (source/text) / share (binary/archive) /
   neither (secrets). Applied to vault + zknot-api.
9. **Legacy biz dump = archive-tier, share-only, never git** — audited, no secrets.
10. **Interim backup via Google Drive, with restic->SSD+B2 as the real target.**
    (Risk of sync-not-backup explicitly accepted for the interim bulk copy.)

---

## Open items / next

- [ ] Apply/confirm the veto'd `[share]` config + `systemctl restart smbd`.
- [ ] Decide whether to also set a DHCP reservation for `mt` (optional now that
      name-mapping works).
- [ ] Stand up restic -> external SSD + Backblaze B2 (INFRA-001 Phase 2) — do NOT
      wait for the NAS for irreplaceable items.
- [ ] Run the `99_SENSITIVE/` plaintext audit (INFRA-001 Phase 1, still open).
- [ ] Choose INFRA-002 forks: board variant, case, CPU; verify CPU ECC on the
      board memory QVL (primary source).
- [ ] Generate ZKNOT-PLAN-INFRA-002 (supersedes 001), commit to `5_PLANS/`, mark
      001 superseded.
- [ ] Promote durable how-it-works facts to `km/systems/network-storage.md`.
- [ ] Migrate scattered files from both machines into the vault structure —
      COPY, don't move; verify each batch; keep originals until backup exists.
- [ ] Wire `enp7s0` (2.5GbE) when Wi-Fi latency on transfers becomes annoying.

## Risk / backup flags (unresolved)

- **The vault now lives single-copy on one unbacked-up Debian disk** and is the
  declared source of truth. Until restic->SSD+B2 (or the NAS) exists, a disk
  failure loses everything. This is the live risk created by consolidating.
- **Google Drive interim backup is sync, not snapshots** — accepted for bulk,
  inadequate for irreplaceables alone.
- **`01_PATENTS/` "backed up off-repo"** per `.gitignore` is still an ASSERTION —
  confirm the off-repo copy exists and restores; it is ZKNOT's most irreplaceable IP.
- **`99_SENSITIVE` audit still open** — veto keeps it off the network, but its
  plaintext exposure on-disk is unverified.

---
Page 1 of 1
