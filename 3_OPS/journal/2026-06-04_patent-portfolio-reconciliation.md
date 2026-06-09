---
date: 2026-06-04
topic: Patent portfolio reconciliation + PAT-019 added to tracker
type: journal
workstream: ip
tags: [patents, pat-019, tracker, doc-001, doc-003, powerverify, puf, patent-center]
status: complete
related: [DOC-001 patent tracker, DOC-003 all-patents summary, PAT-019, PAT-002, PAT-013, PAT-014]
---

# Patent Portfolio Reconciliation + PAT-019

## TL;DR
Cross-checked the patent tracker (DOC-001) against the all-patents summary (DOC-003) and the
Patent Center Receipt History. All **18** filed provisional application numbers are now
primary-verified against Patent Center. PAT-019 (the system umbrella, App# 64/038,840) was
missing from both documents and from the tracker's ground-truth table; added it and corrected
the filed count from 16 to 18. The summary doc needs four edits. Separately confirmed PowerVerify
ships transparent **and** with the holographic-glitter PUF — both UVPs coexist; the provisioning
doc's claim that the glitter "trades the see-no-data-lines UVP" is wrong at this density.

## Decisions
1. **Filed provisional count is 18, not 16.** The tracker header/dashboard "16" was stale and
   miscounted (it listed 17 rows but said 16; PAT-019 makes 18). Tracker updated to 18.
2. **PAT-019 = App# 64/038,840**, priority date **04/14/2026** — the filing date governs over the
   "April 3" on the spec cover. Patent Center 75289198, Conf# 8722. Primary-verified.
3. **All 18 application numbers verified against Patent Center Receipt History** — now safe for
   government-facing use. (Per-item as-filed titles still to be confirmed individually.)
4. **PAT-013 as-filed title is the tracker's** ("Authenticated Heartbeat Key Erasure for Unmanned
   Aerial Evidence Systems"). The summary doc's title is wrong; correct the summary to the filing.
5. **PAT-014 was never filed** — absent from all 30 Patent Center submissions. It's a draft
   consolidated into PAT-015. Do not assign it an application number.
6. **PowerVerify keeps transparency AND carries the glitter PUF.** Confirmed from the physical
   unit (PV1-00053): board readable through the pot, glitter scattered in the same clear epoxy.
   The provisioning doc's "trades the UVP" line is incorrect and should be corrected.
7. **Did not write unverified data into the ground-truth tracker** — left fee totals and PAT-019
   conversion strategy/target/cost for manual reconciliation rather than baking in guesses.

## Open items / follow-ups
- Reconcile USPTO **fee totals** — every fee cell still reads "$1,405 (16×$65...)"; unverified.
  Update from card statements (some receipts showed "ack only," no fee line).
- Confirm **63/961,116 (PAT-006b EvidenceProtocol)** micro-entity SB15A cert actually posted —
  single submission, no cert/receipt row in supporting-docs sheets.
- Identify what the **2026-03-20 submission batch** on the five core January apps was
  (assignment recordation? supplemental?) and log it.
- Apply **four summary-doc edits**: add PAT-019, add PAT-006 OfflineEvidence (63/978,480),
  correct PAT-013 title, remove/relabel PAT-014.
- Set **PAT-019 conversion strategy / target / cost** with attorney (umbrella system claim).
- Before claiming PUF *verification* publicly: run the **entropy test** at current glitter
  density (10 same-unit photos vs 1-each of 10 units; confirm Hamming distributions don't overlap).
- **Commit** updated tracker + PAT-019 receipt set to the git vault; verify tracker formatting via
  diff before replacing the master.
- Forward (confirm w/ counsel): micro-entity **four-application limit** excludes provisionals, so
  the 18 are fine — but non-provisional conversions count; ~5th conversion may drop micro-entity
  status to small-entity fees.

## Promote to systems docs (not journal)
- `km/systems/patents.md`: Provisionals are not publicly inspectable; the public Patent Center
  application-number search will always return "not available" for them. The account Receipt
  History and the stamped USPTO receipts are the proof of filing until a non-provisional publishes.
- `km/systems/patents.md`: The **as-filed title (Patent Center) is the governing record**;
  reconcile internal docs to it, never the reverse.
- `km/systems/powerverify.md`: Sparse holographic glitter preserves epoxy transparency while still
  carrying an **optical PUF**; a silicon PUF is incompatible with the chipless passive design.
- `km/systems/powerverify.md`: verifyknot.io currently does identity lookup, **not** PUF-image
  matching — "PUF verification" cannot be claimed publicly until the imaging pipeline + entropy
  test ship.

## Curiosity / personal monopoly
The transparent-AND-PUF power cable is genuinely uncopyable on a short timescale — a competitor
would have to rebuild manufacturing + a registration backend to match it. Worth treating the
epoxy-fingerprint capture protocol as a reusable primitive across ZKKey/SelfKnot, not just
PowerVerify. Ties to the broader uncrowded intersection: PUF + Federal Rules of Evidence + SDVOSB.

## Follow-up tasks (Taskwarrior)
```bash
task add "Apply 4 edits to DOC-003 all-patents summary (add PAT-019, add PAT-006, fix PAT-013 title, relabel PAT-014)" project:zknot.ip workstream:ip priority:H
task add "Reconcile USPTO fee totals in DOC-001 tracker from card statements" project:zknot.ip workstream:ip priority:M
task add "Confirm PAT-006b (63/961,116) SB15A micro-entity cert posted in Patent Center" project:zknot.ip workstream:ip priority:M
task add "Run PUF entropy test: 10 same-unit vs 10 cross-unit perceptual-hash Hamming distances" project:zknot.fw workstream:fw priority:M
task add "Commit updated DOC-001 tracker + PAT-019 receipt set to git vault" project:zknot.ops workstream:ops priority:H
```

---
*ZKNOT, INC. — William Shane Wilkinson — Journal — Page 1 of 1*
