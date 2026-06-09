# ZKNOT Ecosystem — State of the System
**Journal entry: 2026-05-17**
**Author: Shane Wilkinson (mt@mt)**
**Context: End-of-day snapshot after two days of intensive build work with Claude**

---

## TL;DR

The three-property ZKNOT architecture is live. zknot.org launched today as the editorial arm, with two essays and an interactive Journey. zknot.io was already live and got a routing pass to wire up the buy path. verifyknot.io and api.zknot.io were already deployed. Total shipped: roughly 7,000 words of editorial writing, a 7-chapter interactive experience, a working Shopify buy path on the company site, and the connective tissue between all three properties.

A fourth property — **procedures.zknot.org** — was scoped at the end of the session as a future free-SOP library. It is not built yet; it is in the plan. See "The procedures.zknot.org Plan" below.

What's *not* shipped, and shouldn't be in the next thread without deliberate reason: visual harmonization between .io and .org. That trade-off was made deliberately and the rationale is documented below.

---

## The Architecture (Three Live + One Planned)

```
zknot.io               →  the company         (commercial, federal, evaluators)
verifyknot.io          →  the platform        (functional, end-users)
zknot.org              →  the editorial arm   (essays + Journey, public-interest)
procedures.zknot.org   →  the procedural arm  (free vendor-neutral SOPs; PLANNED)
```

### Visual register per property

- **zknot.io** — dark/mono/green cyberpunk. Syne / DM Sans / DM Mono. Green `#22c55e`. Engineer-fluent.
- **zknot.org** — editorial research-journal. Fraunces / Source Serif 4 / JetBrains Mono. Paper + oxblood `#8a2818`. Academic-fluent.
- **procedures.zknot.org** (planned) — documentation portal. Should share zknot.org typography but denser, scannable, printable. Think MDN / Read the Docs / NIST publication portal.
- **verifyknot.io** — pre-existing, not visually audited this session.

The aesthetic mismatch between .io and .org is **intentional**. The two audiences mostly don't overlap in the same session. If visual coherence ever becomes required (Series A, federal procurement evaluation, acquisition), the recommended path is to redesign **.io toward .org's register**, not the reverse.

---

## What was built in this thread

### zknot.org (new, built from scratch)

- Repo: `github.com/zknot-io/zknot-org-site`
- Local: `~/zknot-org-site/`
- Deploy: Cloudflare Pages → Workers (via `wrangler.toml`, static assets at `./public`)
- Domain: `zknot.org`

**Pages shipped:**
- `/` — editorial homepage with Journey callout, featured essay, past essays, topics index
- `/journey/` — 7-chapter scroll-driven interactive: *"Can a signature extend into the physical world?"*
- `/essays/` — index
- `/essays/usb-power-and-data/` — Essay № 001
- `/essays/what-a-puf-actually-is/` — Essay № 002 with technical appendix
- `/essays/usb-data-attacks-honestly/` — Essay № 003 with technical appendix
- `/about/` — editorial stance, the triangle, "what we are not"
- `/404.html`

**Tech:** pure static HTML/CSS on the publication; ~100 lines of vanilla JS for the Journey only. Two stylesheets (`style.css` + `journey.css`). `prefers-reduced-motion` honored. No tracking, no analytics, no newsletter.

### zknot.io (routing pass only — site was pre-existing)

- Repo: `github.com/zknot-io/zknot-site`
- Local: `~/zknot-site/`
- Deploy: Cloudflare Workers via custom `router.js`
- Domain: `zknot.io`

**Changes made (commit `42cfd00`):**
1. Added "Guides" link in main nav → `zknotio.gumroad.com`
2. Added "zknot.org" link in footer of every page
3. Rewrote PowerVerify CTA: primary "Buy PowerVerify — $39 →" to Shopify, secondary "See a live record" to verifyknot.io
4. Removed duplicate `products/` folder (dead code; router serves from `public/`)

**What was NOT changed:** hero, product cards, doctrine section, diff table, audiences. No buy paths yet on ZKKey, ZK-LocalChain, TrustSeal. No visual changes.

---

## Full inventory

| URL / Surface | Purpose | Status | Notes |
|---|---|---|---|
| zknot.org | Editorial arm | ✅ Live | New this session |
| procedures.zknot.org | Free SOP library | 📋 Planned | Decision made; build deferred |
| zknot.io | Company front | ✅ Live | Pre-existing, routing pass this session |
| verifyknot.io | Verification platform | ✅ Live | Pre-existing |
| shop.zknot.io | Shopify storefront | ✅ Live | PowerVerify AirGap $39 |
| api.zknot.io | FastAPI backend | ✅ Live | Railway + PostgreSQL |
| zknotio.gumroad.com | Digital products | ✅ Live | 8 products (Black Pill free, others $9-$79) |
| editors@zknot.org | Editorial contact | 🟡 In progress | Workspace verification TXT added |
| ops@zknot.io | Ops contact | ✅ Live | Currently obfuscated by Cloudflare Scrape Shield |

