# ZKNOT Session Handoff — 2026-05-20

**Author:** William Shane Wilkinson (with AI engineering assistance)
**Session duration:** ~7 hours
**Branch state:** All work pushed to `main` on `zknot-io/zknot-api` and `~/ZKNOT/` vault.
**Production status:** api.zknot.io v0.3.0 deployed and serving real verification.

---

## TL;DR

Today closed the largest open security gap in the ZKNOT platform: the production
API at `api.zknot.io` was running a *placeholder* signature verifier
(`verify_signature_placeholder` returning `True` for any non-empty input). This
contradicted the core verifiability claims of PAT-001, PAT-005, and PAT-010.

The placeholder is now replaced with real ECDSA P-256 verification. Nine
production PowerVerify Rev 0 artifacts are publicly verifiable end-to-end at
`https://verifyknot.io` and `https://api.zknot.io/v1/verify/{code}`. The
chain has 19 entries: 1-10 are pre-fix (with position 10 as a deliberately
preserved forensic audit witness), 11-19 are post-fix legitimate units.

The acquisition-relevant deliverable: **the patent portfolio is no longer
provisional applications with paper claims — there is a working
end-to-end implementation in production that any acquirer's technical team can
verify in 60 seconds without any access to internal systems.**

---

## What changed in production

### 1. Real ECDSA P-256 signature verification (PAT-001 §4.5 / PAT-005 §3.2)

**File:** `app/services/crypto.py` (full rewrite)

The pre-existing `verify_signature_placeholder` function was:

```python
def verify_signature_placeholder(signature, public_key, challenge_hash):
    if not signature or not public_key or not challenge_hash:
        return False
    # ... comment about production implementation ...
    return True   # <-- accepted ANY non-empty input
```

This was replaced with `verify_signature()` that performs real ECDSA P-256
validation using `cryptography.hazmat.primitives.asymmetric.ec` and the
Prehashed semantics required by both v1 (raw challenge bytes) and v2 (canonical
record-hash) signing schemes.

Key design decisions:

- **64-byte X||Y public keys** accepted, plus optional `0x04` SEC1 uncompressed-point
  prefix (65 bytes total) for ATECC608B compatibility.
- **64-byte raw r||s signatures** parsed and converted to DER for the
  `cryptography` library's verify call.
