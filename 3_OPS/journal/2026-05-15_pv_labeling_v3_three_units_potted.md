# 2026-05-15 — PV Labeling v3 Locked, Three Units Labeled and Potted

**Status:** Three PV demo units (PV1-00042, PV1-00043, PV1-00044) labeled per DECISIONS_pv_labeling.md v3, going into pot.
**Workstream:** mfg / sig / hw
**Outcome:** Production-ready labeling spec locked. Three demo/tester units progressing toward first PUF photography.

## What happened today

Completed multi-thread iteration on PV labeling. Went from concept to printed labels on real PCBs in a single session:

1. Patent portfolio review (16 provisionals filed, 1 trademark pending) clarified what citations belong on labels. Production PV is PAT-002 only (App# 63/961,118); PAT-018 (PowerVerifyPlus) is filed but not yet built.
2. Microscope + ffmpeg + capture_puf.sh working — first capture saved to ~/ZKNOT/6_SIG/puf_images/.
3. P-touch PT-E560BT + qrencode + ptouch-print toolchain validated. Successfully printed and applied 3 labels.
4. QL-820NWB recognized as the right printer for outer (business card) and tamper seal labels — different role from P-touch (internal/PCB labels).
5. Labeling decision record evolved through v1 → v2 → v3.

## Engineering decisions locked

- **Serial format:** PV1-NNNNN (was PV-YYYY-NNNNN). Three-letter prefix opens SKU expansion (PV2, PVA, PVF, PVP). Removes year from label; year stays in registry. 9 chars total.
- **Patent citation on labels:** PAT-002 only (63/961,118). PAT-018 waits until that hardware exists.
- **Label architecture:** internal text-only (potted) + external scannable (in ESD bag) + tamper seal (across bag opening). Decouples pot clarity from QR scannability.
- **Pot clarity goal:** text-legible (not QR-scannable). Easier engineering target, doesn't require vacuum-degassed optical-grade epoxy.
- **PCB internal label:** 3 lines on 24mm white TZe-251: serial / short_code / verifyknot.io. No QR. Visible through clear pot.
- **PUF image workflow:** capture via capture_puf.sh → upload to api.zknot.io → display on verifyknot.io alongside attestation. Enables optical verification as a companion to cryptographic.

## Today's bench output

- 3 P-touch labels printed and applied to 3 PV PCBs (PV1-00042, PV1-00043, PV1-00044)
- All three share short_code ZK-6GUA-7DV (demo units, all point to first chain record)
- All three soldered and wired; CC lines required hand-applied blue jumper wires (PCB layout omission)
- D+/D- through-holes intentionally unpopulated (design decision — confirms "data lines physically absent")
- Three units now going into pot, ~48 hour cure target

## Next-rev (PV Rev 2) decisions captured for future work

- Lettering 20% larger on internal label (more legible through resin)
- CC lines routed in PCB (no hand-applied jumper wires)
- These are tracked in Taskwarrior under the rev-2 design work

## What's NOT happening

- No PAT-018 citation on current labels
- No TrustSeal branding on PV tamper seals (TrustSeal is its own product, PAT-003)
- No QR through-pot scanning (deferred via internal/external split)
- No tamper-evident destructible vinyl stock yet (deferred until real shipping)
- No shipping label (deferred until shipping volume)

## What IS happening next

- 48-hour pot cure on the three units
- PUF photography on each unit after cure (capture_puf.sh PV1-00042 etc.)
- Wednesday: MCP2221A arrives → ATECC provisioning work begins on virgin Pico breadboards
- Eventually: business card label script (Python + brother_ql), tamper seal label script

## Documents

- DECISIONS_pv_labeling.md v3 at ~/ZKNOT/3_OPS/km/
- This journal entry
- capture_puf.sh at ~/capture_puf.sh (working; tested with PV-2026-00042 sample capture)

## Honest notes

- Solo founder bandwidth real — labeling + microscope + provisioning + business strategy in one thread was a lot. Handoff doc + decision record + journal entries are how we keep the next thread productive without dragging history along.
- The v3 split (internal vs external label) emerged from a real engineering constraint (pot clarity), not from over-design. Good test of "let the problem shape the architecture."
- PAT-002 vs PAT-018 distinction would have been a real error if shipped without correction — labeling units with a patent that doesn't apply yet. Catching it via the patent tracker reading was a save.