---

## Outstanding items (deferred from this session)

### Small / immediate

1. **Disable Cloudflare Email Obfuscation** for `zknot.io`. Dashboard → `zknot.io` → Scrape Shield → toggle off. Restores clickable `mailto:` everywhere.
2. **Complete Google Workspace verification for zknot.org.** TXT was added with name `@`. Next: complete Workspace flow, swap MX records from Namecheap `eforward*` to Google's, and **delete the Namecheap SPF TXT before adding Google's** or mail will be flagged.
3. **Delete stale GitHub branch:**
   ```bash
   git push origin --delete update_worker_name_to_zknot-org-site
   ```
4. **Cache SSH key passphrase for the session:**
   ```bash
   eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519_zknot
   ```

### Medium / next-thread work

5. Add buy paths to ZKKey, ZK-LocalChain, TrustSeal pages on zknot.io (pattern below).
6. Build a real `/guides` page on zknot.io rather than the current nav-link-to-Gumroad.
7. Build a dedicated `/compliance` or `/products/compliance-series` page on zknot.io for the $79 Compliance Series — strategically the highest-value Gumroad product for federal/legal/SDVOSB.

### Larger / strategic

8. **Build procedures.zknot.org** — see plan below.
9. **Essay № 004** — should leave USB territory. Pipeline: "Physical vs. Digital Signatures."
10. **Visual harmonization of .io toward .org** — only with a forcing function.
11. **Outreach campaign** — Schneier, Green, Pfefferkorn (from user memory). Now has real content to point at. Remains the highest-leverage next move.

---

## The Manifesto (Editorial Discipline)

### The four rules for zknot.org

**1. The .org publishes; it does not sell.** No product cards, no buy buttons, no Gumroad links in the body. Commercial interests appear only as plain-language footer disclosures at the bottom of individual essays, when the subject overlaps a product.

**2. Free is not the same as educational.** Pricing is a strategy decision; it does not change the category. Free build guides are still products. Commerce belongs on .io.

**3. The properties may link to each other, but only in one direction at a time.** The .org may mention .io and verifyknot in essay footers and about page. The .io may link to .org. But the .org never includes a CTA.

**4. When in doubt: would a reader feel sold to if I put this here?** If yes, .io. If no, maybe .org.

### The trigger phrase

*"This would be really useful on zknot.org because it would reach a lot of people"* — that's the moment to stop. Reach is the .io's job. The .org earns trust through restraint, and restraint compounds.

### The discipline extends to procedures.zknot.org

**1. Vendor-neutral or it doesn't ship.** Every SOP names competitor products alphabetically, no asterisks, no "recommended" badges. If a procurement officer feels ZKNOT is being preferenced, the property's credibility collapses.

**2. The procedure is the artifact, not the vendor.** ZKNOT's presence in tool-options tables is a consequence of being a real player, not the reason the document exists.

**3. Disclosure on every page.** Small footer: *"ZKNOT, Inc. develops products in this category, named alongside competitors in tool-options sections. This document is intended as vendor-neutral procedural guidance."*

**4. Free always, paid never.** Deeper practitioner guidance lives on Gumroad or zknot.io. The procedures site only works if no reader wonders whether they hit a paywall.

---

## The procedures.zknot.org Plan

### Why this exists

Free, vendor-neutral SOPs covering domains where ZKNOT products are one of several valid tools. The play:

1. Establish ZKNOT as the authority writing the procedures, not just a vendor selling hardware.
2. Become part of the consideration set in environments that would never have heard of ZKNOT through advertising.
3. Own search results for high-value queries (e.g. "election equipment chain of custody SOP," "CMMC evidence retention procedure") that currently surface vendor whitepapers and stale PDFs.
4. Defensively reframe ZKNOT from "another security startup" to "the company giving away the procedures the field needs."

### Architectural decisions (made this session)

- **Subdomain, not subpath.** `procedures.zknot.org`, not `zknot.org/sops/`.
- **Why subdomain wins:**
  1. Editorial separation. Essays are arguments; SOPs are reference documents. Mixing confuses both.
  2. Different design language is needed. SOPs must be scannable and printable; essays read linearly.
  3. Citation friction. `procedures.zknot.org/bodycam-chain-of-custody/v1.2/` reads institutional. A subpath under .org reads as a vendor's marketing section.
  4. Operational independence. Procedures get versioned and redlined; essays don't.
  5. Federal/legal-citation friendliness — subdomain authority matters more than it should.