- **Explicit error types**: `InvalidPublicKey`, `InvalidSignatureFormat`,
  `SignatureMismatch`. Each raises with a specific reason ("public key point is
  not on SECP256R1", "signature must be 64 bytes (r||s); got 65 bytes", etc.)
  rather than collapsing all failures into a generic "invalid signature".
- **Prehashed-mode verification.** Since v2 artifacts sign the SHA-256 of a
  canonical JSON record (not raw bytes), and v1 artifacts sign the SHA-256 of
  raw challenge bytes, both reduce to "verify a P-256 signature over a 32-byte
  digest". Using `ec.ECDSA(Prehashed(hashes.SHA256()))` handles both cases
  uniformly.
- **Backward-compat shim**: `verify_signature_placeholder` still exists,
  forwards to `verify_signature`, emits a `DeprecationWarning`. To be removed
  in v0.4.0.

**Tests:** `tests/test_crypto_verification.py` (19 cases). Covers happy path
for both v1 and v2, tamper detection (signature, hash, pubkey, record field),
malformed inputs (each with its specific error type), and the deprecation shim.

### 2. Client-authoritative short codes (PAT-010 §3)

**File:** `app/services/attestation.py`

Previously the server derived its own short code from `signature + artifact_id`
in a 7-char `ZK-XXX-XXXX` format. Our v2 Device SDK, however, computes a
deterministic 12-char `XXXX-XXXX-XXXX` short code from the canonical record
hash and stamps it on the physical unit's label *before* the artifact is ever
pushed to the API.

The mismatch meant: a customer with a unit labeled `501C-LPR0-FSAC` would type
that into verifyknot.io, but the API had stored it under a totally different
server-derived code like `ZK-9VER-GYU`. Public verification was broken by
design.

The fix: the `_resolve_short_code()` helper now honors `metadata.zk_code` when
provided by the client and stores it verbatim. Falls back to server-derived
codes only for legacy artifacts that didn't provide one (backward compatible).

Storage source is logged for audit visibility (`source=client` or
`source=server-derived`).

### 3. Idempotent duplicate handling

**File:** `app/services/attestation.py`, `app/routers/attest.py`

Previously POST `/v1/attest` returned HTTP 409 if the same `artifact_id` was
submitted twice. This made client retry unsafe: if a network blip caused the
client to not see the success response, retrying would fail and the client
would have no way to recover.

New behavior:

- POST same `artifact_id` twice → second returns HTTP 200 with the existing
  record body. Header `X-Already-Existed: true` for client telemetry.
- POST new `artifact_id` → HTTP 201 with the new record.
- Race-condition recovery: if two concurrent POSTs of the same `artifact_id`
  arrive simultaneously, the loser's IntegrityError is caught and converted to
  an idempotent re-post.

Client code now treats both 200 and 201 as success and uses the header to
distinguish.

### 4. Verification endpoint — short-code-first lookup

**File:** `app/routers/verify.py`

Previously the verify endpoint hardcoded the assumption that all short codes
start with `ZK-`:

```python
if code.upper().startswith("ZK-"):
    result = lookup_by_short_code(db, code)
else:
    result = lookup_by_artifact_id(db, code)
```

This rejected the new 12-char client codes which don't have a `ZK-` prefix.
They fell through to the UUID lookup, didn't match, and returned 404 — even
though the artifact was stored correctly. This is the bug that made
`501C-LPR0-FSAC` say "not found" *after* the push succeeded.

New behavior: try short_code lookup first (covers both client-format and
legacy server-format), fall back to UUID only if not found. No prefix
sniffing.

### 5. Version bump

**File:** `app/main.py`

Bumped to 0.3.0 in two places (FastAPI title and a health/info endpoint).
This is now the sentinel for confirming a deploy is live — querying
`/openapi.json` and reading the version is the fastest way to verify Railway
has picked up the latest commit.

---

## Client-side additions

### zksync — manual push tool

**Location:** `~/zkkey-venv/bin/zk_sync.py` (with `~/bin/zksync` wrapper)

A standalone CLI that reads `~/.zkkey/registry/*.json`, maps each local v2
artifact to the API's `ArtifactIngest` schema, and POSTs to `/v1/attest`.

Key behaviors:

- **Idempotent via `pushed_at` field.** After a successful push, the local
  artifact JSON gets stamped with `pushed_at`, `pushed_to`, `api_short_code`,
  `chain_position`. Re-running `zksync` skips already-pushed artifacts.
- **`--dry-run`** shows what would be pushed without POSTing. Used as a sanity
  check before backfills.
- **`--artifact <zk>`** targets a single artifact. Used for the first probe
  push (501C-LPR0-FSAC) to verify the pipeline before bulk-pushing the rest.
- **`--force-all`** ignores `pushed_at` and re-pushes everything. Useful if
  the API state and local state diverge.
- **Browser-like User-Agent** (`ZKNOT-Device-SDK/0.3.0 ...`) to bypass
  Cloudflare bot detection (CF error 1010). This is an interim workaround —
  see "Outstanding" section for the proper WAF allow-rule fix.

### Artifact mapping (v2 local → API schema)

The local v2 artifact JSON has fields the API doesn't natively understand
(`manufacturing_events`, `puf_image_sha256`, `tamper_seal`, etc.). The
mapping:

| Local field | API field |
|---|---|
| `record_sha256` (first 16 bytes → UUID) | `artifact_id` |
| (literal) `"POWERVERIFY_UNIT"` | `artifact_type` |
| `dev` | `device_id` |
| `session_id` | `session_id` |
| `record_sha256` (full 32 bytes hex) | `challenge_hash` |
| `sig` | `signature` |
| `pub` | `public_key` |
| `iso` | `signed_at` |
| `zk` | `metadata.zk_code` |
| `label`, `message`, `fw`, `schema_version`, `ctr`, `prior_record_hash`, `record_sha256`, `manufacturing_events`, `puf_image_sha256`, `tamper_seal`, `customer_receipt` | `metadata.<field>` |

The artifact_id is derived deterministically from record_sha256, so the same
artifact mapped twice produces the same UUID — which combined with the API's
idempotency makes the whole pipeline replay-safe.

### Auto-push hook (NOT YET INSTALLED — see Outstanding)

A patch file (`zk_sign_patch.md`) was prepared to add auto-push at the end of
every `zksign sign` invocation. It was NOT applied cleanly this session due to
a file-handling slip (the patch's `cp` accidentally overwrote `zk_sign.py`
with `zk_sync.py`, and the situation was recovered by restoring from a
prepatch backup). The patch instructions still exist at
`~/Downloads/zk_sign_patch.md` and should be applied fresh tomorrow.

Today's workflow without the hook: sign, then manually run `zksync`. Two
commands instead of one. Functionally identical.

---

## Forensic boundary: chain position 10

Between the placeholder-era v0.2.0 deploy and the verified v0.3.0 deploy, a
deliberate test was conducted at 2026-05-20T19:08Z by submitting an artifact
with a deliberately invalid signature (130 hex zeros) and an obviously fake
device_id (`FAKE-TEST`) to the live production endpoint.

The placeholder accepted it. The artifact was assigned chain position 10 with
entry_hash `b39009c77b358ec61a22e8e7bd17723da29d002e7e722500bb5095d5c3807175`.

**This entry was preserved intentionally** rather than deleted, for three
reasons:

1. **Forensic evidence.** It is contemporaneous proof that the v0.2.0
   verifier was a placeholder. An acquirer's technical reviewer asking "did
   you really have a verifier gap?" can be pointed at position 10. The same
   submission to the v0.3.0 endpoint immediately afterward returned HTTP 400
   ("Signature verification failed").

2. **Chain boundary.** Position 10 is the timestamp boundary between
   placeholder and real verification. All legitimate post-fix entries (11+)
   chain forward from position 10's prev_hash. This is the cleanest possible
   audit trail.

3. **PAT-005 demonstration.** Per the vendor-irrevocable attestation claim,
   the chain *cannot* be modified after the fact without invalidating every
   subsequent entry. Preserving the audit witness *and* documenting it in
   CHANGELOG.md *is* the patent's claim in action — we'd lose that
   demonstration by deleting the entry.

The audit witness is documented at the bottom of `CHANGELOG.md` in the
api repo. The entry is trivially identifiable in any chain audit:
`device_id = "FAKE-TEST"`, `signature = "00...00"`. No legitimate ZKNOT-issued
unit will ever have these values.

---

## Commit history (api.zknot.io repo)

In chronological order:

| SHA (prefix) | Subject |
|---|---|
| `c35defa` | (corrected) chore: backup files + label artifacts + undershrink print script |
| `3f136c2` | feat(crypto): real ECDSA P-256 verification (PAT-001 §4.5 / PAT-005 §3.2) |
| `6cb2567` | chore: trigger redeploy for crypto verification fix (3f136c2) |
| `c99bfde` | chore: bump API version to 0.3.0 (matches CHANGELOG) |
| `32f0b8b` | fix(verify): support all short_code formats per PAT-010 §3 |
| `6c23783` | chore: trigger redeploy for 32f0b8b + c99bfde |
| `761aa90` | docs: add forensic record for chain position 10 (pre-fix audit witness) |

Note: `c35defa` was originally pushed with a misleading commit message
claiming the crypto verification fix (the actual diff was just backup files
and label PNGs). It was amended via `--force-with-lease` to the corrected
honest message before any further work continued. This pattern of correcting
commit messages when the content doesn't match is worth preserving — git
history honesty is something acquirer DD reviewers explicitly look for.

---

## Production state snapshot

### API

- **Version:** 0.3.0
- **URL:** https://api.zknot.io
- **Endpoints in use:** GET `/v1/verify/{code}`, POST `/v1/attest`, GET `/health`, GET `/openapi.json`
- **Tests:** 33 passing locally (14 baseline + 19 new crypto verification)
- **Deploy platform:** Railway (railway.com), us-west-2
- **Repo:** github.com/zknot-io/zknot-api, branch main
- **DB:** Postgres (Railway-managed), single replica

### Frontend

- **URL:** https://verifyknot.io (live, Cloudflare Pages)
- **Status:** Deployed and serving. Verified end-to-end with `501C-LPR0-FSAC`.

### Chain

| Position | Type | Notes |
|---|---|---|
| 1-9 | Pre-fix legitimate entries | Earlier dev signings before today's batch |
| 10 | Pre-fix audit witness | `FAKE-TEST`, all-zero signature, deliberately preserved |
| 11 | `501C-LPR0-FSAC` (PV1-00046) | First post-fix verified entry |
| 12 | `A5RW-3SHW-27A4` | Legacy v1 dev signing |
| 13 | `C4G7-TW89-768V` | Legacy v1 dev signing |
| 14 | `JG3J-ARQ3-6WVP` (PV1-00049) | v2 production unit |
| 15 | `KAM6-M30B-4JHP` | Legacy v1 dev signing |
| 16 | `NDWY-XE6M-GXF7` (PV1-00050) | v2 production unit |
| 17 | `PGLB-GN2D-F4EW` (PV1-00047) | v2 production unit |
| 18 | `Q6B4-H7V3-9CW6` (PV1-00051) | v2 production unit |
| 19 | `QG6M-EK0D-25QY` (PV1-00048) | v2 production unit |

Six v2 production units verifiable (PV1-00046 through 00051), plus three
legacy v1 dev signings retained for compatibility testing.

### Physical units state

| Unit | Pot status | ZK code | Chain position | Next action |
|---|---|---|---|---|
| PV1-00042 | dead/defective | — | — | Discard |
| PV1-00043 | potted | ZK-6GUA-7DV (legacy) | — | PUF capture + post-pot sign |
| PV1-00044 | potted (top) | — | — | PUF capture + post-pot sign |
| PV1-00045 | potted (bottom) | — | — | PUF capture + post-pot sign |
| PV1-00046 | pre-pot signed | `501C-LPR0-FSAC` | 11 | Pigtail + pot; PUF capture after cure |
| PV1-00047 | pre-pot signed | `PGLB-GN2D-F4EW` | 17 | Pigtail + pot; PUF capture after cure |
| PV1-00048 | pre-pot signed | `QG6M-EK0D-25QY` | 19 | Pigtail + pot; PUF capture after cure |
| PV1-00049 | pre-pot signed | `JG3J-ARQ3-6WVP` | 14 | Pigtail + pot; PUF capture after cure |
| PV1-00050 | pre-pot signed | `NDWY-XE6M-GXF7` | 16 | Pigtail + pot; PUF capture after cure |
| PV1-00051 | pre-pot signed | `Q6B4-H7V3-9CW6` | 18 | Pigtail + pot; PUF capture after cure |

---

## What broke and how it was recovered

This is honest documentation of the rough edges encountered, because they
inform future operations.

### Railway auto-deploy is unreliable

Railway is configured to auto-deploy on push to `main`. In this session, it
worked some pushes and didn't fire on others. There's no clear pattern.

The workaround is an empty commit:

```bash
git commit --allow-empty -m "chore: trigger redeploy for <sha>"
git push origin main
```

This reliably triggers the webhook. The right long-term fix is to investigate
the Railway integration — possibly a "Wait for CI" toggle is fighting a GitHub
Action — but for now the empty-commit pattern works.

**Sentinel for confirming a deploy is live:**

```bash
curl -sS "https://api.zknot.io/openapi.json" | \
    python3 -c "import json, sys; print(json.load(sys.stdin)['info']['version'])"
```

If this prints the version you expect, the deploy is current. If it lags,
wait or empty-commit again.

### Cloudflare bot protection blocks scripted POSTs

Initial attempt to POST to `/v1/attest` from `zksync` returned HTTP 403 with
Cloudflare error 1010 (browser fingerprint banned). The workaround is to send
a browser-like User-Agent header:

```python
headers={
    "User-Agent": "ZKNOT-Device-SDK/0.3.0 (https://zknot.io; "
                  "Mozilla/5.0 compatible; vendor attestation client)",
}
```

This is in `zk_sync.py`. The acquisition-grade fix is a Cloudflare WAF
custom rule that explicitly whitelists the ZKNOT-Device-SDK UA on the
`/v1/attest` path. See "Outstanding" for the procedure.

### Commit message integrity

At one point a commit was pushed to main with a message claiming work that
wasn't in the diff (the `cp` commands had silently failed because
`~/Downloads/zknot-api-patches/` didn't exist, but git still found unrelated
changes to commit). This was caught and corrected via `git commit --amend`
+ `git push --force-with-lease` with a corrected `chore:` message before any
further work.

