---
date: 2026-05-29
topic: SDVOSB sole-source (FAR 19.1406) — viability and sequencing
author: William Shane Wilkinson
workstream: biz
tags: [sdvosb, far-19.1406, sole-source, federal-bd, sequencing, gating]
status: parked
---

# SDVOSB Sole-Source (FAR 19.1406) — Viability & Sequencing

## TL;DR

Looked at FAR 19.1406 SDVOSB sole-source as a federal BD vehicle. Thresholds
verified against acquisition.gov (FAC 2026-01, eff. 2026-03-13): **$5M** ceiling
for non-manufacturing NAICS, **$8.5M** for manufacturing NAICS. The vehicle is
real and ZKNOT's {SDVOSB} ∩ {patented unique crypto capability} intersection is a
genuine basis for a CO's "competition unlikely" finding. **But it's a
contracting-officer-invoked tool, not something I can pull, and it's gated on two
things I don't have yet: a demonstrable signing/attestation capability and a
passable responsibility determination.** Decision: **federal BD is parked until I
can cryptographically sign/attest in a way I can show a program officer.** No point
pitching a unique cryptographic capability I can't yet demonstrate. Hardware-first.

## Context — what prompted this

Came in on the framing that 19.1406 is "the most underused federal vehicle in the
toolbox." Tested that framing rather than accepting it. The number was right; the
implied "open door" was not.

## What's verified (promote to km/systems — see Decisions)

These are durable reference facts, not journal material — flagging for promotion to
a systems note rather than living here.

- **Thresholds (primary source, acquisition.gov, FAC 2026-01):** $5M non-mfg /
  $8.5M mfg. Which one applies is decided entirely by the requirement's NAICS code.
- **It's the CO's tool.** A sole source requires the CO to document a finding that
  they have no reasonable expectation of offers from two or more SDVOSBs. That
  finding is driven by *their* market research, upstream of any award.
- **Five conditions of 19.1406(a)** — the one that bites a small new firm is #4:
  the CO must find ZKNOT a *responsible* contractor (capacity, past performance,
  ability to perform). Zero past performance makes a large first award hard to sign.

## Why it's actually "underused"

Not because COs don't know it exists. Because a sole source is *more* audit exposure
for the CO than running a set-aside competition. Competition is the risk-free
default — nobody second-guesses a CO for competing. A sole source means the CO
personally signs a justification for *not* competing. So "underused" = "the CO has
to take on risk to use it." The vehicle opens only when I've removed that risk for a
specific CO with a specific requirement. That reframe is the whole game.

## The gating insight (today's real decision)

The entire pitch rests on "patented, unique cryptographic-authenticity capability —
competition is unlikely." That sentence is only true and only *defensible* if the
capability exists and can be demonstrated. Right now ZKNOT cannot cryptographically
sign/attest in a form I can put in front of a program officer — the hardware pivot
(FT260 bridge + bare TrustCUSTOM provisioning) is mid-flight. Chasing BD before that
is selling a moat I can't yet stand in.

Tradeoff acknowledged (both sides):
- **Park it:** focus stays on the capability that makes every later BD claim true;
  no wasted relationship capital pitching vaporware; no risk of a CO market-research
  conversation I can't back up. Cost: BD clock doesn't start, no early past-performance.
- **Pursue in parallel:** could start warming a requirement-owner relationship now
  so the pipeline isn't cold when hardware lands. Cost: thin credibility today, and
  my attention is the bottleneck — splitting it likely slows the hardware that
  unblocks everything.
- **Chosen:** park, because the gate is real and self-imposed sequencing beats a
  half-credible pitch. Revisit the moment signing is demonstrable.

## Decisions

1. **Park federal SDVOSB BD** until ZKNOT can demonstrably sign/attest
   cryptographically (i.e., hardware pivot produces a working provisioned device +
   live attestation through the existing api.zknot.io path).
2. **When resumed:** target requirement-*owners* (program offices with a real
   supply-chain-integrity / anti-counterfeit pain), not contracting shops. Go
   small-first for a clean CPARS rating before reaching for the $5M ceiling.
3. **Promote FAR 19.1406 mechanics** out of this journal into
   `~/ZKNOT/3_OPS/km/systems/federal-contracting.md` (thresholds, the five
   conditions, CO-risk reframe, and the 6.302-1 "only one responsible source"
   overlap worth studying).

## Next actions (deferred until un-parked)

- [ ] Confirm ZKNOT's primary SAM NAICS code and whether a manufacturing-series
      (334xxx) NAICS legitimately fits a provisioning/device requirement → decides
      $5M vs $8.5M ceiling.
- [ ] Draft capability statement once a signing demo exists.
- [ ] Study FAR 6.302-1 overlap with 19.1406 (moat-within-a-moat).

## Open questions

- Does the VA "Vets First" / VAAR ordering give a materially easier path than the
  FAR for a first award? (Unverified — check VAAR primary source before relying.)
