# 2026-05-22 — LinkedIn Featured Section + PUF Authentication Article

**Workstream:** biz
**Context:** Building out LinkedIn Featured section to support the cryptography/security outreach campaign (Green, Schneier, Pfefferkorn). Featured content is what cold contacts and federal prospects will click before replying.

---

## LinkedIn Featured — Content Plan

Six options available in the Featured "+" menu: Add a post, Add an article, Add a link, Upload from Photos, Take a photo, Add content from profile (Premium-only).

**Tier 1 — make first:**
1. **Add a link → verifyknot.io** (once deployed to Cloudflare Pages). One-tap proof of work for outreach recipients.
2. **Add an article → SDVOSB + PUF positioning piece.** Drafted (see below). Signals to gov buyers + warms cold outreach before reply.
3. **Add a post → marketing video** (once script finalized + shot). Native video = most LinkedIn reach.

**Tier 2 — fill in after:**
4. Add a link → ZKNOT company page / main site (if separate from verifyknot.io).
5. Add an article → deeper technical piece on ZK-LocalChain / attestation protocol, aimed at Schneier/Green-tier audience.

**Skip:** Upload from Photos, Take a photo, Add content from profile (Premium-only).

---

## How to Add the Article (mobile app editor is BROKEN)

The LinkedIn mobile app article editor opens an empty shell with no input field ("no content to display") — known long-standing bug. **Do it from a browser instead.**

**Option A — Desktop (best):**
1. linkedin.com → sign in.
2. Home feed → "Write article" (next to "Start a post").
3. Paste title + body. Format headings with toolbar. Strip the `**` markdown asterisks — they don't auto-convert.
4. Add a cover image (articles without one get less reach).
5. Publish.

**Option B — Phone browser (no laptop):**
1. Open Chrome/Safari (NOT the app).
2. linkedin.com → sign in.
3. Request Desktop site (Chrome: ⋮ → Desktop site; Safari: aA → Request Desktop Website).
4. Tap "Write article" on home feed.
5. Paste, format, publish.

**After publishing:** LinkedIn app → profile → Featured → "+" → "Add an article" → newly published article appears in list to pin.

---

## THE ARTICLE (final draft)

**Title:** Why Physical Authentication Is Still Broken — and What Cryptography Can Finally Do About It

**Subtitle:** Physical Unclonable Functions, zero-knowledge attestation, and a verification model that doesn't require trusting the manufacturer.

---

Every anti-counterfeiting system in wide use today shares the same fatal assumption: that the thing doing the authenticating can be trusted not to lie.

Holograms can be copied. Serial numbers can be cloned. RFID tags can be replayed. Even tamper-evident seals — the gold standard for high-value pharmaceuticals, defense components, and luxury goods — fail the moment an adversary controls the supply chain upstream of the seal application. The verifier is checking a claim made by the manufacturer, and the manufacturer is exactly who you'd need to distrust in a sophisticated counterfeiting operation.

This is not a new problem. It is, however, a problem that has quietly gotten worse. Counterfeit semiconductors are showing up in defense logistics. Counterfeit pharmaceuticals kill an estimated hundreds of thousands of people annually. Counterfeit aerospace parts have grounded aircraft. The economic damage is measured in the hundreds of billions, but the human cost is the part that should bother us.

The interesting question isn't *how do we make better seals*. It's *how do we authenticate a physical object without trusting anyone in the chain that made or shipped it*.

### What a PUF actually is

A Physical Unclonable Function is a physical structure whose micro-scale randomness is, by the laws of physics, impossible to reproduce intentionally — even by the entity that manufactured it. Think of the surface of a piece of paper under a microscope, or the random distribution of particles suspended in a cured polymer, or the variations in silicon doping across a chip die. The randomness is free, ambient, and present in every physical object whether we measure it or not.

The cryptographic insight is this: if you can measure that randomness reliably, you can derive a fingerprint from the object itself. Not from a label attached to the object. Not from a database entry trusting that the label is genuine. From the object.

A PUF-based authentication system, done correctly, has a property that no other physical authentication method has: the manufacturer cannot forge a second copy of the item, because the manufacturer doesn't know how. The randomness that defines the fingerprint emerged from the manufacturing process itself, not from a key the manufacturer generated and could regenerate.

