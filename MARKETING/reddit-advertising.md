---
title: Reddit Advertising Primer (ZKNOT)
system: reddit-advertising
status: active
created: 2026-06-05
owner: Shane
note: Platform mechanics change. Verify specifics in the live Ads Manager before launch.
---

# Reddit Advertising Primer (ZKNOT)

## TL;DR — how to think about Reddit ads

- Reddit is **high-intent and community-driven**: people are there to research passions and problems. That's a gift for a niche, explainable product like PowerVerify — and a trap if you market at them instead of with them.
- Targeting is now **automation-led**. Your community/keyword picks are *signals*, not fences. You steer the algorithm; you don't cage it.
- **Native, honest creative wins; hype gets roasted in the comments.** This is the platform where ZKNOT's "verify, don't trust" candor is an advantage, not a liability.
- **Measurement (the pixel) comes before spend.** Without it you're buying clicks blind.
- First cold runs usually break even at best. The real product of run #1 is **learning + pixel data + a retargeting audience**, not profit.

## 1. Account structure (three levels)

- **Campaign** — objective, overall budget/schedule, brand strategy.
- **Ad Group** — audience targeting, placements, bidding, schedule. (You can run several ad groups to test audiences.)
- **Ad** — the individual creative: hook, format, image/video, headline, CTA. (Run 2+ to test messages.)

Keep tests clean: change one variable per level so you can read what moved the result.

## 2. Objectives — what the algorithm optimizes for

Reddit's current objectives: **Brand Awareness & Reach, Traffic, Conversions, App Installs, Video Views.**

| Objective | Optimizes for | Use when |
|---|---|---|
| Awareness & Reach | Impressions / unique reach | Building recognition; top-of-funnel |
| Traffic | Clicks / landing-page visits | Driving visits cheaply; seeding the pixel |
| Conversions | On-site actions (needs pixel) | Driving purchases once pixel has data |
| App Installs | Installs | (N/A for ZKNOT) |
| Video Views | Views | Storytelling / demo reach |

**The trap:** a Traffic campaign buys clicks, not buyers. It will happily deliver cheap clicks from people who never intended to buy. Pick Traffic to *learn and seed the pixel*; switch to Conversions once the pixel has enough events to optimize toward purchases.

## 3. Targeting — suggestions vs. controls (the single most important thing)

Reddit splits all targeting into two buckets:

- **Audience Suggestions = soft signals (hints).** Communities, keywords, interests, custom audiences. These *guide* automated targeting but **do not limit who sees your ads.** The algorithm will spend beyond your picks wherever it predicts performance.
- **Audience Controls = hard filters (always respected).** Locations, gender, language, devices, custom-audience exclusions, brand-safety exclusions. These are the only true fences.

**Implication:** you can no longer fully lock an ad to a list of subreddits. So your levers for staying relevant are: (1) feed the automation strong, consistent *signals* (several relevant communities + keywords + interests), (2) write creative that **self-selects** the right clicker, and (3) use the hard controls (geo, language, exclusions) plus a spend cap to bound the blast radius.

## 4. Bidding

- **Lowest cost (auto):** maximizes volume for your budget. Best default for getting data fast; you cede control of cost-per-result.
- **Cost cap:** keeps average cost per result at/below a cap while getting as much volume as possible. Use when you need to control CPC/CPA and have a target in mind.
- **Manual max bid:** you set the ceiling per action. More control, more babysitting.

Start on **Lowest cost** to learn the market, then move to **Cost cap** once you know your acceptable cost per click/conversion.

## 5. Budget, schedule & the learning phase

- **Daily vs. lifetime budget.** Daily × number of days = your *real* exposure. Always know that product.
- **Set a campaign spend cap** on any test so total spend can't run away even if the daily looks small.
- **Concentrated beats dribbled for signal.** A healthy daily over a short window produces steady events and stabilizes the algorithm faster than the same money stretched thin. Calendar days aren't the signal driver — event volume is.
- **The learning phase is real.** The algorithm needs a stretch of stable delivery to optimize. **Significant edits (budget, targeting, creative, bid) reset it** and waste spend. Set it up right, then leave it alone for the flight; read results after, not during.

## 6. Measurement — install the pixel first

Do this **before** spending:

- Ads Manager → **Events Manager → Set Up Reddit Pixel.** Paste the snippet in your site `<head>` (or via Google Tag Manager).
- Verify firing with Reddit's **Pixel Helper** browser extension.
- Track at minimum: **PageVisit, ViewContent, AddToCart, Purchase.**
- Consider the **Conversions API (CAPI)** later for server-side resilience against ad-blockers.
- Tag destination URLs with **UTM parameters** so analytics attributes the traffic.

Without the pixel: even a "successful" traffic campaign tells you nothing about whether clicks became sales, and you build no retargeting audience.

## 7. Ad formats

| Format | What it is | Good for |
|---|---|---|
| **Image / Promoted Post** | Single image, looks like a native post (Promoted label) | Simple message, traffic, conversions — the workhorse |
| **Video** | Autoplays muted in-feed | Demos, storytelling; lead hook in first 3s, add captions |
| **Carousel** | 2–6 swipeable cards | Product collections, step-by-step story |
| **Free-form** | Mix of text/image/video/CTA, most native feel | Tailoring to a subreddit's vibe |
| **Conversation (comment) placement** | Ad nested in comment threads | High engagement; users spend big time in comments; often lower CPM when paired with feed |
| **Product / catalog (dynamic)** | Pulls from product feed | Retargeting past site visitors with items they viewed |
| **Lead gen** | Native form inside the ad | Capturing emails without leaving Reddit (e.g. reservation interest) |
| **Reddit Max** | AI auto-combines your headlines/creatives/CTAs | Hands-off optimization; you supply the assets |

