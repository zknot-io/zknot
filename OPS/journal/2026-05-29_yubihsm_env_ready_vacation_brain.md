# 2026-05-29 — YubiHSM env ready; SBIR pivot considered and rejected; vacation brain

**Author:** William Shane Wilkinson
**Project:** ZKNOT, INC.
**Status:** Pre-ceremony prep complete. Awaiting hardware delivery.
**Related:**
- ZKNOT-DOC-HW-003 (Provisioning Station Architecture & Build)
- ZKNOT-DOC-GOV-002 (NAICS Contract-Hunting Brief)
- Prior journal: 2026-05-22_provisioning_station_and_sbir_fork.md (if not yet written, backfill from this entry)

---

## Today in one sentence

YubiHSM 2 v2.4 ordered ($650, direct from Yubico), `yubihsm-shell 2.6.0` and `yubihsm-connector 3.0.5` installed and verified on Debian Trixie, considered pivoting to an adjacent SBIR topic during vacation downtime and decided against it, station prep is gated on finishing the Yubico docs and answering the auth-key vs wrap-key conceptual checkpoint before the ceremony.

---

## Decisions logged

### 1. SKIP June 3 SBIR cycle — no genuine topic fit

Surveyed all 131 topics in the DoD SBIR 2026 solicitation umbrella (CSO + BAA, USAF / Army / Navy / DLA / DARPA / SOCOM / OSD / DHA). Evaluated four in depth:

- **ARM26BX01-NV001 (In Transit Visibility Blockchain):** 1-of-9 capabilities match. Requires location tracking hardware, multi-modal comms (satellite/cell/internet), 15-min update telemetry, <3-min COP latency, integration with five named enterprise systems (TCAIMS-II / IBS / GATES / CMOS / CPCE), and interop with AFRL's existing distributed ledger. ZKNOT has tamper-evident chain of custody and not much else on this list. Decision: skip.
- **DLA26BZ02-NV008 (US Based Fixture Development and Manufacturing):** Initially flagged Tier 1 by Claude based on title pattern-match ("fixture" + "DLA" + "US-based"). Full topic read revealed this is mechanical fixtures for Navy ship maintenance (Auxiliary Seawater test blanks, weapons shipping cradles, vacuum sanitary pump support fixtures, Electric Boat drawings, NAVSEA part numbers). Requires CAD reverse-engineering, machining, material qualification, JCP certification, and submarine maintenance domain expertise. Decision: skip. *Learning: title-level pattern matching is unsafe; always read the full topic before tier-ranking.*
- **DLA26BZ02-NV005 (Defensive Cybersecurity through Agentic AI):** Stretch fit. Worth revisiting if any other DLA topics drop in the late-summer wave; not worth a June 3 forced submission.
- **ARM26BX01-NV002 (Modular Payloads for UAS):** 40 Q&A questions logged — heavily over-subscribed. ZKNOT's authentication angle is adjacent, not central. Decision: skip.

The post-reauthorization wave that articles predicted would be heavy in hardware-security topics did not materialize on this drop. The 131-topic set is heavy on UAS, photonics, sensors, materials, medical, AI/ML. ZKNOT's niche (cryptographic hardware provenance, secure-element provisioning, hardware-rooted trust) didn't appear in force.

**Decision:** Skip June 3 entirely. Target the late-summer / FY26-end wave (agencies must obligate FY26 funds before September 30 — predictable topic drop in June–August). Show up with a finished and demonstrated provisioning station + validated PowerVerify + real per-device records, not slideware.

### 2. NO pivot to an unrelated SBIR domain

Considered during vacation whether to write a "foot in the door" proposal on a GPS, PNT, autonomy, or workflow-automation topic just to learn the proposal process and shake out the format. Three topics flagged as theoretically learnable given proven fast spin-up ability (the ATECC608B diagnostic in 2 months as the precedent): DLA26BZ02-NV005, DAF26BZ01-DV007 (CHORD - Collaborative Human Autonomy Operational Review), ARM26BX02-NV005 (Multifrequency PNT Antenna Solution).

**Decision:** Not pivoting. ZKNOT's existing position (14-17 provisional patents, SDVOSB, active SAM, working code, hands-on hardware credibility, coherent thesis validated by three independent architecture reviews) is more footing than 95% of solo founders ever achieve. Throwing it away to chase a stretch proposal in a domain with no transferable credibility burns TPOC attention and produces nothing reusable. Patents take 12-18 months to issue; reviewers read technical volumes, not patents. The qualifications criterion in SBIR review weighs prior demonstrable work in the topic area — finance + military operations + 2 months of hardware self-teaching does not qualify ZKNOT for PNT antenna design or autonomy evaluation, regardless of how fast I can absorb new domains.

The right tuition payment is a proposal where I have a real (even partial) angle. The right time is when a topic that actually fits ZKNOT drops. The right target is the late-summer wave.

*Important caveat to my own decision-making: Claude pushed back hard on the pivot question with a "this is the seventh time you've moved off the discomfort" framing. The framing was wrong — I was on vacation, couldn't access the bench, and was legitimately scouting in the time available. But the underlying conclusion (don't pivot) was right for separate reasons. Worth holding both: the diagnosis of avoidance was incorrect; the recommendation against pivoting was correct. Lesson: pushback from any source is one input among many, not a verdict — but it can still be load-bearing even when its framing misreads me.*

### 3. CA hierarchy: DEV vs PRODUCTION separation from day one

