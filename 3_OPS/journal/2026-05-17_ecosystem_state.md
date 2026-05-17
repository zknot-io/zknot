# ZKNOT Ecosystem — State of the System
**Journal entry: 2026-05-17**
**Author: Shane Wilkinson (mt@mt)**
**Context: End-of-day snapshot after two days of intensive build work with Claude**

---

## TL;DR

The three-property ZKNOT architecture is live. zknot.org launched today as the editorial arm, with two essays and an interactive Journey. zknot.io was already live and got a routing pass to wire up the buy path. verifyknot.io and api.zknot.io were already deployed. Total shipped: roughly 7,000 words of editorial writing, a 7-chapter interactive experience, a working Shopify buy path on the company site, and the connective tissue between all three properties.

What's *not* shipped, and shouldn't be in the next thread without deliberate reason: visual harmonization between .io and .org. That trade-off was made deliberately and the rationale is documented below.

---

## The Three-Property Architecture

```
zknot.io     →  the company        (commercial, federal, evaluators)
verifyknot.io →  the platform       (functional, end-users)
zknot.org    →  the educational arm (editorial, public-interest)
```

Each has a distinct voice, audience, and purpose. The discipline document is at the end of this journal under "The Manifesto." It is non-negotiable until and unless a deliberate decision is made to revisit it.

### Visual register per property

- **zknot.io** — dark/mono/green cyberpunk aesthetic. Syne (display), DM Sans (body), DM Mono (technical). Green accent `#22c55e`. Engineer-fluent register.
- **zknot.org** — editorial research-journal aesthetic. Fraunces (display), Source Serif 4 (body), JetBrains Mono (details). Paper-and-ink palette with oxblood `#8a2818` accent. Academic-fluent register.
- **verifyknot.io** — TBD inspection (was already deployed before this session, not visually audited)

**The aesthetic mismatch is intentional**, not an oversight. The decision was: the federal/legal/academic audience reads .org for credibility, the engineer/customer audience reads .io for commerce, and the audiences mostly do not overlap in the same session. If a future strategic shift (Series A, federal procurement evaluation, acquisition conversation) requires visual coherence across the ecosystem, the recommended path is to redesign **.io toward .org's editorial register**, not the reverse. See "Path 3" notes below.

---

## What was built in this thread

### zknot.org (built from scratch)

Repo: `github.com/zknot-io/zknot-org-site`
Local: `~/zknot-org-site/`
Deploy: Cloudflare Pages → Workers (via `wrangler.toml`, static assets at `./public`)
Domain: `zknot.org` (Cloudflare DNS, Workers custom domain)

**Pages shipped:**
- `/` — homepage with editorial lead, Journey callout, featured essay, past essays, topics index
- `/journey/` — 7-chapter scroll-driven interactive inquiry: "Can a signature extend into the physical world?"
- `/essays/` — index of all essays
- `/essays/usb-power-and-data/` — Essay № 001 ("USB Carries Both Power and Data on the Same Wire")
- `/essays/what-a-puf-actually-is/` — Essay № 002, with technical appendix
- `/essays/usb-data-attacks-honestly/` — Essay № 003, with technical appendix
- `/about/` — editorial stance, the triangle, "what we are not"
- `/404.html` — editorial 404

**Tech:**
- Pure static HTML/CSS. No JS on publication side.
- `/journey/` uses ~100 lines of vanilla JS for chapter reveal (IntersectionObserver) and Socratic choice handling.
- Two stylesheets: `assets/css/style.css` (publication) and `assets/css/journey.css` (dark variant for Journey).
- `prefers-reduced-motion` honored throughout.
- No tracking, no analytics, no newsletter.

### zknot.io (routing pass on existing site)

Repo: `github.com/zknot-io/zknot-site`
Local: `~/zknot-site/`
Deploy: Cloudflare Workers (via `wrangler.jsonc`, custom `router.js`)
Domain: `zknot.io`

**Changes made in this thread (commit `42cfd00`):**
1. Added "Guides" link in main nav → points to `zknotio.gumroad.com`
2. Added "zknot.org" link in footer of every page
3. Rewrote PowerVerify CTA block: primary "Buy PowerVerify — $39 →" to Shopify, secondary "See a live record →" to verifyknot.io
4. Removed duplicate `products/` folder (was dead code; router serves from `public/`)
5. Email obfuscation **not yet disabled** — see "Outstanding items" below

### What was NOT changed on zknot.io

- Hero, product cards, three-layer doctrine section, diff table, audiences section — all left as-is
- Other product detail pages (ZKKey, ZK-LocalChain, TrustSeal) — buy paths not yet added
- No visual changes to align with zknot.org

---

## Full inventory of zknot ecosystem properties

