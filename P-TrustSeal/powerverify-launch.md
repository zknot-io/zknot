# PROJECT PRIMER — PowerVerify Launch (ship + market the first units)

> Paste this at the top of a fresh chat to run the PowerVerify marketing/sale push.
> Scope is deliberately narrow: get real units sold. NOT the HSM ceremony, NOT Rev 1,
> NOT the SOP library. Those are separate primers/threads. If this thread drifts toward
> "let's also build X," stop — capture it and come back here.
>
> Primer shape: what it is / current state / next actions / blockers / guardrails /
> pointers / done-criteria. (First project primer to use this shape — extract a template
> later if useful.)

---

## WHAT THIS IS

The revenue-first launch of PowerVerify — the power-only USB passthrough dongle.
Goal of the session: **fix the storefront and produce the three marketing artifacts
(video, Reddit post, LinkedIn post) that drive the first real sales.** This is the
3-month "self-sustaining" critical path, the one task that puts a dollar in the door.

Decided at the handoff level (do not re-open here):
- **Ship the HONEST-COPY version now.** PowerVerify's claim today is the *physical* one:
  power-only, data lines physically absent, visibly verifiable through the pot. That is
  true and demonstrable with zero HSM involvement.
- **Do NOT make forensic / "independently verifiable cryptographic provenance" claims.**
  Units currently sign with server-side HMAC, which is not third-party verifiable. The
  cryptographic-provenance story is a Rev 1 / post-ceremony claim. Saying it now would be
  false. (Source: trust-model review, 2026-05-29.)
- **Free Rev 1 swap** is the honest framing for early buyers: they're buying a pre-1.0
  power-only data blocker, with a hardware-attested upgrade coming.

## CURRENT STATE (as of 2026-06-02)

- **Inventory:** 3 genuinely shippable units (new potting process, sharp edges eliminated)
  + 10 older units shippable as **demos** (older potting). So: 3 for sale, 10 for
  reviewer/demo seeding.
- **Storefront:** shop.zknot.io (Shopify), PowerVerify AirGap listed at **$39**. Listing
  is STALE — still says "Pre-Order, ships June 30" and "100W max". Both kill conversion /
  are wrong.
- **Backend/verify:** api.zknot.io live; verifyknot.io live. A buyer CAN scan and see a
  record resolve — but see the honest-copy rule above re: what that record proves.
