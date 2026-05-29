# ZKNOT Ecosystem Build — Comprehensive Thread Journal

**Period covered:** May 16–18, 2026 (two-day build session)
**Journal author:** Shane Wilkinson with Claude
**Status at close:** Three sites live, one site infrastructure deployed, two paid-product paths scoped, full strategic architecture documented
**File location:** `~/ZKNOT/3_OPS/journal/2026-05-18_thread_closeout.md`

---

## TL;DR

In approximately two days of focused work, the ZKNOT public-facing ecosystem went from one operational property (`zknot.io`) to four — three live, one scaffolded. Roughly 10,000 words of editorial writing shipped. A working Shopify buy path on the company site. A complete strategic manifesto and three handoff documents that let any future thread (or contributor) pick up cleanly.

**What's live:** zknot.io (with new routing), zknot.org (editorial publication + Journey), procedures.zknot.org (infrastructure ready for first SOP). The Shopify storefront, Gumroad guides, FastAPI backend, and Workspace email were already operational and got connective tissue added.

**What's documented but parked:** procedures.zknot.org content publishing (parked behind ZKKey Connect + ZKKey Air being sellable), sop.zknot.io paid customization product (parked behind procedures.zknot.org producing signal), visual harmonization of zknot.io toward zknot.org's register (parked unless forcing function).

**What this journal exists to capture:** every decision made in this session that the next thread should not have to reopen, every piece of context that should survive past the end of conversation memory, and every honest observation about what comes next.

---

## The Architecture, Final State

```
zknot.io               →  the company         (commercial, federal, evaluators)
verifyknot.io          →  the platform        (functional, end-users)
zknot.org              →  the editorial arm   (essays + Journey, public-interest)
procedures.zknot.org   →  the procedural arm  (free vendor-neutral SOPs)
sop.zknot.io           →  the paid product    (customized SOP generator; planned)

shop.zknot.io          →  Shopify storefront  (physical products)
zknotio.gumroad.com    →  Gumroad             (digital products)
api.zknot.io           →  Railway / FastAPI   (backend)
```

Five public-facing brand surfaces. Three commerce backends. Each property has one job. Each has its own voice.

---

## What was built in this thread

### zknot.org (new — built from scratch)

- Repo: `github.com/zknot-io/zknot-org-site`
- Local: `~/zknot-org-site/`
- Deployed: Cloudflare Workers Builds → custom domain
- Live URL: `https://zknot.org`

**Pages shipped:**
- `/` — editorial homepage with masthead, lead, Journey callout, featured essay, past essays, topics index
- `/journey/` — seven-chapter scroll-driven interactive piece: *"Can a signature extend into the physical world?"*
- `/essays/` — index page
- `/essays/usb-power-and-data/` — Essay № 001 ("USB Carries Both Power and Data on the Same Wire")
- `/essays/what-a-puf-actually-is/` — Essay № 002 with technical appendix
- `/essays/usb-data-attacks-honestly/` — Essay № 003 with technical appendix
- `/about/` — editorial stance, the property triangle, "what we are not"
- `/404.html` — editorial voice

**Stack:** pure static HTML/CSS for the publication. ~100 lines of vanilla JavaScript only on the Journey for chapter reveal (IntersectionObserver) and Socratic choice handling. Two stylesheets: `style.css` (publication) and `journey.css` (dark-mode variant for the Journey). `prefers-reduced-motion` honored. No tracking, no analytics, no newsletter.

**Typography:** Fraunces (display), Source Serif 4 (body), JetBrains Mono (technical details). Paper-and-ink palette with oxblood `#8a2818` accent on the publication, inverted to dark cream `#ebe5d6` on `#0e0c09` for the Journey.

### zknot.io (pre-existing site — routing pass only)

- Repo: `github.com/zknot-io/zknot-site`
- Local: `~/zknot-site/`
- The site existed and was already excellent. Engineer-fluent dark/mono/green aesthetic. PRODUCTS, PROTOCOL, VERTICALS, DOCS, ABOUT, CONTACT nav. PowerVerify product page already in place with "data conductors are absent, not blocked" framing.

**Changes made (commit `42cfd00`):**
1. Added "Guides" link in main nav → points to `zknotio.gumroad.com`
2. Added "zknot.org" link in footer of every page (the triangle now reciprocates)
3. Rewrote PowerVerify CTA block from "Ready to verify?" → "Get PowerVerify" with primary "Buy PowerVerify — $39 →" linked to `shop.zknot.io/products/powerverify-airgap`
4. Removed duplicate `products/` folder (dead code; router serves from `public/`)

**Not changed:** hero, three-layer doctrine section, product cards, diff table, audiences section, verticals. Buy paths for ZKKey, ZK-LocalChain, TrustSeal NOT yet added because those products aren't sellable yet.

