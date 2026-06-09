# TrustSeal — Production & Fulfillment Runbook (A002, sellable run)

**ZKNOT, INC. | PAT-003 App# 63/961,112 | Owner: William Shane Wilkinson**
**Status: DRAFT — gated on verify-route confirmation (§0). Supersedes nothing; extends DOC-004 spec.**
**Target vault path: `~/ZKNOT/3_OPS/km/systems/trustseal-production-and-fulfillment.md`**

---

## TL;DR

- The 100 **A001** seals are **prototype / internal only** (DOC-004 §10 — not for paying customers). The sellable product is the **A002** run on validated tamper-evident stock.
- Tamper-evidence comes from the **substrate**, not the print. Buy VOID polyester (or destructible vinyl) + **resin** ribbon. Thermal transfer or laser only — never direct thermal for sold seals.
- **Brother QL** = dev-loop printer only (direct thermal, fades). **Zebra ZT or ZD621-TT-300dpi** = production. Both run your existing ZPL.
- A **working ZKKey gates field registration, not manufacture or sale.** You can print and sell now; the verifiable-record value switches on when you/the customer have a ZKKey.
- Fulfillment model: **pre-print rolls, assign serials at packing.** "Sold" and "registered" are orthogonal states.
- **HARD GATE (§0):** confirm `verifyknot.io/seal/{serial}` actually resolves before printing onto stock. A printed QR is permanent.

## Decisions (locked this session)

1. Production printer: **Zebra ZT (industrial)** — current gen is ZT231/ZT411; confirm model at purchase. (Desktop ZD621-TT-300dpi was the right-sized alternative and runs identical ZPL — noted in case of reconsideration.)
2. Fulfillment: **pre-print + assign-at-packing**, POD reserved for TS-ENT.
3. Sellable batch = **A002** (validated substrate). A001 stays internal.

---

## 0. HARD GATE — confirm the QR target route is live (do before buying stock)

Every TrustSeal artifact encodes `https://verifyknot.io/seal/{serial}`. The deployed verifyknot front-end may use a different path (the PowerVerify-style `/v/{code}` was the form confirmed live). A QR that 404s is permanent waste. Confirm on your box:

```bash
# 1. Does the deployed front-end resolve the seal path?
curl -sI https://verifyknot.io/seal/TS-A001-00001-T | head -1
curl -sI https://verifyknot.io/v/TS-A001-00001-T    | head -1
curl -sI https://verifyknot.io/                      | head -1

# 2. What does the API expose for seals?
curl -s -o /dev/null -w "%{http_code}\n" https://api.zknot.io/v1/seal/TS-A001-00001-T
grep -rn "seal" ~/zknot-api/ --include="*.py" | grep -iE "route|@app|@router|def .*seal"

# 3. Can the static site even resolve a dynamic /seal/{serial} lookup?
grep -rn "seal\|/v/" ~/verifyknot-site/ --include="*.html" --include="*.js"
ls ~/verifyknot-site/functions ~/verifyknot-site/_redirects 2>/dev/null
```

**Static-Pages caveat:** if `verifyknot-site` is static Cloudflare Pages, `/seal/{serial}` cannot do a per-serial lookup without either a `_redirects` SPA fallback (serve one page that fetches `api.zknot.io` client-side) or a Pages Function / Worker. If both `functions/` and `_redirects` come back empty, the route does not exist yet — build it before you print.

**If the live path differs**, it is a one-line change in all three places before generating A002 artwork:

```bash
# generate_labels.py, trustseal_print.py, and the registry generator
grep -rn "verifyknot.io/seal/" .   # find every occurrence first
# then change BASE_URL, e.g. "https://verifyknot.io/seal/" → "https://verifyknot.io/v/"
```

Do **not** change it blindly — confirm which route the deployed front-end serves, then match it.

---

## 1. Bill of materials (A002)

| Item | Spec | Notes |
|------|------|-------|
| Printer | Zebra ZT231/ZT411 (or ZD621-TT-300dpi) | Must be **thermal-transfer** capable; 300 dpi (12 dpmm) to match your ZPL |
| Ribbon | **Resin** (not wax, not wax/resin) | Resin bonds to synthetic/polyester face + survives heat, UV, solvents, abrasion |
| Face stock | White gloss **polyester**, tamper-evident | See substrate choice below |
| Size | 50 × 25 mm (2" × 1"), 1" core roll | Matches DOC-004 §2 |
| Laminate | Matte (optional over-laminate or pre-laminated stock) | Protects QR readability long-term |

