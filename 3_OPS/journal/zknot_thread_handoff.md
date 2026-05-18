# ZKNOT Ecosystem — Drop-In Context for a New Thread

**Paste this entire document at the start of a new Claude thread when you want to either:**
- Add a new procedure to `procedures.zknot.org`
- Begin building `sop.zknot.io` (the paid customized-SOP product)
- Continue any other work on the ZKNOT ecosystem

---

## Who I am and what I'm building

I'm William Shane Wilkinson (preferred handle: Zknot or Shane). I run **ZKNOT, Inc.**, a Utah-based SDVOSB-certified company building cryptographic hardware attestation and chain-of-custody products. SAM.gov UEI: C4SKW13JPEL5. Salt Lake City.

I operate four distinct properties under a deliberate multi-property discipline:

| Property | Purpose | Audience | Status |
|---|---|---|---|
| **zknot.io** | The company — commercial, products, contracting | engineers, federal/SDVOSB customers, evaluators | live |
| **zknot.org** | The editorial arm — essays, the Journey | engineers, journalists, academics | live |
| **procedures.zknot.org** | The reference library — free vendor-neutral SOPs | compliance officers, procurement, journalists | live (infrastructure only; first SOP pending) |
| **sop.zknot.io** | The paid product — customized SOP generator | defense contractors, compliance managers | not built; planned |
| **verifyknot.io** | The platform — artifact verification (separate property) | end users | live |

## The discipline (non-negotiable)

**Rule 1 — Each property does one thing.**
- `.io` sells.
- `.org` (essays) and `procedures.zknot.org` (SOPs) do not sell, ever.
- `sop.zknot.io` will sell paid customized SOPs but does not pretend to be reference material.
- `verifyknot.io` is functional only.

**Rule 2 — procedures.zknot.org is vendor-neutral.**
Every "Tool Options" table lists products alphabetically. ZKNOT products appear alongside competitors without preference. No asterisks, no "recommended." If a step's table contains only ZKNOT products, the step is too narrow and gets rewritten.

**Rule 3 — Disclosure on every page with commercial interest.**
Essays on zknot.org disclose ZKNOT's commercial interest in the footer. Procedures on procedures.zknot.org carry a standing disclosure paragraph in every footer. We never hide the commerce; we keep it out of the body.

**Rule 4 — When tempted to put commerce on .org or procedures, stop.**
The properties only work if the editorial/reference surfaces stay clean. The temptation will arrive often. The discipline is what protects the moat.

## Tone and editorial voice

- **zknot.org essays** — research-journal voice. Serif typography (Fraunces / Source Serif 4). Calm, Socratic, never alarmist. "By the Editors."
- **procedures.zknot.org** — institutional reference voice. Closer to NIST publications than to vendor whitepapers. Scannable, printable, citable. "Authored by ZKNOT, Inc." with my name as editor in the colophon.
- **zknot.io** — engineer-fluent commercial voice. Dark/mono/green aesthetic (Syne / DM Sans / DM Mono). Already built, do not redesign.
- **sop.zknot.io** (planned) — professional service voice. Honest about being a paid product. Position A liability framing: "template, not compliance artifact, adopter responsible for fitness."

## Filesystem layout (Linux dev box)

```
~/zknot-org-site/                  # zknot.org source
~/zknot-site/                      # zknot.io source
~/procedures-zknot-org-site/       # procedures.zknot.org source
~/zknot-api/                       # FastAPI backend (Railway, PostgreSQL)
~/ZKNOT/                           # Knowledge management vault
  └── 3_OPS/journal/               # Where session journals get committed
```

All three site repos follow the same pattern: static HTML/CSS in `public/`, deployed via Cloudflare Workers Builds, `wrangler.toml` at root.

## Repo URLs (GitHub org: zknot-io)

- `github.com/zknot-io/zknot-org-site`
- `github.com/zknot-io/zknot-site`
- `github.com/zknot-io/procedures-zknot-org-site`
- `github.com/zknot-io/verifyknot-site`
- `github.com/zknot-io/zknot-api`

SSH alias: `github-zknot` → `~/.ssh/id_ed25519_zknot`

## Deploy workflow (identical for all three site repos)

```bash
cd ~/<repo>
git pull
# edit files in public/
git add -A
git commit -m "<conventional commit message>"
git push
```

