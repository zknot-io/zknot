# HASHSTAMP — Project Handoff

**Document ID:** HASHSTAMP-HANDOFF-001
**Version:** 1.0
**Date:** 2026-05-22
**Author:** William Shane Wilkinson
**Purpose:** Complete ground-truth for the Hashstamp product. Paste-able into a fresh
AI thread as context. If a future session contradicts this doc, this doc wins unless
explicitly revised.

Page 1 of 6

---

## 1. What Hashstamp is

A document-timestamping / proof-of-delivery SaaS for freelancers and agencies. Tagline:
**"Prove what you delivered, and when."** A user uploads a file; it's hashed locally in
their browser; the hash is signed and recorded on the ZKNOT chain; they get a short ZK
code and a public verification link their client can check independently — no account,
no login, no trust in the user required.

**Brand decision:** Hashstamp is a SEPARATE brand from ZKNOT, deliberately. zknot.io is
heavy federal/evidence-toned (contracting officers, law enforcement, election integrity).
That tone repels the freelancer buyer. Hashstamp is light, cheap, self-serve, on its own
domain, with only "Powered by ZKNOT" in the footer. Do not merge the two brands.

**Pitch angle:** specific hook ("a client can never dispute what you sent or when"),
broad capability underneath ("any file you can upload — contracts, designs, code, etc.").

**Status as of 2026-05-22:** LIVE and fully working end-to-end at hashstamp.io.

Page 2 of 6

---

## 2. Architecture (as deployed)

```
  Browser (hashstamp.io — Cloudflare Pages, static index.html)
    │  user drops a file
    │  SHA-256(file) computed locally via Web Crypto API  ← file NEVER uploads
    │  POST { hash, filename }  (JSON)
    ▼
  Cloudflare Worker  (hashstamp-worker.shane-systems.workers.dev)
    │  holds Hashstamp service private key (Worker secret)
    │  challenge_hash = SHA-256(fileHashBytes)
    │  signature = ECDSA-P256 sign of fileHashBytes (WebCrypto SHA-256s it → challenge_hash)
    │  builds ArtifactIngest, POST → api.zknot.io/v1/attest
    │  returns { ok, zk_code, verify_url, chain_position, signed_at, file_sha256, filename }
    ▼
  api.zknot.io  (existing FastAPI on Railway)
    │  verify_signature() PREHASHED against pubkey + challenge_hash
    │  appends to ZK-LocalChain, returns short_code + chain_position
    ▼
  Browser shows receipt + "Open verification page →"  →  https://verifyknot.io/{code}
  verifyknot.io resolves the public record (VERIFIED — CHAIN INTACT).
```

**Why the Worker exists (not browser → API directly):** /v1/attest REQUIRES a real ECDSA
signature (artifact_id, artifact_type, device_id, challenge_hash, signature, public_key,
signed_at). A browser has no signing key. The Worker holds the Hashstamp service key and
signs server-side. The file's hash is what's unique per stamp; Hashstamp's key is the
consistent attesting authority.

Page 3 of 6

---

## 3. The signing detail (CRITICAL — don't "fix" it without understanding it)

The API verifies PREHASHED: `pubkey.verify(der_sig, digest, ec.ECDSA(Prehashed(SHA256())))`
where `digest = bytes.fromhex(challenge_hash)`. It treats challenge_hash AS the digest and
does NOT re-hash it.

WebCrypto's `crypto.subtle.sign({name:"ECDSA",hash:"SHA-256"}, key, INPUT)` computes
SHA-256(INPUT) internally, then signs. WebCrypto cannot do raw/prehashed ECDSA.

To make both sides agree on the same 32 bytes:
- Worker feeds WebCrypto the **fileHashBytes** (the raw SHA-256 of the file, 32 bytes)
- WebCrypto signs **SHA-256(fileHashBytes)**
- Worker sends **challenge_hash = SHA-256(fileHashBytes)** to the API
- API verifies prehashed against challenge_hash = SHA-256(fileHashBytes) → identical → valid

**Consequence:** the on-chain challenge_hash is the DOUBLE hash (SHA-256 of the file hash).
The REAL document fingerprint (SHA-256 of the file) lives in `metadata.file_sha256`. The
user verifies their file against metadata.file_sha256, NOT challenge_hash. This is honest
but indirect; the clean fix is the /v1/timestamp route (section 6).

artifact_type is **COMBINED_SESSION** (an existing enum value) because DOCUMENT_TIMESTAMP
isn't in the API's ArtifactType enum yet. Adding it is part of the fast-follow.

Page 4 of 6

---

## 4. Deployment specifics (exact, reproducible)

**Domain:** hashstamp.io — owned, already a zone in the Cloudflare account
(Shane.systems@gmail.com, account ID 7b0e854973bf365b412d2f6ec53ffdeb). Custom domain
attached to the `hashstamp` Pages project (one-click since the zone is in-account).

