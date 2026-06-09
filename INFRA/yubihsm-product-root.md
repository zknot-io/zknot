---
title: YubiHSM 2 — ZKNOT Product Trust Root (provisioning + DR runbook)
system: hardware-root-of-trust / issuing-attestation-root
domain: ZKNOT PRODUCT trust domain (civilian/commercial — ZKKey Connect / ZKKey Air)
status: IN PROGRESS — phase 1 (SKU/firmware confirmation)
owner: William Shane Wilkinson
created: 2026-05-30
last_verified: 2026-05-30
related: km/systems/hardware-root-of-trust.md, PAT-001
---

# YubiHSM 2 — ZKNOT Product Trust Root

> **What this is.** The on-device, non-extractable issuing/attestation root that
> certifies per-product ZKKey identities. Field secure elements (ATECC / TrustCUSTOM,
> provisioned separately over the FT260) are certified *under* this root —
> HSM-rooted two-tier provisioning.
>
> **Trust-domain rule (hard).** This is the PRODUCT domain. It is NOT the
> open/educational FT260+ATECC path and NOT the future federal/FIPS root.
> Keys are non-extractable across domain boundaries by design. The federal root
> gets **generated fresh on its own FIPS unit** — never migrated from here.

---

## TL;DR — the non-negotiable order

```
1. Confirm SKU (FIPS etch?) + firmware + supported algorithms      [unauth, safe]
2. Connector up; open session on factory key 1; inventory objects  [reversible]
3. Create your admin authkey → verify auth → DELETE factory key 1   [credential swap]
4. Decide wrap-key birth model; PUT/GENERATE wrap key
5. TEST the wrap loop on a DISPOSABLE object (export→delete→import) [<-- before any root]
   + prove held wrap-key bytes re-import via `put wrapkey`
====================  STOP. Confirm backup is real.  ====================
6. Generate the product root (ECDSA, approved set) ON-device
7. Export root wrapped → store offline → verify the wrapped backup
```

**The irreversible-loss point is step 6 happening before step 5 is proven.**
A dead/reset/lost HSM destroys the root and every attestation chained to it —
permanently — unless a tested, portable wrapped backup already exists.

---

## Verified facts (primary sources, checked 2026-05-30)

| Fact | Finding | Source |
|---|---|---|
| Ed25519 / EdDSA in approved mode | **NOT approved.** Listed under "non-approved algorithms disabled in the Approved mode"; EdDSA signing is non-approved-mode only. Device supports it as HW capability, but it cannot be used in approved mode. | cert #3916 Security Policy v1.3 (fw 2.2.0) |
| Approved ECDSA curves (key gen) | P-224, P-256, P-384, P-521 | cert #3916 Security Policy v1.3 |
| Approved wrap (key transport) | AES-CCM (SP800-38F compliant key wrap) | cert #3916 Security Policy v1.3 |
| Cert #3916 status | FIPS 140-2, Overall Level 3, **Active, sunset 2026-05-02** | NIST CMVP cert #3916 |
| FIPS 140-3 | In process (Yubico) — no validated 140-3 cert to cite | Yubico CMVP updates |
| SDK | Current packaged ~2026-03 (2.4 fw line). Download signed pkg from Yubico; verify sig. | developers.yubico.com/YubiHSM2/Releases |

**Algorithm decision for THIS root:** ECDSA, approved set.
Recommend **P-384 for the root** (margin for a long-lived issuing key); **P-256 acceptable**
(faster/smaller, fine for the attestation workload). A P-384 root signing P-256 leaf
attestation certs is a normal, valid chain. Develop against the approved set throughout
so the same codebase runs in approved mode on the future FIPS unit.

**Do NOT** put "140-2 L3 validated" / "140-3 validated" on any federal-facing artifact
from this work. Cert sunset 2026-05-02; federal claims belong to the separate federal-root
effort and require a live CMVP re-check at that time.

---

## Wrap-key birth model — decide before step 4 (the DR-defining choice)

The wrap key is AES-CCM. A replacement HSM can restore the root **only if it holds the
same wrap key**. How the wrap key is born determines whether DR is possible at all:

| Option | Pro | Con |
|---|---|---|
| **Generate ON-device** (`generate wrapkey`) | Best entropy story; raw bytes never touch software | Bytes can't leave → **cannot re-import to a new unit** → dead device = unrecoverable root. Not portable. |
| **Generate bytes yourself + `put wrapkey`** | Only path that restores onto replacement hardware; held bytes = portable DR | Raw AES key exists in SW/offline media at creation → handling discipline is everything |