| URL / Surface | Purpose | Status | Where it lives | Notes |
|---|---|---|---|---|
| zknot.org | Editorial arm | ✅ Live | `~/zknot-org-site/` → Cloudflare Pages → `zknot-org-site` Worker | Built this session |
| zknot.io | Company front | ✅ Live | `~/zknot-site/` → Cloudflare Pages → Worker via `router.js` | Pre-existing, routing pass this session |
| verifyknot.io | Verification platform | ✅ Live | `~/verifyknot-site/` (assumed) → Cloudflare | Pre-existing, not touched this session |
| shop.zknot.io | Shopify storefront | ✅ Live | Shopify, custom domain via Cloudflare | Has PowerVerify AirGap at $39, theme customized |
| api.zknot.io | FastAPI backend | ✅ Live | `~/zknot-api/` → Railway, PostgreSQL | Live endpoints: `POST /v1/attest`, `GET /v1/verify/{code}` |
| zknotio.gumroad.com | Digital products | ✅ Live | Gumroad | 8 products: ZKKey DIY guides (Black Pill free, Blue Pill/ESP32/Arduino/Pi/Pi Pico at $9, bundle at $29) + ZKNOT Compliance Series at $79 |
| editors@zknot.org | Editorial contact | 🟡 In progress | Google Workspace verification was started in this session | TXT record correctly added with `@` name |
| ops@zknot.io | Ops contact | ✅ Live | Existing Workspace setup | Currently obfuscated by Cloudflare Scrape Shield |

---

## Outstanding items (deferred from this session)

### Small / immediate

1. **Disable Cloudflare Email Obfuscation** on `zknot.io`. Dashboard → `zknot.io` → Scrape Shield → toggle off. This will restore `ops@zknot.io` as a clickable `mailto:` link on the PowerVerify page and other product pages.
2. **Complete Google Workspace verification for zknot.org.** The TXT record was added with name `@`. Next step: complete the Workspace verification flow, then swap MX records from the current 5 Namecheap `eforward*` records to Google's. **Important: also delete the current SPF TXT record** (`v=spf1 include:spf.efwd...`) and replace with Google's SPF before mail flips, or Workspace mail will be flagged as spam.
3. **Clean up stale GitHub branch** `update_worker_name_to_zknot-org-site` on `zknot-org-site` repo. It was auto-created by Cloudflare Workers Builds when we fixed the name mismatch. Safe to delete:
   ```bash
   git push origin --delete update_worker_name_to_zknot-org-site
   ```
4. **SSH key passphrase prompts on every push** — slows down development. To cache for the session:
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519_zknot
   ```

### Medium / next-thread work

5. **Add buy paths to other product pages on zknot.io** (ZKKey, ZK-LocalChain, TrustSeal) when those products are ready for sale on Shopify. Currently only PowerVerify has a buy path.
6. **Build a real `/guides` page on zknot.io** that lists the Gumroad guides with descriptions, rather than the current nav link that drops people directly into the Gumroad index. The page exists for SEO and for readers who want to see the catalog before being sent to a checkout. Pattern: keep the actual checkout on Gumroad, but have the *vitrine* on zknot.io.
7. **The ZKNOT Compliance Series ($79) deserves a dedicated page** on zknot.io. It is strategically your highest-value Gumroad product — federal/legal/SDVOSB audiences are the buyers — and it should not be buried in a guide list. Consider `/compliance` or `/products/compliance-series` as a top-level entry.

### Larger / strategic

8. **Essay № 004 on zknot.org.** The current pipeline shows three USB-related essays and the next logical topic is "Physical vs. Digital Signatures." Should be in a different subject area to broaden the publication's surface.
9. **Visual harmonization of .io toward .org's editorial language** ("Path 3") — only if there is a forcing function. Do not do this without a clear strategic reason (Series A, federal procurement, press moment, acquisition conversation). The current visual split is a deliberate strategic choice.
10. **Outreach campaign** — Schneier, Green, Pfefferkorn outreach was in your memory before this session. Now that .org has three real essays and the Journey, the outreach has actual content to point at. This is the highest-leverage next move.

---

## The Manifesto (Editorial Discipline)

This is the contract zknot.org operates under. It is not a style guide; it is a strategic constraint. Breaking it would undermine the architecture that makes the whole ecosystem credible.

### The four rules

**1. The .org publishes; it does not sell.**
No product cards. No buy buttons. No "available now" banners. No Gumroad links in the body. No Shopify embeds. Commercial interests appear only as plain-language footer disclosures at the bottom of individual essays, when the essay's subject overlaps a product.

**2. Free is not the same as educational.**
A free build guide is a free product. A discounted webinar is a discounted product. Pricing is a strategy decision; it does not change the category. Commerce belongs on .io.

**3. The properties may link to each other, but only in one direction at a time.**
The .org can mention .io and verifyknot in essay footers and the about page. The .io can link to .org as the educational arm. But the .org never includes a CTA. Its job is to make the worldview legible; the reader who wants to go further finds the .io on their own.

**4. When in doubt, ask: would a reader feel sold to if I put this here?**
If yes, it goes on .io. If no, it might belong on .org.

### The trigger phrase

When you find yourself thinking *"this would be really useful on zknot.org because it would reach a lot of people"* — that's the moment to stop. Reach is the .io's job. The .org earns trust through restraint, and restraint compounds.

---

## How to update zknot.org (for next thread or contributor)

```bash
cd ~/zknot-org-site
git pull
# edit files in public/
git add -A
git commit -m "essay 004: ..."
git push
```

Cloudflare auto-deploys in ~30 seconds. No build step.

### To add a new essay

1. Copy an existing essay folder as a template:
   ```bash
   cp -r public/essays/what-a-puf-actually-is public/essays/your-new-slug
   ```
2. Edit `public/essays/your-new-slug/index.html`: update essay number, title, dek, body, footer disclosure.
3. Update `public/index.html`: move current featured to "Past Essays," promote new essay to featured. Update the Topics index at the bottom to mark new essay as "Published."
4. Update `public/essays/index.html`: add new essay as the top "Current Essay" entry.
5. Commit and push.

### To add a new chapter to the Journey

The Journey is a single page (`public/journey/index.html`) with seven `<section class="chapter">` blocks. Each chapter has a `data-chapter` number. Adding chapter 8 means: add a new section, add a new `journey-progress-dot` button in the masthead, increment the `data-chapter` and `aria-label` values. No JS changes needed — the `IntersectionObserver` picks up new chapters automatically.

---

## How to update zknot.io (for next thread or contributor)

```bash
cd ~/zknot-site
git pull
# edit files in public/
git add -A
git commit -m "..."
git push
```

Cloudflare auto-deploys via Workers Builds in ~30 seconds.

### Architecture notes for editors

- All content lives in `public/`. The router (`router.js`) maps clean URLs to `.html` files in `public/`.
- The `_redirects` file is a Cloudflare Pages-style redirect map (currently mirrors the router for some routes).
- The `wrangler.jsonc` configures the Worker deploy.
- Do **not** create a top-level `products/` folder again. The router serves from `public/`. The old `products/` was dead code and has been deleted.
- All product pages share the same CSS by being inlined. This is a deliberate choice for portability but means CSS changes happen in N places. If a refactor to shared external CSS is desired, that's worth doing in a focused pass.
- The hero, three-layer doctrine, and footer are duplicated across pages with minor variations. Treat the homepage version as canonical.

### To add a buy path to another product (ZKKey, ZK-LocalChain, TrustSeal)

The pattern that worked for PowerVerify, applied identically:

Replace the existing `<div class="product-cta">` block (currently says "Ready to verify?") with:

```html
<div class="product-cta">
  <h3>Get [PRODUCT_NAME]</h3>
  <p>[ONE_LINE_VALUE_PROP]. $[PRICE] — direct from ZKNOT, Inc.</p>
  <a href="https://shop.zknot.io/products/[shopify-slug]" class="btn-primary">Buy [PRODUCT_NAME] — $[PRICE] →</a>
  <a href="https://verifyknot.io" class="btn-secondary-sm">See a live record →</a>
  <p class="patent-note">[PATENT_ID] — Patent pending. Ships from Salt Lake City.</p>