Cloudflare auto-deploys via Workers Builds in ~30 seconds. No build step. No CI to configure. The asset directory (`./public`) is declared in `wrangler.toml`.

## Existing infrastructure (do not rebuild)

- **Shopify** at `shop.zknot.io` — PowerVerify AirGap $39 live
- **Gumroad** at `zknotio.gumroad.com` — 8 products: ZKKey DIY Guides (Black Pill free, 5 platforms at $9, bundle at $29) + ZKNOT Compliance Series at $79
- **Google Workspace** for `zknot.io` (and being set up for `zknot.org`)
- **api.zknot.io** on Railway with `POST /v1/attest` and `GET /v1/verify/{code}` live

---

## TASK A — Add a new procedure to procedures.zknot.org

If I'm asking you to add a new SOP, follow this process:

### What you need from me first
- Which procedure (e.g., "Bodycam Footage Chain of Custody")
- The next available document ID (currently ZKNOT-SOP-001 is in draft; next would be ZKNOT-SOP-002)
- Whether I have draft content for it or want help writing it from scratch
- The procedure type (Chain of Custody / Evidence Handling / Audit Trail / Access Control / Tamper Evidence)
- The primary audience tag

### CLI commands I'll run

```bash
cd ~/procedures-zknot-org-site
git pull

# Copy the existing SOP as a template
cp -r public/procedures/digital-evidence-chain-of-custody \
      public/procedures/<new-slug>

# Edit the new SOP file in my editor
# Update public/index.html to add the new SOP to the table

git add -A
git commit -m "sop: ZKNOT-SOP-NNN <title>"
git push
```

### What you do
- Write the SOP content into the template structure (header, scope, numbered procedure steps, tool-options tables, verification criteria, references, disclosure footer)
- Follow the vendor-neutrality rule: every tool-options table lists products alphabetically, with at least one non-ZKNOT product, no preferential markings
- Update `public/index.html` to add the new SOP as a row in the main table (Document ID, Title, Type, Status: Published or Draft) and remove it from the "Planned" placeholder rows
- Keep the document-ID badge at the bottom of each SOP page in sync with the document's actual ID
- Provide me with either patched files I can drop in, or copy-paste-ready bash/sed/python commands to apply changes

### Tool-options table format

The exact pattern, reproduced from ZKNOT-SOP-001 step 2.1, is in `public/procedures/digital-evidence-chain-of-custody/index.html`. Every step's table:
- Header row: Tool / Category / Notes
- Rows alphabetical by tool name
- ZKNOT products explicitly noted as ZKNOT in the Notes column
- At least one non-ZKNOT product per category, or the step is rewritten

### Critical content rules
- **No "highly recommended" or vendor-preferenced language.**
- **No marketing copy.** This is a reference document, not a brochure.
- **Disclosures live in the footer, not the body.**
- **Cite real standards** (NIST, ISO, ACPO, etc.). If a citation can't be verified, leave the section as a draft note rather than inventing one.
- **Use the same standing disclosure paragraph** that appears in ZKNOT-SOP-001, with the only variation being the document title.

---

## TASK B — Begin building sop.zknot.io

If I'm asking you to start `sop.zknot.io`, this is what we agreed in the planning thread:

### Strategic constraints
- **Liability position: A** — Template framing, not compliance artifact. Customer responsible for fitness. Marketing language is "template starting point" not "professionally-developed."
- **Customization level: Start at A, build for B** — v1 ships with administrative-only branching (business name, address, POCs, CMMC level, CUI type, personnel count). Architecture supports substantive branching in v2 without rewrite.
- **Pricing: $99** — priced for volume.
- **First vertical: deferred from CMMC.** Use content adapted from the existing $79 Gumroad Compliance Series, which is general digital-evidence chain-of-custody. CMMC becomes v2 once the architecture is proven and dedicated content is developed.
- **Payments: Stripe Checkout.** Not Shopify (overkill for digital), not Gumroad (already in use for static digital products).
- **Delivery: email the customized PDF post-payment.** No user accounts in v1. Store server-side keyed by checkout session ID.

### Build stack (matches existing infrastructure)
- Frontend (`sop.zknot.io`): static HTML form on Cloudflare Pages
- Backend: new endpoints on existing `api.zknot.io` FastAPI:
  - `POST /v1/sop/checkout` — creates Stripe Checkout Session
  - `POST /v1/sop/webhook` — Stripe webhook, triggers PDF generation + email
