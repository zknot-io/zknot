# 2026-05-29 — /protocol & /docs pages: technical content shipped

**Status:** Both pages built, theme-consistent, committed locally. NOT yet pushed/deployed (site repo branch is ahead of origin). Outstanding decisions tracked below.

---

## What shipped

Replaced the marketing bodies of `zknot.io/protocol` and `/docs` with technical content written for a skeptical applied cryptographer. Both pages:

- Lead with assumptions and an explicit "what this does NOT protect against" section (Protocol §6) rather than absolutes.
- Use real primitives: ECDSA P-256 over a SHA-256 `challenge_hash`; tamper-evident hash-linked LocalChain (NOT zero-knowledge — "ZK" = ZKNOT).
- Docs routes every hard question (human? relay? ZK?) straight to Protocol §6 instead of dodging.

Mechanics: each page is static HTML with per-page inline CSS and a hand-duplicated nav/footer (no shared component). Content was delivered as a self-contained `<main>` block with **namespaced** scoped styles (`.zk-protocol` / `.zk-docs`) so it can't collide with the page's own CSS, then spliced between the existing `</nav>` and `<footer>` via a non-destructive `.new` file → eyeball → `mv` pattern.

docs.html's original shell rendered unstyled (white/Times), so it was **rebuilt from protocol.html's working dark-themed shell** + the docs body. Anchor `id`s (`#localchain`, `#zkkey`, `#powerverify`, `#schema-artifact`, `#schema-device-sig`) were preserved so inbound deep-links from other pages resolve.

---

## Decisions locked