### Format every SOP must follow

- Cover page with version number, date, and a "vendor-neutral guidance, not endorsement" header
- One-paragraph summary at top: *"This SOP is for [audience] who need to [outcome]."*
- Numbered procedure steps
- Per-step "tool options" table listing 3-5 products alphabetically (no preferencing)
- "Verification criteria" — how to audit the SOP itself
- "References & further reading" — actual standards, NIST docs, legal authorities
- Honest-disclosure footer

### Recommended first three (in order)

★ **1. Bodycam Footage Chain of Custody** — most well-defined audience, clearest pain point, current tools landscape is a mess, ZKNOT has real differentiation. Tools listed: ZK-LocalChain, Axon Evidence.com, Veritone, hashing utilities.

★ **2. Election Equipment Power Attestation** — lines up with PowerVerify, election years drive demand. Caveat: write technically, stay politically agnostic. Tools: PowerVerify, generic USB data blockers, tamper-evident seals.

★ **3. GRC SOP: CMMC 2.0 / DFARS 252.204-7012 Evidence** — SDVOSB credentials make this the most direct path to federal contracting conversations. Defense contractors are starved for usable CMMC guidance. Tools: PreVeil, CMMC-compliant ITAR storage, ZKKey, traditional GRC platforms.

### Full SOP taxonomy (47 total)

Brainstormed this session, ranked roughly by strategic value. **Do NOT try to build all of these.** Ship 5-7 excellently, then expand based on real demand signal from outreach.

**Law Enforcement & Criminal Justice**
1. Mobile Device Seizure & Power-State Preservation
2. ★ Bodycam Footage Chain of Custody
3. Digital Evidence Acquisition (Field-Portable)
4. Confidential Informant Communication Device Hardening
5. Interview Recording Integrity

**Election Administration**
6. ★ Election Equipment Power Attestation
7. Mail-In Ballot Chain of Custody (Digital Sub-Process)
8. Post-Election Audit & Recount Evidence Handling
9. Election Worker Device Provisioning
10. Election Observer Documentation Protocol

**Journalism**
11. Source Material Reception (Anonymous Tips)
12. Field Reporting Evidence Capture
13. Sensitive Document Handling for Investigative Teams
14. Post-Publication Evidence Preservation
15. Cross-Border Travel Device Protocol

**Whistleblowers & Dissidents**
16. Operational Security for First-Time Whistleblowers
17. Document Authentication Before Disclosure
18. Diaspora-to-Origin-Country Communication Hardening

**GRC**
19. SOC 2 Trust Service Criteria Mapping
20. HIPAA Audit Trail Requirements
21. SOX Section 404 Evidence Retention
22. GDPR Article 30 Records of Processing
23. ★ CMMC 2.0 / DFARS 252.204-7012 Evidence

**Healthcare**
24. Clinical Trial Data Integrity (FDA 21 CFR Part 11)
25. Pharmaceutical Cold-Chain Power Integrity
26. Medical Device Incident Reporting Custody

**Critical Infrastructure & Industrial**
27. OT/ICS Maintenance Window Evidence Trail
28. Substation Inspection Chain of Custody
29. Vendor-Access Power Isolation for Substations & SCADA Rooms

**Legal & Judicial**
30. E-Discovery Production Integrity
31. Court Reporter Audio Custody
32. Notary Public Digital Notarization Augmentation

**Education & Research**
33. Research Data Integrity (NIH/NSF Grants)
34. Academic Misconduct Investigation Evidence Handling

**Personal / Individual**
35. Personal Document Time-Stamping for Litigation
36. Family Estate Documentation Custody

**Addendums (shorter, drop into existing SOPs)**
37. USB Power Isolation for Any Existing Asset-Receiving SOP
38. Hardware-Attested Sign-Off for Any Approval Workflow
39. Append-Only Audit Logging for Any Compliance Program
40. Physical Tamper-Evidence for Any Equipment-Transport SOP
41. Independent Verifiability for Any Citizen-Facing Government Process
42. Air-Gap Power Attestation for Classified-Adjacent Workflows
43. Cryptographic Receipt Generation for Any "I-Was-Here" Workflow

**Specialized / lower priority**
44. Humanitarian Aid Distribution Custody
45. Climate Data Integrity for Carbon Markets
46. Art & Cultural Heritage Provenance
47. Refugee Documentation Integrity

### Relationship to the paid Compliance Series on Gumroad

The existing **ZKNOT Compliance Series — Chain of Custody & Digital Evidence SOPs** at $79 partially overlaps.

