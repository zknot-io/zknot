# 2026-05-22 — Self-Hosted Checkout: Decisions & Build

**Topic:** Moving product sales off Gumroad/Shopify to a self-hosted Stripe checkout on zknot.io, with R2 file delivery and Resend email. Captures the full decision trail and the code that was generated, so the source chat can be deleted.

---

## TL;DR / Where this landed

Decided to **self-host checkout** on zknot.io rather than pay for Shopify themes or stay on Gumroad. Stack chosen:

- **Stripe Checkout** (prebuilt hosted checkout, not Elements) — payment
- **Cloudflare R2** — product file storage (signed download URLs)
- **Resend** — transactional email delivery
- Fulfillment via **webhook**, not the success page

Code for the whole flow was generated (FastAPI module + buy-button frontend + setup walkthrough). Output bundle: `zknot-stripe/` with `STRIPE_SETUP.md` as the master walkthrough. **Need to re-download / re-save those files separately — they live in the chat output, not yet in a repo.**

---

## The decision trail (why, not just what)

### Gumroad → Shopify → self-host
- Started with 8 products live on Gumroad (ZKKey DIY guides per platform + bundle + Compliance SOPs), $0 sales.
- Considered moving to Shopify. Conclusion: **platform isn't the problem, distribution is.** Shopify is a storefront, not a marketplace — zero built-in discovery, same as self-hosting. No marketing advantage to Shopify.
- Shopify default homepage ("Charge with confidence" + stock rainbow USB) looked bad. Premium themes ($350–380 one-time: Impulse/Prestige/Broadcast) judged too expensive for 2 products.
- **Final call: self-host on zknot.io.** Already have the infra (Cloudflare + Railway), digital products are the easy case, and it keeps the full customer relationship (email list) instead of platform-gating it.

### Marketing notes (parked, not acted on)
The real bottleneck is distribution, not checkout. Product is technical/niche. Channels that fit: Hackaday, Hackster.io, r/embedded, r/crypto, r/homelab (read self-promo rules), Hacker News "Show HN", X crypto+hardware crowd. **Content-driven, not ad-driven** — paid ads burn cash on something this niche.
Recommended single next action when ready: write ONE public build tutorial (ESP32 or Pi Pico — most accessible) and post to Hackaday + r/embedded with link to the $29 bundle. That single action tests whether there's a market.

### Self-hosting question, answered
- **Storefront:** never need to self-host — Stripe/Gumroad/Shopify carry indefinitely; platform fee is just cost of doing business.
- **api.zknot.io:** Railway is right for now. Self-host trigger ~ $50–100/mo platform cost, OR specific compliance/customer requirements (gov customers may not accept Railway-class hosts — relevant given SAM.gov).
- **verifyknot.io:** Cloudflare Pages is ~free forever, never leave it.

---

## Stripe account setup (done during the session)

- Switched to **live mode** under ZKNOT, INC.
- Onboarding module choices: **Non-recurring payments ✓ + Tax collection ✓** (Stripe Tax, 0.5% where applicable). Unchecked Recurring + Invoicing (both addable later).
- Payment integration: **Prebuilt checkout form** (Stripe-hosted, minimal PCI scope). Not Payment Links, not Elements.
- Two products created in **live** mode, One-off pricing:
  - `prod_UQXp6tobLJTOKL` → `price_1TRgkBC0q3GgEvbO4v6CXz0Z`
  - `prod_UQXpNH75Gnd0gk` → `price_1TRgk8C0q3GgEvbOqe91htPM`
  - **TODO: confirm which price ID is the $29 ZKKey Bundle vs. the $79 Compliance Series** (map to STRIPE_PRICE_ID_BUNDLE / STRIPE_PRICE_ID_COMPLIANCE).

### Security note
- Pasted the `pk_live_...` publishable key into chat. Publishable keys are designed to be public (frontend-safe), so not a breach — but recommended **rolling it** as hygiene since it's now in a chat log (Developers → API keys → Roll key; safe to roll immediately since not deployed anywhere yet).
- **Secret key (`sk_live_...`) was NOT exposed** — keep it that way. Store in Bitwarden.

---

## Architecture decisions baked into the code