- **Marketing assets:** none shot yet. A video script draft exists at
  `~/zknot-video-script-ep1.md` (untracked — read it first, don't start from scratch).
  PowerVerify product photos exist at `~/ZKNOT/PowerVerify Pics/`.
- **Channels (from prior journals — reuse, don't rebuild):**
  - Personal Reddit account carries product posts (the `u/zknot_io` corporate account was
    deleted/shadowbanned — do NOT try to revive it for this). Founder-voice from a personal
    account outperforms corporate anyway.
  - LinkedIn: a PUF/authentication Featured article was drafted (2026-05-22) — there may be
    reusable copy there.
  - Reddit lesson banked: a post is alive 24–48h; don't read early metrics as fate. Each
    sub needs NATIVE content — never cross-post the same text.

## NEXT ACTIONS (today, in order)

1. **Fix the Shopify listing FIRST** (highest-leverage, smallest effort):
   - "Pre-Order, ships June 30" → a real near-term ship date (you have 3 in hand — you can
     ship within ~24–48h of order).
   - "100W max" → **"60W max"** (GCT 3A rating; this is a correctness fix, not just copy).
   - Lead with the strongest line you already own:
     **"Look through the clear pot. There are no data lines."**
   - Honest claim set only: power-only, data-path physically absent, made in USA,
     veteran-owned, "verify, don't trust." NO "unforgeable", NO "court-grade", NO
     "cryptographically proves provenance."
2. **Marketing video** — read `~/zknot-video-script-ep1.md` first. Threat-model framing,
   NOT a live-attack demo (YouTube removes offensive-tool footage; a malicious cable just
   needs to be shown as *possible*, then PowerVerify physically blocks it). Show the
   see-through pot = the whole story.
3. **Reddit post** — personal account, founder voice, photo of the transparent pot, soft
   CTA. Native to whichever sub (candidates from journals: r/privacy needs account age;
   r/embedded / r/electronics friendlier; the "50yo vet new to electronics" authentic
   register has worked). Do not fire until a unit is shippable within 24h of order.
4. **LinkedIn post** — B2B/authenticity angle is LinkedIn's strength; pull from the
   2026-05-22 Featured-article draft if it still fits. Tue–Thu 8–9am MT best window.
5. **Decide the 10 demo recipients** — mix: 1–2 technical reviewers who'll report bugs,
   1 with reach (journalist/infosec), 1 investor-impression, 1 personal. Frame every one
   as "Rev 0 pilot, please send feedback."

## BLOCKERS / WATCH-ITEMS

- Only **3** units are sale-grade. Don't run paid ads or a big push that outstrips 3 units
  of supply — first sales prove the funnel (pricing, conversion, fulfillment time), they
  don't need volume. 10 demos seed reviews in parallel.
- `verify_url` / bare-code resolution: confirm verifyknot.io resolves the code on a unit's
  label before pointing a buyer at it (prior bug: `/v/CODE` 404'd; bare code worked).
- Packaging/fulfillment: confirm you can actually ship within the window the listing
  promises before you change the listing to promise it.

## GUARDRAILS (the discipline that keeps this thread clean)

- **One outcome: units marketed and on sale.** Not a new SKU, not Graip, not the SOP
  library, not ZKKey. If the urge to build appears, that's the signal to stop and note it.
- **Honest copy is non-negotiable** — every claim passes "is this physically true of the
  unit in hand?" "Reduces data-exposure risk," not "prevents hacking." "Designed to,"
  not "guaranteed to."
- **No forensic/provenance claims** until Rev 1 + HSM ceremony land (different thread).
- Marketing touches no irreplaceable artifact, so no backup gate here — ship freely.

## POINTERS (read before acting; don't reconstruct from memory)

- `~/zknot-video-script-ep1.md` — existing video script draft (untracked)
- `~/ZKNOT/PowerVerify Pics/` — product photos
- `~/ZKNOT/3_OPS/journal/2026-05-22_marketing-push-battle-plan.md` — channel-by-channel plan
- `~/ZKNOT/3_OPS/journal/2026-05-22_pcb-debug-revenue-pivot.md` — the revenue-first reframe,
  PV unit economics (~$9 cost / ~$30 net at $39), "no data lines" as the asset
- `~/ZKNOT/3_OPS/journal/2026-05-19_lessons_software_first.md` — why honest Rev 0 ships now
- `~/ZKNOT/3_OPS/journal/2026-05-29_verify-trust-model-review.md` — WHY no provenance claim
- `~/ZKNOT/3_OPS/journal/2026-05-22_linkedin-featured-article.md` — LinkedIn draft + how-to
- `~/ZKNOT/3_OPS/journal/2026-05-19_thread_capture_strategy_market_social.md` — Reddit
  voice/account hygiene, sub-by-sub lessons
- shop.zknot.io (edit) · zknot.io (PowerVerify product page, buy-path pattern) · verifyknot.io

## DONE-CRITERIA (this thread is finished when)

- [ ] Shopify listing fixed: real ship date, 60W (not 100W), honest-copy lead line, no
      overclaims.
- [ ] Marketing video produced (or scripted + shot-list ready if shooting is offline).
- [ ] Reddit post drafted in native founder voice + posted (or scheduled to post when a
      unit ships within 24h).
- [ ] LinkedIn post drafted + posted.
- [ ] 10 demo recipients chosen with addresses; 3 sale units ready to fulfill.
- [ ] **Journal it** (`~/ZKNOT/3_OPS/journal/2026-06-02_powerverify-launch.md`, per template)
      and update the root primer's "since last session" line. Then come back to the
      high-level thread and report what shipped.

---

## 30-DAY SIGNAL TEST (from the revenue-pivot journal — carry it)

$800–1,200 revenue in 30 days = a business with a heartbeat, keep going. ~$200 = the
offer/price/story needs work (not more inventory, not more planning). The launch's job
is to generate that signal, not to be perfect.

*Honest copy is the asset. The see-through pot IS the pitch.*
