# 2026-05-16 — Infrastructure & SDVOSB Strategic Planning Session

**Status:** Two strategic plans drafted, committed to vault, and operationalized in Taskwarrior.
**Workstream:** ops / gov
**Outcome:** 3-month infra buildout deferred to Tier 1 bootstrap ($340 max spend); SDVOSB procurement and compliance reference established; ~40 new tasks created with cross-references to source docs.

## What happened

Started the session intending to plan a full NAS / app server / provisioning bench
buildout. Through conversation, scope contracted significantly as real constraints
surfaced:

- Limited funds, preference to bootstrap over loans
- SDVOSB procurement route preferred for hardware acquisition
- AM5 workstation build documented in old buildout doc was never executed —
  current Linux box is i9-11900K on Z590, not Ryzen 7 7700 on B650E-F
- Windows rig (12900KF + 64GB DDR5 + RTX 4080) is the daily/gaming machine,
  not available for cannibalization
- Current workstation is genuinely sufficient for all engineering work
  through Q3+
- 107 pending Taskwarrior tasks, most around shipping PV1 — infrastructure
  is not the bottleneck

Final plan reflects reality: workstation continues as-is, infrastructure spend
limited to UPS + backup ($240–400) in Phase 1–2, NAS build deferred behind
explicit trigger gates (revenue, SBIR, or surplus availability).

## What got built

### Two strategic reference docs

1. **ZKNOT-PLAN-INFRA-001** (3-month infrastructure buildout)
   - Path: ~/ZKNOT/5_PLANS/ZKNOT-PLAN-INFRA-001_3month_buildout_20260516.md
   - 8-page reference, structured as Phase 1 (stabilize) -> Phase 2 (backup +
     surplus monitoring) -> Phase 3 (NAS, only if triggered)
   - Three budget tiers with explicit decision triggers between them
   - Paste-ready Taskwarrior add commands in Appendix
   - Cross-references SDVOSB-001 for surplus channels

2. **ZKNOT-PLAN-SDVOSB-001** (procurement, surplus, compliance reference)
   - Path: ~/ZKNOT/5_PLANS/ZKNOT-PLAN-SDVOSB-001_procurement_opportunity_20260516.md
   - 7-page reference, covers certifications, procurement channels,
     surplus channels, outreach targets, compliance maintenance, risks
   - Cross-references INFRA-001 for surplus-tied infrastructure tasks

### Taskwarrior operationalization

- 40+ new tasks created (IDs 108-153)
- Each task includes [REF: ZKNOT-PLAN-XXX section] in description
- New tags: infra, sdvosb, backup, surplus, sbir, compliance,
  capability, outreach, gate, review, bootstrap, security, cmmc
- Two monthly review tasks (152, 153) annotated with full vault paths to
  the source docs so they're discoverable from the task list
- Recurring tasks set up for: SBIR topic monitoring, surplus checks,
  capability statement refresh, monthly plan reviews

## What we learned

1. Infrastructure was the wrong place to start. The real bottleneck is
   PV1 manufacturing and the overdue ATECC provisioning decision (T#88-92,
   urgency 27.9). A NAS doesn't ship PowerVerify units.
2. Current workstation is enough. i9-11900K + 64GB DDR4 + RTX 3080 Ti +
   1.7TB NVMe is genuinely sufficient. The "minimum full capability" plan
   was sizing toward solving a problem that doesn't exist yet.
3. SDVOSB certification is leverage, not magic. Real opportunities
   exist (set-asides, surplus, SBIR) but each requires documentation,
   capability statement, past performance, and active engagement. The
   compliance calendar matters as much as the procurement opportunities.
4. Inventory drift is real. Old buildout docs from months ago said
   AM5 was planned, but checking the actual hardware showed it never
   happened. Always verify current state before planning around old
   intent.

## What changed about the plan

- NAS purchase deferred indefinitely. Trigger-gated behind PV1 revenue,
  SBIR award, or acceptable surplus availability. Re-evaluation point: 2026-07-15.
- Phase 1 spend: $240-250. UPS + ethernet cable. That's it.
- Phase 2 spend: $100-150. External SSD + restic configuration.
- All other infrastructure (NAS, app server build, VLAN deployment,
  Zeek monitoring, PiKVM) parked behind explicit gates.
- Memorial Day NAS shopping spree CANCELED. Cart items to remove:
  UGREEN DXP4800 Plus, MSI H610M, Thermaltake Smart 500W, AMD 9800X3D,
  Noctua NH-U12S SE-AM4, APC BE600M1.
- Memorial Day reasonable buys (if any): Thermalright Peerless
  Assassin 120 SE ($35), CyberPower CP1500PFCLCD UPS ($240), UGREEN
  NVMe enclosure ($18) — all sale-insensitive, can buy anytime.

## What's NOT changed

- ZKNOT vault structure (5_PLANS now houses both new strategic docs)
- Taskwarrior workstream conventions (hw, fw, sw, ip, biz, ops)
- Existing project structure (pv-rev1, zkkey-connect, zknot.sig, etc.)
- The 107 pre-existing pending tasks
- ATECC provisioning approach (cryptoauthlib, P-256, one key per device)
- Federal certifications and registrations
- Outreach targets and acquisition pipeline

## Operational state at end of day

### Vault state
- Two new plan docs committed to 5_PLANS/
- Commits exist on detached HEAD (86f340b, eb06b23) due to in-progress
  rebase — REQUIRES RESOLUTION BEFORE NEXT WORK SESSION

### Taskwarrior state
- 153 task IDs allocated, ~140+ pending
- Filter views to use:
  - task -infra -sdvosb -review list  -> daily engineering work
  - task +infra list                   -> infrastructure-only
  - task +sdvosb list                  -> procurement/compliance only
  - task project:pv-rev1 list          -> shipping work

### Outstanding from this session
- Git rebase in progress on ZKNOT main branch — resolve via abort+merge
  or continue rebase
- enp7s0 still DOWN (workstation on Wi-Fi only)
- No UPS on workstation (T#108 to address)
- 99_SENSITIVE encryption still open (T#111)
- KiCad apt repo DNS broken, MongoDB repo signing key expired —
  both fixable, neither urgent

### Carry-forward for tomorrow (2026-05-17)
- PV1-00042/43/44 cure check (T#101, M priority, due tomorrow)
- ATECC provisioning decision (T#88-92, 5 days overdue, urgency 27.9)
  — separate thread already in progress
- Resolve git rebase before any more commits land on detached HEAD

## Files committed this session

5_PLANS/ZKNOT-PLAN-INFRA-001_3month_buildout_20260516.md             (commit 86f340b)
5_PLANS/ZKNOT-PLAN-SDVOSB-001_procurement_opportunity_20260516.md    (commit eb06b23)

## References

- Source thread: Claude conversation 2026-05-16
- Related journals: 2026-05-16_mcp2221a_amazon_clones_dead_pico_back.md
- Tag glossary: pending creation at ~/ZKNOT/3_OPS/km/taskwarrior_tag_glossary.md