- **ZK = ZKNOT**, always. Never use "zero-knowledge" in prose — the chain is verified with SHA-256 + ECDSA P-256 and walked position-by-position; there is no ZK proof system.
- **PUF is optical** (photo-vs-baseline, PowerVerify only). `puf/enroll` + `puf/verify` both take a multipart photo; the match is **server-side** (secret baseline + server matcher), so it is NOT offline-checkable.
- **Client-side checkability:** signature + short code are checkable offline with only SHA-256 + ECDSA P-256 (no proprietary lib). **Freshness is the single property that requires the issuer** or an out-of-band signal. Chain via `POST /v1/chain/verify`.
- **All patents filed:** PAT-001 (provisional #63/960,933, FSM-gated core), PAT-004 (LocalChain), PAT-005 (attestation ingest), PAT-010 (short-code verification).

---

## Architecture facts pinned (from live OpenAPI v0.3.0)

- **Secure element = ATECC608B** (`device_id` = serial burned into it). Currently written GENERIC ("hardware secure element") on the public docs — naming decision pending (see Open items).
- **ArtifactType enum:** `ZKEY_SIGN`, `POWER_SESSION`, `TRUST_SEAL`, `COMBINED_SESSION`, `POWERVERIFY_UNIT`.
- `session_id` binds a `POWER_SESSION` + `ZKEY_SIGN` into a `COMBINED_SESSION`.
- **Chain-link fields:** `entry_hash` (this record) ← `chain_prev_hash` (next record commits to it); `chain_position` (index; null prev at 0).
- **Endpoints:** `POST /v1/attest`, `GET /v1/verify/{code}`, `POST /v1/chain/verify`, `POST /v1/units/provision`, `/{short_code}/register`, `/{short_code}/puf/enroll`, `/{short_code}/puf/verify`.
- **Short codes (PAT-010 §3):** client-authoritative `XXXX-XXXX-XXXX` (derivable from artifact, no server) and server-derived `ZK-XXX-XXXX`; verify accepts either + raw UUID.
- Emails: **ops@zknot.io** (technical/security), **support@zknot.io** (consumer/verifyknot).

---

## Live-site map (the stuff that evaporates)

- **Deploy repo:** `~/zknot-site`, serves `public/`. Cloudflare Pages (`wrangler.jsonc`, `_redirects`). Remote `git@github-zknot:zknot-io/zknot-site.git`. (Decoys: `~/Desktop/zknot.io` = stale Jan copy; `~/code-review/zknot-site` = HTTPS review clone; `zknot-org-site` / `procedures-zknot-org-site` = different repo, `wrangler.toml`.)
- **Static HTML; inline CSS per page; nav + footer hand-duplicated** across every page — there is no shared nav component. Changing nav site-wide = editing N files (or a backed-up `sed`).
- **Splice boundaries used:** protocol.html `</nav>`=471, `<footer>`=1023. docs.html original 329/864 (now stale — docs.html was rebuilt from protocol's shell).
- **Backups:** `~/zknot-site/.nav-backup/` (gitignored) — pre-hide originals of all pages + `*.prebody` copies.

---

## Commits

- `be3267f` protocol: marketing body → technical spec
- `f150527` protocol: title fix (meta description fixed later)
- `9bca849` docs: publish technical page; restore /docs nav; +.gitignore
- **PENDING:** docs v2 (real schemas + `puf/verify`, dark theme) + protocol meta fix → then `git push` / `wrangler pages deploy public`

---

## Open items

- [ ] **ATECC608B disclosure:** name the SE on docs (analyzability, cryptographers respect it) vs. keep generic (less §6.4 attack-surface signal; matches chip-agnostic patent framing).
- [ ] **EvidenceProtocol™:** other pages (law-enforcement.html etc.) still use the TM in CTAs. Decide whether deep/technical pages keep it.
- [ ] **Relay / distance-bounding layer** — add or deliberately scope out (Protocol §6.2, §11).
- [ ] **Optical-PUF capture-liveness / anti-spoof** posture (§6.5, §11).
- [ ] Inline remaining API schemas (`VerifyResponse`, `ChainVerifyResponse`, `ProvisionRequest`) — currently pointed at `openapi.json`.
- [ ] **Push + deploy** — site commits are local only.
- [ ] verify.html footer labels the link "API Docs" — fine now that docs is live, but note the label inconsistency.

---

## Concepts load (cumulative — tick as they solidify)

### Cryptographic / protocol
- [ ] Post-nonce **temporal ordering** vs. nonce-as-entropy (human action proves ordering, not entropy)
- [ ] FSM-gating: signable state reachable only after challenge-display → actuation
- [ ] **Freshness / anti-replay** = single-use challenge + verifier-side window enforcement
- [ ] Pre-computation resistance (follows from freshness + ordering)
- [ ] **WYSIWYS** / trusted display path (shown == signed)
- [ ] **Mafia-fraud / real-time relay** and why distance-bounding is the only defense
- [ ] Secure-element threat envelope: decapsulation, fault injection, side-channel
- [ ] Optical/physical-fingerprint **PUF**: presentation/spoof attacks, false-accept rate, baseline-as-secret
- [ ] Why optical-PUF verify is **structurally server-side** (secret baseline + server matcher)

### ZKNOT system specifics
- [ ] **ECDSA P-256 + SHA-256** as the offline-verifiable core (NOT zero-knowledge)
- [ ] Tamper-evident hash-linked log vs. a real ZK proof system (statement, soundness, ZK property)
- [ ] Hash-link in practice: `entry_hash` ← `chain_prev_hash`, `chain_position`
- [ ] Client-authoritative vs. server-derived short codes (PAT-010)
- [ ] The **verification split**: signature + code offline; freshness server-bound; chain via `/v1/chain/verify`; optical match server-side
- [ ] ArtifactType taxonomy and `session_id` binding (COMBINED_SESSION)
- [ ] Patent map: PAT-001/004/005/010 and what each covers

### Ops / tooling techniques (earned this arc)
- [ ] **Namespaced/scoped CSS** as a splice-safety technique
- [ ] Non-destructive edit pattern: write `.new` → eyeball → `mv`
- [ ] `<title>` / `og:` / `meta description` are separate from on-page `<h1>` (they drift if you only edit the body)
- [ ] Per-file splice boundaries — each page has its own nav/footer line numbers; never reuse
- [ ] `git restore` (uncommitted) vs. `sed` swap (committed) as two different un-hide paths
- [ ] Anchor `id`s preserving inbound deep links
- [ ] **`components.schemas`** as the source of truth for field-level API docs (vs. inferring/inventing)
- [ ] Committing only genuinely-changed files (restored files fall out of the commit automatically)
- [ ] Reusing a known-good page shell to fix a theme mismatch (cheaper than reverse-engineering the broken one)
- [ ] Named-part-vs-generic **disclosure tradeoff** (analyzability vs. attack-surface signaling)

---

## Note to self

The honesty is the asset. A `/protocol` page that names its own relay gap and optical-PUF spoof surface is the artifact that earns a second read from Green / Schneier / Pfefferkorn — the pages don't oversell, so the claims that remain are believable. The personal monopoly here isn't the device; it's the credibility of describing it plainly. Carry that tone into the outreach drafts.