- PDF generation: `weasyprint` in Python (HTML/CSS → PDF)
- Email: Postmark or AWS SES (any SMTP works for v1 volume)
- Storage: Railway PostgreSQL (already provisioned). New table: `sop_purchases` (checkout_session_id, customer_info, pdf_blob_url, doc_id, created_at)
- Document IDs: reuse the short-code scheme from `api.zknot.io`

### v1 questionnaire fields
Administrative (Section 1): legal business name, DBA, address, CAGE code, UEI, primary POC (name/title/email/phone), secondary POC.
Document control (Section 2): effective date, version (default 1.0), document owner, review cycle (default 12 months).
Environment branching (Section 3): CMMC level (Level 1 / 2 / 3 / not yet determined), CUI type (documents / engineering / mixed / not yet determined), personnel with CUI access (1-10 / 11-50 / 51-200 / 200+). These three drive v1 branching infrastructure even though they don't change the procedure substance much in v1.

### What I will need from you
- Repo scaffold (`zknot-io/sop-zknot-io-site`) for the frontend
- New `~/sop-zknot-io-site/` directory matching the patterns of the other sites
- Branchable template system: the procedure is composed at PDF generation time from section blocks; questionnaire answers determine which blocks include
- Stripe Checkout integration (test mode first; switch to live when ready)
- weasyprint PDF generation with the visual style of procedures.zknot.org (Fraunces / Source Serif 4) but adapted for legal-grade printing
- The first paid template (adapted from my Gumroad Compliance Series content, which I'll provide)
- Disclaimers on the PDF itself, not just the website

### Critical things to NOT build in v1
- User accounts / login
- A library of past SOPs the customer can re-download
- Live editing / preview
- Draft mode or partial customization
- Admin panel (template lives in repo, edited via git)

---

## Patterns to follow

### Visual register decisions (already locked)
- **procedures.zknot.org**: Fraunces (display) + Source Serif 4 (body) + JetBrains Mono (technical details). Paper-and-ink palette `#f6f3ec` background, `#181613` ink, `#8a2818` oxblood accent. Documentation-portal density, printable.
- **zknot.org**: Same fonts, similar palette, but editorial layout (wider line measure, drop caps on essays, ornament dividers).
- **zknot.io**: Syne + DM Sans + DM Mono, dark mode, green accent. **Do not redesign.**
- **sop.zknot.io** (when built): Should share the procedures.zknot.org typographic family but with more "service" feel and a clear form-driven flow.

### Editorial habits
- Numbered sections with mono-styled section numbers in accent color
- Document IDs in mono caps with the badge styling from `.sop-doc-id`
- Standing disclosure paragraph reused verbatim across documents
- Authorship line: "Authored by ZKNOT, Inc., Salt Lake City, Utah. Edited by William Shane Wilkinson."

---

## The key thing for Claude to remember

**Before building anything, check whether it exists.**

In previous sessions, you (Claude) designed from scratch what already existed (the zknot.io site, the PowerVerify product page) because I hadn't yet given you the inventory. The pattern wastes time.

So when I ask for new work in a new thread, the first move is to:
1. Read this whole document
2. Ask me which of the listed properties I want to touch
3. If a property is described as "live," assume it exists in real working condition and ask to see the relevant file before modifying
4. If I want to add to procedures.zknot.org, the template SOP is at `public/procedures/digital-evidence-chain-of-custody/index.html` — read it before writing a new one
5. If I want to start sop.zknot.io, follow Task B but ask which questions or pieces you should clarify before building

## My current state

(Update this section when you paste this prompt into a new thread.)

- procedures.zknot.org infrastructure deployed: YES (May 18, 2026)
- ZKNOT-SOP-001 v1.0 published: NO (draft only)
- sop.zknot.io: NOT STARTED
- Outreach campaign (Schneier, Green, Pfefferkorn, others): IN PROGRESS / NOT STARTED — update before pasting
- Google Workspace for zknot.org: PENDING completion

## What's NOT in scope for a fresh thread

- Redesigning zknot.io to match zknot.org aesthetic (defer until forcing function)
- Creating new properties beyond the four documented
- Adding ZKKey/ZK-LocalChain/TrustSeal buy paths to zknot.io (defer until products are Shopify-ready)
- The free SOP corpus expansion (one SOP at a time, on demand)

— End of handoff context —
