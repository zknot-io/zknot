---
title: ZKKey Software Capability Decisions — v1 (Canonical)
doc_id: SIG-DEC-ZKKEY-001
status: CANONICAL for the v1 build window (~next few months)
author: William Shane Wilkinson (ZKNOT, INC.)
date: 2026-06-08
supersedes: none
companion: SIG-REQ-ZKKEY-001 (ZKKey Software & Firmware Capability Requirements)
governing_constraint: Cost is not a gate. Devices are built from the PCB up; provisions are
  designed into the board and populated when needed. Population is gated by firmware maturity
  and feature need, NOT by cost.
revisit_cadence: Re-read before any hardware purchase; formally revisit at v1 bring-up review.
classification: ZKNOT INTERNAL — patent-sensitive (see §8)
sources_of_truth: filed ZKNOT provisionals PAT-001/004/005/006/007/008/009/010/011/018
---

# ZKKey Software Capability Decisions — v1 (Canonical)

## TL;DR — How to use this document

These are the decisions that are **fixed for the v1 build**. Each is recorded ADR-style: the context, both sides, the determination, the consequences, and — most importantly for future-you — the **revisit trigger** that says what would justify reopening it. If you ever change a decision, change it *here*, bump the version, and note why in §9.

The new governing constraint (cost is not a gate; build into the board, populate when needed) is itself recorded as **D-0**, because it changes how every other decision resolves.

**Decisions at a glance:**

| ID | Decision | v1 determination |
|----|----------|------------------|
| **D-0** | Provisioning philosophy | Design the maximum into the PCB; gate population by firmware maturity / feature need, not cost |
| **D-2** | Human-presence gate | **Hardware-enforced**, strong form (software-unfakeable). Non-negotiable. |
| **D-1** | Secure-element count | **Board: dual-SE topology.** v1 target: dual populated. Bring-up path: single → dual. |
| **D-3** | Display vs LED | **Board carries display path.** Bring up LED-first, add display before flagship firmware ships. |
| **D-4** | Replay protection | **Stateful** rolling consumed-challenge log (default), counter as always-on floor. |
| **D-5** | Manufacturing ledger | **Reserve + genesis self-sign in v1**; build customer-receipt/lifecycle flow when a solicitation requires it. |

**Decision dependency order:** D-0 governs all → **D-2 before D-1** (gate model filters the SE shortlist) → D-1/D-4/D-5 share the storage and slot design → the record format (companion doc, R-10) is the constant that lets v1 grow without a respin.

---

## D-0 — Provisioning philosophy: design-in vs populate

**Status:** Canonical · governs D-1…D-5

**Context.** Cost is not a constraint and devices are fabricated from the PCB up. That removes the usual "include it or not" tension and replaces it with a cleaner one: what gets *designed into the board* (footprints, buses, select/isolation lines, routing, power domains) versus what gets *populated and brought up in firmware* for v1.

**Determination.** Design the full forward-compatible envelope into the PCB — every footprint and trace a future ZKKey version could need (second SE, display, optical paths, storage, tamper provisions, firmware-hash measurement). Gate **population and firmware** by two things only: (1) firmware/bring-up maturity, and (2) whether a feature is actually needed yet. Never gate the *board design* by cost.

**Consequences.**
- One PCB respin is far more expensive (in time and risk) than over-providing footprints. Over-provide.
- "Reserve for later" in the companion requirements doc now means **lay it out on the board now, populate when ready** — not "leave it off the schematic."
- The only legitimate reasons to *not* populate something in v1 become: the firmware to drive it isn't proven yet, or the feature isn't needed yet (and may be patent-gated — see §8).

**Revisit trigger.** Only if you move from build-from-PCB to off-the-shelf modules/dev-boards, at which point footprint headroom stops being free.

---

## D-2 — Human-presence gate: hardware-enforced (strong form)

**Status:** Canonical · **decide before D-1**

