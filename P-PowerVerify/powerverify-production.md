---
title: PowerVerify Production — Runbook, Critical Path & Cost Model
system: powerverify-production
status: active
batch_size: 10
created: 2026-06-04
owner: Shane
---

# PowerVerify Production — Runbook, Critical Path & Cost Model

## TL;DR

- **First-batch wall-clock time (10 units): ~98 hours (~4.1 days continuous)**, gated by two long waits: pot prep (~44 h: print + dry) and epoxy cure (48 h).
- **Hands-on labor: ~10 hours per batch of 10.** Everything else is machine or cure time you can walk away from.
- **Recurring cost: ~$9.13/unit (~$91.30/batch of 10).** Complete BOM. Largest lines: pigtail ($1.50), conformal coat ($1.50), PCB ($1.00), filament ($1.00), Mann Ease Release ($0.90), epoxy ($0.77), label ($0.625).
- Component prices confirmed as **dollars**. Two cost lines worth re-verifying: epoxy yield (fl oz vs weight oz) and labels-per-roll (drives the $0.625 label line).

---

## Process Steps (batch of 10)

| # | Step | Duration | Type | Notes |
|---|------|----------|------|-------|
| 1 | Print pots (10) | 20 h | Machine (unattended) | Filament destroyed on removal |
| 2 | Spray pots — self-leveling enamel *or* conformal coating | ~0.25 h labor + **24 h dry** | Labor + wait | Open decision: enamel vs conformal (see Tradeoffs) |
| 3 | Print labels, assign ZK number + serial | 1 h | Labor | |
| 4 | PCB component placement (10 boards) | 1 h | Labor | |
| 5 | Bake & cool | 0.5 h | Machine + wait | Reflow/cure cycle |
| 6 | Prep pigtails: solder + heat-shrink for strain relief | 1 h | Labor | |
| 7 | Prep boards for potting (silicon dust slug in female end + hot-glue seal; hot-glue around USB-C female to block epoxy from male end; dam cable exit + hot-glue) | 1 h | Labor | |
| 8 | Epoxy + glitter mix | 0.5 h | Labor | ~40 g mixed epoxy per pot |
| 9 | Pour | 2 h | Labor | |
| 10 | Cure | **48 h min** | Wait | |
| 11 | Remove + tear off pots | 2 h | Labor | Pots destroyed |
| 12 | PUF photo, front + back | 1 h | Labor | |

**Total hands-on labor:** ~10.25 h/batch.

---

## Critical Path

The batch runs as **two parallel tracks** that converge at the epoxy pour.

```
TRACK A — POTS (44.25 h elapsed)
  Print 20h ──> Spray ~0.25h ──> Dry 24h
                                        \
                                         ──> [POUR-READY]
TRACK B — BOARDS (4.5 h labor, fits inside Track A window)
  Labels 1h ─> Placement 1h ─> Bake/cool 0.5h ─> Pigtails 1h ─> Board prep 1h
                                        /
CONVERGE ──> Mix 0.5h ─> Pour 2h ─> Cure 48h ─> Remove pots 2h ─> PUF 1h
```

| Phase | Elapsed |
|-------|---------|
| Track A (pots: print + spray + dry) | 44.25 h |
| Mix + pour | 2.5 h |
| Cure | 48 h |
| Remove pots | 2 h |
| PUF photos | 1 h |
| **Critical path total** | **~97.75 h (~4.1 days)** |

Track B (boards, 4.5 h labor) runs entirely inside the 44 h pot window, so it adds **zero** to the critical path as long as you do it during the print/dry wait.

---

## Steady-State / Pipelining (beyond batch 1)

For continuous production, throughput is no longer gated by total critical path — it's gated by the **single most-occupied resource per batch**:

- **3D printer:** 20 h to print 10 pots = **2 h/pot of printer time**. With one printer, this is the most likely steady-state bottleneck.
- **Cure capacity:** 48 h tying up pots + cure space. If you only have 10 pots' worth of mold capacity, cure also throttles you.

Implication: while batch N cures (48 h), the printer should already be running batch N+1's pots (20 h). The printer finishes well before the cure does, so a **second printer or larger pots-per-print does not help** until you also expand cure/pot capacity. Bottleneck is the cure+pot-inventory pair, not the printer — *unless* you scale cure capacity, at which point the printer becomes the limit.

---

## Bill of Materials — Recurring

### Known (per unit)

