# 2026-05-22 — Hashstamp: shipped a live document-timestamping product in one day

**Author:** William Shane Wilkinson
**Workstream:** sw / biz
**Status:** LIVE at hashstamp.io — full end-to-end working

---

## Summary

Built and shipped Hashstamp — a freelancer-facing document-timestamping / proof-of-delivery
SaaS — from zero to live on its own domain in a single session, on top of the existing
ZKNOT attestation infrastructure (api.zknot.io + verifyknot.io + ZK-LocalChain).

A user drops a file -> it's SHA-256 hashed in the browser (file never uploads) -> a
Cloudflare Worker signs the hash with a dedicated Hashstamp service key -> calls the
existing /v1/attest -> the record lands on the live chain -> the user gets a ZK code and a
public verifyknot.io link their client can independently check.

First production stamps on chain: position 26 (ZK-54WE-XLA), position 28 (ZK-PWJL-KQZ),
both VERIFIED with chain integrity confirmed.

---

## Why a separate brand (decision)

zknot.io is pitched at federal/defense/evidence buyers (contracting officers, election
integrity, law enforcement, forensic journalism). That heavy tone works against a cheap,
self-serve product for freelancers. Decision: Hashstamp is a separate standalone brand on
its own domain (hashstamp.io, already owned + in Cloudflare), with only a quiet
"Powered by ZKNOT" in the footer. Pitch angle: specific hook ("Prove what you delivered,
and when") with broad capability underneath ("any file you can upload"). Name chosen:
hashstamp.io (.io available, pronounceable, freelancer-native "stamp" metaphor).

---

## Architecture (shipped)

Browser (hashstamp.io, Cloudflare Pages)
  -> SHA-256(file) computed locally via Web Crypto (file never leaves device)
  -> POST {hash, filename} to the signing Worker
Cloudflare Worker (hashstamp-worker.shane-systems.workers.dev)
  -> holds Hashstamp service key (Worker secret)
  -> signs, builds ArtifactIngest payload, POSTs to api.zknot.io/v1/attest
  -> returns {zk_code, verify_url, chain_position, signed_at}
Browser shows receipt + verify link -> verifyknot.io/{code} resolves the public record.

Key model: a FRESH ECDSA P-256 service key, separate from the ZKNOT signing device
(ZK-EW6E-EERX). Blast-radius isolation + honest provenance ("signed by Hashstamp's key").

---

## Four bugs hit and fixed (the real work)

1. **Prehashed signature mismatch.** WebCrypto's subtle.sign({hash:"SHA-256"}, key, INPUT)
   hashes INPUT then signs. The API verifies PREHASHED (treats challenge_hash as the digest:
   ec.ECDSA(Prehashed(SHA256)) at crypto.py:193). First Worker version signed the already-
   computed challenge bytes -> double-hash -> "signature does not match." FIX: feed WebCrypto
   the fileHashBytes and set challenge_hash = SHA-256(fileHashBytes). Then WebCrypto signs
   SHA-256(fileHashBytes), which equals challenge_hash, which the API verifies prehashed.
   Same 32 bytes both sides. (Verified the logic in Python before redeploy.)

2. **Node 22 wall.** wrangler 4.94 requires Node >=22; box had v20. Installed nvm, `nvm install 22`.
   Gotcha: nvm only applies to the shell it ran in — NEW terminals revert to system v20.
   Reload with: `export NVM_DIR="$HOME/.nvm"; [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"; nvm use 22`

3. **Pages upload 404.** Dashboard drag-and-drop produced a deployment that 404'd at root
   (file nested or didn't register). FIX: deploy via CLI from a clean folder containing only
   index.html: `wrangler pages deploy ~/hashstamp-site --project-name=hashstamp` — uploads
   contents to site root deterministically.

4. **verify_url /v/ path bug.** Worker returned verifyknot.io/v/{code}, but verifyknot.io's
   verify page takes the WHOLE post-domain path as the code (it showed "V/ZK-PWJL-KQZ" in the
   box -> "Not Found"). verifyknot.io resolves BARE codes at verifyknot.io/{code}. FIX:
   verify_url = "https://verifyknot.io/" + shortCode (dropped /v/). Confirmed by curl:
   bare code -> verified:true; "v/CODE" -> Not Found.

---

## Current deployed state

- **Frontend:** Cloudflare Pages project `hashstamp`, custom domain hashstamp.io (live).
  WORKER_URL baked into index.html = https://hashstamp-worker.shane-systems.workers.dev
- **Worker:** hashstamp-worker, version e6ef93ed / 957d9ab0 (final). Bindings:
  HASHSTAMP_PUBLIC_KEY_HEX (var), HASHSTAMP_DEVICE_ID="HASHSTAMP-SVC-01" (var),
  HASHSTAMP_PRIVATE_KEY_PKCS8 (secret).
- **Chain:** Hashstamp records use artifact_type COMBINED_SESSION (until DOCUMENT_TIMESTAMP
  enum added). file_sha256 stored in metadata.file_sha256. Positions 26 & 28 are Hashstamp.

---

## Known limitations / fast-follow (for market mode next week)

1. **Verify page shows ZKNOT generic fields**, not a freelancer-legible "file + time" view.
   challenge_hash on the record = SHA-256(file_hash) (the double-hash), real fingerprint is in
   metadata.file_sha256. CLEAN FIX: a proper `/v1/timestamp` Python API route doing TRUE
   prehashed signing (challenge_hash = the file hash directly) + a DOCUMENT_TIMESTAMP artifact
   type + a Hashstamp-specific verify view ("filename / SHA-256 / stamped at / verified").
2. **Worker is open + CORS wildcard.** Anyone can POST and write to the chain. Add rate
   limiting and set ALLOWED_ORIGIN = "https://hashstamp.io" (then retest the stamp tool).
3. **Reserve email capture not wired.** FORM_ENDPOINT in index.html is empty (logs to console).
   Set to a Formspree URL or a Worker route before driving traffic to the reserve button.
4. **Double-hash is honest but indirect.** Removed entirely by the /v1/timestamp route.

---

## Distribution (the actual bottleneck, deferred to market mode)

The product is the easy part; getting freelancers to look at it is the open question.
User is in "developer mode" this week, "market mode" next week. When that starts: where to
post (r/freelance, freelancer Discords/Slacks, Indie Hackers, DM 10 known freelancers),
how to not get banned for self-promo, and measuring reserve-button click-through.

---

## Files (in this session's outputs, also ~/hashstamp-worker, ~/hashstamp-site)

- index.html (landing page + working stamp tool; WORKER_URL baked in)
- hashstamp-worker.js (signing Worker, final fixed version)
- wrangler.toml (Worker config; pubkey hex filled in)
- Keys: ~/zknot-provision/hs_priv.pem, hs_priv_pkcs8.pem (SECRET, off git)
  Public key hex: cccb34a751ccb1c95f925dfe955555f542d7beb2712aa0af482898fadc3adbb358c662f73c1d9c864c6077b30709bbdbae5e56bf6995cd27af92ae8213211ac0

---

*ZKNOT, Inc. — Hashstamp is a ZKNOT product. Shipped 2026-05-22.*