- **Webhooks fulfill orders, not the success page.** Stripe-recommended: webhooks retry on failure, page hits don't. Success page just says "check your email."
- **Idempotent webhook:** checks for existing `Purchase` row by `stripe_session_id` before processing, so Stripe's duplicate deliveries are safe no-ops.
- **24h signed download links** (R2_DOWNLOAD_TTL_SECONDS, configurable). Expired link → customer emails ops@zknot.io → regenerate manually (or build admin endpoint later).
- **Stripe Tax enabled** in checkout session config (automatic_tax) since it was turned on at onboarding.
- Code matches existing api.zknot.io patterns: env-var driven config via `@property` parsing (Python 3.13 / CORS_ORIGINS_STR style), `/v1/...` namespace, SQLAlchemy 2.0 declarative, pinned deps, new tests added to existing suite. Public webhook uses Stripe signature verification, NOT API_SECRET_KEY.

---

## Files generated (in `zknot-stripe/` output bundle)

Backend (merge into api.zknot.io repo):
- `app/stripe_routes.py` — `POST /v1/checkout/create-session` + `POST /v1/stripe/webhook`
- `app/storage.py` — R2 client (boto3, S3-compatible), presigned URL generator
- `app/email.py` — Resend client + HTML/plaintext delivery template
- `app/config.py` — new env var fields + `get_product_catalog()` product registry
- `app/models.py` — `Purchase` table (session id, email, product, amount, delivery_status, audit)
- `tests/test_stripe.py` — unit tests (unknown product 404, session creation, bad signature, delivery, idempotent replay, ignore unrelated events)

Frontend (merge into zknot-io/zknot-site repo):
- `site-snippets/buy-button.html` — markup + styles + vanilla JS (calls create-session, redirects to Stripe)
- `site-snippets/order-success.html` — `/order/success` redirect target
- `site-snippets/order-cancel.html` — `/order/cancel` redirect target

Master doc:
- `STRIPE_SETUP.md` — full 7-phase setup walkthrough

New deps for requirements.txt: `stripe>=10.0.0`, `boto3>=1.35.0`, `resend>=2.0.0`

---

## Setup checklist (from STRIPE_SETUP.md) — what's left to do

Recommended order so each layer debugs independently:

1. **Cloudflare R2**
   - [ ] Enable R2, create bucket `zknot-products`
   - [ ] Upload `zkkey-bundle-v1.zip` + `compliance-sops-v1.zip` (or change extensions in config if PDFs)
   - [ ] Create R2 API token (Object Read only, scoped to bucket) → R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ACCOUNT_ID → Bitwarden

2. **Resend**
   - [ ] Sign up (ops@zknot.io)
   - [ ] Add domain zknot.io, add the 3 DNS records (MX + SPF TXT + DKIM TXT) in Cloudflare DNS, verify (slow part)
   - [ ] Create API key (Sending access) → RESEND_API_KEY → Bitwarden
   - [ ] Optional: Cloudflare Email Routing forward orders@zknot.io → ops@zknot.io

3. **Deploy code**
   - [ ] Merge files into api.zknot.io repo, add deps, wire router in main.py (`app.include_router(stripe_router, prefix="/v1")`)
   - [ ] Alembic migration for purchases table — locally first, then prod
   - [ ] `pytest tests/` all green
   - [ ] Set Railway env vars **on web service, not Postgres plugin** (full list in STRIPE_SETUP.md §4.6)
   - [ ] Confirm new endpoint shows in /docs

4. **Stripe webhook** (only AFTER API is deployed/reachable)
   - [ ] Add endpoint `https://api.zknot.io/v1/stripe/webhook`, event `checkout.session.completed` only
   - [ ] Reveal signing secret → STRIPE_WEBHOOK_SECRET → Railway + Bitwarden
   - [ ] Confirm which price ID maps to which product (see TODO above)

5. **Frontend** — add buy buttons + success/cancel pages to zknot-site, push to main (Cloudflare auto-deploys)

6. **End-to-end test** — Stripe test mode + card `4242 4242 4242 4242`; confirm redirect → success page → email within ~30s → working download → `purchases` row `delivery_status='sent'`. Then swap to live, buy own product, refund self.

7. **Update platform SOP** (ZKNOT_SOP-001) — add checkout checks to §8.1 monitoring, add new env vars/credentials to §9.

---

## Open TODOs / future enhancements (parked)
- Confirm price ID → product mapping (blocking env var setup)
- Roll the exposed `pk_live_` publishable key (hygiene)
- Possible later: admin endpoint to regenerate expired download links; refund/dispute handling; multi-product cart
- Adding more products later = 2 lines in `get_product_catalog()` + Stripe price ID + R2 upload

---

*Author: William Shane Wilkinson. Source chat captured here for deletion. Code files were in chat output — re-save `zknot-stripe/` bundle into a repo or local dir before relying on this entry alone.*