**Substrate choice — both families work for chain-of-custody:**

- **VOID polyester** (spec default): removal leaves "VOID" in the residue and on the surface. Clean readable tamper message, QR stays intact, evidence of any lift. Best all-rounder.
- **Destructible / frangible vinyl (eggshell):** shatters on removal — physically cannot be lifted and re-applied to another object. Stronger transfer-resistance, but fragments are messy and can damage the QR. Choose when "can't be relocated" matters more than "shows a message."

**Premium / TS-ENT idea (later):** QR + **NFC** where the antenna is severed by removal — the chip itself becomes a tamper element and enables tap-to-verify.

**Substrate validation is the whole point of A002.** Order a small validation lot first, run the field/abuse tests (peel, heat, solvent, UV, scan-after-damage), and record the validated supplier + stock part number in the batch registry before committing to a 1000-unit run.

---

## 2. Print pipeline

Your `trustseal_print.py` already emits ZPL for ZT-series and supports `--serial`, `--batch --from --to`, `--preview`, `--zpl-out`, network (port 9100), USB (`/dev/usb/lp0`), and serial. The Brother-specific `ipp-usb`/`qlprint` dance does **not** apply to the Zebra — that was a QL workaround.

```bash
# Preview without a printer (sanity-check layout)
python3 trustseal_print.py --serial TS-A002-00001-? --preview

# Calibrate media + ribbon on the Zebra once (run the printer's auto-calibration),
# then a single live test print before committing a roll:
python3 trustseal_print.py --serial TS-A002-00001-? --zpl-out /tmp/test.zpl
# USB:
cat /tmp/test.zpl > /dev/usb/lp0
# or network:
nc <printer-ip> 9100 < /tmp/test.zpl
```

Tuning notes for resin on polyester: set **darkness** higher than paper defaults and **print speed** lower (resin needs more dwell to bond). Verify the QR scans *after* a deliberate abrasion + isopropyl wipe — that is the real acceptance test for an evidence seal.

> Replace the `?` with the real check character — generate it from the spec's `check_char()` so SEQ and CHECK always agree.

---

## 3. Seal lifecycle (extended for sale)

DOC-004 §5 covers the crypto lifecycle. Selling adds an **allocation** dimension that is *orthogonal* to it:

```
                      crypto status (DOC-004)
  MANUFACTURED → UNREGISTERED ───────────────→ REGISTERED → VERIFIED | TAMPERED
                      │
   allocation ────────┼──────────────────────────────────
        UNALLOCATED → ALLOCATED (sold to order) → SHIPPED
```

A shipped seal is normally **ALLOCATED + UNREGISTERED** — sold, in the customer's hands, not yet applied. It becomes REGISTERED only when a ZKKey signs the application event in the field. So do **not** fold "sold" into the crypto status enum.

---

## 4. Fulfillment & allocation (pre-print + assign-at-packing)

**Operating model:** batch-print rolls of A002 ahead of time (UNREGISTERED, UNALLOCATED). When an order ships, assign the next *N* unallocated serials to that order, mark them ALLOCATED, and record the order↔range mapping.

**Schema add-on** (orthogonal allocation; keeps the crypto status enum clean):

```sql
-- allocation is separate from crypto status
ALTER TABLE trustseals ADD COLUMN allocated_order TEXT;   -- nullable: NULL = unallocated
CREATE INDEX idx_trustseals_alloc ON trustseals(allocated_order);

CREATE TABLE trustseal_allocations (
    id            SERIAL PRIMARY KEY,
    order_ref     TEXT NOT NULL,                 -- Shopify order name/id
    customer_ref  TEXT,                          -- Shopify customer id or email hash
    sku           TEXT,                          -- TS-010 / TS-050 / TS-500
    batch_id      VARCHAR(4) NOT NULL REFERENCES trustseal_batches(batch_id),
    seq_from      INTEGER NOT NULL,
    seq_to        INTEGER NOT NULL,
    qty           INTEGER GENERATED ALWAYS AS (seq_to - seq_from + 1) STORED,
    allocated_at  TIMESTAMPTZ DEFAULT NOW(),
    shipped_at    TIMESTAMPTZ
);
```