Lesson: **always inspect `git status` and `git diff --cached` before
committing**, especially after running file-copy commands where the source
might not exist. `cp` failing silently is the dangerous part.

### File install errors from Downloads

Multiple times in the session, `cp ~/Downloads/<file>` failed because:

- Downloads subdirectory didn't exist (`~/Downloads/zknot-api-patches/`)
- File was downloaded one-at-a-time and landed flat in `~/Downloads/`
- A file was downloaded with a different name than expected

The robust install pattern that emerged: always check `ls -la ~/Downloads/<expected_file>`
before running `cp`. If it doesn't exist, the previous step failed and
running the install will compound the error.

### Flameshot screenshots not saved to disk

Flameshot by default copies screenshots to clipboard, not to disk. Screenshots
taken during the session were not findable on disk. If documentation
screenshots are needed, Flameshot needs to be configured with auto-save
enabled and a save path.

---

## Outstanding work, in priority order

### Tier 1: blockers for the next acquirer-facing demo

These don't *prevent* the system from working, but each one is a question an
acquirer's technical reviewer might ask.

#### 1.1. Cloudflare WAF allow-rule for ZKNOT-Device-SDK

The browser-UA workaround in `zk_sync.py` works but is fragile and looks
sketchy in a code review. The right fix:

1. Cloudflare dashboard → Security → WAF → Custom rules
2. Add rule:
   - **Name:** "ZKNOT Device SDK allowlist"
   - **Expression:** `(http.request.uri.path eq "/v1/attest" and http.request.method eq "POST" and http.user_agent contains "ZKNOT-Device-SDK")`
   - **Action:** Skip → Skip "Bot Fight Mode" and "Super Bot Fight Mode"
