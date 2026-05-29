---
system: zknot-site
purpose: Public marketing + technical site (zknot.io)
repo: ~/zknot-site  (remote git@github-zknot:zknot-io/zknot-site.git)
last_verified: 2026-05-29
related_journals: [2026-05-29_protocol-docs-pages]
---

# SYSTEM: zknot-site (zknot.io)

> Living doc — overwrite to reflect truth-now. For *how I learned* any of this,
> see the dated journals under related_journals.

## Deploy  ← the answer you'll come back for

**This is a Cloudflare WORKER, not a Pages project.** Deploy:

```bash
cd ~/zknot-site && npx wrangler deploy
```

- Reads `wrangler.jsonc` (name `zknot-site`), uploads `router.js` + everything in `./public/`.
- **NOT git-connected.** `git push` puts code on GitHub but does NOT deploy. You must run `wrangler deploy`.
- **Do NOT use `wrangler pages deploy`** — there is no `zknot-site` Pages project; the interactive picker offers `hashstamp`/`verifyknot` (wrong). Pages is the wrong tool here.
- Cloudflare account: shane.systems@gmail.com (acct 7b0e8549…).
- After deploy: hard-refresh (Ctrl-Shift-R) — router sets `Cache-Control: max-age=300`, so the edge serves the old copy for up to 5 min.
- Verify served content without edge cache: `curl -s https://zknot-site.shane-systems.workers.dev/<path>`.

## Architecture

- Static HTML in `public/`, fronted by `router.js` (a Worker) that maps clean URLs → `.html` via `env.ASSETS`.
- **Per-page inline CSS; nav + footer are hand-duplicated into every page.** No shared component. Changing nav site-wide = editing N files (back up first; the originals from the last nav edit are in `~/zknot-site/.nav-backup/`, gitignored).
- Editing a page body: deliver content as a self-contained block with **namespaced** scoped styles (e.g. `.zk-protocol`, `.zk-docs`) so it can't collide with the page's own CSS. Splice between `</nav>` and `<footer>` via: write to `page.new.html` → eyeball in browser → `mv`. Each page has its OWN nav/footer line numbers — never reuse them across pages.
- Theme inconsistency fix: a sparse page shell can be rebuilt from a known-good page's shell (e.g. docs.html was rebuilt from protocol.html's dark shell).

## Routes (from router.js)

`/` → index · `/protocol` AND `/evidence-protocol` → protocol.html · `/docs` → docs.html ·
`/verify` → verify.html · `/about` · `/faq` · `/products/{zkkey,powerverify,zk-localchain,trustseal}` ·
`/verticals/{journalism,pharmaceutical,law-enforcement,election-integrity}`.

## Page-content conventions (locked 2026-05-29)

- Technical pages (`/protocol`, `/docs`) are sober, assumptions-stated, threat-model-first. No marketing absolutes.
- "ZK" = ZKNOT everywhere. NEVER write "zero-knowledge" — the LocalChain is a hash-linked tamper-evident log (SHA-256 + ECDSA P-256), not a ZK proof system.
- EvidenceProtocol™ is KEPT as the product name; `/protocol` carries a bridge line ("technical specification underlying EvidenceProtocol™") so the product-page CTAs land coherently.
- Secure element named as Microchip ATECC608B on docs (decision: named > generic for the cryptographer audience).
- Anchor `id`s on docs (`#localchain #zkkey #powerverify #schema-artifact #schema-device-sig`) are load-bearing — other pages deep-link to them. Don't rename.

## Gotchas

- `lpadmin`-style: `wrangler` is invoked via `npx` (not globally installed); first run prompts to install.
- The `wrangler.jsonc` warning about `pages_build_output_dir` is a Pages field — irrelevant to a Worker, ignore it.
- Decoy repos: `~/Desktop/zknot.io` (stale Jan copy), `~/code-review/zknot-site` (HTTPS review clone), `~/zknot-org-site` + `~/procedures-zknot-org-site` (a DIFFERENT repo, `wrangler.toml`). The live one is `~/zknot-site`.

## Open

- Inline remaining API schemas (VerifyResponse, ChainVerifyResponse, ProvisionRequest) on /docs — currently points to openapi.json.
- Relay/distance-bounding layer + optical-PUF liveness: stated as open in /protocol §11.