This changes the trust model from "trust the issuer" to "trust the physics."

### The verification problem

The hard part has never been the theory. PUFs have been studied in academic cryptography for over two decades. The hard part is making verification work in the field, with a consumer's smartphone, in three seconds, against an attestation record the verifier doesn't have to trust.

This is where most PUF deployments have historically failed. They required specialized readers. They required online connections to a centralized database — which reintroduces exactly the trust problem you were trying to eliminate. They were brittle to lighting conditions, angle, wear, or environmental contamination.

A verification system that actually works in the wild needs four properties simultaneously:

1. The measurement must be reproducible across consumer-grade hardware without special equipment.
2. The attestation must be cryptographically verifiable without trusting the verifier's infrastructure.
3. The protocol must be tolerant of real-world noise — scratches, dust, lighting variance, camera differences — without losing the property that prevents forgery.
4. The verification result must be intelligible to a non-technical user in seconds.

These constraints fight each other. Reproducibility wants more tolerance; unforgeability wants less. Decentralization wants no trusted infrastructure; usability wants fast, definitive answers. The engineering work is in finding the operating point where all four hold.

### What we're building at ZKNOT

ZKNOT's verification protocol uses a consumer smartphone camera and any 100+ lumen white LED flashlight — equipment most people already own — to read a PUF surface under controlled but unsupervised conditions. The attestation is anchored to a local zero-knowledge chain, which allows verification without exposing the underlying fingerprint data and without requiring trust in a central database operator. Verification returns one of three states — VERIFIED, RETRY, or FAILED — within seconds.

The protocol is live. The first production attestation, ZK-6GUA-7DV, was verified at chain position zero earlier this year. The consumer verification destination is verifyknot.io.

We were granted SDVOSB certification through the SBA in early May 2026, which positions us to work with federal customers where supply chain authentication is moving from a compliance checkbox to a procurement requirement. The DoD's counterfeit electronic parts mandates, FDA pharmaceutical track-and-trace rules, and the broader push for supply chain provenance in critical infrastructure are all converging on the same need: authentication that doesn't break when the adversary is sophisticated.

### Why this matters now

There is a real argument that physical authentication is the last category of security that hasn't been re-founded on cryptographic primitives. We moved identity to public-key cryptography. We moved payments to cryptographic settlement. We moved communications to end-to-end encryption. The physical layer — the actual atoms that constitute the products people buy, the parts that go into the aircraft, the pills that go into the bottle — is still being protected with techniques that would be familiar to a 19th-century banknote engraver.

The technology to fix this exists. The standards conversation is starting to happen. The procurement pressure is building. What's missing is field-ready systems that work for a consumer holding a phone in a kitchen, not just for a researcher in a lab.

That's the gap we're closing.

---

— William Shane Wilkinson
Founder, ZKNOT, INC.
SDVOSB | SAM.gov: C4SKW13JPEL5

---

## Article — drafting notes / decisions

- **Length:** ~1,050 words. Substantive but finishable for a Schneier-tier reader.
- **Signature:** Full legal name per formatting rule + SDVOSB + UEI credibility footer.
- **Specifics included** as proof-of-build: 100+ lumen LED, smartphone camera, three-state result (VERIFIED/RETRY/FAILED), ZK-6GUA-7DV at chain position 0, verifyknot.io.
- **Deliberately did NOT** name-drop or quote Green/Schneier/Pfefferkorn — would read sycophantic and hurt outreach. Article earns the meeting on merits.
- **Most reshareable line:** "the last category of security that hasn't been re-founded on cryptographic primitives."

---

## Open / Next Actions

- [ ] Deploy verifyknot.io to Cloudflare Pages → then add as Featured link.
- [ ] Publish the article via browser (NOT mobile app). Add cover image (ZKNOT logo or PUF surface close-up).
- [ ] Pin published article to Featured.
- [ ] Finalize + shoot marketing video → add as Featured post.
- [ ] (Tier 2) Draft deeper technical article on ZK-LocalChain / attestation protocol.
- [ ] Optionally: draft short LinkedIn announcement post to drive clicks to the article (offered, not yet written).
