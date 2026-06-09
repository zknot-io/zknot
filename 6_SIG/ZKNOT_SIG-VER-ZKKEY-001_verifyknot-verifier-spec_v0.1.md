---
title: verifyknot — Verifier Specification (Gate #4)
doc_id: SIG-VER-ZKKEY-001
status: DRAFT — verification-authority logic under the canonical capability spec
parent: SIG-SPEC-ZKKEY-005 (canonical capability spec)
siblings: SIG-FW-ZKKEY-001 (firmware/secure-config enforcement)
author: William Shane Wilkinson (ZKNOT, INC.)
date: 2026-06-08
surface: verifyknot.io (public verification authority) · api.zknot.io (FastAPI) · ZK-LocalChain
classification: ZKNOT INTERNAL — patent-sensitive (aligns PAT-020 §11/FIG.7, PAT-004, PAT-006, PAT-007)
scope: verifies WitnessMark/ZKKey attestations + combined multi-device sessions; device names provisional
---
SIG-VER-ZKKEY-001 → v0.2 (fold ADD-001, resolve its §7): VER-18 → VER-18′ (upper-bound T_ub rule, fail-closed) + VER-18″ (signing-time TST tighter bound); VER-30 → VER-30′ (declare tier: signing-time / log-anchored / device-asserted); expand VER-31 bundle with inclusion proof + including checkpoint + TST(s) + revocation snapshot; close open item #1. Plus the backend work (TL-01..07: Merkle tree, checkpoints, ≥2 TSAs, publish, inclusion-proof API, revocation-as-logged-entry on api.zknot
# verifyknot — Verifier Specification (Gate #4)

## 0. The one job

verifyknot exists to let a **skeptical third party verify an attestation without trusting ZKNOT.** That single sentence is the whole design constraint, and most of this spec is downstream of it. If any step of the cryptographic verdict requires the verifier to believe ZKNOT's server, the design has failed.

**Explicitly NOT verifyknot's job** (these belong in the backend registry, never on the verification surface): no CRM, no asset tracking, no usage analytics, no login-gated access, no device-management features. Verification and management are opposite trust models — verifyknot answers "is this attestation real and what does it prove," nothing about who owns what or where a device is.

This is a child of SIG-SPEC-005 and the consumer of everything the firmware spec produces. It aligns with PAT-020 §11 / FIG. 7 (verification flow), PAT-004 (LocalChain continuity), PAT-007 (combined session), and PAT-006 (offline evidence).

Requirement IDs: `VER-##`. Force: MUST / SHOULD / MAY.

---

## 1. Trust model and principles

- **VER-01 (MUST) Single trust anchor.** The only thing a verifier must obtain out-of-band and trust is the **YubiHSM civilian root public key**. Everything else in the chain is checked against it. The verifier MUST NOT require trusting ZKNOT's server, DNS, or TLS for the cryptographic verdict.
- **VER-02 (MUST) Offline-reproducible verdict.** The verdict MUST be computable entirely offline from a verification bundle (§8). The online path (`https://verifyknot.io/v/{code}`) is a *convenience* that fetches the same data; it MUST produce the identical verdict to an offline check, and the math MUST run client-side / be independently runnable (ship a small open verifier lib).
- **VER-03 (MUST) Manufacturer-independence.** Verification MUST NOT require contacting ZKNOT (PAT-006). The server may host data; it is never the authority on the verdict.
- **VER-04 (MUST) Honest translation.** The verifier's output MUST state exactly what was cryptographically proven and no more. A valid signature is not "a human was present"; presence is only proven if the presence-binding field supports it. A valid presence is not "the human approved this content"; that requires the content-binding field. The badge wording MUST map 1:1 to the proven facts (§5).
- **VER-05 (MUST) Registry ≠ verification surface.** Any identity/ownership/tracking data lives in the backend registry behind the API; the public verify response returns only what is needed to verify.

---

## 2. Inputs

- The **attestation record** (SIG-SPEC-005 §4 fields).
- The **certificate / attestation chain**: enclave signing key ← OPTIGA identity attestation (R-10) ← OPTIGA device cert ← YubiHSM root.
- A signed **approved-policy statement** (which firmware measurements / lifecycle states are acceptable), under the HSM root.
- (Redoubt) a signed **revocation statement / short-lived cert window**, under the HSM root.
- Optionally a full **offline verification bundle** (§8) bundling all of the above.
- Lookup key: the short code → `https://verifyknot.io/v/{code}`.

---

## 3. The verification algorithm (ordered)

Checks run in order; any MUST failure → fail closed with a specific, honest reason. Mirrors PAT-020 FIG. 7.

| ID | Check | Force |
|----|-------|-------|
| **VER-10** | Parse the record; validate `record_version` / `event_version` and schema. Unknown future version → say so, don't guess. | MUST |
| **VER-11** | Verify the **event signature** over the canonical record using the enclave signing public key. | MUST |
| **VER-12** | Verify the **identity-domain attestation** (R-10): the OPTIGA identity key certifies `{enclave_signing_pubkey, device_serial, firmware_hash, lifecycle}`. Binds the two domains. | MUST |
| **VER-13** | Verify the **chain to the HSM root** (VER-01): OPTIGA device cert chains to the YubiHSM civilian root. Determines the attestation tier (§5). | MUST |
| **VER-14** | Verify **firmware measurement + lifecycle** (R-11/R-16) against the signed approved-policy set: provisioned under an approved signing policy AND in a locked/debug-closed production state. A debug-open or unknown-measurement unit → flag, do not pass as flagship-grade. | MUST |
| **VER-15** | Evaluate the **two binding fields** (R-13 `presence_binding_type`, R-14 `content_binding_type`) independently against the caller's required minimum (§4). Never collapse to one rank. | MUST |
| **VER-16** | **Counter / replay:** verify `monotonic_counter` sanity; check the challenge against known-consumed state where available (online registry convenience) and/or rely on LocalChain continuity (VER-17). Offline verifiers cannot know *global* consumption — state this limitation honestly. | MUST |
| **VER-17** | **LocalChain continuity** (PAT-004): if a chain is presented, verify `prior_event_hash` linkage and ordering. | SHOULD |
| **VER-18** | **(Redoubt) signing-key validity window + revocation** at `physical_actuation_time`: the signing-key cert was within its validity window and not revoked when the actuation occurred. **Subject to the time-binding caveat (§7) — this check is only as strong as the trust in the actuation time.** | MUST (Redoubt) |
| **VER-19** | **Combined / multi-device session** (PAT-007): for a shared `session_id`, verify each participating device's signature independently and render **one badge row per device** (e.g., PV-A + ZKKey under one COMBINED_SESSION). Never assume a single signer. | MUST |
| **VER-20** | Verify `displayed_hash` / `short_code` (R-12) is the deterministic derivation of the signed record (the value a human could have read aloud matches what was signed). | SHOULD |
| **VER-21** | Produce a verdict + per-device honest badge set (§5). | MUST |

---

## 4. Two-field binding policy

The record declares enforcement on two **orthogonal** axes; the verifier reports both and lets the caller require a minimum on each. It MUST NOT reduce them to a single number, and MUST NOT treat firmware-trust as equal to secure-domain.

| `presence_binding_type` | meaning |
|--------------------------|---------|
| `secure-domain` | enforced in the enclave below replaceable firmware (flagship) |
| `hardware-interlock` | electrical interlock gated the signer (A′) |
| `firmware-mediated` | MCU firmware policy only (weak — self-asserted tiers) |
| `none` | no presence enforcement |

| `content_binding_type` | meaning |
|-------------------------|---------|
| `secure-domain-display` | the enclave owned the display; shown = signed (flagship moat) |
| `firmware-display` | display driven by ordinary firmware (rests on firmware trust) |
| `none` | signer never showed the content |

- **VER-22 (MUST)** Flagship WitnessMark = `(secure-domain, secure-domain-display)`. The verifier MUST surface anything weaker as weaker, in plain language.
- **VER-23 (MUST)** Default minimum for an unqualified public verify = report-only (show what was proven); a caller MAY require a minimum (e.g., evidentiary mode requires `secure-domain` + `secure-domain-display`) and the verifier fails closed below it.

---

## 5. Badge / output semantics (honest, per-device)

Three independent dimensions, never merged into one star rating:

**(a) Identity tier — how well the device is anchored:**
- `CA-ATTESTED` — cert chains to the HSM root (VER-13 passed). **GATED: do not render until the X.509 cert-chain provisioning SOP is confirmed in production.** SIG-FW-001 §6 *specs* the cross-cert, but spec ≠ shipped. Until confirmed, the maximum honest tier is `REGISTERED`.
- `REGISTERED` — the device public key is known to the ZKNOT registry, but full cert-chain attestation is not (yet) established.
- `SELF-ASSERTED` — unregistered / DIY unit (AP-0/AP-1 tiers); no ZKNOT anchoring claimed.

**(b) Binding badges — what was actually proven (from §4):** presence badge + content badge, each labelled at its true strength.

**(c) Assurance honesty line:** signing key = PSA-L3 (+ secret-erase); identity = EAL6+. Never imply the signing key is EAL6+/tamper-proof.

- **VER-24 (MUST)** Render **one badge row per device** (VER-19); device-ID prefix taxonomy ZK-K / ZK-A / PV-A / PV-C (subject to the device rename).
- **VER-25 (MUST)** The headline sentence MUST be the honest translation (VER-04). Example (flagship, all checks pass): *"Signed by device ZK-K-#### — a secure enclave that enforced a human press and showed the signer this exact content before signing; identity anchored to the ZKNOT root (EAL6+)."* If content-binding is weaker, the sentence drops the "showed the signer this exact content" clause.
- **VER-26 (MUST)** Failures are specific and honest: "signature valid but device not anchored to the ZKNOT root" ≠ "invalid." Distinguish *cryptographically invalid* from *valid-but-lower-assurance* from *unknown-policy*.

---

## 6. The verification surface stays minimal (the NOT list, enforced)

- **VER-27 (MUST)** The public verify response returns only: the verdict, the per-device badges, the proven facts, and the data needed to reproduce the check offline. It MUST NOT return owner identity, location, usage history, or any management/tracking field.
- **VER-28 (MUST)** No login/account is required to verify. No verification path is gated behind authentication.
- **VER-29 (SHOULD)** Registry-side identity/ownership data is reachable only through the separate authenticated API, never the verify surface.

---

## 7. Time-binding — the sharp residual in Redoubt revocation (decide before building VER-18)

Rotating/short-lived signing keys (Redoubt) only shrink blast radius **if the verifier can trust *when* the actuation happened.** The validity-window and revocation checks (VER-18) are evaluated at `physical_actuation_time` — but if that time is only device- or host-asserted, an attacker holding an extracted signing key can **backdate** an event into the key's valid window and defeat both checks. Naive rotation without a trustworthy time anchor is theater.

Levers, with honest tradeoffs (a decision is required):

- **A — trusted timestamp countersignature.** Bind an external timestamp-authority signature (or a LocalChain published checkpoint) into the record at signing/registration, so the actuation time is anchored to something the attacker can't move. *Cost:* requires connectivity or a periodic anchoring step; the field device may be offline at signing.
- **B — monotonic-ordering + revoke-after-detection.** Don't trust wall-clock; rely on the `monotonic_counter` and LocalChain ordering to bound *where in the sequence* an event sits, and on HSM-root revocation published the moment a unit is reported compromised. *Cost:* the guarantee becomes "events after the revocation checkpoint are rejected," not "events after the real-world compromise time."
- **C — registration-time anchoring.** The first time a record reaches the registry (online path), stamp a server-observed time under the HSM root; offline-at-signing is fine, but the anchor is "seen by registry at T," not "signed at T."

- **VER-30 (MUST)** The verifier MUST state which time basis a given verdict relied on, and MUST NOT present a window/revocation pass as stronger than the underlying time anchor. Revocation lists MUST be HSM-root-signed and offline-checkable.

---

## 8. Offline verification bundle (PAT-006)

- **VER-31 (MUST)** A bundle MUST contain everything needed for a zero-contact verdict: the record, the full chain to the HSM root, the HSM root public key (the user still confirms this out-of-band — VER-01), the signed approved-policy statement, and (Redoubt) the revocation/window snapshot + any time anchor.
- **VER-32 (SHOULD)** The bundle is the canonical export; the online `/v/{code}` path assembles the same bundle server-side and runs the same client-side verifier, so online and offline verdicts are identical (VER-02).

---

## 9. Alignment with existing infrastructure

- API: FastAPI at `api.zknot.io` — `POST /v1/attest`, `GET /v1/verify/{code}`; PostgreSQL registry; ZK-LocalChain in production (first record ZK-6GUA-7DV, COMBINED_SESSION, chain pos 0, integrity verified).
- Frontend: static `verifyknot-site` on Cloudflare Pages; live URL form `https://verifyknot.io/v/{code}`.
- **VER-33 (MUST)** The verdict logic ships as a client-reproducible verifier (the math runs client-side / is independently runnable), not as a server-only "trust us" endpoint — this is VER-02 made concrete against the current stack.
- **VER-34 (MUST)** The verify page renders a **badge row per device** (already a known requirement) — do not regress to a single-signer assumption.

---

## 10. Honesty constraints (carried from SIG-SPEC-005 / SIG-FW-001)

- Do **not** render `CA-ATTESTED` until the cert-chain provisioning SOP is confirmed in production; `REGISTERED` is the ceiling until then.
- Signing key = PSA-L3; identity = EAL6+; gate = immutable-firmware-enforced, not silicon-impossible.
- A signature proves only what the two binding fields say — the output wording must not exceed them.
- No FIPS claims without live NIST CMVP verification.
- Lab-grade signing-key extraction is out of v1 scope (stated, not hidden); Redoubt narrows but does not eliminate the window (§7).

---

## 11. Open items / verify-before-build

1. **Time-binding decision (§7) — gates VER-18.** Pick A / B / C (or a blend) before Redoubt revocation is meaningful. This is the single most consequential open question in this spec.
2. **CA-ATTESTED gating:** confirm the cert-chain provisioning SOP in production before the badge is allowed to render (memory flag, now spec'd in SIG-FW-001 §6 but unconfirmed).
3. **Approved-policy distribution:** how the signed approved-firmware-measurement set is published and updated under the HSM root (so VER-14 is checkable offline).
4. **Revocation list format** (HSM-root-signed, offline-checkable) and its distribution.
5. **HSM-root trust bootstrap:** how a first-time verifier obtains the root public key out-of-band (the one unavoidable trust step — make it auditable).
6. **Bundle format** (VER-31) and the client verifier lib language/packaging.
7. Device-ID prefix taxonomy may change with the device rename (WitnessMark).

---

## 12. Patent alignment

This verification flow instantiates PAT-020 §11 / FIG. 7 (verify signature → device cert → identity-domain cert → firmware/assurance → counter → uniqueness → event hash → chain continuity → offline verdict), PAT-004 (LocalChain continuity, VER-17), PAT-007 (combined session, VER-19), and PAT-006 (offline verification, §8). Keep the as-built verifier consistent with these disclosures.

---

## 13. Changelog

| Version | Date | Change |
|---------|------|--------|
| SIG-VER-001 v0.1 | 2026-06-08 | Initial verifier spec (gate #4): trustless/offline verdict model; single HSM-root trust anchor; ordered verification algorithm (VER-10..21); two-field binding policy; honest per-device badge taxonomy with CA-ATTESTED gating; NOT-list enforcement; Redoubt revocation with the time-binding residual surfaced (§7); offline bundle (PAT-006); alignment to api.zknot.io / ZK-LocalChain / verifyknot.io. |

*Child of SIG-SPEC-ZKKEY-005. Provenance: verification logic derived from the locked architecture and PAT-020 §11/FIG.7, PAT-004, PAT-006, PAT-007, plus existing verifyknot infrastructure. Honest-translation discipline (VER-04) is the spec's spine: the verifier says exactly what was proven and no more.*
