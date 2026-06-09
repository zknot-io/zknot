---
title: verifyknot — Product Primer
type: product primer (paste after root CONTEXT)
status: canonical — supersedes verifyknot.md (charter) and verifyknot-primer v1/v2 (status)
owner: Shane
created: 2026-06-09
canonical_path: ~/ZKNOT/00_COMMAND/primers/verifyknot.md
points_to:
  - km/systems/verifyknot-device-threat-model.md (v2) — device taxonomy + badge logic
  - 6_SIG/SIG-VER-ZKKEY-001 (+ ADD-001) — verifier spec + time-binding decision
  - verifyknot-site/ (Cloudflare Pages) — the frontend, incl. the client-side verifier HTML
  - journal 2026-06-09 — the verification-gap finding
note: Live empirical checks outrank documented status on conflict. Last live check 2026-06-09.
---

# verifyknot — Product Primer

## 1. The one job (the whole discipline)

> **verifyknot exists so a skeptical third party — present nowhere, trusting no one — can turn a code or
> artifact into an independently re-checkable answer about whether a ZKNOT attestation is authentic and
> what it actually claims.**

Hard rule: **if any step of the cryptographic verdict requires trusting ZKNOT's server, the design has
failed.** This is the most load-bearing sentence in the company — verifyknot is the surface that makes
every device worth more than "trust us."

## 2. Scope discipline (the charter, folded in)

**Irreducible four** — remove any one and the job fails:
1. **Resolve** — a code/QR maps to the correct signed record.
2. **Verify in the open** — signature + chain re-checked **client-side** (or downloadable bundle + open
   verifier lib). The load-bearing one: the VERIFIED badge's authority is math the stranger re-runs, not
   verifyknot's say-so.
3. **Disclose honestly** — show exactly what the attestation does and does NOT claim.
4. **Anchor trust** — publish the keys so the root of trust isn't "the website told me."

**The NOT-list** (scope creep is a missing refusal list): NOT a login-gated app; NOT a CRM / asset
tracker / info surface; NOT the system of record. Verification and management are **opposite trust
models** — verification's value is being trust-*minimized*; management needs privileged trust. The
records sit in the backend already, so "just browse them here too" feels free — it isn't.

**Boundary router for any proposed feature:** *"Does this help a stranger check a claim without trusting
us?"* Yes → may belong here. Helps *us* store/manage/track → backend, not verifyknot.

## 3. HONEST current status (live-checked 2026-06-09)

**Live:** frontend serving on Cloudflare Pages (`/v/{code}` resolves); backend `/health` ok;
`GET /v1/verify/{code}` responds.

**The gap (this is the work):**
- **Short-code flow trusts the server.** `/v1/verify/ZK-6GUA-7DV` returns `"verified":true` and the
  browser shows that boolean — violating §1. The demo records are **placeholder** (signature
  `a1b2c3d4…` repeating; `challenge_hash` = SHA-256("test")).
- **A real client-side verifier ALREADY EXISTS** in the site (`verifyknot_io_index.html`): in-browser
  ECDSA P-256 via Web Crypto, short-code derivation from `SHA-256(sig‖nonce)`, no server call. The
  capability is proven — but it's the *paste-artifact* flow, not wired to the short-code flow.
- **That HTML carries a live honesty violation:** "Remote or automated signing is impossible by hardware
  design." This is the killed PAT-001 overclaim — FALSE for a firmware-enforced gate. **Fix immediately**
  (it's public): "a deliberate human press is required, enforced by immutable firmware — not claimed
  physically impossible." Also old-brand (ZKKey/PAT-010) and old-schema (presence-only ATECC sig over a
  nonce; no content-binding / identity-domain attestation / time-binding).

**So the live product currently does the opposite of its one job, and overclaims while doing it.** Caught
before any CO demo — closing it is the platform's top priority.

## 4. The most important work (prioritized)

**Do now (cheap, public, honest):**
- **A.** Remove the "impossible by hardware design" claim from the live frontend. One edit; it's false and live.

**Gating before any external/CO demo:**
- **B.** Wire short-code → fetch record *data* (not verdict) → run client-side verification on it →
  render the verdict the browser computed. Reuse the existing HTML's Web-Crypto approach as the core.