3. Once verified working, revert `zk_sync.py` to use a clean UA without
   the "Mozilla/5.0 compatible" theater.

Estimated time: 15 minutes.

#### 1.2. Auto-push hook on `zksign sign`

The patch file is at `~/Downloads/zk_sign_patch.md`. It contains four small
edits to `~/zkkey-venv/bin/zk_sign.py`:

1. Add `DEFAULT_API_URL` constant
2. Add `push_artifact_to_api()` function
3. Hook the push into `cmd_sign` after successful save
4. Add `--no-push` and `--api-url` arguments

**Critical:** before applying, back up the current `zk_sign.py` and *make sure
not to overwrite it with the wrong source file*. The current size of
the v2 signer is ~22,624 bytes. After the patch it'll be slightly larger.
If after the patch the file is ~8,800 bytes, that's wrong — restore from
`~/zkkey-venv/bin/zk_sign.py.v2-prepatch-20260519`.

Estimated time: 30 minutes (15 minutes if it goes smoothly the first time).

#### 1.3. PUF capture + post-pot sign for already-potted units

PV1-00043, 00044, 00045 are already potted but haven't been PUF-captured or
post-pot signed. The procedure (per the existing `~/bin/puf` and `zk_sign.py`
v2 paths):

For each unit:

1. Place unit under the microscope rig with reference LED light
2. Run `puf <unit_serial>` to capture and hash the PUF image
3. Sign the post-pot artifact: `zksign sign --message "PV1-XXXXX post-pot lifecycle entry" --label "PV1-XXXXX" --session-id $(openssl rand -hex 16) --seal-serial "TS-2026-XXXXX" --puf-hash $(cat ~/ZKNOT/6_SIG/puf_images/PV_*.sha256)`
4. If auto-push hook installed: artifact is on the API automatically.
   If not: run `zksync` after.