### procedures.zknot.org (new — infrastructure only)

- Repo: `github.com/zknot-io/procedures-zknot-org-site`
- Local: `~/procedures-zknot-org-site/`
- Deployed: Cloudflare Workers Builds
- Domain attachment: requires user action — Cloudflare → Compute → procedures-zknot-org-site → Settings → Domains & Routes → Add `procedures.zknot.org`

**Pages shipped:**
- `/` — SOP index with five-column NIST-style table (Document ID, Title, Type, Status), filter strips by procedure type and audience, vendor-neutrality notice
- `/methodology/` — the doctrinal anchor: format, vendor-neutrality rules, disclosure paragraph, "what we will not do"
- `/colophon/` — credits, typography, citation format, license
- `/procedures/digital-evidence-chain-of-custody/` — ZKNOT-SOP-001 placeholder demonstrating the full format with draft content
- `/404.html`

**Content status:** Zero SOPs published. ZKNOT-SOP-001 is a format example, explicitly marked as draft. Writing the first real SOP is parked.

### Documents that left this thread

Three markdown files in `~/ZKNOT/3_OPS/journal/`:

1. **`2026-05-17_ecosystem_state.md`** — point-in-time snapshot of all properties, what's live, what's planned, the manifesto, outstanding items.
2. **`zknot_thread_handoff.md`** — drop-in context for any future Claude thread. Paste at start of new conversation; future Claude has full context immediately.
3. **`sop_backlog_dependency_ordered.md`** — five-phase publishing plan for the SOP library, gated by hardware ship dates and real-world demand signals.

This document is the fourth, capturing the session itself.

---

## The Manifesto (extracted, for the third time, because it matters)

This is the contract the ecosystem operates under. Every decision in this session was evaluated against these four rules. They are non-negotiable until and unless deliberately revisited.

**Rule 1 — Each property does one thing.**
- zknot.io sells.
- zknot.org (essays) and procedures.zknot.org (SOPs) do not sell, ever.
- sop.zknot.io (when built) sells paid customized SOPs but does not pretend to be reference material.
- verifyknot.io is functional only.

**Rule 2 — procedures.zknot.org is vendor-neutral.**
Every Tool Options table lists products alphabetically. ZKNOT products appear alongside competitors without preference. No asterisks, no "recommended." If a step's table contains only ZKNOT products, the step is too narrow and gets rewritten.

**Rule 3 — Disclosure on every page with commercial interest.**
Essays on zknot.org disclose ZKNOT's commercial interest in the footer when the essay's subject overlaps a product. Procedures carry a standing disclosure paragraph in every footer. The commerce is never hidden; it's kept out of the body.

**Rule 4 — When tempted to put commerce on .org or procedures, stop.**
The properties only work if the editorial/reference surfaces stay clean. The temptation will arrive often. The discipline is what protects the moat.

**The trigger phrase to remember:** *"This would be really useful on zknot.org because it would reach a lot of people."* That's the moment to stop. Reach is zknot.io's job. The .org earns trust through restraint, and restraint compounds.

---

## The strategic frame, in one paragraph

ZKNOT is a hardware-rooted-trust company in an environment where most of the security industry is software-rooted-trust. The strategic risk is being categorized as "another security startup" in a market crowded with them. The strategic asset is being categorized as something else: the company writing the procedures the field needs, the company explaining the physics underneath the security, the company building the verification platform anyone can use. The architecture of the ecosystem is in service of that recategorization. Every editorial choice, every property boundary, every disclosure paragraph is calibrated to support being read as *infrastructure* rather than as *vendor*.

If we ever drift into vendor-voice on the editorial properties, the strategic asset collapses. If we maintain the discipline, the SDVOSB credentials + the patents + the editorial work + the free SOPs + the paid customizations + the verifier compound into something that's genuinely hard to compete with — because no one else is doing all of them with the same intentionality.

---

## Key decisions made this session that should not be reopened without a real reason

1. **zknot.org uses Fraunces + Source Serif 4 + JetBrains Mono.** The typographic identity is the editorial signal.
2. **zknot.org is hosted on Cloudflare Pages (Workers Builds), not GitHub Pages.** Migrated mid-build for consistency with the rest of the ecosystem.
3. **Essay № 003 mentions PowerVerify in the disclosure footer but deliberately does not link to it from the body.** This is the strongest version of the "we won't make this essay an ad" move; the restraint is the rhetoric.
4. **The Journey ends with three quiet outbound links** — not a CTA. The restraint is the entire point.
5. **No tracking, analytics, or newsletter on zknot.org.** This is positioning.
6. **procedures.zknot.org gets its own subdomain.** Not a subpath under zknot.org. The architectural reasoning is in the ecosystem journal.
7. **Free SOPs are vendor-neutral with alphabetical tool tables.** Non-negotiable.
8. **zknot.io aesthetic is NOT being harmonized toward zknot.org's editorial register.** The two visual languages diverge intentionally. If a future forcing function (Series A, federal procurement evaluation, acquisition) requires coherence, the direction is .io toward .org, not the reverse.
9. **sop.zknot.io v1, when built, is Position A liability (template framing) + Level A customization (administrative mail-merge) + branchable architecture + $99 pricing + Stripe Checkout + no user accounts.** Multiple scope-reducing decisions are baked in.
10. **The first paid SOP product (v1) will be adapted from the existing $79 Gumroad Compliance Series content, not from CMMC-specific material.** CMMC is v2 once architecture is proven and dedicated content is developed.