**Allocate-at-packing (transactional — assign the next N unallocated, oldest first):**

```sql
-- inside a transaction; :n = qty, :order, :cust, :sku, :batch
WITH picked AS (
  SELECT seq FROM trustseals
  WHERE batch_id = :batch AND allocated_order IS NULL
  ORDER BY seq
  LIMIT :n
  FOR UPDATE SKIP LOCKED
)
UPDATE trustseals t SET allocated_order = :order
FROM picked WHERE t.batch_id = :batch AND t.seq = picked.seq;

INSERT INTO trustseal_allocations (order_ref, customer_ref, sku, batch_id, seq_from, seq_to)
SELECT :order, :cust, :sku, :batch, MIN(seq), MAX(seq)
FROM trustseals WHERE allocated_order = :order;
```

This gives you a clean order→serial-range manifest to drop in the package and to answer "which seals did customer X receive?" later.

---

## 5. Shopify integration

- **At point of sale, seals are fungible SKUs** — TS-010 / TS-050 / TS-500 map to pack sizes. Shopify never needs to know individual serials.
- **Serials are assigned at fulfillment**, not at checkout (the allocation step above). Shopify webhook (`orders/fulfilled`) → call the allocation routine → print a packing manifest with the range.
- **Two tiers of value, by design (razor + blades):**
  - Buyer *with* a ZKKey: full cryptographic chain-of-custody (REGISTERED).
  - Buyer *without*: a working tamper-evident label whose QR shows "valid seal — not yet registered." Decide deliberately whether you sell the cheap tiers to non-ZKKey buyers or gate seals behind device ownership. Selling ungated grows the install base and pulls device sales; gating protects the "seals mean cryptographic proof" brand promise. Reasonable either way — pick on purpose.
- **Unregistered verify page copy matters** for a fresh buyer who scans before applying: it should read as reassuring proof of authenticity ("valid ZKNOT seal, not yet applied"), not as an error. DOC-004 §8 already drafts this.

---

## 6. Registry → DB cutover & backup discipline

- The serial list is **regenerable today** — serials are deterministic from `check_char()` + batch + seq. Losing the A001/A002 JSON costs only a re-run. **Not yet irreplaceable.**
- It becomes **irreplaceable the moment any seal hits REGISTERED** (event hashes, signatures, device IDs are unique crypto artifacts). Before the first registration:
  - **Postgres `trustseals` is the source of truth** (DOC-004 §7), not a JSON file.
  - Keep **git-tracked JSON snapshots** in the vault as backup of the *allocation/registry state*.
  - Confirm tracking:
    ```bash
    find ~/ZKNOT -name "*TS-A00*registry*.json" 2>/dev/null
    git -C ~/ZKNOT status --porcelain | grep -i trustseal
    ```
- This runbook itself: commit it to the vault (`git add` + signed commit) once you've made the printer/substrate calls — it's durable systems knowledge.

---

## 7. Legal / marking (verified)

- "PAT. PEND. — App# 63/961,112" is **accurate** (PAT-003, Confirmation 1239, filed 2026-01-15, status Filed). Keep it accurate — false marking is a real exposure (35 U.S.C. §292).
- That provisional's **12-month bar is 2027-01-15** — earlier than the general 2027-03-01 triage date. TrustSeal commercialization is the tighter clock; flag for the attorney engagement.
- A001 = prototype (not for paying customers / not for legal proceedings per DOC-004 §10). Sell A002.

---

## 8. Open items / next actions

- [ ] **§0 verify-route confirmation** (gates all printing)
- [ ] Order A002 substrate validation lot; run abuse + scan-after-damage tests
- [ ] Buy current-gen Zebra (confirm ZT231/ZT411 model); resin ribbon; matte laminate
- [ ] Get ZKKey working (gates field registration + Gate 2 demo, not sale)
- [ ] Apply schema add-on (§4) to the zknot.io Postgres
- [ ] Decide: gate seals behind ZKKey ownership, or sell ungated (§5)
- [ ] Decide: serial allocation source — keep per-product TS-batch scheme, or draw from the canonical `~/zk-number-ledger.psv`
- [ ] Commit this runbook + registry snapshot to the vault (signed)

---

*ZKNOT, INC. — When physics is policy, trust is optional.*
*Patent Pending — App# 63/961,112 · ops@zknot.io · verifyknot.io*
