# TrustSeal — Product Specification
**ZKNOT, INC. | PAT-003 App# 63/961,112 | 2026-04-16**
UEI: C4SKW13JPEL5 | CAGE: 1AHZ4 | EIN: 36-5165991

---

## 1. What TrustSeal Is

TrustSeal is a tamper-evident physical seal with a cryptographically registered unique identifier. Every seal is individually serialized. When a seal is applied to an object, its serial number is scanned, hashed, and recorded as a signed event in the ZK-LocalChain ledger by a ZKKey device. The seal and the ledger record are permanently linked.

If the seal is broken, removed, or replaced, the original serial number no longer matches the recorded hash. Tampering is detectable by anyone with access to verifyknot.io.

**The patent claim in one sentence:** A physical tamper-evident seal whose identifier is cryptographically bound to a digital evidence record at the moment of application, such that any subsequent tampering with the seal or the record is independently detectable.

---

## 2. Physical Specification — Batch A001

| Property | Value |
|----------|-------|
| Dimensions | 50 × 25mm landscape |
| Substrate | White gloss polyester |
| Adhesive | Permanent acrylic, tamper-evident VOID pattern |
| Tamper mechanism | Destructive void — label tears on removal, VOID text appears in residue on surface |
| Print | Black on white, 300 DPI minimum |
| Finish | Matte laminate over print |
| QR error correction | Level H (30% — survives partial damage) |
| QR encodes | `https://verifyknot.io/seal/{serial}` |
| Serial format | `TS-[BATCH]-[SEQ]-[CHECK]` |
| Batch A001 range | TS-A001-00001-T through TS-A001-00100-R |
| Quantity | 100 seals |

---

## 3. Label Layout

```
┌────────────────────────────────────────────────────────────┐
│ ┌──────────┐  ZKNOT                                        │
│ │          │  TrustSeal                                    │
│ │  QR CODE │  ──────────────────                           │
│ │ 240x240  │  TS-A001                                      │
│ │          │  00001-T                                      │
│ │          │  Scan to verify                               │
│ └──────────┘  verifyknot.io                                │
│              PAT. PEND. — App# 63/961,112                  │
└────────────────────────────────────────────────────────────┘
         50mm wide × 25mm tall
```

Left zone: QR code, ~19×19mm active area, Level H error correction.
Right zone: ZKNOT wordmark, TrustSeal product name, serial in two lines, verify callout, URL.
Bottom: patent pending notice centered across full width.
Substrate: VOID pattern in adhesive layer — invisible until seal is broken.

---

## 4. Serial Number Scheme

### Format
```
TS-[BATCH]-[SEQ]-[CHECK]

TS        Product prefix — TrustSeal
BATCH     4-character alphanumeric batch identifier (A001, A002, ... Z999)
SEQ       5-digit zero-padded sequential number within batch (00001–99999)
CHECK     1 Luhn-style check character from charset: ABCDEFGHJKLMNPQRSTUVWXYZ23456789
          (no 0/O, no 1/I — eliminates visual ambiguity in handwritten logs)

Example:  TS-A001-00047-B
```

### Check Character Algorithm
```python
CHARSET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

def check_char(serial_body: str) -> str:
    val = sum(ord(c) * (i + 1) for i, c in enumerate(serial_body))
    return CHARSET[val % len(CHARSET)]

# serial_body = "TS-A001-00047"
# check = check_char("TS-A001-00047") → single character
# full serial = "TS-A001-00047-" + check
```

### Batch Registry
Each batch has a defined date range, supplier, substrate specification, and adhesive specification. Batch identity is recorded in the ledger event when a seal is applied, creating a complete audit trail from seal manufacture to evidence application.

| Batch | Seals | Date | Notes |
|-------|-------|------|-------|
| A001 | 00001–00100 | 2026-04-16 | Prototype run — validate form factor and ledger flow |
| A002 | 00001–01000 | TBD | First production run after A001 validation |

---

## 5. Seal Lifecycle

### State Machine
```
MANUFACTURED → UNREGISTERED → REGISTERED (applied) → VERIFIED | TAMPERED
```

**MANUFACTURED:** Seal exists physically. Serial exists in batch registry JSON. No ledger record yet.

