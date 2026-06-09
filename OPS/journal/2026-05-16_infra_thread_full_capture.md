# 2026-05-16 — Full Infrastructure Thread Capture (Pre-Trip Brain Dump)

**Status:** Comprehensive capture of a long planning thread before deletion. Everything decided, discussed, or deferred is recorded here.
**Workstream:** ops / gov / hw
**Outcome:** Two strategic docs created (committed), ~40 tasks added, hardware decisions made, Reddit thread active, LinkedIn drafts ready. Thread can be safely deleted after this journal commits.

---

## CORE DECISIONS MADE

### Infrastructure: Tier 1 bootstrap, defer everything else
- Current i9-11900K workstation (Z590, 64GB DDR4, RTX 3080 Ti, 1.7TB NVMe,
  Debian Trixie) is SUFFICIENT for all engineering through Q3+. Do not replace.
- The AM5 build in old buildout docs was NEVER executed. Disregard those docs.
- Windows rig (12900KF + 64GB DDR5 + RTX 4080) is daily/gaming, not for cannibalization.
- Phase 1 spend: $240 (UPS) + cable. Phase 2: $100-150 (external SSD + restic).
- NAS build DEFERRED behind trigger gates (revenue, SBIR, or surplus). Gate review 2026-07-15.
- Two strategic docs created and committed:
  - 5_PLANS/ZKNOT-PLAN-INFRA-001_3month_buildout_20260516.md
  - 5_PLANS/ZKNOT-PLAN-SDVOSB-001_procurement_opportunity_20260516.md

### NAS build (WHEN gate triggers, not now)
- Reddit r/truenas consensus (3 independent experienced builders): go W680 + IPMI,
  NOT cheap B760M. The expensive answer is the cheap answer over 5 years.
- Specific advice received:
  - EmmaRoidz: W480 + used Xeon w-1390p, proper ECC, low idle, strong under load
  - h0lz: IPMI board for remote console; mirrored M.2 SSDs for Docker containers;
    PCIe-to-dual-M.2 adapters exist (watch bifurcation requirement)
  - Thefurnacemaster: ran Jonsbo N3 for years, functional but ITX cable mgmt is hard,
    most mITX boards only have 4 SATA (need HBA or M.2-SATA adapter for 8 drives),
    drives ran warm, eventually moved to rackmount. Treat N3 as 1-2 year platform.
- UPDATE TO INFRA DOC: change Phase 3 recommendation from B760M to W680+IPMI.
  Do this at June 15 monthly review.
- Components when building: Jonsbo N3 ($160) OR rackmount; ASUS Pro WS W680-ACE IPMI
  ($396); i3-14100 or i5-14500; Thermalright Peerless Assassin 120 SE ($35);
  Corsair RM650e ($105); 4-6x WD Red Pro / Seagate IronWolf Pro 12TB (mix brands,
  split retailers); 256GB boot NVMe; 2x 500GB NVMe mirror for special vdev.

### Network architecture (target, build incrementally)
- 3-tier physical: NAS (vault) + app server (engine) + provisioning bench (bench)
- Gear on hand: Protectli VP2420 (OPNsense), TP-Link TL-SG2008P (Omada PoE switch),
  Dualcomm ETAP-2003 (passive TAP)
- VLAN plan: 10=Trust, 20=Mfg, 30=Mgmt, 40=Guest. Mfg can reach Trust API only.
- Pi assignments (future): Pi Zero = Pi-hole DNS; Pi 4 = Tailscale exit + restic
  orchestrator + Uptime Kuma; Pi 5 = Zeek/ntopng on TAP (currently on ATECC bench duty);
  Jetson Nano = future PUF image preprocessing.

### Calendar / email — moving off Google
- No Google Calendar tool available in chat anyway.
- Long-term: khal + vdirsyncer + CalDAV (Radicale self-hosted on NAS, or Fastmail/Migadu).
- Phone sync via DAVx5 (Android) or native iOS CalDAV.
- Mail: do NOT self-host outbound. Use Migadu/Fastmail/Mailbox.org, or Mailcow +
  external SMTP relay later. Already have ops@zknot.io on Cloudflare Email Routing.
