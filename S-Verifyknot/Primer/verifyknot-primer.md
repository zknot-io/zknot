---
title: verifyknot — Platform Primer & Current Status
version: v2
system: verifyknot
status: active
created: 2026-06-09
supersedes: verifyknot-primer v1 (2026-06-09, same day — re-leveled after live verification)
owner: Shane
canonical_path: ~/ZKNOT/3_OPS/km/systems/verifyknot-primer.md
primary_sources:
  - ZKNOT_SOP-001_platform (v1.0, 2026-03-28) — deployment/stack ground truth
  - SIG-VER-ZKKEY-001 verifier spec (v0.1, 2026-06-08) — verification logic
  - SIG-VER-ZKKEY-001-ADD-001 time-binding decision (2026-06-08) — closes verifier §7
  - verifyknot.md purpose/scope (2026-06-05) — the one job + NOT-list
  - verifyknot-device-threat-model v2 (2026-06-04) — device/badge taxonomy
  - LIVE CHECKS 2026-06-09 — see §0/§3 (empirical, supersedes status claims on conflict)
note: Where sources disagree, the disagreement is surfaced, not silently resolved. Live empirical
  checks (2026-06-09) outrank documented status claims.
---

# verifyknot — Platform Primer & Current Status (v2)

## 0. Deployment status — the HONEST two-state picture (re-leveled 2026-06-09)

The earlier "deployed and live" framing was true for the *frontend* but obscured the part that matters
most. Verified empirically on 2026-06-09:

**What IS live:**
- Frontend **deployed and serving** on Cloudflare Pages. `https://verifyknot.io/v/{code}` resolves and
  renders the verification page (messaging: "No trust required," "Math is the testimony," "Independent
  of ZKNOT").
- Backend live: `GET https://api.zknot.io/health` → `{"status":"ok"}`. `GET /v1/verify/{code}` responds.

**What is NOT yet live (and the page's headline currently overstates):**
- **The cryptographic verdict is server-asserted, not client-reproduced.** `/v1/verify/ZK-6GUA-7DV`
  returns `"verified": true` + `"verification_message": "Attestation verified"` — and the browser
  displays that boolean. There is no evidence the signature/chain math runs client-side. This is the
  *opposite* of the one job (§1) and violates VER-02: **today a stranger is trusting ZKNOT's server.**
- **The demo records are PLACEHOLDER data.** `ZK-6GUA-7DV` returns `signature` = `a1b2c3d4e5f6…`
  (repeating filler, not a real ECDSA signature), `public_key` = `04a1b2c3…` (filler), `challenge_hash`
  = `9f86d081…` (= SHA-256 of the literal string "test"). The `verified:true` is asserted over mock data.

**Consequence — do not run the "you didn't trust us, the math verified it" demo line until the
client-side verifier ships AND at least one real signed record exists.** In front of a security-literate
contracting officer, a `curl` of the endpoint exposes the placeholder signature and the trust-minimized
pitch collapses — harder than an ordinary bug, because the entire differentiator is "don't trust us."
This is a candor/honest-translation problem (§1, VER-04), not just a backlog item.

> Re-run anytime:
> ```bash
> curl -sS https://api.zknot.io/health
> curl -sS https://api.zknot.io/v1/verify/ZK-6GUA-7DV | jq .
> curl -sS -o /dev/null -w "/v/ -> %{http_code}\n"  https://verifyknot.io/v/ZK-6GUA-7DV
> curl -sS -o /dev/null -w "bare -> %{http_code}\n" https://verifyknot.io/ZK-6GUA-7DV
> ```

---

## 1. The one job (the whole discipline)

> **verifyknot exists so a skeptical third party — present nowhere, trusting no one — can turn a code or
> artifact into an independently re-checkable answer about whether a ZKNOT attestation is authentic and
> what it actually claims.**

The verifier spec states it as a hard rule: *if any step of the cryptographic verdict requires the
verifier to trust ZKNOT's server, the design has failed.* **Per §0, the live site currently fails this
rule** — closing that gap (the TS client verifier, §7 item 1) is the platform's top priority.

It is for **third-party verification of attestations**, never information tracking.

---

## 2. The irreducible four (remove any one and the job fails)

1. **Resolve** — a short code / QR maps to the correct signed record. *(Live.)*
2. **Verify in the open** — signature + hash chain re-checked **client-side** (or via downloadable bundle
   + open verifier lib). *(NOT yet met — currently server-asserted. This is the gap.)*
3. **Disclose honestly** — show exactly what the attestation does and does NOT claim. *(Discipline
   defined; must be driven by real data, not mock.)*
4. **Anchor trust** — publish the public keys so the root of trust isn't "the website told me."

### The enforced NOT-list
verifyknot must NOT become: a login-gated app; a CRM / asset tracker / info-management surface; the
system of record. Verification and management are **opposite trust models**. **Router for any proposed
feature:** *"Does this help a stranger check a claim without trusting us?"* Yes → verifyknot. Helps *us*
store/manage/track → backend.

---

## 3. Live stack & the URL-path resolution

| System | Status (live 2026-06-09) | Platform | URL |
|---|---|---|---|
| verifyknot.io (frontend) | ✅ Serving | Cloudflare Pages (`verifyknot`) | https://verifyknot.io |
| api.zknot.io (backend) | ✅ `/health` ok | Railway / FastAPI 0.115.12, Py 3.13 | https://api.zknot.io |
| PostgreSQL registry | ✅ Live | Railway managed plugin | via Railway |
| ZK-LocalChain | ✅ records present (demo data placeholder) | production Postgres | n/a |
| **Client-side verifier** | ❌ **NOT live** — verdict is server-asserted | — | — |
| **Real signed demo records** | ❌ **placeholder data** | — | — |

Backend contract: `POST /v1/attest`, `GET /v1/verify/{short_code}`, `POST /v1/chain/verify`,
`GET /health`, `GET /docs`. SQLAlchemy 2.0.40 / Pydantic 2.11.1 pinned (earlier break on Py 3.13).

### URL-path discrepancy — RESOLVED (recommendation, pending implementation)
- `/v/{code}` resolves and serves (confirmed live). SOP-001's bare path `verifyknot.io/{code}` relied on
  `_redirects: /* /index.html 200`.
- **Recommendation: make `/v/{code}` canonical** (it namespaces verification, leaves the rest of the site
  free, matches the verifier spec) **and add a `bare → /v/` redirect** so SOP-001 demo links don't 404.
  Update SOP-001's demo script to `/v/` so both docs stop asserting different "live" forms.
- Tradeoff noted: the bare path is shorter to read aloud, but it collides the whole URL namespace with
  code-lookup and can't coexist with other site pages without carve-outs.

---

## 4. Device & badge taxonomy (what the verify page renders)

A short code resolves to an event record; device class is read from the `device_id` prefix; provenance
from a registry lookup. A `COMBINED_SESSION` may bind more than one device — **render one badge row per
device** (never assume a single signer). *(Note: the live page currently renders VERIFIED over mock data;
badges are not yet computed from real client-side verification — §0.)*

| prefix | product | signs | identity source | human gate |
|---|---|---|---|---|
| ZK-K | ZKKey / WitnessMark Connect | human-presence sig | ZKNOT registry (pubkey) | YES (PAT-001/008 FSM) |
| ZK-A | ZKKey / WitnessMark Air | human-presence sig | ZKNOT registry | YES (optical air-gap, PAT-009) |
| PV-A | PowerVerify Attested | power-session cert | ZKNOT registry | NO — autonomous |
| PV-C | PowerVerify Core | nothing (passive) | multimeter only | n/a — no signed records |

**Three independent badge dimensions, never merged into one star rating:**
- **Identity tier:** `CA-ATTESTED` *(GATED — do not render until the X.509 cert-chain provisioning SOP is
  confirmed in production; cross-cert flow specced in SIG-FW-001 §6 but not yet confirmed live; ceiling is
  `REGISTERED` until then)* → `REGISTERED` (pubkey known to registry) → `SELF-ASSERTED` (DIY/unregistered).
- **Binding badges:** `presence_binding_type` and `content_binding_type` reported **independently**, each
  at true strength. Flagship = `(secure-domain, secure-domain-display)`. Anything weaker surfaced as
  weaker, in plain language.
- **Assurance honesty line:** signing key = PSA-L3; identity = EAL6+. Never imply the signing key is
  EAL6+/tamper-proof.

**Honest-translation rule (VER-04):** a valid signature is not "a human was present"; presence is not
"the human approved this content." The headline sentence maps 1:1 to the two binding fields and no further.

---

## 5. Demo records (SOP-001 §7) — NOT demo-ready until real signatures exist

| Short code | Type | Vertical |
|---|---|---|
| ZK-6GUA-7DV | COMBINED_SESSION | Main demo / genesis (chain pos 0) |
| ZK-4Z7Y-D3N | POWER_SESSION | Election — PowerVerify |
| ZK-CZDG-PP4 | ZKEY_SIGN | Election — ZKKey |
| ZK-69DT-HUS | TRUST_SEAL | Pharma / DSCSA |
| ZK-7TLR-N75 | COMBINED_SESSION | Journalism |

**These currently resolve to placeholder data (§0).** Before any external demo: seed at least one record
that is a **real signature over a real artifact hash** by a real (even dev/software) key, labeled
honestly at its true tier (`SELF-ASSERTED` is fine and honest; a mock record asserting `VERIFIED` is not).

**Honest demo line (use only once the client-side verifier is live AND the record is real):** "Open
[verify URL]/v/{code}. The signature check just ran in *your* browser against the published key — not on
our server. You verified it; you didn't trust us." Until then, do not make the "math verified it" claim.

---

## 6. Two surfaces, same data (do not blur)

| Surface | Trust model | Access | Role |
|---|---|---|---|
| Registry + ZK-LocalChain (backend) | Trusted | Full CRUD | System of record; info tracking lives here |
| verifyknot | Trust-minimized | Read-only | Thin public window onto the verifiable subset |

Public verify response returns only: verdict, per-device badges, proven facts, and data to reproduce the
check offline. Never owner identity, location, usage history, or any management field. No login to verify.

---

## 7. Open / verify-before-build items (re-prioritized 2026-06-09)

**Gating (close before any external/CO demo):**
1. [ ] **Client-side verifier (VER-33) — TS in the browser, Python as reference/test oracle.** The math
   must run client-side; the verdict must be one the browser computed, not the server's boolean. *This is
   the platform's top priority — until it ships, §1 is not met.*
2. [ ] **Real signed demo records** — replace placeholder data with genuine signatures over real artifact
   hashes; label at honest tier.
3. [ ] **URL form:** implement `/v/` canonical + `bare → /v/` redirect; update SOP-001 (§3).

**Build / decided:**
4. [ ] **Transparency-log evolution:** evolve ZK-LocalChain into a Merkle transparency log with
   TSA-anchored checkpoints + inclusion proofs + revocation-as-entry — **modeled on RFC 6962 / Trillian /
   C2SP patterns, not invented** (per 2026-06-09 decision and SIG-VER-001-ADD-001).
5. [x] **Time-binding — DECIDED (ADD-001):** RFC-3161 TSA-anchored LocalChain (primary) + optional
   signing-time TST (upgrade) + honest degradation. *(was the verifier spec's biggest open question.)*
6. [x] **Record serialization — DECIDED:** COSE/CBOR (RFC 9052). Note: event sig + identity-domain
   attestation + combined-session means NOT a plain `COSE_Sign1` — design in the wire-format spec.

**Still open:**
7. [ ] **CA-ATTESTED gating:** confirm cert-chain provisioning SOP in production before the badge renders
   (`REGISTERED` is the ceiling until then).
8. [ ] **Approved-policy + revocation-list distribution** under the HSM root, offline-checkable.
9. [ ] **HSM-root trust bootstrap:** how a first-time verifier obtains the root pubkey out-of-band (the
   one unavoidable trust step — make it auditable).
10. [ ] **Device-ID prefix taxonomy** may shift with the WitnessMark rename.
11. [ ] **DIY/SelfKnot prefixes** not yet canonical in HW-001 — treat as display-layer strings until in a
    primary source.

---

*Provenance: SOP-001 (2026-03-28), SIG-VER-ZKKEY-001 v0.1 + ADD-001 (2026-06-08), verifyknot.md
(2026-06-05), device-threat-model v2 (2026-06-04), live checks (2026-06-09). v2 re-levels §0 to the honest
two-state picture after empirical verification: frontend serving, but cryptographic verification is
server-asserted (not client-reproduced) and demo records are placeholder. Honest-translation discipline
(VER-04) governs every output — including this primer's account of its own readiness.*

*Page 1 of 1*