The $10 community-chip / value-ladder idea makes this load-bearing. The PowerVerify-validation chip will be a DEV chip with "ZKNOT-DEV" in the cert. Any federal-facing units later will be issued under a separate PRODUCTION CA, ideally on a second YubiHSM2 generated via offline root ceremony. The two hierarchies never share a key. This is fixed now to avoid contaminating the production trust chain later.

### 4. Throughput target: 100 chips over 6 months, station capable of scaling to 500 without redesign

Hand-seated SOIC-8 socket, no panel fixture, no automated handling, ~5 min/chip, 10-12 chips per session, 2-3 sessions per month. The "could do 500 from day one" panel-fixture build is post-June-3 buildout, deferred until demand justifies it.

### 5. HSM acquisition: non-FIPS v2.4, not FIPS v2.2

Ordered the $650 YubiHSM 2 v2.4 from Yubico direct, not the $950 FIPS v2.2. Rationale: FIPS 140-2 validation on the FIPS unit expired May 2, 2026 (Yubico's own announcement); FIPS 140-3 validation "expected Q2 2026" but not yet achieved. Paying $300 extra for an expired cert is poor capital allocation. No current ZKNOT contract requires FIPS-validated cryptography; Phase I CMMC posture is Level 2 self-attestation, which doesn't require FIPS HSMs in scope. The v2.4 is also newer firmware (asymmetric backup support, updated crypto library from YubiKey 5.7 release). If FIPS becomes contractually required later, buy the FIPS 140-3 version when it actually exists.

---

## Environment ready

```
yubihsm-shell 2.6.0
yubihsm-connector v3.0.5
OS: Debian Trixie 13
Shell: zsh
```

Connector installed as systemd service (`yubihsm-connector.service`, listening localhost:12345 only). Leaving enabled — localhost-only attack surface is acceptable, and one fewer manual step during ceremonies.

---

## Pending before ceremony (the gate to touching the device)

1. **Bench location decided and fixed.** One location, same orientation every session.
2. **HSM-at-rest location decided.** Fire safe / locked drawer / equivalent. If a small Amazon order is needed (e.g., UL-rated home fire safe), order before device arrives.
3. **Yubico docs read in order:** Quick Start tutorial → Admin Guide → Backup and Restore. Backup and Restore read twice.
4. **Conceptual checkpoint answered in own words: what is the difference between an authentication key and a wrap key, and why are both needed?** This is the gate. If the answer is fuzzy, do not generate the CA key. Slow down and re-read.

---

## What I learned about myself this stretch

Two months ago I didn't know what an ATECC608B was. I now know more about its failure modes (MCP2221A stop-pulse glitches, DM320118 supply pinch, Trust&GO Factory Special Order unavailability, TFLXTLS slot config nuances) than the vast majority of engineers who've heard of the chip. The capability to absorb a hard hardware domain fast is real and demonstrated. That capability is what makes the "no pivot" decision land correctly: the answer isn't "I can't learn GPS" — the answer is "the credibility I've built is in *this* domain and is non-transferable."

The vacation scout was also a real thing to notice: when the next step on the current path got boring (read Yubico docs, decide where the HSM lives), my brain went searching for fresh starts. That's not weakness; it's how creative minds work. But the *pattern* is worth respecting — when I notice myself reaching for a pivot because the current step feels boring, the right move is usually to finish the boring step, not pivot.

---

## Personal monopoly thread

What's accumulating across this work is a specific and rare expertise: solo-founder-level mastery of the boring, irreversible parts of hardware provisioning, told from the perspective of someone who came in cold and learned it hands-on. There are tens of thousands of "security startup founders." There are very few people who can credibly write a runbook for "how a solo SDVOSB stands up a YubiHSM-backed provisioning CA from scratch, with backup ceremony and the full key-custody story." That's the moat forming, whether ZKNOT-the-company is the vehicle that monetizes it or not.

Curiosity to follow: not "how do I build PowerVerify faster," but "how do I capture what I'm learning into a transferable artifact that another founder couldn't reproduce by Googling." That's the personal-monopoly question.

---

## Next session

- HSM arrives in 2-5 days
- Complete Yubico docs and answer auth-key vs wrap-key checkpoint
- Finalize bench + HSM-at-rest locations
- Key ceremony when all three above are done — single focused 2-hour block, no interruptions, no rushing
- Provision first sacrificial chips to prove the lock step before any chip I care about
- Then provision the chip that validates PowerVerify

---

## Concepts ticked off so far

- [x] **CA hierarchy: DEV vs PRODUCTION** — decision made and documented
- [x] **NAICS 334290 vs 541512 as primary** — services-first chosen as current primary
- [x] **CSO vs BAA SBIR vehicles** — surveyed both, understand the difference

## Concepts still open

- [ ] **Authentication key vs wrap key** — gate to ceremony
- [ ] **Security domain** — read in Admin Guide
- [ ] **M-of-N wrap key backup** — read in Backup and Restore
- [ ] **On-chip key generation vs imported key**
- [ ] **Wrap-export-under-key** — the backup pattern
- [ ] **Irreversible provisioning gate** — the patent angle
- [ ] **DEV chip cert naming convention**
- [ ] **Per-device record / device passport**
- [ ] **Fixture signing identity**
- [ ] **Sources Sought / RFI vs solicitation**
- [ ] **SDVOSB sole-source authority (FAR 19.1406)**

---

*— end of entry —*