- todoman can unify Taskwarrior-style VTODO via same CalDAV backend (optional).

### 3D printer — Bambu P1S now, Voron long-term
- Bambu P1S confirmed owned and working great. Keep using it.
- FEDERAL SUPPLY CHAIN ISSUE: Bambu is Chinese-owned, cloud lock-in history,
  Section 889 / CMMC implications for DoD work. Run LAN-only mode meanwhile.
- Voron 2.4/Trident is the long-term answer: open firmware (Klipper on Pi),
  self-hosted control plane (Moonraker/Mainsail), sourceable/documentable supply chain,
  CMMC-defensible. ~$1,500-2,000 in parts, 40-80hr build. This is a 2027 question.
- Slicers all run on Linux (Bambu Studio, PrusaSlicer, OrcaSlicer). Printer OS-agnostic.

### Document/scan/print hardware
- Moving away from ScanSnap (no Linux support) and HP M479fdw (flaky on Linux).
- Scanner: Ricoh fi-8170 ($799) — network-enabled, justified for federal doc workflow.
  VERIFY sane-fujitsu or sane-airscan support before/after purchase: scanimage -L
- Printer: Brother HL-L8360CDW ($570) — best-in-class Linux support (brlaser, IPP
  Everywhere), print-only (decoupled from scanner). Added to cart but is a Tier-2
  spend against bootstrap plan — HP still works, could have deferred.
- Label printers for PUF/PowerVerify: Brother QL-820NWB (brother_ql Python lib),
  Zebra ZT230 (ZPL), Brady (verify Linux support before buying).

### Solder / manufacturing supplies
- SWITCHED from leaded to lead-free for production (RoHS/federal compliance).
- Buy: MG Chemicals 4900 SAC305 0.032" 1/4lb ($42.85) + SAC305 tip tinner ($21) +
  no-clean flux paste ($8).
- Keep leaded 63/37 for prototype/rework on NON-shipping boards only.
- WRITE lead policy doc in 6_SIG/hardware/: "Production = SAC305. Prototype = leaded OK."
- Skip: solder paste (no stencil/reflow workflow yet), YIHUA station (existing iron fine),
  cheap unbranded SAC0307 (not real SAC305).
- MG Chemicals 832WC water-clear epoxy ($95) in cart — directly feeds PV1 manufacturing.

---

## FINANCIAL FRAMING

- Running low on funds, prefer bootstrap over loans.
- Budget tiers: Tier 0 strict ($0-30), Tier 1 recommended ($340-400), Tier 2
  revenue-funded (~$2,100), Tier 3 SBIR-funded ($2,500-3,000).
- Decision triggers documented in INFRA-001 for moving between tiers.
- Current Amazon cart at time of thread: ~$1,575 (fi-8170 + Brother + epoxy +
  dollies + SAC305 supplies). Higher than bootstrap plan called for — Brother
  printer is the discretionary line.

---

## SDVOSB / FEDERAL (full detail in PLAN-SDVOSB-001)

- Certs: ZKNOT INC, UEI C4SKW13JPEL5, CAGE 1AHZ4, EIN 36-5165991, SDVOSB via
  SBA VetCert (~May 2026), SAM.gov renewal 2027-03-17.
- Procurement channels: VA Vets-First set-asides (FAR 19.14 / 38 USC 8127),
  GSA MAS IT (defer until past performance exists), SBIR/STTR (best near-term play),
  APEX Accelerator (already engaged, Sara Ortiz).
- NAICS to verify in SAM: 541330, 541512, 541715, 334290, 334418, 541380, 541990.
- Surplus channels: GSAXcess (registered), GovPlanet (set saved searches for
  APC SmartUPS / Dell PowerVault / rackmount), Utah State Surplus (registered),
  Hill AFB DLA disposition (research contact).
- Compliance future: CMMC Level 1 self-assessment by EOY 2026; TAA/BAA
  country-of-origin tracking for PV1; Section 889 (ties to Bambu->Voron decision).
- Capability statement (1 page) needed by end of June.
- Events: VA OSDBU ICF session May 28 3:30pm MT; GSA Intro May 27 Layton;
  WarU May 14 (past).