**Context.** The product thesis is "a human physically authorized this, and software cannot fake it." The gate is the mechanism behind that promise.

| Option | Pros | Cons |
|--------|------|------|
| Software-detected (MCU reads button, includes state in signed data) | Simple; works with almost any SE | A compromised MCU can lie about the press → the core guarantee becomes marketing |
| **Hardware-enforced (strong form)** — the actuation physically conditions the SE's signing operation; the MCU can *observe* the pressed state but cannot *assert* it | Software-unfakeable human presence; practices PAT-011 §3.2–4.3 / PAT-006 §5.2A; required for the Signing-SE role in the Ultra | Hard filter on SE selection; fussier board routing; a naive "button→MCU→sign command" silently degrades to software-detected |

**Determination.** **Hardware-enforced, strong form.** "Strong form" is defined precisely so it can't quietly degrade: the *physical state* of the actuation must be a precondition the signing element checks, not merely a flag the MCU sets. The actuation line is electrically an **input** to the MCU (observe, not drive). A topology where the SE only gates a key behind a second-key auth handshake that firmware triggers is **insufficient** unless the firmware trigger itself is bound to the physical line.

**Consequences.** This filters the secure-element shortlist hardest of any decision — resolve it before choosing SEs (D-1). If no acceptable part exists at any price/quantity, that is a finding to surface, not a reason to weaken the requirement.

**Revisit trigger.** Only a hardware-level discovery that the strong form is physically unachievable with available silicon — in which case escalate, don't silently downgrade.

---

## D-1 — Secure-element count: design dual, bring up incrementally

**Status:** Canonical (governed by D-0, depends on D-2)

**Context.** A single SE makes a single compromise a *full* forgery (impersonate the device **and** forge events). PAT-011 exists to split those domains so neither single compromise yields a complete forgery.

| Option | Pros | Cons |
|--------|------|------|
| Single SE | Simplest firmware (one bus, no domain router, no isolation) — fastest first bring-up | One compromise = full forgery; doesn't practice the Ultra differentiator |
| **Dual SE** | Compromise of one SE yields only half a forgery; practices PAT-011; Ultra story real immediately | Domain-router firmware, dual bus/select, power-domain isolation, button→Signing-SE trace — adds bring-up/debug risk |

**Determination.** Under D-0, cost no longer argues for single. **Lay out the dual-SE topology on the board** (two SE footprints, independent buses or multiplexed bus with hardware select, ground-plane separation, the actuation trace routed to the Signing SE per D-2, separate power-domain filtering). The remaining honest tension is *firmware bring-up risk*, not cost. So:
- **v1 target end-state:** dual-SE populated (Identity SE + Signing SE), Ultra-grade from the start.
- **Bring-up path:** populate a single SE first and run the firmware domain-router pointing both logical roles at it, to isolate FSM/SE/gate faults cheaply; then fit the second SE and prove bidirectional separation. Both footprints and all routing are present from the first board.

This relies on the companion doc's **R-10 two-component record** + **F-03 role separation** being implemented from day one, so the verifier never changes whether one or two SEs are populated.

**Consequences.** Identity-vs-signing must be separate logical roles / key slots even during single-SE bring-up. The domain router is v1 firmware work regardless. Plan bring-up in two stages.

**Revisit trigger.** If the domain router proves unstable enough to threaten the v1 schedule, ship single-SE-populated v1 (board unchanged) and fit the second SE in a populate-only follow-up. The record format makes this invisible to verifiers.

---

## D-3 — Display vs LED: board carries the display path, bring up LED-first

**Status:** Canonical (governed by D-0)

