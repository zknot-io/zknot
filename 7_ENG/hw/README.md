# ZKNOT Hardware Engineering

KiCad projects and supporting hardware artifacts for all ZKNOT products.

## Layout

- `kicad-libs/` — shared symbols, footprints, 3D models (global libs)
- `kicad-templates/` — drawing sheet templates (ZKNOT title block, etc.)
- `design-rules/` — `.kicad_dru` files per fab (JLCPCB 2L/4L, etc.)
- `datasheets/` — component datasheet PDFs
- `fab-output/` — staging area for gerbers/drill/pos before ordering (not committed)
- `<product>/` — one directory per product family
- `tooling/` — internal fixtures (programming jigs, test boards)

## Products

- **zkkey-connect** — signing device, Pico Plus 2 + ATECC carrier
- **powerverify** — PUF authenticator (currently shipping)
- **zkkey-air** — optical-ingest signing device (camera + QR + OLED)

## Conventions

- Each product has its own top-level directory.
- Each revision lives in `revN-short-description/`.
- KiCad project files use short rev tags: `<product>-r<N>.kicad_pro`.
- Each rev directory contains a `README.md` with status:
  in-design / sent-to-fab / received / validated / shipped.
- Shared libraries referenced via `ZKNOT_SYMBOLS`, `ZKNOT_FOOTPRINTS`,
  `ZKNOT_3DMODELS` path variables (set in KiCad Preferences).
- Manufacturing files (gerbers, drill, pos) generated only when ordering;
  not committed to git (regen from sources).

## Title block

All projects use `kicad-templates/zknot-default/zknot-title.kicad_wks`.
Set in each project: File → Page Settings → Drawing sheet file.

