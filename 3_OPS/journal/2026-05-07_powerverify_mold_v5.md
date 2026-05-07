# 2026-05-07 — PowerVerify Potting Mold v5 + Cable Shim

## Summary

Completed clean-sheet redesign of PowerVerify potting mold (v5) plus
companion cable shim. Both files manifold, rendered to STL, ready to print.
Major shift from v3/v4 lineage: abandoned internal PCB locating features
(rails, plug bumps, support tabs) in favor of a clean rectangular pot with
external sacrificial USB-C plug holding the PCB during cure.

## Decision: External-Plug Locating Strategy

Previous mold versions (v3/v4) tried to locate the PCB inside the cavity
using printed-in features: support rails, plug bumps that filled the
female USB-C slot, support tabs flanking the strain relief boot. Each
iteration revealed new fitment problems — rail spacing tolerances,
plug bump width vs USB-C female slot tolerances, tabs blocking the boot,
cable centerline below PCB plane causing geometry conflicts.

v5 replaces all of that with: a USB-C-shaped hole through the connector-end
wall. A sacrificial USB-C cable plugs into the PV1 PCB from outside the
mold and passes through the hole, suspending the PCB at the correct
height during cure. Hole is sized for the male plug (8.5 x 3.0 mm
stadium), not the female receptacle. PCB self-locates via its own
USB-C connector geometry.

Trade-offs accepted:
  - Need a sacrificial USB-C cable per pour (plug stays embedded in
    epoxy at the connector edge until cure releases). Cheap.
  - Mold must be removed first, then sacrificial plug pulled or trimmed.
  - Lose the "pour-through" simplicity of an enclosed cavity, but gain
    much simpler geometry and no print-tolerance failures.

## Final v5 Geometry

  Outer block:    95 x 35 x 16 mm (physical)
  Cavity:         91 x 31 x 14 mm
  Walls:          2 mm uniform (sides + floor)
  USB-C hole:     8.5 W x 3.0 H mm, stadium/oval, z=7.5 to 10.5
                  from internal floor (matches male plug profile)
  U-channel:      4 mm wide, semicircular bottom at z=4, open to rim
                  (cable lays in from above)

  Cavity volume:  39.5 mL (vs v4's 23.5 mL — 68% larger pour)
  Pour planning:  ~24 units per quart of EpoxAcast 690 (down from ~40 at
                  v4 cavity volume)

## Cable Shim (companion part)

  Plate:          10 W x 14 H x 1 mm thick
  Cable notch:    bottom-center half-circle, r=1.8 mm
                  (snug on 3.5 mm cable OD)
  Function:       Drops over cable from outside; flat face seals against
                  cable-end exterior wall, covering the U-channel gap
                  above the cable. Held with tape during pour.

## Files Produced

  /home/claude/PowerVerify_Mold_v5.scad
  /home/claude/PowerVerify_Mold_v5.stl
  /home/claude/PowerVerify_Cable_Shim.scad
  /home/claude/PowerVerify_Cable_Shim.stl

  All also in /mnt/user-data/outputs/powerverify-mold-v5/
  (need to be moved into ZKNOT vault on next sync — see tasks below)

## Iteration History (this session)

  v5.0  Clean pot, rect USB-C hole 9x4, rect U-channel 4mm wide
  v5.1  Bumped cavity 1mm wider/longer, dropped USB-C hole 1mm
  v5.2  Dropped USB-C hole another 2mm; oval USB-C, U-shaped channel
  v5.3  Moved USB-C hole back up 1.5mm; tightened to 8.5x3.0 (plug-sized)
  ----  Cable shim added as separate part

## Open Questions / Risks

  - USB-C hole tightness: 8.5x3.0 has ~0.16 mm clearance per side over
    nominal 8.34 mm plug width. Print tolerance on a Bambu A1/P1S is
    typically +/-0.2 mm; first article may need light sanding to fit.
    Acceptable per zknot.

  - Shim seal quality: epoxy is viscous (~3000 cP for EpoxAcast 690 mixed)
    so a tape-held shim should hold for the ~30 min working time.
    If leakage observed at first pour, options are:
      (a) thin layer of mold release / petroleum jelly around shim edge
      (b) thicker shim (2 mm) that wedges into U-channel itself
      (c) hot glue bead around shim perimeter

  - Sacrificial plug release: epoxy will bond to USB-C plug overmold.
    Need to verify plug can be (a) cleanly broken off after demold,
    leaving flush face, or (b) cut with razor flush to potted unit.
    Test-cut on first article.

  - Bottom-of-pot finish: PCB silkscreen-back face will be visible
    through floor of potted unit (potted side becomes display side).
    Confirm this is acceptable for marketing/aesthetic, or decide
    to flip orientation. Current v5 doesn't care which way the
    PCB is oriented bottom-vs-top — only constraint is USB-C hole
    height matches PCB connector centerline.

## Next Concrete Actions

  1. Slice + print PowerVerify_Mold_v5.stl (single unit first)
  2. Print 3x PowerVerify_Cable_Shim.stl
  3. Dry-fit a reflowed PV1 PCB:
     - Insert sacrificial USB-C through hole, plug into PCB
     - Lay cable into U-channel
     - Drop shim over cable, tape outside
     - Verify PCB sits flat, cable doesn't strain at exit
  4. If dry-fit OK: do a water test (pour water as proxy for epoxy)
     to verify shim seal before risking $$ epoxy
  5. First epoxy pour: PV1-00001 (the unit photographed for v4 work)