**UNREGISTERED:** Seal is in the field but not yet applied. Scanning the QR returns "Seal not yet applied — valid seal, no record." This is intentional — it proves the seal exists and is genuine without revealing where it will be used.

**REGISTERED:** Seal has been applied to an object. ZKKey device scanned the QR, the ledger event was signed and recorded. `verifyknot.io/seal/{serial}` returns the full event record: timestamp, operator device ID, event hash, object description.

**VERIFIED:** Anyone scanning the QR after application sees the original record. Seal is physically intact. Cryptographic record matches.

**TAMPERED:** Seal has been physically broken, removed, or replaced. Either the physical VOID pattern is visible, or the serial does not match the registered record, or both.

### Application Workflow (what the operator does in the field)

1. Operator opens ZKNOT field app or verifyknot.io on phone.
2. Operator selects "Apply TrustSeal."
3. App generates a challenge incorporating the seal serial and current event context.
4. Operator scans the seal QR with phone — app reads serial, constructs event record.
5. App displays challenge QR on phone screen.
6. Operator holds ZKKey Connect or ZKKey Air to the screen.
7. ZKKey signs the event: `{seal_serial, object_description, operator_id, timestamp, location_hash}`.
8. App posts signed event to `api.zknot.io/v1/seal/register`.
9. Operator physically applies the seal to the object.
10. `verifyknot.io/seal/{serial}` now returns the signed event.

**The seal is applied AFTER the ledger record is created.** This order matters for the patent claim — the cryptographic commitment exists before the physical seal, making it impossible to retroactively create a record for a seal that was applied without registration.

---

## 6. API Specification

### Register a Seal Application
```
POST api.zknot.io/v1/seal/register

Request body:
{
  "seal_serial":         "TS-A001-00047-B",
  "object_description":  "SanDisk 64GB microSD card — case serial 47291",
  "operator_device_id":  "ZKC-A1B2C3D4",          // ZKKey device serial
  "event_hash":          "sha256:abc123...",        // hash of event data
  "signature":           "3045...",                 // ECDSA signature from ZKKey
  "short_code":          "A3F7-K2M9",              // human-readable attestation code
  "timestamp_utc":       "2026-04-16T14:32:11Z",
  "location_hash":       "sha256:def456...",        // optional: hash of GPS coordinates
  "session_id":          "ZK-6GUA-7DV"             // optional: ZK-LocalChain session
}

Response 201:
{
  "status":       "REGISTERED",
  "seal_serial":  "TS-A001-00047-B",
  "verify_url":   "https://verifyknot.io/seal/TS-A001-00047-B",
  "chain_id":     "ZK-8HJP-2MX",
  "registered_at": "2026-04-16T14:32:12Z"
}

Response 409: Seal already registered
Response 400: Invalid serial or check character mismatch
Response 422: Signature verification failed
```

### Verify a Seal
```
GET api.zknot.io/v1/seal/{serial}

Response 200 (registered):
{
  "seal_serial":         "TS-A001-00047-B",
  "status":              "REGISTERED",
  "object_description":  "SanDisk 64GB microSD card — case serial 47291",
  "operator_device_id":  "ZKC-A1B2C3D4",
  "event_hash":          "sha256:abc123...",
  "signature":           "3045...",
  "short_code":          "A3F7-K2M9",
  "timestamp_utc":       "2026-04-16T14:32:11Z",
  "verify_url":          "https://verifyknot.io/seal/TS-A001-00047-B",
  "chain_position":      4,
  "chain_id":            "ZK-8HJP-2MX"
}

Response 200 (unregistered):
{
  "seal_serial":  "TS-A001-00047-B",
  "status":       "UNREGISTERED",
  "message":      "Valid seal — not yet applied. If this seal appears to be in use, it has not been cryptographically registered.",
  "batch":        "A001",
  "manufactured": "2026-04-16"
}

Response 404: Serial not in any batch registry (potential counterfeit)
```

### Check Serial Validity
```
GET api.zknot.io/v1/seal/{serial}/validate

Response 200:
{
  "serial":   "TS-A001-00047-B",
  "valid":    true,
  "batch":    "A001",
  "check_ok": true
}

Response 200 (invalid check char):
{
  "serial":      "TS-A001-00047-X",
  "valid":       false,
  "check_ok":    false,
  "expected":    "B",
  "provided":    "X",
  "message":     "Check character mismatch — possible transcription error"
}
```

