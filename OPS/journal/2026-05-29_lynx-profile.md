---
date: 2026-05-29
topic: lynx-profile
workstream: biz
status: in-progress
tags: [lynx, dow, osbp, federal-bd, profile, capability-statement]
related:
  - 3_OPS/km/systems/lynx.md
---

# 2026-05-29 — LYNX ALLYANCE Profile Build

## TL;DR
Verified LYNX (lynxconnect.io) is a legitimate Department of War / Office of Small
Business Programs platform — a readiness/discovery "front door," NOT a procurement
portal. Began building the ZKNOT company profile: drafted positioning, ranked
competency tags (leading with custom tags over the generic taxonomy), wrote the
Company Snapshot, and worked the FOCI/security-screening section (answer is "No"
across the board for a pre-award, US-owned, single-founder SDVOSB with no
clearances). LYNX is a parallel BD asset, not a deadline. It must not pull focus
from the live priority.

## Decisions
1. **Treat LYNX as a build-once BD asset, not a milestone.** It is a front door for
   readiness/discovery; formal registration + solicitations still flow through
   SAM.gov / standard procurement. No clock attached.
2. **Answer the readiness assessment honestly as an early-stage new entrant.** An
   inflated baseline produces an AI roadmap pointed at the wrong gaps. ZKNOT is
   literally LYNX's target user (strong tech, no contracting history) — own that.
3. **Lead every tag category with a CUSTOM tag.** The canned LYNX taxonomy has no
   "cryptography," "hardware authentication," or "PUF." Generic options flatten the
   moat. Custom field = where the differentiation gets stated.
4. **Do not claim track-record tags** (On-Time Delivery, Client Retention, 24/7,
   Scalability). They imply an operating history ZKNOT doesn't have. Capability
   claims = honest; delivery claims = overreach with the exact audience that checks.
5. **Enter all sensitive identifiers myself, directly in the platform.** UEI / CAGE /
   EIN never go into a chat. Confirmed: the only field that surfaces CAGE in the
   screening section is the facility-clearance table, which is skipped entirely by
   answering "No" to the DCSA question.

## Session Narrative

### Verification (did this first, before entering any identifiers)
LYNX confirmed real via official .gov sources (war.gov, business.defense.gov) and
the APEX Accelerator network. Launched Jan 2026 by DoW OSBP. Positioned by ASW(IBP)
Michael Cadenazzi and OSBP Director James Mismash as a tool to "turn readiness into
action." Target users: new entrants, non-traditional suppliers, growing contractors
with strong tech but limited defense-navigation experience. → Promoted full facts to
`km/systems/lynx.md`.

### Profile content drafted (paste-ready — reproduced here because chat is being deleted)

**Positioning line**
> ZKNOT, INC. builds cryptographic hardware that lets anyone verify a physical item
> is authentic and untampered — using the device's own silicon as an unclonable
> identity, confirmed by a live, human-actuated challenge.

**Ranked tags**

*Key Differentiators*
1. Hardware-Rooted Authenticity Verification (custom)
2. Patented Human-Actuated Cryptographic Attestation (custom)
3. Security & Compliance Focus
4. Technology Enablement
5. Mission-Focused Support

*Core Competencies*
1. Cryptographic Hardware Engineering (custom)
2. Cybersecurity Solutions
3. Compliance and Security
4. Systems Integration
5. Software Services

*Key Capabilities*
1. Research & Development (R&D)
2. Product Development
3. Prototyping & Testing
4. Software Development
5. Cybersecurity

*Core Values*
1. Trustworthiness
2. Integrity
3. Security
4. Data Privacy
5. Mission Focus

**Company Snapshot (~210 words, under 250 cap)**
> ZKNOT, INC. is a service-disabled veteran-owned small business (SDVOSB) developing
> cryptographic hardware that verifies whether a physical item is authentic and
> untampered. The technology uses a device's own silicon as an unclonable identity —
> a physical unclonable function (PUF) — confirmed through a live, human-actuated
> cryptographic challenge. This addresses a documented defense concern: counterfeit
> and untrusted microelectronics in the supply chain.
>
> ZKNOT's patent-pending architecture pairs PUF-based hardware identity with a
> finite-state-machine-gated verification protocol, producing tamper-evident proof
> that a real person verified a genuine, uncloned device at a specific moment in
> time. A zero-knowledge attestation backend records chain-of-custody without
> exposing sensitive data.
>
> Founded and led by William Shane Wilkinson, ZKNOT operates across hardware,
> firmware, software, and intellectual-property workstreams from Salt Lake City,
> Utah. The company holds an active SAM.gov registration and SDVOSB certification
> through SBA VetCert.
>
> ZKNOT is an early-stage, non-traditional supplier with deep technical capability in
> hardware assurance, anti-counterfeit provenance, and zero-trust device
> verification — capabilities aligned with Department of War priorities in
> microelectronics security and supply-chain integrity. The company seeks
> mission-aligned partners and opportunities to bring hardware-rooted authenticity to
> defense applications.

### Advanced Business Info / FOCI screening — answers entered
All "No" for ZKNOT's position:
- Industry-specific licensing → No (crypto dev not licensure-regulated; confirm if PE-stamping)
- Construction → No
- DCSA Facility Clearance → No (NOT "Hold" — no open action). Skips facility table.
- FOCI agreements → No
- Investigated for unauthorized tech transfer / foreign influence → No
- SF-328 ever completed → No
- Regulatory actions (CFIUS/SEC/debarment) → No
- Felony (company/connected party) → No
- DPAS priority-rated contracts past 3yr → No
- Classified contract under EO 12958 past 5yr → No
- Nat'l defense/homeland/security contract past 3yr → No
- IP/tech transfer to foreign country of concern past 5yr → No

Judgment calls (decide to actual plans, not default):
- Foreign travel → likely No today; Yes if attending int'l crypto conf (RWC, CCC, Eurocrypt) on company business
- Trade shows/conferences → Yes if intending to attend defense/crypto events (no downside; signals engagement)

## Verify Before Federal Filing (standing rule — do not take from chat)
- [ ] **Provisional app number format** — pull exact styling from USPTO filing receipt
      ("Application No. 63/960,933"), not memory. Deliberately omitted from snapshot.
- [ ] **"Service-disabled veteran-owned small business"** — confirm exact wording
      matches the VetCert certificate before it goes government-facing.
- [ ] **Registered NAICS/PSC codes** — keep LYNX consistent with what's already in
      SAM.gov. Candidates discussed: PSC 5810; NAICS 334413, 541715, 541512, 541330.

## Open Threads / Next
- [ ] Products & Services section (not yet drafted)
- [ ] Past Performance section — the hard one for pre-award; needs the honest
      "no prior contracts" framing that doesn't read as a blank
- [ ] Cybersecurity / FCI-CUI section — where ZKNOT's real readiness gaps surface and
      where the AI roadmap will point. Highest-signal section. Prep before entering.
- [ ] Contact APEX Accelerator Regional Manager — free advisor, knows regional buyers.
      Higher leverage than most of this week's list if never used.

## Strategic Note
LYNX is a parallel track. The genuinely time-sensitive work is elsewhere. Revisit
this entry when deciding how much more time LYNX earns vs. the active priority —
the honest question is "parallel track or distraction until the priority clears?"