**Context.** Display-then-confirm (see the hash you're signing) and the human-readable short code (PAT-010) are the reason the flagship is more than a signing dongle. The Air variant needs a display to render a QR output (PAT-009) regardless.

| Option | Pros | Cons |
|--------|------|------|
| LED-only | Smallest, simplest; keeps display-then-confirm out of the build entirely (patent-safe for any free/open tier) | No display-then-confirm moat; no short-code UX; can't do optical-out |
| **Display on the board** | Unlocks the moat + the read-aloud/write-in-log workflow the patents target; needed for Air QR-out | Patent-sensitive surface (§8); more firmware |

**Determination.** Under D-0, **design the display path into the board** (display footprint + bus + the FSM "present-representation" hook, companion F-04/F-07). Bring up **LED-first** to de-risk the FSM, SE, and gate without display firmware in the loop, then enable the display before any flagship/display-then-confirm firmware ships. This is sequencing, not waffling — the board is display-capable from board one.

**Consequences.** The LED indicator stays as the always-present status layer (FSM-state signalling) even after the display is added. The display's *content* spec (how many short-code chars, whether it must render a QR for Air) is a hardware-decider input — see §7-D.

**Revisit trigger.** None expected for the board. The *firmware/content* exposure of display-then-confirm is gated by patent timing (§8), not by this decision.

---

## D-4 — Replay protection: stateful log + counter floor

**Status:** Canonical (governed by D-0)

**Context.** The seized-device / colluding-host threat model wants the device itself to refuse to re-sign a challenge it has already seen, without trusting the host.

| Option | Pros | Cons |
|--------|------|------|
| Stateless (counter only) | Simplest | Replay protection leans on host behaviour + verifiers actually checking counter monotonicity |
| **Stateful rolling consumed-challenge log** | True single-use enforcement on-device, host-independent (PAT-008 §4.3, PAT-009 §4.2) | Needs durable storage + wear + power-loss-safe append; the log is a *rolling window* with a horizon |

**Determination.** With storage designed into the board (D-0), the storage cost argument disappears. **Implement the stateful rolling consumed-challenge log as the default**, with the **monotonic counter (companion CAP-02) as the always-on floor** it sits on top of. Close the rolling-window horizon by pairing each record with a timestamp/counter staleness check, so an ancient re-presented challenge is rejected on freshness even if it has aged out of the log window.

**Consequences.** Requires a durable, append-only, wear-leveled, power-loss-safe storage subsystem — **the same subsystem D-5's ledger needs.** Design it once. Sizing is a hardware-decider input — see §7-B.

**Revisit trigger.** Only if the chosen storage part can't meet power-loss-safe append at the needed depth; counter-only is then the documented fallback for the base tier.

---

## D-5 — Manufacturing ledger: reserve + genesis self-sign now

**Status:** Canonical (governed by D-0)

**Context.** PAT-005 vendor-irrevocability ("the customer holds the proof") is a real federal/SDVOSB procurement differentiator. But the *full* flow is a **system** feature — it needs customer-receipt signing and customer-side verification tooling, not just device firmware. That dependency, not cost, is the reason to stage it.

| Option | Pros | Cons |
|--------|------|------|
| Full ledger flow in v1 | Strongest irrevocability story, demonstrable immediately | Requires external customer-side tooling; base tier never exercises it; pulls scope into v1 that isn't device-resident |
| **Reserve + genesis self-sign** | Genesis self-sign proves on-device key origin (valuable alone); ledger storage already on the board via D-4; "turn it on" later | Irrevocability story not *demonstrable* until the receipt/lifecycle flow is built |

**Determination.** **Require two things in v1:** (1) the secure element must emit a **genesis self-signature at provisioning** (companion CAP-03 — proves the keypair was generated on-device), and (2) **reserve the device-resident, hash-chained ledger storage** (already provided by D-4's storage subsystem). **Defer** the customer-receipt and lifecycle-append firmware until an actual solicitation requires supply-chain attestation — that requirement is the trigger.

**Consequences.** Genesis self-sign moves from "nice" to "must" — confirm the candidate SE supports signing an attestation at/around its own keygen. Ledger storage is free-riding on D-4.

**Revisit trigger.** A federal solicitation that requires demonstrable manufacturing provenance → build the receipt/lifecycle flow and the customer verification tool.

---

## 6. The through-line

Four of five decisions land on the same posture: **lay the full capability into the board now, populate/enable when firmware is ready or the feature is needed.** The one exception is D-2 (the hardware gate), which is populated and proven in v1 from the start — deliberately, because the gate is not a future feature, it is the irreducible core of what the device *is*. Clean v1 stance: **one thing done fully (software-unfakeable human presence), everything else designed-in and staged.**

---

## 7. What the hardware decider still needs from you

The companion capability checklist says *what kinds* of parts. To actually shortlist silicon, the decider needs these **parameters**. Each is tagged:
**[DECIDE]** needs your call · **[DEFAULT]** I've proposed a value from your patents/infrastructure — confirm or override · **[SPEC]** I can draft it once the DECIDE items are set.

### 7-A · Signing element (drives SE selection — gated by D-2)
| Item | Tag | Notes |
|------|-----|-------|
| Native signature scheme + curve for v1 | **[DEFAULT]** ECDSA **P-256** for v1 device signing; `algorithm_id` (companion R-03) reserves migration. NOTE: Ed25519 is *not* in the FIPS-approved set per your cert notes — keep it out of any identity root that a federal sibling would inherit. P-384 is the long-lived *issuing-root* curve (that lives in the external HSM, not the device). | confirm P-256 for device |
| Auth-gate mechanism (the D-2 strong form) | **[SPEC]** Define as: signing op conditioned on a physical actuation line the MCU cannot drive. Decider must verify candidate SE datasheets actually support this, not a firmware-triggered handshake. | hard SE filter |
| Key-slot map (per SE) | **[SPEC]** Identity SE: cert-bound slot(s), cannot sign arbitrary event data. Signing SE: event-signing slot, auth-required, counter-linked. | flows from D-1 |
| Genesis self-sign at keygen | **[SPEC]** Required by D-5. Confirm candidate SE can sign an attestation referencing its own key generation. | hard SE filter |
| Monotonic counter(s) | **[SPEC]** Count needed, monotonicity guarantee, rollover behaviour, persistence across power loss. | companion CAP-02 |
| External cert ingestion | **[DEFAULT]** Device Identity slot must accept and store a CA-signed device certificate issued by your **external HSM root** (your two-tier model: HSM holds root/attestation authority, device SEs are field identities under it). | confirm root model |

### 7-B · Storage (drives storage part + partitioning — shared by D-4 and D-5)
| Item | Tag | Notes |
|------|-----|-------|
| Record size estimate | **[SPEC]** Sizes everything below; depends on the finalized record format. | from companion R-format |
| Consumed-challenge log depth | **[DECIDE]** How many recent challenges to retain (sets the rolling-window horizon). | your call on threat window |
| Ledger entry budget | **[DEFAULT]** Reserve for a few hundred lifecycle entries — generous given D-0. | confirm |
| Durability requirements | **[SPEC]** Append-only, wear-leveled, power-loss-safe write. | hard storage filter |

### 7-C · Challenge & artifact data budget (drives MCU RAM + optical/display)
| Item | Tag | Notes |
|------|-----|-------|
| Challenge max size + accepted formats | **[DECIDE]** e.g. raw 32-byte hash only, or structured records up to N bytes (sets canonical-validation bounds + buffer). | your call |
| Artifact size vs optical-out | **[SPEC]** Hard cross-constraint: if Air/optical-out is reserved, the artifact must fit a renderable, scannable 2D code. This pressures the record format to stay compact. | affects R-format |

### 7-D · Human interface (drives indicator + display selection)
| Item | Tag | Notes |
|------|-----|-------|
| Indicator state map | **[SPEC]** LED count/colours mapped to FSM states (READY/SIGNING/ERROR/etc.). | from companion FSM |
| Display content spec | **[DECIDE]** Short-code char count to show; must it render a QR (needed for Air)? | your call |
| Display technology bias | **[DEFAULT]** Lean e-ink for Air/air-gapped/low-power persistence; OLED acceptable for tethered Connect. (Cost-free, so decide on *use context*, not price.) | confirm per variant |

### 7-E · Transport / power / form factor (drives MCU + power + connectors)
| Item | Tag | Notes |
|------|-----|-------|
| v1 transport | **[DEFAULT]** USB for the Connect variant (`ZK-K`); the Air variant (`ZK-A`) reserves the optical path. | confirm v1 = Connect |
| SE bus | **[DECIDE]** I2C vs SPI to the secure element(s). | your call / part-driven |
| Power model | **[DEFAULT]** v1 Connect = USB-tethered. Battery/multi-day (PAT-006) belongs to the field/Offline variant, not v1 Connect. | confirm |
| Form factor / enclosure | **[DECIDE]** Sets tamper-provision headroom (PAT-018) you may want designed into the board now under D-0. | your call |

### 7-F · Trust / provisioning / certification (drives SE eligibility + workflow)
| Item | Tag | Notes |
|------|-----|-------|
| Root-of-trust model | **[DEFAULT]** External HSM root signs device certs; device holds the cert in the Identity slot. | confirm |
| Certification intent | **[DEFAULT]** v1 = civilian, **non-FIPS** (FIPS deferred to a separate federal line). Don't over-constrain to FIPS SE SKUs now — but don't pick a part that *blocks* a future FIPS sibling. **Do not claim FIPS anywhere without checking live NIST CMVP** (your 140-2 cert sunset 2026-05-02; 140-3 pending). | confirm |
| Secure / measured boot | **[DEFAULT]** Pick an MCU that *supports* measured boot so the reserved `firmware_hash` (companion R-11) is meaningful when enabled later. | confirm |
| Post-quantum headroom | **[SPEC]** PQ schemes (ML-DSA/SLH-DSA) may not fit a small SE — keep the signing abstraction able to host an MCU-side or co-processor signer later. Don't pick an MCU with no room to grow that path. | future-proofing |

**The four that genuinely need your call before a decider can start:** challenge max size + formats (7-C), consumed-challenge log depth (7-B), display content spec incl. QR-or-not (7-D), and v1 form factor (7-E). Everything else has a defensible default above.

---

## 8. Patent-sensitivity & federal flags (carried forward)

- **Display-then-confirm (D-3 / companion F-07) and dual-SE separation (D-1 / PAT-011) are the moat.** Documenting them here (internal) is fine. Keeping the display-then-confirm *firmware and any public/free-build content or video narration* out of circulation until the non-provisional is filed is the discipline. The LED-only status layer is the safe-to-open part.
- **Sequencing anchor:** PAT-001 (App 63/960,933) non-provisional deadline **2027-01-15**; attorney engagement target on your calendar precedes public exposure of the moat features.
- **Federal caution:** if any naming, FIPS status, or provisioning terminology here flows into a capability statement, proposal, or government-facing artifact, re-verify against primary sources (USPTO Patent Center; live NIST CMVP for FIPS) before use. Do not propagate from this doc.

---

## 9. Changelog / revisit log

| Version | Date | Change | Reason |
|---------|------|--------|--------|
| v1 | 2026-06-08 | Initial canonical set (D-0…D-5) | v1 build window opened; cost-no-gate constraint adopted |

*When you change a decision: edit the determination in place, add a row here, and bump the version. This is the record future-you comes back to.*

---

*Provenance: every decision traces to a filed ZKNOT provisional and to the companion requirements doc SIG-REQ-ZKKEY-001. No capability is invented beyond those claims. Hardware part numbers are intentionally excluded; §7 lists the parameters a hardware decider needs to convert these decisions into a silicon shortlist.*