**Frontend (Cloudflare Pages, project `hashstamp`):**
- Deploy from CLI (NOT dashboard drag-drop — that 404'd):
  ```
  mkdir -p ~/hashstamp-site && cp index.html ~/hashstamp-site/
  wrangler pages deploy ~/hashstamp-site --project-name=hashstamp
  ```
- index.html has WORKER_URL hardcoded = https://hashstamp-worker.shane-systems.workers.dev
- FORM_ENDPOINT is EMPTY (reserve emails log to console only — wire before traffic)

**Worker (`hashstamp-worker`):**
- Code: ~/hashstamp-worker/hashstamp-worker.js ; config wrangler.toml
- Deploy: `wrangler deploy` (from ~/hashstamp-worker)
- Bindings:
  - HASHSTAMP_PUBLIC_KEY_HEX (var) = cccb34a751ccb1c95f925dfe955555f542d7beb2712aa0af482898fadc3adbb358c662f73c1d9c864c6077b30709bbdbae5e56bf6995cd27af92ae8213211ac0
  - HASHSTAMP_DEVICE_ID (var) = HASHSTAMP-SVC-01
  - HASHSTAMP_PRIVATE_KEY_PKCS8 (secret) — set via:
    `wrangler secret put HASHSTAMP_PRIVATE_KEY_PKCS8 < ~/zknot-provision/hs_priv_pkcs8.pem`

**Keys (~/zknot-provision/, KEEP OFF GIT):**
- hs_priv.pem (EC private), hs_priv_pkcs8.pem (PKCS#8 for the Worker secret)
- Regenerate reference:
  ```
  openssl ecparam -name prime256v1 -genkey -noout -out hs_priv.pem
  openssl pkcs8 -topk8 -nocrypt -in hs_priv.pem -out hs_priv_pkcs8.pem
  openssl ec -in hs_priv.pem -pubout -outform DER \
    | python3 -c "import sys;print(sys.stdin.buffer.read()[-64:].hex())"   # pubkey X||Y
  ```

**Node/wrangler gotcha:** wrangler needs Node >=22. Box default is v20. Per NEW shell:
`export NVM_DIR="$HOME/.nvm"; [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"; nvm use 22`
(Add those lines to ~/.zshrc to make it automatic.)

**verifyknot.io path:** resolves BARE codes at verifyknot.io/{code}. The /v/{code} path
does NOT work for Hashstamp (the verify page passes the whole post-domain segment as the
code). Worker's verify_url MUST be "https://verifyknot.io/" + shortCode (no /v/).

Page 5 of 6

---

## 5. Test / verification procedure

Direct Worker test (from a machine that can reach the Worker):
```
curl -sS -X POST "https://hashstamp-worker.shane-systems.workers.dev" \
  -H "Content-Type: application/json" \
  -d '{"hash":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","filename":"test.txt"}' \
  | python3 -m json.tool
```
Expect: ok:true, a zk_code, verify_url, chain_position.

API record check:
```
curl -sS "https://api.zknot.io/v1/verify/ZK-XXXX-XXX" | python3 -m json.tool
```
(Use the bare code, no v/ prefix.) Expect verified:true.

Full UI test: open hashstamp.io → "Stamp a file right now" → drop a file → get ZK code →
click verify → verifyknot.io shows VERIFIED — CHAIN INTACT.

Known-good production records: ZK-54WE-XLA (pos 26), ZK-PWJL-KQZ (pos 28).

Page 6 of 6

---

## 6. Fast-follow backlog (market mode, next week)

Priority order:

1. **`/v1/timestamp` API route** (the big one). A Python route that:
   - accepts a document hash directly (no signature needed from caller, or its own auth)
   - signs with TRUE prehashed ECDSA (Python can; challenge_hash = the file hash itself)
   - adds a DOCUMENT_TIMESTAMP artifact_type to the enum
   - eliminates the double-hash; the on-chain challenge_hash becomes the real file fingerprint
   - lets the Worker get simpler (or be retired in favor of direct browser→API for the hash)
   - natural home for rate limiting

2. **Freelancer-legible verify view.** Either a Hashstamp-branded verify page or a mode on
   verifyknot.io that shows "📄 filename — SHA-256 — stamped at — VERIFIED" instead of the
   ZKNOT generic chain fields (COMBINED_SESSION, challenge_hash, etc.).

3. **Lock down the Worker.** ALLOWED_ORIGIN = "https://hashstamp.io" (currently "*"), add
   rate limiting so the open endpoint can't be spammed onto the chain. Retest after.

4. **Wire reserve email capture.** Set FORM_ENDPOINT in index.html (Formspree or a Worker
   route storing {email,intent}). Currently logs to console only.

5. **Pricing test.** Page shows $12/mo placeholder. The reserve-button click-through is the
   willingness-to-pay signal — only meaningful once #4 captures it.

6. **Distribution.** The real bottleneck. Where to post to get the first 50-100 freelancers
   in front of it; how to avoid self-promo bans; measure reserve clicks.

---

## 7. One-paragraph context for a cold AI thread

"Hashstamp is a live document-timestamping SaaS for freelancers (hashstamp.io), built on
ZKNOT's existing api.zknot.io + verifyknot.io + ZK-LocalChain. Browser hashes a file
locally, a Cloudflare Worker (holding a dedicated Hashstamp ECDSA-P256 service key) signs
the hash and records it via /v1/attest, the user gets a ZK code + a verifyknot.io link.
It works end-to-end. Key quirk: WebCrypto can't do prehashed ECDSA, so the Worker signs
the file-hash bytes and stores the real file fingerprint in metadata.file_sha256 while the
on-chain challenge_hash is the double-hash; the clean fix is a /v1/timestamp Python route.
artifact_type is COMBINED_SESSION until a DOCUMENT_TIMESTAMP enum is added. The Worker is
currently open with wildcard CORS. Next work is market-mode: the /v1/timestamp route, a
freelancer-legible verify view, locking down the Worker, wiring reserve email capture, and
distribution."

---

*ZKNOT, Inc. — Hashstamp is a ZKNOT product. When physics is policy, trust is optional.*