- **Free SOPs on procedures.zknot.org** — broad-spectrum reference. Brand authority. Vendor-neutral. Framework only.
- **Paid Gumroad Compliance Series** — deep-dive practitioner guides. Worked examples, vendor-specific implementation, templates, ZKNOT-specific deployment.

Pattern: free for the *what*, paid for the *exact how, with our products*.

### When to build it

**Not this week.** The next 10x move is outreach, not more building. The free-SOP play benefits enormously from real demand signal — picking the right first three based on conversations with federal/legal/police-procurement contacts will produce better SOPs than guessing.

**Suggested trigger:** Build after the first outreach round produces at least one signal that someone with procurement authority would use the SOPs. That signal both validates the play and tells you which SOP to write first.

### Build plan (when triggered)

1. New repo `zknot-io/procedures-zknot-org-site`
2. Clone the zknot-org-site Cloudflare Pages → Workers setup pattern
3. Add `procedures.zknot.org` as subdomain in Cloudflare (one-click — domain already in account)
4. Build a documentation-style template (denser than essays, scannable, printable, versioned URLs)
5. Ship the first SOP as both v1.0 of the procedure and v1.0 of the template — they iterate together
6. Add a small link from `zknot.org/about/` to `procedures.zknot.org` once content exists
7. Do not link from zknot.io to procedures.zknot.org in any commercial context — the procedures site's credibility comes from feeling independent of the commerce

---

## How to update zknot.org

```bash
cd ~/zknot-org-site
git pull
# edit files in public/
git add -A
git commit -m "essay 004: ..."
git push
```

Cloudflare auto-deploys in ~30 seconds.

### Add a new essay

1. `cp -r public/essays/what-a-puf-actually-is public/essays/your-new-slug`
2. Edit: essay number, title, dek, body, footer disclosure
3. Update `public/index.html`: move current featured to "Past Essays," promote new essay
4. Update `public/essays/index.html`: add new essay at top
5. Commit, push

### Add a chapter to the Journey

Single page (`public/journey/index.html`) with seven `<section class="chapter">` blocks. Adding chapter 8: new section, new `journey-progress-dot` button in masthead, increment `data-chapter` and `aria-label`. No JS changes needed.

---

## How to update zknot.io

```bash
cd ~/zknot-site
git pull
# edit files in public/
git add -A
git commit -m "..."
git push
```

### Architecture notes

- Content in `public/`. Router (`router.js`) maps clean URLs to `.html` files.
- `_redirects` is a Cloudflare Pages-style redirect map.
- `wrangler.jsonc` configures the Worker deploy.
- Do **not** recreate a top-level `products/` folder.
- All product pages have inlined CSS (portable but means CSS changes in N places).

### Buy-path pattern for new products

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

1. zknot.org uses Fraunces + Source Serif 4 + JetBrains Mono.
2. zknot.org is hosted on Cloudflare (Workers Builds), not GitHub Pages.
3. Essay № 003 mentions PowerVerify in footer disclosure but does not link to it — deliberate.
4. The Journey ends with three quiet outbound links, not a CTA.
5. No newsletter, no analytics, no tracking on zknot.org.
6. **procedures.zknot.org gets its own subdomain.** Not a subpath.
7. Free SOPs are vendor-neutral. Naming competitors alphabetically is non-negotiable.

---

## Files of record

- `~/zknot-org-site/` — editorial site (new this session)
- `~/zknot-site/` — company site (modified this session)
- `~/zknot-api/` — FastAPI backend on Railway (untouched)
- Suggested journal location: `~/ZKNOT/3_OPS/journal/2026-05-17_ecosystem_state.md`

---

## For Claude in the next thread

If you are a Claude instance picking this up: the user operates under a deliberate multi-property discipline. Before suggesting any work that puts commerce on .org, essays on .io, or vendor-preferencing on procedures.zknot.org, re-read the manifesto.

**Before recommending a build, ask whether the user has already built it.** The pattern of "Claude designs from scratch what already exists" cost real time in this session. The user has substantial existing infrastructure: GitHub org `zknot-io` (`zknot-site`, `zknot-org-site`, `zknot-api`, `verifyknot-site`, `zknot`, `zknot-hardware`); Cloudflare for all `zknot.*` domains; Shopify at `shop.zknot.io`; Gumroad at `zknotio.gumroad.com`; Google Workspace; SAM.gov registered; SDVOSB-certified.

**Default recommendation for the next thread, unless the user signals otherwise:** the highest-value next move is outreach, not more building. The product needs traffic, not features. The procedures.zknot.org plan is documented and ready to execute when the user is ready — but it should not be built without a real demand signal from outreach conversations.

— End of journal —
