---
title: verifyknot — Purpose, Critical Capabilities & Scope Boundary
system: verifyknot
status: active
created: 2026-06-05
owner: Shane
---

# verifyknot — Purpose, Critical Capabilities & Scope Boundary

## One-sentence job (the whole discipline)

> **verifyknot exists so a skeptical third party — present nowhere, trusting no one — can turn a code or artifact into an independently re-checkable answer about whether a ZKNOT attestation is authentic and what it actually claims.**

If describing verifyknot's job ever takes two sentences, it has been overloaded. Stop and cut back to this one.

It is for **third-party verification of evidence/attestations**. It is **not** for information tracking. (See the "not" list.)

## Critical capabilities — the irreducible four

Test for "critical": remove it, and the one-sentence job fails. Only these four pass.

1. **Resolve** — a code or QR maps to the correct signed record.
2. **Verify in the open** — check the signature and hash chain against published keys, ideally re-runnable by the verifier themselves (client-side, or downloadable artifact + open verifier). *This is the load-bearing one:* the VERIFIED badge's authority must come from math the stranger can re-check, not from verifyknot's say-so.
3. **Disclose honestly** — show exactly what the attestation does and does not claim: self-asserted vs. ZKNOT-provisioned; manufacture record vs. signed session vs. combined session. The "what a claim is and isn't" candor, as a feature.
4. **Anchor trust** — publish the public keys, so the root of trust is not "the website told me."

Everything else is optional and waits for demand to pull it.

## The "not" list (maintained refusal list)

Scope creep is a missing refusal list, not a willpower problem. verifyknot must **not** become:

- A login-gated app. If you must trust an account to get an answer, it has failed its job.
- A CRM, asset tracker, or info-management surface.
- The system of record.

## Why info-tracking keeps tempting (structural, not a flaw)

The records are already sitting in the backend, so "let me also browse and manage them here" feels free. But verification and management are **opposite trust models**:

- Verification's entire value is being *trust-minimized*.
- Management requires *privileged trust*.

Bolt management onto the verification surface and you erode the one property that made verifyknot worth building.

## The boundary question (single yes/no router)

For any proposed verifyknot feature, ask:

> **"Does this help a stranger check a claim without trusting us?"**
> - **Yes** → it may belong in verifyknot.
> - **It helps *us* store / manage / track instead** → backend, not verifyknot.

## Same data, two surfaces

| Surface | Trust model | Access | Role |
|---|---|---|---|
| **Registry + ZK-LocalChain** (backend) | Trusted | Full CRUD | System of record. Info tracking lives here. |
| **verifyknot** | Trust-minimized | Read-only | Thin public window onto the verifiable subset. |

## End state

A thin, durable, read-only verification spine shared by every ZKNOT product (PowerVerify, ZKey, TrustSeal, …): enter code / scan QR → see the signed record + disclosed claim scope + fingerprint → re-checkable VERIFIED, anchored to published keys. Bootstrapped on the cheapest product; resists gold-plating for any single one.