---

## 7. Database Schema (PostgreSQL, add to existing zknot.io schema)

```sql
-- Batch registry
CREATE TABLE trustseal_batches (
    id              SERIAL PRIMARY KEY,
    batch_id        VARCHAR(4) UNIQUE NOT NULL,      -- 'A001'
    manufactured    DATE NOT NULL,
    quantity        INTEGER NOT NULL,
    substrate_spec  TEXT,
    adhesive_spec   TEXT,
    supplier        TEXT,
    notes           TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Individual seal registry
CREATE TABLE trustseals (
    id              SERIAL PRIMARY KEY,
    serial          VARCHAR(20) UNIQUE NOT NULL,     -- 'TS-A001-00047-B'
    batch_id        VARCHAR(4) REFERENCES trustseal_batches(batch_id),
    seq             INTEGER NOT NULL,
    status          VARCHAR(20) DEFAULT 'UNREGISTERED'
                    CHECK (status IN ('UNREGISTERED','REGISTERED','FLAGGED')),
    object_desc     TEXT,
    operator_device VARCHAR(50),
    event_hash      VARCHAR(80),
    signature       TEXT,
    short_code      VARCHAR(20),
    session_id      VARCHAR(20),
    location_hash   VARCHAR(80),
    timestamp_utc   TIMESTAMPTZ,
    chain_id        VARCHAR(20),
    chain_position  INTEGER,
    verify_url      TEXT GENERATED ALWAYS AS
                    ('https://verifyknot.io/seal/' || serial) STORED,
    registered_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_trustseals_serial  ON trustseals(serial);
CREATE INDEX idx_trustseals_status  ON trustseals(status);
CREATE INDEX idx_trustseals_batch   ON trustseals(batch_id);
CREATE INDEX idx_trustseals_session ON trustseals(session_id);

-- Seed batch A001
INSERT INTO trustseal_batches
    (batch_id, manufactured, quantity, substrate_spec, adhesive_spec, notes)
VALUES
    ('A001', '2026-04-16', 100,
     'White gloss polyester 50x25mm 300DPI matte laminate',
     'Permanent acrylic tamper-evident VOID pattern',
     'Prototype run — validate form factor and ledger integration');
```

---

## 8. verifyknot.io Page — Seal Verification UI

When a user scans a TrustSeal QR, they land on `verifyknot.io/seal/{serial}`.

### Registered seal — what the user sees:
```
┌─────────────────────────────────────────────────────┐
│  ✓  SEAL VERIFIED                                   │
│     TrustSeal TS-A001-00047-B                       │
│                                                     │
│  Applied:    2026-04-16 14:32 UTC                   │
│  Object:     SanDisk 64GB microSD — serial 47291    │
│  Signed by:  Device ZKC-A1B2C3D4                    │
│  Short code: A3F7-K2M9                              │
│                                                     │
│  This seal was cryptographically registered         │
│  before application. The record cannot be           │
│  altered without detection.                         │
│                                                     │
│  [View full cryptographic record]                   │
│                                                     │
│  ZKNOT, INC. · verifyknot.io · PAT. PEND.          │
└─────────────────────────────────────────────────────┘
```

### Unregistered seal:
```
┌─────────────────────────────────────────────────────┐
│  ⚠  SEAL NOT YET APPLIED                           │
│     TrustSeal TS-A001-00047-B                       │
│                                                     │
│  This is a valid ZKNOT TrustSeal (Batch A001).      │
│  It has not yet been cryptographically registered.  │
│                                                     │
│  If this seal appears to be securing an object,    │
│  it was applied without registration.              │
│  The cryptographic chain of custody is broken.     │
└─────────────────────────────────────────────────────┘
```

### Unknown serial (potential counterfeit):
```
┌─────────────────────────────────────────────────────┐
│  ✗  SEAL NOT RECOGNIZED                             │
│     Serial: TS-A001-00047-X                         │
│                                                     │
│  This serial is not in the ZKNOT registry.         │
│  This seal may be counterfeit or damaged.          │
│                                                     │
│  Contact: ops@zknot.io                             │
└─────────────────────────────────────────────────────┘
```

---

## 9. Print Ordering Guide — Batch A001

### Supplier options (tamper-evident label printers)
These suppliers handle short-run tamper-evident label work without minimum quantity issues:

1. **Sticker Mule** — sticker-mule.com — handles custom label sizes, no tamper-evident substrate but good for proof of concept on form factor only. NOT suitable for production.

2. **Lightning Labels** — lightninglabels.com — handles tamper-evident VOID substrate, custom sizes, 100-unit minimums. **Recommended for A001.**

3. **StickerYou** — stickeryou.com — custom die-cut, tamper-evident options available. Good for A001 quantity.

4. **Local commercial print shop** — ask specifically for "tamper-evident security label stock with VOID adhesive, polyester substrate, matte laminate, 50×25mm, 300DPI." Most shops with a digital press can run 100 units.

### Print file requirements for supplier
- Format: PDF or high-res PNG, 300 DPI minimum
- Color mode: CMYK or Grayscale (our labels are black on white — safe either way)
- Bleed: 2mm on all sides (add to 50×25mm → 54×29mm with bleed)
- Safe zone: 3mm inside edge for all text
- Substrate spec: Tamper-evident VOID security label, white gloss polyester face, permanent acrylic adhesive with VOID pattern
- Finish: Matte laminate
- Cutting: Die-cut to 50×25mm

### What to send the printer
- Individual label PNGs from `/home/claude/TrustSeal/labels/`
- OR the sheet files from `/home/claude/TrustSeal/sheets/` (8-up A4 proof sheets)
- Serial registry JSON for your records

### Expected cost
100 tamper-evident labels at 50×25mm: approximately $45–80 USD depending on supplier.

---

## 10. Field Use Protocol — First 100 Seals

### Gates these seals support
- **Gate 2 (Sep 6):** Demo video showing ZKKey Connect or Air signing a TrustSeal application event. This is the complete evidence workflow: device powered through PowerVerify, data sealed with TrustSeal, event signed by ZKKey.
- **Gate 8 (Sep 18):** Data room includes at least one real-world TrustSeal deployment as proof of concept.

### Recommended first uses for A001 seals
1. Seal the PowerVerify boards during the Gate 2 demo — document the device, apply seal, sign with ZKKey. This creates a CombinedSession record (PAT-007) tying power delivery, physical seal, and human presence into one attestation.
2. Seal your own development hardware — establishes real chain of custody records in the ledger.
3. Seed 10 seals to a journalist or researcher contact for feedback on field usability.

### Do not use A001 seals for
- Paying customers (prototype run — substrate vendor not yet validated)
- Legal proceedings (wait for A002 production run with documented supplier spec)
- Any context where seal failure would matter

---

## 11. Revenue Model

TrustSeal is the recurring revenue SKU in the ZKNOT stack. Hardware is one-time; seals are consumable.

| SKU | Quantity | Unit cost est. | Sale price | Margin |
|-----|----------|---------------|------------|--------|
| TS-010 | 10-pack | $0.80 | $14.99 | 94% |
| TS-050 | 50-pack | $0.65 | $59.99 | 95% |
| TS-500 | 500-pack | $0.45 | $449 | 95% |
| TS-ENT | Custom branded, NFC | TBD | Contract | — |

**Acquirer story:** A customer who buys one ZKKey device buys seals forever. The seal SKU converts a hardware sale into a subscription-equivalent revenue stream. This matters for acquisition multiple.

---

## 12. File Naming (ZKNOT Convention)

```
TrustSeal/
  generate_labels.py                              ← label generator script
  labels/
    TS-A001-00001-T.png                           ← individual seal artwork (100 files)
    ...
    TS-A001-00100-R.png
  sheets/
    sheet_01.png through sheet_13.png             ← 8-up proof sheets for printer
  ZKNOT_TS-A001_serial_registry_20260416.json    ← master serial registry
  ZKNOT_DOC-004_TrustSeal_product_spec_20260416.md  ← this document
```

Renamed per ZKNOT convention for master archive:
```
ZKNOT_PCB-004_TrustSeal_A001_label_artwork_20260416.zip
ZKNOT_DOC-004_TrustSeal_product_spec_20260416.md
ZKNOT_TS-A001_serial_registry_20260416.json
```

---

*ZKNOT, INC. — When physics is policy, trust is optional.*
*Patent Pending — App# 63/961,112*
*ops@zknot.io | verifyknot.io | UEI: C4SKW13JPEL5*