---

## What's parked and what triggers each unpark

### Parked: Writing the first real SOP on procedures.zknot.org
**Trigger to unpark:** ZKKey Connect orderable on Shopify AND Phase 0 prep complete (customer conversations, Compliance Series audit, standards reference library, reviewer shortlist)
**Why:** The first SOP will reference both ZK-LocalChain (already live in API) and ZKKey Connect (not yet sellable). Publishing with a non-buyable product in the tool options creates a credibility gap.

### Parked: sop.zknot.io build
**Trigger to unpark:** procedures.zknot.org has 6+ published SOPs AND at least one customer has asked "can I get a customized version of this?"
**Why:** Until someone asks, the paid product is premature. Building it before validating demand wastes weeks of work.

### Parked: Visual harmonization of zknot.io
**Trigger to unpark:** A specific forcing function — a federal procurement evaluation, an acquisition conversation, a press moment where the audiences will compare the two sites in the same session
**Why:** The current visual mismatch is a deliberate strategic choice. Don't undo it without reason.

### Parked: Essay № 004 and beyond on zknot.org
**Trigger to unpark:** None — write when you have something to say
**Why:** The publication operates on availability, not schedule. Three essays in a session was excellent pacing; writing more without something to say is the failure mode.

### Parked: ZKKey/ZK-LocalChain/TrustSeal buy paths on zknot.io
**Trigger to unpark:** Each product, individually, becoming sellable on Shopify
**Why:** The PowerVerify buy path is the pattern. Other products get the same treatment when they're ready.

### Parked: Disabling Cloudflare Email Obfuscation on zknot.io
**Trigger to unpark:** Anytime — it's a 30-second Cloudflare dashboard action
**Why:** Just a UI navigation I haven't done

### Parked: Completing Google Workspace verification for zknot.org
**Trigger to unpark:** Whenever next at Cloudflare DNS
**Why:** TXT record is in place; the Workspace flow needs to be completed and MX records swapped from Namecheap to Google. Important: delete the Namecheap SPF record before adding Google's, or mail will be flagged.

### Parked: SDVOSB outreach campaign (Schneier, Green, Pfefferkorn, others)
**Trigger to unpark:** Anytime — this is the highest-leverage next move
**Why:** The .org now has real content to point at. Outreach was being managed in a separate thread.

---

## What I came in with vs. what I left with

**Came in with (May 16):**
- One live company site (zknot.io)
- One Shopify storefront with one product
- Eight Gumroad guides
- A FastAPI backend
- 19 provisional patents
- SAM.gov registration, SDVOSB certification
- An idea for an educational property at zknot.org
- No editorial voice, no manifesto, no architecture for how the properties relate

**Left with (May 18):**
- Four live brand properties under a clear strategic architecture
- A written manifesto that survives across threads
- Three published essays (USB power/data, PUFs, USB data attacks)
- One interactive piece (the Journey)
- A working Shopify buy path on the company site
- A reference library scaffolded and waiting for content
- A paid-product (sop.zknot.io) scope fully designed but not built
- Four documents in the vault that let any future thread continue without context loss
- An honest, ranked, dependency-ordered backlog of future work

The most valuable thing in that list is not any single artifact. It's the **architecture itself** — the four-property structure with the manifesto holding it together. The artifacts can be replaced; the architecture is the asset.

---

## Honest assessments

A few things worth recording while they're fresh.

### What worked well in this session

- **Asking before building.** Every time the conversation could have spawned premature construction, the question "what does this actually need?" came first. The PowerVerify page didn't get rebuilt because it already existed. sop.zknot.io didn't get built because the content gating wasn't right. The procedures site got infrastructure without content because shipping infrastructure with placeholder content is better than rushing a real SOP.
- **The manifesto as discipline, not aesthetic.** Treating the editorial separation as a strategic constraint rather than a style preference made every subsequent decision easier. When the question came up of whether to put the Gumroad guide announcement on zknot.org, the manifesto answered it instantly.
- **The two-layer essay structure (002 and 003).** Accessible body + technical appendix is the right format for the audience. Engineers respect the appendix; general readers don't have to read it. It's also the structure that will scale to LinkedIn cross-posting later — the accessible body adapts down to a LinkedIn post format naturally.

