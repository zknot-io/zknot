# 2026-05-21 — Small PCB QR labels + pot-survivability test setup

**Author:** William Shane Wilkinson
**Workstream:** hw / ops
**Units:** PV1-00052, PV1-00053, PV1-00054 (ZK codes below)

---

## Summary

Provisioned and signed three new PowerVerify units (52/53/54), then designed and
printed a smaller on-PCB QR label format to replace the larger full-width labels.
The new PROD label fits on the PCB and is the production format going forward. Also
generated a density-test matrix to find how small a QR can go and still scan through
cured pot. Triggered by PV-2026-00042 coming out of pot with the embedded QR clearly
scannable — the clearer-than-expected pot makes QR-under-resin viable, reversing the
v3 "no QR under pot" decision.

---

## Units minted this session

| Serial | ZK code | Chain pos | Verify URL |
|---|---|---|---|
| PV1-00052 | YVTX-RCH2-0JJG | 25 | verifyknot.io/v/YVTX-RCH2-0JJG |
| PV1-00053 | 4JX4-NB4V-57X9 | 23 | verifyknot.io/v/4JX4-NB4V-57X9 |
| PV1-00054 | D38K-Q430-4A57 | 24 | verifyknot.io/v/D38K-Q430-4A57 |

Signed via `zksign` (pre-pot, PUF deferred, Mfg events: 5), pushed via `zksync`.
All three confirmed `verified` at api.zknot.io. Chain now at 25 entries.

Note: the API `POST /v1/units/provision` endpoint FAILED ("public key is not valid
hex") — the v0.3.0 strict ECDSA validation rejects the placeholder pubkey that
provision generates pre-signing. Used the proven `zksign` path instead (consistent
with all prior units 43-51). Provision-endpoint bug logged for a future fix.

---

## Label format (NEW production spec)

**PROD label** — fits on the PCB, replaces the larger full-width label.
- Tape: QL-820NWB 62mm continuous
- Content zone: left 50mm wide x 20mm tall (right 12mm of tape blank, trimmed off)
- Canvas: 696px x 295px = 62mm x 25mm at 300 DPI; ~2.5mm trim margin top/bottom
- Layout: 18mm QR (full URL, EC level H) on left; stacked text right —
  serial / ZK code / "R1 PAT 63/961,118" / verifyknot.io
- Matches the proven PV-2026-00042 layout, scaled down

**Status:** PROD labels are PERFECT for on-PCB use — production-ready.
Test-matrix labels print fine but need minor touch-ups (layout polish).

---

## Pot-survivability test matrix

Purpose shifted from "does QR survive pot" (already proven by 00042) to
"how small can the QR go and still scan through resin."

| Variant | Encoding | QR size | QR version | Notes |
|---|---|---|---|---|
| F15 | full URL (https://verifyknot.io/v/CODE) | 15mm | v5 (37x37) | densest; smallest full-URL test |
| F18 | full URL | 18mm | v5 (37x37) | full-URL at max practical size |
| B15 | bare code (CODE only) | 15mm | v2 (25x25) | coarse modules, small |
| B18 | bare code | 18mm | v2 (25x25) | coarsest, most pot-tolerant |

Each test QR carries an identifying tag (e.g. "52 B18 v2 (18mm)") so variants are
distinguishable after potting. Bare-code variants scan to plain text, NOT a tappable
link, unless verifyknot.io is configured to resolve a bare code without the /v/ path
— confirm before adopting a B-variant for production.

### Results (fill in after cure)

| Variant | Scans pre-pot? | Scans post-cure? | Confidence/notes |
|---|---|---|---|
| F15 |  |  |  |
| F18 |  |  |  |
| B15 |  |  |  |
| B18 |  |  |  |

**Decision rule:** the densest variant that still scans post-cure is the production
spec. If F15 survives -> full-URL UX at smallest size (best outcome). If only B
variants survive -> full URL needs >=18mm, or adopt bare-code + bare-code resolution.

---

## Printer toolchain notes (for future sessions)

The QL-820NWB print path that actually works on this machine (Debian Trixie):

1. **Connection:** USB, vendor:product `04f9:209d`, pyusb backend.
   No `/dev/usb/lpN` device present (usblp didn't bind; printer enumerates raw).
2. **Resource-busy fix:** `ipp-usb` daemon grabs the printer's USB interface.
   Must `sudo systemctl stop ipp-usb` (optionally `mask` it) before printing.
   This was the cause of "[Errno 16] Resource busy". NOT cups, NOT usblp.
3. **Permissions:** udev rule added —
   `/etc/udev/rules.d/99-brother-ql.rules`: `SUBSYSTEM=="usb",
   ATTR{idVendor}=="04f9", ATTR{idProduct}=="209d", MODE="0666"`. Applies on replug.
4. **ANTIALIAS bug:** `brother_ql 0.9.4` calls `Image.ANTIALIAS`, removed in
   Pillow 10+. Crashes whenever brother_ql resizes an image (i.e. when image width
   != 696px printable width). Two fixes:
   - Build label images at exactly 696px wide (no resize triggered), OR
   - Use the `~/bin/qlprint` wrapper that shims `Image.ANTIALIAS = Image.LANCZOS`
     before importing brother_ql. The wrapper works for any image size.
5. **Working print command:**
   `qlprint -b pyusb -m QL-820NWB -p usb://04f9:209d print -l 62 --rotate auto FILE.png`

### qlprint wrapper (~/bin/qlprint)
```python
#!/usr/bin/env python3
import PIL.Image
if not hasattr(PIL.Image, "ANTIALIAS"):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from brother_ql.cli import cli
cli()
```

---

## Open touch-ups (not blocking)

- Test-matrix label layout needs minor polish (tag placement / spacing)
- Confirm whether verifyknot.io resolves bare codes (no /v/) — gates B-variant use
- Fill in pot-survivability results after these three cure
- Fix the `/v1/units/provision` endpoint (placeholder-pubkey rejection under v0.3.0)

---

## Files

Label PNGs (this session): `~/Downloads/PROD_PV1-000{52,53,54}.png`,
`~/Downloads/TEST_{F15,F18,B15,B18}_PV1-000{52,53,54}.png`
Generator: regenerated in-session (see chat); 696px-wide canvas, 50mm content zone.

---

*ZKNOT, Inc. — when physics is policy, trust is optional.*