Estimated time: 5 minutes per unit, 15 minutes total for three.

#### 1.4. PUF capture + post-pot sign for 00046-00051

These units were pre-pot signed today and will be cure-locked for ~48 hours
after potting. Once cure is complete, same procedure as 1.3 but with the
prior_record_hash chaining to the pre-pot entry's record hash.

Estimated time: 30 minutes total once cure is complete.

### Tier 2: acquisition outreach assets

#### 2.1. Acquirer outreach email

One email, sent to one specific target from the 8 named acquirers, with:

- A short hook ("ZKNOT, 16-patent portfolio in human-gated attestation, live
  reduction to practice")
- One verifyknot.io URL embedded as proof ("https://verifyknot.io — type
  501C-LPR0-FSAC")
- A specific ask (15 minutes for a demo, or simply "would you be interested
  in a deeper conversation")

This is the highest-leverage thing remaining. The technical foundation is now
in place to support the claim.

Estimated time: 1 hour for first draft, plus iteration.

#### 2.2. Screenshot of verifyknot.io verified state

Re-take and save to `~/ZKNOT/3_OPS/journal/2026-05-20_first-verified-unit.png`.
Configure Flameshot first to auto-save to `~/Pictures/Screenshots/` so this
doesn't recur.

Estimated time: 5 minutes.

#### 2.3. Data room asset organization

The verifyknot.io URLs (one per unit), the CHANGELOG forensic record, the
git commit log, the patent tracker, and the journal entries are all
acquirer-relevant. Organizing these into a clean folder structure in the
existing `09_ACQUISITION/DATA_ROOM/` is medium-priority but pays off the
moment any acquirer asks for it.

Estimated time: 2 hours of curation.

### Tier 3: technical follow-ups

#### 3.1. Deprecation removal

`verify_signature_placeholder` is still in `crypto.py` as a deprecation
shim. Remove it in v0.4.0 once no internal call sites still reference it.

#### 3.2. PUF enrollment endpoint

The API has `/v1/units/{short_code}/puf/enroll` but `zksync` doesn't push
PUF images yet — only the PUF hash inside the artifact's metadata. Future
work: extend `zksync` (or `puf` itself) to upload the actual PUF image to
the enrollment endpoint after artifact attestation succeeds.

#### 3.3. Customer-signed receipts (PAT-005 §3.4)

The v2 artifact has a `customer_receipt: null` slot. When a customer takes
delivery, they sign a receipt artifact that chains to the unit's attestation,
producing a complete vendor → customer chain of custody. Not yet implemented;
requires a customer-side key infrastructure decision.

#### 3.4. API artifact_type enum expansion

The API's `artifact_type` enum is currently `ZKEY_SIGN`, `POWER_SESSION`,
`TRUST_SEAL`, `COMBINED_SESSION`, `POWERVERIFY_UNIT`. The two-phase signing
(pre-pot, post-pot) currently both use `POWERVERIFY_UNIT` and discriminate
via metadata. Cleaner would be `LIFECYCLE_PRE_POT` and `LIFECYCLE_POST_POT`
in the enum directly. Schema migration required.

---

## Where we're going

This is the strategic framing for the next 3-6 months, derived from how
today's work fits the larger picture.

### The acquisition thesis

ZKNOT is an IP-to-acquisition company. The hardware (PowerVerify) is not a
product to scale; it's evidence the patents reduce to practice. The 16
filed provisionals — six of which already have non-provisional drafts
complete — are the assets being sold. The target buyer is one of the 8
named acquirers, identified in `~/ZKNOT-BIZ/09_ACQUISITION/`. Window: ~6
months from now to file non-provisionals, build referenceable demos, and
run outreach.

### How today fits

The placeholder-verifier gap was the single largest technical liability in
the acquisition story. An acquirer's technical due diligence would have
found `return True` in the verify function within an hour and either flagged
it as a deal-killer or used it as a major price-reduction lever. The fix
preempts that finding.

The 9 verifiable units on chain are the proof-of-reduction-to-practice. They
demonstrate that the patent claims (chain-of-custody attestation, vendor
irrevocability, human-readable verification codes, manufacturing lifecycle
ledgers) work end-to-end with real cryptography, on real hardware, in
production.

### The next three sequenced moves

#### Move 1: Convert one provisional to non-provisional (May-June 2026)

PAT-001 (ZKKey) has a non-provisional draft complete and a deadline of
2026-06-30. This is the highest-priority IP work. Attorney engagement is
the next step — see `~/ZKNOT-BIZ/01_PATENTS/Conversion Timeline` in the
patent tracker for budget and procedure.

The non-provisional gives PAT-001 actual examination at USPTO, which
materially strengthens the acquisition value of the entire portfolio.
Acquirers know how to value granted patents and pending non-provisionals;
provisional applications are riskier and discounted.

#### Move 2: Acquirer outreach (June-August 2026)

With the verifyknot.io demo live, the outreach pitch has a hard credibility
hook. The sequence:

1. Pick one target from the 8 named acquirers — probably the one with the
   strongest existing supply-chain / device-attestation product line (Axon
   for police body-cam attestation, or Anduril for defense supply chain
   integrity, or Booz Allen for federal advisory).
2. Send a 4-paragraph email with a verifyknot.io URL embedded.
3. Aim for a 30-minute technical demo within 2 weeks of first contact.
4. Follow up to the next target after 2 weeks regardless of outcome.

A "no" from a first target is information. A "let's talk" from any is the
beginning of the actual acquisition conversation.

#### Move 3: Build referenceable customer (July-November 2026)

The strongest acquisition pitch isn't "we have working tech" — it's "we
have working tech *that a credible customer has paid for*." Even one
small federal pilot ($25-50K) deployed in a sensitive environment provides
enormous validation. The SDVOSB certification puts ZKNOT in front of these
pilot opportunities, but actually winning one requires sustained business
development effort.

This is where the founder's time is most valuable: not on more hardware,
not on more patents, not on more code, but on the conversations that turn
"16 patents and a working demo" into "16 patents, a working demo, and a
paying federal customer."

### What this implies for daily operations

- **Hardware work is bounded.** Finish the current 9 units (43-51) and
  stop. Don't scale to 100. Don't build a manufacturing line. Hardware
  exists to support the IP story.
- **Code work is bounded.** The API is at 0.3.0, real verification, real
  chain. There's no need to add features unless an acquirer requests them
  during due diligence. Maintenance only.
- **IP work is unbounded.** Convert PAT-001. Then PAT-002. Then PAT-005.
  Then PAT-007. Each conversion is a real value-add to the portfolio.
- **Outreach work is the limiting reagent.** Time spent here directly
  determines the acquisition outcome. Time spent anywhere else does not.

The signal from today's session: when "is anyone going to use this?" came
up, the honest answer was *the people who matter will see it during DD,
nobody else needs to.* That's a reframe worth holding onto. The work isn't
for end users. The work is for the one technical reviewer at the acquirer
who, six months from now, will sit down with the patent portfolio and the
public verifyknot.io URL.

That reviewer is the only audience. Today's work made the answer they get
substantially more credible.

---

## Files of record

### API repo (`~/zknot-api`)

- `app/services/crypto.py` — real verification
- `app/services/attestation.py` — idempotent ingest, client-zk-code
- `app/routers/attest.py` — 200/201 differentiation
- `app/routers/verify.py` — short-code-first lookup
- `app/main.py` — version 0.3.0
- `tests/test_crypto_verification.py` — 19 new tests
- `CHANGELOG.md` — release notes + forensic record

### Client repo (`~/zkkey-venv/bin/`)

- `zk_sign.py` — v2 signer (with `--no-push` and `--api-url` flags pending patch)
- `zk_sync.py` — manual push tool
- `zk_sign.py.v2-prepatch-20260519` — restore point if patch goes sideways

### Vault (`~/ZKNOT/`)

- `3_OPS/journal/2026-05-20_v0.3.0_deploy_first_verified_unit.md` — journal
- `3_OPS/journal/2026-05-19_shipping_session_map.tsv` — session map from yesterday
- (pending) `3_OPS/journal/2026-05-20_first-verified-unit.png` — screenshot

### Reference URLs

- API: https://api.zknot.io
- API health: https://api.zknot.io/health
- API spec: https://api.zknot.io/openapi.json
- Verify endpoint: https://api.zknot.io/v1/verify/{code}
- Public verifier: https://verifyknot.io
- Repo: https://github.com/zknot-io/zknot-api
- Railway dashboard: https://railway.com/project/1e3f0f6b-b9b7-4a6a-a30e-a3068539581c

### Reference ZK codes for testing

- `501C-LPR0-FSAC` — PV1-00046, chain position 11
- `PGLB-GN2D-F4EW` — PV1-00047, chain position 17
- `QG6M-EK0D-25QY` — PV1-00048, chain position 19
- `JG3J-ARQ3-6WVP` — PV1-00049, chain position 14
- `NDWY-XE6M-GXF7` — PV1-00050, chain position 16
- `Q6B4-H7V3-9CW6` — PV1-00051, chain position 18

Any of these returns a verified record at the verify endpoint.

---

*End of handoff. Last updated: 2026-05-20.*
