---
date: 2026-05-29
type: journal
topic: puf-evidence-procurement-thesis
workstream: [biz, ip, fw]
tags: [axon, sbir, fre-707, fre-901, puf, personal-monopoly, strategic-thesis, deepfakes]
related:
  docs:
    - 99_REFERENCE/ZKNOT_PUF_Evidence_Procurement_Reading_Packet.pdf
    - 3_OPS/km/systems/courtroom-evidence-and-attestation.md
  patents:
    - PAT-001 (App #63/960,933)
  tasks: [see Next Actions section]
---

# 2026-05-29 — PUF + Federal Evidence + Federal Procurement: The Personal Monopoly Thesis

## TL;DR

- Worked through whether Axon is a real customer/partner/target for ZKNOT; the honest answer is **yes**, but the framing is "your AI feature roadmap is on a Rule 707 collision course," not "buy our chip."
- The bigger insight is that the intersection of **PUF cryptography + Federal Rules of Evidence + SDVOSB/SBIR procurement access** is a genuinely uncrowded space and is the personal monopoly worth building deliberately.
- Built a 24-page flight reading packet (`ZKNOT_PUF_Evidence_Procurement_Reading_Packet.pdf`) covering the authenticity crisis, FRE primer for engineers, defense-layer stack, market map, and a self-monopoly worksheet.
- Built a companion km/systems doc (`courtroom-evidence-and-attestation.md`) so the durable reference material is grep-able from the vault, not trapped in a PDF.
- **Hard decision: do nothing on any of this until SBIR Phase I is submitted June 3.** Everything else gets `due:2026-06-04` or later. The asymmetry of a missed deadline vs. polished marketing is total.

## Decisions

1. **SBIR Phase I submission is the sole priority through June 3.** No outreach drafting, no paper writing, no Axon BD, no Farid email until after submission. Distraction here is uniquely expensive.
2. **The SBIR narrative gets a Rule 707 / 901(c) revision pass before submit.** Not a rewrite — one targeted pass adding the evidentiary-admissibility framing to Significance, Technical Approach, Commercialization, and Phase II vision sections.
3. **The personal monopoly to deliberately develop is the three-vocabulary intersection.** PUF cryptography fluency + Federal Rules of Evidence literacy + SDVOSB/SBIR procurement access. Almost nobody owns all three. The "monopoly product" is durable writing that translates between them.
4. **Hany Farid is the highest-leverage outreach target identified in this thread.** Above Green, Schneier, or Pfefferkorn for pure leverage — he's the most-cited courtroom forensics expert in the US and his endorsement creates downstream gravity nothing else can match. Outreach drafted post-June-3.
5. **Counterintuitive market lane to evaluate after SBIR: pitch ZKNOT to Axon's competitors (Reveal Media, Getac, WatchGuard) as their differentiator, not to Axon as a component supplier.** Smaller partner, larger share of value, faster decision cycle, contrarian positioning.
6. **Defer (not kill) Axon BD outreach.** They're a real customer, but the path is through SBIR-backed federal references and Rule 707 timeline pressure, not direct cold outreach.

## What changed in my thinking

### The Axon question was the wrong question

Started this thread with "deep-dive Axon and give me 5 ways to value them." That's the wrong frame for where ZKNOT is. The right question — which surfaced two messages in — is **"what does ZKNOT have that moves Axon's needle, and is that the right needle to be moving?"**

Axon's market cap is ~$31B against ~$2.8B revenue. Their entire valuation rests on the legal trustworthiness of their evidence platform. Their current public authenticity story (Merkle-tree hash at capture, SHA-2 on upload, FedRAMP High, SOC 2) is excellent against post-capture tampering and silent on three problems:

- Device identity (the hash doesn't prove the file came from a specific physical device)
- Capture-path integrity (no attestation that bits came from the image sensor, not an injected feed)
- Key extraction (no public claim of PUF-grade non-extractable keys)

So ZKNOT does have something that moves their needle. But "selling to Axon" is the third-best framing of the opportunity. The first-best framings are:

- **Selling to Axon's competitors** as their authenticity differentiator
- **Selling to federal customers via SBIR** with Axon as a downstream commercial multiplier
- **Setting the standard** via a Rule 707 public comment, arXiv paper, and Federal Public Defender brief — which forces Axon to buy whether they want to or not

### The legal vocabulary is the missing piece

The honest gap in my own competence going into this was Federal Rules of Evidence literacy. Rule 702, 901, 902(13)/(14), Daubert, and proposed 707/901(c) are the operating language of the courtroom and I couldn't have used them in a Schneier-tier conversation a week ago. The reading packet's Unit 2 is the highest-leverage section because it closes that gap.

Key things now committed (durable detail in the km/systems doc, summarized here):

- **Rule 707** subjects machine-generated output to Daubert reliability — final committee vote May 7, 2026; if approved, takes effect no earlier than Dec 1, 2027.
- **Proposed Rule 901(c)** would shift the authentication burden to **preponderance of evidence** when the opponent challenges electronic evidence as AI-generated. Hash chains alone don't answer this; hardware-rooted attestation does.
- **Rules 902(13) and 902(14)** are the existing self-authentication on-ramp for cryptographic evidence (since 2017). A future 902(15) for hardware-attested capture is plausible and being there as the reference implementation when it lands is the long game.
- **Daubert reliability factors** map cleanly to standard cryptographic primitives (peer review, error rates, NIST standards, general acceptance). PUF-based attestation built on boring crypto is structurally easier to Daubert-qualify than AI-detection-of-AI tools.

### The sensor-injection problem is the architectural test

The most uncomfortable insight from the thread. The sensor-injection attack — using an HDMI-to-CSI-2 adapter to inject synthetic video into a trusted capture device's sensor bus — defeats every defense layer above PUF-with-sensor-attestation. Layer 1 (software signing), Layer 2 (C2PA), Layer 3 (TEE-based signing), and even Layer 4 (HRoT with attested boot) all sign whatever the capture pipeline delivers, without proving the pipeline data came from the physical sensor.

**PUF alone does not automatically defeat this.** A PUF-derived key signing whatever the pipeline hands it is no better than a TEE key signing the same thing. PUF beats sensor injection only if the PUF system *also* attests the sensor path — cryptographic challenge to the sensor, physical sealing, integrated sensor+PUF die, or equivalent.

This means there's an honest self-assessment to do on ZKNOT's current architecture: does the design close this gap or not? If yes, that's the moat and it needs to be documented as a formal threat model. If no, the threat model exposes the work that needs to be designed in. Either way, "we use PUFs" is not by itself a Layer-5 claim. The packet has a 10-question checklist for self-rating; do it on the flight.

### The personal monopoly framing matters more than any single deal

The most important shift in this thread was the move from "how do I sell to Axon" to "what specific intersection am I uniquely positioned to own." The answer:

- Almost everyone in PUF research is a chip-design or supply-chain-anti-counterfeit person, not an evidence-law person.
- Almost everyone in evidence tech is software-only, with no hardware fluency.
- Almost everyone in either is a commercial company with no federal procurement access.
- Almost nobody is veteran-owned, SDVOSB-certified, SAM.gov-active, and on an SBIR clock right now.

The four-way intersection (PUF + FRE + SDVOSB/SBIR + active patent prosecution at this exact regulatory moment) is uncrowded enough that "build a defensible moat" stops being aspirational and starts being a real plan if I keep writing publicly and keep submitting to federal vehicles. The PDF's Unit 5 worksheet is the forcing function — answer those ten questions by hand on the flight.

## The five needle-moving ideas (ranked, for post-June-3 work)

Generated and filtered down to five from a ~25-item brainstorm. Ranked by leverage, not effort:

1. **Hany Farid outreach.** Single highest-leverage move identified. Specific technical question about limits of detection-based forensics in presence of hardware-rooted attestation. Not "will you advise us." Post-June-3.
2. **arXiv threat-model paper.** Title direction: "Capture-Path Attestation: Closing the Sensor-Injection Gap in Hardware-Rooted Provenance." ~40 hours. Compounds across SBIR Phase II scoring, cryptographer outreach credibility, and IP-priority establishment. The single writing project that pays the most dividends.
3. **Federal Public Defender / Innocence Project consultation.** Counterintuitive: the defense side creates the precedent that forces the prosecution side to buy. One successful 901(c) challenge on body-cam evidence and every AUSA in the country becomes a buyer overnight. Cost: low. Payoff potential: market-creating.
4. **Axon-competitor partnership pivot (Reveal Media / Getac / WatchGuard).** Be the deepfake-proof body cam Axon isn't. Smaller partner, larger share of value, faster decision cycle. Highest payoff and highest uncertainty — needs one focused research session before committing.
5. **Rule 707 / 901(c) supplemental comment and committee briefing offer.** Formal comment period closed Feb 16 but the May 7 committee meeting hasn't happened; a technically-grounded supplemental letter offering to brief the committee puts ZKNOT in the federal-rules conversation in a way no marketing can buy.

All five are in Taskwarrior with `due:2026-06-04` or later. Read the packet on the flight, fill the worksheet, then re-rank these based on what changes in my own understanding.

## Open questions I want to chew on

- **The sensor-injection question** for ZKNOT's current architecture. Specifically: at what point in the capture path does cryptographic binding to the physical sensor occur, and does an attacker with HDMI-to-CSI-2 bridge defeat it? This needs an honest sketch on paper before any cryptographer conversation. (See packet Unit 3.5 checklist.)
- **The right primary outreach order.** Farid is highest leverage but also highest stakes (one shot). Green is most technically forgiving but least courtroom-relevant. Schneier is most policy-relevant but slowest to respond. Pfefferkorn is the evidence-law expert but smallest reach. The packet's draft sequencing is Green → Schneier → Pfefferkorn + Farid, but I'm not sure that's right.
- **Whether PAT-001 needs a continuation-in-part to claim sensor-path attestation.** The chip-agnostic claim language is good for ZKKey Connect/Air but possibly too broad to defend the specific capture-path innovation that closes sensor injection. Worth a focused conversation with patent counsel.
- **Whether the EU AI Act August 2026 deadline creates a near-term sales window I'm underrating.** European law enforcement and journalism markets become non-compliant with current provenance practices in 65 days. ZKNOT-EU is not yet a thing, but maybe it should be.

## Next Actions

Pre-submission (this week, do not deviate):

```
task add "SBIR Phase I: Rule 707 / 901(c) framing revision pass" project:zknot.biz workstream:biz priority:H due:2026-05-30
task add "SBIR Phase I: add evidentiary-admissibility hook to Aim statement" project:zknot.biz workstream:biz priority:H due:2026-05-31
task add "SBIR Phase I: final review and submit" project:zknot.biz workstream:biz priority:H due:2026-06-03
```

Flight reading (between submission and after — packet is built):

```
task add "Read PUF/Evidence/Procurement reading packet on flight" project:zknot.ops workstream:ops priority:H due:2026-06-04
task add "Fill packet Unit 5 personal monopoly worksheet by hand" project:zknot.ops workstream:ops priority:H due:2026-06-04
task add "Self-rate Layer-5 stack questions from packet Unit 3.5" project:zknot.fw workstream:fw priority:H due:2026-06-05
```

Post-submission (week of June 4-10):

```
task add "Draft Hany Farid outreach email with specific technical question" project:zknot.biz workstream:biz priority:H due:2026-06-10
task add "Outline arXiv threat-model paper on capture-path attestation" project:zknot.fw workstream:fw priority:H due:2026-06-12
task add "Sketch sensor-injection threat model for current ZKNOT arch" project:zknot.fw workstream:fw priority:H due:2026-06-08
task add "Research Axon body-cam competitor landscape (Reveal/Getac/WatchGuard)" project:zknot.biz workstream:biz priority:M due:2026-06-15
task add "Review PAT-001 claim scope against Rule 707 / 901(c) framing" project:zknot.ip workstream:ip priority:M due:2026-06-20
```

Quarter:

```
task add "Write arXiv paper: Capture-Path Attestation" project:zknot.fw workstream:fw priority:M due:2026-07-15
task add "Draft Rule 707 supplemental comment + committee briefing offer" project:zknot.biz workstream:biz priority:M due:2026-07-01
task add "Identify three Federal Public Defender contacts for pro bono consultation" project:zknot.biz workstream:biz priority:M due:2026-07-30
task add "Draft Green / Schneier / Pfefferkorn outreach sequence" project:zknot.biz workstream:biz priority:M due:2026-06-25
```

## Pointers

- **Reading packet (durable):** `99_REFERENCE/ZKNOT_PUF_Evidence_Procurement_Reading_Packet.pdf` — drop into 99_REFERENCE folder; this is the flight reading.
- **KM systems reference (grep-able):** `3_OPS/km/systems/courtroom-evidence-and-attestation.md` — Federal Rules of Evidence primer, defense-layer stack, PUF taxonomy, sensor-injection threat model. Searchable from the vault.
- **Patent file to revisit:** PAT-001 (App #63/960,933) — chip-agnostic claims may need a CIP for sensor-path attestation.
- **Related journal entries to write on landing:** `2026-XX-XX_personal-monopoly-worksheet-synthesis.md` (after filling the worksheet), `2026-XX-XX_sensor-injection-threat-model-sketch.md` (after the architecture self-assessment).

## Backup / version control flag

This journal entry and the companion km doc are net-new files in the ZKNOT vault. Both should be committed to git before any further edits:

```
cd ~/ZKNOT
git add 3_OPS/journal/2026-05-29_puf-evidence-procurement-thesis.md
git add 3_OPS/km/systems/courtroom-evidence-and-attestation.md
git commit -m "journal+km: PUF/FRE/procurement personal monopoly thesis"
```

The reading packet PDF should also be committed (or moved to 99_REFERENCE, depending on vault convention):

```
mkdir -p 99_REFERENCE
cp ~/Downloads/ZKNOT_PUF_Evidence_Procurement_Reading_Packet.pdf 99_REFERENCE/
git add 99_REFERENCE/ZKNOT_PUF_Evidence_Procurement_Reading_Packet.pdf
git commit -m "ref: PUF/FRE/procurement reading packet v1"
```

## Concepts to internalize from this thread

For the "tick off as we progress" running list — terms or ideas that need to be in working memory:

- Federal Rule of Evidence 702 (Daubert / expert reliability)
- Federal Rule of Evidence 901 — particularly 901(b)(9) and proposed 901(c)
- Federal Rule of Evidence 902(13) and 902(14) — self-authentication of electronic records
- Proposed Federal Rule of Evidence 707 — machine-generated evidence Daubert gatekeeping
- Daubert reliability factors (testing, peer review, error rate, standards, acceptance)
- The "liar's dividend" (Citron & Chesney)
- Sensor-injection attack class (HDMI-to-CSI-2 bridge)
- C2PA Content Credentials standard
- Defense-layer stack: Layer 0 (metadata) → Layer 5 (PUF + sensor attestation)
- PUF taxonomy: SRAM, Ring Oscillator, Arbiter, Optical/Coating
- Rührmair ML-modeling attacks on Arbiter PUFs
- Microchip Trust&GO vs TFLXTLS provisioning paths
- SBIR Phase I → Phase II → Phase III sole-source authority
- SDVOSB set-aside contracting paths
- The three-vocabulary translation: cryptography ↔ evidence law ↔ federal procurement
- Personal monopoly as durable writing across the intersection
- The sensor-injection question as the architectural test for any "we use PUFs" claim
