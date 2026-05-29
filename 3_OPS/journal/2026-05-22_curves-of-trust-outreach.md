# 2026-05-22 — Curves of Trust: Direct Outreach Plan

Captured from a chat thread before deletion. Project: **Curves of Trust** (cryptography history book), NOT ZKNOT. The book is structured in parts (Part I = ECC origins; Part III = the "trust the math, not the parameters" doctrine + Snowden/Dual_EC_DRBG policy era; Part IV = post-quantum transition).

## Purpose of this file
A handoff list of people to contact for primary-source interviews, what to ask each, how to approach them, and the order to do it in.

---

## Outreach sequencing (the key takeaway)
1. **Green and Schneier first** — they'll point to who else to talk to and which questions matter.
2. **Koblitz, Miller, Bernstein** — the named protagonists.
3. **Specialized narrow asks** (Solinas, Menn, Mosca) once the draft is more advanced.

Do NOT contact everyone at once. The book improves between conversations; later interviewees benefit from earlier ones.

## How to structure each ask
- Send the specific chapter they'd care about, not the whole book.
- Ask ONE specific question in the email, not a list.
- Offer to send the relevant section back for fact-check before publication. **This is the single biggest unlock** — academics engage with someone who will credit them and let them correct errors.
- Do NOT ask for a phone call in the first email. Ask for a written response, then escalate to a call if they're engaged.
- Mention who you've already spoken with. Cryptography is a small field; warm-intro chains beat cold-email sequences.

---

## Tier 1 — Highest value, reasonable likelihood of response

### Neal Koblitz — University of Washington (emeritus)
- **Why:** Co-inventor of ECC. His 1985 recollections are the missing primary source for Part I.
- **Contact:** UW math department directory (public email).
- **Approach:** Approachable, has done many interviews. Politically opinionated (math education, NSA). Engage him as a person with views.
- **Ask:** (1) The Odlyzko letter — did he keep a copy, what did it say? (2) Why ECC sat dormant 20 years — he's hinted NSA may have known earlier and classified internal work; press on this. (3) His reaction to Dual_EC_DRBG. (4) The patent question — any regrets about not patenting?
- **Risk:** Prickly with journalists who haven't done homework. Send the draft first; read his opinion pieces before writing.

### Victor Miller — Independent / formerly IBM Research, IDA CCR
- **Why:** The other ECC co-inventor. IBM industrial-research path, less documented publicly than Koblitz.
- **Contact:** Personal website, direct email listed.
- **Approach:** Lower profile, historically responsive to serious inquiries. Frame as serious history, not journalism.
- **Ask:** (1) IBM context — pressure to patent? Did IBM consider it? (2) Did he and Koblitz ever discuss the simultaneous discovery / ever meet about it? (3) His read on the secp256k1 selection — insight into Satoshi's choice? (4) Awareness of NSA interest in elliptic curves before 1985?
- **Risk:** Older, may be selective.

### Daniel J. Bernstein (djb) — UIC / Ruhr University Bochum
- **Why:** Designed Curve25519, ChaCha20, Poly1305, Ed25519. Architect of the post-2013 parallel infrastructure. Active critic of NIST PQC standardization. Primary source for the Part III doctrine; relevant to Part IV.
- **Contact:** cr.yp.to lists contact info. Responsive, but on his own terms.
- **Ask:** (1) Curve25519 design process — choices made, alternatives rejected, explicit goal re NIST. (2) Current views on ML-KEM / ML-DSA — he's filed public objections; read them first. (3) His read on the Juniper incident. (4) His lawsuit/FOIA work against NIST.
- **Risk:** Notoriously direct; reply may be a list of corrections rather than a conversation. Feature, not bug.

### Matthew Green — Johns Hopkins  ← START HERE
- **Why:** Wrote the most-read public analyses of Dual_EC_DRBG and Juniper. Co-author on the academic paper reverse-engineering the Juniper backdoor. Accessible.
- **Contact:** Public JHU email; also Bluesky/Twitter, DMs sometimes work.
- **Approach:** Working academic who also writes for general audiences — gets the project fast.
- **Ask:** (1) Current attribution thinking on Juniper — field gossip more specific than what's published. (2) Harvest-now-decrypt-later — who's collecting, how much. (3) Corporate aftermath at RSA Security after the Reuters story.
- **Risk:** Busy. Be specific. Don't request a long interview — request a 30-min call after he's read a specific chapter.

### Bruce Schneier — Harvard Kennedy School, Inrupt  ← START HERE
- **Why:** Wrote the original 2007 Wired piece on Dual_EC_DRBG. On the Snowden document review team in 2013. Defining public voice on crypto policy for 20 years.
- **Contact:** schneier.com. Answers selectively but reliably for serious inquiries.
- **Approach:** Has written multiple books; understands book vs. journalism interviews.
- **Ask:** (1) What he saw in the Snowden docs that hasn't been published — he can characterize even if he can't share specifics. (2) Internal reaction at major tech companies 2013–2014. (3) Current read on the post-quantum transition (he's skeptical of the urgency).
- **Risk:** Says no to vague asks. Have a specific question and a specific draft chapter.

---

## Tier 2 — Strong value, may take more work

- **Michele Mosca** — Waterloo / IQC / evolutionQ. The Mosca's-inequality framework is his; also has business-side PQC perspective. Ask: calibration of X, Y, Z for different sectors; whether consensus shifted post-Willow. Frame as wanting to use his framework correctly, then expand.
- **Tanja Lange** — TU Eindhoven. Co-author with Bernstein on Curve25519 ecosystem and Dual_EC_DRBG analysis; primary PQC voice. A more measured counterpart to djb, often easier on specifics.
- **Stephen Checkoway** — Oberlin. Lead author on the academic Juniper paper; knows the reverse-engineering cold. Specific technical questions; would likely enjoy revisiting it.
- **Hovav Shacham** — UT Austin. Co-author on Juniper paper; among the first to publicly raise concerns about NIST curve seeds.
- **Riana Pfefferkorn** — Stanford Internet Observatory (**verify current affiliation — she has moved**). Crypto policy specialist; strong on legal/political dimensions of Snowden and post-2013 standards reform. Useful for Part III policy framing.
- **Joseph Menn** — Reuters / Washington Post. Wrote the Dec 20, 2013 story on the RSA $10M payment. Ask: what he couldn't print — original sources were "people familiar with the deal," implications that fit a book but not a news story.

---

## Tier 3 — Specific narrow asks

- **Jerry Solinas** — formerly NSA, retired. Chose the NIST P-256 seed. Has declined to discuss publicly; worth one polite ask, likely a no. Narrow ask: where did the seed come from?
- **Whitfield Diffie** — father of public-key crypto, witness to the whole era. Approachable in person; harder by email. Best path: meet at RSA Conference or RWC, not cold email.
- **Ralph Merkle** — third inventor of public-key crypto (Merkle puzzles, 1974, before Diffie-Hellman). Now on cryonics/fringe topics. Still has clear memories of the era.
- **Adi Shamir** — Weizmann. The "S" in RSA. Views on ECC, the NSA, and post-quantum. Approachable in academic settings.

---

## Open next action (from the chat, not yet done)
Drafting the first outreach emails to **Green** and **Schneier** was the recommended immediate next step. Those drafts were NOT written before the thread was closed — pick this back up after the trip.

## To-do flagged in the plan
- Verify Pfefferkorn's current affiliation before contacting.
- Read djb's public PQC objections and Koblitz's opinion pieces before drafting to either.
