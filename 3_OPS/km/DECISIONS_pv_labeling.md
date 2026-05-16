# PowerVerify Labeling — Decision Record (v3)

**Document ID:** ZKNOT_DOC-MFG-001
**Version:** 3.0
**Date:** 2026-05-15
**Status:** Production-ready
**Author:** Shane Wilkinson (William Shane Wilkinson)
**Target location:** `~/ZKNOT/3_OPS/km/DECISIONS_pv_labeling.md`

---

## Changes from v2

- **Patent citation reduced to PAT-002 only.** Current production PowerVerify is the basic PAT-002 power-only interface (App# 63/961,118). PAT-018 (PowerVerifyPlus, the cryptographically-signed-session version with multi-layer tamper evidence and sealed secondary interface) is filed as IP but not yet built. Months out. Don't cite a patent we haven't shipped.
- **Architecture split:** internal label (potted) is now text-only; external label (outer package) carries the QR. This decouples pot clarity from QR scannability.
- **Pot clarity goal changed** from "QR-scannable" to "text-legible." Much easier engineering target; doesn't require vacuum-degassed optical-grade epoxy.
- **Three labels total:** internal text label (P-touch, potted), outer scannable label (QL-820NWB, on ESD bag or business card), tamper seal (QL-820NWB, seals ESD bag).
- **PUF image workflow** added: capture PUF photo → upload to api.zknot.io → display at verifyknot.io alongside attestation → customer can visually verify PUF.

---

## 1. Purpose

Locks down labeling for ZKNOT PowerVerify Rev 1 (PAT-002 product) units. Source of truth for production. Paste-able into a fresh AI chat as ground truth.

---

## 2. IP context

**Current production PowerVerify covers:**
- **PAT-002 / App# 63/961,118** — "Power-Delivery Interface With Physical Data-Path Elimination and Verified Power-Only Operation" (filed 2026-01-15)

**Future / aspirational (not yet built):**
- PAT-018 / App# 64/007,940 — PowerVerifyPlus (the enhanced version) — months away
- PAT-003 — TrustSeal (the patented tamper seal product the seal label references)
- PAT-004 — ZK-LocalChain

**Trademark:** ZKNOT™ (USPTO Serial #99597138, Class 009, pending). Use ™ symbol until registration; ® after.

The labels below cite **only PAT-002** because that's the patent the production hardware actually implements. PAT-018 labels and marketing wait until PAT-018 hardware exists.

---

## 3. Three labels per PV unit

| # | Label | Printer | Stock | Purpose | Gets potted? |
|---|-------|---------|-------|---------|--------------|
| 1 | PCB internal | P-touch Edge PT-E560BT | 24mm TZe-251 white (replace SL self-laminating) | Permanent in-unit identity, readable through pot | Yes |
| 2 | Outer scannable | QL-820NWB | 62mm continuous | Customer-facing scan target, full info | No |
| 3 | Tamper seal | QL-820NWB | 62mm continuous | Seals ESD bag closed | No |

Shipping label is deferred until shipping volume exists.

---

## 4. Canonical data fields per unit

| Field | Example | Source |
|-------|---------|--------|
| `serial` | `PV-2026-00042` | Assigned sequentially at provisioning |
| `short_code` | `ZK-6GUA-7DV` | Returned by `POST /v1/attest` |
| `mfg_date` | `2026-05-15` | ISO 8601 UTC |
| `rev` | `R1` | Hardware revision |
| `chain_position` | `0` | Returned as `chain_index` from api.zknot.io |
| `verify_url` | `https://verifyknot.io/ZK-6GUA-7DV` | Built from short_code |
| `puf_image` | `~/ZKNOT/6_SIG/puf_images/PV_PV-2026-00042_*.jpg` | Captured via `capture_puf.sh` |

---

## 5. Label 1 — PCB Internal (text-only, gets potted)

**Goal:** Survive potting. Be readable through imperfect resin. No QR.

### Final content

Two lines, large bold text:

```
+--------------------------------+
|                                |
|        PV-2026-00042           |
|        ZK-6GUA-7DV             |
|                                |
+--------------------------------+
```

### Rationale

- **No QR** — scanning through resin is unreliable even with optical-grade epoxy. Don't fight that battle.
- **Two lines, not four** — bigger text per line, more legible through cloudy pot. Human serial on top (what the customer sees on packaging), verification short_code below (what they type into verifyknot.io if they need to lookup manually).
- **No date, no rev, no chain position** — these are on the outer label and in the registry. Internal label is the permanent identity anchor, nothing more.

### Print command

```bash
ptouch-print --text "PV-2026-00042" \
  --newline "ZK-6GUA-7DV" \
  --cutmark
```

(Substitute actual serial and short_code per unit.)

---

## 6. Label 2 — Outer Scannable (QR + full info, NOT potted)

**Goal:** Customer-facing identity card. Lives in the ESD bag with the unit. This is what the customer scans on day-one and references thereafter.

### Final layout (62mm wide × ~90mm tall, business-card form factor)

```
+--------------------------------------------------+
|                                                  |
|                 POWERVERIFY (TM)                 |
|         ZKNOT, INC. · Salt Lake City, UT         |
|         ─────────────────────────────────        |
|                                                  |
|              Unit Serial: PV-2026-00042          |
|              Verification: ZK-6GUA-7DV           |
|              Hardware Rev: R1                    |
|              Manufactured: 2026-05-15            |
|              Chain Position: 0                   |
|                                                  |
|         ─────────────────────────────────        |
|                                                  |
|               +----------------+                 |
|               |                |                 |
|               |   QR  CODE     |                 |
|               |   (large)      |                 |
|               |                |                 |
|               +----------------+                 |
|                                                  |
|         Verify at  verifyknot.io/ZK-6GUA-7DV     |
|                                                  |
|         ─────────────────────────────────        |
|                                                  |
|         Scan to verify authenticity. This        |
|         device's USB power port carries no       |
|         data signal — data lines physically      |
|         absent. If verification fails, do not    |
|         trust the device. Tamper seal must be    |
|         intact.                                  |
|                                                  |
|         ─────────────────────────────────        |
|                                                  |
|         Patent Pending: US App# 63/961,118       |
|                                                  |
|         ZKNOT(TM) is a trademark of              |
|         ZKNOT, INC.  USPTO 99597138              |
|                                                  |
|         Made in USA · Salt Lake City, UT         |
|         UEI: C4SKW13JPEL5 · CAGE: 1AHZ4          |
|         Veteran-Owned · SDVOSB                   |
|                                                  |
|         support@zknot.io                         |
|                                                  |
+--------------------------------------------------+
```

### Rationale

- **Citing only 63/961,118** — this product implements PAT-002 only. Adding PAT-018 (which is filed but not built) on a label would be a misrepresentation. When PAT-018 hardware exists, that's a new label revision.
- **"Data lines physically absent"** — matches the PCB silkscreen language exactly (`DATA LINES PHYSICALLY ABSENT`, `NO USB ENUMERATION`). Consistent vocabulary between silkscreen and label.
- **Large QR encodes** `https://verifyknot.io/ZK-6GUA-7DV` directly — direct short_code resolution, no `/v/` path.
- **Federal credentials** for procurement-side buyers (UEI, CAGE, SDVOSB).

### Implementation path

Render as PIL image at QL-820NWB native DPI (300 DPI), 62mm × ~85mm. Use `brother_ql` to send. Script lives at `~/ZKNOT/3_OPS/scripts/print_pv_outer_label.py` (to be created).

---

## 7. Label 3 — Tamper Seal (QL-820NWB, seals the ESD bag)

**Goal:** Seal the ESD bag closed. Any tampering produces visible damage.

### Final layout (62mm wide × ~40mm tall)

```
+--------------------------------------------------+
|                                                  |
|         WARNING — TAMPER EVIDENT SEAL            |
|                                                  |
|         If this seal shows ANY damage —          |
|         cuts, tears, lifting, residue, or        |
|         misalignment — DO NOT TRUST this         |
|         device. Contact support@zknot.io         |
|         before powering on.                      |
|                                                  |
|             PV-2026-00042 · ZK-6GUA-7DV          |
|             Sealed: 2026-05-15                   |
|                                                  |
|             ZKNOT(TM) · PAT PEND                 |
|                                                  |
+--------------------------------------------------+
```

### Rationale

- Drops the "TRUSTSEAL" branding from the v2 doc — TrustSeal (PAT-003) is a separately patented product. Using its name on the PV tamper seal would conflate two distinct ZKNOT products. The PV tamper seal is just a tamper seal, not the TrustSeal product.
- Five concrete tamper indicators called out (cuts, tears, lifting, residue, misalignment) — the customer knows what to check.
- Action: "DO NOT TRUST" + support email.
- Unit identifiers + seal date — chains the seal to a specific unit on a specific day.

### Tamper-evident stock

Standard DK continuous labels peel cleanly — not actually tamper-evident. For demo / early production this is acceptable because peel-and-replace would leave residue. For real production, source destructible vinyl or VOID-pattern stock. Deferred.

---

## 8. Production workflow per PV unit

```
1.  Solder PCB
2.  Provision ATECC via cryptoauthlib + MCP2221A   [pending Wednesday]
3.  Generate keypair, lock slot 0
4.  Record (silicon_serial, public_key, timestamp) → registry
5.  POST attestation to api.zknot.io/v1/attest
6.  Receive { short_code, chain_index } from API
7.  Photograph PUF substrate (capture_puf.sh)
8.  Upload PUF image to api.zknot.io → attestation record
9.  Print Label 1 (PCB internal text label)
10. Apply Label 1 to PCB
11. Pot the PCB
12. Wait 48 hours for cure
13. Photograph cured PUF (optional second image)
14. Print Label 2 (outer scannable)
15. Place unit + Label 2 in ESD bag
16. Print Label 3 (tamper seal)
17. Seal ESD bag with Label 3
18. (Eventually) shipping label and dispatch
```

---

## 9. Things explicitly NOT happening yet

- **PAT-018 citation** — wait until PowerVerifyPlus hardware exists
- **TrustSeal branding on tamper seal** — wait until TrustSeal is a separate shipping product
- **Real tamper-evident stock** — defer; current QL stock + visual inspection is acceptable for demo
- **Shipping label** — defer until shipping volume
- **Manufacturer attestation signature on artifact** — Phase 5+ feature
- **Public registry on api.zknot.io** — current path is self-hosted CSV, evolving later

---

## 10. Open items

| # | Item | Status |
|---|------|--------|
| 1 | Print Label 1 for at least one PV unit, pot it, verify text legibility through cured resin | Today's bench work |
| 2 | Write `print_pv_outer_label.py` (Label 2) | Next |
| 3 | Write `print_pv_tamper_seal.py` (Label 3) | Next |
| 4 | Confirm pot clarity is sufficient for text reading at 48hr cure | 2026-05-17 |
| 5 | Upload PUF images to api.zknot.io and display at verifyknot.io | Platform work |
| 6 | Source destructible vinyl tamper-evident stock | Deferred until production |
| 7 | Verify TZe-251 white tape is loaded (replaces TZe-SL self-laminating) | Done per latest bench update |

---

## 11. Revision history

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-15 | Initial draft |
| 2.0 | 2026-05-15 | Read patent portfolio + platform SOP; corrected verifyknot.io URL pattern, added patent citations, added trademark notation |
| 3.0 | 2026-05-15 | Reduced patent citation to PAT-002 only (current production); split internal/external labels; pot clarity goal changed to text-legible; PUF image workflow integrated |

---

## 12. Context for fresh AI sessions

**Tooling state (Debian Trixie, user `mt`):**
- `/usr/bin/ptouch-print` working
- `~/.local/bin/brother_ql` CLI installed
- `ffmpeg`, `v4l-utils`, `qrencode` all installed
- Andonstar microscope at `/dev/video0`, captures via `capture_puf.sh`
- User in `lp` group

**Printers:**
- Brother P-touch PT-E560BT on `/dev/usb/lp2`, **24mm TZe-251 white tape** (just replaced from TZe-SL self-laminating)
- Brother QL-820NWB on `/dev/usb/lp3`, **62mm continuous**

**Platform (per ZKNOT_SOP-001):**
- zknot.io, api.zknot.io, verifyknot.io all LIVE
- ZK-LocalChain: 5 production records, first record `ZK-6GUA-7DV` at position 0
- verifyknot.io resolves `/{short_code}` directly

**Current production product: PAT-002 PowerVerify** (dumb power-only board, 4 functional pins, D+/D− present-but-not-connected). PAT-018 PowerVerifyPlus is filed IP but not yet built — months away.

**This document supersedes v1 and v2. If a future session contradicts what's here, this doc wins unless explicitly revised.**
