---
title: ZKNOT Cryptographic Provisioning Process — Architecture & Decisions Locked
date: 2026-05-29
author: William Shane Wilkinson
status: decisions_final
tags: provisioning, pki, hardware, atecc, yubihsm, trustcustom
---

# Provisioning Process Architecture — Final Decisions

## TL;DR

Committed to a **root CA + intermediate CA on YubiHSM 2** architecture with **TrustCUSTOM ATECC608B** per-product config, **3-chip validation run** before full 100-unit provisioning, and **wrap-key offline backup** of HSM keys. Trust model is one-way: HSM-rooted CA signs device certs, device private keys never leave silicon, provisioning host cannot extract either key. Path forward is locked: bench bring-up on validation chips, TPDS config definition (pending PUF binding decision), then full provisioning loop with manifest + operator sign-off.

## Decisions Made (Irreversible)

### Hierarchy: Root + Intermediate CA (both HSM-resident)
- **Root CA (Object ID 1):** P-256, on-device generated, non-extractable, signs the intermediate cert *once and never again*. Purely offline after issuance.
- **Intermediate CA (Object ID 2):** P-256, on-device generated, non-extractable, signs all device certificates during provisioning. Low-privilege provisioning auth key can *only* execute ECDSA sign with this key.
- **Rationale:** Intermediate-only ops reduces blast radius if provisioning is ever breached; root cert can be published and never changes; rotation path is cleaner (new intermediate, old certs stay valid).

### Config Path: TrustCUSTOM (you write and lock the config zone)
- **Assumption:** DigiKey parts are factory-unlocked ATECC608B (no factory locking mentioned). Confirmed with digikey SKU/lot before manufacturing next batch.
- **Implication:** You own the full config-zone definition and byte-by-byte lock sequence. Max flexibility, max brick risk on typos — mitigated by TPDS validation and 3-chip burn-in.
- **Alternative considered:** TrustFLEX ships config pre-locked (factory-safe, fewer degrees of freedom). Not your path for v1, but worth monitoring for future production scale-up.

### Slot Mapping: Per-Product-Line Templates
- **One config template for PowerVerify, one for ZKKey Connect, one for ZKKey Air.** Same architecture (identity key in slot 0, cert slots 8–9), different support slot assignments if needed downstream.
- **Slot 0:** Primary identity (P-256, internally generated GenKey, never readable/writable after lock).
- **Slots 8–9:** Compressed device cert + signer cert (write-locked, read-enabled for verification).
- **Pending:** Slot allocation for symmetric keys or PUF binding (see decision pending below).

### Backup Strategy: Wrap-Key → Encrypted Offline, Second HSM Later
- **Immediate (today):** Generate on-HSM key-wrap key (Object ID 3), export wrapped copies of root + intermediate to encrypted media (GPG or age), store offline on USB or air-gapped storage.
- **Future (scaling phase):** Second YubiHSM as restore target when ops maturity allows.
- **Rationale:** Single HSM is single point of failure for *future key issuance* (verification always works off public root). Encrypted offline backup is the pragmatic middle ground; second HSM adds cost + operational complexity not justified on day 1.

### Validation Batch: 3 Sacrificial Chips
- **Purpose:** De-risk the config zone lock, GenKey, cert issuance, and end-to-end verification before touching the production 100.
- **Expected loss:** 3 chips (treat as R&D cost, not yields problem).
- **Success criteria:** Read serial → write validated config → lock → GenKey → sign cert → lock → challenge-response verify all pass, chain validates cleanly.
- **Serial tracking:** Validation chips get sequential prefixes (TEST-001, TEST-002, TEST-003) in manifest; never shipped.

---

## Trust Model (Why This Matters)

```
Root CA (HSM, P-256)
    │
    └─ signs once ─> Intermediate CA Cert
                          │
                          ├─ resides on HSM
                          │
                          └─ signs at provisioning time ─> Device Cert
                                                               │
                                                               └─ public key embedded in cert
                                                               └─ device's identity private key
                                                                  never leaves ATECC
```

