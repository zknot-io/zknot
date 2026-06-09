---
date: 2026-06-01
topic: centralized-storage-smb
author: William Shane Wilkinson
workstream: ops
tags: [infra, storage, samba, smb, nas, backup]
related:
  - ZKNOT-PLAN-INFRA-001
  - (pending) ZKNOT-PLAN-INFRA-002
  - (pending) km/systems/network-storage.md
status: complete
---

# 2026-06-01 — Centralized storage between Debian and Windows (SMB), NAS deferred

## TL;DR

Stood up a working centralized file share today for $0 using hardware already on
hand. Debian workstation (`mt`, 10.0.0.162, Wi-Fi) hosts a Samba share at
`/srv/share`; Windows box (`mtpc`, 10.0.0.148, wired) mounts it as a persistent
`Z:` drive. Write verified across the network. No switch was needed — both
machines were already on the same 10.0.0.0/24 subnet routing through the existing
router. Separately, reworked the NAS plan: decided to defer the build and buy the
*right* parts as income comes in rather than rush a deadline build, and corrected
multiple hardware-spec errors found in INFRA-001 along the way.

## What happened

- Confirmed the two machines could see each other on the existing network before
  adding any hardware. Ping Windows -> Debian succeeded (first packet ~1s due to
  Wi-Fi radio power-save wake, subsequent packets 1-3ms).
- Installed Samba on Debian, defined a single scoped share `[share]` ->
  `/srv/share` (deliberately NOT `$HOME`, NOT the ZKNOT vault, NOT 99_SENSITIVE).
- Created Samba user `mt` (separate credential from Linux login).
- Enabled `smbd`/`nmbd` to auto-start on boot (survives reboot — confirmed concept,
  verifying with `systemctl is-active` post-reboot).
- Mapped `Z:` on Windows with `net use ... /persistent:yes`.
- Write test: created `Z:\test.txt` from Windows; `dir Z:` showed the file at
  46 bytes — write across the share verified.
- No `ufw` present on Debian, so no firewall rule needed.

## Decisions

1. **Defer the NAS build; buy the right parts as income comes in.** Rather than
   rush a deadline build, build the correct system over time. This overrides the
   "build this week" impulse and also sits ahead of INFRA-001's original July-15
   Phase-3 gate — recording it here as a deliberate deviation, not a silent one.

2. **NAS will be ECC + IPMI + current-gen socket, not a consumer build.** Target
   platform: ASRock Rack B650D4U family (AM5, DDR5 ECC UDIMM, IPMI). Rationale: the
   box's job is protecting irreplaceable data for years; integrity and remote
   management outrank raw specs. Board variant / case / CPU forks still OPEN
   (pending INFRA-002).

3. **Do NOT reuse the G.SKILL Trident Z5 DDR5-6000 kit in the NAS.** It is
   non-ECC; the build is ECC. It stays gaming inventory. (Also corrected: this kit
   is DDR5 U-DIMM, not the "DDR4-3200" that INFRA-001 incorrectly recorded.)

4. **SMB share is the interim bridge, not the destination.** `/srv/share` solves
   the file-scatter problem now; the NAS is the eventual real store. Keep the share
   one-directional (Windows -> Debian) — single source of truth, no "which copy is
   current" ambiguity.

5. **No switch needed for connectivity.** The Omada TP-Link switch buys wired
   ports, speed, and future VLANs — not connectivity the router already provides.
   Switch work stays deferred to the network phase, after NAS parts arrive.

## Corrections logged against INFRA-001

INFRA-001 contained several hardware-spec errors that would have caused failed/
returned orders if bought as written. Flagging so the doc gets superseded, not
re-trusted:

- "DDR4-3200" kit is actually **DDR5-6000 U-DIMM** (and non-ECC — wrong for NAS).
- Path A spec'd **SODIMM** (laptop RAM); desktop boards take full-size U-DIMM.
- Path A paired a **microATX board + ATX PSU + 155mm cooler** with the **Jonsbo N3**,
  which is **Mini-ITX only, SFX-only, 130mm cooler max** — three parts wouldn't fit.
- Path B assumed reusing DDR4 on a DDR4 board — impossible with a DDR5 kit.

## Open / next

- [ ] Verify `systemctl is-active smbd nmbd` returns active after reboot.
- [ ] Decide GitHub-vs-share split: what gets version-controlled vs. what lives
      only on the share (binaries, large files, scratch). **NEXT.**
- [ ] Choose INFRA-002 forks: board variant (2L2T/BCM vs plain), case
      (Node 804 vs Jonsbo N4), CPU (Ryzen 7600 vs EPYC 4004).
- [ ] Generate ZKNOT-PLAN-INFRA-002 (supersedes 001), commit to 5_PLANS/, mark
      001 superseded.
- [ ] Promote durable facts to km/systems/network-storage.md.

## ⚠️ Backup / risk flags (unresolved)

- **`/srv/share` is one disk on a box with no off-machine backup.** Fine for
  working files and scratch; NOT a safe sole home for anything irreplaceable
  (patent drafts, filed records) until the NAS + offsite (restic -> external SSD +
  B2/rsync.net) plan exists. This is INFRA-001 Phase 2, still open.
- **This journal entry is the only record of today's decisions** until committed
  to git in the ZKNOT vault.
- **99_SENSITIVE plaintext audit** still pending per INFRA-001 — must be done
  before anything sensitive could ever go near a share.

---
Page 1 of 1