| Item | Unit cost | Basis | Per unit |
|------|-----------|-------|----------|
| USB-C pigtail cable | $1.5000 | $60 / 40 pigtails | $1.5000 |
| USB-C female receptacle | $0.5186 | each | $0.5186 |
| Diodes (2/board) | $0.1890 | each | $0.3780 |
| Capacitor (1/board) | $0.1233 | each | $0.1233 |
| PCB | $1.0000 | $100 / 100 boards | $1.0000 |
| Pot filament | $1.0000 | $10 / 10 pots | $1.0000 |
| Epoxy resin (40 g mixed) | $0.0192/g | $20 / ~1,041 g kit (~26 pots) | $0.7684 |
| Heat shrink (adhesive-lined, 1) | $0.0500 | $20 / 400 pcs | $0.0500 |
| Conformal coating spray | $1.5000 | $45 / 30 pots | $1.5000 |
| Mann Ease Release | $0.9000 | $27 / 30 pots | $0.9000 |
| Glitter | $0.4000 | $40 / 100 pots | $0.4000 |
| Hot glue stick (1) | $0.2000 | $5 / 25 sticks | $0.2000 |
| Silicon dust plug | $0.1200 | $6 / 50 plugs | $0.1200 |
| Label (DK-2205) | $0.6250 | $25 / 40 labels per roll | $0.6250 |
| Vinyl gloves | $0.0900 | $9 / 100 gloves (~few pairs/batch) | ~$0.0500 |
| **TOTAL** | | | **~$9.13** |

- **Per unit: ~$9.13**
- **Batch of 10: ~$91.30**

> **Epoxy yield note:** "$20 per 32 oz" read as 32 *fluid* oz (946 mL × ~1.1 g/mL ≈ 1,041 g mixed) → ~26 pots/kit, $0.7684/unit. If the bottle is 32 oz *by weight* (~907 g) → ~23 pots/kit, ~$0.88/unit. Confirm against the label.

> **Label cost flag:** at $25/roll yielding only 40 labels, the label ($0.625) is the 3rd-most-expensive line — bigger than diodes + cap + glitter + glue + plug combined. If a DK-2205 roll actually yields more labels at your print size, this drops fast (e.g. 400 labels/roll → $0.0625). Worth verifying actual labels-per-roll.

> **Gloves:** allocated as a rough ~$0.05/unit (a few pairs across a 10-unit batch). Adjust if you burn through more.

---

## Capital / One-Time Equipment

Not amortized into per-unit cost here — list for total startup outlay.

| Item | Cost |
|------|------|
| 3D printer | NEED PRICE |
| Label printer | NEED PRICE |
| PUF camera | NEED PRICE |
| PC | NEED PRICE |
| Glue gun | NEED PRICE |
| (Scale, mixing cups, etc.) | NEED PRICE |

---

## Tradeoffs / Open Decisions

**Pot coating — resolved: conformal coating ($1.50/pot).** Finish sequence: **mirror-finish the 3D-printed pot interior**, then lay down one or two passes of conformal coat so the cured face reads like glass. Mann Ease Release ($0.90/pot) is the actual release agent on top of that. Self-leveling enamel was the alternative (cheaper, but thicker/softer, risks transferring texture and gumming on tear-off). Conformal chosen for the glass look + clean release.

**Next-version idea (not current batch):** print a *raised ZKNOT indention* into the pot so each cast unit carries a molded ZKNOT mark — a fine-touch brand/anti-counterfeit detail. Deferred to a future pot revision.

**On PUF:** the PUF *is* the glitter — a small amount suspended in otherwise fully transparent epoxy. The unique 3D distribution of glitter is the unclonable fingerprint; the medium stays clear. There is no molded-surface-texture fidelity concern, so the coating choice is a finish/release decision, **not** a PUF-capture decision. The front/back photos (step #12) are the **evidentiary baseline**: the holder photographs the unit on receipt and re-compares periodically to detect tampering/swap.

**Batch size 10 vs. continuous.** Larger batches amortize the 10 h setup labor better, but increase epoxy waste risk if a mix goes bad and tie up more cure/pot inventory. The cure+pot pair is your scaling constraint, not labor.

---

## Open Questions / TODO

- [x] Component prices — **confirmed dollars**.
- [x] Epoxy price — **$20/32 oz; ~$0.77/unit** (verify fl oz vs weight oz on label).
- [x] Coating decision — **conformal coating chosen** (mirror finish + glass-look pass).
- [x] All consumables priced — **BOM complete at ~$9.13/unit**.
- [ ] Verify actual DK-2205 labels-per-roll (drives the $0.625 label line — could drop sharply).
- [ ] Confirm pot inventory + cure-station count (sets steady-state throughput).
- [ ] Capital equipment costs for total startup figure.
- [ ] Future pot rev: raised ZKNOT indention.