- Named outreach Green/Schneier/Pfefferkorn — clarify if procurement/advisory/legal.

---

## TASKS ADDED THIS SESSION (IDs 108-153)

- Tags introduced: infra, sdvosb, backup, surplus, sbir, compliance, capability,
  outreach, gate, review, bootstrap, security, cmmc.
- Each task has [REF: ZKNOT-PLAN-XXX section] inline.
- Monthly review tasks (152, 153) annotated with full doc paths.
- Filter views:
  - task -infra -sdvosb -review list   -> daily engineering focus
  - task +infra list / task +sdvosb list
  - task project:pv-rev1 list          -> shipping work
- Two extra hardware tasks discussed but maybe not yet added:
  - Verify Ricoh fi-8170 SANE/airscan Linux compat
  - Defer HP M479fdw replacement until failure/surplus
  - Confirm Brother QL-820NWB brother_ql workflow for PUF labels
  - PARKED: Voron build for federal supply chain compliance
  - Document Bambu P1S firmware/network/LAN-only status in 6_SIG/hardware/

---

## CONTENT DRAFTED (not yet posted)

### Reddit r/truenas replies (thread at 2.5k views)
- Drafted replies to EmmaRoidz, h0lz, Thefurnacemaster (in chat, copy if wanted).
- Reply hygiene: no ZKNOT/SDVOSB/federal mention, no product links, build karma.
- Post within 24-48h to keep thread alive. Reply to freshest (EmmaRoidz) first.

### LinkedIn post (3 options drafted)
- Option 1 "honest founder" (recommended): bootstrap reality, 3 insights
  (cheapest=do nothing, supply chain matters, patience is the skill).
- Option 2 "what I'm learning" (shorter/lighter).
- Option 3 "technical builder" (engineering judgment on own ops).
- Hashtags: #SDVOSB #Bootstrapped #HardwareStartup #VeteranOwned (3-5 max).
- Best post time: Tue-Thu 8-9am MT. Don't screenshot Reddit (cross-platform doxx).

---

## OUTSTANDING ISSUES TO RESOLVE

1. GIT REBASE IN PROGRESS on ZKNOT vault — plan commits landed on detached HEAD
   (86f340b INFRA, eb06b23 SDVOSB). MUST resolve before more commits. Safe path:
   git branch rescue-branch; git rebase --abort; git checkout main;
   git merge rescue-branch; git push. Or git rebase --continue if intentional.
2. enp7s0 (2.5GbE) still DOWN — workstation on Wi-Fi. Plug into TP-Link switch.
3. No UPS on workstation. 3-day uptime, one brownout from data loss. Buy CyberPower
   CP1500PFCLCD ($240).
4. 99_SENSITIVE still plaintext on disk (flagged since 2026-04-18). Encrypt or move.
5. KiCad apt repo DNS broken (packages.kicad.org not resolving), MongoDB repo
   signing key expired. Both fixable, non-urgent. resolvectl not installed (use
   /etc/resolv.conf or systemd-resolved alternative on this box).
6. This journal commits AFTER the rebase is resolved (or it lands on detached HEAD too).

---

## CARRY-FORWARD PRIORITIES (post-trip)

1. PV1-00042/43/44 cure check (T#101) — was due 2026-05-17.
2. ATECC provisioning decision (T#88-92, overdue, urgency 27.9) — Adafruit 4471 vs
   Pico-as-USB-I2C-bridge. Handled in separate thread.
3. Resolve git rebase.
4. June 15: monthly infra + SDVOSB review (update INFRA-001 Phase 3 to W680+IPMI).

---

## KEY MENTAL MODELS FROM THIS SESSION

- Infrastructure is subordinate to shipping PV1. A NAS doesn't ship product.
- The cheapest thing is often doing nothing — audit before buying.
- Verify current state before planning around old intent (the AM5 build never happened).
- "Own the stack" philosophy extends to manufacturing (Voron) and supply chain (lead-free, US/EU sourcing).
- Discipline = choosing the smallest version of the right answer.
- Every hour on infra is an hour not shipping. Infra can wait, the customer can't.

