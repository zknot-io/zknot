# 2026-05-29 — Outreach Campaign + Site Deploy

## Summary
Sent first-wave cold outreach to three cryptography/security figures, deployed
both public sites, and audited them against the live rendered pages. One reply
already in (Schneier, polite decline). Six audit fixes scoped into three work
threads.

---

## Outreach — sends

| Target | Affiliation (verified) | Channel(s) | Status |
|---|---|---|---|
| Matthew Green | Assoc. Prof, Johns Hopkins ISI; founder, Sealance Corp | LinkedIn DM + Twitter/X | Sent, no reply |
| Riana Pfefferkorn | Policy Fellow, Stanford HAI; lawyer | LinkedIn DM + Twitter/X | Sent, no reply |
| Bruce Schneier | Lecturer, Harvard Kennedy School; Chief of Security Architecture, Inrupt | Email (schneier@schneier.com) + LinkedIn DM | **Replied (declined)** |

Email angle per target: Green = "is the protocol novel?"; Schneier = "where does
this degrade into security theater?"; Pfefferkorn = "is this category legally
useful or a category error?"

**Identity note (lesson):** Bruce Schneier spells with "-eier", NOT "Schneider."
LinkedIn search for "Schneider" returned three unrelated people (a bio consultant,
a food-security advisor, a marketing guy). Reached the real one via his published
contact email on schneier.com. Verify spelling against the person's own canonical
site before sending.

Green and Pfefferkorn were verified as the correct individuals from their LinkedIn
profiles before sending (Sealance Corp / Stanford HAI respectively).

## Outreach — Schneier reply (received ~11:25, ~8 min after send)
> "Cool. I'm too busy to get involved, but good luck."

Read: polite decline, but a real same-session reply from a high-volume inbox =
the email was legible and credible. First real signal of the campaign. His framing
question ("where does it degrade into theater?") is identical to the verifyknot
trustlessness question — see Thread 2 below. Treat Schneier as closed; do not
follow up.

## Follow-up discipline
- Green / Pfefferkorn: NO follow-up for ~1–2 weeks. If either replies, respond fast,
  short, human, in own voice — do not over-polish.
- Schneier: closed.

---

## Site deploy
- **verifyknot.io** — deployed to Cloudflare Pages; live and confirmed. Public
  attestation-verification tool. Copy: "No account. No login. No trust required."
- **zknot.io** — marketing site live. Hero: "Physics enforces. Math proves. You verify."
  Tagline: "ZKNOT is not a security company. It is an evidence company."
- Both links are now live in three expert inboxes (emails referenced verifyknot.io
  as a "demo").

## Audit findings (reviewed against actual rendered pages)
1. **"unforgeable" absolute claim** (zknot.io hero) — must soften to assumption-bound
   language (e.g. EUF-CMA / "computationally infeasible to forge"). PRE-REPLY BLOCKER.
2. **Trustlessness claim** ("No trust required" / "Independent of ZKNOT") — is
   `GET /v1/verify/{code}` actually client-checkable, or is trust just relocated to
   the API? THE key architectural question. PRE-REPLY BLOCKER.
3. **No runnable demo code** — verify box has no example a cold visitor can enter.
   Add live "Try it: ZK-6GUA-7DV" example.
4. **SDVOSB inconsistency** — zknot.io says "SBA VetCert Pending"; verifyknot.io
   footer says "SDVOSB" unqualified. Reconcile across both sites. Compliance-relevant.
5. **PROTOCOL / DOCS pages** — must be substantive or hidden; placeholders do damage.
6. **Mobile** — not yet verified at 380px; whole protocol assumes a phone.

## Work threads dispatched (separate chats)
- **Thread 1 — Copy & claims hardening** (do first): fixes #1, #3, #4, #6.
- **Thread 2 — Trustless verification architecture** (the important one): fix #2;
  determines whether the central claim is true or theater.
- **Thread 3 — PROTOCOL/DOCS content**: fix #5; depends on Thread 2's outcome
  (don't write the verification section until Thread 2 resolves).

Sequence: 1 → 2 → 3. Do not run 2 and 3 in parallel.

---

## Other open tracks (not today's focus)
- Hardware: FT260 USB-I2C bridge + bare TrustCUSTOM provisioning (TFLXTLS slot config).
  No deadline pressure (SBIR no longer a fit). Do it carefully, document well — depth
  of hardware answer is the differentiator if Green replies with a technical question.

## Concepts to review (carryover)
EUF-CMA / existential unforgeability · trustlessness vs. relocated trust ·
falsifiable marketing claims · demo runnability · SDVOSB representation consistency.

---
*Commit: `cd ~/ZKNOT && git add 3_OPS/journal/2026-05-29_outreach_and_deploy.md && git commit -m "journal: outreach campaign + site deploy + audit"`*