For PowerVerify, **image promoted posts** are the obvious start (the product is gorgeous and self-explanatory in one photo). **Lead gen** is worth noting for the Attested *reservation* funnel.

## 8. Creative that works on Reddit

Culture first: redditors have strong ad-radar and will publicly dismantle anything that overclaims or feels corporate. That's why honesty is a moat here.

- **Look native.** Authentic, plainspoken, a little self-aware beats glossy. Image ratios 1:1 or 4:5; put a short text overlay on the image.
- **Lead with the hook.** "You shouldn't have to trust your charger — look through it." Invites scrutiny, which this audience loves.
- **Hold the claim guardrails** (ZKNOT standing rule): use "reduces," "designed to prevent," "physically inspectable." **Avoid absolute security claims** and real-time-threat language. The privacy/infosec subs will fact-check you in the comments — let them, and win.
- **Decide on comments.** Promoted posts can attract real discussion. Engaging honestly builds trust; ignoring a sharp question reads badly. Be ready to show up.
- **Show the object.** The clear epoxy + "DATA LINES PHYSICALLY ABSENT" silkscreen is the strongest creative you have. Use it.

## 9. Designing a run for signal

- Test **2–3 creatives** against the **same audience** to learn which *message* works — but don't over-split a small budget (each variant needs enough events to be readable).
- Or test **audiences** with one creative to learn *who* responds. Don't change both at once.
- Give each cell enough budget to clear the learning phase; otherwise the data is noise.
- Read after the flight. Resist mid-flight tinkering.

## 10. Cost & conversion expectations (do the math before launch)

- Directional benchmarks (vary widely): **CPC ~$0.20–$4.00**, **CPM ~$0.50–$15**.
- Model it: `budget ÷ CPC = clicks`; `clicks × conversion rate = sales`. Cold traffic to a ~$39 niche product converts roughly **0.5–2%**.
- Example: $1,000 at ~$1 CPC ≈ 1,000 clicks; at 1% ≈ 10 sales ≈ $390. **Likely under spend on pure ROAS for a first run.** That's expected — you're buying learning and a pixel/retargeting asset, not immediate margin. Name that goal up front so the result isn't a disappointment.

## 11. ZKNOT playbook

- **Communities (signals):** r/UsbCHardware, r/coldcard (bullseye — verify-don't-trust ethos), r/privacy, r/PrivacyGuides, r/cybersecurity, r/netsec, r/AskNetsec, r/digitalforensics, r/computerforensics, r/GrapheneOS, r/hardware, r/Bitcoin. (ProtonPass/Keeper/Anytype are reasonable privacy-adjacent hints.)
- **Keywords (signals):** juice jacking, USB data blocker, USB condom, OMG cable, public charging, charging cable security, USB-C security.
- **Hard controls:** Locations = United States; Language = English; Devices = All; set brand-safety/excluded audiences as needed.
- **Landing page:** the Core product page (shipping product) — not the Attested preorder. Make sure it's live with current copy and pixel-tagged.
- **Audience framing:** the buyer who must *prove something to a third party* (journalists, attorneys, investigators, forensic/lab/procurement) — lean creative toward that.

## 12. Pre-launch checklist (gates)

- [ ] Reddit Pixel installed and verified firing (PageVisit, ViewContent, AddToCart, Purchase)
- [ ] Landing page live, current copy, fast, mobile-clean, UTM-tagged
- [ ] Storefront has enough products that traffic lands on a real shop, not a single SKU
- [ ] ≥2 creatives ready; claim guardrails respected
- [ ] Objective chosen deliberately (Traffic = learn/seed; Conversions = needs pixel data)
- [ ] Hard controls set: US, English, devices
- [ ] Communities (~10) + keywords filled as signals
- [ ] **Campaign spend cap set** + daily × days exposure understood
- [ ] Campaign renamed from the timestamp default
- [ ] Promo-credit terms read (see below)
- [ ] Plan to monitor comments and not edit mid-flight

## 13. Promo-credit handling

Ad-credit promos ("spend $X get $Y") almost always have structure that changes your plan. Before committing a budget shape, confirm from the **actual promo terms**:

- Does the credit arrive **after** you hit the spend threshold (two phases), or is it available up front?
- Does the credit **expire**? By when must it be spent?
- Any **minimum daily** or eligible-campaign-type requirement?

Sequence the flight to satisfy the threshold and use the credit before it lapses — don't design the run until the terms are confirmed.

## Glossary

- **CPC** — cost per click. **CPM** — cost per 1,000 impressions. **CPV** — cost per (video) view. **CTR** — click-through rate.
- **ROAS** — revenue ÷ ad spend.
- **Learning phase** — initial period where the algorithm optimizes; edits reset it.
- **Pixel** — site snippet that reports on-site events back to Reddit. **CAPI** — server-side event reporting.
- **Custom audience** — your uploaded/curated list (include or exclude). **Lookalike** — users similar to a source audience.
- **Frequency** — average times a user sees your ad (watch for fatigue).
- **Suggestions vs. Controls** — soft signals vs. hard filters (see §3).