**Key properties:**
- Root private key is non-extractable on the HSM. It is never in plaintext, never exported, never at risk during provisioning.
- Device private keys are generated on-chip (GenKey command). They never exist off-chip. ATECC firmware prevents extraction.
- Provisioning host (your Debian box) never holds any private key. It holds the unsigned device public key and asks the YubiHSM to sign the certificate. The signed cert comes back; host writes it to the device.
- **Consequence:** A compromised provisioning host cannot fake a device certificate. It cannot forge a signature. It cannot leak either CA private key.
- **Verification path:** Backend (api.zknot.io) stores only the **public root certificate**. To verify a device, extract its cert, verify the cert signature against the public root, verify the device's identity signature against the cert public key. If both check out, the device is legitimate.

This is the moat. Any company can solder an ATECC to a board. Almost none can show an auditable, HSM-rooted chain of custody from blank silicon to verifiable device.

---

## Phases (Sequenced Checkpoints)

### Phase 0 — Decision Ratification
✅ **DONE** (this entry). All five decision axes locked. PUF binding decision pending (see below).

### Phase 1 — HSM Bootstrap & Backup
- Install YubiHSM tools + Python libraries.
- Change default auth key (0 / password).
- Generate root CA key on-device (Object ID 1).
- Generate intermediate signing key on-device (Object ID 2).
- Export public keys.
- **Generate wrap key (Object ID 3) and export wrapped root + intermediate to encrypted offline media.**
- **Checkpoint:** Root + intermediate are on the HSM and backed up. Default auth key changed. Dev can proceed to Phase 2.

### Phase 2 — Bench Bring-Up & Config Validation
- **Hardware check:** FT260 plugged in, ATECC at 0x60 responds to i2cdetect.
- **Cryptoauthlib integration:** Python script reads serial from test chip #1.
- **TPDS config definition:** Define PowerVerify template (slot layout, cert definitions, config zone bytes). Validate in TPDS, export config binary + cert-def.
- **Test write:** Write validated config to test chip #1, lock config zone. ⚠️ Irreversible.
- **GenKey + cert sign:** Generate identity public key on test chip #1, build cert TBS, send to HSM, receive signature, compress and write cert to chip, lock data zone.
- **Full chain verify:** Confirm device signature validates against cert, cert validates against root, chain completes. Success = move to test chip #2 (same flow), then #3.
- **Expected yield:** 3/3 pass (if config is correct). 0/3 pass (if config has a bug) = config revision needed.
- **Checkpoint:** All three test chips complete provisioning and verify cleanly. Config template is validated. Move to Phase 3.

### Phase 3 — Per-Chip Provisioning Pipeline (The Repeatable Loop)
For each chip in the production batch (4–100):
1. Wake, read serial.
2. Write config zone (same template as Phase 2).
3. **Lock config zone.** ⚠️ Permanent.
4. GenKey on identity slot → public key.
5. HSM signs cert over (serial + public key + metadata).
6. Write cert, lock data zone. ⚠️ Permanent.
7. Challenge-response verify.
8. Append to provisioning manifest.
9. Move to next chip.

**Output:** Provisioning manifest (CSV or JSON): serial, public key, issued cert, batch ID, config-template hash, timestamp, operator (William Shane Wilkinson), pass/fail.

### Phase 4 — Records & Backend Integration
- Provisioning manifest is the source of truth for issued device identity.
- Backend (api.zknot.io) consumes manifest, stores device public keys and certs.
- Verification flow (verifyknot.io + backend): user scans code, backend looks up serial, checks device cert + signature against root, returns status.

---

## Critical Decision Still Pending: PUF Binding

**Question:** Does PowerVerify's PUF binding live entirely in the optical verification (camera + LED, 12" 90° geometry, 100+ lumen), or should the ATECC also store a PUF hash/descriptor and bind it cryptographically to the device identity?

**Option A (optical only, current assumption):**
- ATECC holds device identity key only.
- PUF verification is a separate optical process (verifyknot.io).
- Advantage: simpler ATECC config, no interdependency.
- Disadvantage: identity and PUF are two unrelated facts; a bad actor could in theory move an ATECC to a counterfeit product with a fake PUF, and the ATECC would still verify.

