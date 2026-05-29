# 2026-05-22 — KiCad PCB Editing: Drag, Back-Layer Access, DRC Cleanup

Working board: `GraipPowerVerify-Rev1.kicad_pcb` (PowerVerify product line, back-side GND pour + tamper silk).

## Moving footprints so routes follow (drag vs move)
- `M` = **Move**: picks up footprint cleanly but leaves traces dangling.
- `G` = **Drag**: moves footprint *with* connected traces attached, stretching them.
- `D` = drag a single track segment while keeping it connected to neighbors.
- For drag to behave: **Route → Interactive Router Settings** set to **Walkaround** or **Shove** (Shove is most forgiving — pushes other traces aside). Not "Highlight collisions."
- **Preferences → PCB Editor → Editing Options**: uncheck **Allow free pads**, turn on **Magnetic pads**.

## Can't grab anything on the back of the board
Checklist, in order of likelihood:
1. **Make B.Cu the active layer** — click B.Cu in Layers panel, or press `V` to flip view.
2. **High contrast mode** — press `}` to toggle off. When on, inactive layers are dimmed AND unclickable.
3. **Flip board view** — press `F` (nothing selected) or View → Flip Board View, so the back faces you.
4. **Appearance panel layer visibility** — confirm eye icons ON for B.Cu, B.Silkscreen, B.Mask, B.Paste, B.Courtyard, B.Fab.
5. **Layer preset dropdown** (top of Appearance panel) — set to **All Layers** / **All Copper Layers**, not "Front Layers."
6. **Selection Filter** (bottom-right panel) — confirm Footprints, Tracks, Vias, Pads, Graphics, Zones, and **Locked items** are all checked. Unchecked "Locked items" makes locked stuff unclickable.
7. **Unlock back items** — Ctrl+A with B.Cu active, then `L` to toggle lock.
8. **Stacked items** — Alt+click or repeat-click same spot to cycle through overlapping front/back items.

## "Save As / Save Copy" loses back-layer access
- KiCad's Save As copies the board/schematic but NOT reliably the project settings.
- The **`.kicad_prl`** file stores layer visibility, active layer, and Appearance panel state. Without it, the copy opens with defaults → back layers appear hidden.
- Fix on the copy: turn back-layer eyes on in Appearance panel, toggle high contrast off (`}`), set layer preset to All Layers.
- **Better way to duplicate a project:** close KiCad, copy the entire project *folder* in the file manager, rename it, open the `.kicad_pro` inside. Brings board + schematic + `.kicad_pro` + `.kicad_prl` + libraries.

## Rule Area vs GND pour (the accidental "lock")
- A **Rule Area** (formerly "Keepout") is NOT a copper pour. Its dialog shows Keepouts/Placement tabs with no Net field — shows as a hatched/dashed outline.
- A real **GND pour** uses the **Add a filled zone** tool — dialog lets you pick **Net = GND**.
- If a big hatched rectangle is covering the back, that's an accidental rule area: click its edge, press Delete, then redo as a filled zone.

## DRC report cleanup (DRC.rpt, 2026-05-18 — 14 violations, all warnings, 0 errors, 0 unconnected)
- **7× via_dangling (GND vias):** stitching vias in the GND pour. Press `B` to refill zones, re-run DRC — usually drops to zero. If truly just stitching, harmless; can set via_dangling severity to Ignore in Board Setup → Design Rules → Violation Severity.
- **lib_footprint_mismatch (J2 Pigtail_USB-C):** board copy drifted from ZKNOT library. Intentional if edited on-board. Clear via "Update Footprint from Library" or accept local override.
- **TAMPER silk text:** 0.6 mm tall / 0.075 mm thick vs board min 0.8 mm / 0.08 mm. Bump text size, or lower mins in Board Setup → Design Rules → Constraints. Also overlapping "Patent Pending 63/961,118" text — nudge one.
- **silk_over_copper (GND, VBUS labels on J2):** silk too close to THT pads, clipped by mask. Move labels ~0.5 mm off the pads or accept the clip.
- **silk_overlap (patent text over rectangle):** move one or the other.
- Fast workflow: open board, press `B` to refill zones, re-run DRC, then double-click each remaining issue in the DRC panel to jump to it and nudge.

## Next action when back from trip
- Refill zones (`B`), re-run DRC, clear silk overlaps on TAMPER / patent text / J2 labels.
- Decide whether to set via_dangling to Ignore for GND stitching vias.