</div>
```

---

## Decisions made this thread that the next thread should not reopen without reason

1. **zknot.org uses Fraunces + Source Serif 4 + JetBrains Mono.** Not Inter, not Space Grotesk, not system fonts. The typographic identity is the editorial signal.
2. **zknot.org is hosted on Cloudflare Pages (Workers Builds), not GitHub Pages.** The migration from "use GitHub Pages" to "use Cloudflare" happened mid-build because the rest of the ecosystem was already on Cloudflare. Consistency won.
3. **Essay № 003 mentions PowerVerify in the footer disclosure but does not link to it.** This is a deliberate trust-earning move ("we sell one but we won't make this essay an ad for it"). Don't add a link without a strategic reason.
4. **The Journey ends with three quiet outbound links** (verifyknot.io, zknot.io, /essays/) — not a CTA. The restraint is the point.
5. **No newsletter, no analytics, no tracking on zknot.org.** This is a positioning choice. It will eventually become an explicit footer statement.

---

## Files of record (locations on filesystem)

- `~/zknot-org-site/` — editorial site (this session, new)
- `~/zknot-site/` — company site (pre-existing, modified this session)
- `~/zknot-api/` — FastAPI backend on Railway (pre-existing, untouched)
- `~/ZKNOT/3_OPS/journal/` — recommended location for this journal entry (filename suggestion: `2026-05-17_ecosystem_state.md`)
- `~/ZKNOT/3_OPS/journal/property_discipline.md` — the manifesto as a standalone document

---

## For Claude in the next thread

If you are a Claude instance picking this up: the user is operating under a deliberate three-property discipline (.org editorial, .io commercial, verifyknot.io functional). Before suggesting any work that would put commerce on .org or essays on .io, re-read the manifesto above. The architecture is the asset; the discipline is what makes the architecture work.

Before recommending a build, ask whether the user has already built it. The pattern of "Claude designs from scratch what already exists" cost this session real time. The user has a substantial existing infrastructure: GitHub org `zknot-io` with `zknot-site`, `zknot-org-site`, `zknot-api`, `verifyknot-site`, `zknot`, `zknot-hardware`; Cloudflare with all `zknot.*` domains; Shopify at `shop.zknot.io`; Gumroad at `zknotio.gumroad.com`; Google Workspace; SAM.gov registered; SDVOSB-certified.

The highest-value next move is almost certainly not more building. It is outreach. The product needs traffic, not features.

— End of journal —