**Option B (ATECC-bound):**
- ATECC stores a PUF descriptor hash (e.g., SHA-256 of the PUF's response to a known stimulus).
- Device cert embeds or references the PUF hash.
- Verification flow: verify ATECC identity + cert, *then* verify live PUF against stored hash.
- Advantage: identity and PUF are cryptographically tied; much harder to substitute.
- Disadvantage: adds complexity, requires stable PUF capture at provisioning time, adds a slot in the config.

**Why it matters now:** TPDS config template and slot allocation depend on the answer. If Option B, you need a dedicated slot for the PUF descriptor, and the cert definition changes.

**Recommendation:** Start with Option A (optical only). You can upgrade to Option B later if a buyer or use case demands stronger binding. Simpler = fewer ways to brick the chips on day 1.

**What's your call?** Once you answer, I can guide the TPDS template definition.

---

## Irreversible/High-Risk Steps (Flag These)

- ✅ **HSM keys:** Root + intermediate are on-device, non-extractable, backed up. No risk (can restore from backup if HSM dies). Keys will never leave plaintext.
- ⚠️ **Config zone lock:** Once locked, the config zone is permanently read-only. A single typo in the 128-byte config = 100 bricks. **Mitigated by:** TPDS validation, 3-chip burn-in before production run, careful byte-by-byte review before lock command.
- ⚠️ **Data zone lock:** Once locked, the device cert and slot permissions are permanent. Less risky than config (cert can be overwritten if write-enable persists), but still permanent. **Mitigated by:** Full chain verify before moving to next chip.

---

## Next Actions

### Immediate (this session or next)
1. **Hardware readiness:** Plug in YubiHSM + FT260, confirm `i2cdetect -l` shows FT260 bus, `i2cdetect -y N` shows ATECC at 0x60.
2. **Install YubiHSM tools:** `apt install yubihsm-shell yubihsm-connector`, `pip install yubihsm cryptoauthlib --break-system-packages`.
3. **Bootstrap HSM:** Start connector, generate root + intermediate on-device, create wrap key, export wrapped backups to encrypted media.
4. **Validate cryptoauthlib:** Write `provision_test.py` to read serial from ATECC via FT260 i2c bus.
5. **Pending decision:** Answer the PUF binding question above.

### Before Phase 2 (once hardware + HSM are ready)
6. **Download TPDS:** Microchip Trust Platform Design Suite. Define PowerVerify config template (assuming Option A, PUF optional).
7. **Export config:** TPDS outputs config zone binary + cert definition file.

### Phase 2 (bench bring-up, ~1–2 hours, heavily manual)
8. **Test chip #1:** Write config, lock, GenKey, sign, verify.
9. **Test chips #2–3:** Repeat. If all three pass, config is validated.

### Phase 3 (production run, highly repeatable)
10. **Batch runner:** Write provisioning loop (read serial → write config → lock → GenKey → HSM sign → write cert → verify → log). Run on chips 4–100.
11. **Manifest:** Capture every provisioning event + operator sign-off.

---

## References & Context

- **Hierarchy:** Root CA (HSM, P-256, non-extractable) signs intermediate (HSM, P-256, non-extractable), intermediate signs device certs at provisioning time.
- **Hardware:** UMFT260EV1A (FT260 USB-I2C bridge, confirmed in-tree Linux driver support as of kernel 5.13). ATECC608B TrustCUSTOM (you write config). YubiHSM 2 (v2.4, SKU 5060408465462, AN 100846).
- **Software stack:** cryptoauthlib (C library, Python bindings), yubihsm-connector (HSM daemon), yubihsm (Python SDK), TPDS (Microchip design suite for config validation).
- **Backup:** Wrap key on HSM, encrypted export to offline media (GPG/age).
- **Validation:** 3 sacrificial chips, full chain verify before production run.
- **Operator sign-off:** William Shane Wilkinson on all batch records (federal filing convention).

---

## Journal Links & Related

- **Replaced:** ~~SBIR Phase I June 3 deadline~~ (no good fit, refocus on moat-building).
- **System docs:** See `~/ZKNOT/3_OPS/km/systems/pki-provisioning.md` (to be created in Phase 1).
- **Operational:** See `~/ZKNOT/00_COMMAND/ZKNOT-PROC-PROV-001` (SOP, to be authored once Phase 1 completes).
- **References:** Microchip CryptoAuthLib docs, TPDS user guide, YubiHSM documentation.

---

## Notes

- The PUF binding decision is the only open architectural question. Everything else is locked.
- Do not skip Phase 2 bench bring-up. Three sacrificial chips are the cheapest insurance against discovering a config bug after you've bricked 30 units.
- The provisioning manifest is the foundation of traceability and future revocation. Capture operator, timestamp, batch ID, and pass/fail on *every* chip.
- This process is auditable. A buyer, auditor, or security researcher can follow the chain from root CA → intermediate cert → device cert → device signature → public ledger. That's a competitive edge.