**For a DR root you need the second option.** The held bytes become the crown jewel
(guardrail #3): offline media, not a gitignored file on the working disk. Consider
M-of-N split if you want no single point of compromise.

**Honest limit of the test on one unit:**
- `export → delete → import` on the same device proves wrap/unwrap + capability flags.
- It does **not** prove dead-device→new-device recovery.
- True new-hardware restore is only conclusively testable against a second unit
  (your future FIPS box is a *separate domain* — don't use it for this).
- With one unit now, the most you can prove is that your held bytes re-import cleanly
  via `put wrapkey`. Record this residual gap; close it when a second product unit exists.

---

## Phase commands

> You run all of these. Token names (e.g. `get-device-info`) drift between SDK
> versions — if one errors, check `yubihsm-shell --help` / in-shell `help`.
> Confirm rather than guess.

### Phase 1 — SKU / firmware / inventory  [STATUS: in progress]

```bash
# Install (after downloading + verifying signature yourself):
cd ~/Downloads
gpg --verify yubihsm2-sdk-*.tar.gz.sig yubihsm2-sdk-*.tar.gz   # require: Good signature
tar xzf yubihsm2-sdk-*.tar.gz && cd yubihsm2-sdk
sudo dpkg -i libyubihsm*.deb yubihsm-connector*.deb yubihsm-shell*.deb
sudo apt-get -f install

# Connector up; confirm device seen BEFORE a session:
yubihsm-connector -d
curl -s http://127.0.0.1:12345/connector/status      # expect status=OK + serial

# SKU/firmware (Device Info is unauthenticated — no session):
yubihsm-shell -a get-device-info
#   Physical SKU tell: look for "FIPS" laser-etched on the device body.

# Inventory under factory key (only time you touch key 1):
yubihsm-shell
  connect
  session open 1 password
  list objects
```

Record: firmware = `____`  serial = `____`  FIPS-etched = `____`
objects seen = `____` (expect: authkey ID 1; pre-loaded Yubico attestation cert)

### Phase 3 — credential swap  [STATUS: pending]

```
# In an open factory session, create your admin authkey (give it the caps you need,
# incl. delete-object, put/generate authkey, generate/put wrapkey, export/import-wrapped,
# generate-asymmetric, sign-* as needed). Then VERIFY you can auth with it. Then delete key 1.
#   put authkey  <new-id> <domains> <caps> <delegated-caps> <password>
#   (close session; re-open with the NEW id/password to VERIFY before deleting key 1)
#   delete object 1 authentication-key
```
- [ ] New admin authkey created
- [ ] Re-authenticated with new key (verified) BEFORE deleting key 1
- [ ] Factory key 1 deleted
- Secrets → `~/ZKNOT/99_SENSITIVE/` (mode 600, gitignored) at most.

### Phase 4–5 — wrap key + TESTED restore loop  [STATUS: pending]

```
# Per the birth-model decision above. If importing held bytes:
#   put wrapkey <id> <domains> <caps> <delegated-caps> <algo: aes256-ccm-wrap> <key-bytes>
# Disposable-object loop (do this BEFORE any real root):
#   generate asymmetric <throwaway-id> ... ecp256        # disposable, exportable-under-wrap
#   get wrapped <wrapkey-id> asymmetric-key <throwaway-id> > throwaway.wrap
#   delete object <throwaway-id> asymmetric-key
#   put wrapped <wrapkey-id> throwaway.wrap               # restore; confirm object returns
```
- [ ] Wrap key in place (birth model: ________________)
- [ ] Disposable object export→delete→import succeeded
- [ ] Held wrap-key bytes confirmed re-importable via `put wrapkey`
- [ ] **Wrap-key bytes on OFFLINE media** (not just gitignored disk) — crown jewel
- [ ] Residual gap recorded: new-hardware restore not yet tested (no 2nd unit)

### ===== STOP GATE — confirm with operator before Phase 6 =====

Do not generate the root until every box in Phase 4–5 is ticked.

### Phase 6–7 — generate + back up the product root  [STATUS: pending]

```
#   generate asymmetric <root-id> "zknot-product-root" <domains> \
#       sign-ecdsa,... ecp384            # or ecp256 per decision
#   get wrapped <wrapkey-id> asymmetric-key <root-id> > zknot-product-root.wrap
#   delete + put wrapped on a copy to VERIFY the backup restores
#   (optional) generate attestation certificate for the root / leaf model per step-5 decision
```
- [ ] Root generated ON-device (NOT imported — born here, stays here)
- [ ] Root exported wrapped; wrapped file stored offline
- [ ] Wrapped backup VERIFIED by test-restore
- [ ] Attestation model chosen: factory-certified key vs. own imported key+cert
- [ ] **Backed up?** root (wrapped) = ____   wrap-key bytes (offline) = ____

---

## Secrets / version-control discipline

- **Version-controllable:** this runbook, object IDs/labels/domains, capability sets,
  device serial, firmware notes, the *public* root key + attestation certs.
- **NEVER committed:** any private key material; wrap-key bytes; authkey passwords.
- Auth-key / wrap-key secrets: `~/ZKNOT/99_SENSITIVE/` (mode 600, gitignored) *at most*.
- Wrap-key bytes additionally → **offline media** (their loss = no DR).

---

## Open items

1. [ ] SKU (FIPS etch?) + firmware confirmed
2. [ ] Connector OK; factory inventory captured
3. [ ] Admin identity established; factory key 1 deleted
4. [ ] Wrap-key birth model decided; wrap loop TESTED on disposable object
5. [ ] Root/attestation key type (P-256 vs P-384) + attestation model decided
6. [ ] Root generated, wrapped-backed-up, backup verified