- **C.** Extend the verifier to the WitnessMark schema: two signatures (event + identity-domain
  attestation), the two binding fields (presence / content), chain to the YubiHSM root, COSE/CBOR,
  and the time check (VER-18′). Ship as **TS (browser) + Python (reference/test oracle)**.
- **D.** Seed ≥1 **real** signed record over a real artifact hash; label at its true tier
  (`SELF-ASSERTED` is honest; a mock asserting `VERIFIED` is not). Then the "you verified it, not us"
  line becomes true.
- **E.** `/v/{code}` canonical + `bare → /v/` redirect; update SOP-001 so docs stop asserting two forms.

**Build (decided):**
- Transparency-log evolution: ZK-LocalChain → Merkle log + TSA-anchored checkpoints + inclusion proofs +
  revocation-as-entry, **modeled on RFC 6962 / Trillian / C2SP — not invented**.

## 5. Device & badge taxonomy (brief — detail in threat-model v2)

Short code → event record; device class from `device_id` prefix; provenance from registry lookup.
`COMBINED_SESSION` binds >1 device → **one badge row per device**, never a single-signer assumption.

Prefixes: `ZK-K` Connect (human-presence), `ZK-A` Air (human-presence, optical), `PV-A` PowerVerify
Attested (autonomous power cert, NO human gate), `PV-C` Core (passive, no signed records).
*Generation note: threat-model v2 documents the as-built ATECC generation; WitnessMark (U585+OPTIGA)
records will carry two signatures + two binding fields — the verifier must handle both generations.*

**Three independent badge dimensions, never merged into one rating:**
- **Identity tier:** `CA-ATTESTED` *(GATED — not until cert-chain provisioning SOP confirmed in
  production; ceiling is `REGISTERED` until then)* → `REGISTERED` → `SELF-ASSERTED`.
- **Binding badges:** presence + content reported **independently**, each at true strength.
- **Assurance honesty:** signing key = PSA-L3; identity = EAL6+. Never imply the signing key is EAL6+.

**Honest-translation rule (VER-04):** a valid signature is not "a human was present"; presence is not
"approved this content." The headline maps 1:1 to the binding fields and no further.

## 6. Two surfaces, same data (do not blur)

| Surface | Trust model | Access | Role |
|---|---|---|---|
| Registry + ZK-LocalChain (backend) | Trusted | Full CRUD | System of record; info tracking lives here |
| verifyknot | Trust-minimized | Read-only | Thin public window onto the verifiable subset |

Public verify response returns only: verdict, per-device badges, proven facts, and data to reproduce the
check offline. Never owner identity, location, usage history. No login to verify.

## 7. Stack & decided facts

- Frontend: Cloudflare Pages (project `verifyknot`). Backend: FastAPI on Railway (`api.zknot.io`,
  0.115.12 / Py 3.13; SQLAlchemy 2.0.40 / Pydantic 2.11.1 pinned). Contract: `POST /v1/attest`,
  `GET /v1/verify/{code}`, `POST /v1/chain/verify`, `GET /health`.
- **Decided:** record serialization COSE/CBOR (multi-signer, not `COSE_Sign1`); time basis = RFC-3161
  TSA-anchored LocalChain (ADD-001, VER-18′ fail-closed); verifier libs TS + Python.

## 8. Open / confirm
- [ ] CA-ATTESTED gating: confirm cert-chain provisioning SOP in production before the badge renders.
- [ ] Approved-policy + revocation-list distribution under the HSM root, offline-checkable.
- [ ] HSM-root trust bootstrap: how a first-time verifier gets the root pubkey out-of-band (make auditable).
- [ ] Device-ID taxonomy + WitnessMark generation in threat-model; DIY/SelfKnot prefixes (not yet canonical).

---
*Supersedes verifyknot.md (charter) and verifyknot-primer v1/v2 (status). Points to threat-model v2,
SIG-VER-001(+ADD-001), the frontend, and the 2026-06-09 journal. The discipline that governs every line,
including this primer's account of its own readiness: state exactly what is true and no more.*

*Page 1 of 1*