### What I'd do differently

- **Inventory before designing.** A pattern recurred: Claude started designing something, then learned it already existed. The PowerVerify page existed before I started drafting one. The zknot.io site existed before I started planning it. Asking "what do you already have?" earlier would have saved real time. The thread handoff document is structured to prevent this in future sessions, but it cost time here.
- **Slower transitions between properties.** The thread covered four properties (zknot.org, zknot.io, procedures.zknot.org, sop.zknot.io). Toward the end, the strategic frame started feeling less crisp as scope expanded. Tighter focus per session would have been better.
- **The "let's keep building" momentum needed more pushback.** I caught the impulse a few times — usually by saying "you should chill, the next move is outreach" — but I should have said it more firmly and earlier. Two days of intense building creates an emotional state where building feels like progress; outreach feels harder because it has uncertain outcomes. The discipline of "ship what you have, then go talk to customers" was the right answer almost every time.

### The most important strategic observation

The architecture works because each property serves a different audience in a different register. But **all four audiences only matter if they get exposed to the work.** Right now, the highest-leverage activity in the entire ZKNOT business is not building another property, writing another essay, or shipping another SOP. It is reaching the people who would read what's already published.

Three essays exist. The Journey exists. PowerVerify is buyable. The reference library scaffolding is in place. None of these matter until journalists, engineers, evaluators, and procurement officers know they exist.

The Schneier email, the Show HN, the SDVOSB-channel outreach, the LinkedIn post for Essay № 002 — these are the 10x activities. They're documented in other threads and in user memory. The next session that produces real business value is most likely an outreach session, not a build session.

---

## Specific things the next person reading this should NOT do

- Do not rebuild zknot.io.
- Do not rewrite the manifesto.
- Do not add product cards to zknot.org or procedures.zknot.org.
- Do not start sop.zknot.io before procedures.zknot.org produces signal.
- Do not publish a procedures.zknot.org SOP before ZKKey Connect is sellable.
- Do not add tracking, analytics, or newsletter forms to zknot.org or procedures.zknot.org.
- Do not "harmonize" the visual aesthetic between properties.
- Do not write more than one SOP at a time. One ship, then signal, then next.
- Do not put commerce on .org. Re-read the manifesto if tempted.
- Do not assume Claude has context. Paste the handoff document first.

---

## File locations of record

Everything from this session lives at:

```
~/zknot-org-site/                          # zknot.org source code
~/zknot-site/                              # zknot.io source code
~/procedures-zknot-org-site/               # procedures.zknot.org source code
~/zknot-api/                               # FastAPI backend
~/ZKNOT/3_OPS/journal/
  ├── 2026-05-17_ecosystem_state.md        # Point-in-time snapshot
  ├── zknot_thread_handoff.md              # Drop-in context for future threads
  ├── sop_backlog_dependency_ordered.md    # Phased publishing plan
  └── 2026-05-18_thread_closeout.md        # This document
```

GitHub org: `github.com/zknot-io`
Cloudflare account: `Shane.systems@gmail.com`

---

## Now what

The ranked next-action list:

1. **Right now, ~10 minutes:** Finish deploying procedures.zknot.org. Get the custom domain attached. Verify `https://procedures.zknot.org` loads in a browser. Close the open loop.

2. **Today, 5 minutes:** Commit the journal documents (this one and the others) to the ZKNOT vault.

3. **This week, hours-not-days:** Finish ZKKey Connect KiCad work and order the JLCPCB run. Hardware is the critical path; everything else in this session is downstream of it.

4. **Soon, when you have a free hour:** Send the Schneier email from the other thread. The .org now has Essay № 002 (PUFs) and Essay № 003 (USB data attacks) to point at. That outreach has been waiting for real content; the content exists now.

5. **Within 30 days:** Disable Cloudflare Email Obfuscation on zknot.io. Complete Workspace for zknot.org. Both are minutes of work.

6. **When ZKKey Connect ships:** Begin Phase 0 of the SOP backlog. Customer conversations first. Reviewer shortlist second. Then start writing ZKNOT-SOP-001 v1.0.

7. **When ZKKey Air ships and procedures.zknot.org has 6+ SOPs and one customer asks:** Build sop.zknot.io v1.

The path is laid out. The discipline is documented. The next move is yours.

---

## Closing note

This was a good session. The work landed. The architecture is sound. The documentation will survive future thread rotations.

The single biggest risk going forward is not technical — it's the temptation to keep building when the next 10x activity is outreach. Resist it. The publication is done. The reference library is scaffolded. The buy path works. The Schneier email, the Show HN, the SDVOSB conversations, the LinkedIn posts — those are now the leverage points.

Go finish the hardware. Then go talk to customers. The documents will wait.

— End of thread closeout —
